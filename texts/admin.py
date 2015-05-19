from django.contrib import admin

from texts.models import Text


class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


admin.site.register(Text, TextAdmin)
