import hashlib
import threading
import pickle
import os
import sys


def gen_hash_buffer(data, salt, bufferSize=0x2000):
	m = hashlib.md5()
	m.update(salt)
	m.update(data[:8])
	m.update(b"GCC is the GNU Compiler Collection.")
	result = m.digest()

	buffer = result
	while bufferSize >= len(buffer):
		m = hashlib.md5()
		m.update(buffer[-16:])
		result = m.digest()
		buffer += result
	return buffer

def calc_hash(data_start,data_end,salt,bufferSize):
	if not os.path.isdir(salt.decode()):
		os.makedirs(salt.decode())

	pickle_file_path = "%s/%s-%s.pickle" % (salt.decode(),'%08x'%data_start,'%08x'%data_end)

	if os.path.isfile(pickle_file_path):
		print("already done")
		return

	hash_buffer_map = {}
	for i in range(data_start,data_end):
		data = '%08x'%i
		if data in hash_buffer_map:
			continue

		data = data.encode()
		h = gen_hash_buffer(data,salt,0x2000)
		hash_buffer_map[data] = h

		# if i % 0x1000 == 0:
			# print("0x%x/0x%x" %(i, data_end))


	pickle_file_path = "%s/%s-%s.pickle" % (salt.decode(),'%08x'%data_start,'%08x'%data_end)
	with open(pickle_file_path,'wb') as f:
		pickle.dump(hash_buffer_map, f)

def main():


	salt = sys.argv[1].encode()
	startblock = int(sys.argv[2], 16)
	blockSize = int(sys.argv[3], 16)
	bufferSize = int(sys.argv[4], 16)

	calc_hash(startblock, startblock+blockSize, salt, bufferSize)
	print('done')

	# cur_block = 0
	# while cur_block < maxBlockSize:
	# 	for i in range(threadNum):
	# 		t = threading.Thread(target=calc_hash, args=(cur_block, cur_block+blockSize, salt, 0x2000))
	# 		t.start()
	# 		threadList.append(t)
	# 		print('thread-%d started: 0x%x' % (i,cur_block))
	# 		cur_block += blockSize

	# 	for t in threadList:
	# 		t.join()

if __name__ == '__main__':
	main()
