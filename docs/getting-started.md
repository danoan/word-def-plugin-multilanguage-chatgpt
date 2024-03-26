# Getting started with Multilanguage ChatGPT word-def plugin

Multilanguage plugin for word-def

## Installation

```bash
$ pipx install word-def-plugin-multilanguage-chatgpt
```

## Features

- Get word definition.
- Get word synonym.
- Get part-of-speech tags of a word.
- Get usage examples.

## Examples

```{admonition} word-def
You need to have the [word-def](https://github.com/danoan/word-def) package installed.
```

```bash
$ word-def --plugin-configuration-filepath plugin-config.toml get-definition joy eng
1. A feeling of great pleasure and happiness.
```

```bash
$ word-def --plugin-configuration-filepath plugin-config.toml get-synonym joy eng
1. happiness
2. delight
3. pleasure
4. bliss
5. euphoria
```

```bash
$ word-def --plugin-configuration-filepath plugin-config.toml get-pos-tags joy eng
1. noun.
2. verb.
```

```bash
$ word-def --plugin-configuration-filepath plugin-config.toml get-usage-examples joy eng
1. The children's laughter filled the room with joy and happiness.
2. She felt a sense of joy and contentment when she achieved her lifelong dream.
3. The music festival brought a lot of joy to the attendees.
4. Watching the sunset over the ocean always fills me with joy.
5. The birth of a baby is a moment of pure joy for the new parents.
```

```{admonition} Plugin configuration
   The [word-def documentation](https://danoan.github.io/word-def/how-to/setup-a-plugin.html)
   has more information about how to setup the plugin configuration file.
```

The list of parameters accepted by the plugin is the same as the members of the
dataclass [Configuration](https://danoan.github.io/word-def-plugin-multilanguage-chatgpt/reference/danoan.word_def.plugins.modules.multilanguage_chatgpt.html#module-danoan.word_def.plugins.modules.multilanguage_chatgpt).


## Contributing

Please reference to our [contribution](http://danoan.github.io/word-def-plugin-multilanguage-chatgpt/contributing) and [code-of-conduct](http://danoan.github.io/word-def-plugin-multilanguage-chatgpt/code-of-conduct) guidelines.
