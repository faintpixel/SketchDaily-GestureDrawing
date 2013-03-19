from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext
from sketchdaily.models import *


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def imageViewer(request):
    image = GetNextImage(request)
    return render_to_response('imageViewer.html', {'image': image, 'minutes': 2, 'seconds': 0}, context_instance=RequestContext(request))


def startSession(request):
    request.session['gender'] = request.GET.get('gender', '')
    request.session['clothing'] = request.GET.get('clothing', '')
    request.session['pose'] = request.GET.get('pose', '')
    request.session['view'] = request.GET.get('view', '')
    request.session['time'] = request.GET.get('time', '')
    return imageViewer(request)


def GetNextImage(request):
    gender = request.session.get('gender', "")
    clothing = request.session.get('clothing', "")
    pose = request.session.get('pose', "")
    view = request.session.get('view', "")

    imagePool = ReferenceImage.objects.all()

    if gender != "":
        imagePool = imagePool.filter(tags__name=gender)
    if clothing != "":
        imagePool = imagePool.filter(tags__name=clothing)
    if pose != "":
        imagePool = imagePool.filter(tags__name=pose)
    if view != "":
        imagePool = imagePool.filter(tags__name=view)

    return imagePool.order_by('?')[0]
