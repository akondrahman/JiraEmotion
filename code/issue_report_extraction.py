# -*- coding: utf-8 -*-
import db_connection, os


def getIssueReports():
 connection = db_connection.giveConnection()
 try:
    with connection.cursor() as cursor:
     sql = "SELECT DISTINCT(`issue_report_id`) FROM `issue_comment` ;"
     cursor.execute(sql)
     result = cursor.fetchall()
 finally:
   connection.close()
 return result
def preProcessIssueReports():
    issueDicts = getIssueReports()
    allIssueReports = []
    for dictItem in issueDicts:
        issue_report_id_ = dictItem['issue_report_id']
        allIssueReports.append(issue_report_id_)
    return allIssueReports

def extractEmotion(fieldParam, idParam):
 connection = db_connection.giveConnection()
 try:
    with connection.cursor() as cursor:
     sql = "SELECT `"+ fieldParam+ "` AS `CNT` FROM `issue_comment` WHERE `issue_report_id`=%s;"
     dataTuple=(str(idParam))
     cursor.execute(sql, dataTuple)
     result = cursor.fetchall()

 finally:
   connection.close()
 return result

def preProcessCount(resultParam):
   countto_ret = 0
   for dict_ in resultParam:
     val_ = dict_['CNT']
     if val_=='':
       countto_ret = 0
     else:
       countto_ret= float(val_)
   return countto_ret

def giveSentenceCount(issue_report_ID_param):
   queryResult = extractEmotion('sentence_count', issue_report_ID_param)
   countToret = preProcessCount(queryResult)
   return countToret
def giveJoyCount(issue_report_ID_param):
   queryResult = extractEmotion('joy_count', issue_report_ID_param)
   countToret = preProcessCount(queryResult)
   return countToret
def giveSadnessCount(issue_report_ID_param):
   queryResult = extractEmotion('sadness_count', issue_report_ID_param)
   countToret = preProcessCount(queryResult)
   return countToret
def giveLoveCount(issue_report_ID_param):
   queryResult = extractEmotion('love_count', issue_report_ID_param)
   countToret = preProcessCount(queryResult)
   return countToret
def giveAngerCount(issue_report_ID_param):
   queryResult = extractEmotion('anger_count', issue_report_ID_param)
   countToret = preProcessCount(queryResult)
   return countToret

def determinePosAndNeg(issue_report_list_param):
   pos_issue_report_IDs = []
   neg_issue_report_IDs = []
   neutral_iss_report_IDs=[]
   for issue_report_ID in issue_report_list_param:
     sen_count = giveSentenceCount(issue_report_ID)
     joy_count = giveJoyCount(issue_report_ID)
     sad_count = giveSadnessCount(issue_report_ID)
     luv_count = giveLoveCount(issue_report_ID)
     ang_count = giveAngerCount(issue_report_ID)
     #print "ID: {}, joy: {}, sad: {}, luv: {}, ang: {}, tot: {}".format(issue_report_ID, joy_count, sad_count, luv_count, ang_count, sen_count)
     if sen_count > 0.0:
        pos_ = joy_count + luv_count
        neg_ = sad_count + ang_count
        pos_ratio = pos_ / sen_count
        neg_ratio = neg_ / sen_count
        if pos_ratio > neg_ratio:
           pos_issue_report_IDs.append(issue_report_ID)
        elif pos_ratio < neg_ratio:
           neg_issue_report_IDs.append(issue_report_ID)
        else:
           neutral_iss_report_IDs.append(issue_report_ID)
        pos_ratio, neg_ratio = 0.0, 0.0
   return (pos_issue_report_IDs, neg_issue_report_IDs)


def getVADForIssue(issue_report_ID_param, vadFlagParam):
   vadValue = 0.0
   if vadFlagParam=='V':
       queryRes = extractEmotion('valence_mean_sum', issue_report_ID_param)
   if vadFlagParam=='A':
       queryRes = extractEmotion('arousal_mean_sum', issue_report_ID_param)
   if vadFlagParam=='D':
       queryRes = extractEmotion('dominance_mean_sum', issue_report_ID_param)
   vadValue = preProcessCount(queryRes)
   return vadValue
def determineHighAndLowVAD(issue_report_list_param, flagParam, cutOffParam):
   VAD_H_issue_report_IDs = []
   VAD_L_issue_report_IDs = []
   for issue_report_ID in issue_report_list_param:
       vadForIssueID = getVADForIssue(issue_report_ID, flagParam)
       #print "ID:{}, V:{}".format(issue_report_ID, valenceForIssueID)
       if vadForIssueID > cutOffParam:
           VAD_H_issue_report_IDs.append(issue_report_ID)
       else:
           VAD_L_issue_report_IDs.append(issue_report_ID)
       vadForIssueID = 0.0
   return (VAD_H_issue_report_IDs, VAD_L_issue_report_IDs)
#print preProcessIssueReports()
allIssueReportIDs = preProcessIssueReports()
#testList=[10952, 6485, 285]
print "##### Report #####"
pos_and_neg_report_IDs = determinePosAndNeg(allIssueReportIDs)
print "All the +ve emotions", len(pos_and_neg_report_IDs[0])
print "All the -ve emotions", len(pos_and_neg_report_IDs[1])
print "--------------------"
valence_threshold = 0.0
arousal_threshold = 0.0
dominance_threshold = 0.0
high_and_low_valence = determineHighAndLowVAD(allIssueReportIDs, 'V', valence_threshold)
print "All the high valence:", len(high_and_low_valence[0])
print "All the low valence:",  len(high_and_low_valence[1])
print "--------------------"
high_and_low_arousal = determineHighAndLowVAD(allIssueReportIDs, 'A', arousal_threshold)
print "All the high arousal:", len(high_and_low_arousal[0])
print "All the low arousal:",  len(high_and_low_arousal[1])
print "--------------------"
high_and_low_arousal = determineHighAndLowVAD(allIssueReportIDs, 'D', dominance_threshold)
print "All the high dominance:", len(high_and_low_arousal[0])
print "All the low  dominance:",  len(high_and_low_arousal[1])
print "--------------------"
