from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tagging.models import Tag, TaggedItem

from texts.models import Text, Source, TagRelationship


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('source', 'title', 'description', 'link', 'published',)}),
        ('Manual options', {
            'fields': ('days_to_life', 'keywords')}))
    list_display = ('source', 'title', 'published')
    readonly_fields = ('source', 'title', 'description', 'link', 'published')
    list_filter = ('source', 'published')
    search_fields = ['title', 'description']
    inlines = [TaggedItemInline, ]


admin.site.register(Text, TextAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_link')


admin.site.register(Source, SourceAdmin)


class TagRelationshipAdmin(admin.ModelAdmin):
    list_display = ('first_tag', 'second_tag', 'weigh')
    search_fields = ['first_tag__name', 'second_tag__name']
    list_filter = ('weigh',)


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
    search_fields = ['name']
    inlines = [
        TagRelationshipInline,
        TagRelationshipInverseInline
    ]


admin.site.register(Tag, TagAdmin)
