from fastapi import FastAPI 
from tokenizer import BasicTokenizer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

api = FastAPI()
tokenizer = BasicTokenizer()

class TrainRequest(BaseModel):
    text: str = 'hello world'
    vocab_size: int = 280

class EncodeRequest(BaseModel):
    text: str = 'hello world'


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post('/train')
def train(request: TrainRequest):
    text = request.text
    vocab_size = request.vocab_size
    print(f'training tokenizer with text: {text} and vocab size: {vocab_size}')
    tokenizer.train(text, vocab_size)

    merges = {
        str(k): v for k,v in tokenizer.merges.items()
    }
    return {
        'merges': merges,
        'length': len(tokenizer.vocab),
        'message': 'Tokenization training successful!'
        }

@api.post('/encode')
def encode(request: EncodeRequest):
    text = request.text
    print(f'encoding text: {text}')
    if hasattr(tokenizer, 'merges'):
        encoded_ids = tokenizer.encode(text)
        decoded_text = tokenizer.decode(encoded_ids)

        return {
            'encoded ids': encoded_ids, 
            'decoded text': decoded_text, 
            'message': 'Tokenization encoding successful!'
            }
    else:
        return {'message': 'No merges, run train first'}

@api.get('/')
def root():
    return {'message': 'API is running!'}
