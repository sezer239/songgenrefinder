from maxlist import MaxList
import pandas as pd
import re
import math
import operator
import time, sys
import sys
import os
import time
from multiprocessing import Pool

from PrintTable import printTable
from WordCounter import wordCountDistance
from ProgressBar import progressBar

# TODO: seperate algorightm and printing logic
def findClosestLyrics(data,inpData,kth,x,y):
	"""Applies the kth nearst algoritm using word count as distance 

    Parameters:
    data (list): Lyric data that will be used for comparing inpData
	inpData (str): Input lyric data
	kth (int): how many neaighbort
	x (int): Print the algorithm procces onto temrianl window x
	y (int): Print the algorithm procces onto temrianl window y
	
    Returns:
    list: kth nearset values 

   """
	maxList = MaxList(kth , lambda it , inp : inp['dist'] < it['dist'])
	count = 0 
	badStrings = 0
	beginTime = currentMilliTime()
	lastTimePrinted = 0
	rcount = len(data)
	for elem in data:
		if type(inpData) is str and type(elem[3]) is str:
			dis = wordCountDistance( re.findall(r'\w+', inpData), re.findall(r'\w+',elem[3]))

			maxList.pushAndReplace({
				"genre": elem[2],
				"song": elem[0],
				"artist": elem[1],
				"dist": dis
			})
		else:
			badStrings += 1

		count += 1

		currentMili = currentMilliTime()
		if  count >= rcount - 5 or currentMili - lastTimePrinted > 500:
			lastTimePrinted = currentMili 
			progressBar(count, rcount , " Completed, Time Elapsed ~= " + str((currentMili - beginTime)/1000) + " secs, " + str(count) + " Songs compared, Bad Data:" + str(badStrings) , x , y)
		
	return maxList.getItems()

howToUse = "Usage:\n[trainingFile] [inputFile] [k] [howManyRow] [threads]"
errorNotDigitRowCount = "[trainingFile] [inputFile] [k] --->[howManyRow]<--- [threads] \nerror [howManyRow], should be a number"
errorNotDigitK = "[trainingFile] [inputFile] -->[k]<-- [howManyRow] [threads]\nerror, [k] should be a number"
errorInvalidTraningFile = "-->[trainingFile]<-- [inputFile] [k] [howManyRow] [threads] \nerror, [trainingFile] does not exits"
errorInvalidInpFile = "[trainingFile] -->[inputFile]<-- [k] [howManyRow] [threads] \nerror, [inputFile] does not exits"
errorInvalidThread = "[trainingFile] [inputFile] [k] [howManyRow] -->[threads]<--\nerror, [threads] is invalid"


currentMilliTime = lambda: int(round(time.time() * 1000))

if __name__ == "__main__":

	#Argument assingment and validity cheking
	
	if len(sys.argv) != 5 + 1 or sys.argv[1] == "help":
		print (howToUse)
		exit()
	
	os.system("clear")

	traningLyricFile = sys.argv[1]
	inpLyricFile = sys.argv[2]

	if not os.path.isfile('./' + traningLyricFile ):
		print errorInvalidTraningFile 
		print'Error the file: ./' + traningLyricFile + ' Doest not exist'
		exit()
	print "Traning lyric file is " , traningLyricFile

	if not os.path.isfile('./' + inpLyricFile ):
		print errorInvalidInpFile 
		print 'Error the file: ./' + inpLyricFile + " Doest not exist" 
		exit()
	print "Input lyric file is " , inpLyricFile

	if not str.isdigit(sys.argv[3]):
		print( errorNotDigitK )
		exit()	

	kth = int(sys.argv[3])

	if not str.isdigit(sys.argv[4]):
		print( errorNotDigitRowCount )
		exit()

	if not str.isdigit(sys.argv[5]):
		print( errorInvalidThread )
		exit()


	rowcount = int(sys.argv[4])
	threadCount = int(sys.argv[5])

	#Reading the files and assining into correct vars

	print "Finding the closest genre with the k-value of " , kth 
	print "Using the first " , rowcount , " rows for the k-th closest point algorithm" 

	print "Reading the traning file ", traningLyricFile," ..."
	data = pd.read_csv(traningLyricFile, nrows=rowcount ,usecols=[1,3,4,5]).apply(lambda x: x.astype(str).str.lower())
	print "Converting the read file to list read from ", traningLyricFile ,"..."
	data = data.values.tolist()

	print "Opening the input lyric file ",inpLyricFile,"... "
	inpFile = open(inpLyricFile , "r")
	print "Reading the input lyric file ",inpLyricFile,"... "
	inpData = inpFile.read()
	inpData = inpData.lower()
	datalen = len(data)

	#User can purposely assing larger values to read all the data from the given lyric files
	if rowcount > datalen:
		print "Given rowcount is:" , rowcount , " but lenght of the data is " , datalen, " setting rowcount = " , datalen
		rowcount = datalen

	#Creating threads
	#create pool of threads with max procces count of threadCount
	pool = Pool(processes=threadCount)

	#this vars keeps the splited data from the variable 'data'; basically splietedData contains len(data) / threadCount chunks of data
	splitedData = []
	#all results from apply_async kept here
	threadResults = []
	#all the result from threadResults[i] are kept here
	results = []

	#Splited the original data for threads
	for i in range(threadCount):
		#print  i , "* (",rowcount,"/threadCount): (",i,"+1)*(",rowcount,"/threadCount)=", i * (rowcount/threadCount),",", (i+1)*(rowcount/threadCount)
		splitedData.append(data[i * (rowcount/threadCount): (i+1)*(rowcount/threadCount)])
	
	#Delete the original data to save memory
	del data[:]

	#Create 'threadCount' number of threads and assing the splited data to apply algorithm, later we can access the thread results from threadResults[i]
	print "----Spreading the algorightm into",threadCount,"diffrenet threads----"
	for i in range(threadCount):
		threadResults.append( pool.apply_async(findClosestLyrics, (splitedData[i], inpData,kth,0,12 + i)) ) 

	#Close the pool so it wont accept any more
	pool.close()

	#wait for all of the threads to finish
	for thread in threadResults:
		thread.wait()

	#Destroy the pool and remaing workers
	pool.join()
	pool.terminate()
	pool = None

	#Delete the splited data for memory because it wont be needed anymore
	del	splitedData[:]

	#Get the data from threads and asing them into 'results'
	for thread in threadResults:
		results.append( thread.get(timeout=None) )
	
	#Delete threadResult since it wont be needed again
	del threadResults[:]
	
	#Print some space before prining the results, this is needed because of how threads print their procces onto terminal screen 
	for i in range(threadCount):
		print "\n"
	
	#Create MaxList for combining the results from threads
	maxList = MaxList(kth , lambda it , inp : inp['dist'] < it['dist'])

	#Combine the results into maxList, maxList will keep only N maximum amount of data defined by its constructor, in this case it will compare the distances
	# and keep the maximum 10 data
	for res in results:
		for it in res:
			#pushAndReplace will look all the data and if there is smaller value than given input it will replace them
			maxList.pushAndReplace(it)

	items = maxList.getItems()
	print "[DONE]"
	print "------ Printing the closest", kth , " genres of lyrics and distances ------"

	#sums will keep the sums of each genre, e.g. if there is 2 rock it will sum them as 1/x1^2 + 1/x2^2	
	sums = {}
	#disatacneTable is for printing to terminal more beatifuly, 1'st item on the list is the col names
	distanceTable = []
	#put the col names so it can print beatifiyulll
	distanceTable.append(["Artist", "Song" , "Genre" , "Distance"])
	
	for it in items:
		#calculate the weigted sums in here
		if it['genre'] in sums:
			sums[ it['genre'] ] = sums[ it['genre'] ] + (1 / (it['dist']**2) )
		else:
			sums[ it['genre'] ] = 1/(it['dist']**2)
			
		#while calculating the sums, also build the table for printing 
		distanceTable.append( [ it['artist'], it['song'],  it['genre'], it['dist'] ] )

	printTable(distanceTable)

	#delte cuz it wont be needed again
	del distanceTable[:]

	print "------ Weigted Sums ------"
	
	#These will keep track of latgest sums and its genre, largerst sum is the estimated genre
	largestVal = 0
	largestValText = ""

	#weightedSumTable weigted sums of each genre
	weightedSumTable = []
	weightedSumTable.append(["Genre" , "Weighted Sum"])

	for it in sums:
		#while builging the sums table also find the largest sum
		if largestVal < sums[it]:
			largestVal = sums[it]
			largestValText = it
		
		#build the sums table for printing beatifuly
		weightedSumTable.append([it , sums[it]])
		#print "Weigteg sum of " , it , " is : " , sums[it]

	printTable(weightedSumTable)

	print "[So the estimated genre of the input lyric is " , largestValText , " with the value of " , largestVal,"]"

	exit()
