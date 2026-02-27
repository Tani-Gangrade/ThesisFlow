"use client"

import PdfUpload from "@/components/PdfUpload" 
import { useState } from "react"

export default function ChatPage() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  async function sendMessage() {
    if (!message.trim()) return
  
    // Show user message
    setMessages(prev => [...prev, "You: " + message, "Bot: "])
    setMessage("")
    setLoading(true)
  
    const res = await fetch("http://127.0.0.1:8000/chat-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    })
  
    if (!res.body) return
  
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
  
    let botText = ""
  
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
  
      botText += decoder.decode(value)
  
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = "Bot: " + botText
        return updated
      })
    }
  
    setLoading(false)
  }  

  return (
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      <h1>Chat</h1>
      <PdfUpload />

      <div style={{ minHeight: 200, border: "1px solid #ccc", padding: 10 }}>
        {messages.map((m, i) => (
          <div key={i}>{m}</div>
        ))}
        {loading && <div>Bot is typing...</div>}
      </div>

      <input
        value={message}
        onChange={e => setMessage(e.target.value)}
        placeholder="Type message"
        style={{ width: "100%", marginTop: 10 }}
      />

      <button onClick={sendMessage} style={{ marginTop: 10 }}>
        Send
      </button>
    </div>
  )
}
