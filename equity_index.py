import redis
import os
import cherrypy
import pickle
from cherrypy.process.servers import ServerAdapter
from wsgiserver import WSGIServer
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader= file_loader)


class StockInfo(object):
	# @cherrypy.expose
	# def index(self):
	# 	self.conn = redis.Redis(host='localhost', port=6379, db=1)
	# 	top_ten_dict = {}
	# 	top10_stock_names = [item.decode("utf-8") for item in self.conn.keys()[:10]]
		
	# 	for key in top10_stock_names:
	# 		top_ten_dict[key] = eval(self.conn.get(key).decode("utf-8"))
	# 		if len(top_ten_dict) == 10:
	# 			break

	# 	templ = env.get_template("top_10_stock.html")
	# 	return templ.render(data=top_ten_dict)

	@cherrypy.expose
	def index(self):
		self.conn = pickle.load(open("equity_data_dict.pickle", "rb"))
		top_ten_dict = {}
		top10_stock_names = [item for item in list(self.conn.keys())[:10]]
		
		for key in top10_stock_names:
			top_ten_dict[key] = self.conn.get(key)
			if len(top_ten_dict) == 10:
				break

		templ = env.get_template("top_10_stock.html")
		return templ.render(data=top_ten_dict)


	# @cherrypy.expose	
	# def get_stock(self, name):
	# 	self.conn = redis.Redis(host='localhost', port=6379, db=1)
	# 	search_data = self.conn.get(name.lower()).decode("utf-8")
	# 	search_data = eval(search_data)
	# 	print("eval(search_data)", search_data)
	# 	search_data['NAME'] = name.capitalize()


	# 	templ = env.get_template("get_stock.html")
	# 	return templ.render(data=search_data)
	@cherrypy.expose	
	def get_stock(self, name):
		self.conn = pickle.load(open("equity_data_dict.pickle", "rb"))

		search_data = self.conn.get(name.strip().lower())
		if search_data is None:
			templ = env.get_template("get_stock.html")
			return templ.render(data=search_data)
		
		search_data['NAME'] = name

		templ = env.get_template("get_stock.html")
		return templ.render(data=search_data)

if __name__ == '__main__':
	config = {
		    'global': {
		        'server.socket_host': '0.0.0.0',
		        'server.socket_port': int(os.environ.get('PORT', 5000)),
		    },
		    '/static': {
		        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
		        'tools.staticdir.on': True,
		        'tools.staticdir.dir': 'static',
		    }
		}
	cherrypy.quickstart(StockInfo(), '/', config=config)
	#server = WSGIServer(StockInfo())
	#server.start()
	


 


