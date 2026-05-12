import collections
from collections import defaultdict

def get_stats(ids):
    pairs = collections.defaultdict(int)
    for i, id_ in enumerate(ids):
        if i < len(ids) - 1:
            pairs[(id_, ids[i+1])] += 1
    return pairs

def merge_tokens(ids, pair, idx):
    new_ids = []
    i =0

    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1]==pair[1]:
            new_ids.append(idx)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids