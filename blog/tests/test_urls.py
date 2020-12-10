from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import PostListView, UserPostListView, PostDeleteView, PostUpdateView
from blog.views import *



class TestUrls(SimpleTestCase):


    def test_blog(self):
        url=reverse("blog-home")
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_blog_about(self):
        url=reverse("blog-about")
        self.assertEquals(resolve(url).func, about)
    
    def test_postupdate(self):
        url= reverse("post-update",args=[1])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)
    
    def test_postdelete(self):
        url=reverse("post-delete",args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_postcreate(self):
        url=reverse("post-create")
        self.assertEquals(resolve(url).func.view_class, PostCreateView)
    
    def test_postdetail(self):
        url=reverse("post-detail",args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_user_posts(self):
        url=reverse("user-posts",args=["abc"])
        self.assertEquals(resolve(url).func.view_class, UserPostListView)

    def test_user_follows(self):
        url=reverse("user-follows",args=["abc"])
        self.assertEquals(resolve(url).func.view_class, FollowsListView)

    
    


    
    

    