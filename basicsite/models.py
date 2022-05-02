import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from cloudinary.models import CloudinaryField

class Housing(models.Model):
    # need to create a location field as well as others
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    address = models.CharField(max_length=1000, default = 'No Address Entered')
    # rating is an average of the number of reviews created
    rating = models.FloatField(null=True)# null = True means this isn't a required field for submission
    ratedYet = models.BooleanField(default=False)
    numReviews = models.IntegerField(default=0)
    #available = models.BooleanField()
    numRooms = models.IntegerField(default=0)
    numBathrooms = models.IntegerField(default=0)
    #handicapAccessible = models.BooleanField(default=False)
    publishDate = models.DateTimeField('date published', null=True)
    startRentalDate = models.CharField(max_length=500, null=True)
    endRentalDate = models.CharField(max_length=500, null=True)
    image = CloudinaryField('image', blank=True,null=True)

    # add images
    def __str__(self):
        return self.name
    def get_description(self):
        return self.description
    def has_reviews(self):
        return self.ratedYet
    def get_current_rating(self):
        return self.rating
    def get_numReviews(self):
        return self.numReviews
    def get_price(self):
        return self.price

    @admin.display(
        ordering='publish date',
        description='Publish Date',
    )
    def when_published(self):
        return self.publishDate

class Review(models.Model):
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=2000)
    rating = models.IntegerField()
    # add images
    def __str__(self):
        return self.review_text
    # possibly change to have a title as well

class Image(models.Model):
     title = models.CharField(max_length=200)
     image = models.ImageField(upload_to='images')

     def __str__(self):
         return self.title
