import { useState, useRef, useEffect } from "react";
import { sendQuery } from "./api";
import ChatInput from "./components/ChatInput";
import ResultPanel from "./components/ResultPanel";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (query) => {
    setMessages((prev) => [...prev, { type: "user", text: query }]);
    setLoading(true);
    try {
      const result = await sendQuery(query, sessionId);
      if (!sessionId) setSessionId(result.session_id);
      setMessages((prev) => [...prev, { type: "result", data: result }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "error", text: "Failed to connect to Justicia API. Please ensure the backend is running." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-950">
      {/* Header */}
      <header className="flex items-center gap-3 px-6 py-4 border-b border-gray-800 bg-gray-900">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">J</div>
        <div>
          <h1 className="text-white font-semibold text-sm">Justicia</h1>
          <p className="text-gray-500 text-xs">AI Legal Assistant — RERA Real Estate Disputes</p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          <span className="text-xs text-gray-500">Online</span>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-6">
            <div className="w-16 h-16 bg-indigo-900/50 rounded-2xl flex items-center justify-center mb-4">
              <span className="text-3xl">⚖️</span>
            </div>
            <h2 className="text-white font-semibold text-lg mb-2">Welcome to Justicia</h2>
            <p className="text-gray-500 text-sm max-w-md">
              Describe your real estate dispute and I'll analyse applicable RERA laws,
              detect conflicts, identify missing evidence, and generate a legal strategy.
            </p>
            <div className="mt-6 grid grid-cols-1 gap-2 w-full max-w-md">
              {[
                "I paid full amount but builder delayed possession by 2 years",
                "Builder is not responding to my emails about possession date",
                "I want to file a RERA complaint against my builder in Maharashtra"
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => handleSubmit(suggestion)}
                  className="text-left text-xs text-gray-400 bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-lg transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i}>
            {msg.type === "user" && (
              <div className="flex justify-end px-4 py-3">
                <div className="bg-indigo-600 text-white text-sm px-4 py-2 rounded-2xl rounded-tr-sm max-w-lg">
                  {msg.text}
                </div>
              </div>
            )}
            {msg.type === "result" && <ResultPanel result={msg.data} />}
            {msg.type === "error" && (
              <div className="mx-4 my-3 p-3 bg-red-900/40 border border-red-700 rounded-lg text-red-300 text-sm">
                {msg.text}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 px-6 py-4">
            <div className="flex gap-1">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                  style={{ animationDelay: `${i * 0.15}s` }}
                />
              ))}
            </div>
            <span className="text-xs text-gray-500">Justicia is analysing your case...</span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSubmit={handleSubmit} loading={loading} />
    </div>
  );
}
