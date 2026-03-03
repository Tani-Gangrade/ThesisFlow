"use client"

import { useState } from "react"
import type { CSSProperties } from "react"
import { API_BASE_URL } from "@/lib/api"

export default function PdfUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState("")
  const [failed, setFailed] = useState(false)

  async function uploadFile() {
    if (!file) return

    setFailed(false)
    setStatus("Uploading & indexing paper...")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(`${API_BASE_URL}/upload-pdf`, {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        setFailed(true)
        setStatus("Upload failed")
        return
      }

      const data = await res.json()
      const count = data.chunks_stored ?? 0
      setStatus(`Indexed ${count} chunks`)
    } catch {
      setFailed(true)
      setStatus("Upload failed")
    }
  }

  const card: CSSProperties = {
    border: "1px solid #d7cec0",
    background: "#fffdf8",
    borderRadius: 16,
    boxShadow: "0 10px 22px rgba(36, 29, 20, 0.08)",
    padding: "1rem",
    minWidth: 0,
  }

  const eyebrow: CSSProperties = {
    fontSize: "0.76rem",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#615646",
    fontWeight: 600,
  }

  const subtitle: CSSProperties = {
    color: "#615646",
    marginTop: "0.4rem",
    fontSize: "0.94rem",
    lineHeight: 1.45,
  }

  const button: CSSProperties = {
    border: 0,
    borderRadius: 10,
    padding: "0.72rem 1rem",
    background: file ? "#0f766e" : "#89b5b0",
    color: "#fff",
    cursor: file ? "pointer" : "not-allowed",
    fontWeight: 600,
  }

  return (
    <div style={card}>
      <div style={eyebrow}>Paper Ingestion</div>
      <h3 style={{ fontSize: "1.1rem", marginTop: "0.35rem", fontWeight: 650 }}>
        Upload a PDF to build context
      </h3>
      <p style={subtitle}>
        MARA will chunk, embed, and index this paper for retrieval.
      </p>
      <input
        style={{ display: "block", width: "100%", marginTop: "0.6rem" }}
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <div style={{ marginTop: "0.72rem", display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <button style={button} onClick={uploadFile} disabled={!file}>
          Upload Paper
        </button>
        <span style={{ color: "#615646", fontSize: "0.82rem" }}>
          {file ? file.name : "No file selected"}
        </span>
      </div>

      {status && (
        <p style={{ marginTop: "0.72rem", color: failed ? "#9f1239" : "#615646", fontSize: "0.9rem" }}>
          {status}
        </p>
      )}
    </div>
  )
}
