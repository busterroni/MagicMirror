import web, json, requests, random, time
from random import randint

urls = (
	'/', 'Index',
	'/alexa', 'Alexa',
	'/r', 'Refresh'
)

# from web.wsgiserver import CherryPyWSGIServer
# CherryPyWSGIServer.ssl_certificate = '/etc/nginx/ssl/nginx.crt'
# CherryPyWSGIServer.ssl_private_key = '/etc/nginx/ssl/nginx.key'

app = web.application(urls, globals())
render = web.template.render('templates/')

class Index:
	def GET(self):

		##################
		#    0 = white-tshirt            #
		#    1 = blue-tank
		#    2 = phillies-shirt
		#    3 = 
		#
		#
		#
		#
		#
		#
		#
		##################
		web.header('Transfer-Encoding', 'chunked')

		temperature = requests.get('https://api.darksky.net/forecast/').json()['currently']
		temp_f = int(temperature['temperature'])
		# temp_f = 100
		summary = temperature['summary']
		weather_icon = temperature['icon']
		temp_f = 80

		if temp_f < 40:
			rand_top = randint(6, 8)
			rand_bottom = randint(0, 2)
			rand_beanie = randint(0, 2)
		elif temp_f < 70:
			rand_top = randint(6, 9)
			rand_bottom = randint(0, 2)
		else:
			rand_top = randint(0, 4)
			rand_bottom = randint(10, 11)
			rand = random.random()
			if rand > .5:
				rand_sunglasses = randint(0, 1)
		try:
			return render.index(temp_f, summary, weather_icon, rand_top, rand_bottom, rand_beanie)
		except UnboundLocalError:
			pass

		try:
			return render.index(temp_f, summary, weather_icon, rand_top, rand_bottom, rand_sunglasses)
		except UnboundLocalError:
			pass


		return render.index(temp_f, summary, weather_icon, rand_top, rand_bottom)


class Alexa:
	def POST(self):
		web.header('Transfer-Encoding', 'chunked')
		response = "Good morning Jonathan, head on over to your mirror for a status report! "

		weather = requests.get('https://api.darksky.net/forecast/')
		
		temperature = int(requests.get('https://api.darksky.net/forecast/').json()['currently']['temperature'])
		temperature = 80
		response += "It's currently " + str(temperature) + " degrees. "

		if temperature < 40:
			response += "Brrr! It's cold outside. I've recommended some jackets and pants for you to wear."
		if temperature < 70:
			response += "It's a little chilly outside. I've recommended a sweatshirt for you."
		else:
			response += "It's warm outside! I've recommended you wear some clothes for warm weather. Enjoy the sun!"

		data = {}
		data['version'] = '1.0'
		data['response'] = {"outputSpeech": {"type": "PlainText", "text": response}}

		return json.dumps(data)

if __name__=='__main__':
	app.run()