import { useEffect, useState } from "react";
import {
  AlertTriangle,
  ArrowUpRight,
  BarChart3,
  Bot,
  CheckCircle2,
  ChevronRight,
  CircleDollarSign,
  Database,
  LayoutDashboard,
  RefreshCw,
  Send,
  ShieldAlert,
  Sparkles,
  Target,
  TrendingUp,
  WalletCards,
  XCircle,
} from "lucide-react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from "recharts";

const API_BASE = "http://127.0.0.1:8000";

/* =========================================================
   HELPERS
========================================================= */

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "—";
  }

  const number = Number(value);
  const crore = number / 10000000;

  if (Math.abs(crore) >= 1) {
    return `₹${crore.toFixed(2)} Cr`;
  }

  const lakh = number / 100000;

  if (Math.abs(lakh) >= 1) {
    return `₹${lakh.toFixed(2)} L`;
  }

  return `₹${number.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
  })}`;
}

function safeNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
}

/* =========================================================
   KPI CARD
========================================================= */

function StatCard({
  icon: Icon,
  label,
  value,
  description,
  accent = "neutral",
  progress,
}) {
  return (
    <div className={`stat-card ${accent}`}>
      <div className="stat-top">
        <div className="stat-icon">
          <Icon size={19} strokeWidth={2} />
        </div>

        <ArrowUpRight size={15} className="stat-arrow" />
      </div>

      <div className="stat-main">
        <p className="stat-label">{label}</p>

        <h2>{value}</h2>

        <p className="stat-description">{description}</p>
      </div>

      {progress !== undefined && (
        <div className="mini-progress">
          <div
            className="mini-progress-fill"
            style={{
              width: `${Math.min(Math.max(progress, 0), 100)}%`,
            }}
          />
        </div>
      )}
    </div>
  );
}

/* =========================================================
   SECTION HEADER
========================================================= */

function SectionHeader({
  eyebrow,
  title,
  description,
  icon: Icon,
}) {
  return (
    <div className="section-heading">
      <div>
        {eyebrow && <span className="section-eyebrow">{eyebrow}</span>}

        <h2>{title}</h2>

        {description && <p>{description}</p>}
      </div>

      {Icon && (
        <div className="section-icon">
          <Icon size={19} />
        </div>
      )}
    </div>
  );
}

/* =========================================================
   APP
========================================================= */

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const [activePage, setActivePage] = useState("overview");

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm Skylark BI Agent. Ask me about pipeline, sectors, finance, receivables, deal risks, or data quality.",
    },
  ]);

  const [sending, setSending] = useState(false);

  /* =====================================================
     LOAD DASHBOARD
  ===================================================== */

  async function loadDashboard(initial = false) {
    try {
      if (initial) {
        setLoading(true);
      } else {
        setRefreshing(true);
      }

      const response = await fetch(
        `${API_BASE}/analytics/dashboard`
      );

      if (!response.ok) {
        throw new Error("Failed to load dashboard");
      }

      const data = await response.json();

      setDashboard(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadDashboard(true);
  }, []);

  /* =====================================================
     CHAT
  ===================================================== */

  async function sendQuestion(text = question) {
    const message = text.trim();

    if (!message || sending) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    setQuestion("");
    setSending(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          tools: data.tools_used || [],
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't retrieve that information. Please check that the backend is running.",
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  /* =====================================================
     LOADING
  ===================================================== */

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-orbit">
          <div className="loading-logo">S</div>
        </div>

        <h2>Loading Skylark BI</h2>

        <p>
          Connecting to live business intelligence data...
        </p>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="loading-screen">
        <div className="loading-logo error-logo">!</div>

        <h2>Unable to load dashboard</h2>

        <p>
          Make sure the FastAPI backend is running.
        </p>

        <button
          className="primary-button"
          onClick={() => loadDashboard(true)}
        >
          <RefreshCw size={16} />
          Retry connection
        </button>
      </div>
    );
  }

  /* =====================================================
     DATA
  ===================================================== */

  const pipeline = dashboard.pipeline || {};
  const finance = dashboard.finance || {};
  const dataQuality = dashboard.data_quality || {};

  const sectors = dashboard.pipeline_by_sector || [];
  const risks = dashboard.risks || [];

  const dealsQuality = dataQuality.deals || {};
  const workOrdersQuality = dataQuality.work_orders || {};

  const totalMissingDealFields =
    safeNumber(dealsQuality.missing_deal_value) +
    safeNumber(dealsQuality.missing_probability) +
    safeNumber(dealsQuality.missing_sector);

  const totalMissingWOFields =
    safeNumber(workOrdersQuality.missing_amount) +
    safeNumber(workOrdersQuality.missing_billing) +
    safeNumber(workOrdersQuality.missing_collection) +
    safeNumber(workOrdersQuality.missing_sector);

  const sectorTotal = sectors.reduce(
    (sum, item) => sum + safeNumber(item.pipeline),
    0
  );

  const largestSector = sectors.length
  ? [...sectors].sort(
      (a, b) =>
        safeNumber(b.pipeline) - safeNumber(a.pipeline)
    )[0]
  : null;

const largestSectorShare =
  largestSector && sectorTotal > 0
    ? (safeNumber(largestSector.pipeline) / sectorTotal) * 100
    : 0;

const sortedRisks = [...risks].sort(
  (a, b) =>
    safeNumber(b.deal_value) -
    safeNumber(a.deal_value)
);

const topRisk = sortedRisks[0];

  /* =====================================================
     SIDEBAR
  ===================================================== */

  const navItems = [
    {
      id: "overview",
      label: "Overview",
      icon: LayoutDashboard,
    },
    {
      id: "pipeline",
      label: "Pipeline",
      icon: TrendingUp,
    },
    {
      id: "finance",
      label: "Finance",
      icon: CircleDollarSign,
    },
    {
      id: "risk",
      label: "Risk Intelligence",
      icon: ShieldAlert,
    },
    {
      id: "quality",
      label: "Data Quality",
      icon: Database,
    },
  ];

  return (
    <div className="app-shell">
      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">S</div>

          <div className="brand-text">
            <h1>Skylark</h1>
            <span>Business Intelligence</span>
          </div>
        </div>

        <div className="nav-label">
          WORKSPACE
        </div>

        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`nav-item ${
                  activePage === item.id ? "active" : ""
                }`}
                onClick={() => setActivePage(item.id)}
              >
                <Icon size={17} />

                <span>{item.label}</span>

                {activePage === item.id && (
                  <ChevronRight
                    size={14}
                    className="nav-arrow"
                  />
                )}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-divider" />

        <button
          className="nav-item ai-nav"
          onClick={() => {
            setActivePage("overview");

            setTimeout(() => {
              document
                .querySelector(".chat-panel")
                ?.scrollIntoView({
                  behavior: "smooth",
                });
            }, 100);
          }}
        >
          <Sparkles size={17} />
          <span>Ask Skylark AI</span>
        </button>

        <div className="sidebar-bottom">
          <div className="live-card">
            <span className="live-dot" />

            <div>
              <strong>Live data</strong>
              <small>Monday.com connected</small>
            </div>
          </div>
        </div>
      </aside>

      {/* =================================================
          MAIN
      ================================================= */}

      <main className="main-content">
        {/* TOPBAR */}

        <header className="topbar">
          <div>
            <div className="breadcrumb">
              Skylark BI
              <ChevronRight size={12} />
              Executive Dashboard
            </div>

            <h1>
              {activePage === "overview" &&
                "Executive Overview"}

              {activePage === "pipeline" &&
                "Pipeline Intelligence"}

              {activePage === "finance" &&
                "Financial Position"}

              {activePage === "risk" &&
                "Risk Intelligence"}

              {activePage === "quality" &&
                "Data Quality"}
            </h1>

            <p>
              Real-time visibility into deals,
              work orders and cash flow.
            </p>
          </div>

          <div className="topbar-actions">
            <div className="live-pill">
              <span />
              Live
            </div>

            <button
              className="refresh-button"
              onClick={() => loadDashboard(false)}
              disabled={refreshing}
            >
              <RefreshCw
                size={16}
                className={
                  refreshing ? "spin" : ""
                }
              />

              {refreshing
                ? "Refreshing"
                : "Refresh data"}
            </button>
          </div>
        </header>

        {/* =================================================
            OVERVIEW
        ================================================= */}

        {activePage === "overview" && (
          <>
            {/* KPI */}

            <section className="stats-grid">
              <StatCard
                icon={TrendingUp}
                label="Open Pipeline"
                value={formatCurrency(
                  pipeline.total_pipeline
                )}
                description={`${safeNumber(
                  pipeline.open_deals
                )} open deals`}
                accent="blue"
              />

              <StatCard
                icon={Target}
                label="Weighted Pipeline"
                value={formatCurrency(
                  pipeline.weighted_pipeline
                )}
                description="Probability-adjusted value"
                accent="purple"
              />

              <StatCard
                icon={WalletCards}
                label="Billed"
                value={formatCurrency(
                  finance.total_billed
                )}
                description={`${finance.billing_rate_pct ?? 0}% billing rate`}
                progress={safeNumber(
                  finance.billing_rate_pct
                )}
                accent="green"
              />

              <StatCard
                icon={CircleDollarSign}
                label="Receivable"
                value={formatCurrency(
                  finance.total_receivable
                )}
                description={`${finance.collection_rate_pct ?? 0}% collection rate`}
                progress={safeNumber(
                  finance.collection_rate_pct
                )}
                accent="orange"
              />
            </section>

            {/* EXECUTIVE SNAPSHOT */}

            <section className="executive-strip">
              <div className="snapshot-title">
                <Sparkles size={17} />
                <div>
                  <strong>Executive Snapshot</strong>
                  <span>
                    Verified business signals
                  </span>
                </div>
              </div>

              <div className="snapshot-item">
                <span>Deals</span>
                <strong>
                  {safeNumber(pipeline.total_deals)}
                </strong>
              </div>

              <div className="snapshot-item">
                <span>Largest sector</span>
                <strong>
                  {largestSector?.sector || "—"}
                </strong>
              </div>

              <div className="snapshot-item">
                <span>Sector concentration</span>
                <strong>
                  {largestSector
                    ? `${largestSectorShare.toFixed(1)}%`
                    : "—"}
                </strong>
              </div>

              <div className="snapshot-item">
                <span>Risk entries</span>
                <strong>{risks.length}</strong>
              </div>
            </section>

            {/* CHART + FINANCE */}

            <section className="dashboard-grid">
              <div className="panel chart-panel">
                <div className="panel-header">
                  <div>
                    <span className="panel-eyebrow">
                      PIPELINE
                    </span>

                    <h3>Pipeline by Sector</h3>

                    <p>
                      Current open pipeline distribution
                    </p>
                  </div>

                  <div className="header-icon">
                    <TrendingUp size={18} />
                  </div>
                </div>

                <div className="chart-container">
                  {sectors.length > 0 ? (
                    <ResponsiveContainer
                      width="100%"
                      height={320}
                    >
                      <BarChart
                        data={sectors.slice(0, 10)}
                        layout="vertical"
                        margin={{
                          top: 5,
                          right: 25,
                          left: 10,
                          bottom: 5,
                        }}
                      >
                        <XAxis
                          type="number"
                          tickFormatter={(value) =>
                            `₹${(
                              value / 10000000
                            ).toFixed(0)}Cr`
                          }
                          fontSize={10}
                          axisLine={false}
                          tickLine={false}
                        />

                        <YAxis
                          dataKey="sector"
                          type="category"
                          width={110}
                          fontSize={10}
                          axisLine={false}
                          tickLine={false}
                        />

                        <Tooltip
                          cursor={{
                            fill: "#f5f7fa",
                          }}
                          formatter={(value) => [
                            formatCurrency(value),
                            "Pipeline",
                          ]}
                        />

                        <Bar
                          dataKey="pipeline"
                          radius={[
                            0,
                            6,
                            6,
                            0,
                          ]}
                          barSize={22}
                        >
                          {sectors
                            .slice(0, 10)
                            .map((_, index) => (
                              <Cell
                                key={index}
                                fill={
                                  index === 0
                                    ? "#202838"
                                    : "#aeb7c8"
                                }
                              />
                            ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <EmptyState text="No sector data available." />
                  )}
                </div>
              </div>

              <FinancePanel finance={finance} />
            </section>

            {/* LOWER */}

            <section className="dashboard-grid lower-grid">
              <RiskPanel
                risks={sortedRisks}
                compact
              />

              <QualityPanel
                dataQuality={dataQuality}
                totalMissingDealFields={
                  totalMissingDealFields
                }
                totalMissingWOFields={
                  totalMissingWOFields
                }
              />
            </section>

            {/* AI */}

            <ChatPanel
              messages={messages}
              question={question}
              setQuestion={setQuestion}
              sending={sending}
              sendQuestion={sendQuestion}
            />
          </>
        )}

        {/* =================================================
            PIPELINE PAGE
        ================================================= */}

        {activePage === "pipeline" && (
          <PipelinePage
            pipeline={pipeline}
            sectors={sectors}
            largestSector={largestSector}
            largestSectorShare={largestSectorShare}
          />
        )}

        {/* =================================================
            FINANCE PAGE
        ================================================= */}

        {activePage === "finance" && (
          <FinancePage finance={finance} />
        )}

        {/* =================================================
            RISK PAGE
        ================================================= */}

        {activePage === "risk" && (
          <RiskPage risks={sortedRisks} />
        )}

        {/* =================================================
            QUALITY PAGE
        ================================================= */}

        {activePage === "quality" && (
          <QualityPage
            dataQuality={dataQuality}
            totalMissingDealFields={
              totalMissingDealFields
            }
            totalMissingWOFields={
              totalMissingWOFields
            }
          />
        )}
      </main>
    </div>
  );
}

/* =========================================================
   FINANCE PANEL
========================================================= */

function FinancePanel({ finance }) {
  const billing = safeNumber(
    finance.billing_rate_pct
  );

  const collection = safeNumber(
    finance.collection_rate_pct
  );

  return (
    <div className="panel finance-panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            FINANCIAL POSITION
          </span>

          <h3>Cash & Billing</h3>

          <p>
            Work order billing and collection
          </p>
        </div>

        <div className="header-icon">
          <CircleDollarSign size={18} />
        </div>
      </div>

      <div className="finance-body">
        <div className="finance-highlight">
          <span>Total order value</span>

          <strong>
            {formatCurrency(
              finance.total_order_value
            )}
          </strong>
        </div>

        <FinanceRow
          label="Billed"
          value={finance.total_billed}
        />

        <FinanceRow
          label="Collected"
          value={finance.total_collected}
        />

        <FinanceRow
          label="Receivable"
          value={finance.total_receivable}
          warning
        />

        <FinanceRow
          label="To be billed"
          value={finance.total_to_be_billed}
        />

        <div className="finance-progress-block">
          <div className="progress-heading">
            <span>Billing progress</span>
            <strong>{billing.toFixed(2)}%</strong>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${billing}%` }}
            />
          </div>
        </div>

        <div className="finance-progress-block">
          <div className="progress-heading">
            <span>Collection progress</span>
            <strong>
              {collection.toFixed(2)}%
            </strong>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill collection"
              style={{
                width: `${collection}%`,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function FinanceRow({ label, value, warning }) {
  return (
    <div className="finance-row">
      <span>{label}</span>

      <strong className={warning ? "warning-value" : ""}>
        {formatCurrency(value)}
      </strong>
    </div>
  );
}

/* =========================================================
   RISK PANEL
========================================================= */

function RiskPanel({ risks, compact = false }) {
  const displayed = compact
    ? risks.slice(0, 6)
    : risks;

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            RISK INTELLIGENCE
          </span>

          <h3>Priority Deal Risks</h3>

          <p>
            Deals requiring management attention
          </p>
        </div>

        <div className="header-icon risk-header">
          <ShieldAlert size={18} />
        </div>
      </div>

      <div className="risk-list">
        {displayed.length === 0 ? (
          <EmptyState text="No risk entries available." />
        ) : (
          displayed.map((risk, index) => {
            const probability =
              String(
                risk.probability || ""
              ).toLowerCase();

            const severity =
              probability === "low"
                ? "high"
                : probability === "medium"
                ? "medium"
                : "unknown";

            return (
              <div
                className="risk-row"
                key={`${
                  risk.deal_id || risk.deal_name
                }-${index}`}
              >
                <div
                  className={`risk-icon ${severity}`}
                >
                  <AlertTriangle size={15} />
                </div>

                <div className="risk-info">
                  <strong>
                    {risk.deal_name || "Unknown deal"}
                  </strong>

                  <span>
                    {risk.sector ||
                      "Unknown sector"}
                    {" · "}
                    {formatCurrency(
                      risk.deal_value
                    )}
                  </span>
                </div>

                <div
                  className={`risk-badge ${severity}`}
                >
                  {risk.probability ||
                    "Unknown"}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

/* =========================================================
   QUALITY PANEL
========================================================= */

function QualityPanel({
  dataQuality,
  totalMissingDealFields,
  totalMissingWOFields,
}) {
  const deals = dataQuality.deals || {};
  const workOrders =
    dataQuality.work_orders || {};

  const totalRecords = safeNumber(
    deals.total_records
  );

  const missingPercentage =
    totalRecords > 0
      ? Math.min(
          (totalMissingDealFields /
            (totalRecords * 3)) *
            100,
          100
        )
      : 0;

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            DATA QUALITY
          </span>

          <h3>Completeness Signals</h3>

          <p>
            Missing fields detected in source data
          </p>
        </div>

        <div className="header-icon">
          <Database size={18} />
        </div>
      </div>

      <div className="quality-body">
        <div className="quality-hero">
          <div className="quality-score">
            {totalMissingDealFields}
          </div>

          <div>
            <strong>
              Deal fields missing
            </strong>

            <span>
              Across {totalRecords} deal records
            </span>
          </div>
        </div>

        <div className="quality-progress">
          <div className="progress-heading">
            <span>Missing-field ratio</span>

            <strong>
              {missingPercentage.toFixed(1)}%
            </strong>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill warning"
              style={{
                width: `${missingPercentage}%`,
              }}
            />
          </div>
        </div>

        <QualityItem
          label="Missing deal value"
          value={deals.missing_deal_value}
        />

        <QualityItem
          label="Missing probability"
          value={deals.missing_probability}
        />

        <QualityItem
          label="Missing sector"
          value={deals.missing_sector}
        />

        <QualityItem
          label="WO missing collection"
          value={workOrders.missing_collection}
        />

        <div className="quality-footer">
          {totalMissingWOFields} work-order
          field gaps detected
        </div>
      </div>
    </div>
  );
}

function QualityItem({ label, value }) {
  const count = safeNumber(value);

  return (
    <div className="quality-item">
      <span>{label}</span>

      <strong
        className={
          count > 0
            ? "quality-warning"
            : "quality-good"
        }
      >
        {count}
      </strong>
    </div>
  );
}

/* =========================================================
   CHAT
========================================================= */

function ChatPanel({
  messages,
  question,
  setQuestion,
  sending,
  sendQuestion,
}) {
  const suggestions = [
    "What is our current pipeline?",
    "Which sectors have the largest pipeline?",
    "How much money is billed, collected and receivable?",
    "What are our biggest deal risks?",
    "What data quality problems should I know about?",
  ];

  return (
    <section className="panel chat-panel">
      <div className="panel-header">
        <div className="panel-title">
          <div className="agent-icon">
            <Bot size={19} />
          </div>

          <div>
            <span className="panel-eyebrow">
              AI ASSISTANT
            </span>

            <h3>Ask Skylark BI</h3>

            <p>
              Conversational access to verified
              business data
            </p>
          </div>
        </div>

        <span className="agent-badge">
          <span />
          GROUNDED AI
        </span>
      </div>

      <div className="messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role}`}
          >
            {message.role === "assistant" && (
              <div className="message-avatar">
                <Bot size={14} />
              </div>
            )}

            <div className="message-content">
              {message.content}

              {message.tools?.length > 0 && (
                <div className="tool-used">
                  <Database size={10} />
                  Data source:{" "}
                  {message.tools.join(", ")}
                </div>
              )}
            </div>
          </div>
        ))}

        {sending && (
          <div className="message assistant">
            <div className="message-avatar">
              <Bot size={14} />
            </div>

            <div className="message-content typing">
              <span />
              <span />
              <span />
              Analyzing verified business data...
            </div>
          </div>
        )}
      </div>

      <div className="suggestions">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() =>
              sendQuestion(suggestion)
            }
          >
            {suggestion}
          </button>
        ))}
      </div>

      <div className="chat-input">
        <Bot size={17} />

        <input
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              sendQuestion();
            }
          }}
          placeholder="Ask a business question..."
        />

        <button
          onClick={() => sendQuestion()}
          disabled={
            sending || !question.trim()
          }
        >
          <Send size={17} />
        </button>
      </div>
    </section>
  );
}

/* =========================================================
   PIPELINE PAGE
========================================================= */

function PipelinePage({
  pipeline,
  sectors,
  largestSector,
  largestSectorShare,
}) {
  return (
    <div className="page-stack">
      <section className="stats-grid">
        <StatCard
          icon={TrendingUp}
          label="Total Deals"
          value={safeNumber(
            pipeline.total_deals
          ).toLocaleString()}
          description="All deals in pipeline"
          accent="blue"
        />

        <StatCard
          icon={Target}
          label="Open Deals"
          value={safeNumber(
            pipeline.open_deals
          ).toLocaleString()}
          description="Currently open"
          accent="purple"
        />

        <StatCard
          icon={BarChart3}
          label="Open Pipeline"
          value={formatCurrency(
            pipeline.total_pipeline
          )}
          description="Current open value"
          accent="green"
        />

        <StatCard
          icon={Sparkles}
          label="Weighted Pipeline"
          value={formatCurrency(
            pipeline.weighted_pipeline
          )}
          description="Probability-adjusted"
          accent="orange"
        />
      </section>

      <div className="insight-banner">
        <div className="insight-banner-icon">
          <TrendingUp size={20} />
        </div>

        <div>
          <strong>
            {largestSector?.sector ||
              "No sector data"}
          </strong>

          <p>
            is the largest sector by pipeline,
            representing{" "}
            <strong>
              {largestSector
                ? `${largestSectorShare.toFixed(
                    1
                  )}%`
                : "0%"}
            </strong>{" "}
            of the sector pipeline.
          </p>
        </div>
      </div>

      <div className="panel large-chart">
        <SectionHeader
          eyebrow="PIPELINE COMPOSITION"
          title="Sector Pipeline"
          description="Open pipeline value across sectors"
          icon={BarChart3}
        />

        <div className="chart-container tall">
          <ResponsiveContainer
            width="100%"
            height={450}
          >
            <BarChart
              data={sectors}
              layout="vertical"
              margin={{
                top: 10,
                right: 35,
                left: 15,
                bottom: 10,
              }}
            >
              <XAxis
                type="number"
                tickFormatter={(value) =>
                  `₹${(
                    value / 10000000
                  ).toFixed(0)}Cr`
                }
                axisLine={false}
                tickLine={false}
                fontSize={10}
              />

              <YAxis
                dataKey="sector"
                type="category"
                width={130}
                axisLine={false}
                tickLine={false}
                fontSize={11}
              />

              <Tooltip
                formatter={(value) => [
                  formatCurrency(value),
                  "Pipeline",
                ]}
              />

              <Bar
                dataKey="pipeline"
                radius={[0, 7, 7, 0]}
                barSize={25}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   FINANCE PAGE
========================================================= */

function FinancePage({ finance }) {
  const billing = safeNumber(
    finance.billing_rate_pct
  );

  const collection = safeNumber(
    finance.collection_rate_pct
  );

  const chartData = [
    {
      name: "Billed",
      value: safeNumber(
        finance.total_billed
      ),
    },
    {
      name: "To be billed",
      value: safeNumber(
        finance.total_to_be_billed
      ),
    },
  ];

  return (
    <div className="page-stack">
      <section className="stats-grid">
        <StatCard
          icon={WalletCards}
          label="Order Value"
          value={formatCurrency(
            finance.total_order_value
          )}
          description="Total work order value"
          accent="blue"
        />

        <StatCard
          icon={CircleDollarSign}
          label="Billed"
          value={formatCurrency(
            finance.total_billed
          )}
          description={`${billing.toFixed(
            2
          )}% billing rate`}
          progress={billing}
          accent="green"
        />

        <StatCard
          icon={CheckCircle2}
          label="Collected"
          value={formatCurrency(
            finance.total_collected
          )}
          description={`${collection.toFixed(
            2
          )}% collection rate`}
          progress={collection}
          accent="purple"
        />

        <StatCard
          icon={AlertTriangle}
          label="Receivable"
          value={formatCurrency(
            finance.total_receivable
          )}
          description="Currently outstanding"
          accent="orange"
        />
      </section>

      <section className="dashboard-grid">
        <FinancePanel finance={finance} />

        <div className="panel finance-visual">
          <SectionHeader
            eyebrow="BILLING MIX"
            title="Order Value Progress"
            description="Billed versus remaining value"
            icon={CircleDollarSign}
          />

          <div className="donut-container">
            <ResponsiveContainer
              width="100%"
              height={270}
            >
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={75}
                  outerRadius={105}
                  paddingAngle={4}
                >
                  {chartData.map((_, index) => (
                    <Cell
                      key={index}
                      fill={
                        index === 0
                          ? "#202838"
                          : "#dfe3ea"
                      }
                    />
                  ))}
                </Pie>

                <Tooltip
                  formatter={(value) =>
                    formatCurrency(value)
                  }
                />
              </PieChart>
            </ResponsiveContainer>

            <div className="donut-center">
              <strong>
                {billing.toFixed(1)}%
              </strong>

              <span>Billed</span>
            </div>
          </div>

          <div className="legend">
            <div>
              <span className="legend-dot dark" />
              Billed
            </div>

            <div>
              <span className="legend-dot light" />
              To be billed
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

/* =========================================================
   RISK PAGE
========================================================= */

function RiskPage({ risks }) {
  return (
    <div className="page-stack">
      <div className="insight-banner risk-banner">
        <div className="insight-banner-icon">
          <ShieldAlert size={20} />
        </div>

        <div>
          <strong>
            {risks.length} risk entries identified
          </strong>

          <p>
            Review the highest-value entries first.
            Risk reasons below are taken directly
            from the business data.
          </p>
        </div>
      </div>

      <RiskPanel risks={risks} />

      <div className="panel">
        <SectionHeader
          eyebrow="RISK DETAILS"
          title="Deal Risk Register"
          description="Verified risk information from the analytics layer"
          icon={AlertTriangle}
        />

        <div className="risk-table">
          <div className="risk-table-header">
            <span>Deal</span>
            <span>Value</span>
            <span>Sector</span>
            <span>Probability</span>
            <span>Risk reasons</span>
          </div>

          {risks.map((risk, index) => (
            <div
              className="risk-table-row"
              key={`table-${index}`}
            >
              <strong>
                {risk.deal_name || "Unknown"}
              </strong>

              <span>
                {formatCurrency(
                  risk.deal_value
                )}
              </span>

              <span>
                {risk.sector || "Unknown"}
              </span>

              <span>
                <span
                  className={`probability ${
                    String(
                      risk.probability || ""
                    ).toLowerCase()
                  }`}
                >
                  {risk.probability ||
                    "Unknown"}
                </span>
              </span>

              <span>
                {risk.risk_reasons?.length
                  ? risk.risk_reasons.join(", ")
                  : "No specific risk reason provided"}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   QUALITY PAGE
========================================================= */

function QualityPage({
  dataQuality,
  totalMissingDealFields,
  totalMissingWOFields,
}) {
  return (
    <div className="page-stack">
      <div className="quality-overview-grid">
        <div className="quality-big-card">
          <div className="quality-big-icon">
            <Database size={22} />
          </div>

          <span>Total deal field gaps</span>

          <strong>
            {totalMissingDealFields}
          </strong>

          <small>
            Across the available deal records
          </small>
        </div>

        <div className="quality-big-card">
          <div className="quality-big-icon">
            <Database size={22} />
          </div>

          <span>Work-order field gaps</span>

          <strong>
            {totalMissingWOFields}
          </strong>

          <small>
            Missing fields detected in work orders
          </small>
        </div>
      </div>

      <div className="dashboard-grid">
        <QualityPanel
          dataQuality={dataQuality}
          totalMissingDealFields={
            totalMissingDealFields
          }
          totalMissingWOFields={
            totalMissingWOFields
          }
        />

        <div className="panel quality-guidance">
          <SectionHeader
            eyebrow="MANAGEMENT VIEW"
            title="What to watch"
            description="Areas where data completeness can affect analysis"
            icon={ShieldAlert}
          />

          <div className="guidance-item">
            <div className="guidance-icon">
              <XCircle size={16} />
            </div>

            <div>
              <strong>Deal values</strong>
              <p>
                Missing deal values can limit
                pipeline-value analysis.
              </p>
            </div>
          </div>

          <div className="guidance-item">
            <div className="guidance-icon">
              <XCircle size={16} />
            </div>

            <div>
              <strong>Probability</strong>
              <p>
                Missing probability information
                limits weighted pipeline analysis.
              </p>
            </div>
          </div>

          <div className="guidance-item">
            <div className="guidance-icon">
              <XCircle size={16} />
            </div>

            <div>
              <strong>Collection data</strong>
              <p>
                Missing collection information can
                affect cash-flow visibility.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   SMALL COMPONENTS
========================================================= */

function QualityItemSimple() {
  return null;
}

function EmptyState({ text }) {
  return (
    <div className="empty-state">
      <Database size={22} />
      <span>{text}</span>
    </div>
  );
}

export default App;