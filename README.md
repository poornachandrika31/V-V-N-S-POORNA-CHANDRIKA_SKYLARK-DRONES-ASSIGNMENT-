````markdown
# Skylark BI Agent

> **AI-powered Business Intelligence platform for turning operational data into actionable executive insights.**

Skylark BI Agent is a full-stack Business Intelligence application that combines **live business data, analytics, risk intelligence, financial insights, data-quality monitoring, and a grounded AI assistant** into a single executive dashboard.

Instead of manually navigating spreadsheets and dashboards, users can ask natural-language questions such as:

- *What is our current pipeline?*
- *Which sectors have the largest pipeline?*
- *How much money is currently receivable?*
- *What are our biggest deal risks?*
- *Why is a particular deal considered risky?*
- *What is our billing and collection rate?*

Skylark retrieves the relevant business data through its analytics layer and provides concise, decision-oriented answers.

---

✨ Key Highlights

| Capability | Description |
|---|---|
| 📊 **Executive Dashboard** | High-level view of pipeline, weighted pipeline, billing, collections and receivables |
| 📈 **Pipeline Intelligence** | Analyze open deals and pipeline distribution across sectors |
| 💰 **Financial Intelligence** | Track order value, billing, collections, receivables and remaining billing |
| ⚠️ **Risk Intelligence** | Identify potentially risky deals using probability and deal metadata |
| 🧹 **Data Quality Monitoring** | Surface missing fields and data-completeness issues |
| 🤖 **Grounded AI Assistant** | Ask business questions using natural language |
| 🔗 **Monday.com Integration** | Connect business data from Monday.com |
| 🔄 **Live Data Refresh** | Refresh analytics directly from the backend |
| 🖥️ **Modern Web Interface** | Responsive React-based executive dashboard |

---

🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      User / Exec     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │                      │
                         │  Executive Dashboard │
                         │  Pipeline Intelligence│
                         │  Financial Position  │
                         │  Risk Intelligence   │
                         │  Data Quality        │
                         │  AI Assistant        │
                         └──────────┬───────────┘
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │                      │
                         │ /analytics/dashboard │
                         │ /chat                │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │ Analytics  │  │ AI Agent   │  │  Monday    │
             │   Layer    │  │   Layer    │  │  Client    │
             └────────────┘  └────────────┘  └────────────┘
                    │               │               │
                    ▼               ▼               ▼
             Pipeline / Finance   Planner /      Business
             Risk / Operations    Tools /        Data
             Data Quality         Schemas
````

---

# 🎯 Problem

Business teams often have valuable operational data spread across multiple sources.

Although the data exists, answering basic management questions can still require:

* manually inspecting records
* calculating financial metrics
* filtering deals
* identifying risky opportunities
* checking data completeness
* navigating multiple systems

This creates unnecessary friction between **raw business data and management decisions**.

Skylark addresses this by providing a unified intelligence layer that converts operational data into:

**Data → Analytics → Insights → Decisions**

---

# 💡 Solution

Skylark provides a single interface where executives and business users can:

### 1. Monitor business performance

The executive dashboard surfaces:

* Open pipeline
* Weighted pipeline
* Total deals
* Billing progress
* Collection progress
* Receivables
* Sector concentration

### 2. Understand financial position

Users can quickly inspect:

* Total order value
* Billed amount
* Collected amount
* Receivable amount
* Amount yet to be billed
* Billing rate
* Collection rate

### 3. Identify deal risks

The Risk Intelligence module highlights deals with signals such as:

* Low closure probability
* Missing close dates
* Early sales stages
* Unknown probability
* Other risk indicators returned by the analytics layer

### 4. Monitor data quality

Skylark identifies missing business fields that may affect analytical reliability.

Examples include:

* Missing deal values
* Missing probabilities
* Missing sectors
* Missing work-order collection information

### 5. Ask questions naturally

Instead of navigating through multiple screens, users can ask:

> "How much money is currently receivable?"

or:

> "Which deal is the biggest risk?"

The AI assistant retrieves the relevant information from the business intelligence layer and presents the result conversationally.

---

# 🤖 AI Assistant

The Skylark AI Assistant is designed around **grounded business intelligence** rather than unrestricted conversational generation.

The assistant can use the application's analytics tools to retrieve relevant information before generating an answer.

### Example

**User**

> Which deal is the biggest risk?

**Skylark**

> Sakura — ₹30.59 Cr
> Probability: Low
> Sector: Tender
> Risks: Low closure probability, close date is missing.

This approach helps keep responses tied to the underlying business data.

---

# 📊 Analytics Modules

## Pipeline Intelligence

Provides visibility into:

* Total deals
* Open deals
* Open pipeline
* Weighted pipeline
* Pipeline by sector
* Sector concentration

The weighted pipeline provides a probability-adjusted view of potential business value.

---

## Financial Intelligence

Tracks the movement from order value to cash collection:

```text
Total Order Value
       │
       ▼
     Billed
       │
       ▼
   Collected
```

While also highlighting:

```text
Receivable
To Be Billed
```

Key metrics include:

* Billing Rate
* Collection Rate
* Receivables
* Billed Value
* Collected Value
* Remaining Billing Value

---

## Risk Intelligence

The risk engine surfaces deals that require management attention.

Risk signals can include:

```text
Low Probability
      +
Missing Close Date
      +
Early Sales Stage
      ↓
Potentially Risky Deal
```

The dashboard ranks risk entries so that high-value opportunities can be reviewed first.

---

## Data Quality

Reliable analytics depends on reliable source data.

The Data Quality module surfaces missing fields and provides visibility into potential gaps affecting:

* Pipeline analysis
* Weighted forecasting
* Sector analysis
* Cash-flow visibility
* Work-order analytics

---

# 🖥️ Application Screens

### Executive Overview

The main dashboard provides an executive-level snapshot of the business.

It combines:

* KPI cards
* Pipeline visualization
* Financial position
* Risk intelligence
* Data-quality signals
* AI assistant

### Pipeline Intelligence

Visualizes the distribution of open pipeline across business sectors.

### Financial Position

Provides a detailed view of billing, collections and outstanding receivables.

### Risk Intelligence

Provides a prioritized deal-risk register with supporting risk reasons.

### Data Quality

Highlights missing fields that may reduce analytical confidence.

---

# 🛠️ Technology Stack

## Frontend

* **React**
* **Vite**
* **JavaScript**
* **Recharts**
* **Lucide React**
* CSS

## Backend

* **Python**
* **FastAPI**
* REST APIs
* Modular analytics services

## AI / Agent Layer

* AI agent architecture
* Tool-based business intelligence retrieval
* Structured schemas
* Prompt-driven reasoning
* Grounded responses

## Data & Integration

* Monday.com integration
* Business analytics layer
* Pipeline analytics
* Financial analytics
* Risk analytics
* Data-quality analytics

---

# 📁 Project Structure

```text
skylark-bi-agent/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── agent.py
│   │   │   ├── planner.py
│   │   │   ├── prompts.py
│   │   │   ├── schemas.py
│   │   │   └── tools.py
│   │   │
│   │   ├── analytics/
│   │   │   ├── finance.py
│   │   │   ├── operations.py
│   │   │   ├── pipeline.py
│   │   │   ├── risk.py
│   │   │   └── service.py
│   │   │
│   │   ├── data/
│   │   │   ├── data_quality.py
│   │   │   └── normalizer.py
│   │   │
│   │   ├── monday/
│   │   │   └── client.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── DataQuality.jsx
│   │   │   ├── Finance.jsx
│   │   │   ├── Overview.jsx
│   │   │   ├── Pipeline.jsx
│   │   │   └── Risk.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── docs/
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Make sure you have installed:

* Python 3.10+
* Node.js 18+
* npm
* Git

---

# 1. Clone the Repository

```bash
git clone https://github.com/poornachandrika31/V-V-N-S-POORNA-CHANDRIKA_SKYLARK-DRONES-ASSIGNMENT-.git

cd V-V-N-S-POORNA-CHANDRIKA_SKYLARK-DRONES-ASSIGNMENT-
```

---

# 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 3. Configure Environment Variables

Create a `.env` file inside `backend/`.

Add the required configuration values for the business-data integration and AI services.

> **Never commit `.env` or API keys to GitHub.**

---

# 4. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 5. Start the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will provide the local frontend URL in the terminal.

---

# 🔌 API Overview

The frontend communicates with the FastAPI backend through REST endpoints.

### Dashboard

```http
GET /analytics/dashboard
```

Returns the consolidated analytics required by the executive dashboard.

The response contains information such as:

```text
pipeline
finance
pipeline_by_sector
risks
data_quality
```

### AI Chat

```http
POST /chat
```

Example request:

```json
{
  "message": "What is our current receivable?"
}
```

The backend processes the request through the AI/analytics layer and returns the grounded answer.

---

# 📌 Example Business Questions

Skylark can answer questions such as:

### Pipeline

```text
What is our current pipeline?
```

```text
Which sectors have the largest pipeline?
```

```text
What is our weighted pipeline?
```

### Finance

```text
What is our billing rate?
```

```text
How much money is currently receivable?
```

```text
How much has been collected?
```

### Risk

```text
Show me risky deals.
```

```text
Which deal is the biggest risk?
```

```text
Why is Sakura considered risky?
```

### Data Quality

```text
What data quality problems should I know about?
```

---

# 🔐 Security Considerations

Sensitive configuration should be stored through environment variables.

The repository intentionally excludes:

```text
.env
venv/
.venv/
node_modules/
dist/
```

API keys, authentication credentials and private integration tokens should never be committed to source control.

---

# 📈 Design Philosophy

Skylark is designed around three principles:

### 01 — Clarity

Executives should understand the business situation within seconds.

### 02 — Actionability

The dashboard should highlight what requires attention, not simply display raw numbers.

### 03 — Trust

AI responses should be grounded in actual business data and analytics rather than unsupported assumptions.

---

# 🔄 Data Flow

```text
Business Data
     │
     ▼
Monday.com / Data Sources
     │
     ▼
Normalization
     │
     ▼
Analytics Services
 ┌───┼────┬──────┐
 ▼   ▼    ▼      ▼
Pipeline Finance Risk  Data Quality
 └───┼────┴──────┘
     ▼
AI Agent / API
     │
     ▼
React Dashboard
     │
     ▼
Executive Decision
```

---

# 🌟 Why Skylark?

Traditional BI dashboards answer:

> **"What happened?"**

Skylark aims to go one step further:

> **"What is happening, why does it matter, and what should I look at next?"**

By combining structured analytics with a grounded conversational interface, Skylark creates a more accessible way for business users to interact with operational data.

---

# 📚 Project Context

**Project:** Skylark BI Agent
**Organization:** Skylark Drones
**Application Type:** AI-powered Business Intelligence Platform
**Architecture:** Full-stack React + FastAPI application

---

# 👩‍💻 Author

**V. V. N. S. Poorna Chandrika**

Computer Science & Artificial Intelligence

---

## ⭐ Acknowledgements

Built as part of the **Skylark Drones assignment** with a focus on business intelligence, analytics, AI-assisted decision support and full-stack application development.

---

> **Skylark BI Agent — From business data to better decisions.**

````

