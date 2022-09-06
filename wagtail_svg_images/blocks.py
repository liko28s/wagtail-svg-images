from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.core.blocks import (
    BooleanBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtailsvg.blocks import SvgChooserBlock


class ImageOrSVGBlock(StructBlock):
    """Trick to support SVG."""

    def __init__(self, field, **kwargs):
        """
        Start a reactive component with svg or image support.
        :arg field set subblocks name."""
        self.field = field
        self.is_required = kwargs.get("required", True)
        self.child_kwargs = kwargs
        self.child_kwargs.update({"required": False})
        super().__init__(
            [
                (
                    f"{field}_is_svg",
                    BooleanBlock(
                        label=_("Usar imagen SVG"),
                        required=False,
                        default=False,
                        classname=f"ag-choice-handler ag-choice-handler--{field}_is_svg",
                    ),
                ),
                (
                    f"{field}",
                    ImageChooserBlock(
                        **self.child_kwargs,
                        classname=f"ag-choice-handler-target--{field}_is_svg ag-choice-handler-hidden-if--true",
                    ),
                ),
                (
                    f"{field}_svg",
                    SvgChooserBlock(
                        **self.child_kwargs,
                        classname=f"ag-choice-handler-target--{field}_is_svg ag-choice-handler-hidden-if--false",
                    ),
                ),
            ],
            **kwargs,
        )

    @property
    def required(self):
        """Just show if field is required."""
        if self.is_required:
            return True
        return super().required

    def bulk_to_python(self, values):
        """Return the model instances for the given list of blocks.
        The instances must be returned in the same order as the values and keep None values.
        if prev value comes from ImageChooserBlock, translate to ImageOrSVGStructValue.
        """
        if (
            isinstance(values[0], int)
            or not values[0]
            or values[0] is None
            or not values
            or not len(values)
        ):
            return super().bulk_to_python(
                [
                    {
                        f"{self.field}_is_svg": False,
                        f"{self.field}": values[0] if values[0] else None,
                        f"{self.field}_svg": None,
                    }
                ]
            )
        return super().bulk_to_python(values)

    def clean(self, value):
        """Validate field and childblocks."""
        if self.is_required or self.required:
            image = value.get(f"{self.field}", None)
            field_name = self.field
            if value.get(f"{self.field}_is_svg", False):
                image = value.get(f"{self.field}_svg", None)
                field_name = f"{self.field}_svg"
            if not image:
                raise StructBlockValidationError(
                    {
                        field_name: ErrorList(
                            [_("Es requerido seleccionar una imagen o SVG.")]
                        )
                    }
                )
        return super().clean(value)

    class Meta:
        label = _("Imagen o SVG")
        icon = "picture"
