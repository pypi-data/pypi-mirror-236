import tempfile
import pytest

SAMPLE_JSON = '{"obj": {"json": "yes", "foo": "bar", "spam": "eggs", "a_list": [1,2,3]}}'
SAMPLE_YAML = """\
obj:
  yaml: yes
  foo: bar
  spam: eggs
  a_list:
    - 1
    - 2
    - 3
"""

import clamg


def test_load_json_file_as_str():
    tf = tempfile.mktemp(prefix="pytest.clamg_", suffix=".json")
    tfp = open(tf, "w")
    tfp.write(SAMPLE_JSON)
    tfp.close()
    x = clamg.load(tf, _json=True)
    assert x.obj.json

def test_load_yaml_file_as_str():
    tf = tempfile.mktemp(prefix="pytest.clamg_", suffix=".yaml")
    tfp = open(tf, "w")
    tfp.write(SAMPLE_YAML)
    tfp.close()
    x = clamg.load(tf, _yaml=True)
    assert x.obj.yaml

def test_loads_json():
    x = clamg.loads(SAMPLE_JSON, _yaml=False, _json=True)
    assert x.obj.json

def test_loads_yaml():
    x = clamg.loads(SAMPLE_YAML)
    assert x.obj.yaml

def test_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        _ = clamg.load(tempfile.mktemp(prefix="pytest.clamg_", suffix=".yaml"))
