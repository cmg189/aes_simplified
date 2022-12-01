#!/usr/bin/env python3
import sys
import re

# main point of execution
def main():

	# receive filenames from user
	input_file, key_file, output_file = get_files()

	# read plaintext and key from files
	message, key = get_text(input_file, key_file)

	# remove all punctuation marks and whitespace
	preprocess = parse_text(message)

	# output preprocess
	output_data("\nPreprocessing:\n", preprocess)

	# encrypt text by substitution using vigenere cypher
	cipher_text, cipher_groups = Vcipher_encrypt(preprocess, key)

	# output encrypted text
	output_data("\nSubstitution:\n", cipher_text)

	# add padding if necessary
	#padded_text, padded_groups = padding(cipher_text, cipher_groups, len(key))
	padding(cipher_text, cipher_groups, len(key))

	# end program
	sys.exit("\n\nProgram ended\n")

# receives filenames from user
def get_files():
	print("\n\n\t\t\tAES Simplified\n\n")
	input_file = input("Enter the name of the input file containing the plaintext: ")
	key_file = input("\nEnter the name of the input file containing the encryption key: ")
	output_file = input("\nEnter the name of the output file that will contain the cyphertext: ")

	return input_file, key_file, output_file

# read plaintext and key from files
def get_text(input_file, key_file):

	# read all lines from input file
	message = []
	try:
		file_obj = open(input_file, "r")
		for line in file_obj:
			message.append(line)
		file_obj.close()
	except IOError:
		print("\nCould not read from: ", input_file)
		print("\nProgram ended\n")
		sys.exit()

	# read key from file
	key_list = []
	try:
		file_obj = open(key_file, "r")
		for line in file_obj:
			key_list.append(line)
		file_obj.close()
	except IOError:
		print("\nCould not read from: ", key_file)
		print("\n\nProgram ended\n")
		sys.exit()

	# turn list into string
	key = "".join(key_list)
	final_key = key.strip()

	return message, final_key

# remove all punctuation marks and whitespace
def parse_text(message):

	# remove all punctuation marks and whitespace from list
	new_message = []
	new_string = ''
	for line in message:
		for char in line:
			if char not in (' ', '\t', '\n', '?', '!', '.', ':', ';', '-', '~', ',', '\'', '`', '\"', '[', ']', '(', ')', '<', '>', '{', '}'):
				new_string += char
		new_message.append(new_string)
		new_string = ''

	# remove any empty stings from list
	count = 0
	for line in new_message:
		if re.search("^\s*$", line):
			new_message.pop(count)
		count += 1

	# turn the list into one string
	final_message = "".join(new_message)

	return final_message

# output information
def output_data(title, data):
	print(title)
	if type(data) is str:
		print(data)
	else:
		for line in data:
			print(line)
	return

# encrypt text by substitution using vigenere cypher
def Vcipher_encrypt(text, key):
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	size = len(alphabet)

	letter_to_index = dict( zip(alphabet, range(size)) )	# mapping a, b, c, ... to 0, 1, 2, ...
	index_to_letter = dict( zip(range(size), alphabet) )	# mapping 0, 1, 2, ... to a, b, c, ...

	# split text into groups based on the size of the key
	group_text = [ text[i:i +len(key)] for i in range(0, len(text), len(key))]

	encrypted_text = ''
	# traverse through each group then traverse through each letter in each group
	for group in group_text:
		count = 0
		for char in group:
			# create an index from mapping the current letter in the group with the current letter in the key
			# encrypt the letter by using that index to get its corresponding letter
			mapping_index = ( letter_to_index[char] + letter_to_index[key[count]] ) % size
			encrypted_text += index_to_letter[mapping_index]
			count +=1

	# group the encrypted text into groups of size len(key)
	encrypted_groups = [ encrypted_text[i:i +len(key)] for i in range(0, len(encrypted_text), len(key))]

	return encrypted_text, encrypted_groups

# add padding if necessary
def padding(text, groups, key_len):
	# check if last group in list has 16 chars or not
	last_index = len(groups) -1
	num = len(groups[last_index]) % key_len

	# add padding to the last group if needed
	if num is not 0:
		print("padding")
	else:
		print("no padding")

	return

# execute program
if __name__ == "__main__":
	main()
