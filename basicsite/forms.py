from django import forms
from .models import *

class HousingForm(forms.ModelForm):

    class Meta:
        model = Housing
        fields = ('name', 'description',
                  'price', 'address',#'available',
                  'numRooms', 'numBathrooms',
                  #'handicapAccessible',
                  'startRentalDate',
                  'endRentalDate','image')
        #I excluded rating, ratedYet, numReviews, and publishDate

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('review_text', 'rating')
