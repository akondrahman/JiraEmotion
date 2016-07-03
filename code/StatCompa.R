library(effsize)
valence_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/Valence_H_L.csv"
arousal_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/Arousal_H_L.csv"
dominance_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/Dominance_H_L.csv"
pos_neg_file= "/Users/akond/Documents/AkondOneDrive/OneDrive/emotion_in_jira/Pos_Neg.csv"

valence_data <- read.csv(file=valence_file, header=TRUE, sep=",")
arousal_data <- read.csv(file=arousal_file, header=TRUE, sep=",")
dominance_data <- read.csv(file=dominance_file, header=TRUE, sep=",")
pos_neg_data <- read.csv(file=pos_neg_file, header=TRUE, sep=",")

getExtractedDetails<- function(high, low, infoParam) 
{
  print(infoParam)
  print("---------------")
  print("Extraction: Mean of high")
  mean_high = mean(high, na.rm=TRUE)
  print(mean_high)
  print("Extraction: Mean of low")
  mean_low = mean(low, na.rm=TRUE)
  print(mean_low)  
  print("Extraction: S.D of high")
  sd_high = sd(high, na.rm = TRUE)
  print(sd_high)
  print("Extraction: S.D of low")
  sd_low = sd(low, na.rm = TRUE) 
  print(sd_low)  
  print("---------------")  
}

perform_t_tests <- function(highParam, lowParam, infoParam) 
{
  print(infoParam)  
  print("-------------------------")
  print("H != L")
  t_test_output <- t.test(highParam, lowParam, alternative="two.sided", var.equal=FALSE, paired=FALSE) 
  print(t_test_output)
  print("-------------------------")  
  print("H > L")  
  t_test_output <- t.test(highParam, lowParam, alternative="greater", var.equal=FALSE, paired=FALSE) 
  print(t_test_output)
  print("-------------------------")  
  print("H < L")    
  t_test_output <- t.test(highParam, lowParam, alternative="less", var.equal=FALSE, paired=FALSE) 
  print(t_test_output )
  print("-------------------------")  
}


getCohen<- function(cohen_amount_high, cohen_amount_low, infoParam) 
{
  print(infoParam)  
  print("---------------")
  mean_high = mean(cohen_amount_high, na.rm=FALSE)
  mean_low = mean(cohen_amount_low, na.rm=FALSE)

  sd_high = sd(cohen_amount_high, na.rm = FALSE)
  sd_low = sd(cohen_amount_low, na.rm = FALSE) 

  cohen_numerator = mean_high - mean_low 
  cohen_denominator = sqrt(( sd_high ^ 2 + sd_low ^ 2 ) / 2 )
  cohen_ = cohen_numerator / cohen_denominator 
  print("Finally:::Cohen's D:::")
  print(cohen_)
  print("---------------")  
}

getA12 <- function(high_, low_, infoParam)
{
  print(infoParam)
  print("---------------")
  print(":::::VD-A12:::::")
  print(VD.A( high_, low_))    
  print("---------------")  
}

getCliffs <- function(high_, low_, infoParam)
{
  print(":::::Cliffs-Delta:::::")
  print(infoParam)
  res_effect_ = cliff.delta(high_,  low_, return.dm=FALSE)
  print(res_effect_)  
}

performIndiAnalysis <- function(high_, low_, infoParam)
{
  #Step-1 
  getExtractedDetails(high_, low_, infoParam)
  #Step-2 
  high_mod <- na.omit(high_)
  low_mod <- na.omit(low_) 
  #Step-3
  perform_t_tests(high_mod, low_mod, infoParam)  
  #Step-4 
  getCohen(high_mod, low_mod, infoParam)
  #Step-5 
  getA12(high_mod, low_mod, infoParam)
  # Step-6
  getCliffs(high_mod, low_mod, infoParam)
}



performAnalysis<- function(dataParam) 
{ 
  ## Pre-requisite 
  H_PreRequisiteCount <- dataParam$H_PreRequisiteCount
  L_PreRequisiteCount <- dataParam$L_PreRequisiteCount  
  performIndiAnalysis(H_PreRequisiteCount, L_PreRequisiteCount, "Pre-requisite")
  
  ##  Follower Count
  H_FollowerCount <- dataParam$H_FollowerCount
  L_FollowerCount <- dataParam$L_FollowerCount  
  performIndiAnalysis(H_FollowerCount, L_FollowerCount, "Follower Counts")               
  
  ##  Following Count
  H_FollowingCount <- dataParam$H_FollowingCount
  L_FollowingCount <- dataParam$L_FollowingCount  
  performIndiAnalysis(H_FollowingCount, L_FollowingCount, "Following Counts")             
  
  ## Total Follow-type Counts 
  H_FollowAllCount <- dataParam$H_FollowAllCount
  L_FollowAllCount <- dataParam$L_FollowAllCount  
  performIndiAnalysis(H_FollowAllCount, L_FollowAllCount, "Total Follow-type Counts")           
  
  ## Related Counts
  H_RelatedCount <- dataParam$H_RelatedCount
  L_RelatedCount <- dataParam$L_RelatedCount  
  performIndiAnalysis(H_RelatedCount, L_RelatedCount, "Related Counts")         
  
  ## Clone Counts
  H_CloneCount <- dataParam$H_CloneCount
  L_CloneCount <- dataParam$L_CloneCount  
  performIndiAnalysis(H_CloneCount, L_CloneCount, "Clones")       
   
  ## Fix And Repair Count
  H_FixNRepairCount <- dataParam$H_FixNRepairCount
  L_FixNRepairCount <- dataParam$L_FixNRepairCount  
  performIndiAnalysis(H_FixNRepairCount, L_FixNRepairCount, "Fix And Repairs")     
  
  ## Causality Count
  H_CausalityCount <- dataParam$H_CausalityCount
  L_CausalityCount <- dataParam$L_CausalityCount  
  performIndiAnalysis(H_CausalityCount, L_CausalityCount, "Causality")   
  
  ##Blockers
  H_BlockerCount <- dataParam$H_BlockerCount
  L_BlockerCount <- dataParam$L_BlockerCount  
  performIndiAnalysis(H_BlockerCount, L_BlockerCount, "Blocks")      
  
  ##Blocked By
  H_BlockedByCount <- dataParam$H_BlockedByCount
  L_BlockedByCount <- dataParam$L_BlockedByCount  
  performIndiAnalysis(H_BlockedByCount, L_BlockedByCount, "No.of Blocked Bys")        
  
  ## Total Block Count  
  H_TotalBlockCount <- dataParam$H_TotalBlockCount
  L_TotalBlockCount <- dataParam$L_TotalBlockCount  
  performIndiAnalysis(H_TotalBlockCount, L_TotalBlockCount, "Total Blocks")    
  
  ## Total RelationCount
  H_TotalRelCount <- dataParam$H_TotalRelCount
  L_TotalRelCount <- dataParam$L_TotalRelCount  
  performIndiAnalysis(H_TotalRelCount, L_TotalRelCount, "Total Relations")  
  
  ## Attachment Count
  H_AttachmentCount <- dataParam$H_AttachmentCount
  L_AttachmentCount <- dataParam$L_AttachmentCount  
  performIndiAnalysis(H_AttachmentCount, L_AttachmentCount, "Attachments")    
}


#performAnalysis(valence_data)
#performAnalysis(arousal_data)
#performAnalysis(dominance_data)
#performAnalysis(pos_neg_data)