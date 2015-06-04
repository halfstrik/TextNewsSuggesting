from django.conf.urls import url

from texts import views

urlpatterns = [
    url(r'^tags_relationships_json$', views.tags_relationships_json, name='tags_relationships_json'),
    url(r'^general_tags_relationships_json$', views.general_tags_relationships_json,
        name='general_tags_relationships_json$'),
]
