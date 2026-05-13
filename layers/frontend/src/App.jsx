import { useState } from "react";
import TokenizerPanel from "./TokenizerPanel";

const API = 'http://localhost:8000';

export default function App(){
    const [corpus, setCorpus] = useState('the cat sat on the mat');
    const [vocabSize, setVocabSize] = useState(280);
    const [trained, setTrained] = useState(false);
    const [input, setInput] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    async function handleTrain() {
      setLoading(true);
      await fetch(`${API}/train`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: corpus, vocab_size: vocabSize }),
      });
      setTrained(true);
      setLoading(false);
    }
   
    async function handleEncode() {
      setLoading(true);
      const res = await fetch(`${API}/encode`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      setResult(await res.json());
      setLoading(false);
    }
  return (
    <div style={{ maxWidth: 760, margin: "0 auto", padding: "2rem 1rem", fontFamily: "monospace" }}>
      <h1 style={{ fontSize: 22, fontWeight: 500, marginBottom: "2rem" }}>BPE tokenizer explorer</h1>
 
      {/* --- train section --- */}
      <section style={{ marginBottom: "2rem" }}>
        <label style={label}>training corpus</label>
        <textarea
          rows={3}
          value={corpus}
          onChange={e => setCorpus(e.target.value)}
          style={{ ...field, resize: "vertical" }}
        />
 
        <div style={{ display: "flex", alignItems: "center", gap: 12, margin: "10px 0" }}>
          <label style={label}>vocab size</label>
          <input
            type="range" min={260} max={500} value={vocabSize}
            onChange={e => setVocabSize(Number(e.target.value))}
            style={{ flex: 1 }}
          />
          <span style={{ fontSize: 13, minWidth: 32 }}>{vocabSize}</span>
        </div>
 
        <button onClick={handleTrain} disabled={loading} style={btn}>
          {loading && !trained ? "training…" : "train"}
        </button>
      </section>
 
      {/* --- encode section (only after training) --- */}
      {trained && (
        <section style={{ marginBottom: "2rem" }}>
          <label style={label}>text to tokenize</label>
          <div style={{ display: "flex", gap: 8 }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="type something…"
              style={{ ...field, flex: 1 }}
            />
            <button onClick={handleEncode} disabled={loading} style={btn}>
              {loading ? "…" : "tokenize"}
            </button>
          </div>
        </section>
      )}
 
      {/* --- results (only after encoding) --- */}
      {result && (
        <>
          <TokenizerPanel result={result} />
          <MergeReplay steps={result.steps} />
        </>
      )}
    </div>
  );
}

// shared micro-styles
const label = { display: "block", fontSize: 11, color: "gray", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" };
const field  = { width: "100%", padding: "8px 10px", fontSize: 13, fontFamily: "monospace", boxSizing: "border-box", marginBottom: 8 };
const btn    = { padding: "7px 18px", fontSize: 13, fontFamily: "monospace", cursor: "pointer" };
