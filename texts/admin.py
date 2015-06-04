from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tagging.models import Tag, TaggedItem
from django.utils.translation import ugettext_lazy as _

from texts.models import Text, Source, TagRelationship, PropertyFirst, PropertySecond, Comment


class TaggedItemModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TaggedItemModelForm, self).__init__(*args, **kwargs)
        ids = list(Tag.objects.exclude(name__contains=':').values_list('id', flat=True))
        if 'instance' in kwargs:
            ids += list(Tag.objects.filter(name__startswith=kwargs['instance'].object.source.name)
                        .values_list('id', flat=True))
        self.fields['tag'].queryset = Tag.objects.filter(id__in=ids)


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    form = TaggedItemModelForm


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
    inlines = [TaggedItemInline, CommentInline]


admin.site.register(Text, TextAdmin)


class SourceAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)
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


admin.site.unregister(TaggedItem)
admin.site.unregister(Tag)


class CreatorTagFilter(admin.SimpleListFilter):
    title = _('is creator specific')
    parameter_name = 'creator'

    def lookups(self, request, model_admin):
        return (
            ('creator', _('creator\'s')),
            ('general', _('general')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'creator':
            return queryset.filter(name__contains=':')
        if self.value() == 'general':
            return queryset.exclude(name__contains=':')


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = (CreatorTagFilter,)
    inlines = [
        TagRelationshipInline,
        TagRelationshipInverseInline
    ]


admin.site.register(Tag, TagAdmin)

admin.site.register(PropertyFirst)
admin.site.register(PropertySecond)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'updated', 'text')
    readonly_fields = ['user', 'created', 'updated', 'news']


admin.site.register(Comment, CommentAdmin)
