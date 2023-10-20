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


# Hide all models from any user but a superuser:
class CustomModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict to hide the model from the admin index
        for non-superusers.
        """
        perms = super().get_model_perms(request)
        if not request.user.is_superuser:
            # Apply specific logic for non-superusers
            perms.update(
                {
                    "view": False,  # Allow non-superusers to view the model
                    "add": False,  # Allow non-superusers to add instances
                    "change": False,  # Allow non-superusers to change instances
                    "delete": False,  # Allow non-superusers to delete instances
                }
            )
        return perms


# model registrations:
admin.site.register(textsplitter, CustomModelAdmin)
admin.site.register(fontregion, CustomModelAdmin)
admin.site.register(lineregion, CustomModelAdmin)
admin.site.register(readingline, CustomModelAdmin)
admin.site.register(readinghistogram, CustomModelAdmin)
admin.site.register(textpart, CustomModelAdmin)
admin.site.register(title, CustomModelAdmin)
admin.site.register(body, CustomModelAdmin)
admin.site.register(footer, CustomModelAdmin)
admin.site.register(headlines, CustomModelAdmin)
admin.site.register(headlines_hierarchy, CustomModelAdmin)
admin.site.register(enumeration, CustomModelAdmin)
admin.site.register(enumeration_hierarchy, CustomModelAdmin)
admin.site.register(Native_TOC_Element, CustomModelAdmin)
admin.site.register(breakdown_decisions, CustomModelAdmin)
admin.site.register(textalinea, CustomModelAdmin)
