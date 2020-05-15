import requests
from pages.profile import ProfilePage
from bs4 import BeautifulSoup
from parsers.ProfileParcer import ProfileParser
from parsers.ResultTableParser import ResultsTableParser
from parsers.SubjectParser import SubjectParser
from flask import Flask, request, jsonify
import json

import os


def getContent(roll_number):
    dicter = {
        'roll': roll_number
    }
    s = requests.Session()
    r = s.post('https://nilekrator.pythonanywhere.com/', dicter)
    if r.status_code == 200:
        text = r.text
        dictr = text
        profile = s.get(url='https://nilekrator.pythonanywhere.com/profile', params=dictr).content
        return profile

    else:
        return "invalid"


def getBasicProfil(roll_number):
    page = ProfilePage(getContent(roll_number))
    img = page.getImage
    new_img = BeautifulSoup(str(img), 'html.parser')
    print(new_img.find('img')['src'])








    parsed = [ProfileParser(details).getDetails for details in page.getProfile]
    profile_list = [BeautifulSoup(str(item),'html.parser').text for item in parsed[0]]
    profile_json = {
        "name": profile_list[0],
        "roll": profile_list[1],
        "branch": profile_list[2],
        "rank": profile_list[3],

    }



print(getBasicProfil('2018ugcs015'))
