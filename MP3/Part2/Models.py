import os
import sys
import math


# Class A = 1
# Class B = -1

class Multinomial:
	def __init__(self,train_data,test_data,case):
		self.case = case
		self.k = 1
		self.A_dic = train_data[0]
		self.B_dic = train_data[1]
		self.A_total = train_data[2]
		self.A_voc_size = train_data[3]
		self.B_total = train_data[4]
		self.B_voc_size = train_data[5]
		self.A_dic_copy = train_data[0]		# used for calculating confusion matrix
		self.B_dic_copy = train_data[1]
		self.A_dic_len = len(self.A_dic) - 1
		self.B_dic_len = len(self.B_dic) - 1
		self.test = test_data
		self.test_label = []		# list of true labels of each line (document)
		self._get_test_label()				
		self.test_prediction = []   # list of prediction for each line (document)
		self._param_estimate()
		self._predict()


	def _param_estimate(self):
		A_word_list = self.A_dic.keys()
		B_word_list = self.B_dic.keys()
		k = 1
		A_V = self.A_voc_size
		B_V = self.B_voc_size

		for word in A_word_list:
			count = self.A_dic[word] 
			likelihood = float( (count+k)/(self.A_total+A_V) ) 	
			self.A_dic[word] = likelihood
			if word not in B_word_list:
				likelihood = float( k/(self.B_total+B_V) )
				self.B_dic[word] = likelihood
		
		for word in B_word_list:
			count = self.B_dic[word] 
			likelihood = float( (count+k)/(self.B_total+B_V) )		
			self.B_dic[word] = likelihood
			if word not in A_word_list:
				likelihood = float( k/(self.A_total+A_V) )
				self.A_dic[word] = likelihood


	def _get_test_label(self):
		for line in self.test:
			if line[0] == 1:
				self.test_label.append(1)
			elif line[0] == -1:
				self.test_label.append(-1)


	def _predict(self):

		for line in self.test:
			A_posterior = math.log10(1)
			B_posterior = math.log10(1)
			for pair in line:
				if (pair == 1) or (pair == -1):
					continue
				else:
					word = pair[0]
					count = pair[1]
					if count == 1:
						if word in self.A_dic:
							A_posterior += (math.log10(self.A_dic[word]))
						if word in self.B_dic:
							B_posterior += (math.log10(self.B_dic[word]))	
					else:
						while count != 0:
							if word in self.A_dic:
								A_posterior += (math.log10(self.A_dic[word]))
							if word in self.B_dic:
								B_posterior += (math.log10(self.B_dic[word]))
							count -= 1

			if self.case == 1:		# Movie Classification, prior of A, B are both 0.5
				A_posterior = float(A_posterior * 0.5)
				B_posterior = float(B_posterior * 0.5)
				if A_posterior > B_posterior:
					self.test_prediction.append(1)
				else:
					self.test_prediction.append(-1)
			elif self.case == 2:	# Conversation Classification, prior of A = 440/878, prior of B = 438/878
				A_posterior = float(A_posterior * 440/878)
				B_posterior = float(B_posterior * 438/878)
				if A_posterior > B_posterior:
					self.test_prediction.append(1)
				else:
					self.test_prediction.append(-1)


	def get_accuracy(self):
		RIGHT = 0
		WRONG = 0
		for i in range(len(self.test_label)):
			if self.test_label[i] == self.test_prediction[i]:
				RIGHT += 1
			else:
				WRONG +=1
		accuracy = float(RIGHT / (RIGHT+WRONG))
		return accuracy


	def get_top_likelihood(self):
		A_top_likelihood = []
		B_top_likelihood = []
		for A_key, value in sorted(self.A_dic.items(), key=lambda kv: kv[1], reverse=True):
			A_top_likelihood.append(A_key)
		for B_key, value in sorted(self.B_dic.items(), key=lambda kv: kv[1], reverse=True):
			B_top_likelihood.append(B_key)
		A_top_ten = A_top_likelihood[0:10]
		B_top_ten = B_top_likelihood[0:10]
		print('Top 10 Words in Class A:',A_top_ten)
		print('Top 10 Words in Class B:',B_top_ten)


	def get_odds_ratio(self):
		A_odds = []
		A_top_ten_odds = []
		A_word_list = self.A_dic_copy.keys()	# only consider words appeared in A
		for word in A_word_list:
			A_prob = self.A_dic[word]
			B_prob = self.B_dic[word]
			odds = float(A_prob/B_prob)
			A_odds.append([word,odds])
		A_sorted_odds = sorted(A_odds,key= lambda x:x[1],reverse=True)
		temp = A_sorted_odds[0:10]
		for i in range(10):
			A_top_ten_odds.append(temp[i][0])
		print('Top 10 Odds Ratio (in class A not B): ',A_top_ten_odds) 


	def get_confusion_matrix(self):
		actual_A_predict_A = 0
		actual_A_predict_B = 0
		actual_B_predict_A = 0
		actual_B_predict_B = 0
		for i in range(len(self.test_label)):
			if self.test_label[i] == 1:				# actual A
				if self.test_prediction[i] == 1:	# predict A
					actual_A_predict_A += 1
				else:								# predict B
					actual_A_predict_B += 1
			else:									# actual B
				if self.test_prediction[i] == 1:	# predict A
					actual_B_predict_A += 1
				else:								# predict B
					actual_B_predict_B += 1

		print('confusion matrix:   predict A   predict B')
		print('     	  acutal A   ',actual_A_predict_A,'       ',actual_A_predict_B)
		print('          actual B   ',actual_B_predict_A,'       ',actual_B_predict_B)



class Bernoulli(Multinomial):
	def __init__(self,train_data,test_data,case):
		self.case = case
		self.k = 1
		self.A_dic = train_data[0]
		self.B_dic = train_data[1]
		self.A_dic_len = len(self.A_dic) - 1
		self.B_dic_len = len(self.B_dic) - 1
		self.test = test_data
		self.test_label = []		# list of true labels of each line (document)
		self._get_test_label()				
		self.test_prediction = []   # list of prediction for each line (document)		
		self._param_estimate_Ber()
		self._predict_Ber()


	def _param_estimate_Ber(self):
		A_word_list = self.A_dic.keys()
		B_word_list = self.B_dic.keys()

		for word in A_word_list:
			count = self.A_dic[word] 
			likelihood = float( (count+self.k)/(self.A_dic_len+2) ) 	
			self.A_dic[word] = likelihood
			if word not in B_word_list:
				likelihood = float( self.k/(self.B_dic_len+2) )
				self.B_dic[word] = likelihood
		
		for word in B_word_list:
			count = self.B_dic[word] 
			likelihood = float( (count+self.k)/(self.B_dic_len+2) ) 	
			self.B_dic[word] = likelihood
			if word not in A_word_list:
				likelihood = float( self.k/(self.A_dic_len+2) )
				self.A_dic[word] = likelihood


	def _predict_Ber(self):
		for line in self.test:
			A_posterior = math.log10(1)
			B_posterior = math.log10(1)
			for pair in line:
				if (pair == 1) or (pair == -1):
					continue
				else:
					word = pair[0]
					if word in self.A_dic:
						A_posterior += math.log10(self.A_dic[word])
					if word in self.B_dic:
						B_posterior += math.log10(self.B_dic[word])
					
			if self.case == 1:		# Movie Classification, prior of A, B are both 0.5
				A_posterior = float(A_posterior * 0.5)
				B_posterior = float(B_posterior * 0.5)
				if A_posterior > B_posterior:
					self.test_prediction.append(1)
				else:
					self.test_prediction.append(-1)
			elif self.case == 2:	# Conversation Classification, prior of A = 440/878, prior of B = 438/878
				A_posterior = float(A_posterior * 440/878)
				B_posterior = float(B_posterior * 438/878)
				if A_posterior > B_posterior:
					self.test_prediction.append(1)
				else:
					self.test_prediction.append(-1)


	def get_odds_ratio_Ber(self):
		A_odds = []
		A_top_ten_odds = []
		A_word_list = self.A_dic.keys()
		for word in A_word_list:		# only consider words appeared in A
			A_prob = self.A_dic[word]
			B_prob = self.B_dic[word]
			odds = float(A_prob/B_prob)
			A_odds.append([word,odds])
		A_sorted_odds = sorted(A_odds,key= lambda x:x[1],reverse=True)
		temp = A_sorted_odds[0:10]
		for i in range(10):
			A_top_ten_odds.append(temp[i][0])
		print('Top 10 Odds Ratio (in class A not B): ',A_top_ten_odds) 



class Multinomial_40(Multinomial):
	def __init__(self,train_data,test_data):
		self.k = 1
		self.all_dic = train_data[0]		# list of dictionaries
		self.all_total = train_data[1]
		self.all_voc_size = train_data[2]
		self.all_prior = train_data[3]
		self.test = test_data
		self.test_label = [] 		 		# list of true labels of each line (document)
		self._get_test_label_40()				
		self.test_prediction = []   		# list of prediction for each line (document)
		self._param_estimate_40()
		self._predict_40()


	def _get_test_label_40(self):
		for line in self.test:
			true_class = int(line[0])
			self.test_label.append(true_class)


	def _param_estimate_40(self):
		all_word_list = [None] * 40
		for i in range(0,40):
			all_word_list[i] = self.all_dic[i].keys()		# get keys for each class

		for i in range(0,40):
			for word in all_word_list[i]:
				count = self.all_dic[i][word] 
				likelihood = float( (count+self.k) / (self.all_total[i]+self.all_voc_size[i]) ) 	
				self.all_dic[i][word] = likelihood
				for j in range(0,40):
					if word not in all_word_list[j]:
						likelihood = float( self.k/(self.all_total[j]+self.all_voc_size[j]) )
						self.all_dic[j][word] = likelihood
		

	def _predict_40(self):

		for line in self.test:
			all_posterior = [0] * 40
			for n in range(0,40):
				all_posterior[n] = math.log10(self.all_prior[n])		# add prior first
			for i in range(1,len(line)):
				pair = line[i]
				word = pair[0]
				count = int(pair[1])
				if count == 1:
					for j in range(0,40):
						if word in self.all_dic[j]:
							all_posterior[j] += math.log10(self.all_dic[j][word])	
				else:
					while count != 0:
						for j in range(0,40):
							if word in self.all_dic[j]:
								all_posterior[j] += math.log10(self.all_dic[j][word])
						count -= 1

			max_posterior = all_posterior[0]
			for j in range(0,40):
				if all_posterior[j] > max_posterior:
					max_posterior = all_posterior[j]
					max_j = j
			self.test_prediction.append(max_j)



class Bernoulli_40(Multinomial_40):
	def __init__(self,train_data,test_data):
		self.k = 12
		self.all_dic = train_data[0]
		self.all_prior = train_data[1]
		self.all_dic_len = [0] * 40
		for i in range(0,40):
			self.all_dic_len[i] = len(self.all_dic[i]) - 1
		self.test = test_data
		self.test_label = []		# list of true labels of each line (document)
		self._get_test_label_40()			
		self.test_prediction = []   # list of prediction for each line (document)		
		self._param_estimate_Ber_40()
		self._predict_Ber_40()



	def _param_estimate_Ber_40(self):
		all_word_list = [None] * 40
		for i in range(0,40):
			all_word_list[i] = self.all_dic[i].keys()		# get keys for each class

		for i in range(0,40):
			for word in all_word_list[i]:
				count = self.all_dic[i][word] 
				likelihood = float( (count+self.k)/(self.all_dic_len[i]+2) ) 	
				self.all_dic[i][word] = likelihood
				for j in range(0,40):
					if word not in all_word_list[j]:
						likelihood = float( self.k/(self.all_dic_len[j]+2) )
						self.all_dic[j][word] = likelihood
		


	def _predict_Ber_40(self):
		for line in self.test:
			all_posterior = [0] * 40
			for n in range(0,40):
				all_posterior[n] = math.log10(self.all_prior[n])		# add prior first
			for i in range(1,len(line)):
				pair = line[i]
				word = pair[0]
				for j in range(0,40):
					if word in self.all_dic[j]:
						all_posterior[j] += math.log10(self.all_dic[j][word])	
					
			max_posterior = all_posterior[0]
			for j in range(0,40):
				if all_posterior[j] > max_posterior:
					max_posterior = all_posterior[j]
					max_j = j
			self.test_prediction.append(max_j)



	def get_odds_ratio_Ber_40(self):
		A_odds = []
		A_top_ten_odds = []
		A_word_list = self.A_dic.keys()
		for word in A_word_list:		# only consider words appeared in A
			A_prob = self.A_dic[word]
			B_prob = self.B_dic[word]
			odds = float(A_prob/B_prob)
			A_odds.append([word,odds])
		A_sorted_odds = sorted(A_odds,key= lambda x:x[1],reverse=True)
		temp = A_sorted_odds[0:10]
		for i in range(10):
			A_top_ten_odds.append(temp[i][0])
		print('Top 10 Odds Ratio (in class A not B): ',A_top_ten_odds) 








