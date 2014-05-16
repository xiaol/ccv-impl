
import cnnclassify

def test():
	results =  cnnclassify.cnnclassify("../samples/dex.png".encode('utf8'), "../samples/image-net-2012.sqlite3".encode('utf8'))
	cnnclassify.end()
	for (k, v) in results.items():
		print wordsDict[k],' ',v
	
wordsDict = {}
def initWords():
	words = open("../samples/image-net-2012.words")
	i = 0
	for line in words.readlines():
		wordList = line.split(',')
		wordsDict[i] = line
		i += 1

if __name__ == '__main__':
	initWords()	
  	while True:
  		result = test()
