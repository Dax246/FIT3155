
"""
Get rid of bad character rule. Good suffix has a number of situations where it ensures it does not pull a suffix that
mismatches for the same reason. Because this is binary, when it ensures it does not mismatch the same reason, it actually
pulls out the next character that matches with the mismatch (if it matches 0, it will get a 1). This does what
bad character rule does so there's no need for BC. Need to account for the edge case where there are no 1s or 0s but
maybe good suffix already accounts for it

"""

# Bad character rule probably doesn't help much considering that there are so many occurrences of each letter in the
# alphabet.