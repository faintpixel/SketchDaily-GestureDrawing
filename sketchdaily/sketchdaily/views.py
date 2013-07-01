from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext
from sketchdaily.models import *


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def help(request):
    return render_to_response('help.html', {}, context_instance=RequestContext(request))


def imageViewer(request):
    minutes = request.session.get('time-minutes', 1)
    seconds = request.session.get('time-seconds', 11)

    action = request.GET.get('action', '')
    if action == "rewind":
        image = getPreviousImage(request)
    else:
        try:
            image = getNextImage(request)
        except Exception:
            return render_to_response('error.html', {'message': "No images found matching your criteria."})

    return render_to_response('imageViewer.html', {'image': image, 'minutes': minutes, 'seconds': seconds}, context_instance=RequestContext(request))


def getNextImage(request):
    history = request.session.get('fullHistory', [])
    historyPosition = request.session.get('historyPosition', 0)

    if historyPosition != 0:
        historyPosition += 1
        request.session['historyPosition'] = historyPosition
        historyIndex = len(history) + historyPosition - 1  # this is awkward
        image = FullBodyReference.objects.get(id=history[historyIndex])
    else:
        image = getNextImageForSession(request)


    return image


def getPreviousImage(request):
    history = request.session.get('fullHistory', [])
    historyPosition = request.session.get('historyPosition', 0)
    historyPosition -= 1

    historyIndex = len(history) + historyPosition - 1  # oh god what am i doing
    if historyIndex >= 0:
        request.session['historyPosition'] = historyPosition
    else:
        historyIndex = 0

    image = FullBodyReference.objects.get(id=history[historyIndex])
    return image


def startSession(request):
    imageType = request.GET.get('imageType', '')
    request.session['imageType'] = imageType
    request.session['time'] = request.GET.get('time', '')
    request.session['drawnImages'] = []
    request.session['fullHistory'] = []
    request.session['historyPosition'] = 0

    splitTime = request.GET.get('time', '1:11').split(":")
    request.session['time-minutes'] = splitTime[0]
    request.session['time-seconds'] = splitTime[1]

    if imageType == 'animals':
        imagePool = startAnimalSession(request)
    elif imageType == 'bodyParts':
        imagePool = startBodyPartSession(request)
    else:
        imagePool = startFullBodySession(request)

    return imageViewer(request)


def startFullBodySession(request):
    request.session['gender'] = request.GET.get('gender', '')
    request.session['clothing'] = request.GET.get('clothing', '')
    request.session['pose'] = request.GET.get('pose', '')
    request.session['view'] = request.GET.get('view', '')
    request.session['showNSFW'] = request.GET.get('showNSFW', False)


def startBodyPartSession(request):
    request.session['view'] = request.GET.get('view', '')
    request.session['gender'] = request.GET.get('gender', '')
    request.session['bodyPart'] = request.GET.get('bodyPart', '')


def startAnimalSession(request):
    request.session['view'] = request.GET.get('view', '')
    request.session['species'] = request.GET.get('species', '')
    request.session['category'] = request.GET.get('category', '')


def getNextImageForSession(request):
    drawnImages = request.session.get('drawnImages', [])
    history = request.session.get('fullHistory', [])
    imageType = request.session.get('imageType', '')

    if imageType == 'animals':
        imagePool = getAnimalReference(request)
    elif imageType == 'bodyParts':
        imagePool = getBodyPartReference(request)
    else:
        imagePool = getFullBodyReference(request)

    filteredImagePool = imagePool
    for image in drawnImages:
        filteredImagePool = filteredImagePool.exclude(id=image)

    if len(imagePool) == 0:
        raise Exception('No images match selected criteria.')

    if len(filteredImagePool) == 0:
        drawnImages.pop(0)  # once we have more images we can probably drop this and just clear the whole drawnImages list
        filteredImagePool = imagePool
        for image in drawnImages:
            filteredImagePool = filteredImagePool.exclude(id=image)

    selectedImage = filteredImagePool.order_by('?')[0]
    drawnImages.append(selectedImage.id)
    history.append(selectedImage.id)
    request.session['drawnImages'] = drawnImages
    request.session['fullHistory'] = history
    return selectedImage


def getFullBodyReference(request):
    gender = request.session.get('gender', "")
    clothing = request.session.get('clothing', "")
    pose = request.session.get('pose', "")
    view = request.session.get('view', "")
    showNSFW = request.session.get('showNSFW', False)

    imagePool = FullBodyReference.objects.all()
    if gender != "":
        imagePool = imagePool.filter(gender=gender)
    if clothing != "":
        imagePool = imagePool.filter(clothing=clothing)
        if clothing == "1":
            if showNSFW == False:
                imagePool = imagePool.filter(image__nudity=False)
    if pose != "":
        imagePool = imagePool.filter(pose=pose)
    if view != "":
        imagePool = imagePool.filter(view=view)


    return imagePool


def getAnimalReference(request):
    view = request.session.get('view', "")
    species = request.session.get('species', "")
    category = request.session.get('category', "")

    imagePool = AnimalReference.objects.all()
    if view != "":
        imagePool = imagePool.filter(view=view)
    if species != "":
        imagePool = imagePool.filter(species=species)
    if category != "":
        imagePool = imagePool.filter(category=category)

    return imagePool


def getBodyPartReference(request):
    view = request.session.get('view', "")
    gender = request.session.get('gender', "")
    bodyPart = request.session.get('bodyPart', "")

    imagePool = BodyPartReference.objects.all()
    if view != "":
        imagePool = imagePool.filter(view=view)
    if gender != "":
        imagePool = imagePool.filter(gender=gender)
    if bodyPart != "":
        imagePool = imagePool.filter(bodyPart=bodyPart)

    return imagePool