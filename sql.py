import time

import psycopg2

from User import User
from dataDao import DataDao
from logger import getLogger
from miqaat import Miqaat

logger = getLogger()

timestamp = time.time()
defaultData = DataDao([], User('30334344', 'gadiwala'))


def get_data_from_cache():
    global timestamp
    global defaultData
    if time.time() - timestamp > 60:
        timestamp = time.time()
        data = get_data()
        defaultData = data
    return defaultData


def get_data():
    logger.info("Getting data from mysql")
    data = defaultData
    try:
        connection = psycopg2.connect(user="nwxtqskgzcnsjg",
                                      password="15f94c81777cf0ae1a2fdcf0b061b19dbc442b70ca11695b34645a929e31df53",
                                      host="ec2-52-203-27-62.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d6vpt6453up78o")
        cursor = connection.cursor()
        data.user = getUser(cursor)
        data.miqaatList = getMiqaats(cursor)
        logger.info("Success in getting data from mysql")
    except Exception as e:
        logger.error("Exception occred while getting username and pwd: " + str(e))
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")

    return data


def update_miqaat(miqaat):
    logger.info("updating miqaat")
    try:
        connection = psycopg2.connect(user="nwxtqskgzcnsjg",
                                      password="15f94c81777cf0ae1a2fdcf0b061b19dbc442b70ca11695b34645a929e31df53",
                                      host="ec2-52-203-27-62.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d6vpt6453up78o")
        cursor = connection.cursor()
        query = "Update miqaats set isActive=false where id=" + str(miqaat.id) + ";"
        cursor.execute(query)
        connection.commit()
        logger.info("Success in updating miqaat from mysql")
    except Exception as e:
        logger.error("Exception occred while updating miqaat: " + str(e))
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")


def getUser(cursor):
    cursor.execute("Select its, pwd from users order by id desc limit 1;")
    record = cursor.fetchall()
    return User(record[0][0], record[0][1])


def getMiqaats(cursor):
    cursor.execute("Select * from miqaats where miqaats.isActive=true;")
    records = cursor.fetchall()
    return parseMiqaats(records)


def parseMiqaats(records):
    miqaats = []
    for record in records:
        miqaats.append(Miqaat(record[0], record[1], record[2], record[3], record[4], record[6]))

    return miqaats
