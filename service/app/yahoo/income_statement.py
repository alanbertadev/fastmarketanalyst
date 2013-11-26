from ..utils.redis_facade import RedisFacade
from ..utils.mechanize_facade import MechanizeFacade
from BeautifulSoup import BeautifulSoup
import logging
import re

class IncomeStatement:
    def __init__(self):
        self.symbolParse = '*SYMBOL*'
        self.annualReport = '&annual'
        self.quarterlyReport = ''
        self.URL = 'http://finance.yahoo.com/q/is?s=' + self.symbolParse + '+Income+Statement'
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
                        return None
                else:
                    logging.warn('extractIncomeStatementFromString - no modTitle TD parent found')
                    return None
        
            #strip out any promo table items
            allPromo = soup.findAll('table',{ "class" : "yfnc_promooutline1" })
            if not allPromo:
                logging.warn('extractIncomeStatementFromString - no class=yfnc_promooutline1 found')
                return None
            for promo in allPromo:
                promo.extract()
            
            #strip out the annual/quarter toggle links from yahoo
            allViewToggle = soup.findAll(text=re.compile("\AView.*$"))
            if not allViewToggle:
                logging.warn('extractIncomeStatementFromString - \AView.*$ has found no items!')
                return None
            for viewItem in allViewToggle:
                if viewItem.parent is not None:
                    viewItem.parent.extract()
                else:
                    logging.warn('extractIncomeStatementFromString - viewItem.parent is null!')
                    return None
            
            #Add styles from the page so that it looks ok
            styleCompressed = ""
            
            allInlineStyles = soup.findAll('style')
            if not allInlineStyles:
                logging.warn('extractIncomeStatementFromString - allInlineStyles is empty')
                return None
            for inlineStyle in allInlineStyles:
                styleCompressed = styleCompressed + inlineStyle.prettify()
            
            allCssObjects = soup.findAll('link')
            if not allCssObjects:
                logging.warn('extractIncomeStatementFromString - allCssObjects is empty')
                return None
            for cssObject in allCssObjects:
                styleCompressed = styleCompressed + cssObject.prettify()
                
            tbl = soup.find(id='yfncsumtab')
            
            strStyleModifier = "<style>html{ padding:0px !important; }</style>"
            
            return styleCompressed + tbl.prettify() + strStyleModifier

        return None
        
    def fetchAnnualFromYahooAsHtml( self, symbol ):
        fetchURL = self.URL.replace( self.symbolParse, symbol ) + self.annualReport
        fullPageHtml = self.browser.fetchSimpleURLAsString(fetchURL)
        return self.extractIncomeStatementFromString(fullPageHtml)
            
    def fetchQuarterlyFromYahooAsHtml( self, symbol ):
        fetchURL = self.URL.replace( self.symbolParse, symbol ) + self.quarterlyReport
        fullPageHtml = self.browser.fetchSimpleURLAsString(fetchURL)
        return self.extractIncomeStatementFromString(fullPageHtml)