# Copyright (c) 2022 CRS4
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

import os
import shutil
import uuid
from pathlib import Path

import pytest

PROJECT = "Testing"
THIS_DIR = Path(__file__).absolute().parent


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


@pytest.mark.skipif(not os.getenv("WHUB_API_KEY"), reason="requires API key")
def test_upload_crate(client, tmpdir):
    crate_dir = THIS_DIR / "data" / "sort-and-change-case"
    crate_zip = tmpdir / "{crate_dir.name}.crate"
    crate = shutil.make_archive(crate_zip, "zip", crate_dir)
    p_id_ = client.resolve_project(PROJECT)
    data = client.upload_crate(crate, p_id_)
    wf_id = data["id"]
    new_name = str(uuid.uuid4())
    client.update_workflow_name(wf_id, new_name)
    id_ = client.resolve_workflow(p_id_, new_name)
    assert id_ == wf_id
    data = client.get(f"workflows/{id_}")
    assert data["attributes"]["title"] == new_name
    client.delete(f"workflows/{id_}")
