"""Submodule of pgparagraph responsible of parsing rich text strings using html parsing"""
from html import parser as _html_parser

from ._modifiers import ModifierName as _ModifierName
from ._modifiers import empty_modifiers as _empty_modifiers
from ._modifiers import ModifiersValue as _ModifiersValue
from ._modifiers import ModifierValue as _ModifierValue


class _RichTextParser(_html_parser.HTMLParser):
    """Internal rich text parser using the builtin html parser. Functions aren't be documented"""

    def __init__(self):
        super().__init__()
        self.reset_text("")

    def reset_text(self, raw_text: str):
        self.raw_text: str = raw_text
        self.output_text: str = ""
        self.modifiers: _ModifiersValue = _empty_modifiers()
        self.modifiers_stack: list[_ModifierValue] = []
        self.start_i_stack: list[int] = []

    def parse_text(self, raw_text: str) -> tuple[str | _ModifiersValue]:
        self.reset_text(raw_text)
        self.feed(self.raw_text)
        self.close()
        return self.output_text, self.modifiers

    def handle_data(self, data: str) -> None:
        self.output_text += data

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.modifiers_stack.append([tag, attrs])
        self.start_i_stack.append(len(self.output_text))

    def handle_endtag(self, tag: str) -> None:
        modifier = self.modifiers_stack[-1]
        start_i = self.start_i_stack[-1]
        end_i = len(self.output_text)-1

        self.parse_modifier(modifier, start_i, end_i)

        self.modifiers_stack.pop()
        self.start_i_stack.pop()

    def parse_modifier(self, mod: tuple[str, tuple[str, str]], start_i: int, end_i: int):
        tag_name = mod[0]
        tagmod = tag_name.lower().strip()
        match tagmod:
            case "i" | "italic":
                self.modifiers[_ModifierName.italic].append(
                    [start_i, end_i, True])
            case "b" | "bold":
                self.modifiers[_ModifierName.bold].append(
                    [start_i, end_i, True])
            case "u" | "underline":
                self.modifiers[_ModifierName.underline].append(
                    [start_i, end_i, True])
            case "s" | "strike" | "strikethrough":
                self.modifiers[_ModifierName.strikethrough].append(
                    [start_i, end_i, True])
            case "a" | "antialasing" | "antialas":
                self.modifiers[_ModifierName.antialiasing].append(
                    [start_i, end_i, True])
            case "m" | "mod" | "modifier":
                for attr, value in mod[1]:
                    attrmod = attr.lower().strip()
                    match attrmod:
                        case "color" | "fg-color" | "fg_color" | "fgcolor" | "col" | "c":
                            self.modifiers[_ModifierName.fg_color].append(
                                [start_i, end_i, eval(value)])
                        case "bg-color" | "bg_color" | "bgcolor" | "bgcol" | "bg-col" | "bg_col" | "bgc":
                            self.modifiers[_ModifierName.bg_color].append(
                                [start_i, end_i, eval(value)])
                        case "font-size" | "fs":
                            self.modifiers[_ModifierName.font_size].append(
                                [start_i, end_i, eval(value)])
                        case "font-name" | "fn":
                            self.modifiers[_ModifierName.font_name].append(
                                [start_i, end_i, eval(value)])


_global_rich_text_parser: _RichTextParser = _RichTextParser()
"""The instance of the rich text parser, used internally by `parse_rich_text`"""


def parse_rich_text(rich_text: str) -> tuple[str, _ModifiersValue]:
    """
    Take a string with html-like rich text and return its version without tags and the tags converted to modifiers in a tuple\n
    Rich text rules: (case unsensitive, shorter alias)
    - <b / bold> -> bold
    - <i / italic> -> italic
    - <u / underline> -> underline
    - <s / strike / striketrough> -> striketrough
    - <a / antialas / antialiasing> -> antialiasing
    - <m / mod  / modifier> -> other modifier
    - <m color=ColorValue> -> fg color, where ColorValue is a value supported by pygame (also 'fg-color, fgcolor, fg_color, col, c')
    - <m bg-color=ColorValue> -> bg color, where ColorValue is a value supported by pygame (also 'bgcolor, bg_color, bg-col, bgcol, bg_col, bgc')
    - <m font-size=FontSize> -> font size, where FontSize is a number (also 'fs')
    - <m font-name=FontName> -> font name, where FontName is a string (also 'fn')
    """
    return _global_rich_text_parser.parse_text(rich_text)
