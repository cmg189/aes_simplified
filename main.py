#!/usr/bin/env python3

# main point of execution 
def main():

	# recieve filenames from user
	input_file, key_file, output_file = get_files()



	print("\nProgram ended\n\n")

# recieves filenames from user
def get_files():
	print("\n\n\t\t\tAES Simplified\n\n")
	input_file = input("Enter the name of the input file containing the plaintext: ")
	key_file = input("\nEnter the name of the input file containing the encryption key: ")
	output_file = input("\nEnter the name of the output file that will contain the cyphertext: ")

	return input_file, key_file, output_file

# execute program
if __name__ == "__main__":
	main()
