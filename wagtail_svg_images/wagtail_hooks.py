from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks


#
# @hooks.register("construct_main_menu")
# def hide_menu_items(request, menu_items):
#     """Hide certain registered items in the main menu."""
#     items_to_hide = ["colores", "coleciones", "imagenes-svg"]
#     menu_items[:] = [item for item in menu_items if item.name not in items_to_hide]


@hooks.register("insert_editor_js")
def editor_js():
    return format_html('<script src="{}"></script>', static("js/svg_handler.js"))
