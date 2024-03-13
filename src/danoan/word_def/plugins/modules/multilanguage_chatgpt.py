from danoan.word_def.core import exception, model

from danoan.word_guru import core as WG 

from dataclasses import dataclass 
import importlib
import json
import toml
from typing import Optional, Sequence, TextIO

@dataclass 
class Configuration:
    openai_key: str 

class Adapter:
    def __init__(self, configuration:Configuration, language: str):
        self.configuration = configuration 
        self.language = language
        
    def get_definition(self, word: str) -> Sequence[str]:
        try:
            return json.loads(WG.api.get_definition(self.configuration.openai_key, word, self.language))
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(404,"OpenAI returned nothing.") from ex  

    def get_pos_tag(self, word: str) -> Sequence[str]: 
        try:
            return json.loads(WG.api.get_pos_tag(self.configuration.openai_key, word, self.language))
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(404,"OpenAI returned nothing.") from ex  

    def get_synonyme(self, word: str) -> Sequence[str]:
        try:
            return json.loads(WG.api.get_synonyme(self.configuration.openai_key, word, self.language))
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(404,"OpenAI returned nothing.") from ex  

    def get_usage_example(self, word: str) -> Sequence[str]:
        try:
            return json.loads(WG.api.get_usage_examples(self.configuration.openai_key, word, self.language))
        except WG.exception.OpenAIEmptyResponse as ex:
            raise WG.exception.UnexpectedResponseError(404,"OpenAI returned nothing.") from ex  



class AdapterFactory:
    def version(self) -> str:
        return importlib.metadata.version("word-def-plugin-multilanguage-chatgpt")

    def get_language(self) -> str:
        return ""

    def get_adapter(self, configuration_stream: Optional[TextIO]) -> model.PluginProtocol:
        if not configuration_stream:
            raise exception.ConfigurationFileRequiredError()

        config = Configuration(**toml.load(configuration_stream))
        return Adapter(config,self.get_language())

