import os
import json
from json.decoder import JSONDecodeError
from material_color_utilities_python import CorePalette, argbFromHex, sourceColorFromImage, Blend, TonalPalette, hexFromArgb, redFromArgb, blueFromArgb, greenFromArgb
from PIL import Image
import toml
from colorthief import ColorThief


def get_cached_colors():
    cache_file_path = os.path.expanduser(
        '~/.cache/pmt/source_colors.json')

    if not os.path.isfile(cache_file_path):
        os.makedirs(os.path.expanduser('~/.cache/pmt/'), exist_ok=True)
        open(cache_file_path, "x")

    with open(cache_file_path, "r", encoding="utf8") as json_file:
        try:
            return json.load(json_file)
        except JSONDecodeError:
            return {}


def get_argb_core_theme(color_scheme_type, source_color):
    """
    Returns colorscheme from source color

    :param color_scheme_type string: "dark" or "light"
    :param source_color string: argb color
    """
    theme = {}  # Our resulted theme dict
    core_palette = CorePalette.of(source_color)

    color_categories = {
        "primary": "a1",
        "secondary": "a2",
        "tertiary": "a3",
        "error": "error"
    }

    if color_scheme_type == "dark":
        for category, suffix in color_categories.items():
            # Building primary, secondary, tertiary and error colors
            theme[f"{category}"] = getattr(core_palette, suffix).tone(80)
            theme[f"on{category.capitalize()}"] = getattr(core_palette,
                                                          suffix).tone(20)
            theme[f"{category}Container"] = getattr(
                core_palette, suffix).tone(30)
            theme[f"on{category.capitalize()}Container"] = getattr(core_palette,
                                                                   suffix).tone(90)

        # Building surfaces and outlines
        theme["surfaceDim"] = getattr(core_palette, "n1").tone(6)
        theme["surface"] = getattr(core_palette, "n1").tone(6)
        theme["surfaceBright"] = getattr(core_palette, "n1").tone(24)

        theme["surface1"] = getattr(core_palette, "n1").tone(4)
        theme["surface2"] = getattr(core_palette, "n1").tone(10)
        theme["surface3"] = getattr(core_palette, "n1").tone(12)
        theme["surface4"] = getattr(core_palette, "n1").tone(17)
        theme["surface5"] = getattr(core_palette, "n1").tone(22)

        theme["onSurface"] = getattr(core_palette, "n1").tone(90)
        theme["onSurfaceVariant"] = getattr(core_palette, "n2").tone(80)

        theme["outline"] = getattr(core_palette, "n2").tone(60)
        theme["outlineVariant"] = getattr(core_palette, "n2").tone(30)

    if color_scheme_type == "light":
        for category, suffix in color_categories.items():
            # Building primary, secondary, tertiary and error colors
            theme[f"{category}"] = getattr(core_palette, suffix).tone(40)
            theme[f"on{category.capitalize()}"] = core_palette.get(
                suffix).tone(100)
            theme[f"{category}Container"] = getattr(
                core_palette, suffix).tone(90)
            theme[f"on{category.capitalize()}Container"] = core_palette.get(
                suffix).tone(10)

        # Building surfaces and outlines
        theme["surfaceDim"] = getattr(core_palette, "n1").tone(87)
        theme["surface"] = getattr(core_palette, "n1").tone(98)
        theme["surfaceBright"] = getattr(core_palette, "n1").tone(98)

        theme["surface1"] = getattr(core_palette, "n1").tone(100)
        theme["surface2"] = getattr(core_palette, "n1").tone(96)
        theme["surface3"] = getattr(core_palette, "n1").tone(94)
        theme["surface4"] = getattr(core_palette, "n1").tone(92)
        theme["surface5"] = getattr(core_palette, "n1").tone(90)

        theme["onSurface"] = getattr(core_palette, "n1").tone(10)
        theme["onSurfaceVariant"] = getattr(core_palette, "n2").tone(30)

        theme["outline"] = getattr(core_palette, "n2").tone(50)
        theme["outlineVariant"] = getattr(core_palette, "n2").tone(80)

    return theme


def get_argb_additional_theme(colors_scheme_type, source_color):
    """
    returns additional colorscheme from colors in config file

    :param colors_scheme_type string: "dark" or "light"
    :param source_color string: argb color
    """
    additional_theme = {}

    with open(os.path.expanduser("~/.config/pmt/colors.toml"), encoding="utf8") as file:
        colors = toml.load(file)

    # Iterate over the items in the configuration
    for item in colors['color']:
        name = item['name']
        value = argbFromHex(item['value'])
        blend = item['blend']
        dark_tone = item.get('darkTone')
        light_tone = item.get('lightTone')

        if blend:
            value = Blend.harmonize(value, source_color)
        value_palette = TonalPalette.fromInt(value)

        if colors_scheme_type == "dark":
            if dark_tone:
                additional_theme[name] = value_palette.tone(dark_tone)
            else:
                additional_theme[name] = value_palette.tone(80)
            additional_theme[f"on{name.capitalize()}"] = value_palette.tone(20)
        else:
            if light_tone:
                additional_theme[name] = value_palette.tone(light_tone)
            else:
                additional_theme[name] = value_palette.tone(40)
            additional_theme[f"on{name.capitalize()}"] = value_palette.tone(
                100)

    return additional_theme


def build_theme(argb_core_theme, argb_additional_theme):
    """
    combines additional colorscheme with main colorscheme and adds rgb key colors

    :param argb_core_theme dict: main colorscheme
    :param argb_additional_theme dict: additional colorscheme
    """
    theme = {**argb_core_theme, **argb_additional_theme}
    rgb_theme = {}

    for key, value in theme.items():
        theme[key] = hexFromArgb(value)[1:]
        rgb_theme[key+"-r"] = redFromArgb(value)
        rgb_theme[key+"-g"] = greenFromArgb(value)
        rgb_theme[key+"-b"] = blueFromArgb(value)

    theme.update(rgb_theme)

    return theme


def get_theme_from_color(source_color, color_scheme_type):
    """
    returns colorscheme

    :param source_color string: argb color
    :param color_scheme_type string: "dark" or "light"
    """
    argb_core_theme = get_argb_core_theme(color_scheme_type, source_color)
    argb_additional_theme = get_argb_additional_theme(
        color_scheme_type, source_color)

    return build_theme(argb_core_theme, argb_additional_theme)


def get_theme_from_image(path, color_scheme_type):
    """
    returns colorscheme from given image

    :param path string: path to wallpaper
    :param color_scheme_type string: "dark" or "light"
    """
    cache_file_path = os.path.expanduser(
        '~/.cache/pmt/source_colors.json')

    source_colors = get_cached_colors()
    color_thief = ColorThief(path)
    source_color = argbFromHex(
        "#%02x%02x%02x" % color_thief.get_color(quality=20))
    source_colors[path] = source_color
    with open(cache_file_path, "w", encoding="utf8") as json_file:
        json.dump(source_colors, json_file, indent=4)

    argb_core_theme = get_argb_core_theme(color_scheme_type, source_color)
    argb_additional_theme = get_argb_additional_theme(
        color_scheme_type, source_color)

    return build_theme(argb_core_theme, argb_additional_theme)
