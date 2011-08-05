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