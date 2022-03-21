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

import pytest
import uuid
from whub import WorkflowHub

BASE_URL = "https://dev.workflowhub.eu"
PROJECT = "Testing"


@pytest.fixture(scope="module")
def client():
    with WorkflowHub(base_url=BASE_URL) as c:
        yield c


def test_resolve_project(client):
    id_ = client.resolve_project(PROJECT)
    assert id_ is not None


def test_resolve_project_not_found(client):
    id_ = client.resolve_project(str(uuid.uuid4()))
    assert id_ is None


def test_resolve_workflow_not_found(client):
    p_id_ = client.resolve_project(PROJECT)
    id_ = client.resolve_workflow(p_id_, str(uuid.uuid4()))
    assert id_ is None
