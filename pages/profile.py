from bs4 import BeautifulSoup
from locators.ProfileLocator import ProfileLocator


class ProfilePage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def getProfile(self):
        locator = ProfileLocator.PROFILE
        profile = self.soup.select(locator)
        return profile

    @property
    def getAllResultTables(self):
        locator = ProfileLocator.TABLE
        tables = self.soup.select(locator)
        return tables

    @property
    def getImage(self):
        locator = ProfileLocator.PROFILE_PICTURE
        return self.soup.select(locator)[0]







