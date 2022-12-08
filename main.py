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
	print("\nPreprocessing:\n\n", preprocess, sep='')
	save_data("\nPreprocessing:\n\n", preprocess, output_file, '1')

	# encrypt text by substitution using vigenere cypher, output and save results
	cipher_text, cipher_groups = Vcipher_encrypt(preprocess, key)
	print("\nSubstitution:\n\n", cipher_text, sep='')
	save_data("\nSubstitution:\n\n", cipher_text, output_file, '1')

	# add padding if necessary, output and save results
	padded_text, padded_groups = padding(cipher_text, cipher_groups, len(key))
	output_data("\nPadding:\n", padded_text, len(key))
	save_data("\nPadding:\n\n", padded_text, output_file, '2')

	# shift rows of groups, output and save results
	shifted_text, shifted_groups = shift_rows(padded_text, padded_groups, len(key))
	output_data("\nShifted Rows:\n", shifted_text, len(key))
	save_data("\nShifted Rows:\n\n", shifted_text, output_file, '2')

	# add parity bit if necessary, output and save results
	parity_text = parity_bit(shifted_text, len(key))
	output_doubles("\nParity Bit:\n", parity_text, len(key))
	save_data("\nParity Bit:\n\n", parity_text, output_file, '3')

	# mix columns
	mixed_text = mix_columns(parity_text, len(key))
	output_doubles("\nMix Columns:\n", mixed_text, len(key))
	save_data("\nMix Columns:\n\n", mixed_text, output_file, '3')

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
	hex_str = [(text[i:i+2]) for i in range(0, len(text), 2)]

	# turn hex into binary
	bins = []
	for i in range(len(hex_str)):
		prefix_bin = bin(int(hex_str[i], 16))
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

	# hex groups
	hg = []
	for i in range(0, len(hex_str), 4):
		hgr = [] # rows
		count = i
		for j in range(4):
			hgr.append(hex_str[count])
			count +=1
		hg.append(hgr)

	# 2d list reordering
	reorder = []
	for skip in range(0, len(hg), 4):
		count = skip
		for j in range(4):
			cols = []
			for i in range(count, count+4):
				cols.append(hg[i][j])
			reorder.append(cols)

	# hex into binary
	collection = []
	for column in reorder:
		tbins = []
		for i in range(len(column)):
			prefix_bin = bin(int(column[i], 16))
			short_bin = prefix_bin[2:]	# removing the prefix 0b of binary number
			full_bin = short_bin.rjust(8, '0') # ensure all binaries are 8 bits long
			tbins.append(full_bin)
		collection.append(tbins)

	# perform the mix columns procedure
	transformed = []
	for columns in collection:
		# column transformation with rijndael galois field
		a0 = (int(rgf(columns[0], 2),2) ^ int(rgf(columns[1], 3),2) ^ int(columns[2], 2) ^ int(columns[3], 2))
		a1 = (int(columns[0], 2) ^ int(rgf(columns[1], 2),2) ^ int(rgf(columns[2], 3),2) ^ int(columns[3], 2))
		a2 = (int(columns[0], 2) ^ int(columns[1], 2) ^ int(rgf(columns[2], 2),2) ^ int(rgf(columns[3], 3),2))
		a3 = (int(rgf(columns[0], 3),2) ^ int(columns[1], 2) ^ int(columns[2], 2) ^ int(rgf(columns[3], 2),2))

		store = []
		a0 = str(a0)
		a0 = a0.rjust(8, '0')
		a0 = hex(int(a0))
		store.append(a0[2:])

		a1 = str(a1)
		a1 = a1.rjust(8, '0')
		a1 = hex(int(a1))
		store.append(a1[2:])

		a2 = str(a2)
		a2 = a2.rjust(8, '0')
		a2 = hex(int(a2))
		store.append(a2[2:])

		a3 = str(a3)
		a3 = a3.rjust(8, '0')
		a3 = hex(int(a3))
		store.append(a3[2:])

		transformed.append(store)


	# reorder hex values
	done = []
	for skip in range(0, len(transformed), 4):
		count = skip
		for j in range(4):
			cols = []
			for i in range(count, count+4):
				cols.append(transformed[i][j])
			done.append(cols)

	# turn list into one string
	one_str = ''
	for row in done:
		temp_text = ''
		for chars in row:
			temp_text = ''.join(chars)
			one_str = one_str + temp_text

	return one_str

# perform multiplication
def rgf(value, constant):

	xor_value = '00011011'
	xor_value = bin(int(xor_value, 2))
	xor_value = xor_value[2:]
	xor_value = xor_value.rjust(8, '0')

	extra_step = 0 # msb is 0
	if value[0] == '1':
		extra_step = 1 # msb is 1

	shifted = int(value,2) << 1 # multiply by 2
	shifted = bin(int(shifted))
	# account for shift in binary number if msb is 0
	# 01110011 becomes 110011
	if len(shifted) == 11:
		shifted = shifted[3:]
	elif len(shifted) == 10:
		shifted = shifted[2:]

	# multiplying by 2 or 3
	if constant == 2:
		finished = shifted
	else:
		finished = int(shifted, 2) ^ int(value, 2)
		finished = bin(finished)
		finished = finished[2:]

	# perform another xor
	if extra_step:
		finished = int(finished,2) ^ int(xor_value,2)
		finished = str(finished)
		finished = bin(int(finished))
		finished = finished[2:]  # remove 0b prefix and ensure 8bits
		finished = finished.rjust(8, '0')

	return finished

# write data to file
def save_data(title, data, file, flag):

	try:
		file_obj = open(file, "a")
	except IOError:
		print("\nCould not write to: ", file)
		print("\nProgram ended\n")
		sys.exit()

	if flag == '1':
		file_obj.write(title)
		file_obj.write(data)
		file_obj.write('\n')
	if flag == '2':
		file_obj.write(title)
		# print data in 4x4 blocks
		count = 0
		for i in range(0, len(data), 16):
			for j in range(4):
				for k in range(4):
					#file_obj.write(data[count], end='')
					file_obj.write(data[count])
					file_obj.write(' ')
					count += 1
				file_obj.write('\n')
			file_obj.write('\n')
		file_obj.write('\n')
	if flag == '3':
		file_obj.write(title)
		# print data in 4x4 blocks grouping each output by 2
		count = 0
		for i in range(0, len(data), 16):
			for j in range(4):
				for k in range(8):
					if(count >= len(data)):
						return
					#file_obj.write(data[count], end='')
					file_obj.write(data[count])
					count += 1
					if count % 2 == 0:
						#file_obj.write(' ', end='')
						file_obj.write(' ')
						#file_obj.write('\n')
				file_obj.write('\n')
			file_obj.write('\n')
		file_obj.write('\n')


	file_obj.close()
	return


# execute program
if __name__ == "__main__":
	main()
