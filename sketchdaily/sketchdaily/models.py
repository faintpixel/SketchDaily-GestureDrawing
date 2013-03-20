from django.db import models
from django.contrib.auth.models import User


class ReferenceImage(models.Model):
    file = models.FileField(upload_to='sketchdaily/static/referenceImages')
    sourceURL = models.URLField(max_length=1000, blank=True)
    photographer = models.ForeignKey('Contact', related_name='photographer', blank=True)
    model = models.ForeignKey('Contact', related_name='model', blank=True)
    dateAdded = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __unicode__(self):
        return self.file.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    webpage = models.URLField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.webpage + ")"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Session(models.Model):
    images = models.ManyToManyField('ReferenceImage')
    dateCreated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.dateCreated


class UserSubmittedImage(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey('ReferenceImage')
    imageURL = models.URLField(max_length=500, blank=True)
    score = models.IntegerField()
    dateAdded = models.DateTimeField(auto_now=True)
