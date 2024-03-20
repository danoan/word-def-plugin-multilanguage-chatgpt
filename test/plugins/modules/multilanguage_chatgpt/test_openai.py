from danoan.word_def.plugins.modules import multilanguage_chatgpt as mlc

import io
import pytest
import toml
import warnings


@pytest.fixture(scope="session")
def openai_key(pytestconfig):
    v = pytestconfig.getoption("openai_key")
    if v is None:
        warnings.warn("The openai_key is not specified. Tests won't be executed.")
    return pytestconfig.getoption("openai_key", skip=True)


@pytest.mark.api
@pytest.mark.parametrize(
    "method_name,word",
    [
        ("get_definition", "microphone"),
        ("get_synonym", "reliable"),
        ("get_pos_tag", "minister"),
        ("get_usage_example", "thoughtful"),
    ],
)
def test_integration_test(openai_key: str, method_name: str, word: str):
    factory = mlc.AdapterFactory()

    def get_language():
        return "eng"

    factory.__setattr__("get_language", get_language)

    ss = io.StringIO()
    config = {"openai_key": openai_key}
    toml.dump(config, ss)
    ss.seek(io.SEEK_SET)

    adapter = factory.get_adapter(ss)
    response = adapter.__getattribute__(method_name)(word)

    assert response
    assert len(response) > 0
