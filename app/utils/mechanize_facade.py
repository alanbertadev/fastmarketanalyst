import mechanize
import cookielib

class MechanizeFacade:
	
	def __init__(self):

		# Browser
		self.br = mechanize.Browser()
		
		# Cookie Jar
		self.cj = cookielib.LWPCookieJar()
		self.br.set_cookiejar(self.cj)
		
		# Browser options
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(False)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		
		# Follows refresh 0 but not hangs on refresh > 0
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
		# Want debugging messages?
		# br.set_debug_http(True)
		# br.set_debug_redirects(True)
		# br.set_debug_responses(True)
		
		# User-Agent (this is cheating, ok?)
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		
	def fetchSimpleURLAsString(self, url):
		# Open some site, let's pick a random one, the first that pops in mind:
		r = self.br.open(url)
		html = r.read()
		return html
		
	
