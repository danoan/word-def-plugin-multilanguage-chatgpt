from danoan.word_def.core import exception, model

from danoan.word_guru import core as WG

from dataclasses import dataclass
import importlib
import json
import toml
from typing import Any, Optional, Sequence, TextIO


@dataclass
class Configuration:
    openai_key: str


class Adapter:
    """
    Adapter class that communicates with the word-guru API.

    Each method is divided in two subtasks:
    - _[method_name]_api: Returns the raw api response.
    - _[method_name]_handle: Manipulate the response to return in the desired format.

    Dividing this way allows us to create tests with mock responses for the handle.
    """

    def __init__(self, configuration: Configuration, language: str):
        self.configuration = configuration
        self.language = language

    def _get_definition_api(self, word: str) -> str:
        return WG.api.get_definition(self.configuration.openai_key, word, self.language)

    def _get_definition_handle(self, response: str) -> Any:
        return json.loads(response)

    def get_definition(self, word: str) -> Sequence[str]:
        try:
            response = self._get_definition_api(word)
            return self._get_definition_handle(response)
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(
                404, "OpenAI returned nothing."
            ) from ex

    def _get_pos_tag_api(self, word: str) -> str:
        return WG.api.get_pos_tag(self.configuration.openai_key, word, self.language)

    def _get_pos_tag_handle(self, response: str) -> Any:
        return json.loads(response)

    def get_pos_tag(self, word: str) -> Sequence[str]:
        try:
            response = self._get_pos_tag_api(word)
            return self._get_pos_tag_handle(response)
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(
                404, "OpenAI returned nothing."
            ) from ex

    def _get_synonym_api(self, word: str) -> str:
        return WG.api.get_synonym(self.configuration.openai_key, word, self.language)

    def _get_synonym_handle(self, response: str) -> Any:
        return json.loads(response)

    def get_synonym(self, word: str) -> Sequence[str]:
        try:
            response = self._get_synonym_api(word)
            return self._get_synonym_handle(response)
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(
                404, "OpenAI returned nothing."
            ) from ex

    def _get_usage_example_api(self, word: str) -> str:
        return WG.api.get_usage_examples(
            self.configuration.openai_key, word, self.language
        )

    def _get_usage_example_handle(self, response: str) -> Any:
        return json.loads(response)

    def get_usage_example(self, word: str) -> Sequence[str]:
        try:
            response = self._get_usage_example_api(word)
            return self._get_usage_example_handle(response)
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(
                404, "OpenAI returned nothing."
            ) from ex


class AdapterFactory:
    def version(self) -> str:
        return importlib.metadata.version("word-def-plugin-multilanguage-chatgpt")

    def get_language(self) -> str:
        """
        Language which the plugin is configured to respond.

        Multilanguage plugins should return an empty string.
        The word-def api is responsible to create specific language versions
        upon request. You can rely on this methos to return the appropriated
        language code.
        """
        return ""

    def get_adapter(
        self, configuration_stream: Optional[TextIO] = None
    ) -> model.PluginProtocol:
        if not configuration_stream:
            raise exception.ConfigurationFileRequiredError()

        config = Configuration(**toml.load(configuration_stream))
        return Adapter(config, self.get_language())
