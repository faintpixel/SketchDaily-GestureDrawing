from django.contrib import admin
from sketchdaily.models import *


class ReferenceImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'file')
    list_per_page = 15
    list_max_show_all = 30
    pass


admin.site.register(ReferenceImage, ReferenceImageAdmin)
admin.site.register(FullBodyReference)
admin.site.register(AnimalReference)
admin.site.register(BodyPartReference)
admin.site.register(Session)
admin.site.register(UserSubmittedImage)
admin.site.register(Contact)
admin.site.register(TermsOfUse)