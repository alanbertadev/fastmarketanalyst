import income_statement
import logging
import base64

class OnlineApplicationLayer:

    	def __init__(self):
            #logging.basicConfig(filename='/var/tmp/callmaker_OAL.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
            self.incomStatementFetcher = income_statement.IncomeStatement()
            
        def fetchIncomeStatement(self, params):
            retObj = {'IncomeStatement':""}
            retObj['IncomeStatement'] = base64.b64encode(self.incomStatementFetcher.fetchAnnualFromYahoo( params['symbol'] ))
            return retObj