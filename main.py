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
	key = []
	try:
		file_obj = open(key_file, "r")
		for line in file_obj:
			key.append(line)
		file_obj.close()
	except IOError:
		print("\nCould not read from: ", key_file)
		print("\n\nProgram ended\n")
		sys.exit()

	return message, key

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

	return new_message

# output information
def output_data(type, data):
	print(type)
	for line in data:
		print(line)
	return

# execute program
if __name__ == "__main__":
	main()
