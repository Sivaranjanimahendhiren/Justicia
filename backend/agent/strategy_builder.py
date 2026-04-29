"""
Category-aware strategy builder for the mock LLM.
Returns realistic legal strategies for all 10 categories.
"""
import json

STRATEGIES = {
    "Family Law": {
        "divorce": {
            "applicable_acts_sections": [
                "Hindu Marriage Act 1955 Section 13 — Grounds for divorce including cruelty, desertion, adultery",
                "Hindu Marriage Act 1955 Section 13B — Divorce by mutual consent after 1 year separation",
                "Hindu Marriage Act 1955 Section 24 — Interim maintenance during proceedings",
                "CrPC Section 125 — Maintenance for wife and children",
            ],
            "legal_grounds": [
                "Ground 1: Cruelty (mental or physical) under Section 13(1)(ia) of Hindu Marriage Act",
                "Ground 2: Desertion for 2+ years under Section 13(1)(ib)",
                "Ground 3: Mutual consent available if both parties agree under Section 13B",
            ],
            "evidence_strategy": "Gather evidence of cruelty — messages, medical records, witness statements. Maintain a diary of incidents with dates. Preserve all financial records for maintenance claim.",
            "precedent_arguments": [
                "Naveen Kohli v. Naveen Kohli (SC 2006): Irretrievable breakdown of marriage is a valid ground — Supreme Court recommended legislative amendment.",
                "Samar Ghosh v. Jaya Ghosh (SC 2007): Defined mental cruelty comprehensively — includes false allegations, persistent humiliation.",
            ],
            "compensation_calculation": "Interim maintenance under Section 24 HMA: 20-25% of spouse's net income. Permanent alimony under Section 25 based on standard of living and earning capacity.",
            "recommended_relief": "File divorce petition in Family Court. Apply for interim maintenance under Section 24. Seek permanent alimony and return of Streedhan.",
            "risk_assessment": "MEDIUM risk. Outcome depends on evidence of cruelty/desertion. Mutual consent divorce is fastest (3-6 months). Contested divorce can take 2-5 years.",
            "immediate_action_items": [
                "Step 1: Consult a family lawyer and assess grounds for divorce.",
                "Step 2: File divorce petition in Family Court with supporting evidence.",
                "Step 3: Apply for interim maintenance under Section 24 HMA.",
                "Step 4: Attend mandatory counselling sessions ordered by court.",
                "Step 5: Preserve all evidence — messages, photos, medical records, financial documents.",
            ],
        },
        "maintenance": {
            "applicable_acts_sections": [
                "CrPC Section 125 — Right to maintenance for wife, children, and parents",
                "Hindu Marriage Act Section 24 — Interim maintenance during proceedings",
                "Hindu Adoption and Maintenance Act 1956 — Maintenance obligations",
            ],
            "legal_grounds": [
                "Ground 1: Husband has sufficient means and neglects to maintain wife/children",
                "Ground 2: Wife is unable to maintain herself",
                "Ground 3: Children are unable to maintain themselves",
            ],
            "evidence_strategy": "Gather proof of husband's income — salary slips, ITR, bank statements. Document your expenses and children's needs. Preserve marriage certificate and children's birth certificates.",
            "precedent_arguments": [
                "Rajnesh v. Neha (SC 2020): Supreme Court issued comprehensive guidelines on maintenance — husband must disclose income, maintenance should be adequate.",
                "Bhuwan Mohan Singh v. Meena (SC 2014): Maintenance must be sufficient for wife to maintain same standard of living as during marriage.",
            ],
            "compensation_calculation": "Maintenance typically 20-30% of husband's net income for wife. Additional amount for each child. Interim maintenance can be claimed from date of application.",
            "recommended_relief": "File maintenance petition under CrPC 125 in Magistrate court. Apply for interim maintenance. Claim arrears from date of application.",
            "risk_assessment": "LOW-MEDIUM risk. Strong case if husband's income can be proven. Court can order attachment of salary if husband defaults.",
            "immediate_action_items": [
                "Step 1: File maintenance petition under CrPC 125 at nearest Magistrate court.",
                "Step 2: Apply for interim maintenance — court can grant within 60 days.",
                "Step 3: Gather proof of husband's income and your expenses.",
                "Step 4: Attach marriage certificate, children's birth certificates.",
                "Step 5: If husband defaults on payment, apply for execution of order.",
            ],
        },
    },
    "Dowry & Domestic Violence": {
        "default": {
            "applicable_acts_sections": [
                "IPC Section 498A — Husband or relative subjecting woman to cruelty (cognizable, non-bailable)",
                "Protection of Women from Domestic Violence Act 2005 — Protection, residence, monetary relief",
                "Dowry Prohibition Act 1961 — Giving/taking dowry is illegal",
                "IPC Section 406 — Criminal breach of trust for Streedhan recovery",
            ],
            "legal_grounds": [
                "Ground 1: Dowry demand constitutes cruelty under IPC 498A",
                "Ground 2: Physical/mental abuse is domestic violence under DV Act 2005",
                "Ground 3: Economic abuse (withholding money) is covered under DV Act Section 3",
                "Ground 4: Right to reside in matrimonial home under DV Act Section 17",
            ],
            "evidence_strategy": "Preserve medical records of injuries. Screenshot all threatening messages. Note dates and witnesses for each incident. Collect receipts/photos of dowry items given.",
            "precedent_arguments": [
                "Hiral P. Harsora v. Kusum Narottamdas Harsora (SC 2016): DV Act applies to all respondents including female relatives.",
                "Indra Sarma v. V.K.V. Sarma (SC 2013): Live-in relationships also covered under DV Act.",
            ],
            "compensation_calculation": "Monetary relief under DV Act: actual losses + compensation for mental agony (courts typically award ₹10,000–₹50,000/month). Streedhan recovery: full value of items given.",
            "recommended_relief": "File FIR under IPC 498A. Apply for Protection Order, Residence Order, and Monetary Relief under DV Act 2005. Claim return of Streedhan.",
            "risk_assessment": "MEDIUM risk. Strong case with medical evidence and witnesses. Protection order can be obtained within 3 days in urgent cases.",
            "immediate_action_items": [
                "Step 1: Call Women Helpline 181 or police helpline 100 for immediate help.",
                "Step 2: File FIR at local police station under IPC 498A.",
                "Step 3: Contact District Protection Officer for DV Act complaint.",
                "Step 4: Apply for emergency Protection Order from Magistrate.",
                "Step 5: Preserve all evidence — medical records, messages, photos of injuries.",
                "Step 6: Apply for interim monetary relief for immediate financial support.",
            ],
        },
    },
    "Consumer Complaints": {
        "default": {
            "applicable_acts_sections": [
                "Consumer Protection Act 2019 Section 2(10) — Definition of defect in goods",
                "Consumer Protection Act 2019 Section 2(11) — Deficiency in service",
                "Consumer Protection Act 2019 Section 35 — Complaint to District Consumer Commission",
                "Consumer Protection Act 2019 Section 2(47) — Unfair trade practice",
            ],
            "legal_grounds": [
                "Ground 1: Defect in goods / deficiency in service under Consumer Protection Act 2019",
                "Ground 2: Unfair trade practice — misrepresentation or overcharging",
                "Ground 3: Breach of warranty/guarantee terms",
                "Ground 4: Failure to provide promised service",
            ],
            "evidence_strategy": "Preserve purchase invoice, warranty card, and all receipts. Document the defect with photos/videos. Keep records of all complaints made to the company. Get independent expert assessment if needed.",
            "precedent_arguments": [
                "Lucknow Development Authority v. M.K. Gupta (SC 1994): Deficiency in service by public bodies is actionable under Consumer Protection Act.",
                "Spring Meadows Hospital v. Harjol Ahluwalia (SC 1998): Medical negligence is deficiency in service.",
            ],
            "compensation_calculation": "Claim: Full refund/replacement value + compensation for mental harassment (₹5,000–₹50,000 typically) + litigation costs. District Commission handles claims up to ₹1 crore.",
            "recommended_relief": "Send legal notice demanding remedy within 15 days. File complaint at District Consumer Commission. Claim refund/replacement + compensation + litigation costs.",
            "risk_assessment": "LOW risk. Consumer forums are consumer-friendly. Most cases resolved within 3-6 months. Filing fee is nominal (₹100–₹500).",
            "immediate_action_items": [
                "Step 1: Send a legal notice to the company/service provider demanding remedy within 15 days.",
                "Step 2: Preserve all evidence — invoice, warranty, photos, repair records.",
                "Step 3: File complaint at District Consumer Commission (for claims up to ₹1 crore).",
                "Step 4: Attach all documents with the complaint.",
                "Step 5: Claim full refund/replacement + compensation for mental harassment + litigation costs.",
                "Step 6: Attend hearings — most cases resolved within 3-6 months.",
            ],
        },
    },
    "Financial Disputes": {
        "cheque_bounce": {
            "applicable_acts_sections": [
                "Negotiable Instruments Act 1881 Section 138 — Dishonour of cheque (criminal offence)",
                "NI Act Section 142 — Cognizance of offences — complaint within 30 days of dishonour",
                "NI Act Section 143A — Interim compensation up to 20% of cheque amount",
                "IPC Section 420 — Cheating (if fraudulent intent proven)",
            ],
            "legal_grounds": [
                "Ground 1: Cheque dishonoured due to insufficient funds — offence under NI Act 138",
                "Ground 2: Demand notice sent but payment not made within 15 days",
                "Ground 3: Criminal liability of drawer — up to 2 years imprisonment or fine up to twice cheque amount",
            ],
            "evidence_strategy": "Preserve original cheque, bank's dishonour memo, demand notice with proof of delivery. Ensure demand notice was sent within 30 days of dishonour.",
            "precedent_arguments": [
                "Dashrath Rupsingh Rathod v. State of Maharashtra (SC 2014): Jurisdiction lies where cheque was presented for payment.",
                "Meters and Instruments Pvt. Ltd. v. Kanchan Mehta (SC 2017): Court can order interim compensation under Section 143A.",
            ],
            "compensation_calculation": "Criminal fine: up to twice the cheque amount. Civil recovery: full cheque amount + interest + legal costs. Interim compensation: up to 20% of cheque amount during trial.",
            "recommended_relief": "File criminal complaint under NI Act 138 in Magistrate court. Apply for interim compensation under Section 143A. Also file civil suit for recovery.",
            "risk_assessment": "LOW risk. NI Act 138 is a strong remedy. Conviction rate is high. Most cases settled before trial once criminal complaint is filed.",
            "immediate_action_items": [
                "Step 1: Obtain the bank's dishonour memo immediately.",
                "Step 2: Send legal demand notice within 30 days of dishonour via registered post.",
                "Step 3: If no payment in 15 days, file complaint under NI Act 138 in Magistrate court.",
                "Step 4: Apply for interim compensation (20% of cheque amount) under Section 143A.",
                "Step 5: Attach original cheque, dishonour memo, demand notice, proof of delivery.",
            ],
        },
        "default": {
            "applicable_acts_sections": [
                "Indian Contract Act 1872 Section 73 — Compensation for breach of contract",
                "Code of Civil Procedure 1908 — Civil suit for money recovery",
                "Limitation Act 1963 — 3-year limitation for money recovery suits",
                "Indian Evidence Act Section 65B — Electronic records as evidence",
            ],
            "legal_grounds": [
                "Ground 1: Breach of contract / failure to repay money owed",
                "Ground 2: Unjust enrichment at the expense of the claimant",
                "Ground 3: Electronic evidence (messages, emails) admissible under Section 65B",
            ],
            "evidence_strategy": "Preserve all payment records, bank transfers, messages, and emails. Get Section 65B certificate for electronic evidence. Send legal notice before filing suit.",
            "precedent_arguments": [
                "Trimex International FZE Ltd. v. Vedanta Aluminium Ltd. (SC 2010): Electronic communications constitute valid contracts.",
            ],
            "compensation_calculation": "Claim: Principal amount + interest at 18% p.a. (or as agreed) + legal costs. File within 3 years of cause of action.",
            "recommended_relief": "Send legal notice demanding payment within 15 days. File civil suit for recovery in appropriate court. Consider Lok Adalat for faster resolution.",
            "risk_assessment": "MEDIUM risk. Depends on quality of evidence. WhatsApp/email evidence is admissible with Section 65B certificate.",
            "immediate_action_items": [
                "Step 1: Send a legal notice demanding repayment within 15 days.",
                "Step 2: Preserve all evidence — bank transfers, messages, emails.",
                "Step 3: Get Section 65B certificate for electronic evidence.",
                "Step 4: File civil suit for recovery in appropriate court.",
                "Step 5: Consider Lok Adalat for faster, free resolution.",
            ],
        },
    },
    "Property & RERA Issues": {
        "default": {
            "applicable_acts_sections": [
                "RERA Section 18 — Right to refund or interest for delayed possession at SBI MCLR + 2% p.a.",
                "RERA Section 19(4) — Allottee's right to claim possession as per declared date",
                "RERA Section 19(5) — Right to claim refund with interest if promoter fails to comply",
                "RERA Section 31 — Filing of complaint with State RERA Authority within 3 years",
                "Consumer Protection Act 2019 — Deficiency in service (alternative forum)",
            ],
            "legal_grounds": [
                "Ground 1: Delayed possession constitutes breach under RERA Section 18",
                "Ground 2: Full payment made — builder cannot claim non-payment as defence",
                "Ground 3: Unanswered communications create adverse inference against builder",
                "Ground 4: No valid force majeure post-2022",
            ],
            "evidence_strategy": "Primary evidence: Registered Sale Agreement + payment receipts + bank statements. Certify email communications under Section 65B. Download RERA certificate from state portal.",
            "precedent_arguments": [
                "Kolkata West International City v. Devasis Rudra (SC 2019): Right to refund is absolute after prolonged delay.",
                "DLF Home Developers v. Capital Greens (NCDRC 2020): Grace period clauses cannot override RERA rights.",
                "Sharma v. Prestige Constructions (MREAT 2022): Force majeure must be proven month-by-month.",
            ],
            "compensation_calculation": "Interest at SBI MCLR (8.75%) + 2% = 10.75% p.a. on amount paid for delay period. For >12 months delay: full refund + 10% compensation on total paid.",
            "recommended_relief": "File complaint with State RERA Authority under Section 18. Claim possession or full refund with interest. Claim litigation costs.",
            "risk_assessment": "LOW-MEDIUM risk. RERA is a strong consumer-friendly law. Most cases resolved within 6-12 months.",
            "immediate_action_items": [
                "Step 1: Send legal notice to builder demanding possession or refund within 15 days.",
                "Step 2: Download RERA Registration Certificate from state RERA portal.",
                "Step 3: File complaint on state RERA portal under Section 18.",
                "Step 4: Gather all payment receipts and bank statements.",
                "Step 5: Engage a RERA advocate for filing.",
            ],
        },
    },
    "Employment Disputes": {
        "default": {
            "applicable_acts_sections": [
                "Industrial Disputes Act 1947 Section 25F — Retrenchment compensation (15 days per year of service)",
                "Payment of Wages Act 1936 — Right to timely payment of wages",
                "Payment of Gratuity Act 1972 Section 4 — Gratuity after 5 years of service",
                "Maternity Benefit Act 1961 — 26 weeks paid maternity leave",
                "POSH Act 2013 — Sexual harassment at workplace",
            ],
            "legal_grounds": [
                "Ground 1: Wrongful termination without following due process under Industrial Disputes Act",
                "Ground 2: Non-payment of statutory dues — gratuity, PF, salary",
                "Ground 3: Violation of employment contract terms",
            ],
            "evidence_strategy": "Preserve appointment letter, salary slips, performance records, and all communications with employer. Document all incidents with dates.",
            "precedent_arguments": [
                "Workmen of Meenakshi Mills v. Meenakshi Mills (SC 1992): Retrenchment without following Section 25F procedure is void.",
                "Rajesh Sharma v. State of UP (SC 2017): Employee rights cannot be waived by contract.",
            ],
            "compensation_calculation": "Retrenchment compensation: 15 days wages per year of service. Gratuity: (Last salary × 15 × years) / 26. Unpaid salary: full amount + 18% interest.",
            "recommended_relief": "File complaint with Labour Commissioner. File case before Labour Court. Claim all statutory dues — salary, gratuity, PF, retrenchment compensation.",
            "risk_assessment": "MEDIUM risk. Labour courts are employee-friendly. Process takes 6-18 months. Interim relief available.",
            "immediate_action_items": [
                "Step 1: Send legal notice to employer demanding dues within 15 days.",
                "Step 2: File complaint with Labour Commissioner.",
                "Step 3: File case before Labour Court or Industrial Tribunal.",
                "Step 4: Preserve all employment documents — appointment letter, salary slips, PF records.",
                "Step 5: Claim all statutory dues — salary, gratuity, PF, retrenchment compensation.",
            ],
        },
    },
    "Cyber Complaints": {
        "default": {
            "applicable_acts_sections": [
                "IT Act 2000 Section 66C — Identity theft (up to 3 years imprisonment)",
                "IT Act 2000 Section 66D — Cheating by impersonation using computer resource",
                "IT Act 2000 Section 66E — Violation of privacy",
                "IPC Section 420 — Cheating and dishonestly inducing delivery of property",
                "IPC Section 503 — Criminal intimidation",
            ],
            "legal_grounds": [
                "Ground 1: Cyber fraud / cheating by impersonation under IT Act 66D",
                "Ground 2: Identity theft under IT Act 66C",
                "Ground 3: Financial loss due to fraudulent transaction",
            ],
            "evidence_strategy": "Preserve screenshots of all communications, transaction records, and fraudulent messages. Get Section 65B certificate for electronic evidence. Report to bank immediately for transaction reversal.",
            "precedent_arguments": [
                "Shreya Singhal v. Union of India (SC 2015): IT Act provisions must be applied carefully to protect free speech while punishing genuine cyber crimes.",
                "RBI Circular on Limiting Liability: Zero liability for customers who report fraud within 3 days.",
            ],
            "compensation_calculation": "Criminal fine under IT Act. Civil recovery of full amount lost. Bank reversal possible if reported within 3 days (RBI zero-liability guidelines).",
            "recommended_relief": "Report on cybercrime.gov.in immediately. File FIR at cyber crime police station. Contact bank for transaction reversal. File complaint with relevant regulatory authority.",
            "risk_assessment": "MEDIUM risk. Recovery depends on speed of reporting. Faster reporting = higher chance of money recovery. Cyber crime police have technical tools to trace perpetrators.",
            "immediate_action_items": [
                "Step 1: Report immediately on cybercrime.gov.in (National Cyber Crime Reporting Portal).",
                "Step 2: Call your bank immediately to block account and request transaction reversal.",
                "Step 3: File FIR at local cyber crime police station.",
                "Step 4: Preserve all evidence — screenshots, transaction records, communications.",
                "Step 5: Get Section 65B certificate for electronic evidence.",
                "Step 6: Follow up with bank and police regularly.",
            ],
        },
    },
    "General Criminal Issues": {
        "default": {
            "applicable_acts_sections": [
                "CrPC Section 154 — Mandatory registration of FIR for cognizable offences",
                "CrPC Section 156(3) — Magistrate can direct police to register FIR",
                "CrPC Section 436/437 — Bail in bailable/non-bailable offences",
                "CrPC Section 357A — Victim compensation scheme",
                "Constitution Article 22 — Right to legal counsel upon arrest",
            ],
            "legal_grounds": [
                "Ground 1: Right to have FIR registered for cognizable offences under CrPC 154",
                "Ground 2: Right to bail — bailable offences at police station, non-bailable before Magistrate",
                "Ground 3: Right to free legal aid under Legal Services Authorities Act",
            ],
            "evidence_strategy": "Document all evidence immediately — photos, medical records, witness names. File FIR promptly. Preserve all communications related to the incident.",
            "precedent_arguments": [
                "Lalita Kumari v. Govt. of UP (SC 2013): Police must mandatorily register FIR for cognizable offences — no preliminary inquiry required.",
                "D.K. Basu v. State of West Bengal (SC 1997): Guidelines on arrest and detention — rights of arrested persons.",
            ],
            "compensation_calculation": "Victim compensation under CrPC 357A — varies by state scheme. Medical expenses claimable. Compensation for loss of income during injury period.",
            "recommended_relief": "File FIR at police station. If refused, approach Superintendent of Police or Magistrate under CrPC 156(3). Engage a criminal lawyer. Apply for victim compensation.",
            "risk_assessment": "Depends on nature of offence and evidence. Engage a criminal lawyer immediately for best outcome.",
            "immediate_action_items": [
                "Step 1: File FIR at local police station immediately.",
                "Step 2: If police refuse, send complaint by registered post to Superintendent of Police.",
                "Step 3: If still refused, file complaint before Magistrate under CrPC 156(3).",
                "Step 4: Engage a criminal lawyer.",
                "Step 5: Apply for victim compensation under CrPC 357A.",
                "Step 6: Contact District Legal Services Authority (DLSA) for free legal aid if needed.",
            ],
        },
    },
    "Small Civil Disputes": {
        "default": {
            "applicable_acts_sections": [
                "Consumer Protection Act 2019 — Deficiency in service / unfair trade practice",
                "Indian Contract Act 1872 Section 73 — Compensation for breach of contract",
                "Code of Civil Procedure 1908 — Civil suit for recovery/damages",
                "Legal Services Authorities Act 1987 — Lok Adalat for fast resolution",
            ],
            "legal_grounds": [
                "Ground 1: Breach of contract — failure to deliver promised service/goods",
                "Ground 2: Deficiency in service under Consumer Protection Act",
                "Ground 3: Negligence causing damage — law of torts",
            ],
            "evidence_strategy": "Preserve all contracts, receipts, photos of damage, and communications. Get independent assessment of damage/loss. Send legal notice before filing.",
            "precedent_arguments": [
                "Spring Meadows Hospital v. Harjol Ahluwalia (SC 1998): Service providers are liable for negligence causing loss.",
            ],
            "compensation_calculation": "Claim: Actual loss/damage + compensation for mental harassment + litigation costs. Lok Adalat: free, fast, binding settlement. Consumer Commission: nominal filing fee.",
            "recommended_relief": "Send legal notice first. File consumer complaint at District Consumer Commission OR approach Lok Adalat for faster resolution. File civil suit for larger claims.",
            "risk_assessment": "LOW risk. Consumer forums and Lok Adalat are accessible and affordable. Most small disputes resolved within 3-6 months.",
            "immediate_action_items": [
                "Step 1: Send a legal notice to the other party demanding remedy within 15 days.",
                "Step 2: Preserve all evidence — contracts, receipts, photos, communications.",
                "Step 3: File consumer complaint at District Consumer Commission (for service/goods disputes).",
                "Step 4: Alternatively, approach Lok Adalat through DLSA for free, fast resolution.",
                "Step 5: File civil suit in Civil Court for larger claims or non-consumer disputes.",
            ],
        },
    },
    "General Legal Advice": {
        "default": {
            "applicable_acts_sections": [
                "Constitution of India — Fundamental Rights (Articles 12-35)",
                "Legal Services Authorities Act 1987 — Free legal aid for eligible persons",
                "Right to Information Act 2005 — Access to government information",
                "Limitation Act 1963 — Time limits for filing legal cases",
            ],
            "legal_grounds": [
                "Ground 1: Every citizen has the right to access justice under Article 39A",
                "Ground 2: Free legal aid available for BPL, women, SC/ST, and persons in custody",
                "Ground 3: Lok Adalat provides free, fast, binding dispute resolution",
            ],
            "evidence_strategy": "Gather all relevant documents related to your issue. Consult a lawyer or DLSA for specific advice. File RTI if government information is needed.",
            "precedent_arguments": [
                "Hussainara Khatoon v. State of Bihar (SC 1979): Right to speedy justice is a fundamental right under Article 21.",
                "M.H. Hoskot v. State of Maharashtra (SC 1978): Right to free legal aid is a fundamental right.",
            ],
            "compensation_calculation": "Depends on specific legal issue. Consult a lawyer for case-specific assessment.",
            "recommended_relief": "Consult a lawyer or visit the District Legal Services Authority (DLSA) for free legal advice. File RTI for government information. Approach appropriate forum based on your specific issue.",
            "risk_assessment": "Depends on specific legal issue. Early legal consultation improves outcomes significantly.",
            "immediate_action_items": [
                "Step 1: Visit the District Legal Services Authority (DLSA) for free legal advice.",
                "Step 2: Call NALSA helpline 15100 for immediate legal guidance.",
                "Step 3: Gather all relevant documents related to your issue.",
                "Step 4: Consult a lawyer specialising in your area of concern.",
                "Step 5: File RTI if you need government information (₹10 fee, 30-day response).",
            ],
        },
    },
}


def get_strategy_for_query(query: str, category: str, context: dict) -> dict:
    """Return the best matching strategy template for the query."""
    query_lower = query.lower()
    cat_strategies = STRATEGIES.get(category, STRATEGIES["General Legal Advice"])

    # Try to find a specific sub-type match
    chosen = None
    if category == "Family Law":
        if any(w in query_lower for w in ["divorce", "separate", "annul"]):
            chosen = cat_strategies.get("divorce")
        elif any(w in query_lower for w in ["maintenance", "alimony", "support"]):
            chosen = cat_strategies.get("maintenance")
    elif category == "Financial Disputes":
        if any(w in query_lower for w in ["cheque", "bounce", "dishonour"]):
            chosen = cat_strategies.get("cheque_bounce")

    if not chosen:
        chosen = cat_strategies.get("default", list(cat_strategies.values())[0])

    # Build the full strategy response
    case_summary = (
        f"Based on your query, this appears to be a {category} matter. "
        f"{query.strip().rstrip('.')}. "
        f"The applicable Indian laws and recommended course of action are outlined below."
    )

    return {
        "case_summary": case_summary,
        "applicable_acts_sections": chosen["applicable_acts_sections"],
        "legal_grounds": chosen["legal_grounds"],
        "evidence_strategy": chosen["evidence_strategy"],
        "precedent_arguments": chosen["precedent_arguments"],
        "compensation_calculation": chosen["compensation_calculation"],
        "recommended_relief": chosen["recommended_relief"],
        "risk_assessment": chosen["risk_assessment"],
        "immediate_action_items": chosen["immediate_action_items"],
        "disclaimer": (
            "IMPORTANT: This is AI-assisted legal analysis generated by Justicia and does NOT "
            "constitute legal advice. Please consult a qualified advocate before taking any legal "
            "action. Justicia does not guarantee any legal outcome."
        ),
    }
