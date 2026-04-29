import { useState } from "react";

export default function ChatInput({ onSubmit, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim() || loading) return;
    onSubmit(value.trim());
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t border-gray-800">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Describe your property dispute... e.g. 'I paid full amount but builder delayed possession'"
        className="flex-1 bg-gray-800 text-gray-100 rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-500"
        disabled={loading}
        aria-label="Legal query input"
      />
      <button
        type="submit"
        disabled={loading || !value.trim()}
        className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white px-5 py-3 rounded-lg text-sm font-medium transition-colors"
        aria-label="Submit query"
      >
        {loading ? "Analysing..." : "Ask Justicia"}
      </button>
    </form>
  );
}
