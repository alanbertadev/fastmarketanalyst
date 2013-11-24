from ..utils.redis_facade import RedisFacade
from ..utils.mechanize_facade import MechanizeFacade
from BeautifulSoup import BeautifulSoup
import logging
import re
from logging.handlers import RotatingFileHandler

class IncomeStatement:
	def __init__(self):
		self.symbolParse = '*SYMBOL*'
		self.annualReport = 'annual'
		self.URL = 'http://finance.yahoo.com/q/is?s=' + self.symbolParse + '+Income+Statement&'
		self.redis = RedisFacade()
		self.browser = MechanizeFacade()
		
	def extractIncomeStatementFromString(self, pageHtml):
		if pageHtml == "" or pageHtml is None:
			logging.debug('extractIncomeStatementFromString - pageHtml input is null or empty!')
			return None
		soup = BeautifulSoup(pageHtml)
		
		tbl = soup.find(id='yfncsumtab')
		if tbl is not None:
			
			#remove first header <tr> that has Income: and search + GO button
			modTitle = soup.find('table',{ "class" : "yfnc_modtitle1" })
			if modTitle is None:
				logging.warn('extractIncomeStatementFromString - no modTitletr id found')
			else:
				if modTitle.parent is not None:
					if modTitle.parent.parent is not None:
						modTitle.parent.parent.extract()
					else:
						logging.warn('extractIncomeStatementFromString - no modTitle TR parent found')
				else:
					logging.warn('extractIncomeStatementFromString - no modTitle TD parent found')
		
			#strip out any promo table items
			allPromo = soup.findAll('table',{ "class" : "yfnc_promooutline1" })
			if not allPromo:
				logging.warn('extractIncomeStatementFromString - no class=yfnc_promooutline1 found')
			for promo in allPromo:
				promo.extract()
			
			#strip out the annual/quarter toggle links from yahoo
			allViewToggle = soup.findAll(text=re.compile("\AView.*$"))
			if not allViewToggle:
				logging.warn('extractIncomeStatementFromString - \AView.*$ has found no items!')
			for viewItem in allViewToggle:
				if viewItem.parent is not None:
					viewItem.parent.extract()
				else:
					logging.warn('extractIncomeStatementFromString - viewItem.parent is null!')
			
			#Add styles from the page so that it looks ok
			styleCompressed = ""
			
			allInlineStyles = soup.findAll('style')
			if not allInlineStyles:
				logging.warn('extractIncomeStatementFromString - allInlineStyles is empty')
			for inlineStyle in allInlineStyles:
				styleCompressed = styleCompressed + inlineStyle.prettify()
			
			allCssObjects = soup.findAll('link')
			if not allCssObjects:
				logging.warn('extractIncomeStatementFromString - allCssObjects is empty')
			for cssObject in allCssObjects:
				styleCompressed = styleCompressed + cssObject.prettify()
				
			tbl = soup.find(id='yfncsumtab')
			
			strStyleModifier = "<style>html{ padding:0px !important; }</style>"
			
			return styleCompressed + tbl.prettify() + strStyleModifier

		return None
        
        def fetchAnnualFromYahoo( self, symbol ):
            fetchURL = self.URL.replace( self.symbolParse, symbol ) + self.annualReport
            fullPageHtml = self.browser.fetchSimpleURLAsString(fetchURL)
            return self.extractIncomeStatementFromString(fullPageHtml)
        
if __name__ == '__main__':
	
	print "Test 1 - extractIncomeStatementFromString with null input"
	iStmt = IncomeStatement()
	assert iStmt.extractIncomeStatementFromString(None) == None
	print "PASS"
	
	print "Test 2 - extractIncomeStatementFromString with testing/income_statement_annual.html input"
	iStmt = IncomeStatement()
	data = ""
	with open ("testing/income_statement_annual.html", "r") as myfile:
		data=myfile.read()
	response = iStmt.extractIncomeStatementFromString(data)
	text_file = open("testing/income_statement_annual.output.html", "w")
	text_file.write(response)
	text_file.close()
	assert response is not None
	print "PASS"
	
	print "Test 3 - Fetch MSFT income statement"
	iStmt = IncomeStatement()
	response = iStmt.fetchAnnualFromYahoo( "MSFT" )
	text_file = open("testing/MSFT_income_statement_annual.output.html", "w")
	text_file.write(response)
	text_file.close()
	assert response is not None
	print "PASS"
	