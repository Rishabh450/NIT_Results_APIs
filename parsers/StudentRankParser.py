from bs4 import BeautifulSoup
from locators.RankLocator import RankLocator


class StudentRankParser:
    def __init__(self, parent):
        self.soup = BeautifulSoup(parent, 'html.parser')

    def getDetails(self):
        locator = RankLocator.STUDENT_DETAIL
        detaillist = self.soup.select(locator)
        return detaillist
