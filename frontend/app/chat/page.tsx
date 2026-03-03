"use client"

import PdfUpload from "@/components/PdfUpload" 
import { useEffect, useRef, useState } from "react"
import type { CSSProperties } from "react"
import { API_BASE_URL } from "@/lib/api"

type ChatMessage = {
  role: "user" | "assistant"
  content: string
}

export default function ChatPage() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const listRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight
    }
  }, [messages, loading])

  const page: CSSProperties = {
    minHeight: "100vh",
    background:
      "radial-gradient(circle at 15% 10%, #f5ecdb 0, #f2efe8 38%), radial-gradient(circle at 92% 85%, #dff0ee 0, transparent 34%), #f2efe8",
    color: "#1f1b16",
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
    padding: "2rem 1rem",
  }

  const shell: CSSProperties = {
    maxWidth: 1000,
    margin: "0 auto",
  }

  const title: CSSProperties = {
    marginTop: "0.25rem",
    fontSize: "clamp(1.9rem, 4vw, 2.7rem)",
    lineHeight: 1.1,
    fontWeight: 730,
  }

  const subtitle: CSSProperties = {
    marginTop: "0.5rem",
    color: "#5d5345",
    fontSize: "1.06rem",
  }

  const grid: CSSProperties = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
    gap: "1rem",
    marginTop: "1rem",
  }

  const chatPanel: CSSProperties = {
    border: "1px solid #d7cec0",
    background: "#fffdf8",
    borderRadius: 16,
    boxShadow: "0 12px 28px rgba(36, 29, 20, 0.08)",
    minHeight: 540,
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  }

  const messagesStyle: CSSProperties = {
    flex: 1,
    padding: "1rem",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "0.72rem",
  }

  const composer: CSSProperties = {
    borderTop: "1px solid #e2d9ca",
    padding: "0.8rem",
    display: "flex",
    gap: "0.6rem",
  }

  const input: CSSProperties = {
    flex: 1,
    border: "1px solid #d7cec0",
    borderRadius: 10,
    padding: "0.8rem 0.9rem",
    fontSize: "1rem",
    background: "#fff",
    color: "#1f1b16",
  }

  const button: CSSProperties = {
    border: 0,
    borderRadius: 10,
    padding: "0.75rem 1rem",
    background: loading ? "#89b5b0" : "#0f766e",
    color: "#fff",
    fontWeight: 600,
    cursor: loading ? "not-allowed" : "pointer",
    minWidth: 92,
  }

  const eyebrow: CSSProperties = {
    fontSize: "0.76rem",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#5f5649",
    fontWeight: 700,
  }

  async function sendMessage() {
    if (!message.trim()) return
    const outgoing = message

    setMessages(prev => [
      ...prev,
      { role: "user", content: outgoing },
      { role: "assistant", content: "" },
    ])
    setMessage("")
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE_URL}/chat-stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: outgoing, use_memory: true, use_rag: true }),
      })

      if (!res.ok || !res.body) {
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: "assistant",
            content: "Backend request failed.",
          }
          return updated
        })
        return
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let botText = ""

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        botText += decoder.decode(value)

        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: "assistant",
            content: botText,
          }
          return updated
        })
      }
    } catch {
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: "assistant",
          content: "Could not reach backend.",
        }
        return updated
      })
    } finally {
      setLoading(false)
    }
  }  

  return (
    <main style={page}>
      <div style={shell}>
      <header>
        <div style={eyebrow}>MARA Workspace</div>
        <h1 style={title}>Memory-Augmented Research Agent</h1>
        <p style={subtitle}>
          Upload papers, ask questions, and build persistent research context.
        </p>
      </header>

      <section style={grid}>
        <PdfUpload />

        <div style={chatPanel}>
          <div style={messagesStyle} ref={listRef}>
            {messages.length === 0 && (
              <div style={{ background: "#f7f2e8", border: "1px solid #d7cec0", borderRadius: 14, padding: "0.75rem 0.85rem", maxWidth: "92%" }}>
                <div style={{ fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: "0.35rem", color: "#5f5649", fontWeight: 600 }}>
                  Assistant
                </div>
                Start by uploading one paper, then ask for findings, methods, or limitations.
              </div>
            )}

            {messages.map((m, i) => (
              <article
                key={i}
                style={{
                  background: m.role === "user" ? "#e4f7f4" : "#f7f2e8",
                  border: "1px solid #d7cec0",
                  borderRadius: 14,
                  padding: "0.75rem 0.85rem",
                  maxWidth: "92%",
                  lineHeight: 1.45,
                  alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                }}
              >
                <div style={{ fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: "0.35rem", color: "#5f5649", fontWeight: 600 }}>
                  {m.role === "user" ? "You" : "Assistant"}
                </div>
                {m.content || (loading && m.role === "assistant" ? "Thinking..." : "")}
              </article>
            ))}
          </div>

          <div style={composer}>
            <input
              style={input}
              value={message}
              onChange={e => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading) void sendMessage()
              }}
              placeholder="Ask about methodology, findings, or evidence gaps..."
            />
            <button style={button} onClick={sendMessage} disabled={loading}>
              {loading ? "Sending..." : "Send"}
            </button>
          </div>
        </div>
      </section>
      </div>
    </main>
  )
}
