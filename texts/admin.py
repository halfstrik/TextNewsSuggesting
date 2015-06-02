from django.contrib import admin
from tagging.models import Tag

from texts.models import Text, Source, TagRelationship


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('source', 'title', 'description', 'link', 'published',)}),
        ('Manual options', {
            'fields': ('days_to_life', 'keywords')}))
    list_display = ('source', 'title', 'published')
    readonly_fields = ('source', 'title', 'description', 'link', 'published')
    list_filter = ('source', 'published')


admin.site.register(Text, TextAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_link')


admin.site.register(Source, SourceAdmin)


class TagRelationshipAdmin(admin.ModelAdmin):
    list_display = ('first_tag', 'second_tag', 'weigh')


admin.site.register(TagRelationship, TagRelationshipAdmin)


class TagRelationshipInline(admin.TabularInline):
    model = TagRelationship
    fk_name = 'first_tag'
    extra = 0


class TagRelationshipInverseInline(admin.TabularInline):
    model = TagRelationship
    fk_name = 'second_tag'
    extra = 0
    verbose_name_plural = 'Inverse relationships to this tag'


admin.site.unregister(Tag)


class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagRelationshipInline,
        TagRelationshipInverseInline
    ]


admin.site.register(Tag, TagAdmin)
