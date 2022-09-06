"""Custom Database Fields."""

from django.db.models import BooleanField, ForeignKey
from django.utils.translation import gettext_lazy as _
from wagtailsvg.models import Svg


class ImageOrSvgField(ForeignKey):
    """Add an image_field, image_field_svg and image_field_is_svg fields, combine with ImageOrSvgPanel."""

    def __init__(self, *args, **kwargs):
        """Set Field parameters."""
        self.init_args = args
        self.init_kwargs = kwargs
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        """Bound attrs to the parent container class."""
        self.name = name

        # Add Real field
        original_field_name = f"{self.name}"
        real_field = ForeignKey(*self.init_args, **self.init_kwargs)
        real_field.contribute_to_class(cls, original_field_name)

        # Add Trigger Field
        trigger_field_name = f"{self.name}_is_svg"
        trigger_field = BooleanField(
            default=False, verbose_name=_("Usar imagen SVG"), null=True, blank=True
        )
        setattr(cls, trigger_field_name, trigger_field)
        trigger_field.contribute_to_class(cls, trigger_field_name)

        # Add SVG Field
        svg_field_name = f"{self.name}_svg"
        self.init_kwargs.pop("related_name")
        svg_field = ForeignKey(
            Svg,
            related_name="+",
            **self.init_kwargs,
        )
        setattr(cls, svg_field_name, svg_field)
        svg_field.contribute_to_class(cls, svg_field_name)
