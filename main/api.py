#-*- coding: utf-8 -*-
import twoauth
import django

def get_consumers():
	from models import OAuthConsumer
	consumer = OAuthConsumer.objects.get(enabled = True)
	return str(consumer.key), str(consumer.secret)

def create_api(request):
	from models import Authorization
	user_id = request.session['user_id']
	auth = Authorization.objects.get(user_id = user_id)
	(ckey, csecret) = get_consumers()
	return twoauth.api(ckey, csecret, auth.token, auth.token_secret)

def tweet(request):
	import base64
	import pyDes
	import re
	import json
	api = create_api(request)
	tweet = request.GET['tweet']

	tweetbin = base64.b64decode(tweet)
	k = pyDes.des(request.session.session_key[:8], pyDes.ECB)
	tweetdec = k.decrypt(tweetbin)
	tweetrep = re.compile('\x05*$').sub('', tweetdec)
	
	content_type = 'application/json;charset=UTF-8'
	try :
		api.status_update(tweetrep)
		pass
	except :
		result = {'result': 'fail'}
		response = django.http.HttpResponseServerError(
				content = json.dumps(result), content_type=content_type)
	else:
		result = {"result": 'success'}
		response = django.http.HttpResponse(
				content = json.dumps(result), content_type=content_type)

	return response
