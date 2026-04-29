"""
Domain Guard — classifies whether a query is a valid Indian legal matter.
Accepts all 10 categories from the legal dataset.
"""

# ── Category keyword maps ─────────────────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "Family Law": [
        "divorce", "maintenance", "custody", "marriage", "husband", "wife",
        "separation", "matrimonial", "alimony", "child support", "guardianship",
        "adoption", "will", "inheritance", "succession", "family", "spouse",
        "annulment", "bigamy", "second marriage", "nri husband", "grandchildren",
        "visitation", "streedhan", "dowry return", "senior citizen", "parents neglect"
    ],
    "Dowry & Domestic Violence": [
        "dowry", "domestic violence", "498a", "498-a", "dv act", "harassment",
        "in-laws", "cruelty", "physical abuse", "mental harassment", "beaten",
        "assault", "protection order", "residence order", "abusive husband",
        "intimate photos", "blackmail", "threatening divorce"
    ],
    "Consumer Complaints": [
        "consumer", "defective", "product", "refund", "warranty", "service",
        "overcharged", "not delivered", "insurance claim", "hospital bill",
        "electricity bill", "telecom", "mobile", "online shopping", "gym",
        "travel agency", "school fees", "catering", "dry cleaner", "mechanic",
        "jeweller", "gold", "e-commerce", "amazon", "flipkart", "deficiency"
    ],
    "Financial Disputes": [
        "cheque bounce", "cheque", "bounce", "bounced", "dishonour", "loan", "emi",
        "bank", "interest", "salary unpaid", "wages", "pf", "provident fund",
        "chit fund", "ponzi", "investment fraud", "mutual fund", "fixed deposit",
        "fd", "tds", "credit card", "recovery", "money lent", "debt",
        "non-payment", "ni act", "negotiable instruments", "repay", "borrow",
        "lend", "lent", "borrowed", "money back", "refund money"
    ],
    "Property & RERA Issues": [
        "builder", "flat", "possession", "rera", "apartment", "property",
        "developer", "allotment", "sale agreement", "delay", "construction",
        "housing", "real estate", "plot", "installment", "tower", "project",
        "bhk", "registry", "maharera", "promoter", "landlord", "tenant",
        "rent", "eviction", "encroachment", "boundary", "noc", "society",
        "common area", "disputed title", "ancestral property", "partition"
    ],
    "Employment Disputes": [
        "employer", "employee", "job", "salary", "termination", "fired",
        "retrenchment", "gratuity", "pf deduction", "sexual harassment",
        "workplace", "posh", "experience certificate", "relieving letter",
        "non-compete", "maternity leave", "contract employee", "regularisation",
        "labour", "industrial dispute", "wrongful termination", "notice period",
        "blank documents", "coercion employer"
    ],
    "Cyber Complaints": [
        "cyber", "online fraud", "upi", "otp", "hacked", "phishing",
        "morphed photos", "fake job", "social media", "instagram", "facebook",
        "loan app", "ransomware", "defamatory post", "fake legal notice",
        "matrimonial fraud", "romance scam", "child predator", "online",
        "internet", "scam", "digital", "it act", "cybercrime"
    ],
    "General Criminal Issues": [
        "fir", "police", "arrest", "bail", "theft", "robbery", "assault",
        "stalking", "threatening", "neighbour threatening", "road rage",
        "drunk driving", "accident", "mob", "lynching", "fake government job",
        "criminal", "complaint", "magistrate", "sessions court", "ipc",
        "crpc", "offence", "crime", "victim", "acid attack"
    ],
    "Small Civil Disputes": [
        "contractor", "advance", "shopkeeper", "expired", "parking dispute",
        "wedding venue", "tree fell", "car repair", "catering", "jeweller",
        "civil dispute", "small claim", "neighbour dispute", "damage",
        "compensation", "civil court", "recovery", "money dispute"
    ],
    "General Legal Advice": [
        "how to", "what is", "legal process", "procedure", "rights",
        "will", "testament", "legal heir", "name change", "rent agreement",
        "rti", "right to information", "caste certificate", "driving licence",
        "free legal aid", "lok adalat", "partnership firm", "adoption",
        "traffic challan", "police complaint", "legal advice", "what can i do",
        "what are my rights", "can i file", "is it legal"
    ]
}

# Flat list for quick "is it a legal query at all" check
ALL_LEGAL_KEYWORDS = [kw for kws in CATEGORY_KEYWORDS.values() for kw in kws]

OUT_OF_SCOPE_RESPONSE = (
    "I'm Justicia, an AI legal assistant for Indian law. "
    "I can help with Family Law, Domestic Violence, Consumer Complaints, "
    "Financial Disputes, Property/RERA, Employment, Cyber Crimes, Criminal matters, "
    "Civil Disputes, and General Legal Advice. "
    "Please describe your legal issue and I'll guide you."
)


def detect_category(query: str) -> str:
    """Detect the most likely legal category for a query."""
    query_lower = query.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[category] = score
    if not scores:
        return "General Legal Advice"
    return max(scores, key=scores.get)


def is_legal_query(query: str) -> bool:
    """Returns True if query is a valid Indian legal matter."""
    query_lower = query.lower()
    if any(kw in query_lower for kw in ALL_LEGAL_KEYWORDS):
        return True
    # Accept general help/question queries
    question_words = ["how", "what", "can i", "should i", "is it", "help",
                      "advice", "legal", "my problem", "i want to", "i need",
                      "what to do", "rights", "complaint", "case", "court",
                      "police", "lawyer", "advocate", "file", "sue"]
    return any(q in query_lower for q in question_words)


# Keep backward compat alias
def is_rera_query(query: str) -> bool:
    return is_legal_query(query)
