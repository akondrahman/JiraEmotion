# -*- coding: utf-8 -*-
import utility, db_connection, os, numpy as np


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
   countto_ret = 0.0
   for dict_ in resultParam:
     val_ = dict_['CNT']
     if val_=='':
       countto_ret = 0.0
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

def generateVADSummary(vad_list_param):
   print "Summary"
   print "-->Median: ", np.median(vad_list_param)
   print "-->Mean: ",   np.mean(vad_list_param)
   print "-->25th: ",   np.percentile(vad_list_param, 25)
   print "-->60th: ",   np.percentile(vad_list_param, 60)
   print "-->65th: ",   np.percentile(vad_list_param, 65)
   print "-->70th: ",   np.percentile(vad_list_param, 70)
   print "-->75th: ",   np.percentile(vad_list_param, 75)

def extractRelationFromDB(strMatchParam, issue_id_param):
 connection = db_connection.giveConnection()
 try:
    with connection.cursor() as cursor:
     sql = "SELECT COUNT(*) AS `CNT` FROM `issue_changelog_item` WHERE `field_name`='Link' AND `issue_report_id`=%s AND `new_value` LIKE %s ;"
     dataTuple=(str(issue_id_param), strMatchParam)
     cursor.execute(sql, dataTuple)
     result = cursor.fetchall()

 finally:
   connection.close()
 return result

def extractAttachmentForIssue(issue_id_param):
 connection = db_connection.giveConnection()
 try:
    with connection.cursor() as cursor:
     sql = "SELECT COUNT(*) AS `CNT` FROM `issue_attachment` WHERE `issue_report_id`=%s;"
     dataTuple=(str(issue_id_param))
     cursor.execute(sql, dataTuple)
     result = cursor.fetchall()

 finally:
   connection.close()
 return result

def getRelationshipCount(issueReportIDParam):
   listOfRelationships = []
   requiredCount = preProcessCount(extractRelationFromDB('%required for%', issueReportIDParam))
   dependentCount = preProcessCount(extractRelationFromDB('%depend%', issueReportIDParam))
   preRequisiteCount = requiredCount + dependentCount
   followerCount = preProcessCount(extractRelationFromDB('%followed up by%', issueReportIDParam))
   followingCount = preProcessCount(extractRelationFromDB('%follows up on%', issueReportIDParam))
   followAllCount = followerCount + followingCount
   relatedCount = preProcessCount(extractRelationFromDB('%relates to%', issueReportIDParam))
   cloneCount = preProcessCount(extractRelationFromDB('%duplicate%', issueReportIDParam))
   fixNRepairCount = preProcessCount(extractRelationFromDB('%fix%', issueReportIDParam))
   causalityCount = preProcessCount(extractRelationFromDB('%cause%', issueReportIDParam))
   ##added later
   blockedByCount = preProcessCount(extractRelationFromDB('%blocked by%', issueReportIDParam))
   blockerCount = preProcessCount(extractRelationFromDB('%blocks%', issueReportIDParam))
   totBlockCnt = blockerCount + blockedByCount
   ##
   totRelCount = preRequisiteCount + followerCount + followingCount + followAllCount + relatedCount + cloneCount + fixNRepairCount + causalityCount + totBlockCnt
   listOfRelationships = [preRequisiteCount, followerCount, followingCount, followAllCount, relatedCount, cloneCount, fixNRepairCount, causalityCount, blockedByCount, blockerCount, totBlockCnt, totRelCount]
   return listOfRelationships


def dumpComplexityFeatures(listParam, fileNameToDumpParam):
   dictToDump={}
   for issue_report_ in listParam:
      relationshipListForIssue =  getRelationshipCount(issue_report_)
      attachmentForIssue = preProcessCount(extractAttachmentForIssue(issue_report_))
      print "ID: {}, relation-status: {}, attachments: {}".format(issue_report_, relationshipListForIssue, attachmentForIssue)
      dictToDump[issue_report_]=(relationshipListForIssue, attachmentForIssue)
   status = utility.writeDictofRelToFile(dictToDump, fileNameToDumpParam)
   print "Finished dumping with {} bytes".format(status)


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
   all_vad_values = []
   for issue_report_ID in issue_report_list_param:
       vadForIssueID = getVADForIssue(issue_report_ID, flagParam)
       #print "ID:{}, V:{}".format(issue_report_ID, valenceForIssueID)
       all_vad_values.append(vadForIssueID)
       if vadForIssueID > cutOffParam:
           VAD_H_issue_report_IDs.append(issue_report_ID)
       else:
           VAD_L_issue_report_IDs.append(issue_report_ID)
       vadForIssueID = 0.0
   generateVADSummary(all_vad_values)
   return (VAD_H_issue_report_IDs, VAD_L_issue_report_IDs)
#print preProcessIssueReports()
allIssueReportIDs = preProcessIssueReports()
#testList=[10952, 6485, 285]
print "Starting at:", utility.giveTimeStamp()
print "##### Report #####"
pos_and_neg_report_IDs = determinePosAndNeg(allIssueReportIDs)
pos_list = pos_and_neg_report_IDs[0]
neg_list = pos_and_neg_report_IDs[1]
# print "All the +ve emotions:", len(pos_list)
# print "All the -ve emotions:",  len(neg_list)
# dumpComplexityFeatures(pos_list, 'Pos')
# dumpComplexityFeatures(neg_list, 'Neg')
print "--------------------"
valence_threshold = 0.535559711363 # mean valence
arousal_threshold = 0.375755970058 # mean arousal
dominance_threshold = 0.551809711921 # mean dominance
high_and_low_valence = determineHighAndLowVAD(allIssueReportIDs, 'V', valence_threshold)
high_valence_list = high_and_low_valence[0]
low_valence_list = high_and_low_valence[1]
# print "All the high valence:", len(high_valence_list)
# dumpComplexityFeatures(high_valence_list, 'H_V')
# print "All the low valence:",  len(low_valence_list)
# dumpComplexityFeatures(low_valence_list, 'L_V')
# print "--------------------"
high_and_low_arousal = determineHighAndLowVAD(allIssueReportIDs, 'A', arousal_threshold)
high_arousal_list = high_and_low_arousal[0]
low_arousal_list = high_and_low_arousal[1]
print "All the high arousal:", len(high_arousal_list)
dumpComplexityFeatures(high_arousal_list, 'H_A')
print "All the low arousal:",  len(low_arousal_list)
dumpComplexityFeatures(low_arousal_list, 'L_A')
print "--------------------"
# high_and_low_dominance = determineHighAndLowVAD(allIssueReportIDs, 'D', dominance_threshold)
# high_dominance_list = high_and_low_dominance[0]
# print "All the high dominance:", len(high_dominance_list)
# dumpComplexityFeatures(high_dominance_list, 'H_D')
# low_dominance_list = high_and_low_dominance[1]
# print "All the low  dominance:",  len(low_dominance_list)
# dumpComplexityFeatures(low_dominance_list, 'L_D')
# print "--------------------"
print "Ending at:", utility.giveTimeStamp()
