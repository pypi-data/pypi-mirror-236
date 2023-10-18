"""Submodule of pgparagraph defining the modifiers structure, types, enums and functions"""
from enum import StrEnum as _str_enum
from typing import Iterable as _Iterable
import pygame as _pg


class ModifierName(_str_enum):
    """The type that a modifier can have. You can use strings too, but the enum notation is preferred"""
    font_name = "font-name"
    font_size = "font-size"
    fg_color = "fg-color"
    bg_color = "bg-color"
    antialiasing = "antialiasing"
    bold = "bold"
    underline = "underline"
    italic = "italic"
    strikethrough = "strike"


_ColorValue = str | _Iterable[int] | _pg.Color
"""Similar to pygame.common.pyi _ColorValue"""
ModifierValue = tuple[int, int, str | int | _ColorValue | bool | None]
"""Type alias representing what a modifier looks like. For example: `[0, 30, "consolas"]`"""
ModifiersValue = dict[ModifierName, list[ModifierValue]]
"""Type alias representing what a modifiers dict looks like. For example: `{ModifierName.font_size:[[0,20,15], [12,30,30]...]...}`"""
DefaultModifiersValue = dict[ModifierName, ModifierValue]
"""Type alias representing what a default modifiers dict looks like. It's like the normal modifiers but instead of a list of modifiers for each name there is a single value"""

DEFAULT_MODIFIERS: DefaultModifiersValue = {
    ModifierName.font_name: "consolas",
    ModifierName.font_size: 30,
    ModifierName.fg_color: "white",
    ModifierName.bg_color: None,
    ModifierName.antialiasing: True,
    ModifierName.bold: False,
    ModifierName.underline: False,
    ModifierName.italic: False,
    ModifierName.strikethrough: False,
}
"""The built-in default modifiers dict"""


class ModifiersHolder:
    """
    Hold modifiers and default modifiers in the same object, implementing methods on them
    If modifiers is passed as `'empty'`, `empty_modifiers()` will be used instead
    """

    def __init__(self, start_modifiers: str | ModifiersValue = "empty", default_modifiers: DefaultModifiersValue = DEFAULT_MODIFIERS):
        self.modifiers: ModifiersValue = start_modifiers if start_modifiers != "empty" else empty_modifiers()
        self.default_modifiers: DefaultModifiersValue = default_modifiers.copy()

    def update_modifiers(self, modifiers: ModifiersValue):
        """Add the modifiers from `modifiers` into this object's modifiers"""
        for key, val in modifiers.items():
            for v in val:
                self.modifiers[key].append(v)

    def reset(self):
        """Set `modifiers` to `empty_modifiers()`"""
        self.modifiers = empty_modifiers()

    def add_modifier(self, name: ModifierName, start_i: int, end_i: int, value: str | int | _ColorValue | bool | None):
        """Shortcut for adding a modifier of a name to the modifiers"""
        self.modifiers[name].append([start_i, end_i, value])


def empty_modifiers() -> ModifiersValue:
    """Return a fresh empty modifiers dict"""
    return {
        ModifierName.font_name: [],
        ModifierName.font_size: [],
        ModifierName.fg_color: [],
        ModifierName.bg_color: [],
        ModifierName.antialiasing: [],
        ModifierName.bold: [],
        ModifierName.underline: [],
        ModifierName.italic: [],
        ModifierName.strikethrough: [],
    }


def add_modifier(modifiers: ModifiersValue, name: ModifierName, start_i: int, end_i: int, value: str | int | _ColorValue | bool | None):
    """Shortcut for adding a modifier of a name to some modifiers"""
    modifiers[name].append([start_i, end_i, value])


def create_default_modifiers(**changed_modifiers: dict[str, str | int | _ColorValue | bool | None]) -> DefaultModifiersValue:
    """Creates a custom version of the default modifiers copying the built-in one and adding the `**changed_modifiers`"""
    default_modifier = DEFAULT_MODIFIERS.copy()
    default_modifier.update(changed_modifiers)
    return default_modifier


def modifier_of_char(char_i: int, modifier_name: ModifierName, modifiers: ModifiersValue, default_modifiers: DefaultModifiersValue, start_i: int):
    """Given a char index, modifiers, default modifiers and the start index of the text, return the modifier of that type at the given position if any, or return the default one"""
    for mod in modifiers[modifier_name]:
        if (mod[0]-start_i) <= char_i and (mod[1]-start_i) >= char_i:
            return mod[2] if len(mod) == 3 else False
    return default_modifiers[modifier_name]


def modifiers_of_char(char_i: int, modifiers: ModifiersValue, default_modifiers: DefaultModifiersValue, start_i: int) -> DefaultModifiersValue:
    """Given a char index, modifiers, default modifiers and the start index of the text, return the modifiers of every type at the given position if any, or the default one, as a dictionary"""
    return {
        ModifierName.font_name: modifier_of_char(char_i, ModifierName.font_name, modifiers, default_modifiers, start_i),
        ModifierName.font_size: modifier_of_char(char_i, ModifierName.font_size, modifiers, default_modifiers, start_i),
        ModifierName.fg_color: modifier_of_char(char_i, ModifierName.fg_color, modifiers, default_modifiers, start_i),
        ModifierName.bg_color: modifier_of_char(char_i, ModifierName.bg_color, modifiers, default_modifiers, start_i),
        ModifierName.antialiasing: modifier_of_char(char_i, ModifierName.antialiasing, modifiers, default_modifiers, start_i),
        ModifierName.italic: modifier_of_char(char_i, ModifierName.italic, modifiers, default_modifiers, start_i),
        ModifierName.bold: modifier_of_char(char_i, ModifierName.bold, modifiers, default_modifiers, start_i),
        ModifierName.underline: modifier_of_char(char_i, ModifierName.underline, modifiers, default_modifiers, start_i),
        ModifierName.strikethrough: modifier_of_char(char_i, ModifierName.strikethrough, modifiers, default_modifiers, start_i),
    }
