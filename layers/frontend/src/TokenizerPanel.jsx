const COLORS = [
    { bg: "#EEEDFE", text: "#3C3489" },
    { bg: "#E1F5EE", text: "#085041" },
    { bg: "#FAEEDA", text: "#633806" },
    { bg: "#FAECE7", text: "#712B13" },
    { bg: "#EAF3DE", text: "#27500A" },
  ];
  
  export default function TokenizerPanel({ result }) {
    const { tokens, ids, compression } = result;
  
    return (
      <div style={{ marginBottom: "2rem" }}>
  
        {/* stats row */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10, marginBottom: 16 }}>
          {[
            ["tokens", ids.length],
            ["unique", new Set(ids).size],
            ["compression", `${compression}x`],
          ].map(([label, value]) => (
            <div key={label} style={{ background: "#f5f5f5", borderRadius: 8, padding: "10px 14px", textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 500, fontFamily: "monospace" }}>{value}</div>
              <div style={{ fontSize: 11, color: "gray", marginTop: 2, textTransform: "uppercase", letterSpacing: "0.05em" }}>{label}</div>
            </div>
          ))}
        </div>
  
        {/* token pills */}
        <div style={{ lineHeight: 2.6 }}>
          {tokens.map((tok, i) => {
            const c = COLORS[i % COLORS.length];
            return (
              <span
                key={i}
                title={`id: ${ids[i]}`}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  background: c.bg,
                  color: c.text,
                  padding: "3px 10px",
                  borderRadius: 20,
                  margin: 3,
                  fontFamily: "monospace",
                  fontSize: 13,
                  fontWeight: 500,
                  cursor: "default",
                }}
              >
                {tok.replace(/ /g, "·")}
                <span style={{ fontSize: 10, marginLeft: 6, opacity: 0.5 }}>{ids[i]}</span>
              </span>
            );
          })}
        </div>
  
      </div>
    );
  }