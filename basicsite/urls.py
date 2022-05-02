from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('<int:housing_id>/', views.detail, name='detail'),
    path('submit/', views.upload, name='submit'),
    path('<int:housing_id>/newreview/', views.newreview, name='newreview'),
    path('<int:housing_id>/newreview/submit_review', views.submit_review, name='submit_review'),
    path('Rating/', views.RatingView.as_view(), name='Rating'),
    path('Rating/lowest/', views.RatingViewLow.as_view(), name='Rating'),
    path('Price/', views.PriceView.as_view(), name='Price'),
    path('Price/highest', views.PriceViewHigh.as_view(), name='Price'),
    # path('maps/', views.default_map, name='maps'),
    #path('maps/', views.geocoding, name='geocoding'),
    path('maps/<int:housing_id>', views.geocoding2, name='geocoding2'),
    path('geocode/', views.geocoding, name='geocoding'),
    path('maps/', views.coordinates, name='coordinates')

]
