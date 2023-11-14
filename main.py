import difflib
import re

def tokenize(s):
    return re.split(r'\s+', s)

def untokenize(ts):
    return ' '.join(ts)

def equalize(s1, s2):
    l1 = tokenize(s1)
    l2 = tokenize(s2)
    res1 = []
    res2 = []
    prev = difflib.Match(0, 0, 0)
    # Iterate through matching blocks using SequenceMatcher
    for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
        # Check for unmatched tokens between the previous and current match in the first sequence (l1)
        if prev.a + prev.size != match.a:
            # Add placeholder tokens for unmatched tokens in the second sequence (res2)
            for i in range(prev.a + prev.size, match.a):
                res2 += ['_' * len(l1[i])]
            res1 += l1[prev.a + prev.size:match.a]
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                res1 += ['_' * len(l2[i])]
            res2 += l2[prev.b + prev.size:match.b]
        res1 += l1[match.a:match.a + match.size]
        res2 += l2[match.b:match.b + match.size]
        prev = match #updating for the next iteration
    return untokenize(res1), untokenize(res2)

def insert_newlines(string, every=64, window=10):
    result = []
    from_string = string
    while len(from_string) > 0:
        cut_off = every
        if len(from_string) > every:
            while from_string[cut_off - 1] != ' ' and cut_off > every - window:
                cut_off -= 1
        else:
            cut_off = len(from_string)
        part = from_string[:cut_off]
        result += [part]
        from_string = from_string[cut_off:]
    return result

def show_comparison(s1, s2, width=40, margin=10, sidebyside=True, compact=False):
    s1, s2 = equalize(s1, s2)

    if sidebyside:
        s1 = insert_newlines(s1, width, margin)
        s2 = insert_newlines(s2, width, margin)
        if compact:
            for i in range(0, len(s1)):
                lft = re.sub(' +', ' ', s1[i].replace('_', '')).ljust(width)
                rgt = re.sub(' +', ' ', s2[i].replace('_', '')).ljust(width)
                print(f"{lft} | {rgt} | ")
        else:
            for i in range(0, len(s1)):
                lft = s1[i].ljust(width)
                rgt = s2[i].ljust(width)
                print(f"{lft} | {rgt} | ")
    else:
        print(s1)
        print(s2)

# Accept user inputs for the two texts
text1 = input("Enter the first text: ")
text2 = input("Enter the second text: ")

# Example usage:
show_comparison(text1, text2)
