from django.conf.urls import url

from texts import views

urlpatterns = [
    url(r'^assign_common_tags_to_text/(?P<text_id>[0-9]+)/$', views.assign_common_tags_to_text,
        name='assign_common_tags_to_text'),
    url(r'^general_tags_relationships_json$', views.general_tags_relationships_json,
        name='general_tags_relationships_json$'),
]
