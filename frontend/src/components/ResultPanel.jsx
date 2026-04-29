export default function ResultPanel({ result, categoryColors = {} }) {
  if (!result) return null;

  if (result.status === "out_of_scope") {
    return (
      <div className="mx-4 my-3 p-4 bg-yellow-900/40 border border-yellow-700 rounded-xl text-yellow-300 text-sm">
        <span className="font-semibold">Out of scope: </span>{result.message}
      </div>
    );
  }

  const strategy = result.legal_strategy;
  const catClass = categoryColors[result.category] || "bg-gray-800 text-gray-300 border-gray-600";

  return (
    <div className="flex flex-col gap-3 p-4">

      {/* Category + Case Summary */}
      <Section title="Case Summary" color="indigo">
        {result.category && (
          <span className={`text-xs px-2 py-1 rounded-full border mb-2 inline-block ${catClass}`}>
            {result.category}
          </span>
        )}
        <p className="text-sm text-gray-300 mt-1">{result.case_summary}</p>
        <div className="flex flex-wrap gap-2 mt-2">
          {result.risk_score != null && <RiskBadge score={result.risk_score} />}
          {result.case_readiness && (
            <span className={`text-xs px-2 py-1 rounded-full ${
              result.case_readiness === "ready" ? "bg-green-800 text-green-200" :
              result.case_readiness === "needs_attention" ? "bg-yellow-800 text-yellow-200" :
              "bg-red-800 text-red-200"}`}>
              Readiness: {result.case_readiness.replace(/_/g, " ")}
            </span>
          )}
          {result.compliance_flag && (
            <span className={`text-xs px-2 py-1 rounded-full ${
              result.compliance_flag === "PASS" ? "bg-green-900 text-green-300" :
              result.compliance_flag === "REVIEW" ? "bg-yellow-900 text-yellow-300" :
              "bg-red-900 text-red-300"}`}>
              {result.compliance_flag}
            </span>
          )}
        </div>
      </Section>

      {/* Applicable Laws */}
      {strategy?.applicable_acts_sections?.length > 0 && (
        <Section title="Applicable Acts & Sections" color="blue">
          <ul className="space-y-1">
            {strategy.applicable_acts_sections.map((law, i) => (
              <li key={i} className="text-sm text-blue-200 flex gap-2">
                <span className="text-blue-500 shrink-0 mt-0.5">§</span>
                <span>{law}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Legal Grounds */}
      {strategy?.legal_grounds?.length > 0 && (
        <Section title="Legal Grounds" color="green">
          <ul className="space-y-1">
            {strategy.legal_grounds.map((g, i) => (
              <li key={i} className="text-sm text-gray-300 flex gap-2">
                <span className="text-green-500 shrink-0">✓</span>{g}
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
              <p className="text-xs text-gray-400">You said: <span className="text-gray-200">{c.client_value}</span></p>
              <p className="text-xs text-gray-400">Document: <span className="text-gray-200">{c.document_value}</span></p>
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
              <p className="text-xs text-gray-400 mt-1">{m.how_to_obtain}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Judicial Precedents */}
      {result.judicial_precedents?.length > 0 && (
        <Section title="Relevant Precedents" color="purple">
          {result.judicial_precedents.map((p, i) => (
            <div key={i} className="mb-2 p-3 bg-purple-950/40 rounded-lg border border-purple-800">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-purple-300">#{p.rank} {p.case_name}</span>
                <span className="text-xs text-purple-400">{p.relevance_score}</span>
              </div>
              <p className="text-xs text-gray-400 mt-1">{p.applicable_to_current_case}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Strategy details */}
      {strategy && (
        <Section title="Legal Strategy" color="teal">
          {strategy.evidence_strategy && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Evidence Strategy</p>
              <p className="text-sm text-gray-300">{strategy.evidence_strategy}</p>
            </div>
          )}
          {strategy.compensation_calculation && (
            <div className="mb-3 p-3 bg-teal-950/40 rounded-lg border border-teal-800">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Compensation / Relief Estimate</p>
              <p className="text-sm text-teal-300 whitespace-pre-line">{strategy.compensation_calculation}</p>
            </div>
          )}
          {strategy.recommended_relief && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Recommended Relief</p>
              <p className="text-sm text-gray-300 whitespace-pre-line">{strategy.recommended_relief}</p>
            </div>
          )}
          {strategy.risk_assessment && (
            <div className="mb-3 p-3 bg-yellow-950/30 rounded-lg border border-yellow-800">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Risk Assessment</p>
              <p className="text-sm text-yellow-300">{strategy.risk_assessment}</p>
            </div>
          )}
          {strategy.immediate_action_items?.length > 0 && (
            <div className="mb-3">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Immediate Action Items</p>
              <ol className="space-y-2">
                {strategy.immediate_action_items.map((a, i) => (
                  <li key={i} className="flex gap-2 text-sm text-gray-300">
                    <span className="shrink-0 w-5 h-5 bg-indigo-700 rounded-full flex items-center justify-center text-xs text-white">{i + 1}</span>
                    <span>{a}</span>
                  </li>
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
  const border = {
    indigo: "border-indigo-800", blue: "border-blue-800", green: "border-green-800",
    red: "border-red-800", orange: "border-orange-800", purple: "border-purple-800",
    teal: "border-teal-800",
  };
  const text = {
    indigo: "text-indigo-400", blue: "text-blue-400", green: "text-green-400",
    red: "text-red-400", orange: "text-orange-400", purple: "text-purple-400",
    teal: "text-teal-400",
  };
  return (
    <div className={`border rounded-xl p-4 bg-gray-900 ${border[color]}`}>
      <h3 className={`text-xs font-semibold uppercase tracking-widest mb-3 ${text[color]}`}>{title}</h3>
      {children}
    </div>
  );
}

function RiskBadge({ score }) {
  const c = score < 30 ? "bg-green-800 text-green-200" : score < 60 ? "bg-yellow-800 text-yellow-200" : "bg-red-800 text-red-200";
  return <span className={`text-xs px-2 py-1 rounded-full ${c}`}>Risk: {score}/100</span>;
}

function SeverityBadge({ severity }) {
  const c = severity === "low" ? "bg-green-800 text-green-200" : severity === "medium" ? "bg-yellow-800 text-yellow-200" : "bg-red-800 text-red-200";
  return <span className={`text-xs px-2 py-0.5 rounded-full ${c}`}>{severity}</span>;
}
