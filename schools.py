import csv
from flask import make_response, abort
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.csvtomongo

# MdbURI = "mongodb://heroku_n22qp0w4:ie7fjj59dm14gap8hafjfae9eg@ds131963.mlab.com:31963/heroku_n22qp0w4"
# client = MongoClient(MdbURI)
# db = client['heroku_n22qp0w4']

coll = db.samplecoll

with open('data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    coll.remove()
    next(csvreader)
    for row in csvreader:
        coll.insert_one({'school': row[2], 'students': row[13]})


def read_all():
    data_list = []
    for doc in coll.find():
        data_list.append({
            "school": doc['school'],
            "students": doc['students']
        })
    return data_list


def create(info):
    school = info.get("school", None)
    students = info.get("students", None)
    existing_school = coll.find_one({'school': school})

    if existing_school is None:
        coll.insert(
            {'school': school, 'students': students})
        return make_response(
            "{school} successfully created".format(school=school), 201
        )
    else:
        abort(
            406,
            "{school} already exists".format(school=school),
        )


def read_one(school):
    existing_school = coll.find_one({'school': school})
    data_list = []

    if existing_school:
        data_list.append({
            "school": existing_school['school'],
            "students": existing_school['students']
        })
        return data_list

    else:
        abort(
            404, "{school} not found".format(school=school)
        )


def update(school, info):
    existing_school = coll.find_one({'school': school})
    data_list = []

    if existing_school:
        existing_school['students'] = info.get("students")
        data_list.append({
            "school": existing_school['school'],
            "students": existing_school['students']
        })
        coll.save(existing_school)
        return data_list

    else:
        abort(
            404, "{school} not found".format(school=school)
        )


def delete(school):
    existing_school = coll.find_one({'school': school})

    if existing_school:
        coll.remove(existing_school)
        return make_response(
            "{school} successfully deleted".format(school=school), 200
        )
    else:
        abort(
            404, "{school} not found".format(school=school)
        )
