from django.views import generic, View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Housing, Review
from .forms import HousingForm, ReviewForm
from cloudinary.forms import cl_init_js_callbacks
import pandas as pd
from geopy.geocoders import Nominatim


# Create your views here.
def index(request):
    # This is hardcoded, in the future we can write a function to sort this list
    # housing_list = Housing.objects.order_by('-pub_date')[:5] THis is like tutorial may use this kind of orderby later
    housing_list = Housing.objects.all()
    rating_list = Housing.objects.all().order_by('rating')
    price_list = Housing.objects.all().order_by('price')
    context = {
        'housing_list': housing_list,
        'rating_list': rating_list,
        'price_list': price_list
    }
    return render(request, 'basicsite/index.html', context)

def detail(request, housing_id):
    housing = get_object_or_404(Housing, pk=housing_id)
    return render(request, 'basicsite/detail.html', {'housing': housing})

def about(request):
    return render(request, 'basicsite/about.html')

class NameView(ListView):
    template_name = 'basicsite/index.html'

    def get_queryset(self):
        """
        sorts by name
        """
        return Housing.objects.all().order_by('name')

class RatingView(ListView):
    template_name = 'basicsite/index.html'

    def get_queryset(self):
        """
        sorts by ratings (high to low)
        """
        return Housing.objects.all().order_by('-rating')

class RatingViewLow(ListView):
    template_name = 'basicsite/index.html'

    def get_queryset(self):
        """
        sorts by ratings (low to high)
        """
        return Housing.objects.all().order_by('rating')

class PriceView(ListView):
    template_name = 'basicsite/index.html'

    def get_queryset(self):
        """
        sorts by price (low to high)
        """
        return Housing.objects.all().order_by('price')

class PriceViewHigh(ListView):
    template_name = 'basicsite/index.html'

    def get_queryset(self):
        """
        sorts by price high to low
        """
        return Housing.objects.all().order_by('-price')

def some_view(request):
    my_products = Housing.objects.all().order_by('-rating')
    return render(request, 'basicsite/index.html')

# def submitpage(request):
#     if request.method == "POST":
#         Housing_Form = HousingForm(request.POST,request.FILES)
#         #print(Housing_Form.errors)
#         if Housing_Form.is_valid():
#             object = Housing_Form.save()
#             object.name = Housing_Form["name"].data
#             object.description = Housing_Form["description"].data
#             object.address = Housing_Form["address"].data
#             object.price = Housing_Form['price'].data
#             #object.rating = 0
#             object.ratedYet = False
#             object.numRooms = Housing_Form["numRooms"].data
#             object.numBathrooms = Housing_Form["numBathrooms"].data
#             object.publishDate = timezone.now()
#             object.startRentalDate = Housing_Form['startRentalDate'].data
#             object.endRentalDate = Housing_Form['endRentalDate'].data
#             object.image = Housing_Form['image'].data
#             object.save()
#         if not Housing_Form.is_valid():
#             return render(request=request, template_name="basicsite/failedsubmit.html")
#     return render(request, "basicsite/housingsubmit.html", {'form' : Housing_Form})

def upload(request):
  context = dict( backend_form = HousingForm())
  if request.method == 'POST':
    form = HousingForm(request.POST, request.FILES)
    context['posted'] = form.instance
    if form.is_valid():
        form.save()
    if not form.is_valid():
        return render(request=request, template_name="basicsite/failedsubmit.html")
  return render(request, 'basicsite/housingsubmit.html', context)
# def newreview(request, housing_id):
#     housing = get_object_or_404(Housing, pk=housing_id)
#     print("new rev ran")
#     if request.method == "POST":
#         print("post ran")
#         Review_Form = ReviewForm(request.POST)
#         # print(Review_Form.errors)
#         if Review_Form.is_valid():
#             housing.review_set.create(review_text=Review_Form["review_text"].data, rating=Review_Form["rating"].data)
#             print("valid ran")
#             if housing.ratedYet == False:
#                 print("if ran")
#                 housing.ratedYet = True
#                 housing.numReviews = 1
#                 housing.rating = Review_Form["rating"].data
#             else:
#                 housing.numReviews += 1

#             #return HttpResponseRedirect(reverse('basicsite:detail', args=(housing_id)))
#             #submit_review(housing_id)
#             # object = Review_Form.save()
#             # object.review_text = Review_Form["review_text"].data
#             # object.rating = Review_Form["rating"].data
#             # object.save()
#     return render(request, "basicsite/newreview.html", {'housing': housing})

def newreview(request, housing_id):
    housing = get_object_or_404(Housing, pk=housing_id)
    template = loader.get_template('basicsite/newreview2.html')
    context = {
        "housing": housing
    }
    return HttpResponse(template.render(context, request))

def submit_review(request, housing_id):
    housing = get_object_or_404(Housing, pk=housing_id)
    try:
        housing.review_set.create(review_text=request.POST['review_text'], rating=request.POST['rating'])
    except (KeyError, Review.DoesNotExist):
        # return render(request=request, template_name="basicsite/failedsubmit.html")
        return render(request, 'basicsite/failedreview.html', {
            'housing' : housing,
        })
    else:
        rating_list = housing.review_set.all()
        numRatings = housing.review_set.count()
        rating_sum = 0
        for i in range(len(rating_list)):
            rating_sum += rating_list[i].rating
        housing.rating = rating_sum/numRatings
        housing.numReviews += 1
        if housing.ratedYet == False:
            housing.ratedYet = True
        housing.save()


    # old rating update method, keeping if needed as reference
    # if housing.ratedYet == False:
    #     print("if ran")
    #     housing.ratedYet = True
    #     housing.numReviews = 1
    #     housing.rating = request.POST['rating']
    #     housing.save()
    # else:
    #     oldRating = housing.rating
    #     oldNumReviews = housing.numReviews
    #     newRating = float(request.POST['rating'])
    #     print(type(newRating))
    #     housing.rating = ((oldRating*oldNumReviews) + newRating)/(oldNumReviews+1)
    #     housing.numReviews += 1
    #     housing.save()
    # Response.objects.all().create(response_text=request.POST['newResponse'])
    return HttpResponseRedirect(reverse('basicsite:detail', args=(housing_id,)))


def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'basicsite/maps.html',{ 'mapbox_access_token': mapbox_access_token})

def geocoding(request):
    housing_list = Housing.objects.all()
    rating_list = Housing.objects.all().order_by('rating')
    price_list = Housing.objects.all().order_by('price')
    housing_addresses = []
    for i in range(len(housing_list)):
        address = housing_list[i].address
        housing_addresses.append(address)

    if (len(housing_addresses) == 0):
        selected_housing = []
    else:
        selected_housing = housing_addresses[0]

    context = {
        'selected_housing': selected_housing,
        'housing_addresses': housing_addresses,
        'housing_list': housing_list,
        'rating_list': rating_list,
        'price_list': price_list
    }
    return render(request, 'basicsite/geocoding.html', context)

def geocoding2(request, housing_id):
    housing_list = Housing.objects.all()
    rating_list = Housing.objects.all().order_by('rating')
    price_list = Housing.objects.all().order_by('price')
    housing_addresses = []
    for i in range(len(housing_list)):
        address = housing_list[i].address
        housing_addresses.append(address)
    # selected_housing = housing_addresses[0]
    this_housing = Housing.objects.get(pk=housing_id)
    selected_housing = this_housing.address
    context = {
        'id': housing_id,
        'selected_housing': selected_housing,
        'housing_addresses': housing_addresses,
        'housing_list': housing_list,
        'rating_list': rating_list,
        'price_list': price_list
    }
    return render(request, 'basicsite/geocoding2.html', context)

def coordinates(request):
    geolocator = Nominatim(user_agent="basicsite")
    housing_list = Housing.objects.all()
    housing_addresses = []
    coordinates = []
    address_string_indices = []
    name_string_indices = []
    next_string_index = 7
    next_name_index = 7
    ids = []
    housing_names = []
    for i in range(len(housing_list)):
        address = housing_list[i].address
        name = housing_list[i].name
        location = (geolocator.geocode(address))
        if location==None:
            continue
        else:
            coordinates.append([location.longitude, location.latitude])
            housing_addresses.append(address)
            address_string_indices.append([next_string_index, next_string_index+len(address)])
            name_string_indices.append([next_name_index, next_name_index+len(name)])
            next_name_index = next_name_index + len(name) + 14
            next_string_index = next_string_index + len(address) + 14
            ids.append(housing_list[i].id)
            housing_names.append(name)

    rating_list = Housing.objects.all().order_by('rating')
    price_list = Housing.objects.all().order_by('price')
    context = {
        'housing_addresses': housing_addresses,
        'housing_list': housing_list,
        'rating_list': rating_list,
        'price_list': price_list,
        'coordinates': coordinates,
        'indices': address_string_indices,
        'names': name_string_indices,
        'ids' : ids,
        'housing_names': housing_names
    }
    return render(request, 'basicsite/coordinates.html', context)

#def submit_review(housing_id):
    #housing = get_object_or_404(Housing, pk=housing_id)
    #return HttpResponseRedirect(reverse('basicsite:detail', args=(housing_id)))
    # housing = get_object_or_404(Housing, pk=housing_id)
    # try:
    #     selected_choice = housing.review_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
