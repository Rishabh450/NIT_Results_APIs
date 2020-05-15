from bs4 import BeautifulSoup
from locators.RankLocator import RankLocator

class ResultPage:
    def __init__(self,page):
        self.soup = BeautifulSoup(page, 'html.parser')

    def getRankTable(self):
        locators = RankLocator.RANK_TABLE
        rankTable = self.soup.select(locators)
        return rankTable

