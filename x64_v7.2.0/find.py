from binascii import unhexlify
import sys
import glob
import pickle

def find_seed(hash_buffer_map, value, offset):
	base_offset = 0x1c00-28
	matchedKey = None
	for d in hash_buffer_map:
		if hash_buffer_map[d][base_offset+offset:].startswith(value):
			matchedKey = d
			break

	return matchedKey

def find_in_file(filePath, value, offset):
	# print('searching %s' % filePath)
	with open(filePath,"rb") as f:
		hash_buffer_map = pickle.load(f)

	result = find_seed(hash_buffer_map, value, offset)
	return result


def find(salt,value,offset):
	result = None

	pickleFileList = glob.glob('%s/*.pickle'%salt)

	for pickleFile in pickleFileList:
		result = find_in_file(pickleFile, value, offset)
		if result != None:
			break
	return result


def main():


	salt = sys.argv[1]
	value = sys.argv[2]
	offset = int(sys.argv[3], 16)
	value = sys.argv[2]
	value = unhexlify(value.encode())


	if len(sys.argv) == 4:
		result = find(salt,value,offset)
	elif len(sys.argv) > 4:
		filePath = sys.argv[4]
		result = find_in_file(filePath, value, offset)
		# result = find(salt,value,offset)


	print("result: %s" % result)



if __name__ == '__main__':
	main()
