import React, { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User as UserIcon } from "lucide-react";
import axios from "axios";


/**
 * Minimal Chat UI
 * ------------------------------------------------------
 * A single-file React + TypeScript component that renders
 * a clean, responsive chat interface suitable for a chatbot.
 * - Tailwind CSS classes for styling
 * - Framer Motion for subtle animations
 * - Keyboard UX: Enter=send, Shift+Enter=newline
 * - Auto-scroll to newest message
 * - Simple mocked assistant reply (replace with real API call)
 *
 * Drop this into App.tsx (or any route file). Ensure Tailwind is set up.
 */

type Role = "user" | "assistant";

type Message = {
  id: string;
  role: Role;
  content: string;
  createdAt: number; // epoch ms
};

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

function formatTime(ts: number) {
  return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function useAutoscroll(deps: any[]) {
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return ref;
}

const bubbleVariants = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
};

function Avatar({ role }: { role: Role }) {
  const Icon = role === "assistant" ? Bot : UserIcon;
  return (
    <div className={`flex items-center justify-center h-8 w-8 rounded-full shadow ${role === "assistant" ? "bg-blue-100" : "bg-emerald-100"}`}>
      <Icon className="h-4 w-4" />
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  return (
    <motion.div
      variants={bubbleVariants}
      initial="initial"
      animate="animate"
      className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
    >
      {!isUser && <Avatar role={msg.role} />}
      <div className={`max-w-[80%] rounded-2xl px-4 py-2 shadow-sm ring-1 ${
        isUser
          ? "bg-emerald-600 text-white ring-emerald-700"
          : "bg-white text-slate-900 ring-slate-200"
      }`}
      >
        <div className="whitespace-pre-wrap leading-relaxed text-sm">{msg.content}</div>
        <div className={`mt-1 text-[10px] ${isUser ? "text-emerald-100" : "text-slate-500"}`}>{formatTime(msg.createdAt)}</div>
      </div>
      {isUser && <Avatar role={msg.role} />}
    </motion.div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-slate-500">
      <div className="h-2 w-2 rounded-full bg-slate-400 animate-pulse" />
      <div className="h-2 w-2 rounded-full bg-slate-400 animate-pulse [animation-delay:120ms]" />
      <div className="h-2 w-2 rounded-full bg-slate-400 animate-pulse [animation-delay:240ms]" />
    </div>
  );
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([{
    id: uid(),
    role: "assistant",
    content: "Hi! I’m your AI assistant. Ask me anything.",
    createdAt: Date.now(),
  }]);
  const [input, setInput] = useState("");
  const [isReplying, setIsReplying] = useState(false);

  const scrollRef = useAutoscroll([messages.length, isReplying]);

  // Derived: placeholder dynamic text
  const placeholder = useMemo(() =>
    isReplying ? "Assistant is thinking..." : "Type a message…",
  [isReplying]);

  function pushMessage(role: Role, content: string) {
    setMessages((prev) => [...prev, { id: uid(), role, content, createdAt: Date.now() }]);
  }

  async function mockAssistantReply(userText: string) {
    setIsReplying(true);
    // Simulate latency
    await new Promise((r) => setTimeout(r, 400));
    // Very simple echo-style response. Replace with your API call.
    // const reply = `You said: "${userText.trim()}".\n(Replace this with your model’s response.)`;
    const reply = await axios.post('http://localhost:5050/recommendation', { question: userText }).then(res => res.data);
    console.log(reply.answer);
    pushMessage("assistant", reply.answer);
    setIsReplying(false);
  }

  async function handleSend() {
    const text = input.trim();
    if (!text || isReplying) return;
    pushMessage("user", text);
    setInput("");
    mockAssistantReply(text);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-slate-50 to-slate-100 text-slate-900 flex items-center justify-center p-4">
      <div className="mx-auto w-full max-w-3xl grid grid-rows-[auto,1fr,auto] rounded-2xl border border-slate-200 bg-white shadow-xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between gap-3 px-5 py-4 bg-white/70 backdrop-blur border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-2xl bg-blue-100 grid place-items-center shadow">
              <Bot className="h-4 w-4" />
            </div>
            <div>
              <h1 className="text-base font-semibold">Chatbot</h1>
              <p className="text-xs text-slate-500">Book Recommender</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div ref={scrollRef} className="overflow-y-auto px-4 py-4 md:px-6 md:py-6 bg-slate-50/50">
          <div className="flex flex-col gap-4">
            <AnimatePresence initial={false}>
              {messages.map((m) => (
                <MessageBubble key={m.id} msg={m} />
              ))}
            </AnimatePresence>
            {isReplying && (
              <div className="flex items-center gap-3 text-sm text-slate-500">
                <Avatar role="assistant" />
                <div className="rounded-2xl px-4 py-2 bg-white ring-1 ring-slate-200 shadow-sm">
                  <TypingIndicator />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Composer */}
        <div className="border-t border-slate-200 bg-white p-3">
          <div className="flex items-end gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm focus-within:ring-2 focus-within:ring-emerald-500/30">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              rows={1}
              className="min-h-[44px] max-h-40 w-full resize-y rounded-xl bg-white px-3 py-2 outline-none placeholder:text-slate-400"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isReplying}
              className="inline-flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium shadow-sm transition active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed bg-emerald-600 text-white hover:bg-emerald-600/90"
              aria-label="Send message"
            >
              <Send className="h-4 w-4" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </div>
          <p className="mt-2 text-[11px] text-slate-500">Press <kbd className="rounded border border-slate-300 bg-slate-50 px-1">Enter</kbd> to send • <kbd className="rounded border border-slate-300 bg-slate-50 px-1">Shift</kbd>+<kbd className="rounded border border-slate-300 bg-slate-50 px-1">Enter</kbd> for a new line</p>
        </div>
      </div>
    </div>
  );
}
