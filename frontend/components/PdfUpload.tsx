"use client"

import { useState } from "react"

export default function PdfUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState("")

  async function uploadFile() {
    if (!file) return

    setStatus("Uploading & indexing paper...")

    const formData = new FormData()
    formData.append("file", file)

    const res = await fetch("http://127.0.0.1:8000/upload-pdf", {
      method: "POST",
      body: formData
    })

    if (!res.ok) {
      setStatus("Upload failed ❌")
      return
    }

    const data = await res.json()
    setStatus(`Indexed ${data.chunks} chunks ✅`)
  }

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button
        onClick={uploadFile}
        style={{
          marginLeft: 10,
          padding: "6px 12px",
          background: "black",
          color: "white"
        }}
      >
        Upload Paper
      </button>

      {status && <p>{status}</p>}
    </div>
  )
}
