import math

def wordCountDistance(words1, words2):
	word_count1 = {}
	word_count2 = {}
	total_distance = 0
	
	for word1 in words1:
		if word1 in word_count1:
			word_count1[str(word1)] = word_count1[str(word1)] + 1
		else:
			word_count1[str(word1)] = 1
			
	for word2 in words2:
		if word2 in word_count2:
			word_count2[str(word2)] = word_count2[str(word2)] + 1
		else:
			word_count2[str(word2)] = 1
	
	if len(word_count1) >= len(word_count2):
		for word1 in word_count1:
			found = False
			for word2 in word_count2:
				if word1 == word2:
					found = True
					total_distance += (int(word_count1[word1]) - int(word_count2[word2])) ** 2
					break
			if not found:
				total_distance += (int(word_count1[word1]) - 0) ** 2
	else:	
		for word2 in word_count2:
			found = False
			for word1 in word_count1:
				if word2 == word1:
					found = True
					total_distance += (int(word_count2[word2]) - int(word_count1[word1])) ** 2
					break
			if not found:
				total_distance += (int(word_count2[word2]) - 0) ** 2

	#print "max wordcount 1 ", max(word_count1.iteritems(), key=operator.itemgetter(1))
	#print "max wordcount 2 ", max(word_count2.iteritems(), key=operator.itemgetter(1))
	
	if total_distance == 0:
		total_distance = 0.0000001
		
	return math.sqrt(total_distance)