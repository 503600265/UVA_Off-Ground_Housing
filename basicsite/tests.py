from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse
from django.core import mail
from .models import Housing, Review
from .forms import HousingForm
from cloudinary.models import CloudinaryField

# Create your tests here.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2

    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class LogInTest(TestCase):
    # Login User
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('123456789')
        user.save()

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='123456789')
        self.assertTrue(logged_in)

    def test_authentification(self):
        c = Client() #annoying how I have to respecify this
        c.login(username='testuser', password='123456789')
        User = get_user_model()
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        c = Client()
        logged_in = c.login(username='testuser', password='123456789')
        self.assertTrue(logged_in) #making sure logged_in works for logout to also work
        User = get_user_model()
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated) #necessary to test before testing logout
        c.logout()
        self.assertFalse(user.is_anonymous)

class Submission(TestCase):
    #testing object creation
    def createListing(self, name="test", description="test_desc", address="123 Cherry Grove", price=100.21, rating=0,\
                      ratedYet=True,numReviews=1,numRooms=1,numBathrooms=1,publishDate=datetime.now(),\
                      startRentalDate="1/1/11", endRentalDate="12/12/12"):
        return Housing.objects.create(name=name,description=description,address=address,price=price,rating=rating,\
                                      ratedYet=ratedYet,numReviews=numReviews,numRooms=numRooms,
                                      numBathrooms=numBathrooms,publishDate=publishDate,\
                                      startRentalDate=startRentalDate,endRentalDate=endRentalDate)

    #testing if object was created correctly using getters
    def test_creation_and_getters(self):
        test_object = self.createListing()
        self.assertTrue(isinstance(test_object, Housing))
        self.assertEqual(test_object.__str__(), test_object.name)
        self.assertEqual(test_object.get_description(), test_object.description)
        self.assertEqual(test_object.has_reviews(), test_object.ratedYet)
        self.assertEqual(test_object.get_current_rating(), test_object.rating)
        self.assertTrue(test_object.get_numReviews(), test_object.numReviews)
        self.assertTrue(test_object.get_price(), test_object.price)

    #tests validity of this form
    def test_valid_form(self):
        test_object = Housing.objects.create(name="Test", description="Test_Desc", address="123 Cherry Grove",\
                                             price=100.00, numRooms=1, numBathrooms=1,\
                                             startRentalDate="1/1/11", endRentalDate="12/12/12")
        data = {'name':test_object.name, 'description':test_object.description,'address':test_object.address, 'price':test_object.price,\
                'numRooms':test_object.numRooms, 'numBathrooms':test_object.numBathrooms,\
                'startRentalDate':test_object.startRentalDate, 'endRentalDate':test_object.endRentalDate}
        form = HousingForm(data=data)
        self.assertTrue(form.is_valid())

    #correctly returns false for an invalid form
    def test_invalid_form(self):
        test_object = Housing.objects.create(name="Test", description="",address="123 Cherry Grove",\
                                             price=100.00, numRooms=1, numBathrooms=1,\
                                             startRentalDate="1/1/11", endRentalDate="12/12/12")
        data = {'name': test_object.name, 'description': test_object.description,'address':test_object.address,'price': test_object.price, \
                'numRooms': test_object.numRooms, 'numBathrooms': test_object.numBathrooms, \
                'startRentalDate': test_object.startRentalDate, 'endRentalDate': test_object.endRentalDate}
        form = HousingForm(data=data)
        self.assertFalse(form.is_valid())

class List_Testing(TestCase):
    #copied from under submission
    def createListing(self, name="test", description="test_desc", address="123 Cherry Grove", price=100.21, rating=0,\
                      ratedYet=True,numReviews=1,numRooms=1,numBathrooms=1,publishDate=datetime.now(),\
                      startRentalDate="1/1/11", endRentalDate="12/12/12"):
        return Housing.objects.create(name=name,description=description,address=address,price=price,rating=rating,\
                                      ratedYet=ratedYet,numReviews=numReviews,numRooms=numRooms,
                                      numBathrooms=numBathrooms,publishDate=publishDate,\
                                      startRentalDate=startRentalDate,endRentalDate=endRentalDate)

    #verifies list order
    def test_list_order_basic(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        housing_object2 = self.createListing()
        housing_object2.name = "test1"
        housing_object2.save()
        self.assertTrue(Housing.objects.filter(price=100.21).first().name, "test")
        self.assertTrue(Housing.objects.filter(price=100.21).last().name, "test1")

    #rating descending
    def test_rating_ascending(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        housing_object2 = self.createListing()
        housing_object2.rating = 1
        housing_object2.save()
        self.assertEqual(Housing.objects.filter(name="test").order_by('rating').first().rating, 0)
        self.assertEqual(Housing.objects.filter(name="test").order_by('rating').last().rating, 1)

    def test_rating_descending(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        housing_object2 = self.createListing()
        housing_object2.rating = 1
        housing_object2.save()
        self.assertEqual(Housing.objects.filter(name="test").order_by('-rating').first().rating, 1)
        self.assertEqual(Housing.objects.filter(name="test").order_by('-rating').last().rating, 0)

    def test_price_ascending(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        housing_object2 = self.createListing()
        housing_object2.price = 100.22
        housing_object2.save()
        self.assertEqual(Housing.objects.filter(name="test").order_by('price').first().price, 100.21)
        self.assertEqual(Housing.objects.filter(name="test").order_by('price').last().price, 100.22)

    def test_price_descending(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        housing_object2 = self.createListing()
        housing_object2.price = 100.22
        housing_object2.save()
        self.assertEqual(Housing.objects.filter(name="test").order_by('-price').first().price, 100.22)
        self.assertEqual(Housing.objects.filter(name="test").order_by('-price').last().price, 100.21)

    def test_review_field(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        Review5 = Review.objects.create(housing=housing_object1, review_text="Testing", rating=5)
        Review5.save()
        self.assertEqual(Review5.housing, housing_object1)
        self.assertEqual(Review5.review_text, "Testing")
        self.assertEqual(Review5.rating, 5)

    def test_multiple_reviews(self):
        housing_object1 = self.createListing()
        housing_object1.save()
        Review5 = Review.objects.create(housing=housing_object1, review_text="Testing", rating=5)
        Review5.save()
        Review2 = Review.objects.create(housing=housing_object1, review_text="Testing2", rating=2)
        Review2.save()
        Review4 = Review.objects.create(housing=housing_object1, review_text="Testing4", rating=4)
        Review4.save()
        self.assertEqual(round((Review5.rating + Review2.rating + Review4.rating)/3, 2), 3.67)

    