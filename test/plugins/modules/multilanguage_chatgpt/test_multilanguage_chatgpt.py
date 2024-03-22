from danoan.word_def.plugins.modules import multilanguage_chatgpt as mlc

from danoan.word_def.core import api, exception
import io
import toml
import json
from pathlib import Path
import pytest

SCRIPT_FOLDER = Path(__file__).parent


def test_language():
    af = mlc.AdapterFactory()
    assert af.get_language() == ""


def test_adapter_no_config_file_error():
    af = mlc.AdapterFactory()

    with pytest.raises(exception.ConfigurationFileRequiredError) as e:
        af.get_adapter()
        assert e.type == exception.ConfigurationFileRequiredError


def test_plugin_compatibility():
    assert api.is_plugin_compatible(mlc.AdapterFactory())


@pytest.mark.parametrize(
    "input_filepath,method_name",
    [
        (SCRIPT_FOLDER / "input" / "get-definition.json", "get_definition"),
        (SCRIPT_FOLDER / "input" / "get-synonym.json", "get_synonym"),
        (SCRIPT_FOLDER / "input" / "get-pos-tag.json", "get_pos_tag"),
        (
            SCRIPT_FOLDER / "input" / "get-usage-example.json",
            "get_usage_example",
        ),
    ],
)
def test_get_definition(monkeypatch, input_filepath: Path, method_name: str):
    factory = mlc.AdapterFactory()

    def mock_api_call(self, word: str):
        with open(input_filepath) as f:
            api_mock_response = json.load(f)
            return json.dumps(api_mock_response)

    monkeypatch.setattr(mlc.Adapter, f"_{method_name}_api", mock_api_call)

    config_toml = {"openai_key": ""}
    ss = io.StringIO()
    toml.dump(config_toml, ss)
    ss.seek(io.SEEK_SET)

    adapter = factory.get_adapter(ss)
    adapter_response = adapter.__getattribute__(method_name)("dontcare")
    assert len(adapter_response) > 0
