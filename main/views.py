#-*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import twoauth

_ckey = r'bXDe1Etl6queYlu6t6Ntvg'
_csecret = r'ifNrQpnXUxYsuJTMVo6A5wzLjB6FPlYRULY9WIquc'

def access_token(request):
	oauth = twoauth.oauth(_ckey, _csecret)

	req_token = oauth.request_token()
	url = oauth.authorize_url(req_token)
	request.session['req_token'] = req_token

	return HttpResponseRedirect(url)

def auth(request):
	from models import Authorization

	verifier = request.GET['oauth_verifier']
	req_token = request.session['req_token']

	oauth = twoauth.oauth(_ckey, _csecret)
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

def create_api(request):
	from models import Authorization
	user_id = request.session['user_id']
	auth = Authorization.objects.get(user_id = user_id)
	return twoauth.api(_ckey, _csecret, auth.token, auth.token_secret)

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

def tweet(request):
	import base64
	import pyDes
	api = create_api(request)
	tweet = request.GET['tweet']

	tweetbin = base64.b64decode(tweet)
	k = pyDes.des(request.session.session_key[:8], pyDes.ECB)
	tweetdec = k.decrypt(tweetbin)
	
	api.status_update(tweetdec)
	return HttpResponseRedirect('/')
