import json

from django.core import management
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from texts.models import CommonTag, CommonTaggedItem, CommonTagRelationship, WEAK, AVERAGE


def general_tags_relationships_json(request):
    tags = CommonTag.objects.all()
    nodes = []
    tag_ids = []
    for tag in tags:
        tag_counts = CommonTaggedItem.objects.filter(tag=tag).count()
        nodes.append({'label': tag.name, 'size': str(tag_counts), 'id': str(tag.id)})
        tag_ids.append(tag.id)
    relationships = CommonTagRelationship.objects.filter(first_tag__in=tag_ids).filter(second_tag__in=tag_ids)
    edges = []
    for relationship in relationships:
        edges.append({'source': str(relationship.first_tag.id),
                      'target': str(relationship.second_tag.id),
                      'id': str(relationship.id),
                      'label': str(relationship.weigh),
                      'size': str(1 if relationship.weigh == WEAK else 2 if relationship.weigh == AVERAGE else 3),
                      'type': 'curve'})

    return HttpResponse(json.dumps({'edges': edges, 'nodes': nodes}))


def assign_common_tags_to_text(request, text_id):
    management.call_command('update_common_tags_on_text_by_id', text_id)
    return HttpResponseRedirect(reverse('admin:texts_text_change', args=(text_id,)))
