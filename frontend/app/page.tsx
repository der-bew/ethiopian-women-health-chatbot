"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";
import AuthForm from "@/components/AuthForm";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
);

export default function Home() {
  const [user, setUser] = useState(null);
  const [showAuth, setShowAuth] = useState(false); // Modal for login without gating chat

  // Auth listener (simplified; full in NavBar)
  // ...

  return (
    <>
      <main className="flex min-h-screen flex-col items-center justify-center p-8">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Welcome to Your Health Companion
        </h1>
        <p className="text-center mb-8 text-gray-600">
          Ask about maternal health, fistula, or cancers—get empathetic,
          accurate advice tailored for you.
        </p>
        <ChatInterface
          userId={user?.id || null}
          onLoginClick={() => setShowAuth(true)}
        />
      </main>
      {showAuth && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-md w-full">
            <AuthForm onClose={() => setShowAuth(false)} />
          </div>
        </div>
      )}
    </>
  );
}
