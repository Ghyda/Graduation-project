from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator


class Question(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    body = models.TextField(max_length=800)
    pub_date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, NULL=True, on_delete=models.SET_NULL)
    qualifications = models.CharField(max_length=200)
    answer_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.answer_text, self.user, ("Answer by %s on question %s" % (self.user,
                                            self.question.title))
        
class Comment(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    body = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body, self.user

    def __unicode__(self):
        return self.body, self.user, ("Comment by %s on answer %s" % (self.user,
                                            self.answer.title))

    
class Vote(models.Model):
    user = models.ForeignKey(User, NULL=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer)
    comment = models.ForeignKey(Comment)
    value = models.IntegerField(default=0)
    vote_time = models.DateTimeField(auto_now_add=True)

    def upvote(self):
        self.value += 1

    def downvote(self):
        self.value -= 1

    def __unicode__(self):
        pass


class Follow(models.Model):
    follow_time = models.DateTimeField(auto_now_add=True)
    following = models.ForeignKey(User)
    follower = models.ForeignKey(User)


class Profile(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='../accounts/uploads/')
    bio = models.TextField(max_length=300)
