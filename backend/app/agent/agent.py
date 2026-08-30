from app.agent.tools import (
    get_pipeline_summary,
    get_pipeline_by_sector,
    get_financial_summary,
    get_receivables,
    get_deal_risks,
    get_data_quality,
)

import httpx

from app.agent.prompts import SYSTEM_PROMPT
import json
import httpx

def format_currency(value):
    """Format INR values for business-friendly responses."""

    if value is None:
        return "₹0"

    crore = value / 10_000_000

    if crore >= 1:
        return f"₹{crore:.2f} Cr"

    lakh = value / 100_000

    return f"₹{lakh:.2f} L"

async def ask_llm(prompt: str, json_mode: bool = False) -> str:

    async with httpx.AsyncClient(timeout=300.0) as client:

        payload = {
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
        }

        if json_mode:
            payload["format"] = "json"

        response = await client.post(
            "http://localhost:11434/api/generate",
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]


async def classify_intent(user_message: str) -> str:

    prompt = f"""
You are an intent classifier for a Business Intelligence system.

Classify the user's question into EXACTLY ONE of these intents:

pipeline
sector
finance
receivables
risk
data_quality
management_insights
general

IMPORTANT:
- Questions about sales opportunities, sales concentration,
  opportunity distribution, or industry contribution → sector
- Questions about deals needing attention, problematic deals,
  dangerous deals, deals to watch, or deals at risk → risk
- Questions about what management should focus on, business priorities,
  major concerns, or overall business health → management_insights
- Questions about money collected, billing, order value,
  cash, or financial performance → finance
- Questions about outstanding money, unpaid amounts,
  customer dues, or receivables → receivables
- Questions about missing/incomplete/quality problems in the data
  → data_quality
- Questions about sales pipeline, open deals, or pipeline value
  → pipeline
- Questions specifically asking for breakdown by industry/sector
  → sector

Never invent information.

User question:
{user_message}

Return ONLY valid JSON:

{{"intent": "one_of_the_allowed_intents"}}
"""

    response = await ask_llm(prompt, json_mode=True)

    try:
        result = json.loads(response)
        return result.get("intent", "general")
    except json.JSONDecodeError:
        return "general"

def build_management_facts(
    pipeline,
    sectors,
    finance,
    receivables,
    risks,
    data_quality,
):
    """Build exact, preformatted business facts for the management LLM."""

    # =========================================================
    # PIPELINE
    # =========================================================

    total_deals = pipeline.get("total_deals", 0)
    open_deals = pipeline.get("open_deals", 0)
    total_pipeline = pipeline.get("total_pipeline", 0)
    weighted_pipeline = pipeline.get("weighted_pipeline", 0)

    # =========================================================
    # SECTOR CONCENTRATION
    # =========================================================

    sector_total = sum(
        float(item.get("pipeline") or 0)
        for item in sectors
    )

    largest_sector = None

    if sectors:
        largest_sector = max(
            sectors,
            key=lambda x: float(x.get("pipeline") or 0)
        )

    if largest_sector:
        largest_sector_name = (
            largest_sector.get("sector") or "Unknown"
        )

        largest_sector_value = float(
            largest_sector.get("pipeline") or 0
        )

        largest_sector_share = (
            largest_sector_value / sector_total * 100
            if sector_total > 0
            else 0
        )
    else:
        largest_sector_name = "Unknown"
        largest_sector_value = 0
        largest_sector_share = 0

    sector_lines = []

    for item in sectors[:10]:
        sector_name = item.get("sector") or "Unknown"
        sector_value = float(item.get("pipeline") or 0)

        sector_lines.append(
            f"- {sector_name}: {format_currency(sector_value)}"
        )

    # =========================================================
    # FINANCE
    # =========================================================

    total_order_value = finance.get("total_order_value", 0)
    total_billed = finance.get("total_billed", 0)
    total_collected = finance.get("total_collected", 0)
    total_receivable = finance.get("total_receivable", 0)
    total_to_be_billed = finance.get("total_to_be_billed", 0)

    billing_rate = finance.get("billing_rate_pct", 0)
    collection_rate = finance.get("collection_rate_pct", 0)

    # =========================================================
    # RECEIVABLES
    # =========================================================

    receivable_total = sum(
        float(item.get("receivable") or 0)
        for item in receivables
    )

    receivable_lines = []

    for item in receivables:
        priority = item.get("priority") or "Unknown"
        amount = float(item.get("receivable") or 0)

        receivable_lines.append(
            f"- {priority}: {format_currency(amount)}"
        )

    # =========================================================
    # DATA QUALITY
    # =========================================================

    deals_quality = data_quality.get("deals", {})
    work_orders_quality = data_quality.get("work_orders", {})

    deals_total = deals_quality.get("total_records", 0)

    missing_deal_value = deals_quality.get(
        "missing_deal_value", 0
    )

    missing_probability = deals_quality.get(
        "missing_probability", 0
    )

    missing_sector = deals_quality.get(
        "missing_sector", 0
    )

    work_orders_total = work_orders_quality.get(
        "total_records", 0
    )

    missing_amount = work_orders_quality.get(
        "missing_amount", 0
    )

    missing_billing = work_orders_quality.get(
        "missing_billing", 0
    )

    missing_collection = work_orders_quality.get(
        "missing_collection", 0
    )

    missing_value_pct = (
        missing_deal_value / deals_total * 100
        if deals_total > 0
        else 0
    )

    missing_probability_pct = (
        missing_probability / deals_total * 100
        if deals_total > 0
        else 0
    )

    missing_sector_pct = (
        missing_sector / deals_total * 100
        if deals_total > 0
        else 0
    )

    # =========================================================
    # DEAL RISKS
    # =========================================================

    sorted_risks = sorted(
        risks,
        key=lambda x: float(x.get("deal_value") or 0),
        reverse=True
    )

    risk_lines = []

    for deal in sorted_risks[:5]:

        deal_name = deal.get("deal_name") or "Unknown"

        deal_value = format_currency(
            deal.get("deal_value")
        )

        sector = deal.get("sector") or "Unknown"

        probability = deal.get("probability")

        probability = (
            str(probability)
            if probability not in [None, ""]
            else "Unknown"
        )

        reasons = deal.get("risk_reasons") or []

        reasons_text = (
            "; ".join(str(reason) for reason in reasons)
            if reasons
            else "No specific risk reason provided"
        )

        risk_lines.append(
            f"""
- Deal: {deal_name}
  Value: {deal_value}
  Sector: {sector}
  Probability: {probability}
  Risk reasons: {reasons_text}
"""
        )

    # =========================================================
    # VERIFIED FACT SHEET
    # =========================================================

    return f"""
SKYLARK BI — VERIFIED BUSINESS FACTS

IMPORTANT:
These values were calculated by the Python analytics layer.
The language model must treat them as the source of truth.

Do NOT recalculate, reinterpret, convert, or modify these values.

==================================================
PIPELINE
==================================================

Total deals: {total_deals}
Open deals: {open_deals}
Total open pipeline: {format_currency(total_pipeline)}
Weighted pipeline: {format_currency(weighted_pipeline)}

==================================================
SECTOR PIPELINE
==================================================

{chr(10).join(sector_lines)}

Largest sector: {largest_sector_name}
Largest sector pipeline: {format_currency(largest_sector_value)}
Largest sector share of open pipeline: {largest_sector_share:.1f}%

==================================================
FINANCIAL POSITION
==================================================

Total order value: {format_currency(total_order_value)}
Billed: {format_currency(total_billed)}
Collected: {format_currency(total_collected)}
Receivable: {format_currency(total_receivable)}
To be billed: {format_currency(total_to_be_billed)}
Billing rate: {billing_rate:.2f}%
Collection rate: {collection_rate:.2f}%

==================================================
RECEIVABLES
==================================================

{chr(10).join(receivable_lines)}

Total receivables from receivables breakdown:
{format_currency(receivable_total)}

==================================================
DATA QUALITY
==================================================

Deals:
Total records: {deals_total}
Missing deal values: {missing_deal_value} of {deals_total} ({missing_value_pct:.1f}%)
Missing probabilities: {missing_probability} of {deals_total} ({missing_probability_pct:.1f}%)
Missing sectors: {missing_sector} of {deals_total} ({missing_sector_pct:.1f}%)

Work orders:
Total records: {work_orders_total}
Missing amounts: {missing_amount}
Missing billing data: {missing_billing}
Missing collection data: {missing_collection}

==================================================
PRIORITY DEAL RISKS
==================================================

{chr(10).join(risk_lines)}
"""


async def get_management_insights():

    # =========================================================
    # 1. FETCH REAL DATA
    # =========================================================

    pipeline = await get_pipeline_summary()
    sectors = await get_pipeline_by_sector()
    finance = await get_financial_summary()
    receivables = await get_receivables()
    risks = await get_deal_risks()
    data_quality = await get_data_quality()

    # =========================================================
    # 2. BUILD VERIFIED FACT SHEET
    # =========================================================

    fact_sheet = build_management_facts(
        pipeline=pipeline,
        sectors=sectors,
        finance=finance,
        receivables=receivables,
        risks=risks,
        data_quality=data_quality,
    )

    # =========================================================
    # 3. MANAGEMENT LLM PROMPT
    # =========================================================

    prompt = f"""
You are Skylark BI Agent's management briefing assistant.

Your job is ONLY to summarize the verified business facts
provided below into a concise executive briefing.

The Python analytics layer is the source of truth.

==================================================
STRICT RULES
==================================================

1. NEVER change any number.

2. NEVER recalculate any number.

3. NEVER convert ₹ Cr or ₹ L into raw rupees.

4. Copy monetary values exactly as provided.

5. NEVER invent percentages.

6. NEVER invent trends.

7. NEVER invent deals.

8. NEVER invent risk reasons.

9. NEVER merge deals with the same name.

10. If a value is "Unknown", keep it "Unknown".

11. NEVER introduce USD.

12. NEVER use outside knowledge.

13. Recommendations must be based ONLY on supplied facts.

14. Missing data is a DATA QUALITY limitation.
    Do not describe missing probability as a business trend.

15. Do not claim the business is "strong", "weak",
    "healthy", "impressive", "declining", or "improving"
    unless that conclusion is directly supported by the facts.

==================================================
VERIFIED BUSINESS FACTS
==================================================

{fact_sheet}

==================================================
OUTPUT FORMAT
==================================================

Return ONLY Markdown.

Use EXACTLY these three sections.

## Key Business Observations

Give 3–5 concise bullets.

Cover the most important facts about:

- Pipeline
- Sector concentration
- Financial position
- Receivables
- Data quality

## Highest-Priority Risks

Give up to 5 bullets.

Use ONLY the supplied priority-risk deals.

For each deal include:

- Deal name
- Value
- Sector
- Probability when available
- Actual risk reasons

Do not invent or modify anything.

## Recommended Management Actions

Give 3–5 practical recommendations.

Every recommendation must be directly connected
to a verified issue in the facts.

Good examples:

- Review high-value risky deals.
- Improve missing probability information.
- Complete missing close dates when missing close dates
  are explicitly identified as a risk.
- Monitor significant sector concentration.
- Improve missing collection information.

Do NOT recommend unrelated actions.

==================================================
FINAL CHECK
==================================================

Before answering, verify:

- Numbers copied exactly
- ₹ Cr / ₹ L preserved
- No currency conversion
- No invented percentages
- No invented trends
- No invented deals
- No merged same-name deals
- Risk reasons copied exactly
- Recommendations tied to actual facts
- Exactly three sections

Return ONLY the final Markdown briefing.
"""

    answer = await ask_llm(prompt)

    return answer

async def chat(user_message: str):

    question = user_message.lower().strip()
    management_keywords = [
    "management",
    "management focus",
    "management prioritize",
    "what should we focus",
    "what should we prioritize",
    "what should we do",
    "what needs attention",
    "what requires attention",
    "business priorities",
    "business health",
    "overall business",
    "overall performance",
    "executive briefing",
    "management briefing",
    "key concerns",
    "main concerns",
]

    if any(keyword in question for keyword in management_keywords):

        answer = await get_management_insights()

        return {
            "answer": answer,
            "tools_used": [
                "get_pipeline_summary",
                "get_pipeline_by_sector",
                "get_financial_summary",
                "get_receivables",
                "get_deal_risks",
                "get_data_quality",
            ],
            "agent_mode": "llm_management",
        }


    # =========================================================
    # 1. PIPELINE BY SECTOR
    # =========================================================

    if (
        ("pipeline" in question and "sector" in question)
        or "pipeline by industry" in question
        or "which sector" in question
        or "which industry" in question
    ):

        result = await get_pipeline_by_sector()

        if not result:
            return {
                "answer": "No sector pipeline data is currently available.",
                "tools_used": ["get_pipeline_by_sector"],
                "agent_mode": "deterministic",
            }

        total = sum(
            item.get("pipeline") or 0
            for item in result
        )

        top_sector = result[0]

        share = (
            top_sector["pipeline"] / total * 100
            if total > 0
            else 0
        )

        lines = []

        for item in result[:10]:
            lines.append(
                f"• {item['sector']}: "
                f"{format_currency(item['pipeline'])}"
            )

        answer = (
            f"**Pipeline by sector**\n\n"
            + "\n".join(lines)
            + "\n\n"
            f"**Key insight:** {top_sector['sector']} "
            f"is the largest contributor at "
            f"{format_currency(top_sector['pipeline'])}, "
            f"representing approximately {share:.1f}% "
            f"of the open pipeline."
        )

        return {
            "answer": answer,
            "tools_used": ["get_pipeline_by_sector"],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 2. OVERALL PIPELINE
    # =========================================================

    if (
        "pipeline" in question
        or "deal value" in question
        or "sales value" in question
        or "sales pipeline" in question
    ):

        result = await get_pipeline_summary()

        return {
            "answer": (
                f"**Current Pipeline**\n\n"
                f"Open deals: {result['open_deals']}\n"
                f"Total pipeline: "
                f"{format_currency(result['total_pipeline'])}\n"
                f"Weighted pipeline: "
                f"{format_currency(result['weighted_pipeline'])}\n\n"
                f"The weighted pipeline represents the "
                f"probability-adjusted value of the open deals."
            ),
            "tools_used": [
                "get_pipeline_summary"
            ],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 3. FINANCE
    # =========================================================

    if (
        "billed" in question
        or "collected" in question
        or "cash" in question
        or "financial" in question
        or "finance" in question
        or "billing" in question
        or "collection" in question
    ):

        result = await get_financial_summary()

        return {
            "answer": (
                f"**Financial Position**\n\n"
                f"Total order value: "
                f"{format_currency(result['total_order_value'])}\n"
                f"Billed: "
                f"{format_currency(result['total_billed'])}\n"
                f"Collected: "
                f"{format_currency(result['total_collected'])}\n"
                f"Receivable: "
                f"{format_currency(result['total_receivable'])}\n"
                f"To be billed: "
                f"{format_currency(result['total_to_be_billed'])}\n\n"
                f"Billing rate: "
                f"{result['billing_rate_pct']:.2f}%\n"
                f"Collection rate: "
                f"{result['collection_rate_pct']:.2f}%"
            ),
            "tools_used": [
                "get_financial_summary"
            ],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 4. RECEIVABLES
    # =========================================================

    if (
        "receivable" in question
        or "receivables" in question
        or "outstanding" in question
        or "money due" in question
        or "amount due" in question
    ):

        result = await get_receivables()

        if not result:
            return {
                "answer": "No receivable data is currently available.",
                "tools_used": ["get_receivables"],
                "agent_mode": "deterministic",
            }

        total = sum(
            item.get("receivable") or 0
            for item in result
        )

        lines = []

        for item in result:
            lines.append(
                f"• {item['priority']}: "
                f"{format_currency(item['receivable'])}"
            )

        return {
            "answer": (
                f"**Receivables**\n\n"
                + "\n".join(lines)
                + "\n\n"
                f"Total receivables: "
                f"{format_currency(total)}"
            ),
            "tools_used": [
                "get_receivables"
            ],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 5. DEAL RISKS
    # =========================================================

    if (
        "risk" in question
        or "risky" in question
        or "at risk" in question
        or "problematic deals" in question
        or "deal risk" in question
    ):

        result = await get_deal_risks()

        if not result:
            return {
                "answer": "No significant deal risks were detected.",
                "tools_used": ["get_deal_risks"],
                "agent_mode": "deterministic",
            }

        lines = []

        for deal in result[:10]:

            value = format_currency(
                deal.get("deal_value")
            )

            reasons = ", ".join(
                deal.get("risk_reasons") or []
            )

            lines.append(
                f"• **{deal['deal_name']}** — {value}\n"
                f"  Probability: "
                f"{deal.get('probability') or 'Unknown'}\n"
                f"  Sector: "
                f"{deal.get('sector') or 'Unknown'}\n"
                f"  Risks: {reasons}"
            )

        return {
            "answer": (
                "**Potentially Risky Deals**\n\n"
                + "\n\n".join(lines)
            ),
            "tools_used": [
                "get_deal_risks"
            ],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 6. DATA QUALITY
    # =========================================================

    if (
        "data quality" in question
        or "missing data" in question
        or "data issue" in question
        or "data issues" in question
        or "incomplete" in question
        or "missing fields" in question
    ):

        result = await get_data_quality()

        deals = result["deals"]
        work_orders = result["work_orders"]

        return {
            "answer": (
                "**Data Quality Summary**\n\n"
                f"Deals: {deals['total_records']} records\n"
                f"• Missing deal values: "
                f"{deals['missing_deal_value']}\n"
                f"• Missing probabilities: "
                f"{deals['missing_probability']}\n"
                f"• Missing sectors: "
                f"{deals['missing_sector']}\n\n"
                f"Work orders: "
                f"{work_orders['total_records']} records\n"
                f"• Missing amounts: "
                f"{work_orders['missing_amount']}\n"
                f"• Missing billing data: "
                f"{work_orders['missing_billing']}\n"
                f"• Missing collection data: "
                f"{work_orders['missing_collection']}\n\n"
                f"**Key limitation:** "
                f"{deals['missing_probability']} deals are missing "
                f"probability, so weighted pipeline figures "
                f"should be interpreted with caution."
            ),
            "tools_used": [
                "get_data_quality"
            ],
            "agent_mode": "deterministic",
        }


    # =========================================================
    # 7. FALLBACK
    # =========================================================

        # -------------------------
    # LLM FALLBACK
    # -------------------------

        # -------------------------
    # LLM INTENT TEST
    # -------------------------

        # -------------------------
    # LLM INTENT → BI TOOL
    # -------------------------

    intent = await classify_intent(user_message)

    if intent == "pipeline":
        result = await get_pipeline_summary()

        return {
            "answer": (
                f"We currently have {result['open_deals']} open deals "
                f"with a total pipeline of "
                f"₹{result['total_pipeline']:,.2f}. "
                f"The weighted pipeline is "
                f"₹{result['weighted_pipeline']:,.2f}."
            ),
            "tools_used": ["get_pipeline_summary"],
            "agent_mode": "llm_tool"
        }

    elif intent == "sector":
        result = await get_pipeline_by_sector()

        lines = [
            f"{item['sector']}: ₹{item['pipeline']:,.2f}"
            for item in result[:10]
        ]

        return {
            "answer": (
                "Open pipeline by sector:\n\n"
                + "\n".join(lines)
            ),
            "tools_used": ["get_pipeline_by_sector"],
            "agent_mode": "llm_tool"
        }

    elif intent == "finance":
        result = await get_financial_summary()

        return {
            "answer": (
                f"Financial position:\n\n"
                f"Total order value: ₹{result['total_order_value']:,.2f}\n"
                f"Billed: ₹{result['total_billed']:,.2f}\n"
                f"Collected: ₹{result['total_collected']:,.2f}\n"
                f"Receivable: ₹{result['total_receivable']:,.2f}\n"
                f"To be billed: ₹{result['total_to_be_billed']:,.2f}\n"
                f"Billing rate: {result['billing_rate_pct']:.2f}%\n"
                f"Collection rate: {result['collection_rate_pct']:.2f}%"
            ),
            "tools_used": ["get_financial_summary"],
            "agent_mode": "llm_tool"
        }

    elif intent == "receivables":
        result = await get_receivables()

        lines = [
            f"{item['priority']}: ₹{item['receivable']:,.2f}"
            for item in result
        ]

        total = sum(item["receivable"] for item in result)

        return {
            "answer": (
                "**Receivables**\n\n"
                + "\n".join(f"• {line}" for line in lines)
                + f"\n\nTotal receivables: ₹{total:,.2f}"
            ),
            "tools_used": ["get_receivables"],
            "agent_mode": "llm_tool"
        }

    elif intent == "risk":
        result = await get_deal_risks()

        lines = []

        for deal in result[:10]:
            reasons = ", ".join(deal["risk_reasons"])

            lines.append(
                f"{deal['deal_name']} — "
                f"₹{deal['deal_value'] or 0:,.2f}\n"
                f"Reason: {reasons}"
            )

        return {
            "answer": (
                "Potentially risky open deals:\n\n"
                + "\n\n".join(lines)
            ),
            "tools_used": ["get_deal_risks"],
            "agent_mode": "llm_tool"
        }

    elif intent == "data_quality":
        result = await get_data_quality()

        deals = result["deals"]
        work_orders = result["work_orders"]

        return {
            "answer": (
                "Data quality summary:\n\n"
                f"Deals: {deals['total_records']} records\n"
                f"Missing deal values: {deals['missing_deal_value']}\n"
                f"Missing probabilities: {deals['missing_probability']}\n"
                f"Missing sectors: {deals['missing_sector']}\n\n"
                f"Work orders: {work_orders['total_records']} records\n"
                f"Missing amounts: {work_orders['missing_amount']}\n"
                f"Missing billing data: {work_orders['missing_billing']}\n"
                f"Missing collection data: {work_orders['missing_collection']}"
            ),
            "tools_used": ["get_data_quality"],
            "agent_mode": "llm_tool"
        }

        # -------------------------
    # GENERAL / MANAGEMENT
    # -------------------------

        # -------------------------
    # MANAGEMENT INSIGHTS
    # -------------------------

    if intent == "management_insights":

        answer = await get_management_insights()

        return {
            "answer": answer,
            "tools_used": [
                "get_pipeline_summary",
                "get_pipeline_by_sector",
                "get_financial_summary",
                "get_receivables",
                "get_deal_risks",
                "get_data_quality"
            ],
            "agent_mode": "llm_management"
        }

    # -------------------------
    # GENERAL
    # -------------------------

    answer = await ask_llm(user_message)

    return {
        "answer": answer,
        "tools_used": [],
        "agent_mode": "llm"
    }