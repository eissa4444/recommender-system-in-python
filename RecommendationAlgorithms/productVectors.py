from math import sqrt
from math import pow
from data import critics as data
import csv
import random
import operator

def euc(person1,person2):

	euc_sqr = 0
	cond = False                         # to avoid such x/0 
	for k1 in person1:                  # k is the key value of the dict (id of restaurant)
		for k2 in person2:
			#if(k1 < k2):
			#    break

			if(k1 == k2):
				p1 = person1[k1]
				p2 = person2[k2]
				
				euc_sqr+=((p1-p2)*(p1-p2))                #euclidean algorithm
				cond =True
				
	if (cond==False):
		return 0
  
	euc_result=sqrt(euc_sqr)                                      #euclidean algorithm
  
	return euc_result


def pearson(person1,person2):
	

	pea_sub_p1 = 0                                    #pearson algorithm Variable   
	pea_sub_p2 = 0
	pea_sub_sq_p1 = 0
	pea_sub_sq_p2 = 0
	pea_sub_p1p2 = 0
	pea_result=0
	n=0
	cond = False                         # to avoid such x/0 
	for k1 in person1:                  # k is the key value of the dict (id of restaurant)
		for k2 in person2:
			if(k1 < k2):
				break

			if(k1 == k2):
				p1 = person1[k1]
				p2 = person2[k2]
							
				pea_sub_p1+=p1                                     #pearson algorithm    
				pea_sub_p2+=p2
				pea_sub_sq_p1+=(p1*p1)
				pea_sub_sq_p2+=(p2*p2)
				pea_sub_p1p2+=p1*p2
				n+=1
				cond =True
				break
	if (cond==False):
		return 0
	pea_result=(((n)*(pea_sub_p1p2))-((pea_sub_p1)*(pea_sub_p2)))/( sqrt(((n)*(pea_sub_sq_p1)-((pea_sub_p1)*(pea_sub_p1)))*((n)*(pea_sub_sq_p2)-((pea_sub_p1)*(pea_sub_p1)))))  #pearson algorithm result 
	#pea_result=((n*pea_sub_p1p2)-(pea_sub_p1*pea_sub_p2))/( sqrt((n*pea_sub_sq_p1-pow(pea_sub_p1,2))(n*pea_sub_sq_p2-pow(pea_sub_p2,2))) ) 
	return pea_result

def CosinAveraged(person1,person2):    # person1 , person2 is dictionary have (id of Restaurant) and (rating)
	cos_bast = 0
	cos_sqr1 = 0
	cos_sqr2 = 0
	#person11 = sorted(person1.items(), key=operator.itemgetter(0))
	#person22 = sorted(person2.items(), key=operator.itemgetter(0))
	cond = False                         # to avoid such x/0 
	for k1 in person1:                  # k is the key value of the dict (id of restaurant)
		for k2 in person2:
			#if(k1[0] < k2[0]):
			#    break

			if(k1 == k2):
				p1 =person1[k1]
				p2 =person2[k2]
				cos_bast+=p1 * p2                          #cos algorithm
				cos_sqr1+=p1 * p1
				cos_sqr2+=p2 * p2
				
				cond =True
				break
	if (cond==False):
		return 0
	cos_result = cos_bast / ((sqrt(cos_sqr1)) * (sqrt(cos_sqr2))) ##cos algorithm result
  


	return cos_result

#atef = {'1':3,'2':5,'10':1}
#eissa = {'4':3,'3':2,'4':4}

#data = {'atef' : {'1':3,'2':5,'10':1},'eissa' : {'2':3,'10':2,'11':4},'hassan' : {'4':3,'3':2,'4':4},
#'magdy' : {'2':1,'10':2,'11':4},'sleem' : {'2':3,'10':2,'11':4},'engy' : {'1':3,'2':5,'10':1}}

#result = CosinAveraged(atef,eissa)
#r = ((5 * 3) + (1 * 2)) / ((sqrt(26)) * sqrt(13))



def getSimilarities(person,data):    # person is string and data dictionary      output is dict id of user and it similarity score
	sim_score = {}
	sim_resut = 0
	
	for person2 in data:
		if(person != person2):
			sim_resut = CosinAveraged(data[person],data[person2])
			sim_score[person2] = sim_resut
	return sim_score


def recom(person_sim,person,data): 
	rec_res_total = {}
	rec_res_simSum={}
	rec_res={}
	for id_user in person_sim:   #give me one from the user with similarity
		sim=person_sim[id_user]  #save the similarity score in sim
		for id_res in data[id_user]: # give me the user rating dic key  ex (wavlez : 5)
			
			if id_res in rec_res_total.keys():
				rec_res_total[id_res]+=sim*data[id_user][id_res]
			else:
				rec_res_total[id_res]=sim*data[id_user][id_res]        
			if id_res in rec_res_simSum.keys():
				rec_res_simSum[id_res]+=sim
			else:
				 rec_res_simSum[id_res]=sim
	for key in rec_res_total:
		rec_res[key]=rec_res_total[key]/rec_res_simSum[key] 

	sorted_x =list(reversed(sorted(rec_res.items(), key=operator.itemgetter(1))))
	return(sorted_x)


def loadDataset(filename,all_data_set={},list_of_tuple=[]):
	
	with open(filename)  as csvfile:
		lines = csv.reader(csvfile)
		#to separate header of data
		headers = next(lines)[21:42]
		#prepare the traning set to be dictionary of lists
		dataset = list(lines)
		for row in dataset:
			all_data_set[row[0]]={}
			for h,v in zip(headers,row[21:42]):
				if v=="":
					continue
				all_data_set[row[0]][h]=float(v)
		




#######################################
#TESTING
#######################################



all_data_set = {}

										
loadDataset("itarget.csv",all_data_set)


#sim = getSimilarities("Atef",data)
#eissaa =   recom(sim,'atef',data)

#test our new data
similarities = getSimilarities("a44b92ffc230e5467234433ac3803960",all_data_set)
recommendations = recom(similarities,'a44b92ffc230e5467234433ac3803960',all_data_set)

#print(eissaa)
#print(recommendations)
for(k,v) in recommendations:
	print(k+": "+str(v))
#for i in eissaa:
#    print("");
#    print(i,eissaa[i]);