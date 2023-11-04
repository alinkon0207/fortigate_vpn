import subprocess
import os
import sys
import shutil

def runCalcProcesses(nProcess, salt, block, blockSize, bufferSize):
	processList = []
	for i in range(nProcess):
		cmd = "python3 calc_hashes.py %s 0x%x 0x%x 0x%x" % (salt, block, blockSize, bufferSize)
		p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		processList.append(p)

		block += blockSize
	return processList

def waitCalcProcesses(processList):
	for i in range(len(processList)):
		p = processList[i]

		output = b''
		errout = b''
		while True:
			output += p.stdout.read()
			errout += p.stderr.read()
			if output.strip().endswith(b"done"):
				break
			if errout != b'':
				print("ERROR OCCURED")
				print(errout.decode())
				exit()


def runFindProcesses(nProcess, salt, value, offset, block, blockSize):
	processList = []
	for i in range(nProcess):
		filePath = "%s/%s-%s.pickle" % (salt,'%08x'%block,'%08x'%(block+blockSize))
		cmd = "python3 find.py %s %s 0x%x %s" % (salt, value, offset, filePath)
		# print(cmd)
		p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		processList.append(p)

		block += blockSize
	return processList

def waitFindProcesses(processList):
	result = b''
	for i in range(len(processList)):
		p = processList[i]

		output = b''
		errout = b''
		while True:
			output += p.stdout.read()
			errout += p.stderr.read()
			if b"result: " in output:
				break
			if errout != b'':
				print("ERROR OCCURED")
				print(errout.decode())
				exit()

		result = output.split(b"result: ")[1]

		if b'None' not in result:
			break

	return result

def main():

	maxBlockSize = 0x100000000

	nProcess	= int(sys.argv[1], 16)
	salt		= sys.argv[2]
	block		= int(sys.argv[3], 16)
	blockSize	= int(sys.argv[4], 16)
	bufferSize	= int(sys.argv[5], 16)
	values		= sys.argv[6]
	offsets		= sys.argv[7]

	valueList	= values.split(',')
	offsetList	= offsets.split(',')
	offsetList	= list(map(lambda x: int(x,16),offsetList))
	resultList	= [None] * len(valueList)

	assert(len(valueList) == len(offsetList))

	print('values : %s' % valueList)
	print('offsets: %s' % offsetList)
	
	curBlock = block
	while curBlock < maxBlockSize:
		print("[+] calculating 0x%x-0x%x"%(curBlock, curBlock+blockSize*nProcess))
		processList = runCalcProcesses(nProcess, salt, curBlock, blockSize, bufferSize)
		waitCalcProcesses(processList)

		for i in range(len(resultList)):
			result = resultList[i]
			if result == None:
				value  = valueList[i]
				offset = offsetList[i]
				print("[+] finding %s at 0x%x"%(value, offset))

				processList = runFindProcesses(nProcess,salt,value,offset,curBlock,blockSize)
				result = waitFindProcesses(processList).strip()

				if b'None' not in result:
					if result.startswith(b"b'"):
						result = result.split(b"b'")[1].split(b"'")[0].decode()
					resultList[i] = result

					for i in range(nProcess):
						block = curBlock + i*blockSize
						if int(result,16) >= block and int(result,16) < (block+blockSize):
							filePath = "%s/%s-%s.pickle" % (salt,'%08x'%block,'%08x'%(block+blockSize))
							destPath = "%s/%x_%s.%s-%s.pickle" % (salt,offset,value,'%08x'%block,'%08x'%(block+blockSize))
							shutil.copyfile(filePath,destPath)

					print('    found: %s' % result)

		for i in range(nProcess):
			block = curBlock + i*blockSize
			filePath = "%s/%s-%s.pickle" % (salt,'%08x'%block,'%08x'%(block+blockSize))
			os.remove(filePath)

		if None not in resultList:
			print('resultList: %s' % resultList)
			break

		curBlock += blockSize*nProcess

if __name__ == '__main__':
	main()
