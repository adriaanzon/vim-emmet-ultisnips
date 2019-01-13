Emmet for Vim, implemented with UltiSnips. [![CircleCI](https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips.svg?style=svg)](https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips)

## Installation

Requires Python 3.4 or higher (`:python3 print(sys.version)`) and
[UltiSnips](https://github.com/SirVer/ultisnips).

Install via e.g. vim-plug:

```vim
Plug 'adriaanzon/vim-emmet-ultisnips'
Plug 'SirVer/ultisnips'
```

### Configuration

The snippets are enabled by default in HTML files. To use it in Vue files for
example, put the following in your `UltiSnips/vue.snippets`:

```
extends html
```

## Supported syntax

| name    | example            |
| ---     | ---                |
| element | `div`, `p`         |
| class   | `.foo`, `.foo.bar` |
| id      | `#foobar`          |
| child   | `ul>li`            |
| repeat  | `div*3`            |

## Alternatives

* [mattn/emmet-vim](https://github.com/mattn/emmet-vim)
* [jceb/emmet.snippets](https://github.com/jceb/emmet.snippets)

Both of these didn't work the way I wanted. I wanted it to simply work by
writing an Emmet abbreviation and pressing `<Tab>`, while also still having
`<Tab>` mapped to trigger a snippet.
