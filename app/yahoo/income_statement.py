from ..utils.redis_facade import RedisFacade
from ..utils.mechanize_facade import MechanizeFacade
from BeautifulSoup import BeautifulSoup
import logging
import re

class IncomeStatement:

    def __init__(self, htmlSrc):
        self.htmlSrc = htmlSrc
        
    def getHtml(self):
        return self.htmlSrc
        
class Annual(IncomeStatement):

    def __init__(self, htmlSrc):
        IncomeStatement.__init__(self, htmlSrc)
                
class Quarterly(IncomeStatement):

    def __init__(self, htmlSrc):
        IncomeStatement.__init__(self, htmlSrc)
        
class IncomeStatementManager:

    def __init__(self, symbol):
        self.annualReport = '&annual'
        self.quarterlyReport = ''
        if symbol is None:
            symbol = ''
        self.URL = 'http://finance.yahoo.com/q/is?s=' + symbol + '+Income+Statement'
        self.redis = RedisFacade()
        self.browser = MechanizeFacade()
        self.quarterlyReportDownloaded = None
        self.annualReportDownloaded = None
        
    def extractIncomeStatementFromString(self, pageHtml):
        if pageHtml == "" or pageHtml is None:
            logging.debug('extractIncomeStatementFromString - pageHtml input is null or empty!')
            return None
        soup = BeautifulSoup(pageHtml)
        
        tbl = soup.find(id='yfncsumtab')
        if tbl is not None:
            
            # remove first header <tr> that has Income: and search + GO button
            modTitle = soup.find('table', { "class" : "yfnc_modtitle1" })
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
        
            # strip out any promo table items
            allPromo = soup.findAll('table', { "class" : "yfnc_promooutline1" })
            if not allPromo:
                logging.warn('extractIncomeStatementFromString - no class=yfnc_promooutline1 found')
                return None
            for promo in allPromo:
                promo.extract()
            
            # strip out the annual/quarter toggle links from yahoo
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
            
            # Add styles from the page so that it looks ok
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
        
    def getAnnual(self):
        if self.annualReportDownloaded is None:
            fetchURL = self.URL + self.annualReport
            fullPageHtml = self.browser.fetchSimpleURLAsString(fetchURL)
            self.annualReportDownloaded = Annual(self.extractIncomeStatementFromString(fullPageHtml))
        return self.annualReportDownloaded
            
    def getQuarterly(self):
        if self.annualReportDownloaded is None:
            fetchURL = self.URL + self.quarterlyReport
            fullPageHtml = self.browser.fetchSimpleURLAsString(fetchURL)
            self.annualReportDownloaded = Quarterly(self.extractIncomeStatementFromString(fullPageHtml))
        return self.annualReportDownloaded
        
