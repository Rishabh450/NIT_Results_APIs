import requests
from pages.profile import ProfilePage
from bs4 import BeautifulSoup
from parsers.ProfileParcer import ProfileParser
from parsers.ResultTableParser import ResultsTableParser
from parsers.SubjectParser import SubjectParser
from flask import Flask, request, jsonify
from pages.ResultPage import ResultPage
from parsers.StudentRankParser import StudentRankParser
from parsers.DetailParser import RankDetailParser
import logging
import json
import os

app = Flask("__name__")


@app.route('/', methods=['POST'])
def get_user():
    return jsonify({'Developed by': "Rishabh Bhardwaj", 'status': 500})


def getRankDetails(semester, method, roll_number):
    dicter = {
        'roll': roll_number
    }
    s = requests.Session()
    login = s.post('https://nilekrator.pythonanywhere.com/', dicter)
    if login.status_code == 200:
        param = {
            "semester": semester,
            "method": method
        }
        rankpage = s.get(url='https://nilekrator.pythonanywhere.com/rank', params=param).content
        return rankpage


def getRankTable(semester, method, roll_number):
    rankpage = getRankDetails(semester, method, roll_number)
    rankTable = ResultPage(rankpage).getRankTable()
    return rankTable


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
        return profile, s
    else:
        return "invalid"


@app.route('/api/profile', methods=['POST'])
def getBasicProfile():
    roll_number = request.json['roll']
    page = ProfilePage(getContent(roll_number)[0])
    img = page.getImage
    new_img = BeautifulSoup(str(img), 'html.parser')
    image = new_img.find('img')['data-src']
    parsed = [ProfileParser(details).getDetails for details in page.getProfile]
    profile_list = [BeautifulSoup(str(item), 'html.parser').text for item in parsed[0]]
    profile_json = {
        "name": profile_list[0],
        "roll": profile_list[1],
        "branch": profile_list[2],
        "rank": profile_list[3],
        "img": image

    }
    return jsonify(profile_json)


@app.route('/api/rank', methods=['POST'])
def getStudentRankJson():
    semester = request.json['semester']
    method = request.json['method']
    roll_number = request.json['roll']
    studentlist = getRankTable(semester, method, roll_number)
    studentlistParsed = []
    for student in studentlist:
        singleStudentDetail = StudentRankParser(str(student)).getDetails()
        rank = RankDetailParser(str(singleStudentDetail[0])).eachDetail()
        img, name = RankDetailParser(str(singleStudentDetail[1])).eachDetail()
        marks = RankDetailParser(str(singleStudentDetail[2])).eachDetail()
        studentDict = {
            "rank": rank,
            "name": name,
            "img": img,
            "marks": marks

        }
        studentlistParsed.append(studentDict)

    return jsonify(studentlistParsed)


@app.route('/api/cgpa', methods=['POST'])
def getCGPA():
    roll_number = request.json['roll']
    page = ProfilePage(getContent(roll_number)[0])
    totalsems = []
    for table in page.getAllResultTables:
        res = ResultsTableParser(table)
        status_list = res.getSemesterStatus

        if status_list:
            status_json = {
                "semester": status_list[2],
                "status": status_list[3],
                "sgpa": status_list[0],
                "cgpa": status_list[1]
            }
            totalsems.append(status_json)
    return jsonify(totalsems)


@app.route('/api/results', methods=['POST'])
def getSemesterResults():
    roll_number = request.json['roll']

    page = ProfilePage(getContent(roll_number)[0])
    semester_list = []
    for table in page.getAllResultTables:
        res = ResultsTableParser(table)
        totalsubjects = res.getAllSubjects
        sem_marks = []
        for subject in totalsubjects:
            subject_details_obj = SubjectParser(subject)
            subject_details = [subject_detail.string for subject_detail in subject_details_obj.getSubjectDetails]
            subject_details_json = {
                "code": subject_details[0],
                "name": subject_details[1],
                "mid_sem": subject_details[2],
                "internals": subject_details[3],
                "assignement": subject_details[4],
                "quiz": subject_details[5],
                "end_sem": subject_details[6],
                "total": subject_details[7],
                "grade": subject_details[8]
            }
            sem_marks.append(subject_details_json)
        if sem_marks:
            semester_list.append(sem_marks)
    return jsonify(semester_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'), debug=True)
