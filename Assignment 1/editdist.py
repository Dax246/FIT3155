

""" Description of method used to solve question 1, editdist, of the assignment.

The standard Gusfield's Z algorithm was used to determine Z values and Z suffixes. This was used in a standard pattern
matching algorithm using Z values. The difference is that normal Z values are used to determine how much of the pat
matches the txt. If the whole pattern does not match, the algorithm attempts to insert, substitute and delete the
mismatch part of the txt. Then the algorithm will use the Z suffixes to determine if the rest of the pattern matches
the relevant part of the txt.

Calculating Z values and Z suffixes is O(m+n) time in the preprocessing stage where m is len(pat) and n is len(txt).
Then the algorithm will run through  each part of the txt and do O(1) work for each character which is overall O(n)
work.

"""
from copy import deepcopy
import sys

def editdist(txt, pat):

    # Z Value preprocessing
    zString = pat + "$" + txt
    z_values = z_calculator(zString)

    # Z suffix value preprocessing
    zSuffixString = txt + "$" + pat
    reverse_string_list = [zSuffixString[i] for i in range(len(zSuffixString)-1, -1, -1)]
    reverse_string = "".join(reverse_string_list)

    # z_suffix_in_wrong_order puts the z value at the end of the matched substring. We want at front of the matched
    # substring
    z_suffix_in_wrong_order = z_calculator(reverse_string)
    z_suffix = []
    for i in range(len(pat)-1, -1, -1):
        z_suffix.append(z_suffix_in_wrong_order[i])
    z_suffix.append(0)
    index = len(zString) - 1
    for i in range(len(txt)):
        z_suffix.append(z_suffix_in_wrong_order[index])
        index -= 1

    z_suffix_correct = deepcopy(z_suffix)
    for i in range(len(z_suffix)):
        x = z_suffix[i]
        if x > 0:
            z_suffix_correct[i-x+1] = x
            if x != 1:
                z_suffix_correct[i] = 0


    res = []
    for i in range(len(pat)+1, len(zString)):

        # If the pat matches the txt perfectly
        if z_values[i] == len(pat):
            matchingtxt = []
            for j in range(len(pat)):
                matchingtxt.append(zString[i+j])
            res.append([i - len(pat) - 1, 0])
        else:


            mismatch_txt_index = i + z_values[i]

            # insert when at end of txt
            if mismatch_txt_index == len(zString):
                if z_values[i] == len(pat) - 1:
                    matchingtxt = []
                    for j in range(len(pat) - 1):
                        matchingtxt.append(zString[i + j])
                    res.append([i - len(pat) - 1, 1])

            # insert edit
            elif z_suffix_correct[mismatch_txt_index] == len(pat) - z_values[i] - 1:
                matchingtxt = []
                for j in range(len(pat) - 1):
                    matchingtxt.append(zString[i + j])
                res.append([i - len(pat) - 1, 1])

            # delete edit
            elif z_suffix_correct[mismatch_txt_index] == len(pat) - z_values[i]:
                matchingtxt = []
                for j in range(len(pat) - 1):
                    matchingtxt.append(zString[i + j])
                res.append([i - len(pat) - 1, 1])

            # substitution edit

            # This is if substitution occurs at the end of the txt
            elif mismatch_txt_index == len(zString):
                if z_values[i] == len(pat) - 1:
                    matchingtxt = []
                    for j in range(len(pat)):
                        matchingtxt.append(zString[i + j])
                    res.append([i - len(pat) - 1, 1])

            # Normal substitution
            elif mismatch_txt_index + 1 < len(zString):
                if z_suffix_correct[mismatch_txt_index+1] == len(pat) - z_values[i] - 1:
                    matchingtxt = []
                    for j in range(len(pat) - 1):
                        matchingtxt.append(zString[i + j])
                    res.append([i - len(pat) - 1, 1])

    # Save results to output_editdist.txt
    f = open("output_editdist.txt", "w")
    for match in res:
        f.write(str(match[0]) + " " + str(match[1]) + "\n")
    f.close()
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
    return pat, txt

# Following based on FIT3155 Lecture
if __name__ == "__main__":
    txtFileName = sys.argv[1]
    patFileName = sys.argv[2]
    pat, txt = readFile(txtFileName, patFileName)
    editdist(txt, pat)