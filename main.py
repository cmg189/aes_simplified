#!/usr/bin/env python3
import sys
import re
from collections import deque

# main point of execution
def main():

	# receive filenames from user and read plaintext and key
	input_file, key_file, output_file = get_files()
	message, key = get_text(input_file, key_file)

	# remove all punctuation marks and whitespace then output and save results
	preprocess = parse_text(message)
	#print("\nPreprocessing:\n\n", preprocess, sep='')

	# encrypt text by substitution using vigenere cypher, output and save results
	cipher_text, cipher_groups = Vcipher_encrypt(preprocess, key)
	#print("\nSubstitution:\n\n", cipher_text, sep='')

	# add padding if necessary, output and save results
	padded_text, padded_groups = padding(cipher_text, cipher_groups, len(key))
	#output_data("\nPadding:\n", padded_text, len(key))

	# shift rows of groups, output and save results
	shifted_text, shifted_groups = shift_rows(padded_text, padded_groups, len(key))
	#output_data("\nShifted Rows:\n", shifted_text, len(key))

	# add parity bit if necessary, output and save results
	parity_text = parity_bit(shifted_text, len(key))
	#output_doubles("\nParity Bit:\n", parity_text, len(key))

	# mix columns
	mix_columns(parity_text, len(key))
	#output_doubles("\nMix Columns:\n", mixed_text, len(key))

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

# output data by grouping 4x4
def output_data(title, data, key_size):
	print(title)

	# print data in 4x4 blocks
	count = 0
	for i in range(0, len(data), key_size):
		for j in range(4):
			for k in range(4):
				print(data[count], end='')
				count += 1
			print('')
		print('')

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
def padding(text, groups, key_length):

	# check if last group in list has 16 chars or not
	last_index = len(groups) -1
	remainder = len(groups[last_index]) % key_length

	# add padding to the last group if needed
	fill_data = 'A'
	if remainder != 0:
		# determine how many spots need to be padded
		last_block = groups[last_index]
		fill_amount = key_length - len(last_block)

		# pad data
		for count in range(fill_amount):
			last_block += fill_data

		# update list and create new string with updated data
		groups.pop(last_index)
		groups.append(last_block)
		updated_text = "".join(groups)

		return updated_text, groups
	else:
		# return original data if no padding is required
		return text, groups

# shift rows
def shift_rows(text, groups, key_length):
	num_cols = 4
	block_size = key_length / num_cols

	# create 2d list of 4x4 blocks
	collection = []
	for i in range(len(groups)):
		block = []
		line = groups[i]
		curr_index = 0
		for j in range(int(block_size)):
			row = []
			for k in range(num_cols):
				row.append(line[curr_index])
				curr_index +=1
			block.append(row) # new row of 4 chars
		collection.append(block) # new group of 4x4

	# shift rows of each block
	# 1st row: no shift, 2nd row: left 1, 3rd row: left 2, 4th row: left 3
	shifted_collection = []
	for block in collection:
		count = 0
		shifted_block = []
		temp_row = []
		for row in block:
			new_row = deque(row)
			if count != 0:
				new_row.rotate(-count) # rotate entire row left
			count += 1
			shifted_block.append(new_row) # saving shifted row
			temp_char = []
			for char in new_row:
				temp_char.append(char) # making new list out of shifted rows
			temp_row.append(temp_char)
		shifted_collection.append(temp_row)

	# turn list into one string
	shifted_text = ''
	for line in shifted_collection:
		temp_text = ''
		for row in line:
			temp_text = ''.join(row)
			shifted_text = shifted_text + temp_text

	return shifted_text, shifted_collection

# add parity bit if necessary
def parity_bit(text, key_length):
	# a char requires a parity bit if its binary ascii value contains an odd amount of 1s
	# party bit of 1 will be added to the most significant bit

	# predetermined which uppercase letters will need a parity bit and the resulting hexadecimal value
	chars = ['C', 'E', 'F', 'I', 'J', 'L', 'O', 'Q', 'R', 'T', 'W', 'X']
	hex = ['c3', 'c5', 'c6', 'c9', 'ca', 'cc', 'cf', 'd1', 'd2', 'd4', 'd7', 'd8']
	bits = dict( zip(chars, hex) )

	hex_string = ''
	for i in range(len(text)):
		# replace chars that need parity bit
		if text[i] in bits:
			hex_string += bits.get(text[i])
		# convert chars to hex value if not party bit is needed
		else:
			chars_hex = format( ord(text[i]), 'x' )
			hex_string += chars_hex

	return hex_string

# output data by grouping 4x4 and grouping each element by 2
def output_doubles(title, data, key_size):
	print(title)

	# print data in 4x4 blocks grouping each output by 2
	count = 0
	for i in range(0, len(data), key_size):
		for j in range(4):
			for k in range(8):
				if(count >= len(data)):
					return
				print(data[count], end='')
				count += 1
				if count % 2 == 0:
					print(' ', end='')
			print('')
		print('')

	return

# mix columns
def mix_columns(text, key_length):
	# group text by 2 chars to represent hex
	hex = [(text[i:i+2]) for i in range(0, len(text), 2)]

	# turn hex into binary
	bins = []
	for i in range(len(hex)):
		prefix_bin = bin(int(hex[i], 16))
		short_bin = prefix_bin[2:]	# removing the prefix 0b of binary number
		full_bin = short_bin.rjust(8, '0') # ensure all binaries are 8 bits long
		bins.append(full_bin)

	# group binary numbers by 4 to represent 4x4 blocks
	bin_groups = []
	for i in range(0, len(bins), 4):
		bin_row = []
		count = i
		for j in range(4):
			bin_row.append(bins[count])
			count +=1
		bin_groups.append(bin_row)

	#
	#	FIX ME: ONLY LOOPS THROUGH ENTIRE FIRST COLUMN
	#			MUST LOOP THROUGH ALL COLUMNS
	#
	# traverse all bin_groups by groups of 4 representing 4x4 block size
	mixed_cols = []
	for i in range(0, len(bin_groups), 4):
		count = i
		# traverse each column in the 4x4 group, start of new 4x4 block
		for cols in range(4):
			# 0c, 1c, 2c, 3c
			temp = []
			for row in range(count, count+4):
				#print("[", row, "] [", cols, "]")
				# r0, r0, r0, r0
				temp.append( bin_groups[row][cols] )
			transformed = RGF_multiples(temp)
			mixed_cols.append(transformed)


	# 00, 01, 02, 03
	# 10, 11, 12, 13
	# 20, 21, 22, 23
	# 30, 31, 32, 33
	print(mixed_cols)
	return


# multiplication with Rijndael's Galois Field
def RGF_multiples(columns):
	msb1 = '00011011'
	rgf = [ [2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2] ]

	sum = []
	#
	#	FIX ME: MUST TRAVERSE THROUGH ENTIRE RGF NOT JUST ONE INDEX
	#
	line = rgf[0]
	for i in range(len(line)):
		if line[i] == 1:
			sum.append(columns[i])
		elif line[i] == 2:
			shifted_bin = int(columns[i], 2) << 1
			shifted_str = bin(int(shifted_bin))
			if len(shifted_str) == 10:
				# necessary bc if the most significant bit is 0 it will be discarded
				# therefore need to add it back on there so that the shifted_str[3:] works
				temp_str = '0b0'
				temp_str += shifted_str[2:]
				shifted_str = temp_str
			shifted_str = shifted_str[3:] # remove 0b and the most significant bit
			if shifted_str[0] == '1':
				# must turn into binary
				shifted_str = int(shifted_str,2) ^ int(msb1,2)
				final_shift = bin(int(shifted_str))
				final_shift = final_shift[2:]
				sum.append(final_shift)
			else:
				sum.append(shifted_str) # do nothing, already in binary
		elif line[i] == 3:
			shifted_bin = int(columns[i], 2) << 1
			shifted_str = bin(int(shifted_bin))
			if len(shifted_str) == 10:
				# necessary bc if the most significant bit is 0 it will be discarded
				# therefore need to add it back on there so that the shifted_str[3:] works
				temp_str = '0b0'
				temp_str += shifted_str[2:]
				shifted_str = temp_str
			shifted_str = shifted_str[3:] # remove 0b and the most significant bit
			temp = int(shifted_str,2) ^ int(columns[i],2)
			x = bin(int(temp))
			x = x[2:]
			x = x.rjust(8, '0')
			if x[0] == '1':
				# must turn into binary
				x = int(x,2) ^ int(msb1,2)
				final_shift = bin(int(x))
				final_shift = final_shift[2:]
				sum.append(final_shift)
			else:
				sum.append(x) # do nothing, already in binary

	# XOR all resulting binaries
	first = int(sum[0],2) ^ int(sum[1],2)
	first = bin(int(first))
	first = first[2:]

	second = int(first,2) ^ int(sum[2],2)
	second = bin(int(second))
	second = second[2:]

	third = int(second,2) ^ int(sum[3],2)
	third = bin(int(third))
	third = third[2:]
	third = third.rjust(8, '0')

	# turn result from XOR to hex
	bin_result = int(third,2)
	hex_result = hex(bin_result)
	hex_result = hex_result[2:]

	return hex_result

# execute program
if __name__ == "__main__":
	main()
