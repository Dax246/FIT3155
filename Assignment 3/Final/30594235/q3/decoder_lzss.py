"""
Assignment 3 Question 3 FIT3155
Author: Damien Ambegoda 30594235
"""
import sys


def elias_decoder(code, start_index=0):
    """ Given the code and the index of that code that begins the encoded section, this method returns the integer
    represented by that section

    :param code: entire header
    :param start_index: index of the code that begins the section that needs to be decoded
    :return:
    """
    i = start_index
    read_length = 1
    while i < len(code):
        next_length = code[i:i+read_length]
        if next_length[0] == '0':
            next_length = next_length.replace('0', '1', 1)
            next_length_integer = int(next_length, 2) + 1
            i += read_length
            read_length = next_length_integer
        else:
            return int(next_length, 2), i+read_length


def huffman_decoder(code):
    """ Decodes the header to determine the huffman encoding for each character

    :param code:
    :return: dictionary containing the code for each character in the string and the index of the header after the
    huffman codes (to determine where the data of the header begnis)
    """

    unique_characters, encoding_start_index = elias_decoder(code)
    huffman_dict = {}
    curr_index = encoding_start_index
    while len(huffman_dict) < unique_characters:
        ascii_code = code[curr_index:curr_index+7]
        curr_index += 7
        read_length, index = elias_decoder(code, curr_index)
        curr_index = index
        huffman_dict[code[index:index+read_length]] = chr(int(ascii_code, 2))
        curr_index += read_length
    return huffman_dict, curr_index

def lzss_decoder(code):
    """
    Given a code, it decodes the header to identify the huffman encoding and then uses the rest of the code to
    determine the string encoded
    :param code: header containing huffman encoding + data containing string encoded
    :return: string decoded
    """
    huffman_dict, data_index = huffman_decoder(code)
    total_formats, curr_index = elias_decoder(code, data_index)
    res = []
    current_no_of_format = 0
    while current_no_of_format < total_formats:
        if code[curr_index] == '1':
            x = 1
            curr_index += 1
            while curr_index - 1 + x < len(code):
                char = huffman_dict.get(code[curr_index:curr_index+x])
                if char is not None:
                    res.append(char)
                    current_no_of_format += 1
                    curr_index += x
                    break
                x += 1
        elif code[curr_index] == '0':
            curr_index += 1
            starting_res_length = len(res)
            offset, curr_index = elias_decoder(code, curr_index)
            length, curr_index = elias_decoder(code, curr_index)
            for i in range(length):
                res.append(res[starting_res_length - offset + i])
            current_no_of_format += 1
    return "".join(res)


if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    input_string = f.read()
    f.close()

    output = lzss_decoder(input_string)
    f = open("output_decoder_lzss.txt", "w")
    f.write(output)
    f.close()