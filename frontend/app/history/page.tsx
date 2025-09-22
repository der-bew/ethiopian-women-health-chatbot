"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
);

export default function ChatHistory() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      if (!user) {
        // Redirect to login if needed
        return;
      }
      const { data } = await supabase
        .from("conversations")
        .select("id, title, created_at")
        .eq("user_id", user.id)
        .order("created_at", { ascending: false });
      setConversations(data || []);
      setLoading(false);
    };
    fetchHistory();
  }, []);

  if (loading) return <div>Loading history...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Your Chat History</h1>
      <div className="grid gap-4">
        {conversations.map((convo) => (
          <div key={convo.id} className="border p-4 rounded">
            <h2 className="font-semibold">{convo.title}</h2>
            <p className="text-gray-500">
              {new Date(convo.created_at).toLocaleDateString()}
            </p>
            {/* Add "View Chat" button to load messages */}
          </div>
        ))}
      </div>
      {conversations.length === 0 && (
        <p>No chats yet. Start one on the home page!</p>
      )}
    </div>
  );
}
