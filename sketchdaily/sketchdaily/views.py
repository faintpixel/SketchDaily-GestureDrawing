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
    request.session['drawnImages'] = []
    return imageViewer(request)


def GetNextImage(request):
    gender = request.session.get('gender', "")
    clothing = request.session.get('clothing', "")
    pose = request.session.get('pose', "")
    view = request.session.get('view', "")
    drawnImages = request.session.get('drawnImages', [])

    imagePool = ReferenceImage.objects.all()
    for image in drawnImages:
        imagePool = imagePool.exclude(id=image)

    if len(imagePool) == 0:
        drawnImages = []
        imagePool = ReferenceImage.objects.all()

    if gender != "":
        imagePool = imagePool.filter(tags__name=gender)
    if clothing != "":
        imagePool = imagePool.filter(tags__name=clothing)
    if pose != "":
        imagePool = imagePool.filter(tags__name=pose)
    if view != "":
        imagePool = imagePool.filter(tags__name=view)

    selectedImage = imagePool.order_by('?')[0]
    drawnImages.append(selectedImage.id)
    request.session['drawnImages'] = drawnImages
    return selectedImage
