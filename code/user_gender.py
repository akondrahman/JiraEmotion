# -*- coding: utf-8 -*-
import db_connection, os
from genderComputer import GenderComputer

def jiraUserDetails():
 connection = db_connection.giveConnection()
 try:
    with connection.cursor() as cursor:
     sql = "SELECT * FROM `user` ;"
     cursor.execute(sql)
     result = cursor.fetchall()
 finally:
   connection.close()
 return result





def giveGender(nameParam, gcObj):
    returnGender=''
    unicoded_name=unicode(nameParam, 'latin-1')
    returnGender = gcObj.resolveGender(unicoded_name , None )
    return returnGender







def processNames(userParam):
    listOfUsersToRet=[]
    gcObj = GenderComputer(os.path.abspath('./nameLists'))
    for dictItem in userParam:
        name_ = dictItem['name']
        id_  = dictItem['id']
        if '0x' in name_:
            print "Invalid name detected ... skipping value:", name_
        else:
            gender_ = giveGender(name_, gcObj)
            #print id_
            gender_tuple = (id_, gender_)
            listOfUsersToRet.append(gender_tuple)
            #print "ID: {}, Name: {}, Gender: {}".format(id_, name_, gender_)
            name_=""
            gender_=''
    return listOfUsersToRet



def updateDatabaseTable(genderListParam):
   import db_connection
   record_count = 1
   for tupleElem in genderListParam:
        IDToLookup = tupleElem[0]
        genderToUpdate = tupleElem[1]
        connection = db_connection.giveConnection()
        try:
            with connection.cursor() as cursor:
                 updateStatement = "UPDATE `user` SET `gender`=%s WHERE `id`=%s ;"
                 dataTuple = (genderToUpdate, IDToLookup)
                 cursor.execute(updateStatement,  dataTuple)
                 connection.commit()
                 print "Records updated so far: ", record_count
                 record_count = record_count + 1
        finally:
            connection.close()

users_all = jiraUserDetails()
processedNamesWithGender  = processNames(users_all)
#print processedNamesWithGender
updateDatabaseTable(processedNamesWithGender)
