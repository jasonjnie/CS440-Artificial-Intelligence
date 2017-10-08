from Models import *
import os
import sys
import time

# Class A = 1
# Class B = -1


def Create_Train_Dic(text_file):
	A_dic = {}
	B_dic = {}
	A_num_word = 0
	B_num_word = 0
	A_unique_word = 0
	B_unique_word = 0

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = temp[0]					# positive or negative / min_wage or life partners

			if label == '1':
				for pair in temp:
					if (pair == '1') or (pair == '-1') :
						continue
					temp_pair = pair.split(':')
					word = temp_pair[0]
					count = int(temp_pair[1])
					A_num_word += count
					if word in A_dic:		# word aleardy counted, not unique
						A_dic[word] += count
					else:					# new word
						A_dic[word] = count
						A_unique_word += 1
			else:
				for pair in temp:
					if (pair == '1') or (pair == '-1') :
						continue
					temp_pair = pair.split(':')
					word = temp_pair[0]
					count = int(temp_pair[1])
					B_num_word += count
					if word in B_dic:		# word aleardy counted, not unique
						B_dic[word] += count
					else:					# new word, but not unique
						B_dic[word] = count	
						B_unique_word += 1			

	return (A_dic,B_dic,A_num_word,A_unique_word,B_num_word,B_unique_word)



def Create_Train_Dic_Bernoulli(text_file):
	A_dic = {}
	B_dic = {}

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = temp[0]					# positive or negative / min_wage or life partners

			if label == '1':
				for pair in temp:
					if (pair == '1') or (pair == '-1') :
						continue
					temp_pair = pair.split(':')
					word = temp_pair[0]
					if word in A_dic:		# word appear in current document
						A_dic[word] += 1
					else:					# word never appeared in another document before
						A_dic[word] = 1
			else:
				for pair in temp:
					if (pair == '1') or (pair == '-1') :
						continue
					temp_pair = pair.split(':')
					word = temp_pair[0]
					if word in B_dic:		# word appear in current document
						B_dic[word] += 1
					else:					# word never appeared in another document before
						B_dic[word] = 1	

	return (A_dic,B_dic)



def Create_Test_list(text_file):
	words = []								# list of list: every list => [label, (word,count), (word,count)...]

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = temp[0]	

			if label == '1':
				temp_words = [1]
			elif label == '-1':
				temp_words = [-1]

			for pair in temp:
				if (pair == '1') or (pair == '-1') :
					continue
				temp_pair = pair.split(':')
				word = temp_pair[0]
				count = int(temp_pair[1])
				temp_words.append((word,count))
			words.append(temp_words)
	return words



def Create_Train_Dic_40(text_file):
	all_dic = []				# list of dictionaries of 40 classes
	all_prior = [0] * 40								
	for i in range(0,40):
		all_dic.append({})
	all_num_word = [0] * 40
	all_unique_word = [0] * 40

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = int(temp[0])					# Class
			all_prior[label] += 1

			for i in range(1,len(temp)):
				pair = temp[i]
				temp_pair = pair.split(':')
				word = temp_pair[0]
				count = int(temp_pair[1])
				all_num_word[label] += count
				if word in all_dic[label]:			# word aleardy counted, not unique
					all_dic[label][word] += count
				else:					# new word
					all_dic[label][word] = count
					all_unique_word[label] += 1
	check = 0
	for i in range(0,40):
		check += all_prior[i]
		all_prior[i] = float( all_prior[i]/10244 )
	return (all_dic,all_num_word,all_unique_word,all_prior)



def Create_Train_Dic_Bernoulli_40(text_file):
	all_dic = []				# list of dictionaries of 40 classes
	all_prior = [0] * 40								
	for i in range(0,40):
		all_dic.append({})

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = int(temp[0])					
			all_prior[label] += 1

			for i in range(1,len(temp)):
				pair = temp[i]
				temp_pair = pair.split(':')
				word = temp_pair[0]
				if word in all_dic[label]:		# word appear in current document
					all_dic[label][word] += 1
				else:							# word never appeared in another document before
					all_dic[label][word] = 1

	return (all_dic,all_prior)



def Create_Test_list_40(text_file):
	all_words = [] 									# list of list: every list => [label, (word,count), (word,count)...]

	with open(text_file,'r') as file:
		for line in file:
			temp = line.split(' ')
			label = int(temp[0])
			temp_words = [label]					

			for i in range(1,len(temp)):
				pair = temp[i]
				temp_pair = pair.split(':')
				word = temp_pair[0]
				count = int(temp_pair[1])
				temp_words.append((word,count))
			all_words.append(temp_words)
	#print('all words : ',all_words)
	return all_words




if __name__ == "__main__":
	
	MOVIE_TRAIN = Create_Train_Dic('rt-train.txt')					# movie dataset
	CONVERS_TRAIN = Create_Train_Dic('fisher_train_2topic.txt')		# conversation topic dataset
	MOVIE_TEST = Create_Test_list('rt-test.txt')					# movie dataset
	CONVERS_TEST = Create_Test_list('fisher_test_2topic.txt')		# conversation topic dataset

#### Multinomial Model: 1 for Movie Classification, 2 for COnversation Classification ####
	
	print()
	print('******************* Multinomial Model: ********************')
	MOVIE_Multinomial = Multinomial(MOVIE_TRAIN,MOVIE_TEST,1)
	CONVERSE_Multinomial = Multinomial(CONVERS_TRAIN,CONVERS_TEST,2)
	MOVIE_Multi_accuracy = float(MOVIE_Multinomial.get_accuracy())
	print('Movie Multinomial model has accuracy: ',MOVIE_Multi_accuracy)
	CONVERSE_Multi_accuracy = float(CONVERSE_Multinomial.get_accuracy())
	print('Conversation Multinomial model has accuracy: ',CONVERSE_Multi_accuracy)

	print('********* Movie Classification: *********')
	MOVIE_Multinomial.get_top_likelihood()
	MOVIE_Multinomial.get_odds_ratio()
	MOVIE_Multinomial.get_confusion_matrix()
	print('***** Conversation Classification: ******')
	CONVERSE_Multinomial.get_top_likelihood()
	CONVERSE_Multinomial.get_odds_ratio()
	CONVERSE_Multinomial.get_confusion_matrix()


#### Bernoulli Model: 1 for Movie Classification, 2 for COnversation Classification ####

	print()
	print('******************** Bernoulli Model: *********************')
	MOVIE_TRAIN_Ber = Create_Train_Dic_Bernoulli('rt-train.txt')					# movie dataset
	CONVERS_TRAIN_Ber = Create_Train_Dic_Bernoulli('fisher_train_2topic.txt')	# conversation topic dataset


	MOVIE_Bernoulli = Bernoulli(MOVIE_TRAIN_Ber,MOVIE_TEST,1)
	CONVERSE_Bernoulli = Bernoulli(CONVERS_TRAIN_Ber,CONVERS_TEST,2)
	MOVIE_Ber_accuracy = float(MOVIE_Bernoulli.get_accuracy())
	print('Movie Bernoulli model has accuracy: ',MOVIE_Ber_accuracy)
	CONVERSE_Ber_accuracy = float(CONVERSE_Bernoulli.get_accuracy())
	print('Conversation Bernoulli model has accuracy: ',CONVERSE_Ber_accuracy)
	
	print('********* Movie Classification: **********')
	MOVIE_Bernoulli.get_top_likelihood()
	MOVIE_Bernoulli.get_odds_ratio_Ber()
	MOVIE_Bernoulli.get_confusion_matrix()
	print('****** Conversation Classification: ******')
	CONVERSE_Bernoulli.get_top_likelihood()
	CONVERSE_Bernoulli.get_odds_ratio_Ber()
	CONVERSE_Bernoulli.get_confusion_matrix()
	
	
	CONVERSE_TRAIN_40 = Create_Train_Dic_40('fisher_train_40topic.txt')		# conversation topic dataset
	CONVERSE_TRAIN_Ber_40 =Create_Train_Dic_Bernoulli_40('fisher_train_40topic.txt')
	CONVERSE_TEST_40 = Create_Test_list_40('fisher_test_40topic.txt')		# conversation topic dataset	
	CONVERSE_Multinomial_40 = Multinomial_40(CONVERSE_TRAIN_40,CONVERSE_TEST_40)
	CONVERSE_Bernoulli_40 = Bernoulli_40(CONVERSE_TRAIN_Ber_40,CONVERSE_TEST_40)
	CONVERSE_Multi_accuracy_40 = float(CONVERSE_Multinomial_40.get_accuracy())
	print('Conversation Multinomial model has accuracy: ',CONVERSE_Multi_accuracy_40)
	CONVERSE_Ber_accuracy_40 = float(CONVERSE_Bernoulli_40.get_accuracy())
	print('Conversation Bernoulli model has accuracy: ',CONVERSE_Ber_accuracy_40)
	





