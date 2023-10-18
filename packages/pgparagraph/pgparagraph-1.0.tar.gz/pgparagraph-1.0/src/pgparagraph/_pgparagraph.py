"""Pygame paragraph renderer with modifiers and rich text parsing"""
import pygame
from enum import StrEnum as _str_enum

from ._modifiers import (
    ModifiersHolder,
    ModifierName,
    empty_modifiers,
    modifiers_of_char,
    DEFAULT_MODIFIERS,
    ModifiersValue,
    DefaultModifiersValue
)
from ._richtext import parse_rich_text


class TextAlign(_str_enum):
    """
    Enum to specify the alignment of the paragraph. Strings can be used but not recommended
    NOTE: Center is replaced with middle for IDE linting errors
    """
    middle = "middle"
    left = "left"
    right = "right"


class FontCache:
    """
    Keeps a reference to all the fonts object a paragraph could need.
    For each font and for each size a font object will be cached, so don't use too many 
    (The number of font objects is N*M where N is the amount of font names used and M is the amount of font size uses in the modifiers)
    """
    def __init__(self):
        self.cache: dict[str, pygame.Font] = {}

    def refresh_cache(self, modifiers: ModifiersValue, default_modifiers: DefaultModifiersValue):
        """Remake the font-name & font-size checks to cache fonts that are not already cached"""
        sysfonts = pygame.font.get_fonts()
        done_names = []
        done_sizes = []
        dfn, dfs = default_modifiers[ModifierName.font_name], default_modifiers[ModifierName.font_size]
        for _, _, font_name in list(modifiers[ModifierName.font_name])+[[0, 0, dfn]]:
            if font_name in done_names:
                continue
            for _, _, font_size in list(modifiers[ModifierName.font_size])+[[0, 0, dfs]]:
                if font_size in done_sizes:
                    continue
                cache_str = f"{font_name}_{font_size}"
                if cache_str in self.cache:
                    continue

                font_func = pygame.font.SysFont if font_name.lower() in sysfonts else pygame.Font
                self.cache[cache_str] = font_func(font_name, font_size)

                done_sizes.append(font_size)
            done_names.append(font_name)

    def reset(self):
        """Reset the cache to an empty dictionary, python will garbage collect the fonts"""
        self.cache = {}


CharsDataValue = list[dict[str, int | tuple[int]]]
"""
Type alias representing how chars data is returned. In detail layout:\n
chars_data = [\n
    line1, line2, line3...\n
]\n
Where a line is: {\n
    "height": # the tallest char of the line\n
    "width": # the width used by characters\n
    "full-width": # the total width of the line\n
    "chars": [char1, char2, char3...]\n
}\n
Where a char is:\n
(unicode, render_width, render_height, render_pos, char_index)\n\n\n
"""


class Paragraph:
    """
    Holds text, rendering settings, font caches, modifiers and rendering data of paragraphs\n
    - start_i and end_i control which portions of output_text are sent to the renderer
    - the mask, a rect relative to the topleft of the paragraph, will avoid rendering outside its bounds
    - if the mask is strict, only chars that are 100% inside the mask will be rendered
    """
    
    def __init__(self,
                 text: str,
                 align: TextAlign = TextAlign.middle,
                 default_modifiers: DefaultModifiersValue = DEFAULT_MODIFIERS,
                 start_i: int = 0,
                 end_i: int = -1,
                 mask: pygame.Rect | None = None,
                 strict_mask: bool = False
                 ):
        self.raw_text: str = text
        self.output_text: str = text
        self.align: TextAlign = align
        self.start_i: int = start_i
        self.end_i: int = end_i
        self.mask: pygame.Rect = mask
        self.strict_mask: bool = strict_mask
        self.output_surface: pygame.Surface = None
        self.output_rect: pygame.Rect = None
        self.modifiers_holder: ModifiersHolder = ModifiersHolder(
            empty_modifiers(), default_modifiers)
        self.font_cache: FontCache = FontCache()

    def set_text(self, text: str):
        """Set raw_text (and temporarely output_text) to the given string"""
        self.raw_text = text
        self.output_text = text

    def parse_rich_text(self):
        """Change output_text and update the modifiers after parsing the rich text string. Check the `parse_rich_text` docstring about rich text rules"""
        self.output_text, mods = parse_rich_text(self.raw_text)
        self.modifiers_holder.update_modifiers(mods)

    def render(self, wraplength: int = 500, get_chars_data: bool = False) -> tuple[pygame.Surface, pygame.Rect, CharsDataValue | None]:
        """
        Call `pgparagraph.render` with the class settings and save and return the result (surface, rect, data?)
        - wraplength will force a new line when the line is too long
        - get_chars_data will make the third return value a list with the rendered data (check `CharsDataValue` docstring for the layout)
        """
        self.output_surface, self.output_rect, chars_data = render(
            self.output_text,
            self.modifiers_holder.modifiers,
            self.modifiers_holder.default_modifiers,
            self.font_cache,
            self.align,
            wraplength,
            self.start_i,
            self.end_i,
            self.mask,
            self.strict_mask,
            get_chars_data
        )
        return self.output_surface, self.output_rect, chars_data


def render(text: str,
           modifiers: ModifiersValue,
           default_modifiers: DefaultModifiersValue,
           font_cache: FontCache,
           align=TextAlign.middle,
           wraplength=500,
           start_i: int = 0,
           end_i: int = -1,
           mask: pygame.Rect = None,
           strict_mask: bool = False,
           get_chars_data: bool = False
        ) -> tuple[pygame.Surface, pygame.Rect, CharsDataValue | None]:
    """
    Render the given text and modifiers with the given settings
    - the font cache is refreshed
    - start_i and end_i will filter out portions of the text
    - mask will avoid rendering what is out of its bounds
    - strict_mask will render only chars that are 100% inside the bounds
    - get_chars_data will make the third return value the render data. Check `CharsDataValue` docstring for more\n
    Return the surface rendered and its absolute rect (+ the optional data)
    """
    font_cache.refresh_cache(modifiers, default_modifiers)
    text = text[start_i:] if end_i == -1 else text[start_i:end_i]

    longest_line = cur_x = tallest_char = total_h = 0
    lines, cur_line = [], []
    for i, char in enumerate(text):
        if char == "\n":
            if cur_x > longest_line:
                longest_line = cur_x
            cur_line.append(tallest_char)
            cur_line.append(cur_x)
            total_h += tallest_char
            lines.append(cur_line)
            tallest_char = cur_x = 0
            cur_line = []
            continue
        char_mods = modifiers_of_char(i, modifiers, default_modifiers, start_i)
        font = font_cache.cache[f"{char_mods[ModifierName.font_name]}_{char_mods[ModifierName.font_size]}"]
        char_w, char_h = font.size(char)
        if wraplength != -1:
            if cur_x + char_w > wraplength:
                if cur_x > longest_line:
                    longest_line = cur_x
                cur_line.append(tallest_char)
                cur_line.append(cur_x)
                total_h += tallest_char
                lines.append(cur_line)
                tallest_char = cur_x = 0
                cur_line = []

        cur_line.append((char_mods, char_w, char_h, font, char))
        if char_h > tallest_char:
            tallest_char = char_h
        cur_x += char_w
        
    if cur_x > 0:
        if cur_x > longest_line:
            longest_line = cur_x
        cur_line.append(tallest_char)
        cur_line.append(cur_x)
        total_h += tallest_char
        lines.append(cur_line)

    line_w = longest_line
    if mask is not None:
        if longest_line > mask.w:
            longest_line = mask.w
        if total_h > mask.h:
            total_h = mask.h

    render_surf = pygame.Surface((longest_line, total_h), pygame.SRCALPHA)
    render_surf.fill(0)
    render_rect = pygame.Rect(
        0, 0, mask.w, mask.h) if mask is not None else render_surf.get_rect()

    render_data = []
    y = i = 0
    for line in lines:
        x = 0
        tall = line[-2]
        this_line_w = line[-1]
        line.pop()
        line.pop()
        line_data = {"height": tall, "width": this_line_w,
                     "full-width": line_w, "chars": []} if get_chars_data else None
        for c_mods, c_w, c_h, font, char in line:
            rx = x
            if align == TextAlign.right:
                rx = line_w-this_line_w+x
            elif align == TextAlign.middle:
                rx = (line_w//2)-(this_line_w//2)+x
            pos = (rx, y+((tall//2)-c_h//2))
            x += c_w

            if mask is not None:
                c1, c2 = mask.collidepoint(pos), mask.collidepoint(
                    (pos[0]+c_w, pos[1]+c_h))
                if ((not c1 and not c2) and not strict_mask) or ((not c1 or not c2) and strict_mask):
                    i += 1
                    continue
                pos = (pos[0]-mask.x, pos[1]-mask.y)
                
            font.bold, font.italic, font.underline, font.strikethrough = (
                c_mods[ModifierName.bold],
                c_mods[ModifierName.italic],
                c_mods[ModifierName.underline],
                c_mods[ModifierName.strikethrough],
            )
            render_surf.blit(font.render(char,
                                      c_mods[ModifierName.antialiasing],
                                      c_mods[ModifierName.fg_color],
                                      c_mods[ModifierName.bg_color]), 
                             pos)
            i += 1
            if get_chars_data:
                line_data["chars"].append((char, char_w, char_h, pos, i))

        y += tall
        if get_chars_data:
            render_data.append(line_data)

    return render_surf, render_rect, render_data if get_chars_data else None
