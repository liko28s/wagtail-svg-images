Under Construction
Use for fields
```
from wagtail_svg_images.models import ImageOrSvgField
from wagtail_svg_images.panels import ImageOrSVGPanel
````

Use for Blocks
```
from wagtail_svg_images.blocks import ImageOrSVGBlock
my_field_name = ImageOrSVGBlock("my_field_name", label=_("imagen"), required=True)
```

Use in templates
```
{% load svg_tags %}
{# Drop in Replacement of image tag #}
{% svg-image %}
```



