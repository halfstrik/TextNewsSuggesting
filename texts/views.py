import json

from django.http import HttpResponse
from tagging.models import Tag

from texts.models import Text, TagRelationship


def tags_relationships_json(request):
    tags = Tag.objects.usage_for_model(Text, counts=True)
    nodes = []
    for name, count, tag_id in [(tag.name, tag.count, tag.id) for tag in tags]:
        nodes.append({'label': name, 'size': str(count), 'id': str(tag_id)})

    relationships = TagRelationship.objects.all()
    edges = []
    for relationship in relationships:
        edges.append({'source': str(relationship.first_tag.id),
                      'target': str(relationship.second_tag.id),
                      'id': str(relationship.id),
                      'label': str(relationship.weigh),
                      'size': str(2 * relationship.weigh),
                      'type': 'curve'})

    return HttpResponse(json.dumps({'edges': edges, 'nodes': nodes}))
