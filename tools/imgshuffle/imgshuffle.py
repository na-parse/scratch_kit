#!/usr/bin/python3
# imgshuffle.py
# - shuffles image file names to crease random order slide-show sort for dumb slideshow programs
# - that don't actually include a shuffle option.  Can you believe it, in this day and age?
# - Works by taking current filename + current timestamp and sha256 hashing it to create a
# - a new filename.  Includes an option to revert to 'orig' or an sha1 hash filename based on
# - the actual file contents.  Helps weed out duplicates as well.

import os
import hashlib
import threading
import time

# limit shuffle ops to image files only by extensions
file_exts = [ 'png', 'jpg', 'jpeg', 'gif']

# This only works in current directory right now
# One day this will be a real argument
usedir = './'

# Limiters to restrain our awesomeness
BUFFER_SIZE = 256*1024 # 256k buffer size
MAX_THREADS = 24 # Limit our max simultaneous threads


def get_img_files(usedir,extensions):
	filelist = []
	for file in os.listdir(usedir):
		ext = get_file_ext(file)
		if os.path.isfile(file) and ext in extensions:
			filelist.append(file)
	return filelist


def get_file_ext(filename):
	# Don't check non-file entries like directories
	if not os.path.isfile(filename):
		return False

	filename = filename.split('.')
	if len(filename) <= 1:
		print(f'Unable to find extension in {filename}')
		return None
	ext = filename[len(filename) - 1].lower()
	return ext


def file_rename_shuffle(usedir,filename):
	# Using timestamp in hash will prevent hash-loops
	TS = time.time()
	ext = get_file_ext(filename)
	hashme = f'{TS}_{filename}'
	newfile = f'{hashlib.sha256(hashme.encode("utf-8")).hexdigest()}.{ext}'
	print(f'Shuffle: {filename} -> {newfile}')
	os.rename(filename,newfile)


def file_rename_orighash(usedir,filename):
	ext = get_file_ext(filename)
	filehash = hash_file_sha1(filename)
	if not filehash:
		print(f'ERROR: {filename} could not be hashed.')
		return False
	newfile = f'{filehash}.{ext}'
	if filename == newfile:
		print(f'No Change: {filename} already original hash name')
		return

	# Previously I was doing an isfile check to see if dup
	# This was however my first 'race' condition situation where some threads could
	# be working on renaming causing the dupcheck to pass then still except on the os.rename()
	# Better Python seems to be to just try it and let the FileExistsError exception raise.
	try:
		os.rename(filename,newfile)
		print(f'Filehash Rename: {filename} -> {newfile}')
	except FileExistsError:
		print(f'{filename} not renamed - Duplicate of already hashed {newfile}')


def hash_file_sha1(filename):
	try:
		sha1 = hashlib.sha1()
		with open(filename,'rb') as hashfile:
			while True:
				data = hashfile.read(BUFFER_SIZE)
				if not data:
					break
				sha1.update(data)
		filehash = '{0}'.format(sha1.hexdigest())
		return filehash
	except FileNotFoundError:
		print(f'ERROR: {filename} could not be found.')
	except IOError as e:
		print(f'ERROR: IO issue while reading {filename} - {e}')
	# we only get here if there was a problem


def file_rename_testcase(usedir,filename):
	ext = get_file_ext(filename)
	numval = str(time.time()).split('.')[1]
	newfile = f'nicefile_{numval}.{ext}'
	print(f'Test Rename: {filename} -> {newfile}')
	os.rename(filename,newfile)



######################3
# Actual start that should be in a main
imgfiles = get_img_files(usedir,file_exts)

if imgfiles:
	print(f'imgshuffle: Found {len(imgfiles)} img files / Proceed with Shuffle?')
	runme = None
	response = input("[test/orig/yes/no] > ")
	if response.lower() == 'yes':
		runme = file_rename_shuffle
	if response.lower() == 'orig':
		runme = file_rename_orighash
	if response.lower() == 'test':
		runme = file_rename_testcase
	
	start = time.time()

	if runme: 
		threadlist = []
		for file in imgfiles:
			# First catch if we're at max thread count
			if len(threadlist) >= MAX_THREADS:
				# At max threads, push a join and wait for quiesce
				print('... Max Threads ... waiting for queue...')
				for thread in threadlist:
					thread.join()
				#empty the threadlist to make room for the next suckers
				threadlist = []
			
			t = threading.Thread(target=runme,args=[usedir,file])
			t.start()
			threadlist.append(t)

		# Join on the last remainder of the <= MAX_THREADS group
		for thread in threadlist:
			thread.join()

	print(f'[{runme}] completed execution in {int(time.time() - start)} seconds')
