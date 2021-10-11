
""" Description of method used to solve question 2, binary_boyermoore, of the assignment.
The standard boyermoore algorithm was used however galil's optimisation was optimised even more for binary. This
algorithm subtracts one from galil_start from the standard algorithm (except when using a matched prefix). This
is a safe skip because normal good suffix ensures a matching substring is shifted forward but it also ensures that
the previous substring does not mismatch for the same reason. For example if 011 was already matched and it mismatches
on a 1, the good suffix method will find a previous substring that matches 011 as well as not being preceded by a 1.
In non binary situations, the character preceding must be checked as good suffix just ensures it is not the same
character that was originally mismatched. In this binary situation, when it ensures it does not mismatch for the same
reason, it actually also finds the matching character as the length of the alphabet is only 2.

Bad Character was also removed from the algorithm as good suffix does the job of bad character in binary alphabets. The
explanation above both finds a matching substring as well as finding a character that matches the mismatched character.
This was removed from the algorithm but it does not save comparisons.

"""
import sys

# Modified from algorithm presented in FIT3155 lectures
def binary_boyermoore(txt, pat):

    # Finds the z values and z suffixes
    reverse_pat_list = []
    for i in range(len(pat) - 1, -1, -1):
        reverse_pat_list.append(pat[i])
    reverse_pat = "".join(reverse_pat_list)
    z_suffix_reverse = z_calculator(reverse_pat)
    z_suffix = []
    for i in range(len(z_suffix_reverse)-1, -1, -1):
        z_suffix.append(z_suffix_reverse[i])
    z_values = z_calculator(pat)

    # Finds good suffixes
    # -1 is used for when there is no good suffix. 0 is not used because 0 is an index
    good_suffix = [-1 for _ in range(len(pat)+1)]
    for i in range(len(pat)-1):
        j = len(pat) - z_suffix[i]
        good_suffix[j] = i

    # Matched prefixes are also preprocessed
    matched_prefix = [0 for _ in range(len(pat)+1)]
    curr_max_mp = z_values[len(pat)-1]
    for i in range(len(z_values)-1, -1, -1):
        if z_values[i] > curr_max_mp:
            curr_max_mp = z_values[i]
        matched_prefix[i] = curr_max_mp
    matched_prefix[0] = len(pat)

    res = []
    galil_start = -10
    galil_stop = -10
    comparison_count = 0
    curr_index = len(pat)-1
    while curr_index < len(txt):
        mismatch_check = False
        i = 0
        k = len(pat) - 1 - i
        while i < len(pat):

            # Applies galil skip
            galil_skip = 0
            if len(pat) - 1 - i == galil_stop:
                while len(pat) - 1 - (i + galil_skip) >= galil_start:
                    galil_skip += 1
                i += galil_skip
            if i == len(pat):
                continue

            # If a mismatch, breaks out of loop otherwise iterates i if there is a match
            comparison_count += 1
            if pat[len(pat)-1 - i] != txt[curr_index - i]:
                mismatch_check = True
                mismatch_char = txt[curr_index - i]
                break
            i += 1

        # If there has been a mismatch
        if mismatch_check:

            # good suffix
            # Case 1a
            if good_suffix[len(pat) - i] > -1:
                good_suffix_shift = len(pat) - good_suffix[len(pat) - i] - 1

                # Galil_start is -1 from the usual algorithm which is the optimisaiton
                galil_start = good_suffix[len(pat) - i] - (len(pat)-1) + (len(pat) - 1 - i) + 1 - 1
                galil_stop = good_suffix[len(pat) - i]


            # Case 1b using matched prefix
            else:
                good_suffix_shift = len(pat) - matched_prefix[len(pat) - i]
                galil_start = 0
                galil_stop = matched_prefix[len(pat) - i] - 1

        # Case 2 when pat matches txt
        elif not mismatch_check:
            res.append(curr_index - i + 1)
            good_suffix_shift = len(pat) - matched_prefix[1]
            galil_start = 0
            galil_stop = matched_prefix[1] - 1

        # Accounts for edge case when prefix matches all of suffix (so avoids matched prefix) but with the galil
        # optimisation, galil_start is -1 which is not an index
        if galil_start < 0:
            galil_start = 0

        # Applies the skip
        curr_index += good_suffix_shift

    # Saves start of matching txt index to output_binary_boyermoore
    f = open("output_binary_boyermoore.txt", "w")
    for match in res:
        f.write(str(match) + "\n")
    f.close()
    # Prints all comparison counts to terminal
    print(comparison_count)
    return

# Z algorithm based on the FIT3155 Lectures
def z_calculator(zString):
    z_values = [0 for _ in range(len(zString))]
    z_values[1] = naive_comparison(zString, 1, 0)
    if z_values[1] > 0:
        r = z_values[1]
        l = 1
    else:
        r = 0
        l = 0
    for k in range(2, len(zString)):
        if k > r:
            z_values[k] = naive_comparison(zString, k, 0)
            if z_values[k] > 0:
                r = z_values[k] + k - 1
                l = k
        elif k <= r:
            if z_values[k - l] < (r - k + 1):
                z_values[k] = z_values[k - l]
            elif z_values[k - l] >= r - k + 1:
                q = naive_comparison(zString, r + 1, r - k + 1)
                z_values[k] = q
                r = q + k - 1
                l = k
    return z_values

def naive_comparison(zString, zString_index, pat_index):
    while zString[pat_index] != "$" and zString_index < len(zString):
        if zString[pat_index] != zString[zString_index]:
            break
        else:
            pat_index += 1
            zString_index += 1
    return pat_index

# Algorithm based on FIT3155 Lecture
def readFile(txtFilename, patFilename):
    patFile = open(patFileName, "r")
    pat = patFile.read()
    patFile.close()
    txtFile = open(txtFileName, "r")
    txt = txtFile.read()
    txtFile.close()
    return txt, pat

# Following based on FIT3155 Lecture
if __name__ == "__main__":
    txtFileName = sys.argv[1]
    patFileName = sys.argv[2]
    txt, pat = readFile(txtFileName, patFileName)
    binary_boyermoore(txt, pat)