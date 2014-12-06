import json, requests, urllib

def bingTranslate(text,origin='zh-CHS',to='en'):

	args = {
		'client_id': 'wangwangxianbei_2014',#your client id here
		'client_secret': 'ZhzP5sHEpYemPvnccRxO5dfc6Oytxi2ZrfZfDwTQG60=',#your azure secret here
		'scope': 'http://api.microsofttranslator.com',
		'grant_type': 'client_credentials'
		}
	oauth_url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
	oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)
	translation_args = {
		'text': text,
		'to': to,
		'from': origin
		}
	headers={'Authorization': 'Bearer '+oauth_junk['access_token']}
	translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
	translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
	return translation_result.content
		