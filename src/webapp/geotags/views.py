# coding=utf-8


from django.shortcuts import render_to_response
from django.shortcuts import Http404
from django.template import RequestContext
    
from geouser.decorators import login_required

@login_required
def view_tag_suggestions(request, slug, template='webapp/view_tag.html'):
    slug = slug.lower()
    from models import Tag
    tag = Tag.objects.get_by_name(slug)
    if tag is None:
        raise Http404
    from geoalert.models import Suggestion
    user_suggestions = Suggestion.objects.get_by_tag_owner(tag, request.user)
    suggestions = Suggestion.objects.get_by_tag_querier(tag, request.user)
    return render_to_response(template, {
                                        'suggestions': suggestions,
                                        'user_suggestions': user_suggestions,
                                        },
                               context_instance=RequestContext(request))

def search_tag_suggestion(request, tag):
    from models import Tag
    from geoalert.models import Suggestion
    from geolist.models import List
    tags_instance = Tag.objects.get_by_name(tag)
    suggestions = Suggestion.objects.get_by_tag_querier(tags_instance, request.user)
    return suggestions

@login_required
def add_suggestion_tag(request, event_id, tags):
    from geoalert.models import Event
    event = Event.objects.get_by_id_user(event_id, request.user)
    if event is None:
        raise Http404
    if hasattr(event, '_tags_setter'):
        event._tags_setter(tags)
        return event
    return False