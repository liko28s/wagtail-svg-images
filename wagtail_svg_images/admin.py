from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from instance_selector.registry import registry
from instance_selector.selectors import ModelAdminInstanceSelector
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import SVGImage


@modeladmin_register
class SVGImageAdmin(ModelAdmin):
    model = SVGImage
    list_display = ("title", "image_preview")

    def image_preview(self, instance):
        if instance:
            return mark_safe(
                f'<img src="{instance.file_url}" width="165px" heigth="165px">'
            )
        return ""

    image_preview.short_description = _("Muestra")


class SVGImageSelector(ModelAdminInstanceSelector):
    model_admin = SVGImageAdmin()

    def get_instance_display_title(self, instance):
        if instance:
            return instance.title

    def get_instance_display_image_url(self, instance):
        if instance:
            return instance.file_url


registry.register_instance_selector(SVGImage, SVGImageSelector())
