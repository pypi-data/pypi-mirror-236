import os
import random
from posaydones_material_theming.modules.theming import get_theme_from_image
from posaydones_material_theming.modules.theming import get_theme_from_color
from posaydones_material_theming.modules.theming import get_cached_colors
from posaydones_material_theming.modules.templates import handle_templates
from posaydones_material_theming.modules.wallpaper import set_wallpaper


def add_slash_if_needed(string):
    """
    adds slash to string if it's needed

    :param s string: string to add slash in
    """
    if string == "":
        return ""
    if string[-1] != '/':
        string += '/'
    return string


def proceed_theme(path, color_scheme_type, wallpaper_setter):
    """
    proceeds theme setting

    :param path string: wallpaper path
    :param color_scheme_type string: "dark" or "light"
    :param wallpaper_setter string: wallpapaer setter string
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        random_file = random.choice(files)
        path = os.path.join(path, random_file)

    source_colors = get_cached_colors()

    if path in source_colors:
        source_color = source_colors[path]
        theme = get_theme_from_color(source_color, color_scheme_type)
    else:
        theme = get_theme_from_image(path, color_scheme_type)

    set_wallpaper(path, wallpaper_setter)
    handle_templates(theme)
