from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)
CLOTHING_CHOICES = (
    (1, 'Clothed'),
    (2, 'Nude'),
)
POSE_CHOICES = (
    (1, 'Action'),
    (2, 'Stationary'),
)
VIEW_CHOICES = (
    (1, 'Front'),
    (2, 'Side'),
    (3, 'Back'),
    (4, 'Above/Below'),
)
SPECIES_CHOICES = (
    (1, 'Bird'),
    (2, 'Fish'),
    (3, 'Reptile/Amphibian'),
    (4, 'Bug'),
    (5, 'Mammal'),
)
BODY_PART_CHOICES = (
    (1, 'Hand'),
    (2, 'Foot'),
    (3, 'Head'),
)
LIFE_CATEGORIES = (
    (1, 'Living'),
    (2, 'Skeletons/Bones'),
)


class ReferenceImage(models.Model):
    file = models.FileField(upload_to='sketchdaily/static/referenceImages')
    sourceURL = models.URLField(max_length=1000, blank=True)
    photographer = models.ForeignKey('Contact', related_name='photographer', blank=True, null=True)
    model = models.ForeignKey('Contact', related_name='model', blank=True, null=True)
    dateAdded = models.DateTimeField(auto_now=True)
    nudity = models.BooleanField()
    termsOfUse = models.ForeignKey('TermsOfUse', related_name='termsOfUse', blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    def thumbnail(self):
        imageLink = u"http://reference.sketchdaily.net" + self.file.url[11:]
        if self.file:
            return u'<img style="width: 125px; height:125px;" src="%s" />' % imageLink
        else:
            return '(no thumbnail)'
    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True


class FullBodyReference(models.Model):
    image = models.ForeignKey('ReferenceImage')
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    clothing = models.IntegerField(choices=CLOTHING_CHOICES, blank=True, null=True)
    pose = models.IntegerField(choices=POSE_CHOICES, blank=True, null=True)
    view = models.IntegerField(choices=VIEW_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return self.image.file.name[35:]


class AnimalReference(models.Model):
    image = models.ForeignKey('ReferenceImage')
    species = models.IntegerField(choices=SPECIES_CHOICES, blank=True, null=True)
    category = models.IntegerField(choices=LIFE_CATEGORIES, blank=True, default=1, null=True)
    view = models.IntegerField(choices=VIEW_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return self.image.file.name


class BodyPartReference(models.Model):
    image = models.ForeignKey('ReferenceImage')
    bodyPart = models.IntegerField(choices=BODY_PART_CHOICES, blank=True, null=True)
    view = models.IntegerField(choices=VIEW_CHOICES, blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return "(" + self.get_bodyPart_display() + ") " + self.image.file.name[35:]


class Contact(models.Model):
    name = models.CharField(max_length=200)
    webpage = models.URLField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.webpage + ")"


class TermsOfUse(models.Model):
    name = models.CharField(max_length=200)
    keyTerms = models.TextField(max_length=2000)
    fullTermsURL = models.URLField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.fullTermsURL + ")"


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
