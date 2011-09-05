# coding=utf-8

   
def add_suggestion(request):
    from geoalert.views import add_suggestion
    return add_suggestion(request, template='add_suggestion.html')

