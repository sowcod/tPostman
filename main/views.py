#-*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import twoauth
from api import get_consumers

def create_oauth(token = '', token_secret = ''):
	(ckey, csecret) = get_consumers()
	return twoauth.oauth(ckey, csecret, token, token_secret)

def access_token(request):
	oauth = create_oauth()

	req_token = oauth.request_token()
	url = oauth.authorize_url(req_token)
	request.session['req_token'] = req_token

	return HttpResponseRedirect(url)

def auth(request):
	from models import Authorization

	verifier = request.GET['oauth_verifier']
	req_token = request.session['req_token']

	oauth = create_oauth()
	acc_token = oauth.access_token(req_token, verifier)

	try:
		auth = Authorization.objects.get(user_id = acc_token['user_id'])
	except Authorization.DoesNotExist:
		auth = Authorization(user_id = acc_token['user_id'])
	
	auth.screen_name = acc_token['screen_name']
	auth.token = acc_token['oauth_token']
	auth.token_secret = acc_token['oauth_token_secret']
	auth.save()

	del request.session['req_token']

	request.session['user_id'] = auth.user_id

	return HttpResponseRedirect('/')

def logout(request):
	request.session.clear()

	return HttpResponseRedirect('/')

def toppage(request):
	from models import Authorization
	try:
		user_id = request.session['user_id']
		auth = Authorization.objects.get(user_id = user_id)
		values = {'auth':auth}
		return render_to_response('main/member.html',
				values,
				RequestContext(request))
	except (Authorization.DoesNotExist, KeyError):
		return render_to_response('main/top.html')

def opentweet(request):
	from models import Authorization
	user_id = request.session['user_id']
	auth = Authorization.objects.get(user_id = user_id)
	values = {'auth':auth}
	return render_to_response('main/tweetwin.html',
			values,
			RequestContext(request))

