"""
Assignment 3 Question 2 FIT3155
Author: Damien Ambegoda 30594235
"""

import heapq
import sys


def elias(n):
    """
    Finds the elias code for integer n
    :param n: integer that needs to be encoded
    :return: binary string containing the elias code for n
    """
    x = bin(n)

    # Binary of the integer without 0b at the front
    code_component = x[2:len(x)]

    last_encoding = code_component
    encodings = [code_component]
    while len(last_encoding) != 1:
        x = bin(len(last_encoding) - 1)
        last_encoding = x[2:len(x)]

        # Converts first char to 0 for length components
        last_encoding = "0" + last_encoding[1:len(last_encoding)]
        encodings.append(last_encoding)

    # code components and list components in the wrong order in encodings. Final string needs to be reversed
    encodings.reverse()
    encodings = "".join(encodings)
    return encodings


def huffman(string):
    """ Encodes a string in a huffman encoding based on each characters occurrence in the string

    :param string: string to encode
    :return: list of binary strings to be used as the code for each letter
    """

    # Position in array for each possible character
    counters = [0] * 96
    for i in range(len(string)):
        char = string[i]

        # index will be 0 if new line character
        index = max(ord(char) - 31, 0)
        counters[index] += 1

    # Pqueue is a priority queue based on the occurrence of each char/substring
    pqueue = []
    codes = []
    for i in range(96):
        codes.append([])

    for i in range(len(counters)):
        if counters[i] > 0:
            if i == 0:
                heapq.heappush(pqueue, (counters[i], '\n'))
            else:
                heapq.heappush(pqueue, (counters[i], chr(i + 31)))

    list_of_symbols = []

    while len(pqueue) > 1:
        min = heapq.heappop(pqueue)
        second_min = heapq.heappop(pqueue)
        list_of_symbols.append(min)
        list_of_symbols.append(second_min)

        for i in range(len(min[1])):
            index = max(ord(min[1][i]) - 31, 0)
            codes[index].append("0")
        for i in range(len(second_min[1])):
            index = max(ord(second_min[1][i]) - 31, 0)
            codes[index].append("1")

        heapq.heappush(pqueue, (min[0] + second_min[0], min[1]+second_min[1]))

    # Codes (list_of_symbols) created are in reverse order
    for i in range(len(codes)):
        if codes[i]:
            codes[i].reverse()
            codes[i] = "".join(codes[i])
    return codes

def header(string):
    """ Converts the string into the header required for question 2
    """
    res = []
    codes = huffman(string)
    unique_characters = 0
    for i in range(len(codes)):
        if codes[i]:
            unique_characters += 1
            str = ""
            if i == 0:
                ascii_binary = bin(10)[2:]
            else:
                ascii_binary = bin(i + 31)[2:]

            # Ensures the binary of the ascii for each character is of length 7
            if len(ascii_binary) < 7:
                number_of_padded_zeroes = 7 - len(ascii_binary)
                padding = ""
                for _ in range(number_of_padded_zeroes):
                    padding += "0"
                ascii_binary = padding + ascii_binary

            str += ascii_binary
            str += elias(len(codes[i]))
            str += codes[i]
            res.append(str)
    unique_characters_string = elias(unique_characters)
    res_combined_into_string = "".join(res)
    return unique_characters_string + res_combined_into_string


if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    input_string = f.read()
    f.close()

    output = header(input_string)
    f = open("output_header.txt", "w")
    f.write(output)
    f.close()