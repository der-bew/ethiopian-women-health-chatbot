// frontend/components/ChatInterface.tsx (Updated for Guest Mode)
"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatInterface({
  userId,
  onLoginClick,
}: {
  userId: string | null;
  onLoginClick: () => void;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );

  useEffect(() => {
    if (messages.length > 2 && !userId) {
      setShowLoginPrompt(true); // Prompt after a few messages
    }
  }, [messages, userId]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userMessage = { role: "user" as const, content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const session = await supabase.auth.getSession();
      const token = session.data.session?.access_token;

      // If no user, use backend guest endpoint (add one later) or skip saving
      const body = { message: input, conversation_id: conversationId };
      if (userId) {
        body.conversation_id =
          conversationId || (await createNewConversation(userId));
      }

      const res = await fetch("http://localhost:8000/api/chat", {
        // Update to prod URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) throw new Error("Failed to get response");

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant" as const, content: data.response },
      ]);
      if (userId) setConversationId(data.conversation_id);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant" as const,
          content: "Sorry, something went wrong. Try again?",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const createNewConversation = async (userId: string) => {
    // Stub: Call backend to create convo
    const res = await fetch("http://localhost:8000/api/conversations", {
      // Add this endpoint
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${await getToken()}`,
      },
      body: JSON.stringify({ user_id: userId }),
    });
    const { id } = await res.json();
    return id;
  };

  const getToken = async () =>
    (await supabase.auth.getSession()).data.session?.access_token;

  return (
    <>
      <div className="flex flex-col w-full max-w-2xl h-96 border rounded p-4 bg-white shadow-lg">
        <div className="flex-1 overflow-y-auto mb-4 space-y-2">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <span
                className={`max-w-xs p-3 rounded-lg ${msg.role === "user" ? "bg-blue-100" : "bg-green-100"}`}
              >
                {msg.content}
              </span>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <span className="bg-green-100 p-3 rounded-lg">Thinking...</span>
            </div>
          )}
        </div>
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-3 border rounded-l-lg focus:outline-none"
            placeholder="Ask about your health..."
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-500 text-white p-3 rounded-r-lg hover:bg-blue-600 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
      {showLoginPrompt && !userId && (
        <div className="mt-4 p-4 bg-yellow-100 border rounded text-center">
          <p>Login to save your chat history and get personalized tips!</p>
          <button
            onClick={onLoginClick}
            className="mt-2 bg-yellow-500 text-white px-4 py-2 rounded"
          >
            Login Now
          </button>
        </div>
      )}
    </>
  );
}
