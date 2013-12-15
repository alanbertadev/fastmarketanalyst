from BeautifulSoup import BeautifulSoup
import sys

class DocGenUtils:

    @staticmethod
    def removeDocumenationNavBar( pageHtml ):
        soup = BeautifulSoup(pageHtml)
        allNavBar = soup.findAll('table',{ "class" : "navbar" })
        for navbar in allNavBar:
            navbar.extract()
            
        firstTable = soup.findAll('table')
        firstTable[0].extract()
            
        return soup.prettify()

    @staticmethod
    def renameHeaderToNewHeader( pageHtml ):
        return pageHtml.replace("Class OnlineApplicationLayer", "FastMarketAnalyst Service Methods").replace( "app.oal.OnlineApplicationLayer", "FastMarketAnalyst Service Methods")
        
    @staticmethod
    def loadFileAsString( filePath ):
        linestring = open(filePath, 'r').read()
        return linestring
        
    @staticmethod
    def writeStringToFile( filePath, fileString ):
        text_file = open(filePath, "w")
        text_file.write(fileString)
        text_file.close()


if  __name__ =='__main__':

    if len(sys.argv) > 1:    
        strFile = DocGenUtils.loadFileAsString( sys.argv[1] )
        strFile = DocGenUtils.removeDocumenationNavBar( strFile )
        strFile = DocGenUtils.renameHeaderToNewHeader( strFile )
        DocGenUtils.writeStringToFile( sys.argv[1], str(strFile) )
    else:
        raise Exception("Missing file path argument!")