#-*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

class Authorization(models.Model):
	user_id = models.CharField(max_length = 20, primary_key = True)
	screen_name = models.CharField(max_length = 20)
	token = models.CharField(max_length = 100)
	token_secret = models.CharField(max_length = 100)

class OAuthConsumer(models.Model):
	enabled = models.BooleanField()
	key = models.CharField(max_length = 100)
	secret = models.CharField(max_length = 100)

admin.site.register(OAuthConsumer)
