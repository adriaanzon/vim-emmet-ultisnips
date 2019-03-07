<p align="center">Emmet for Vim, implemented with UltiSnips.</p>

<p align="center">
<a href="https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips"><img src="https://circleci.com/gh/adriaanzon/vim-emmet-ultisnips.svg?style=svg" alt="CircleCI" /></a>
</p>

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

| name              | example            |
| ---               | ---                |
| [element]         | `div`, `p`         |
| [class][id-class] | `.foo`, `.foo.bar` |
| [id][id-class]    | `#foobar`          |
| [child]           | `ul>li`            |
| [sibling]         | `div+p`            |
| [repeat]          | `div*3`            |
| [text]            | `a{Click me}`      |

[element]: https://docs.emmet.io/abbreviations/syntax/#elements
[id-class]: https://docs.emmet.io/abbreviations/syntax/#id-and-class
[child]: https://docs.emmet.io/abbreviations/syntax/#child-gt
[sibling]: https://docs.emmet.io/abbreviations/syntax/#sibling
[repeat]: https://docs.emmet.io/abbreviations/syntax/#multiplication
[text]: https://docs.emmet.io/abbreviations/syntax/#text

## Alternatives

* [mattn/emmet-vim](https://github.com/mattn/emmet-vim)
* [jceb/emmet.snippets](https://github.com/jceb/emmet.snippets)

Both of these didn't work the way I wanted. I wanted it to simply work by
writing an Emmet abbreviation and pressing `<Tab>`, while also still having
`<Tab>` mapped to trigger a snippet.
