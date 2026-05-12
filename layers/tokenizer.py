from utils import get_stats, merge_tokens

class BasicTokenizer:
    def __init__(self):
        super().__init__()

    def train(self, text, vocab_size, verbose=False):
        assert vocab_size >= 256
        self.text = text 
        self.vocab_size = vocab_size

        num_merges = vocab_size - 256
        ids = list(text.encode('utf-8'))

        merges= {}
        vocab = {idx: bytes([idx]) for idx in range(256)}


        for i in range(num_merges):
            stats = get_stats(ids)
            if not stats:
                break
            pair = max(stats, key=stats.get)
            #print(pair)
            idx = 256 + i
            #print(f'merging {pair} into a new token {idx}')
            ids = merge_tokens(ids,pair, idx)
            merges[(pair)] = idx
            #print(merges[pair])
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]
            #print(vocab[idx])
        self.merges = merges
        self.vocab = vocab


    def encode(self,text):
        tokens = list(text.encode('utf-8')) # getting the unicode tokens from the input text
        while len(tokens)  >= 2:
            stats = get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float('inf')))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens = merge_tokens(tokens, pair, idx)
        return tokens

    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode('utf-8', errors='replace')
        return text
