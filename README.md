Emmet for Vim, implemented with UltiSnips. [![CircleCI](https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips.svg?style=svg)](https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips)

Before using this plugin, make sure you have:

* [UltiSnips](https://github.com/SirVer/ultisnips) (`Plug 'SirVer/ultisnips'`)
* python 3.7 or higher (`python3 --version`)

The snippets are enabled by default in HTML files. To use it in Vue files for
example, put the following in your `UltiSnips/vue.snippets`:

```
extends html
```

## Supported syntax

Currently, only a small subset of Emmet's features are supported, though it is
sufficient for what I need.

| name    | example            |
| ---     | ---                |
| element | `div`, `p`         |
| class   | `.foo`, `.foo.bar` |
| id      | `#foobar`          |
| repeat  | `div*3`            |

## Alternatives

* [mattn/emmet-vim](https://github.com/mattn/emmet-vim)
* [jceb/emmet.snippets](https://github.com/jceb/emmet.snippets)

Both of these didn't work the way I wanted. I wanted it to simply work by
writing an Emmet abbreviation and pressing `<Tab>`, while also still having
`<Tab>` mapped to trigger a snippet.
