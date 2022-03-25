# Copyright (c) 2021-2022 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""\
Provides a client for interacting with the WorkflowHub API.

WorkflowHub (https://workflowhub.eu) is a computational workflow registry.
"""

import os
import requests
from .version import VERSION

__version__ = VERSION


class JsonApiClient:

    API_HEADERS = {}

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"authorization": f"Token {api_key}"})

    def disconnect(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()

    def request(self, method, endpoint, payload=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs = {}
        if self.API_HEADERS:
            kwargs["headers"] = self.API_HEADERS
        if payload:
            kwargs["json"] = payload
        r = self.session.request(method, url, **kwargs)
        r.raise_for_status()
        return r.json()

    def get(self, endpoint, payload=None):
        return self.request("GET", endpoint, payload=payload)

    def post(self, endpoint, payload=None):
        return self.request("POST", endpoint, payload=payload)

    def put(self, endpoint, payload=None):
        return self.request("PUT", endpoint, payload=payload)

    def patch(self, endpoint, payload=None):
        return self.request("PATCH", endpoint, payload=payload)

    def delete(self, endpoint, payload=None):
        return self.request("DELETE", endpoint, payload=payload)


class WorkflowHub(JsonApiClient):

    BASE_URL = "https://workflowhub.eu"
    API_HEADERS = {
        "Content-type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Accept-Charset": "ISO-8859-1",
    }

    def __init__(self, base_url=BASE_URL, api_key=None):
        if not api_key:
            api_key = os.getenv("WHUB_API_KEY")
        super().__init__(base_url, api_key=api_key)
        self._wf_id_to_name = {}
        self._project_map = {}
        self._wf_maps = {}

    def reset(self):
        for d in self._wf_id_to_name, self._project_map, self._wf_maps:
            d.clear()

    def request(self, method, endpoint, payload=None):
        response = super().request(method, endpoint, payload=payload)
        return response.get("data")

    def resolve_project(self, name):
        if not self._project_map:
            for p in self.get("/projects"):
                self._project_map[p["attributes"]["title"]] = p["id"]
        return self._project_map.get(name)

    def resolve_workflow(self, proj_id, wf_name):
        try:
            m = self._wf_maps[proj_id]
        except KeyError:
            if not self._wf_id_to_name:
                for w in self.get("/workflows"):
                    self._wf_id_to_name[w["id"]] = w["attributes"]["title"]
            data = self.get(f"/projects/{proj_id}")
            wf_ids = [_["id"] for _ in data["relationships"]["workflows"]["data"]]
            self._wf_maps[proj_id] = m = {self._wf_id_to_name.get(_): _ for _ in wf_ids}
            m.pop(None, None)  # from workflows not visible to user
        return m.get(wf_name)

    def upload_crate(self, filename, proj_id, wf_id=None):
        endpoint = f"{self.base_url}/workflows"
        if wf_id:
            endpoint = f"{endpoint}/{wf_id}/create_version"
        with open(filename, "rb") as f:
            payload = {
                "ro_crate": (os.path.basename(filename), f),
                "workflow[project_ids][]": (None, proj_id)
            }
            r = self.session.post(endpoint, files=payload)
        r.raise_for_status()
        return r.json()["data"]

    def update_workflow_name(self, wf_id, new_name):
        payload = {
            "data": {
                "id": wf_id,
                "type": "workflows",
                "attributes": {
                    "title": new_name
                }
            }
        }
        return self.patch(f"/workflows/{wf_id}", payload=payload)
