from fastapi import FastAPI 
from tokenizer import BasicTokenizer

api = FastAPI()
tokenizer = BasicTokenizer()

@api.post('/train')
def train(text: str ='hello world', vocab_size: int =280):
    print('tokenizer')
    tokenizer.train(text, vocab_size)

    merges = {
        str(k): v for k,v in tokenizer.merges.items()
    }
    return {
        'merges': merges,
        'length': len(tokenizer.vocab)
        }
@api.post('/encode')
def encode(text: str = 'hello world'):
    if hasattr(tokenizer, 'merges'):
        encoded_ids = tokenizer.encode(text)
        

        return {'encoded ids': encoded_ids}
    else:
        return 'No merges, run train first'

@api.get('/')
def root():
    return {'message': 'API is running!'}
