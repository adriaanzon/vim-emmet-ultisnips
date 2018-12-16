Emmet for Vim, implemented with UltiSnips.

Before using this plugin, make sure you have:

* [UltiSnips](https://github.com/SirVer/ultisnips) 
* a recent version of python 3

The snippets are enabled by default in html files. To use it in e.g. `.vue`
files, put the following in `UltiSnips/vue.snippets`:

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

## Alternatives

* [mattn/emmet-vim](https://github.com/mattn/emmet-vim)
* [jceb/emmet.snippets](https://github.com/jceb/emmet.snippets)

Both of these didn't work the way I wanted. I wanted it to simply work by
writing an Emmet abbreviation and pressing `<Tab>`, while also still having
`<Tab>` mapped to trigger a snippet.
