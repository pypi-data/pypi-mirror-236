"""
This module is used to register the models of the django app.
"""

from django.contrib import admin

# model import:
from .models import textsplitter
from .models import fontregion
from .models import lineregion
from .models import readingline
from .models import readinghistogram
from .models import textpart
from .models import title
from .models import body
from .models import footer
from .models import headlines
from .models import headlines_hierarchy
from .models import enumeration
from .models import enumeration_hierarchy
from .models import Native_TOC_Element
from .models import breakdown_decisions
from .models import textalinea

# model registrations:
admin.site.register(textsplitter)
admin.site.register(fontregion)
admin.site.register(lineregion)
admin.site.register(readingline)
admin.site.register(readinghistogram)
admin.site.register(textpart)
admin.site.register(title)
admin.site.register(body)
admin.site.register(footer)
admin.site.register(headlines)
admin.site.register(headlines_hierarchy)
admin.site.register(enumeration)
admin.site.register(enumeration_hierarchy)
admin.site.register(Native_TOC_Element)
admin.site.register(breakdown_decisions)
admin.site.register(textalinea)
