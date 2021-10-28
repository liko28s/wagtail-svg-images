"""Snippets are always commons."""
from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Collection, get_root_collection_id
from wagtail.documents import get_document_model_string
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class SVGImage(models.Model):
    """Snippet that provides SVG Image Support."""

    title = models.CharField(max_length=255, verbose_name=_("Título"))
    file = ForeignKey(
        get_document_model_string(),
        verbose_name=_("Imagen SVG"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        # validators=[FileExtensionValidator([".svg"])],
    )
    collection = models.ForeignKey(
        Collection,
        default=get_root_collection_id,
        verbose_name=_("collection"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    tags = TaggableManager(help_text=None, blank=True, verbose_name=_("tags"))

    panels = [
        FieldPanel("title"),
        DocumentChooserPanel("file"),
        FieldPanel("collection"),
        FieldPanel("tags"),
    ]

    @property
    def file_url(self):
        return self.file.url

    def __str__(self):
        """A readable representation."""
        return self.title

    class Meta:
        verbose_name = _("Imagen SVG")
        verbose_name_plural = _("Imágenes Svg")



