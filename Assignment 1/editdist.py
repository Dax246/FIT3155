

"""
Calculate Z i values and Z suffix values. If len(z box) = len(pattern) then there is a match. For each index
where z box is not long enough, check the character after the z box (if z box is empty it will be that character) and
apply all three edits (insert, delete, substitution). Then use the good suffixes to check the rest of the string to
see if it matches
"""

def editdist(txt, pat):
    zString = pat + "$" + txt
    z_values = z_calculator(zString)
    zSuffixString = txt + "$" + pat
    reverse_string_list = [zSuffixString[i] for i in range(len(zSuffixString)-1, -1, -1)]
    reverse_string = "".join(reverse_string_list)
    z_suffix = z_calculator(reverse_string)
    print("z_suffix", z_suffix)
    print("z_values", z_values)
    res = []
    for i in range(len(pat)+1, len(zString)):
        if z_values[i] == len(pat):
            matchingtxt = []
            for j in range(len(pat)):
                matchingtxt.append(zString[i+j])
            res.append([i, matchingtxt])
        else:

    return res

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
        elif k <= r:
            if z_values[k - l + 1] < (r - k + 1):
                z_values[k] = z_values[k - l + 1]
            elif z_values[k - l + 1] >= r - k + 1:
                q = naive_comparison(zString, r + 1, r - k + 2)
                z_values[k] = q - k
                r = q - 1
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


#editdist("acdef", "abcdef")
print(editdist("aabcdef", "abcd"))