# Take averages of three sizes of buffer

class class_average:
	def __init__(self,size1,size2,period):
		self.buffer1  = [0.0]*size1
		self.buffer2  = [0.0]*size2

		self.buffer1Ind = 0
		self.buffer2Ind = 0

		self.__size1 = size1
		self.__size2 = size2
		
		self.__period = period


	def store(self,value):
		self.buffer1[self.buffer1Ind] = value
		self.buffer2[self.buffer2Ind] = value

		if self.buffer1Ind < self.__size1 -1 :
			self.buffer1Ind += 1
		else:
			self.buffer1Ind = 0

		if self.buffer2Ind < self.__size2 -1:
			self.buffer2Ind += 1
		else:
			self.buffer2Ind = 0

		# Output averages per unit period
		self.average1 = sum(self.buffer1)/self.__size1/self.__period
		self.average2 = sum(self.buffer2)/self.__size2/self.__period

if __name__ == '__main__':
		average = class_average(3,6)
		testValue = 0
		testIncrement = 1
		for step in range(12):
			average.store(testValue)
			testValue +=testIncrement
			print(average.buffer1,average.average1)
			print(average.buffer2,average.average2,"\n")
		
		
