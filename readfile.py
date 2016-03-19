'''

Georgios Pierris
Cognitive Robotics Research Centre,
University of Wales, Newport
August 2011

Class to read data from an AMC motion file into a Frame class in Python and interact with them.
AMC file has to be in the AMC format used in the online CMU motion capture library.

INSTALATION:
	Paste amc.py and frame.py in the same folder as your project, or add them in your path
	and simply:
		import amc
	or
		from amc import *
	or
		import amc as whatever

	depending on how you prefer to use it

For examples on how to use the data read the main() function.
For help, more information, or for addtions to this class please contact us at

georgios.pierris@newport.ac.uk
georgios@pierris.gr



'''

class Frame:


	def __init__(self, frameNum):

		self.frameNum = frameNum
		self.frameDictionary = dict()


	def addJoint(self, name, values):

		self.frameDictionary[name] = values


class AMC:

	frames = []
	header = []

	def __init__(self):
		pass

	def __init__(self, filename):

		self.loadAMC(filename)


	def loadAMC(self, filename):

		try:
			fid = open(filename, 'r')
		except:
			print 'Load file error!'
			print 'Cannot open ' + filename
			return

		allFile = fid.readlines() #Read all the file

		noHeaderData = self.readHeader(allFile) #Read the header of the file and save it for future use. Then return the data without the header

		#print noHeaderData

		for line in noHeaderData:

			words = line.rstrip().split()

			try:

				frameNum = int(words[0]) #If there is an exception then it is not a number so we continue on the same frame
				self.frames.append(Frame(frameNum))

			except:

				tempVals = []
				for i in words[1:]: #Iterate through all values after the string
					tempVals.append(float(i))

				self.frames[-1].addJoint(words[0], tempVals) # The name of the joint will be the keyword to the dictionary

		return




	# Read the header of the amc file and return the rest for processing.
	def readHeader(self, allFile):

		for index, line in enumerate(allFile):
			#print index, line
			if('DEGREES' in line):
				self.header.append(allFile[0:index+1]) #Ignore the header
				return allFile[index+1:]



	# Return all the values of a specific joint
	def getAllValuesOf(self, nameOfJoint):

		tempList = []

		for frame in self.frames:
			if nameOfJoint in frame.frameDictionary:
				tempList.append(frame.frameDictionary[nameOfJoint])
			else:
				print 'Error: ' + nameOfJoint + ' does not exist!'
				return []

		return	tempList


	# Return all the values of a specific joint
	def getAllValuesInOrder(self, sequence):

		allData = []
		row = []
		for frame in self.frames:
			for joint in sequence:
				for value in frame.frameDictionary[joint]:
					row.append(value)
			allData.append( row )
			row = []

		return allData



	#Usefull for writing the data to a file. Returns a line with all the values for every frame if called after a getAllValuesOf
	def printableVector(self, vector):

		string = ''
		for i in vector:
			for j in i:
				string = string + str(j) + ' '
			string = string.rstrip()
			string = string + '\n'
		return string # Skip the last space



	# For those familiar with the Matlab script that returns everything on single matrix
	# Every line of the map is one frame
	def matlabScriptLikeMatrix(self):

		sequence = [	'root',
				'lowerback',
				'upperback' ,
				'thorax',
				'lowerneck',
				'upperneck',
				'head',
				'rclavicle',
				'rhumerus',
				'rradius',
				'rwrist',
				'rhand',
				'rfingers',
				'rthumb',
				'lclavicle',
				'lhumerus',
				'lradius',
				'lwrist',
				'lhand',
				'lfingers',
				'lthumb',
				'rfemur',
				'rtibia',
				'rfoot',
				'rtoes',
				'lfemur',
				'ltibia',
				'lfoot',
				'ltoes']
		allData = []
		row = []
		for frame in self.frames:
			for joint in sequence:
				for value in frame.frameDictionary[joint]:
					row.append(value)
			allData.append( row )
			row = []

		return allData




# If the file is not imported to a different program run a demo
# This main() function also serves as a minimal documentation of the AMC class
def main():

	amc = AMC('test.amc')

	#WARNING: Frames start from zero!!!
	print '\nThe header of the file:\n'
	print amc.header, '\n\n'


	#Example 1
	# Getting all the values of 'ltoes' from frame 3 to 7 (the end is not included)
	print '\n\n----------\n', 'Example 1\n', '----------\n\n'
	print 'Getting all the values of \'ltoes\' from frame 3 to 7\n\n'
	ltoes = amc.getAllValuesOf('ltoes')[2:7]
	print '\'ltoes\' as a vector: \n', ltoes, '\n\n'
	print '\n\'ltoes\' as a printable vector:\n', amc.printableVector(ltoes)
	print '\n\n'

	print 'Getting all the values of \'root\' from frame 2 to 5\n\n'
	root = amc.getAllValuesOf('root')[1:5]
	print '\'root\' as a vector: \n', root, '\n\n'
	print '\n\'root\' as a printable:\n', amc.printableVector(root)
	print '\n\n\n'



	#Example 2
	#Every row is a frame, and we have 62 columns with all the values
	print '----------\n', 'Example 2\n', '----------\n'
	print '\nLoading all .amc file in a single matrix\n'
	allData = amc.matlabScriptLikeMatrix()
	print 'Size of matrix ', len(allData), ' x ', len(allData[0]), ' -> (frames) x (parameters)'
	#print allData # Will print LOADS of data
	print '\n\n'


	#Example 3
	# We focus only on a few parameters from some specific frames
	# As in example 2 by we take only the specific joints we want and in the desired sequence
	print '----------\n', 'Example 3\n', '----------\n'
	print '\nWe focus only on a few parameters from some specific frames\n'
	print 'We read only the following parameters in that order'

	sequence = ['ltoes', 'root', 'lthumb'] # This will be the sequence of the data
	print sequence
	dataset = amc.getAllValuesInOrder(sequence)
	print '\nSize of matrix ', len(dataset), ' x ', len(dataset[0]), ' -> (frames) x (parameters)'
	print '\n\nFrames from 3 to 4 using only the desired parameters:\n'
	print amc.printableVector(dataset[3:5])
	print '\n\n\n'



if __name__ == "__main__":
    main()
