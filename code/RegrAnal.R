valence_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/LogiReg_Valence.csv"
arousal_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/LogiReg_Arousal.csv"
dominance_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/LogiReg_Dominance.csv"
pos_neg_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/LogiReg_PosNeg.csv"

valence_data <- read.csv(file=valence_file, header=TRUE, sep=",")
arousal_data <- read.csv(file=arousal_file, header=TRUE, sep=",")
dominance_data <- read.csv(file=dominance_file, header=TRUE, sep=",")
pos_neg_data <- read.csv(file=pos_neg_file, header=TRUE, sep=",")



#head(valence_data)
#summary(valence_data)
#sapply(valence_data, sd)
# xtabs(~ PreRequisiteCount + FollowerCount + FollowingCount + FollowAllCount + RelatedCount + 
#         CloneCount + FixNRepairCount + CausalityCount + BlockedByCount + BlockerCount + 
#         TotalBlockCount + TotalRelCount + AttachmentCount, 
#         data = valence_data)
#xtabs(~  TotalRelCount  + Class, data = valence_data)


performLogiRegr <- function(dataParam, infoParam)
{
  print("#########################")
  print(infoParam)
  logit_output <- glm(  
                        Class ~ PreRequisiteCount + FollowerCount + FollowingCount + FollowAllCount + RelatedCount + 
                        CloneCount + FixNRepairCount + CausalityCount + BlockedByCount + BlockerCount + 
                        TotalBlockCount + TotalRelCount + AttachmentCount , 
                        data = dataParam, family = "binomial"
                     )
  print(summary(logit_output))
  print("#########################")  
}




performLogiRegr(valence_data, "Valence")
performLogiRegr(arousal_data, "Arousal")
performLogiRegr(dominance_data, "Dominance")
performLogiRegr(pos_neg_data, "PosNeg")