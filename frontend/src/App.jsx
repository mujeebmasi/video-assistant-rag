import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function cleanResultText(text) {
  return String(text || "")
    .split("\n")
    .map((line) => line.replace(/\*/g, "").trimEnd())
    .join("\n")
    .trim();
}

function App() {
  const [sourceType, setSourceType] = useState("url");
  const [sourceValue, setSourceValue] = useState("");
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    setAnalysis(null);
    setMessages([]);
    setSessionId("");

    try {
      const formData = new FormData();
      formData.append("source_type", sourceType);

      if (sourceType === "upload") {
        if (!file) {
          throw new Error("Choose a file first.");
        }
        formData.append("file", file);
      } else {
        if (!sourceValue.trim()) {
          throw new Error("Enter a URL or local file path first.");
        }
        formData.append("source_value", sourceValue.trim());
      }

      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setAnalysis(data);
      setSessionId(data.session_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleChat(event) {
    event.preventDefault();
    if (!question.trim() || !sessionId) {
      return;
    }

    const userQuestion = question.trim();
    setQuestion("");
    setChatLoading(true);
    setMessages((current) => [...current, { role: "user", content: userQuestion }]);

    try {
      const response = await fetch(`${API_BASE}/chat/${sessionId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed.");
      }

      setMessages((current) => [...current, { role: "assistant", content: data.answer }]);
    } catch (err) {
      setMessages((current) => [...current, { role: "assistant", content: `Error: ${err.message}` }]);
    } finally {
      setChatLoading(false);
    }
  }

  function handleReset() {
    setSourceValue("");
    setFile(null);
    setAnalysis(null);
    setSessionId("");
    setMessages([]);
    setQuestion("");
    setError("");
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">React frontend + FastAPI backend</p>
          <h1>AI Meeting Assistant</h1>
          <p className="hero-copy">
            Upload a file, paste a link, or point to a local path. The backend will transcribe it,
            summarize it, extract tasks, and let you chat with the result.
          </p>
        </div>
      </header>

      <main className="workspace-grid">
        <div className="left-column">
          <section className="card source-card">
          <div className="card-header">
            <h2>Source</h2>
            <button type="button" className="secondary" onClick={handleReset}>
              Reset
            </button>
          </div>

          <form onSubmit={handleAnalyze} className="form-stack">
            <label className="field">
              <span>Source type</span>
              <select value={sourceType} onChange={(event) => setSourceType(event.target.value)}>
                <option value="url">YouTube URL</option>
                <option value="upload">Upload file</option>
                <option value="local">Local file path</option>
              </select>
            </label>

            {sourceType === "upload" ? (
              <label className="field">
                <span>Audio or video file</span>
                <input
                  type="file"
                  accept=".mp3,.wav,.m4a,.mp4,.webm,.mov,.ogg,.flac"
                  onChange={(event) => setFile(event.target.files?.[0] || null)}
                />
              </label>
            ) : (
              <label className="field">
                <span>{sourceType === "url" ? "YouTube URL" : "Local file path"}</span>
                <input
                  type="text"
                  value={sourceValue}
                  onChange={(event) => setSourceValue(event.target.value)}
                  placeholder={
                    sourceType === "url"
                      ? "https://www.youtube.com/watch?v=..."
                      : "D:\\path\\to\\meeting.mp4"
                  }
                />
              </label>
            )}

            <button type="submit" className="primary" disabled={loading}>
              {loading ? "Analyzing..." : "Run analysis"}
            </button>

            {error ? <div className="error-box">{error}</div> : null}
          </form>
          </section>

          <section className="card chat-card">
            <div className="card-header">
              <h2>Chat</h2>
              <span className="status-pill">{sessionId ? "Connected" : "No session"}</span>
            </div>

            <div className="chat-log">
              {messages.length ? (
                messages.map((message, index) => (
                  <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
                    <strong>{message.role === "user" ? "You" : "AI"}</strong>
                    <p>{message.content}</p>
                  </div>
                ))
              ) : (
                <p className="muted">Ask a question after running the analysis.</p>
              )}
            </div>

            <form onSubmit={handleChat} className="chat-form">
              <input
                type="text"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask something about the meeting..."
                disabled={!sessionId || chatLoading}
              />
              <button type="submit" className="primary" disabled={!sessionId || chatLoading}>
                {chatLoading ? "Sending..." : "Ask"}
              </button>
            </form>
          </section>
        </div>

        <section className="card results-card">
          <div className="card-header">
            <h2>Results</h2>
            <span className="status-pill">{analysis ? "Ready" : "Waiting"}</span>
          </div>

          <div className="results-scroll">
            {analysis ? (
              <div className="results-stack">
              <div className="result-block">
                <h3>Title</h3>
                <p>{cleanResultText(analysis.title)}</p>
              </div>
              <div className="result-block">
                <h3>Summary</h3>
                <p className="pre-wrap">{cleanResultText(analysis.summary)}</p>
              </div>
              <div className="result-block">
                <h3>Actionable Items</h3>
                <p className="pre-wrap">{cleanResultText(analysis.actionable_items)}</p>
              </div>
              <div className="result-block">
                <h3>Decisions</h3>
                <p className="pre-wrap">{cleanResultText(analysis.decisions)}</p>
              </div>
              <div className="result-block">
                <h3>Questions</h3>
                <p className="pre-wrap">{cleanResultText(analysis.questions)}</p>
              </div>
              <div className="result-block">
                <h3>Transcript preview</h3>
                <pre className="transcript-box">{cleanResultText(analysis.transcript)}</pre>
              </div>
              </div>
            ) : (
              <p className="muted">Run an analysis to see the transcript and AI output here.</p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
