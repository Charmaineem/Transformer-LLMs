import gradio as gr
from tokenizer import BasicTokenizer

tokenizer = BasicTokenizer()

COLORS = [
    ("bg:#EEEDFE", "color:#3C3489"),
    ("bg:#E1F5EE", "color:#085041"),
    ("bg:#FAEEDA", "color:#633806"),
    ("bg:#FAECE7", "color:#712B13"),
    ("bg:#EAF3DE", "color:#27500A"),
]

def train(corpus, vocab_size):
    if not corpus.strip():
        return "Please enter a corpus"
    tokenizer.train(corpus, int(vocab_size))
    num_merges = len(tokenizer.merges)
    vocab_len  = len(tokenizer.vocab)
    return f"trained — {num_merges} merges learned, vocab size: {vocab_len}"


def encode(text):
    if not hasattr(tokenizer, "merges") or not tokenizer.merges:
        return "<p style='color:red'>Run Train first</p>", ""

    ids    = tokenizer.encode(text)
    tokens = [tokenizer.vocab[i].decode("utf-8", errors="replace") for i in ids]
    compression = round(len(text.encode("utf-8")) / len(ids), 2)

    # build colored pills
    pills = ""
    for i, (tok, id_) in enumerate(zip(tokens, ids)):
        bg, fg = COLORS[i % len(COLORS)]
        display = tok.replace(" ", "·")
        pills += (
            f"<span style='display:inline-flex;align-items:center;"
            f"background:{bg.split(':')[1]};{fg};"
            f"padding:3px 10px;border-radius:20px;margin:3px;"
            f"font-family:monospace;font-size:13px;font-weight:500' "
            f"title='id: {id_}'>"
            f"{display}"
            f"<span style='font-size:10px;margin-left:6px;opacity:0.5'>{id_}</span>"
            f"</span>"
        )

    stats = (
        f"tokens: {len(ids)}  |  "
        f"unique: {len(set(ids))}  |  "
        f"compression: {compression}x"
    )

    return pills, stats


with gr.Blocks(title="BPE Tokenizer Explorer") as demo:
    gr.Markdown("# BPE Tokenizer Explorer")


    with gr.Tab("Train"):
        corpus_box  = gr.Textbox(label="Training corpus", lines=4,
                                  value="the cat sat on the mat")
        vocab_slider = gr.Slider(minimum=260, maximum=400, step=1,
                                  value=280, label="Vocab size")
        train_btn    = gr.Button("Train")
        train_out    = gr.Textbox(label="Result", interactive=False)

        train_btn.click(fn=train, inputs=[corpus_box, vocab_slider], outputs=train_out)

    with gr.Tab("Encode"):
        input_box  = gr.Textbox(label="Text to tokenize", placeholder="type something…")
        encode_btn = gr.Button("Tokenize")
        stats_out  = gr.Textbox(label="Stats", interactive=False)
        pills_out  = gr.HTML(label="Tokens")

        encode_btn.click(fn=encode, inputs=input_box, outputs=[pills_out, stats_out])

    close_btn = gr.Button('Shutdown server')
    close_btn.click(fn=demo.close)


demo.launch(share=True)

