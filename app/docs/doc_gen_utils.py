from BeautifulSoup import BeautifulSoup
import sys

class DocGenUtils(object):
    """
    Utility class that providing static methods to manipulate
    the generated epydoc html documents to make it easier
    to read the service methods in order for clients to develop
    apps to consume the services.
    """

    @staticmethod
    def remove_documentation_nav_bar(page_html):
        soup = BeautifulSoup(page_html)
        all_nav_bar = soup.findAll('table', { "class" : "navbar" })
        for nav_bar in all_nav_bar:
            nav_bar.extract()

        first_table = soup.findAll('table')
        first_table[0].extract()

        return soup.prettify()

    @staticmethod
    def rename_header_to_new_header(page_html):
        page_html = page_html.replace("Class OnlineApplicationLayer",
            "FastMarketAnalyst Service Methods")
        return page_html.replace("app.oal.OnlineApplicationLayer",
            "FastMarketAnalyst Service Methods")

    @staticmethod
    def load_file_as_string(file_path):
        linestring = open(file_path, 'r').read()
        return linestring

    @staticmethod
    def write_string_to_file(file_path, file_string):
        text_file = open(file_path, "w")
        text_file.write(file_string)
        text_file.close()


if  __name__ == '__main__':
    if len(sys.argv) > 1:
        STR_FILE = DocGenUtils.load_file_as_string(sys.argv[1])
        STR_FILE = DocGenUtils.remove_documentation_nav_bar(STR_FILE)
        STR_FILE = DocGenUtils.rename_header_to_new_header(STR_FILE)
        DocGenUtils.write_string_to_file(sys.argv[1], str(STR_FILE))
    else:
        raise Exception("Missing file path argument!")
