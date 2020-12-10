from django.test import TestCase, Client
from django.urls import reverse
from blog.models import *
import json
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from blog.views import *

class TestViews(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testname', email='testmail@…', password='top_secret')


    def test_about(self):
        

        response= self.client.get(reverse("blog-about"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

    
   # def test_post_update(self):
      #  request = self.factory.get('/post/new/')
      #  request.user = self.user
      #  request.user = AnonymousUser()
      #  response = PostCreateView(request)

      #  response = PostCreateView.as_view()(request)
       # self.assertEqual(response.status_code, 200)
        # response=self.client.get(reverse("post-create"))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, "blog/post_new.html")

