"use client";

import { useMemo, useState, type ChangeEvent } from "react";
import { Space_Grotesk, Newsreader } from "next/font/google";

const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space" });
const newsreader = Newsreader({ subsets: ["latin"], variable: "--font-news" });

type ChatMessage = {
  id: string;
  role: "assistant" | "user";
  content: string;
};

const initialMessages: ChatMessage[] = [
  {
    id: "m1",
    role: "assistant",
    content:
      "Hi! Drop PDFs or links on the right, and I can answer questions grounded in those sources.",
  },
  {
    id: "m2",
    role: "user",
    content: "Can you summarize the attached paper and list key assumptions?",
  },
];

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <a
        href="/chat"
        className="rounded bg-blue-600 px-6 py-3 text-white"
      >
        Start Chatting →
      </a>
    </main>
  )
}

// export default function Home() {
//   const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);

//   const [draft, setDraft] = useState("");
//   const [linkDraft, setLinkDraft] = useState("");
//   const [links, setLinks] = useState<string[]>([]);
//   const [files, setFiles] = useState<File[]>([]);

//   const canSend = draft.trim().length > 0;
//   const canAddLink = linkDraft.trim().length > 0;

//   const handleSend = () => {
//     if (!canSend) return;
//     const nextMessage: ChatMessage = {
//       id: `m${messages.length + 1}`,
//       role: "user",
//       content: draft.trim(),
//     };
//     setMessages((prev) => [...prev, nextMessage]);
//     setDraft("");
//   };

//   const handleClear = () => {
//     setMessages(initialMessages);
//   };

//   const handleAddLink = () => {
//     if (!canAddLink) return;
//     const normalized = linkDraft.trim();
//     setLinks((prev) => [...prev, normalized]);
//     setLinkDraft("");
//   };

//   const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
//     if (!event.target.files) return;
//     const selected = Array.from(event.target.files);
//     setFiles((prev) => [...prev, ...selected]);
//   };

//   const handleRemoveFile = (index: number) => {
//     setFiles((prev) => prev.filter((_, i) => i !== index));
//   };

//   const handleRemoveLink = (index: number) => {
//     setLinks((prev) => prev.filter((_, i) => i !== index));
//   };

//   const messageCount = useMemo(() => messages.length, [messages]);

//   return (
//     <div
//       className={`${spaceGrotesk.variable} ${newsreader.variable} min-h-screen bg-[radial-gradient(circle_at_top,_#f8f5f0_10%,_#f3e9db_55%,_#e7d6c3_100%)] text-slate-900`}
//     >
//       <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-8">
//         <header className="flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-black/10 bg-white/70 px-6 py-4 shadow-[0_20px_60px_-40px_rgba(15,23,42,0.45)] backdrop-blur">
//           <div>
//             <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-500">
//               ThesisFlow · Sources Chat
//             </p>
//             <h1 className="font-[var(--font-space)] text-2xl sm:text-3xl">
//               Source-grounded chatbot UI
//             </h1>
//           </div>
//           <div className="flex items-center gap-3 rounded-full bg-black px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-white">
//             <span className="h-2 w-2 rounded-full bg-emerald-400" />
//             {messageCount} messages
//           </div>
//         </header>

//         <main className="mt-8 grid flex-1 gap-6 lg:grid-cols-[1.4fr_0.6fr]">
//           <section className="flex h-full flex-col gap-6 rounded-3xl border border-black/10 bg-white/80 p-6 shadow-[0_25px_70px_-45px_rgba(15,23,42,0.4)]">
//             <div className="flex items-center justify-between">
//               <div>
//                 <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
//                   Conversation
//                 </p>
//                 <h2 className="font-[var(--font-space)] text-xl">Chat workspace</h2>
//               </div>
//               <button
//                 className="rounded-full border border-black/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-700 transition hover:border-black/30"
//                 type="button"
//                 onClick={handleClear}
//               >
//                 Clear
//               </button>
//             </div>

//             <div className="flex-1 space-y-4 overflow-y-auto pr-2">
//               {messages.map((message) => (
//                 <div
//                   key={message.id}
//                   className={`flex ${
//                     message.role === "user" ? "justify-end" : "justify-start"
//                   }`}
//                 >
//                   <div
//                     className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 shadow-sm sm:text-base ${
//                       message.role === "user"
//                         ? "bg-slate-900 text-white"
//                         : "bg-white text-slate-800"
//                     }`}
//                   >
//                     <p className="font-[var(--font-news)]">{message.content}</p>
//                   </div>
//                 </div>
//               ))}
//             </div>

//             <div className="space-y-3">
//               <textarea
//                 value={draft}
//                 onChange={(event) => setDraft(event.target.value)}
//                 placeholder="Ask something about your uploaded PDFs or links…"
//                 className="h-24 w-full resize-none rounded-2xl border border-black/10 bg-white px-4 py-3 text-sm font-[var(--font-news)] text-slate-800 shadow-sm focus:border-black/40 focus:outline-none"
//               />
//               <div className="flex flex-wrap items-center justify-between gap-3">
//                 <p className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">
//                   Ready to ask
//                 </p>
//                 <button
//                   type="button"
//                   onClick={handleSend}
//                   disabled={!canSend}
//                   className="rounded-full bg-slate-900 px-6 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
//                 >
//                   Send
//                 </button>
//               </div>
//             </div>
//           </section>

//           <aside className="flex h-full flex-col gap-6 rounded-3xl border border-black/10 bg-white/70 p-6 shadow-[0_25px_70px_-50px_rgba(15,23,42,0.35)]">
//             <div>
//               <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
//                 Sources
//               </p>
//               <h2 className="font-[var(--font-space)] text-xl">Add PDFs & links</h2>
//               <p className="mt-2 text-sm text-slate-600">
//                 Upload the documents or URLs you want the assistant to read. Hook this
//                 up to your backend later.
//               </p>
//             </div>

//             <div className="space-y-3 rounded-2xl border border-dashed border-black/20 bg-white px-4 py-5 text-sm">
//               <label className="flex cursor-pointer flex-col items-center gap-2 rounded-xl border border-black/10 bg-slate-50 px-3 py-4 text-center text-xs font-semibold uppercase tracking-[0.2em] text-slate-600 transition hover:border-black/30">
//                 <span>Click to upload PDFs</span>
//                 <span className="text-[11px] font-normal normal-case text-slate-500">
//                   PDF only · Multiple files allowed
//                 </span>
//                 <input
//                   type="file"
//                   accept="application/pdf"
//                   multiple
//                   onChange={handleFileChange}
//                   className="hidden"
//                 />
//               </label>

//               {files.length === 0 ? (
//                 <p className="text-xs text-slate-500">No PDFs uploaded yet.</p>
//               ) : (
//                 <div className="space-y-2">
//                   {files.map((file, index) => (
//                     <div
//                       key={`${file.name}-${index}`}
//                       className="flex items-center justify-between rounded-xl border border-black/10 bg-white px-3 py-2"
//                     >
//                       <div>
//                         <p className="text-sm font-medium text-slate-800">{file.name}</p>
//                         <p className="text-[11px] text-slate-500">
//                           {(file.size / 1024 / 1024).toFixed(2)} MB
//                         </p>
//                       </div>
//                       <button
//                         type="button"
//                         onClick={() => handleRemoveFile(index)}
//                         className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500 transition hover:text-slate-800"
//                       >
//                         Remove
//                       </button>
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>

//             <div className="space-y-3">
//               <label className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
//                 Add link
//               </label>
//               <div className="flex items-center gap-2">
//                 <input
//                   value={linkDraft}
//                   onChange={(event) => setLinkDraft(event.target.value)}
//                   placeholder="https://example.com/research-paper"
//                   className="h-11 flex-1 rounded-2xl border border-black/10 bg-white px-4 text-sm font-[var(--font-news)] focus:border-black/40 focus:outline-none"
//                 />
//                 <button
//                   type="button"
//                   onClick={handleAddLink}
//                   disabled={!canAddLink}
//                   className="h-11 rounded-2xl bg-slate-900 px-4 text-xs font-semibold uppercase tracking-[0.3em] text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
//                 >
//                   Add
//                 </button>
//               </div>

//               {links.length === 0 ? (
//                 <p className="text-xs text-slate-500">No links added yet.</p>
//               ) : (
//                 <div className="space-y-2">
//                   {links.map((link, index) => (
//                     <div
//                       key={`${link}-${index}`}
//                       className="flex items-center justify-between gap-3 rounded-xl border border-black/10 bg-white px-3 py-2"
//                     >
//                       <span className="truncate text-sm text-slate-700">{link}</span>
//                       <button
//                         type="button"
//                         onClick={() => handleRemoveLink(index)}
//                         className="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500 transition hover:text-slate-800"
//                       >
//                         Remove
//                       </button>
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>

//             <div className="mt-auto rounded-2xl border border-black/10 bg-slate-50 px-4 py-4 text-xs text-slate-600">
//               <p className="font-semibold uppercase tracking-[0.28em] text-slate-500">
//                 Integration note
//               </p>
//               <p className="mt-2 leading-5">
//                 Wire the file and link arrays to your ingestion endpoint. This UI only
//                 captures the inputs for now.
//               </p>
//             </div>
//           </aside>
//         </main>
//       </div>
//     </div>
//   );
// }
