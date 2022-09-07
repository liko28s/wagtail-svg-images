import re
from collections import namedtuple
from copy import copy

from django import template
from django.template import TemplateSyntaxError
from django.template.context import ContextDict
from django.utils.safestring import mark_safe
from wagtail.core.blocks import StructValue
from wagtail.images import get_image_model
from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtail.images.templatetags.wagtailimages_tags import ImageNode, image

register = template.Library()
allowed_filter_pattern = re.compile(r"^[A-Za-z0-9_\-\.]+$")

# TODO add more properties if you need
available_fields = ["url", "alt", "height", "width", "fill", "max", "original"]
FakeRendition = namedtuple(
    "FakeRendition",
    available_fields,
    defaults=(None,) * len(available_fields),
)


@register.tag(name="svg-image")
def svg_image(parser, token):
    """Render an <img> tag, drop-in replacement of wagtail image tag."""
    try:
        original_tag = image(parser, token)
    except TemplateSyntaxError as error:
        raise TemplateSyntaxError(error)
    except ValueError as error:
        raise ValueError("Rami:", error)
    return CustomImageNode(
        original_tag.image_expr,
        original_tag.filter_spec,
        attrs=original_tag.attrs,
        output_var_name=original_tag.output_var_name,
    )


class CustomImageNode(ImageNode):
    """Search in context"""

    def render(self, context):
        """Render the image tag, no matter if is a normal image or a SVG Image."""
        # TODO: would you like to optimize this?
        # Check if image has _svg alternative in global context
        add_image_expr_suffix(self.image_expr, "_is_svg")
        is_svg = self.image_expr.resolve(context)
        remove_image_expr_suffix(self.image_expr, "_is_svg")

        # Check if image is inside StructValue
        resolved = self.image_expr.resolve(context)
        resolved_image = None
        alt_context = copy(context)
        if isinstance(resolved, StructValue):
            add_image_expr_suffix(self.image_expr, "_is_svg")
            values = {key: value for key, value in resolved.items()}
            alt_context.update(values)
            ContextDict(
                alt_context,
                {self.image_expr.var.lookups[0]: {**values, "value": values}},
            )
            is_svg = self.image_expr.resolve(alt_context)
            remove_image_expr_suffix(self.image_expr, "_is_svg")
            add_image_expr_suffix(self.image_expr, "_svg")
            resolved_image = self.image_expr.resolve(alt_context)
            remove_image_expr_suffix(self.image_expr, "_svg")

        if is_svg in ["true", "1", True, "True"]:
            # Hack the image_expr to resolve with svg in context
            if not resolved_image:
                add_image_expr_suffix(self.image_expr, "_svg")
                resolved_image = self.image_expr.resolve(alt_context)

            # Generates img tag
            if resolved_image:
                # Parse filters
                dummy_rendition = get_rendition_or_not_found(
                    get_image_model().objects.first(), self.filter
                )
                if not dummy_rendition.pk:
                    # TODO Dummy image must be big, renditions are limited by its size
                    dummy_image = get_image_model().objects.first()
                    dummy_rendition = dummy_image.get_rendition_model()(
                        image=dummy_image, filter_spec=self.filter_spec
                    )

                resolved_attrs = {
                    "height": f"{dummy_rendition.height}px",
                    "width": f"{dummy_rendition.width}px",
                }
                from xml.dom import minidom

                svg_content = resolved_image.file.file.file
                # svg_parsed = minidom.parse(resolved_image.file.file.file)
                svg_parsed = minidom.parse(svg_content)
                svg_content.seek(0)
                for key in self.attrs:
                    resolved_attrs[key] = self.attrs[key].resolve(alt_context)

                for attr_name, value in resolved_attrs.items():
                    svg_parsed.documentElement.setAttribute(attr_name, value)
                # Save object into output variable
                if self.output_var_name:
                    # Object like experience
                    resolved_attrs["url"] = resolved_attrs.pop("src", "")
                    context[self.output_var_name] = FakeRendition(**resolved_attrs)
                    return ""
                # Must be printed as <svg> for animations
                return mark_safe(svg_parsed.toxml())
            remove_image_expr_suffix(self.image_expr, "_svg")
        # Do usual stuff
        return super().render(alt_context)


def add_image_expr_suffix(image_expr, suffix):
    image_expr.token += suffix
    image_expr.var.var = image_expr.var.var + suffix
    lookups = list(image_expr.var.lookups)
    lookups[-1] = lookups[-1] + suffix
    image_expr.var.lookups = tuple(lookups)


def remove_image_expr_suffix(image_expr, suffix):
    end_slice = -len(suffix)
    image_expr.token = image_expr.token[:end_slice]
    image_expr.var.var = image_expr.var.var[:end_slice]
    lookups = list(image_expr.var.lookups)
    lookups[-1] = lookups[-1][:end_slice]
    image_expr.var.lookups = tuple(lookups)
