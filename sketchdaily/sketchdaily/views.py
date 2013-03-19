from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext
from sketchdaily.models import *


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def imageViewer(request):
    minutes = request.session.get('time-minutes', 1)
    seconds = request.session.get('time-minutes', 11)

    action = request.GET.get('action', '')
    if action == "rewind":
        image = getPreviousImage(request)
    else:
        image = getNextImage(request)

    return render_to_response('imageViewer.html', {'image': image, 'minutes': minutes, 'seconds': seconds}, context_instance=RequestContext(request))


def getNextImage(request):
    rewoundImages = request.session.get('rewoundImages', [])
    drawnImages = request.session.get('drawnImages', [])
    if len(rewoundImages) > 0:
        imageId = rewoundImages.pop()
        image = ReferenceImage.objects.get(id=imageId)
        drawnImages.append(image.id)
        request.session['drawnImages'] = drawnImages
        request.session['rewoundImages'] = rewoundImages
    else:
        image = GetNextImage(request)

    return image


def getPreviousImage(request):
    rewoundImages = request.session.get('rewoundImages', [])
    drawnImages = request.session.get('drawnImages', [])
    if len(drawnImages) > 1:
        currentImage = drawnImages.pop()
        rewoundImages.append(currentImage)
        previousId = drawnImages.pop()
        image = ReferenceImage.objects.get(id=previousId)
        drawnImages.append(image.id)
        request.session['drawnImages'] = drawnImages
        request.session['rewoundImages'] = rewoundImages
    else:
        image = GetNextImage(request)

    return image


def startSession(request):
    request.session['gender'] = request.GET.get('gender', '')
    request.session['clothing'] = request.GET.get('clothing', '')
    request.session['pose'] = request.GET.get('pose', '')
    request.session['view'] = request.GET.get('view', '')
    request.session['time'] = request.GET.get('time', '')
    request.session['drawnImages'] = []
    request.session['rewoundImages'] = []

    splitTime = request.GET.get('time', '1:11').split(":")
    request.session['time-minutes'] = splitTime[0]
    request.session['time-seconds'] = splitTime[1]

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
        drawnImages.pop(0)
        imagePool = ReferenceImage.objects.all()
        for image in drawnImages:
            imagePool = imagePool.exclude(id=image)

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
