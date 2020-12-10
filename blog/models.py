from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#for python scripts
from .plag import *
import docx2txt
import os
#import re
#from bs4 import BeautifulSoup
#import requests 

from difflib import SequenceMatcher

class Post(models.Model):
    content = models.CharField(max_length=255, blank=True)                         #changed
    document = models.FileField(upload_to='Assignments/')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    grammar = models.TextField(max_length=10000)
    onlinePlag= models.IntegerField(default=0)
    InternalPlag= models.IntegerField(default=0)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def get_absolute_url(self):
        return u'/post/%d' % self.id 

    def __str__(self):
        return self.content[:5]

    def save(self, *args, **kwargs): 
        doc = self.document
        plag=0
        if doc.name.endswith('.docx'):
            my_text = docx2txt.process(doc)
            #print(my_text)
        elif doc.name.endswith('.pdf'):
            pass
        elif doc.name.endswith('.txt'):
            pass
        links=extract_link(my_text)
        for link in links:
            page=scrape(link)
            cand_doc=get_document(page)
            seq_match=sequence_check(my_text,cand_doc)
            jac=plag_check(my_text,cand_doc)
            if seq_match>60:
                plag=max(plag,jac)
            else:
                plag= max(plag,seq_match)
        print('Online plag:',plag)
        self.onlinePlag=plag   
        #print(os.listdir) 
        
        #internal plagiarism
        internal_plag=0
        for fil in os.listdir(r'C:\Users\Pranay Chowdary\Desktop\finalplag\Final_dev_plagiarism_check\media\Assignments'):
            if fil.endswith('.docx'):
                my_friend_text = docx2txt.process('C:\\Users\\Pranay Chowdary\\Desktop\\finalplag\\Final_dev_plagiarism_check\\media\\Assignments\\'+fil)
                #print(my_text)
            elif fil.endswith('.pdf'):
                pass
            elif fil.endswith('.txt'):
                pass
            #my_friend_text = docx2txt.process('../media/Assignments'+fil)
            in_seq_match=sequence_check(my_text,my_friend_text)
            in_jac=plag_check(my_text,my_friend_text)
            if in_seq_match>60:
                internal_plag=max(internal_plag,in_jac)
            else:
                internal_plag= max(internal_plag,in_seq_match)

        print('Internal plag:',internal_plag) 
        self.InternalPlag=internal_plag
         

        #grammar checker
        '''
        checked= gram_check(my_text)
        print(checked)
        '''
        self.grammar='This is a place holder'



        return super(Post, self).save(*args, **kwargs) 
        

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()


class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)


class Preference(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")
