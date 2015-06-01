from django.contrib import admin

from texts.models import Text, Source, TagRelationship


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('source', 'title', 'description', 'link', 'published', 'publisher_tags',)}),
        ('Manual options', {
            'fields': ('days_to_life', 'keywords', 'tags')}))
    list_display = ('source', 'title', 'published')
    readonly_fields = ('source', 'title', 'description', 'link', 'published', 'publisher_tags')
    list_filter = ('source', 'published')


admin.site.register(Text, TextAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_link')


admin.site.register(Source, SourceAdmin)


class TagRelationshipAdmin(admin.ModelAdmin):
    list_display = ('first_tag', 'second_tag', 'weigh')


admin.site.register(TagRelationship, TagRelationshipAdmin)
