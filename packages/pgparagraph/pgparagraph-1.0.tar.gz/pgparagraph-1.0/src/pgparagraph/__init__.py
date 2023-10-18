"""Pygame paragraph renderer with modifiers and rich text parsing"""
from ._pgparagraph import (
    Paragraph,
    FontCache,
    TextAlign,
    render,
    CharsDataValue
)

from ._modifiers import (
    DEFAULT_MODIFIERS,
    create_default_modifiers,
    add_modifier,
    empty_modifiers,
    modifiers_of_char,
    modifier_of_char,
    ModifierName,
    ModifiersHolder,
    ModifierValue,
    ModifiersValue,
    DefaultModifiersValue
)

from ._richtext import parse_rich_text

from . import _richtext as richtext
from . import _modifiers as modifiers