## AES Simplified

Python based program that implements an encryption system using a simplified version of the Advanced Encryption System (AES)

## Table of Contents

1. [Description](#description)
2. [Program Output](#output)
3. [Execution](#exe)
4. [Function Headers](#function)
5. [Other](#other)

## Description <a name="description"></a>

AES simplified start by asking the user for the filenames of the files that have the plaintext to be encrypted, the encryption key, and the file where the resulting cyphertext will be written to

**NOTE:**
When executing this program, ensure to have files in the same directory containing plaintext, the encryption key, and where the cyphertext will be written to


AES simplified encrypts plaintext using various methods implemented by AES such as:

- Polyalphabetic Substitution via the Encryption Key

	A Vigenere table is used to encrypt the plaintext

- Padding

	Further encryption is done on 4x4 character blocks therefore, the character A is used for padding so that the length of the message is divisible by 16

- Row Shifts

	Shifting of the four rows are done in the following fashion: row one is unshifted, row two is shifted one position, row three is shifted two positions, and row four is shifted three positions. All shifts are done to the left

- Parity Bits

	Each character's binary representation will have either an even amount of 1s or an odd amount of 1s. If it is odd then its most significant bit set to 1, if it is even then no changes will occur

- Mix Columns

	This step diffuses the data by transformation. The transformation is performed by multiplying the circulant MDS matrix with each column of the blocks of characters

## Program Output <a name="output"></a>


## Execution <a name="exe"></a>

	To execute run the command `python3 main.py`

## Function Headers <a name="function"></a>

``` python
get_files()
```

Description:

	Receives filenames from user

Parameters:

	None

Return:

	`input_file` String representing the name of the file that contains the plaintext to be encrypted

	`key_file` String representing the name of the file that contains the encryption key

	`output_file` String representing the name of the file that the cyphertext will be written to

---

``` python
```

Description:



Parameters:



Return:



---

``` python
```

Description:



Parameters:



Return:



## Other <a name="other"></a>
