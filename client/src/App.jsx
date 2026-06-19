import React, { useState, useRef, useEffect } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [status, setStatus] = useState("idle");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [dragging, setDragging] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const uploadFiles = async (files) => {
    const pdfs = Array.from(files).filter((f) => f.name.endsWith(".pdf"));
    if (pdfs.length === 0) { setUploadError("Please upload PDF files only."); return; }
    setUploadError("");
    setStatus("uploading");
    const formData = new FormData();
    pdfs.forEach((f) => formData.append("files", f));
    try {
      const res = await fetch(`${API}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (data.error) { setUploadError(data.error); setStatus("idle"); return; }
      setUploadedFiles(pdfs.map((f) => f.name));
      setMessages([{ role: "assistant", text: `${pdfs.length === 1 ? pdfs[0].name : `${pdfs.length} PDFs`} loaded — ${data.chunks} chunks indexed. Ask me anything.` }]);
      setStatus("ready");
    } catch (e) {
      setUploadError("Could not reach the server. Is it running?");
      setStatus("idle");
    }
  };

  const handleDrop = (e) => { e.preventDefault(); setDragging(false); uploadFiles(e.dataTransfer.files); };

  const sendMessage = async () => {
    const q = input.trim();
    if (!q || status === "chatting") return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setStatus("chatting");
    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", text: data.answer || data.error || "No answer returned." }]);
    } catch (e) {
      setMessages((prev) => [...prev, { role: "assistant", text: "Server error. Please try again." }]);
    }
    setStatus("ready");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const reset = () => { setStatus("idle"); setUploadedFiles([]); setMessages([]); setInput(""); setUploadError(""); };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <h1 className="logo">PDF<span>Chat</span></h1>
          <p className="tagline">Ask questions about your documents</p>
        </div>

        <div className="sidebar-divider" />

        <div
          className={`upload-zone ${dragging ? "dragging" : ""} ${status === "uploading" ? "uploading" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input ref={fileInputRef} type="file" accept=".pdf" multiple style={{ display: "none" }} onChange={(e) => uploadFiles(e.target.files)} />
          {status === "uploading" ? (
            <div className="upload-inner"><div className="spinner" /><span>Processing...</span></div>
          ) : (
            <div className="upload-inner">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span>{uploadedFiles.length > 0 ? "Upload new PDFs" : "Drop PDFs here"}</span>
              <span className="upload-sub">or click to browse</span>
            </div>
          )}
        </div>

        {uploadError && <p className="upload-error">{uploadError}</p>}

        {uploadedFiles.length > 0 && (
          <div className="files-list">
            {uploadedFiles.map((name) => (
              <div className="file-chip" key={name}>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14 2 14 8 20 8" />
                </svg>
                <span>{name}</span>
              </div>
            ))}
            <button className="reset-btn" onClick={reset}>Clear & start over</button>
          </div>
        )}
      </aside>

      {/* Chat */}
      <main className="chat-area">
        <div className="chat-topbar">
          <div className={`status-dot ${status === "ready" || status === "chatting" ? "ready" : ""}`} />
          <span className="chat-topbar-title">
            {status === "idle" ? "No document loaded" : status === "uploading" ? "Processing..." : uploadedFiles[0]}
          </span>
          {(status === "ready" || status === "chatting") && (
            <span className="chat-topbar-sub">· {status === "chatting" ? "Thinking..." : "Ready"}</span>
          )}
        </div>

        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" strokeLinecap="round" strokeLinejoin="round"/>
                <polyline points="14 2 14 8 20 8" strokeLinecap="round" strokeLinejoin="round"/>
                <line x1="16" y1="13" x2="8" y2="13" strokeLinecap="round"/>
                <line x1="16" y1="17" x2="8" y2="17" strokeLinecap="round"/>
              </svg>
            </div>
            <p>Upload a PDF to get started</p>
          </div>
        ) : (
          <div className="messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                <div className="bubble">{m.text}</div>
              </div>
            ))}
            {status === "chatting" && (
              <div className="message assistant">
                <div className="bubble typing"><span /><span /><span /></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        <div className="input-bar">
          <textarea
            placeholder={status === "ready" || status === "chatting" ? "Ask a question..." : "Upload a PDF first"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={status !== "ready"}
            rows={1}
          />
          <button className="send-btn" onClick={sendMessage} disabled={status !== "ready" || !input.trim()}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;