from django.forms import CheckboxInput
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailsvg.edit_handlers import SvgChooserPanel


class ImageOrSVGPanel(MultiFieldPanel):
    """Provide a Field Panel with SVG Support, combine with svg-image tag and ImageOrSvgField."""

    template = "wagtailadmin/edit_handlers/image_or_svg_panel.html"

    def __init__(self, field, **kwargs):
        self.field = field
        self.children = [
            FieldPanel(
                f"{field}_is_svg",
                classname=f"ag-choice-handler ag-choice-handler--{field}_is_svg",
                widget=CheckboxInput,
            ),
            ImageChooserPanel(
                field,
                classname=f"ag-choice-handler-target--{field}_is_svg ag-choice-handler-hidden-if--true",
            ),
            SvgChooserPanel(
                f"{field}_svg",
                classname=f"ag-choice-handler-target--{field}_is_svg ag-choice-handler-hidden-if--false",
            ),
        ]
        kwargs.update({"children": self.children})
        self.verbose_name = kwargs.pop("verbose_name", "")
        super().__init__(**kwargs)

    def clone_kwargs(self):
        """Called on panel instantiation and django checks."""
        kwargs = super().clone_kwargs()
        kwargs["field"] = self.field
        kwargs["children"] = self.children
        # Extract Field Verbose Name
        if hasattr(self.model, self.field):
            kwargs["verbose_name"] = [
                field.verbose_name
                for field in self.model._meta.fields
                if field.name == self.field
            ][0]
        return kwargs
