import { useState, useRef, useEffect } from "react";
import { sendQuery } from "./api";
import ChatInput from "./components/ChatInput";
import ResultPanel from "./components/ResultPanel";

const SUGGESTIONS = [
  { label: "Family Law", text: "My husband refuses to pay maintenance after separation. What can I do?", icon: "👨‍👩‍👧" },
  { label: "Domestic Violence", text: "My husband and in-laws are demanding dowry and harassing me. How do I get protection?", icon: "🛡️" },
  { label: "Consumer", text: "I bought a phone 2 months ago, it's defective and the company refuses to replace it.", icon: "📱" },
  { label: "Cheque Bounce", text: "My friend gave me a cheque for ₹2 lakhs but it bounced. How do I recover the money?", icon: "🏦" },
  { label: "Property/RERA", text: "I paid full amount but builder delayed possession by 2 years in Maharashtra.", icon: "🏠" },
  { label: "Employment", text: "My employer terminated me without notice after 5 years of service. What are my rights?", icon: "💼" },
  { label: "Cyber Crime", text: "I was cheated in a UPI fraud and lost ₹45,000. How do I recover it?", icon: "💻" },
  { label: "Criminal", text: "The police are refusing to register my FIR for a robbery. What should I do?", icon: "⚖️" },
];

const CATEGORY_COLORS = {
  "Family Law": "bg-pink-900/40 text-pink-300 border-pink-700",
  "Dowry & Domestic Violence": "bg-red-900/40 text-red-300 border-red-700",
  "Consumer Complaints": "bg-blue-900/40 text-blue-300 border-blue-700",
  "Financial Disputes": "bg-yellow-900/40 text-yellow-300 border-yellow-700",
  "Property & RERA Issues": "bg-indigo-900/40 text-indigo-300 border-indigo-700",
  "Employment Disputes": "bg-orange-900/40 text-orange-300 border-orange-700",
  "Cyber Complaints": "bg-cyan-900/40 text-cyan-300 border-cyan-700",
  "General Criminal Issues": "bg-purple-900/40 text-purple-300 border-purple-700",
  "Small Civil Disputes": "bg-teal-900/40 text-teal-300 border-teal-700",
  "General Legal Advice": "bg-gray-800 text-gray-300 border-gray-600",
};

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
        { type: "error", text: "Failed to connect to Justicia API. Please ensure the backend is running on port 8000." }
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
          <p className="text-gray-500 text-xs">AI Legal Assistant — Indian Law · All Categories</p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span className="text-xs text-gray-500">Online</span>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center min-h-full text-center px-4 py-8">
            <div className="w-16 h-16 bg-indigo-900/50 rounded-2xl flex items-center justify-center mb-4">
              <span className="text-3xl">⚖️</span>
            </div>
            <h2 className="text-white font-semibold text-lg mb-1">Welcome to Justicia</h2>
            <p className="text-gray-500 text-sm max-w-lg mb-6">
              Describe your legal problem in plain language. I'll identify the applicable Indian laws,
              relevant case precedents, and give you a step-by-step legal strategy.
            </p>

            {/* Category pills */}
            <div className="flex flex-wrap justify-center gap-2 mb-6 max-w-xl">
              {Object.entries(CATEGORY_COLORS).map(([cat, cls]) => (
                <span key={cat} className={`text-xs px-2 py-1 rounded-full border ${cls}`}>{cat}</span>
              ))}
            </div>

            {/* Suggestion grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-2xl">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s.text}
                  onClick={() => handleSubmit(s.text)}
                  className="text-left bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-500 px-4 py-3 rounded-xl transition-colors group"
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-base">{s.icon}</span>
                    <span className="text-xs text-gray-400 group-hover:text-gray-300">{s.label}</span>
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed">{s.text}</p>
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
            {msg.type === "result" && (
              <ResultPanel result={msg.data} categoryColors={CATEGORY_COLORS} />
            )}
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
                <div key={i} className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                  style={{ animationDelay: `${i * 0.15}s` }} />
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
