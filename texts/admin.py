from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from taggit.models import Tag

from texts.models import Text, Source, PropertyFirst, PropertySecond, Comment, CommonTaggedItem, CommonTagRelationship, \
    CommonTag, SourceTaggedItem, KeyNormalizedWords


class SourceTaggedItemInline(GenericTabularInline):
    model = SourceTaggedItem
    extra = 0

    readonly_fields = ('tag',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CommonTaggedItemInline(GenericTabularInline):
    model = CommonTaggedItem
    extra = 0

    raw_id_fields = ('tag',)


class CommentInlineFormset(forms.models.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = super(CommentInlineFormset, self).save_new(form, commit=False)
        obj.user = self.request.user

        if commit:
            obj.save()

        return obj


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['user', 'created', 'updated']
    formset = CommentInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class TextAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('source', 'title', 'description', 'body', 'link', 'published', 'created', 'updated',)}),
        ('Manual options', {
            'fields': ('days_to_life', 'keywords', 'property_first', 'property_second', 'is_moderated')}))
    list_display = ('source', 'title', 'published', 'is_moderated', 'comments_count')
    readonly_fields = ('source', 'title', 'description', 'link', 'published', 'created', 'updated',)
    list_filter = ('is_moderated', 'published', 'source',)
    search_fields = ['title', 'description']
    inlines = [SourceTaggedItemInline, CommonTaggedItemInline, CommentInline]


admin.site.register(Text, TextAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_link')


admin.site.register(Source, SourceAdmin)


class CommonTagRelationshipAdmin(admin.ModelAdmin):
    list_display = ('first_tag', 'second_tag', 'weigh')
    search_fields = ['first_tag__name', 'second_tag__name']
    list_filter = ('weigh',)
    raw_id_fields = ('first_tag', 'second_tag',)


admin.site.register(CommonTagRelationship, CommonTagRelationshipAdmin)


class CommonTagKeyNormalizedWordsInline(admin.TabularInline):
    model = KeyNormalizedWords
    extra = 0

class CommonTagRelationshipInline(admin.TabularInline):
    model = CommonTagRelationship
    fk_name = 'first_tag'
    extra = 0
    raw_id_fields = ('second_tag',)


class CommonTagRelationshipInverseInline(admin.TabularInline):
    model = CommonTagRelationship
    fk_name = 'second_tag'
    extra = 0
    verbose_name_plural = 'Inverse relationships to this tag'
    raw_id_fields = ('first_tag',)


admin.site.unregister(Tag)


class CommonTagAdmin(admin.ModelAdmin):
    search_fields = ['name', 'associations']
    list_display = ['name', 'associations']
    inlines = [
        CommonTagKeyNormalizedWordsInline,
        CommonTagRelationshipInline,
        CommonTagRelationshipInverseInline
    ]


admin.site.register(CommonTag, CommonTagAdmin)

admin.site.register(PropertyFirst)
admin.site.register(PropertySecond)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'updated', 'text')
    readonly_fields = ['user', 'created', 'updated', 'news']


admin.site.register(Comment, CommentAdmin)
