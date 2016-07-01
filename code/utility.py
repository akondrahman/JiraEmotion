# -*- coding: utf-8 -*-



import os, time, datetime
def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret
def writeDictofRelToFile(dictParam, fileNameParam):
  completeStrToWrite=""
  fileParam =  fileNameParam + ".csv"
  fileToWrite = open( fileParam, 'w');
  lineStr =  "ID,PreRequisiteCount,FollowerCount,FollowingCount,FollowAllCount,RelatedCount,CloneCount,FixNRepairCount,CausalityCount,BlockedByCount,BlockerCount,TotalBlockCount,TotalRelCount,AttachmentCount"


  fileToWrite.write(lineStr + "\n");
  for id_, values in dictParam.items():
    lineStr = str(id_) + ","
    relCountItems = values[0]
    attachmentCount = values[1]
    for item in relCountItems:
        lineStr = lineStr + str(item) + ","
    lineStr = lineStr + str(attachmentCount)
    lineStr = lineStr + "\n"
    completeStrToWrite = completeStrToWrite + lineStr
    lineStr="";
  fileToWrite.write(completeStrToWrite );
  fileToWrite.close()
  return str(os.stat(fileParam).st_size)
