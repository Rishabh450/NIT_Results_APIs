from bs4 import BeautifulSoup


class RankDetailParser:
    def __init__(self, parent):
        self.soup = BeautifulSoup(parent, 'html.parser')

    def eachDetail(self):
        returnval = ""
        if len(self.soup.find_all('img')) != 0:
            img = self.soup.find('img').attrs['data-src']
            name = self.soup.text.strip()
            returnval = img, name
        else:
            returnval = self.soup.text
        return returnval
