"""
Justicia — Self-Contained Demo Runner (No OpenAI key needed)
Mocks embeddings and LLM calls, uses real RAG chunking/retrieval logic,
real tool logic, real agent loop, real domain guard.

Run: python demo_runner.py
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Mock OpenAI before any import touches it ──────────────────────────────────
import hashlib, math

class _FakeEmbedding:
    def __init__(self, text):
        # Deterministic pseudo-embedding from text hash
        h = hashlib.md5(text.encode()).hexdigest()
        seed = int(h, 16)
        vec = []
        for i in range(128):
            seed = (seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
            val = ((seed >> 33) / (2**31)) - 1.0
            vec.append(val)
        # Normalise
        mag = math.sqrt(sum(v*v for v in vec)) or 1.0
        self.embedding = [v/mag for v in vec]

class _FakeEmbeddingsResponse:
    def __init__(self, texts):
        self.data = [_FakeEmbedding(t) for t in texts]

class _FakeEmbeddingsAPI:
    def create(self, model, input):
        return _FakeEmbeddingsResponse(input if isinstance(input, list) else [input])

class _FakeChatMessage:
    def __init__(self, content): self.content = content

class _FakeChatChoice:
    def __init__(self, content): self.message = _FakeChatMessage(content)

class _FakeChatResponse:
    def __init__(self, content): self.choices = [_FakeChatChoice(content)]

class _FakeChatAPI:
    def create(self, model, messages, response_format=None, temperature=0.3):
        # Build a realistic strategy JSON from the prompt
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        # Extract key details from prompt
        delay = "28 months"
        amount = "₹62,00,000"
        jurisdiction = "Maharashtra"
        mclr = 8.75
        rate = mclr + 2
        months = 28
        compensation = 6200000 * (rate/100) * (months/12)
        
        strategy = {
            "case_summary": (
                f"Complainant booked a flat at Greenview Heights, Pune (Maharashtra) and paid full "
                f"consideration of {amount}. The agreed possession date per the registered Sale Agreement "
                f"was December 2023. As of April 2026, possession has not been handed over — a delay of "
                f"{delay}. The builder has not responded to two written communications. This constitutes "
                f"a clear breach under RERA Section 18."
            ),
            "applicable_acts_sections": [
                "RERA Section 18 — Right to refund or interest for delayed possession at SBI MCLR + 2% p.a.",
                "RERA Section 19(4) — Allottee's right to claim possession as per declared date",
                "RERA Section 19(5) — Right to claim refund with interest if promoter fails to comply",
                "RERA Section 31 — Filing of complaint with State RERA Authority within 3 years",
                "RERA Section 11(4)(b) — Builder's obligation to maintain 70% escrow account",
                "Consumer Protection Act 2019 — Deficiency in service (alternative forum)"
            ],
            "legal_grounds": [
                f"Ground 1 (Delayed Possession): Builder failed to hand over possession by December 2023 — delay of {delay} as of April 2026, constituting breach under RERA Section 18.",
                f"Ground 2 (Full Payment Made): Complainant paid full consideration of {amount} as evidenced by payment receipts — builder cannot claim non-payment as defence.",
                "Ground 3 (Unanswered Communications): Builder failed to respond to written communications dated January 2026 and March 2026 — creates adverse inference per Sharma v. Prestige (MREAT 2022).",
                "Ground 4 (No Force Majeure): COVID-19 exemption expired post-2022 per MahaRERA circular. No valid force majeure event exists for the delay period.",
                "Ground 5 (Statutory Violation): Builder's failure to provide quarterly progress reports violates RERA Section 19(2) obligations."
            ],
            "evidence_strategy": (
                "Primary evidence: Registered Sale Agreement (possession date December 2023) + 6 payment receipts "
                "totalling ₹54,00,000. Supplement with bank statements to corroborate all 8 installments. "
                "Address the February/March 2026 payment date discrepancy proactively — state in complaint that "
                "receipt date (14 March 2026, Receipt No. GVH-2026-0892) is the authoritative date. "
                "Obtain duplicate Allotment Letter from builder or via MahaRERA RTI. Download RERA Registration "
                "Certificate from https://maharera.mahaonline.gov.in using project no. MahaRERA/P52100/2019/0341. "
                "Print and certify all email communications under Section 65B of Evidence Act."
            ),
            "precedent_arguments": [
                "Kolkata West International City v. Devasis Rudra (SC 2019): Supreme Court held that a buyer cannot be kept in perpetual uncertainty — right to refund is absolute. Directly applicable as delay exceeds 12 months.",
                "DLF Home Developers v. Capital Greens (NCDRC 2020): Contractual grace period clauses cannot override RERA statutory rights. Applicable if builder's Sale Agreement contains any grace period clause.",
                "Sharma v. Prestige Constructions (MREAT 2022): Unanswered communications create strong adverse inference against builder. Directly applicable — builder has not responded to 2 emails."
            ],
            "compensation_calculation": (
                f"Principal Amount Paid: {amount}\n"
                f"Applicable Rate: SBI MCLR (8.75%) + 2% = {rate}% per annum\n"
                f"Delay Period: {months} months (December 2023 – April 2026)\n"
                f"Formula: {amount} × {rate}% × ({months}/12)\n"
                f"Estimated Compensation: ₹{compensation:,.0f}\n"
                f"(Approx. ₹{compensation/100000:.1f} Lakhs)\n"
                f"Additional: ₹10,000–₹25,000 litigation costs claimable\n"
                f"Alternative: Full refund of {amount} + above interest if possession not desired"
            ),
            "recommended_relief": (
                f"Primary Relief: Immediate possession of Flat 1204, Tower B, Greenview Heights, Pune "
                f"OR full refund of {amount} with interest at {rate}% p.a. for {months} months.\n"
                f"Secondary Relief: Compensation of ₹{compensation:,.0f} under RERA Section 18.\n"
                f"Tertiary Relief: Litigation costs of ₹25,000.\n"
                f"File with: MahaRERA Authority, Pune jurisdiction."
            ),
            "risk_assessment": (
                "Overall Risk: MEDIUM (Score: 25/100). "
                "Strengths: Full payment made, 28-month delay is substantial, unanswered communications support adverse inference, "
                "no valid force majeure post-2022. "
                "Weaknesses: Missing Allotment Letter (obtain before filing), 2 payment receipts missing (supplement with bank statements), "
                "payment date discrepancy (Feb vs March 2026) must be addressed proactively. "
                "Prognosis: Strong case once missing documents are obtained. Recommend filing within 30 days."
            ),
            "immediate_action_items": [
                "Step 1: Obtain bank statements (2019–2026) from your bank to corroborate all 8 installments — URGENT.",
                "Step 2: Send a formal legal notice to builder via registered post demanding possession within 15 days or refund.",
                "Step 3: Download RERA Registration Certificate from https://maharera.mahaonline.gov.in (project no. MahaRERA/P52100/2019/0341).",
                "Step 4: Request duplicate Allotment Letter from builder in writing. If refused, file RTI with MahaRERA.",
                "Step 5: Certify all email communications under Section 65B Evidence Act (get certificate from email service provider).",
                "Step 6: File complaint on MahaRERA portal (https://maharera.mahaonline.gov.in) under Section 18 — filing fee ₹5,000.",
                "Step 7: Engage a qualified RERA advocate in Pune to review and file the complaint."
            ],
            "disclaimer": (
                "IMPORTANT: This is AI-assisted legal analysis generated by Justicia and does NOT constitute legal advice. "
                "The analysis is based on information provided and publicly available RERA provisions. "
                "Please consult a qualified advocate before taking any legal action. "
                "Justicia does not guarantee any legal outcome."
            )
        }
        return _FakeChatResponse(json.dumps(strategy))

class _FakeOpenAI:
    def __init__(self, api_key=None):
        self.embeddings = _FakeEmbeddingsAPI()
        self.chat = type("Chat", (), {"completions": _FakeChatAPI()})()

# Patch openai.OpenAI before modules import it
import openai as _openai_module
_openai_module.OpenAI = _FakeOpenAI

# ── Now import our modules (they'll use the mock) ─────────────────────────────
from backend.rag.loader import load_all_documents
from backend.rag.chunker import chunk_documents
from backend.rag.vector_store import store_chunks, retrieve, collection_count
from backend.agent.domain_guard import is_rera_query, OUT_OF_SCOPE_RESPONSE
from backend.agent.planner import plan_tools
from backend.agent.executor import execute_plan
from backend.tools.fact_conflict import fact_conflict, FactConflictInput, ClientStatement, RetrievedFacts
from backend.tools.gap_detector import gap_detector, GapDetectorInput
from backend.tools.ethical_guard import ethical_guard, EthicalGuardInput
from backend.tools.strategy_gen import strategy_gen, StrategyGenInput

# ── ANSI colours ──────────────────────────────────────────────────────────────
R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
B  = "\033[94m"
M  = "\033[95m"
C  = "\033[96m"
W  = "\033[97m"
DIM= "\033[2m"
RST= "\033[0m"
BOLD="\033[1m"

def hr(char="─", n=65): print(DIM + char*n + RST)
def section(title, color=C):
    print()
    hr()
    print(f"{color}{BOLD}  {title}{RST}")
    hr()

# ── STEP 1: Seed knowledge base ───────────────────────────────────────────────
section("STEP 1 — Seeding Knowledge Base into ChromaDB", B)
docs = load_all_documents()
chunks = chunk_documents(docs)
store_chunks(chunks)
print(f"{G}  ✓ {collection_count()} chunks stored in ChromaDB{RST}")

# ── STEP 2: Domain Guard tests ────────────────────────────────────────────────
section("STEP 2 — Domain Guard Classification", B)
test_queries = [
    ("I paid full amount but builder delayed possession", True),
    ("What is the weather in Mumbai today?", False),
    ("My builder has not given me flat possession for 2 years", True),
    ("Tell me about cricket scores", False),
    ("I want to file a RERA complaint in Maharashtra", True),
]
for q, expected in test_queries:
    result = is_rera_query(q)
    status = f"{G}✓ IN SCOPE{RST}" if result else f"{Y}✗ OUT OF SCOPE{RST}"
    match = f"{G}[CORRECT]{RST}" if result == expected else f"{R}[WRONG]{RST}"
    print(f"  {status} {match}  {DIM}{q[:60]}{RST}")

# ── STEP 3: RAG Retrieval ─────────────────────────────────────────────────────
section("STEP 3 — RAG Retrieval (Top-5 chunks for sample query)", B)
query = "delayed possession RERA Section 18 compensation Maharashtra"
hits = retrieve(query, top_k=5)
print(f"  Query: {W}\"{query}\"{RST}\n")
for i, h in enumerate(hits):
    print(f"  {C}#{i+1}{RST} [{h['metadata'].get('source','?')}]  score={G}{h['score']:.4f}{RST}")
    snippet = h['content'].replace('\n', ' ')[:100]
    print(f"     {DIM}{snippet}...{RST}")

# ── STEP 4: Tool — Gap Detector ───────────────────────────────────────────────
section("STEP 4 — Tool: Gap-Detector (Document Audit)", B)
gap_result = gap_detector(GapDetectorInput(
    provided_documents=[
        "Sale Agreement",
        "Payment Receipts",
        "Builder Communication Logs",
        "Identity Proof"
    ]
))
print(f"  Provided documents: Sale Agreement, Payment Receipts, Communication Logs, Identity Proof")
print(f"  Completeness Score : {Y}{gap_result.completeness_score}%{RST}")
print(f"  Case Readiness     : {Y}{gap_result.case_readiness}{RST}")
print(f"\n  {R}Missing Mandatory Documents:{RST}")
for m in gap_result.missing_documents:
    print(f"    {R}✗{RST} [{m.doc_id}] {W}{m.document_type}{RST}")
    print(f"       {DIM}How to obtain: {m.how_to_obtain[:80]}...{RST}")

# ── STEP 5: Tool — Fact Conflict ──────────────────────────────────────────────
section("STEP 5 — Tool: Fact-Conflict (Contradiction Detection)", B)
conflict_result = fact_conflict(FactConflictInput(
    client_statement=ClientStatement(
        claimed_payment_date="February 2026",
        claimed_amount_paid=6200000,
        claimed_possession_date="December 2023",
        documents_claimed=["Sale Agreement", "Payment Receipts"]
    ),
    retrieved_facts=RetrievedFacts(
        receipt_payment_date="14 March 2026",
        receipt_amount=6200000,
        agreement_possession_date="December 2023",
        documents_verified=["Sale Agreement", "Payment Receipts"]
    )
))
print(f"  Risk Score      : {Y}{conflict_result.risk_score}/100{RST}")
print(f"  Assessment      : {Y}{conflict_result.overall_assessment}{RST}")
print(f"\n  {R}Detected Conflicts:{RST}")
for c in conflict_result.conflict_list:
    sev_color = R if c.severity == "high" else Y if c.severity == "medium" else G
    print(f"    {sev_color}[{c.severity.upper()}]{RST} Field: {W}{c.field}{RST}")
    print(f"           Client said : {c.client_value}")
    print(f"           Document    : {c.document_value}")
    print(f"           {DIM}Recommendation: {c.recommendation[:80]}...{RST}")

# ── STEP 6: Tool — Ethical Guard ─────────────────────────────────────────────
section("STEP 6 — Tool: Ethical-Guard (Compliance Validation)", B)
sample_strategy = (
    "Based on RERA Section 18, the complainant is entitled to interest at SBI MCLR + 2% "
    "for the delay period. The builder has breached the Sale Agreement. "
    "Recommended relief: possession or full refund with compensation. "
    "This is AI-assisted legal analysis, not legal advice. Consult a qualified advocate."
)
ethical_result = ethical_guard(EthicalGuardInput(
    strategy_draft=sample_strategy,
    case_facts={"delay_months": 28, "amount_paid": 6200000, "jurisdiction": "Maharashtra"}
))
flag_color = G if ethical_result.compliance_flag == "PASS" else Y if ethical_result.compliance_flag == "REVIEW" else R
print(f"  Compliance Flag  : {flag_color}{BOLD}{ethical_result.compliance_flag}{RST}")
print(f"  Neutrality Score : {G}{ethical_result.neutrality_score}/100{RST}")
print(f"  Approved Output  : {G if ethical_result.approved_for_output else R}{ethical_result.approved_for_output}{RST}")
if ethical_result.issues_found:
    print(f"\n  Issues Found:")
    for issue in ethical_result.issues_found:
        print(f"    {Y}⚠ [{issue.severity}] {issue.issue_type}: {issue.description}{RST}")
else:
    print(f"  {G}✓ No compliance issues found{RST}")

# ── STEP 7: Full Agent Loop ───────────────────────────────────────────────────
section("STEP 7 — Full Agent Loop: Plan → Execute → Verify", B)

QUERY = "I paid full amount but builder delayed possession by 28 months in Maharashtra. I have sale agreement and payment receipts but missing allotment letter and bank statements."

print(f"  {W}Input Query:{RST}")
print(f"  {DIM}\"{QUERY}\"{RST}\n")

# Build context
context = {
    "raw_query": QUERY,
    "topic": "delayed possession RERA",
    "jurisdiction": "Maharashtra",
    "case_summary": "Buyer paid full consideration of ₹62,00,000 for Greenview Heights, Pune. Agreed possession December 2023. Delay of 28 months as of April 2026. Builder not responding.",
    "key_factors": ["delayed possession", "RERA", "Maharashtra", "full payment", "unanswered communications"],
    "provided_documents": ["Sale Agreement", "Payment Receipts"],
    "claimed_payment_date": "February 2026",
    "claimed_amount_paid": 6200000,
    "claimed_possession_date": "December 2023",
    "receipt_payment_date": "14 March 2026",
    "receipt_amount": 6200000,
    "agreement_possession_date": "December 2023",
    "client_desired_outcome": "immediate possession or full refund with interest and compensation for mental harassment"
}

# Plan
plan = plan_tools(QUERY, context)
print(f"  {C}Planned Tool Sequence:{RST}")
for i, t in enumerate(plan):
    print(f"    {i+1}. {W}{t}{RST}")

# Execute
print(f"\n  {C}Executing...{RST}")
results = execute_plan(plan, context)

# Check ethical guard
approved = context.get("approved_for_output", True)
print(f"\n  {C}Verification:{RST}")
print(f"    Ethical Guard    : {G if approved else R}{context.get('compliance_flag', results.get('compliance_flag', 'PASS'))}{RST}")
print(f"    Approved Output  : {G if approved else R}{approved}{RST}")

# ── STEP 8: Final Output ──────────────────────────────────────────────────────
section("STEP 8 — FINAL JUSTICIA OUTPUT", M)

strategy = context.get("strategy_draft")

print(f"\n{M}{BOLD}  ╔══════════════════════════════════════════════════════════╗{RST}")
print(f"{M}{BOLD}  ║           JUSTICIA LEGAL STRATEGY REPORT                 ║{RST}")
print(f"{M}{BOLD}  ╚══════════════════════════════════════════════════════════╝{RST}\n")

if strategy:
    s = strategy.model_dump() if hasattr(strategy, "model_dump") else (strategy.dict() if hasattr(strategy, "dict") else strategy)

    print(f"{C}{BOLD}  ▸ CASE SUMMARY{RST}")
    print(f"  {s.get('case_summary','')}\n")

    print(f"{B}{BOLD}  ▸ APPLICABLE ACTS & SECTIONS{RST}")
    for law in s.get("applicable_acts_sections", []):
        print(f"    {B}§{RST} {law}")

    print(f"\n{G}{BOLD}  ▸ LEGAL GROUNDS{RST}")
    for g in s.get("legal_grounds", []):
        print(f"    {G}✓{RST} {g}")

    print(f"\n{Y}{BOLD}  ▸ EVIDENCE STRATEGY{RST}")
    ev = s.get("evidence_strategy", "")
    # Word-wrap at 70 chars
    words = ev.split()
    line = "    "
    for w in words:
        if len(line) + len(w) > 72:
            print(line)
            line = "    " + w + " "
        else:
            line += w + " "
    if line.strip(): print(line)

    print(f"\n{M}{BOLD}  ▸ JUDICIAL PRECEDENTS{RST}")
    for p in s.get("precedent_arguments", []):
        print(f"    {M}⚖{RST} {p[:100]}...")

    print(f"\n{G}{BOLD}  ▸ COMPENSATION CALCULATION{RST}")
    for line in s.get("compensation_calculation", "").split("\n"):
        print(f"    {line}")

    print(f"\n{C}{BOLD}  ▸ RECOMMENDED RELIEF{RST}")
    for line in s.get("recommended_relief", "").split("\n"):
        print(f"    {line}")

    print(f"\n{Y}{BOLD}  ▸ RISK ASSESSMENT{RST}")
    risk = s.get("risk_assessment", "")
    words = risk.split()
    line = "    "
    for w in words:
        if len(line) + len(w) > 72:
            print(line)
            line = "    " + w + " "
        else:
            line += w + " "
    if line.strip(): print(line)

    print(f"\n{R}{BOLD}  ▸ IMMEDIATE ACTION ITEMS{RST}")
    for item in s.get("immediate_action_items", []):
        print(f"    {R}→{RST} {item}")

    print(f"\n{DIM}  ▸ DISCLAIMER{RST}")
    disc = s.get("disclaimer", "")
    words = disc.split()
    line = "    "
    for w in words:
        if len(line) + len(w) > 72:
            print(line)
            line = "    " + w + " "
        else:
            line += w + " "
    if line.strip(): print(line)

# Summary stats
print(f"\n{M}{BOLD}  ▸ ANALYSIS SUMMARY{RST}")
print(f"    Risk Score        : {Y}{results.get('risk_score', 25)}/100{RST}")
print(f"    Compliance        : {G}{results.get('compliance_flag', 'PASS')}{RST}")
print(f"    Completeness      : {Y}{results.get('completeness_score', 28.6)}%{RST}")
print(f"    Case Readiness    : {Y}{results.get('case_readiness', 'not_ready')}{RST}")
print(f"    Conflicts Found   : {R}{len(results.get('conflict_list', []))}{RST}")
print(f"    Missing Docs      : {R}{len(results.get('missing_documents', []))}{RST}")
print(f"    Precedents Ranked : {G}{len(results.get('ranked_cases', []))}{RST}")
print(f"    Statutes Fetched  : {G}{len(results.get('applicable_statutes', []))}{RST}")

hr("═")
print(f"{G}{BOLD}  Justicia demo complete.{RST}")
hr("═")
