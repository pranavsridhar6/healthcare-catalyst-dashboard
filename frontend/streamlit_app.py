import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
import sys
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ensure project root is on path so `config` package is always importable
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import categories

st.set_page_config(layout="wide")

# -----------------------
# Theme / CSS
# -----------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

    .stApp {
        font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
        background:
            radial-gradient(circle at 20% 0%, rgba(14, 165, 233, 0.18), transparent 30%),
            radial-gradient(circle at 85% 10%, rgba(16, 185, 129, 0.12), transparent 35%),
            linear-gradient(160deg, #050913 0%, #091326 45%, #0b1b33 100%);
        color: #f8fafc;
    }
    .block-container {
        padding-top: 1.25rem;
        max-width: 98%;
    }
    .header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: 0.01em;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.45);
    }
    .panel-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .watch-card {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.7));
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 0.55rem 0.65rem;
        margin-bottom: 0.45rem;
    }
    .watch-meta {
        font-size: 0.8rem;
        color: #cbd5e1;
        display: flex;
        justify-content: space-between;
        margin-top: 0.2rem;
    }
    .good { color: #34d399; font-weight: 700; }
    .bad { color: #fb7185; font-weight: 700; }
    .neutral { color: #fbbf24; font-weight: 700; }
    .muted { color: #94a3b8; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.8);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 10px;
        font-weight: 600;
        padding: 0.32rem 0.8rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #0ea5e9, #22c55e);
        color: #041421;
        border-color: transparent;
        box-shadow: 0 0 18px rgba(14, 165, 233, 0.35);
    }

    [data-testid="stMetric"] {
        background: rgba(10, 17, 32, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        padding: 0.55rem 0.7rem;
    }
    [data-testid="stMetricLabel"] {
        color: #cbd5e1;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        color: #f8fafc;
        font-weight: 600;
    }
    .stButton > button:hover {
        border-color: rgba(14, 165, 233, 0.9);
        color: #e0f2fe;
    }

    .stSelectbox label, .stNumberInput label, .stCheckbox label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }

    /* Dark theme for all popover/modal content */
    [data-testid="stPopoverBody"] {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.98), rgba(20, 30, 48, 0.98)) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }
    [data-testid="stPopoverBody"] p, [data-testid="stPopoverBody"] div, [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] h1, [data-testid="stPopoverBody"] h2, [data-testid="stPopoverBody"] h3,
    [data-testid="stPopoverBody"] h4, [data-testid="stPopoverBody"] h5, [data-testid="stPopoverBody"] h6 {
        color: #f8fafc !important;
        background-color: transparent !important;
    }
    [data-testid="stPopoverBody"] * {
        color: #f8fafc !important;
    }

    /* Dark theme for inputs */
    .stSelectbox [data-baseweb="select"] {
        background-color: rgba(10, 17, 32, 0.9) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.95) !important;
        color: #f8fafc !important;
        border-color: rgba(148, 163, 184, 0.25) !important;
    }
    .stSelectbox [data-baseweb="popover"] {
        background-color: rgba(10, 17, 32, 0.95) !important;
    }
    .stSelectbox [data-baseweb="option"] {
        background-color: rgba(10, 17, 32, 0.95) !important;
        color: #f8fafc !important;
    }
    .stSelectbox [data-baseweb="option"]:hover {
        background-color: rgba(30, 58, 138, 0.7) !important;
    }

    /* AGGRESSIVE dropdown/select option styling */
    [data-baseweb="listbox"],
    [data-baseweb="menu"],
    [role="listbox"],
    [role="menu"],
    ul[role="listbox"] {
        background-color: rgba(10, 17, 32, 0.95) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }

    [data-baseweb="listbox"] li,
    [data-baseweb="menu"] div,
    [role="listbox"] li,
    [role="option"],
    ul[role="listbox"] li {
        background-color: rgba(10, 17, 32, 0.95) !important;
        color: #f8fafc !important;
    }

    [data-baseweb="listbox"] li:hover,
    [data-baseweb="menu"] div:hover,
    [role="option"]:hover,
    ul[role="listbox"] li:hover {
        background-color: rgba(30, 58, 138, 0.7) !important;
        color: #f8fafc !important;
    }

    /* Generic dropdown overlay */
    div[class*="Menu"],
    div[class*="menu"],
    div[class*="popup"],
    div[class*="popover"],
    div[class*="Popover"] {
        background-color: rgba(10, 17, 32, 0.95) !important;
    }
    div[class*="Menu"] *,
    div[class*="menu"] *,
    div[class*="popup"] *,
    div[class*="popover"] *,
    div[class*="Popover"] * {
        background-color: transparent !important;
        color: #f8fafc !important;
    }

    /* Dark theme for number input */
    .stNumberInput input {
        background-color: rgba(10, 17, 32, 0.9) !important;
        color: #f8fafc !important;
        border-color: rgba(148, 163, 184, 0.25) !important;
    }

    /* Dark theme for checkbox */
    .stCheckbox {
        color: #f8fafc !important;
    }

    /* Dark theme for expander */
    .streamlit-expanderHeader {
        background-color: rgba(15, 23, 42, 0.95) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
    }
    .streamlit-expanderContent {
        background-color: rgba(10, 17, 32, 0.9) !important;
        color: #f8fafc !important;
    }

    /* Dark theme for dataframe */
    [data-testid="stDataFrameContainer"] {
        background-color: rgba(10, 17, 32, 0.9) !important;
    }

    /* AGGRESSIVE dark theme for all modals, popovers, dialogs */
    [role="dialog"], [role="alertdialog"], .streamlit-container {
        background-color: rgba(5, 9, 19, 0.98) !important;
        color: #f8fafc !important;
    }

    /* Target all modal-like divs */
    div[class*="modal"], div[class*="popover"], div[class*="dialog"],
    .st-emotion-cache-bm2z3a, [data-testid="modal"], [data-testid="dialog"] {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.98), rgba(20, 30, 48, 0.98)) !important;
        color: #f8fafc !important;
    }

    /* Override all div backgrounds that aren't explicitly styled */
    [data-testid="stVerticalBlock"] div,
    [data-testid="stHorizontalBlock"] div,
    [class*="stForm"] div {
        background-color: transparent !important;
        color: #f8fafc !important;
    }

    /* Ensure all text is visible */
    p, span, h1, h2, h3, h4, h5, h6, label, li, td, th {
        color: #f8fafc !important;
    }

    /* Progress bars */
    .stProgress > div > div {
        background-color: rgba(30, 50, 100, 0.6) !important;
    }

    /* Captions and small text */
    .caption, small, .text-muted {
        color: #cbd5e1 !important;
    }

    /* Links */
    a {
        color: #38bdf8 !important;
    }
    a:hover {
        color: #7dd3fc !important;
    }

    /* Override Streamlit default container backgrounds */
    .element-container div[class*="st"],
    .element-container > div {
        background-color: transparent !important;
    }

    /* Ensure metric container background is dark */
    [data-testid="stMetricContainer"],
    [data-testid="stMetric"] > div {
        background-color: transparent !important;
    }

    /* Help tooltips */
    [role="tooltip"] {
        background-color: rgba(15, 23, 42, 0.98) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.2);
    }
    footer {visibility: hidden}
    header {visibility: hidden}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Config
# -----------------------
TICKERS = ["NVO", "LLY", "PFE", "MRK", "JNJ", "ABBV", "BMY", "AMGN", "GILD"]


@st.cache_data(ttl=180)
def load_intraday(tickers: list) -> pd.DataFrame:
    rows = []
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            hist = stock.history(period="1d", interval="5m")
            if len(hist) < 2:
                continue
            price = hist["Close"].iloc[-1]
            open_price = hist["Open"].iloc[0]
            change = ((price - open_price) / open_price) * 100
            volume = int(hist["Volume"].sum())
            rows.append({
                "Ticker": t,
                "Price": round(price, 2),
                "Change": round(change, 2),
                "Volume": volume,
                "Series": hist["Close"],
                "HistoryDF": hist.reset_index()
            })
        except Exception:
            continue
    return pd.DataFrame(rows)


@st.cache_data(ttl=600)
def load_history(ticker: str, period: str = "6mo") -> pd.DataFrame:
    t = yf.Ticker(ticker)
    return t.history(period=period).reset_index()


df = load_intraday(TICKERS)

# session state for selected ticker
if "selected" not in st.session_state:
    st.session_state.selected = df.sort_values("Change", key=abs, ascending=False)["Ticker"].iloc[0] if not df.empty else TICKERS[0]


# ---------- SurgeScore: live computation with NewsAPI + VADER ----------
analyzer = SentimentIntensityAnalyzer()


def fetch_newsapi(ticker_q: str):
    """Fetch news articles from NewsAPI.org if API key is set."""
    key = os.environ.get("NEWSAPI_KEY")
    if not key:
        return []
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": ticker_q,
            "language": "en",
            "pageSize": 10,
            "sortBy": "publishedAt",
            "apiKey": key,
        }
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data.get("articles", [])
    except Exception:
        return []


@st.cache_data(ttl=60)
def compute_surge_score_for_ticker(ticker: str, intraday_row: dict) -> dict:
    """Compute SurgeScore using momentum, relative volume, news sentiment (VADER), and options/IV signals.

    Returns a dict with fields: SurgeScore (0-100), rel_vol, momentum, news_score, opt_score, articles_with_scores
    """
    # --- volume & momentum
    try:
        hist60 = load_history(ticker, period="60d")
        avg_daily_vol = float(hist60["Volume"].mean()) if not hist60.empty else 0.0
    except Exception:
        avg_daily_vol = 0.0

    current_vol = float(intraday_row.get("Volume") or 0)
    rel_vol = (current_vol / avg_daily_vol) if avg_daily_vol > 0 else 0.0

    momentum = float(intraday_row.get("Change") or 0.0)

    # Map momentum (pct) to 0-100 assuming 10% is a very large move
    momentum_score = min((abs(momentum) / 10.0) * 100.0, 100.0)

    # Map relative volume: 1x -> 0, 5x -> 100 (linear between)
    relvol_score = 0.0
    if rel_vol > 1.0:
        relvol_score = min(((rel_vol - 1.0) / 4.0) * 100.0, 100.0)

    # --- news / sentiment (NewsAPI with VADER)
    articles_with_scores = []
    try:
        # prefer NewsAPI when key is available
        articles = fetch_newsapi(ticker) if os.environ.get("NEWSAPI_KEY") else []
        if not articles:
            # fallback to yfinance headlines
            t = yf.Ticker(ticker)
            raw = t.news if hasattr(t, "news") else []
            articles = [{"title": (n.get("title") or ""), "description": (n.get("summary") or "")} for n in raw[:6]]

        # score each article with VADER compound and store with metadata
        scores = []
        for a in articles:
            text = ((a.get("title") or "") + " " + (a.get("description") or ""))
            if not text.strip():
                continue
            vader_scores = analyzer.polarity_scores(text)
            compound = vader_scores.get("compound", 0.0)
            scores.append(compound)
            # map compound to 0-100 scale for display
            sentiment_score = (compound + 1.0) / 2.0 * 100.0
            articles_with_scores.append({
                "title": a.get("title", "No title"),
                "description": a.get("description", ""),
                "source": a.get("source", {}).get("name", "Unknown") if isinstance(a.get("source"), dict) else "Unknown",
                "compound": round(compound, 3),
                "sentiment_score": round(sentiment_score, 1),
                "tone": "Positive" if sentiment_score > 60 else ("Negative" if sentiment_score < 40 else "Neutral")
            })

        if not scores:
            news_score = 50.0
        else:
            # compound in [-1,1] -> map to [0,100]
            avg_compound = sum(scores) / len(scores)
            news_score = (avg_compound + 1.0) / 2.0 * 100.0
    except Exception:
        news_score = 50.0

    # --- options / IV signals (nearest expiry)
    try:
        opt_score = 0.0
        t = yf.Ticker(ticker)
        exps = t.options
        if exps:
            expiry = exps[0]
            oc = t.option_chain(expiry)
            calls = oc.calls
            iv = float(calls["impliedVolatility"].replace({np.nan: 0}).mean()) if not calls.empty else 0.0
            oi = float(calls["openInterest"].sum()) if not calls.empty else 0.0
            # scale iv (~0.0-1.0) to 0-100
            iv_score = min(iv * 250.0, 100.0)
            oi_score = min(oi / 10000.0 * 100.0, 100.0)
            opt_score = 0.6 * iv_score + 0.4 * oi_score
        else:
            opt_score = 0.0
    except Exception:
        opt_score = 0.0

    # --- combine: weights tuned for quick-event detection
    # momentum 35%, rel vol 25%, news 20%, options 20%
    surge = 0.35 * momentum_score + 0.25 * relvol_score + 0.20 * news_score + 0.20 * opt_score

    return {
        "SurgeScore": int(min(max(surge, 0), 100)),
        "rel_vol": round(rel_vol, 2),
        "momentum": round(momentum, 2),
        "news_score": round(news_score, 1),
        "opt_score": int(opt_score),
        "articles_with_scores": articles_with_scores
    }


def compute_surges(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        info = compute_surge_score_for_ticker(r["Ticker"], r)
        r2 = r.copy()
        r2["SurgeScore"] = info["SurgeScore"]
        r2["RelVol"] = info["rel_vol"]
        r2["Momentum"] = info["momentum"]
        r2["NewsScore"] = info["news_score"]
        r2["OptScore"] = info["opt_score"]
        r2["ArticlesList"] = info["articles_with_scores"]
        rows.append(r2)
    return pd.DataFrame(rows)


# compute surge scores for current universe
if not df.empty:
    df = compute_surges(df)

# -----------------------
# Layout: Top header + body
# -----------------------
_hcol1, _hcol3, _hcol4 = st.columns([3, 0.4, 0.4])
with _hcol1:
    st.markdown(f"<div class='header'>Healthcare Terminal · {datetime.now().strftime('%b %d %H:%M:%S')}</div>", unsafe_allow_html=True)
with _hcol3:
    with st.popover("⚙️"):
        st.markdown("**Refresh Settings**")
        if st.button("Refresh Now", key="topbar_refresh"):
            st.rerun()
        auto = st.checkbox("Auto-refresh", value=False, key="topbar_auto")
        interval = st.number_input("Interval (sec)", min_value=5, max_value=600, value=30, key="topbar_interval")
        if auto:
            st.markdown(f"<meta http-equiv='refresh' content='{int(interval)}'>", unsafe_allow_html=True)
with _hcol4:
    with st.popover("☰"):
        st.markdown("**Category**")
        _cat = st.selectbox("Category", options=list(categories.CATEGORIES.keys()), index=0, key="cat_pop", label_visibility="collapsed")

# pull values set in popovers (fallback defaults if not yet interacted)
_category = st.session_state.get("cat_pop", "All")

category_tickers = categories.CATEGORIES.get(_category, [])
if _category != "All" and category_tickers:
    market_df = df[df["Ticker"].isin(category_tickers)].copy()
else:
    market_df = df.copy()

# fallback so view does not go empty when category contains non-loaded names
if market_df.empty:
    market_df = df.copy()

if not market_df.empty and st.session_state.selected not in market_df["Ticker"].tolist():
    st.session_state.selected = market_df.sort_values("Change", key=np.abs, ascending=False)["Ticker"].iloc[0]

st.markdown("---")

# Tabs for each dashboard mode
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Market", "Monitoring / Ops", "Product Analytics", "Executive KPI", "Sales / CRM", "FP&A"])

# ===== TAB 1: MARKET VIEW (DEFAULT) =====
with tab1:
    left, center, right = st.columns([1.55, 3.1, 1.35])

    with left:
        st.markdown("<div class='panel-title'>Watchlist Command Center</div>", unsafe_allow_html=True)
        if market_df.empty:
            st.warning("No market data currently available.")
        else:
            adv = int((market_df["Change"] > 0).sum())
            dec = int((market_df["Change"] < 0).sum())
            flat = int((market_df["Change"] == 0).sum())
            avg_move = float(market_df["Change"].mean())
            avg_surge = int(market_df["SurgeScore"].mean())

            c1, c2 = st.columns(2)
            c1.metric("Advancers", adv)
            c2.metric("Decliners", dec)
            c3, c4 = st.columns(2)
            c3.metric("Avg Move", f"{avg_move:+.2f}%")
            c4.metric("Avg Surge", f"{avg_surge}")

            mood = "Risk-On" if avg_move > 0.35 else ("Risk-Off" if avg_move < -0.35 else "Balanced")
            mood_cls = "good" if mood == "Risk-On" else ("bad" if mood == "Risk-Off" else "neutral")
            st.markdown(
                f"<div class='watch-card'><span class='muted'>Session Mood</span><br><span class='{mood_cls}'>{mood}</span>"
                f"<div class='watch-meta'><span>Flat: {flat}</span><span>{datetime.now().strftime('%H:%M:%S')}</span></div></div>",
                unsafe_allow_html=True,
            )

            _sort_mode = st.selectbox(
                "Sort watchlist",
                ["SurgeScore", "Change", "Volume", "Ticker"],
                index=0,
                key="watchlist_sort",
            )

            if _sort_mode == "Ticker":
                watch_df = market_df.sort_values("Ticker", ascending=True)
            else:
                watch_df = market_df.sort_values(_sort_mode, ascending=False)

            st.markdown("<div class='panel-title' style='margin-top:0.5rem;'>Pick A Ticker</div>", unsafe_allow_html=True)
            for _, r in watch_df.iterrows():
                is_selected = st.session_state.selected == r["Ticker"]
                btn_label = f"{r['Ticker']}  {r['Change']:+.2f}%"
                if st.button(btn_label, key=f"watch_btn_{r['Ticker']}", use_container_width=True, type="primary" if is_selected else "secondary"):
                    st.session_state.selected = r["Ticker"]
                    st.rerun()
                change_cls = "good" if r["Change"] > 0 else ("bad" if r["Change"] < 0 else "neutral")
                st.markdown(
                    f"<div class='watch-meta'><span class='{change_cls}'>Move {r['Change']:+.2f}%</span>"
                    f"<span>Surge {int(r['SurgeScore'])}/100</span></div>",
                    unsafe_allow_html=True,
                )

    with right:
        _tm_hdr, _tm_info = st.columns([3, 0.7])
        _tm_hdr.markdown("**Top Movers**")
        with _tm_info:
            with st.popover("ℹ️"):
                st.markdown("**Top Movers**")
                st.markdown("Ranked by absolute % change from today's open. Largest moves (up or down) appear first. Click any change value for more context on that ticker.")
        movers = market_df.sort_values("Change", key=np.abs, ascending=False).head(8)
        for _, r in movers.iterrows():
            arrow = "↑" if r["Change"] > 0 else "↓"
            _m_name, _m_chg = st.columns([1.8, 1.2])
            _m_name.markdown(f"<div style='padding-top:5px'><b>{r['Ticker']}</b> <span class='muted'>· ${r['Price']}</span></div>", unsafe_allow_html=True)
            with _m_chg:
                with st.popover(f"{arrow} {abs(r['Change']):.2f}%"):
                    st.markdown(f"**{r['Ticker']}** — {r['Change']:+.2f}% intraday")
                    st.markdown(f"Price: **${r['Price']}**  ·  Vol: **{r['Volume']:,}**")
                    _ms = market_df.loc[market_df['Ticker'] == r['Ticker'], 'SurgeScore']
                    _mscore = int(_ms.iloc[0]) if not _ms.empty else 0
                    st.markdown(f"SurgeScore: **{_mscore}/100**")
                    st.caption("Select ticker in watchlist to load full chart")

        st.markdown("---")
        _hm_hdr, _hm_info = st.columns([3, 0.7])
        _hm_hdr.markdown("**Heatmap**")
        with _hm_info:
            with st.popover("ℹ️"):
                st.markdown("**Performance Heatmap**")
                st.markdown("Each tile = one stock's intraday % change. **Green** = positive, **Red** = negative. Click ▶ on any tile for details.")
        heat_cols = st.columns(3)
        for i, (_, r) in enumerate(market_df.iterrows()):
            c = heat_cols[i % 3]
            bg = "linear-gradient(140deg, #064e3b, #065f46)" if r["Change"] > 0 else "linear-gradient(140deg, #7f1d1d, #991b1b)"
            c.markdown(f"<div style='background:{bg};padding:8px;border-radius:8px;text-align:center;margin-bottom:4px;border:1px solid rgba(241,245,249,0.2)'>{r['Ticker']}<br><b>{r['Change']:+.2f}%</b></div>", unsafe_allow_html=True)
            with c:
                with st.popover("▶", use_container_width=True):
                    st.markdown(f"**{r['Ticker']}** — {r['Change']:+.2f}% today")
                    st.markdown(f"Price: **${r['Price']}**  ·  Vol: **{r['Volume']:,}**")
                    _hs = market_df.loc[market_df['Ticker'] == r['Ticker'], 'SurgeScore']
                    _hscore = int(_hs.iloc[0]) if not _hs.empty else 0
                    st.caption(f"SurgeScore {_hscore}/100")

    with center:
        sel = st.session_state.selected
        _cv_row1, _cv_row2, _cv_row3 = st.columns([2.5, 1.5, 0.5])
        with _cv_row1:
            st.markdown(f"**Market View** · {sel}")
        with _cv_row2:
            _range = st.selectbox("Range", ["1mo", "3mo", "6mo", "1y"], index=2, label_visibility="collapsed")
        with _cv_row3:
            with st.popover("ℹ️"):
                st.markdown("**Price Chart — Moving Averages**")
                st.markdown("""
- **Green line** — Daily closing price  
- **Purple dashed (MA20)** — 20-day moving average; tracks short-term trend  
- **Orange dotted (MA50)** — 50-day moving average; tracks medium-term trend  
- **Golden Cross** — MA20 crosses above MA50 → historically bullish  
- **Death Cross** — MA20 crosses below MA50 → historically bearish  
Hover any point to see exact date + price values.
""")
        history = load_history(sel, period=_range)

        # main interactive chart with moving averages
        history["MA20"] = history["Close"].rolling(20).mean()
        history["MA50"] = history["Close"].rolling(50).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=history["Date"], y=history["Close"], mode="lines", name="Close", line=dict(color="#00ff9c")))
        fig.add_trace(go.Scatter(x=history["Date"], y=history["MA20"], mode="lines", name="MA20", line=dict(color="#7c3aed", dash="dash")))
        fig.add_trace(go.Scatter(x=history["Date"], y=history["MA50"], mode="lines", name="MA50", line=dict(color="#f97316", dash="dot")))

        fig.update_layout(
            plot_bgcolor="#0a1324",
            paper_bgcolor="#0a1324",
            font_color="#f8fafc",
            height=460,
            margin=dict(t=25, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)

        # stat bar + clickable SurgeScore popover
        stats = market_df.set_index("Ticker").to_dict(orient="index")
        if sel in stats:
            s = stats[sel]
            score = int(s.get("SurgeScore", 0))
            momentum = float(s.get("Momentum", 0))
            rel_vol = float(s.get("RelVol", 0))
            news_score = float(s.get("NewsScore", 50))
            opt_score = float(s.get("OptScore", 0))
            surge_label = "High" if score >= 70 else ("Moderate" if score >= 40 else "Low")
            news_tone = "positive" if news_score > 60 else ("negative" if news_score < 40 else "neutral")
            if score >= 70:
                investor_msg_sel = f"**Strong signal** — {sel} is showing unusual price action, volume spike, and/or elevated options activity. This likely indicates a pending catalyst. Consider immediate attention."
            elif score >= 40:
                investor_msg_sel = f"**Watch closely** — {sel} has moderate activity. Worth watching for 15–30 min for confirmation."
            else:
                investor_msg_sel = f"**Quiet** — {sel} is trading normally. Good for baseline or long-term monitoring."

            signal_state = "Momentum Breakout" if momentum > 1.5 and rel_vol > 1.5 else ("High-Risk Fade" if momentum < -1.5 else "Range Battle")

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Price", s["Price"], delta=f"{s['Change']}%")
                with st.popover("ℹ️ Price"):
                    st.markdown(f"**{sel} — Intraday Price**")
                    st.markdown(f"Current price **${s['Price']}**, {'+' if s['Change'] > 0 else ''}{s['Change']}% from today's open.")
                    st.markdown("The delta arrow and color show movement direction relative to today's open.")
            with col_b:
                st.metric("Volume", f"{s['Volume']:,}")
                with st.popover("ℹ️ Volume"):
                    st.markdown(f"**{sel} — Today's Volume**")
                    st.markdown(f"**{s['Volume']:,}** shares traded intraday so far.")
                    st.markdown(f"Relative vs 60-day avg: **{rel_vol:.2f}x**. Above 1.5x = elevated interest; above 3x = unusual activity.")
            with col_d:
                st.metric("News Sentiment", f"{news_score:.0f}/100")
                with st.popover("ℹ️ Sentiment"):
                    st.markdown(f"**{sel} — News Sentiment Score**")
                    st.markdown(f"Score: **{news_score:.0f}/100** ({news_tone} tone)")
                    st.progress(int(news_score))
                    st.markdown("Scored using VADER NLP on recent headlines. 0 = very negative · 50 = neutral · 100 = very positive. Sourced from yfinance + NewsAPI.")
            with col_c:
                with st.popover(f"Surge Score: {score}"):
                    st.markdown(f"### {sel} · SurgeScore {score}/100 — {surge_label}")
                    st.markdown(f"**Momentum** ({momentum:+.2f}%)")
                    st.progress(min(int(abs(momentum) / 10 * 100), 100))
                    st.markdown(f"**Relative Volume** ({rel_vol:.2f}x avg)")
                    st.progress(min(int(max((rel_vol - 1) / 4 * 100, 0)), 100))
                    st.markdown(f"**News Sentiment** ({news_tone})")
                    st.progress(int(news_score))
                    st.markdown("**Options / IV Signal**")
                    st.progress(min(int(opt_score), 100))
                    st.divider()
                    st.markdown(investor_msg_sel)
                    
                    # Show actionable news stories driving sentiment
                    st.markdown("---")
                    st.markdown("### 📰 News Drivers (VADER Analyzed)")
                    articles_list = market_df.loc[market_df["Ticker"] == sel, "ArticlesList"].values
                    if articles_list is not None and len(articles_list) > 0:
                        articles = articles_list[0]
                        if articles:
                            for i, article in enumerate(articles[:5], 1):
                                tone_color = "🟢" if article["tone"] == "Positive" else ("🔴" if article["tone"] == "Negative" else "🟡")
                                st.markdown(
                                    f"{tone_color} **[{i}] {article['title'][:70]}...**",
                                    help=article["description"][:200] if article["description"] else "No description"
                                )
                                st.caption(
                                    f"Sentiment: {article['sentiment_score']:.0f}/100 · Source: {article['source']} · Confidence: {abs(article['compound']):.2f}"
                                )
                        else:
                            st.caption("No recent news articles found.")
                    else:
                        st.caption("No news data available.")

            st.markdown(
                f"<div class='watch-card'><span class='muted'>Decision Engine</span><br><span class='good'>{signal_state}</span>"
                f"<div class='watch-meta'><span>RelVol {rel_vol:.2f}x</span><span>Momentum {momentum:+.2f}%</span></div></div>",
                unsafe_allow_html=True,
            )

        # clickable features: show underlying data table and allow export
        with st.expander("Data & Export"):
            st.dataframe(history.tail(50))
            csv = history.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv, file_name=f"{sel}_history.csv")


# ===== TAB 2: MONITORING / OPS =====
with tab2:
    def render_monitoring(data: pd.DataFrame):
        st.markdown("**Monitoring — compact sparklines & alerts**")
        if data.empty:
            st.info("No intraday data available")
            return

        cols = st.columns(3)
        for i, (_, r) in enumerate(data.iterrows()):
            c = cols[i % 3]
            series = r.get("Series")
            if series is None:
                c.write(r["Ticker"])
                continue
            fig = go.Figure(data=go.Scatter(y=series.values, mode="lines", line=dict(color="#00ff9c")))
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=80, plot_bgcolor="#071027", paper_bgcolor="#071027")
            alert = abs(r["Change"]) > 3
            badge = "🔴" if alert else "●"
            _sc_t, _sc_p = c.columns([3, 1])
            _sc_t.markdown(f"**{r['Ticker']}** {badge}")
            with _sc_p:
                with st.popover("ℹ️"):
                    st.markdown(f"**{r['Ticker']} — Intraday Sparkline**")
                    st.markdown(f"Change today: **{r['Change']:+.2f}%**  ·  Vol: **{r['Volume']:,}**")
                    if alert:
                        st.markdown("🔴 **Alert triggered** — move exceeds ±3% threshold. Warrants attention.")
                    else:
                        st.markdown("● Within normal range. No alert triggered.")
                    st.caption("Sparkline = 5-min interval intraday price path")
            c.plotly_chart(fig, use_container_width=True)

    render_monitoring(df)


# ===== TAB 3: PRODUCT ANALYTICS =====
with tab3:
    def render_product_analytics():
        st.markdown("**Product Analytics — cohort retention & funnel (synthetic demo)**")
        _ret_hdr, _ret_info = st.columns([5, 0.5])
        _ret_hdr.markdown("**Cohort Retention**")
        with _ret_info:
            with st.popover("ℹ️"):
                st.markdown("**Cohort Retention Chart**")
                st.markdown("Shows % of users from each cohort still active after N days. A steep drop = poor retention. A flat line = strong stickiness. Each cohort = a different acquisition batch.")
        days = list(range(0, 30, 5))
        cohorts = {f"Cohort {i}": np.maximum(100 - np.array(days) - i * 2, 10) for i in range(3)}
        ret_df = pd.DataFrame(cohorts, index=days).reset_index().melt(id_vars=["index"])
        ret_df.columns = ["Days", "Cohort", "Retention"]
        fig = px.line(ret_df, x="Days", y="Retention", color="Cohort", markers=True)
        fig.update_layout(plot_bgcolor="#071027", paper_bgcolor="#071027", font_color="#cbd5e1")
        st.plotly_chart(fig, use_container_width=True)

        _fn_hdr, _fn_info = st.columns([5, 0.5])
        _fn_hdr.markdown("**Conversion Funnel**")
        with _fn_info:
            with st.popover("ℹ️"):
                st.markdown("**Conversion Funnel**")
                st.markdown("Shows user drop-off at each stage of the journey. Wide-to-narrow shape is normal. Large gaps between stages = conversion bottlenecks worth investigating.")
        funnel_df = pd.DataFrame({"stage": ["Visited", "Signed Up", "Activated", "Paid"], "value": [10000, 2400, 1200, 300]})
        ff = px.funnel(funnel_df, x="value", y="stage")
        st.plotly_chart(ff, use_container_width=True)

    render_product_analytics()


# ===== TAB 4: EXECUTIVE KPI =====
with tab4:
    def render_executive_kpi(data: pd.DataFrame):
        st.markdown("**Executive KPI — focused cards & sparklines**")
        k1, k2, k3 = st.columns(3)
        mom = round(data["Change"].mean() if not data.empty else 0, 2)
        total_vol = int(data["Volume"].sum() if not data.empty else 0)
        with k1:
            st.metric("Avg Momentum", f"{mom}%", delta=f"{mom/2:.2f}%")
            with st.popover("ℹ️ Avg Momentum"):
                st.markdown("**Average Momentum**")
                st.markdown(f"Mean intraday % change across all **{len(data)}** watched tickers today.")
                st.markdown("Positive = universe net bullish today. Negative = broad selling pressure.")
        with k2:
            st.metric("Universe Vol", f"{total_vol:,}")
            with st.popover("ℹ️ Universe Vol"):
                st.markdown("**Universe Volume**")
                st.markdown(f"Total shares traded today across **{len(data)}** tickers: **{total_vol:,}**.")
                st.markdown("Elevated universe volume can signal broad institutional activity or a macro/sector event.")
        with k3:
            st.metric("Watchlist", len(data))
            with st.popover("ℹ️ Watchlist"):
                st.markdown("**Watchlist Size**")
                st.markdown(f"**{len(data)}** tickers currently active in the monitoring universe.")
                st.markdown("Configure the ticker list in config/tickers.py.")
        st.markdown("---")

    render_executive_kpi(df)


# ===== TAB 5: SALES / CRM =====
with tab5:
    def render_sales_crm():
        st.markdown("**Sales / CRM — funnel & leaderboard (demo)**")
        _sf_hdr, _sf_info = st.columns([5, 0.5])
        _sf_hdr.markdown("**Sales Pipeline Funnel**")
        with _sf_info:
            with st.popover("ℹ️"):
                st.markdown("**Sales Pipeline Funnel**")
                st.markdown("- **Lead** — initial contact identified\n- **Qualified** — confirmed budget/need/timeline\n- **Proposal** — formal proposal submitted\n- **Closed** — deal won and booked\n\nConversion rate = Closed ÷ Lead. Large gaps between stages indicate where the pipeline needs attention.")
        funnel_df = pd.DataFrame({"stage": ["Lead", "Qualified", "Proposal", "Closed"], "value": [1200, 400, 180, 45]})
        f = px.funnel(funnel_df, x="value", y="stage")
        st.plotly_chart(f, use_container_width=True)

        _lb_hdr, _lb_info = st.columns([5, 0.5])
        _lb_hdr.markdown("**Rep Leaderboard**")
        with _lb_info:
            with st.popover("ℹ️"):
                st.markdown("**Rep Leaderboard**")
                st.markdown("Revenue closed per sales rep this period, sorted descending. Use to identify top performers and reps who may need coaching or support.")
        leaders = pd.DataFrame({"Rep": ["Alice", "Bob", "Cara"], "Revenue": [240000, 180000, 150000]})
        st.table(leaders)

    render_sales_crm()


# ===== TAB 6: FP&A =====
with tab6:
    def render_fp_a():
        _fp_hdr, _fp_info = st.columns([5, 0.5])
        _fp_hdr.markdown("**FP&A — Waterfall & Variance**")
        with _fp_info:
            with st.popover("ℹ️"):
                st.markdown("**Waterfall Chart — P&L Breakdown**")
                st.markdown("Shows how each line item builds to or reduces net income:\n- **Revenue** — starting value\n- **COGS** — cost of goods sold (reduces)\n- **OpEx** — operating expenses (reduces)\n- **Tax** — tax provision (reduces)\n- **Net** — final bottom-line total\n\nGreen bars add value; red bars reduce it.")
        measures = ["Revenue", "COGS", "OpEx", "Tax", "Net"]
        vals = [1000000, -350000, -250000, -90000, 310000]
        wf = go.Figure(go.Waterfall(x=measures, y=vals, measure=["relative", "relative", "relative", "relative", "total"]))
        wf.update_layout(plot_bgcolor="#071027", paper_bgcolor="#071027", font_color="#cbd5e1")
        st.plotly_chart(wf, use_container_width=True)

    render_fp_a()
