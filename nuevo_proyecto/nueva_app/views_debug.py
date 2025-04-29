from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound

def debug_500(request):
    return HttpResponseServerError(render(request, "500.html"))

def debug_403(request):
    return HttpResponseForbidden(render(request, "403.html"))

def debug_404(request):
    return HttpResponseNotFound(render(request, "404.html"))
