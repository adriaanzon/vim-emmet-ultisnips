import vim

html_rendered_syntaxes = [
    "htmlStrike",
    "htmlBold",
    "htmlBoldUnderline",
    "htmlBoldItalic",
    "htmlBoldUnderlineItalic",
    "htmlBoldItalicUnderline",
    "htmlUnderline",
    "htmlUnderlineBold",
    "htmlUnderlineItalic",
    "htmlUnderlineItalicBold",
    "htmlUnderlineBoldItalic",
    "htmlItalic",
    "htmlItalicBold",
    "htmlItalicBoldUnderline",
    "htmlItalicUnderline",
    "htmlItalicUnderlineBold",
    "htmlLink",
    "htmlH1",
    "htmlH2",
    "htmlH3",
    "htmlH4",
    "htmlH5",
    "htmlH6",
    "htmlHead",
]


def should_expand_emmet():
    """
    Checks if the cursor is at the top level of a file, syntax-wise.
    """
    expr = "map(synstack(line('.'), col('.')), {_, id -> synIDattr(id, 'name')})"

    try:
        synstack = vim.api.eval(expr)
    except AttributeError:
        synstack = vim.eval(expr)

    return synstack == [] or (
        "htmlTag" not in synstack
        and any(syntax in synstack for syntax in html_rendered_syntaxes)
    )
