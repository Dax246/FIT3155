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


print(lzss_decoder("000001101000010000001111111100110001011101111010000001011101011100100001011100111011000001011100011010110001111011111100000100110111011110111110100110011011101111011100100001001101110111101101100111000110111011110110010011000011011101111010111011001001101110111101010100001100110111011110100110001100011011101111010001010100001100010111100110011100011010111011101010001011011011101000001001010110111100010010010001010000110100011110001000011010001001011100001111000011100100100011110000101100110000110100000110000100010001111101110000100011011100000001100101111110110000110010110110010000010101010111100100010101001010110000011101000111010111001101001000101111110001001101001000101101101010001100101000101011110000011000010001001110111000110010000110010101100111010010001000001110001100010100001110110100010100000001001010101010000111101000001101000110111100110011111110101110101001111111101111010110110101010100110110110101110111100011110001111011110100111001101101101110111001101111101011011011100010111110101000111001101101110111101111011011111110111101100110011101011111010001010110110111011110101111110000011001111001111110101010011000011100110101010001101101101110000000111010101110001111011111110000111001111001111001100110000111010111000101001101000111111110001011011000000011000010001101110011001101111000011110100000001100001000110100111111001101101010101111110011100000111110111101101100100011110011111001111111101110011000001001111011110101001111001110000111100011110111101010110011101101111111011111010110011101101110001010101111101111110001110001111110001010011111100011000001000001001101101110111001111000101001111110101111110011100111011000000011101110001011010000111010101111101011111010010000001101010011111010101111010110100111110000010101011100010010011010110100110101011000011111111011110000000101011010011110110101101110011001111000100110110110100000010110101000010010101111100111101110001110101000110101101000111010101001000001011010100111010101111101011110111111011111011100011100110110111111000111010101000111101110101111110001011110100110011010101111110001010100111110000001111011011111001101001110011011010011111110101110101000111101100000111000101000110010000010101101101111101100000101111110011100110110111110001101101110111010111100011110010000010100111101110100011000001010001010001011100001000000101110101000110101101100100000011011110110000010110001101111000101101101101011111010111111001101111000111101110011111110000011001111001111110111111000111000111111001110000011111010011100111011011000011110001111000111101111011111110110000001110010011111110011010101101101000011011111010000000011100011100011101011111000010000000100000111100010100111111001101111110111010011111110101100100000011100100111000011101101110111111000001110010010011101000011101010111110100000010101101001110101000000001001100010011100100000111000100101110011111111011110101101101010101001101101101011111100010101111110111001101000110000010110011000010111000010111110100001100111011011100010101000000101000000000100111001100110000010001111011111011000001110000100000100110001100000101000110011101111000011101111110110110011010000111000100110101011011100000010101101001110101101001111001101001110101110101000110110110111000000101000110011000001010101000110000010100101100000010000111111101010111111011000001011001110111011010010000010110100100010110000010011100001111111101111010001110011100110000011111101111110011001101011100000011101000001001000001001111110000111001100000101011110111101101010011111101010110110111001000001010001100001101001110001111100010001101011010011111111000100110000111010110110111001100111101110100011111100000101110011011000001010011110111001111001110101011110001101100000001100011000100101111011010101011111000011110101011111100011100010011011011011100000010100010100011110100001000111010111010111110110110011010110100111100011111010001011011011010011110111101010001110011011011101100000011010000001011101011101011001110110110111011101011010000001110000100011000001010111110001101000001010011111111000101111100010111011101000111100011110011011000000101101011000100000001110010110000100110110100000101000111111110011110011111000000111110101111100111111001100000101111000111100011000011111111000010000000011100011101111011011011111111110100111001110110111100000101101000011000000110011000010011111000001011111011111000001010000010001001101011101010001111011111111101110011000000000010110010101100000011100000111110111100111111001101101010001010110011010011011111000101110001001110000111100011110001111011110111010101111001000000110011000011011001110000011111001101010110110100001101111101011001111001111011101000110000010100111101110000011011011101111010111111011101000110101101001111111001101100000010111010101110001101101011111100011111110111110101100111011011010111100001000001001101011001111110000010100111111101010011011110000111101000000101100011000101100110111100000110000111111110111100000001011010010001001010000100010000010111111001111000101001000000011111000100111000101111110111101011000110000010111100100110011110001001100001110101101101110010000011100100010011001110110101101000111010111110111101101010101111111000110011100100000111000000100010111000101011110000111011111000001011011000110000001111001000100110001011100110001100111000001111110101000110000010011111101110000010110110001111101010011111111010100111100010000000000111001010101110000110111101101011011001110101111111011110101110011001111011111011111111101011001101000011000111000110110100001111001100110101010001110001011100000000101101111011110110100001110111111010010000001100101011110000010011001111000111111010110011111111010101111010110100100000111000101001110011011011111110111101101110011110011100111011010110101010100110101011111100010101001000111100111000011110101111100110100010010000110011110001110001001101101101011111010111100111001101011111100010011100001111111101111001110101001101001111110000111001101101110111000111101111010000000011000011000001010100010111010111111001110011010110100010000001110101011000001011001010111010110101111110001101101011111000101110001001000001010111010001001010101100010101111000011101111111111011110110101010111110100001001111001100111111000110110000001110001111011110110100000000000111001101110111111000000111010111111110101110100000000101000111000000000010101001101100000001001100010111010100011100110110111111001110000011111110111001101011010011110010000001100001011100001111010101111011011011101001111011000000110011001110111110101111110000101111111010110011010111100111000110000000101000001101010100000001111010000101110110101101000111010111111000001100111100100011101000101110001010011101011010100111100111000011111111011110011101010011010011111101000011001111001110111110000010110000001110000111100110011010101000111000101110001010011111111010101111110010000001110011011110011111101010100111100010001000001010111000111111000010001110100100000101011111000100111000111000100110110110111010001101101101110111110000111001101101101000000111000001101100000111001010000010010111110001110101111011111100010111110101011111000101110001001111110111101101010101111000000110001001110111000000110010000010110100001011110100100000001000100010110111111001000000011001011111000111000111110011010001001000011001101011111010100011100110110101111110001111101011110011100110101111110001001110000111111101000101111001000001011111000111101101110001010101111101101100111010000001011101100111010110100111111000001011110101010011111100011101000000101111110000100110101110101000111101111111010111110011000110110110101100011101000010001110101110101100111011000000001011001111101010011000001100001111000111100011110111101011110011100111011111000001011000110001001100000110011110011010000101111110011010101010001111111100001011111101111110110110011010000000000011111011101111101000000001010100010000000101000110011101101010011111110011100000111110100111001110110000001010001110001101010000100010000011100000100111100010100100000001000100010011100111111100000100010000011100001000001001010011001101111110011111000000111000001111011010110100011010110100111100111101110001110101010011010001111111011110110101010000001010011000111110101100110101111001110001100000101001100000101101000011101010011011000000101000101000101111000000001011100100111111110001010111100001110111111111110110101011111001000000010011000101111001111110100010100000101011101101001101001000000110000000010110101101011111100011011010010000010110101101110011111100110100010010101111001111001100011001101101000010000010110110100010111111110101011110101000000111000001000011011101110011000001001111011110101001111001110000111111101000101111110101001000000110100101111100111111000111010111111000111010000101111110111111110001010011000011011111011011101110010000000100000001000001111100010010111111110000111101010111111000111000100110110110111000000101010001000100000001110000101011000001010001110001001000001011110110101111101110100100000101001011011110011111110011010110100111100110000111001100000100110100011111111001111001000000111110000110010000001100100000100110000010011001111000000001011101000001111010110100111111011110000110100010110110110100011110011001101010110001111101100000011011000111111100011011010101010001111011101011110011011011101110111110001011100010011111110111111011011001101000011100010011010101101110000001010001000111100001011111110111000110110100001100111100110011110001010011111111010110011010111000001011100110001111101011101000011001011100110111100000111110111101101010100000001100011011000001010100010001011110101011110101011111011111111010111110011110111000111010100010001111101110001100000101011110111100001110101111110011011000000101110011000100111001110001111100010001110000010011100001111000111100011110000101111101000010001111011111010000001110000110000101101111110001110000000010100100000010110101101001111001101001111111000101001111011000000110110001111000001111111000110110100001110111111111110000011001111001000000011010000101100110100010000000101100010000111000001010000100001001111110000011011011010110110111001000000010101011101101010101001101111010110000000010001011111011000001010011110111101111001110101011110110110111111110111010001100011001011101111010011110001100111100111000011"))


# if __name__ == '__main__':
#     f = open(sys.argv[1], "r")
#     input_string = f.read()
#     f.close()
#
#     output = lzss_decoder(input_string)
#     f = open("output_decoder_lzss.txt", "w")
#     f.write(output)
#     f.close()