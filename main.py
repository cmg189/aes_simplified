#!/usr/bin/env python3
import sys

# main point of execution
def main():

	# receive filenames from user
	input_file, key_file, output_file = get_files()

	# read plaintext and key from files
	message, key = get_text(input_file, key_file)
	print(message)
	print("\n", key)
	print("\nProgram ended\n\n")

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
# execute program
if __name__ == "__main__":
	main()
