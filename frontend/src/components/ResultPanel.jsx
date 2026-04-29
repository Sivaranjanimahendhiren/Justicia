export default function ResultPanel({ result }) {
  if (!result) return null;

  if (result.status === "out_of_scope") {
    return (
      <div className="mx-4 my-3 p-4 bg-yellow-900/40 border border-yellow-700 rounded-lg text-yellow-300 text-sm">
        {result.message}
      </div>
    );
  }

  const strategy = result.legal_strategy;

  return (
    <div className="flex flex-col gap-4 p-4">

      {/* Case Summary */}
      <Section title="Case Summary" color="indigo">
        <p className="text-sm text-gray-300">{result.case_summary}</p>
        {result.risk_score !== null && result.risk_score !== undefined && (
          <RiskBadge score={result.risk_score} />
        )}
        {result.case_readiness && (
          <span className={`text-xs px-2 py-1 rounded-full mt-2 inline-block ${
            result.case_readiness === "ready" ? "bg-green-800 text-green-200" :
            result.case_readiness === "needs_attention" ? "bg-yellow-800 text-yellow-200" :
            "bg-red-800 text-red-200"
          }`}>
            Case Readiness: {result.case_readiness.replace("_", " ")}
          </span>
        )}
      </Section>

      {/* Applicable Laws */}
      {strategy?.applicable_acts_sections?.length > 0 && (
        <Section title="Applicable Acts & Sections" color="blue">
          <ul className="space-y-1">
            {strategy.applicable_acts_sections.map((law, i) => (
              <li key={i} className="text-sm text-blue-200 flex gap-2">
                <span className="text-blue-500 mt-0.5">§</span>
                <span>{law}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Detected Conflicts */}
      {result.detected_conflicts?.length > 0 && (
        <Section title="Detected Conflicts" color="red">
          {result.detected_conflicts.map((c, i) => (
            <div key={i} className="mb-3 p-3 bg-red-950/50 rounded-lg border border-red-800">
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-medium text-red-300">{c.field}</span>
                <SeverityBadge severity={c.severity} />
              </div>
              <p className="text-xs text-gray-400">Client said: <span className="text-gray-200">{c.client_value}</span></p>
              <p className="text-xs text-gray-400">Document shows: <span className="text-gray-200">{c.document_value}</span></p>
              <p className="text-xs text-yellow-400 mt-1">→ {c.recommendation}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Missing Evidence */}
      {result.missing_evidence?.length > 0 && (
        <Section title="Missing Evidence" color="orange">
          {result.missing_evidence.map((m, i) => (
            <div key={i} className="mb-2 p-3 bg-orange-950/40 rounded-lg border border-orange-800">
              <p className="text-sm font-medium text-orange-300">{m.document_type}</p>
              <p className="text-xs text-gray-400 mt-1">How to obtain: {m.how_to_obtain}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Judicial Precedents */}
      {result.judicial_precedents?.length > 0 && (
        <Section title="Judicial Precedents" color="purple">
          {result.judicial_precedents.map((p, i) => (
            <div key={i} className="mb-3 p-3 bg-purple-950/40 rounded-lg border border-purple-800">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-purple-300">#{p.rank} {p.case_name}</span>
                <span className="text-xs text-purple-400">Score: {p.relevance_score}</span>
              </div>
              <p className="text-xs text-gray-400 mt-1">{p.applicable_to_current_case}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Legal Strategy */}
      {strategy && (
        <Section title="Legal Strategy" color="green">
          {strategy.legal_grounds?.length > 0 && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Legal Grounds</p>
              <ul className="space-y-1">
                {strategy.legal_grounds.map((g, i) => (
                  <li key={i} className="text-sm text-gray-300 flex gap-2">
                    <span className="text-green-500">✓</span>{g}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {strategy.compensation_calculation && (
            <div className="mb-3 p-3 bg-green-950/40 rounded-lg border border-green-800">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Compensation Estimate</p>
              <p className="text-sm text-green-300">{strategy.compensation_calculation}</p>
            </div>
          )}
          {strategy.recommended_relief && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Recommended Relief</p>
              <p className="text-sm text-gray-300">{strategy.recommended_relief}</p>
            </div>
          )}
          {strategy.immediate_action_items?.length > 0 && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Immediate Action Items</p>
              <ol className="space-y-1 list-decimal list-inside">
                {strategy.immediate_action_items.map((a, i) => (
                  <li key={i} className="text-sm text-gray-300">{a}</li>
                ))}
              </ol>
            </div>
          )}
          {strategy.disclaimer && (
            <p className="text-xs text-gray-500 italic border-t border-gray-700 pt-2 mt-2">
              {strategy.disclaimer}
            </p>
          )}
        </Section>
      )}
    </div>
  );
}

function Section({ title, color, children }) {
  const colors = {
    indigo: "border-indigo-700 text-indigo-400",
    blue: "border-blue-700 text-blue-400",
    red: "border-red-700 text-red-400",
    orange: "border-orange-700 text-orange-400",
    purple: "border-purple-700 text-purple-400",
    green: "border-green-700 text-green-400",
  };
  return (
    <div className={`border rounded-xl p-4 bg-gray-900 ${colors[color]}`}>
      <h3 className={`text-xs font-semibold uppercase tracking-widest mb-3 ${colors[color]}`}>
        {title}
      </h3>
      {children}
    </div>
  );
}

function RiskBadge({ score }) {
  const color = score < 30 ? "bg-green-800 text-green-200" :
                score < 60 ? "bg-yellow-800 text-yellow-200" :
                "bg-red-800 text-red-200";
  return (
    <span className={`text-xs px-2 py-1 rounded-full mt-2 inline-block ${color}`}>
      Risk Score: {score}/100
    </span>
  );
}

function SeverityBadge({ severity }) {
  const color = severity === "low" ? "bg-green-800 text-green-200" :
                severity === "medium" ? "bg-yellow-800 text-yellow-200" :
                "bg-red-800 text-red-200";
  return <span className={`text-xs px-2 py-0.5 rounded-full ${color}`}>{severity}</span>;
}
