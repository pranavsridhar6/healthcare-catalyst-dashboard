<img width="1847" height="877" alt="Market View" src="https://raw.githubusercontent.com/pranavsridhar6/healthcare-catalyst-dashboard/main/ss1.jpg" />
<img width="952" height="721" alt="SurgeScore" src="https://raw.githubusercontent.com/pranavsridhar6/healthcare-catalyst-dashboard/main/ss2.jpg" />
<img width="457" height="342" alt="Executive KPI" src="https://raw.githubusercontent.com/pranavsridhar6/healthcare-catalyst-dashboard/main/ss3.jpg" />

# Healthcare Catalyst Dashboard

A Streamlit terminal for tracking catalyst-driven moves in healthcare and pharma equities. The idea came out of watching GLP-1 and oncology names gap on FDA headlines and wanting one screen that showed price action, unusual volume, news tone, and options positioning together instead of four tabs.

Live app: https://hdashboard.streamlit.app/

## What it does

**Market view** is the main tab. Left panel is the watchlist with advancers/decliners, average move, and a session mood read. Center is a price chart with MA20/MA50 overlays and golden/death cross context. Right side has top movers ranked by absolute move and a performance heatmap. Clicking into any ticker gives you a plain-English read on what the signals are saying.

**SurgeScore** is the piece I spent the most time on. It's a 0-100 composite that blends four inputs:

| Input | Weight | Source |
|---|---|---|
| Intraday momentum | 35% | % change from open, scaled against a 10% move |
| Relative volume | 25% | Session volume vs 60-day average |
| News sentiment | 20% | VADER compound score across recent headlines |
| Options signal | 20% | Mean implied vol + call open interest, nearest expiry |

The weights are tuned toward catching fast events rather than predicting direction. A high score means something is happening, not that it's going up.

**Monitoring / Ops** gives compact intraday sparklines for the full universe with an alert badge on anything moving more than ±3%.

**Executive KPI** is the roll-up view. Eight headline metrics split into market state (average move, breadth, participation, dispersion) and catalyst state (active catalysts, average SurgeScore, news tone, risk flags), then a session verdict that reads those together into one of Risk-On, Risk-Off, Catalyst-Driven, Quiet Tape, or Balanced. Below that: session leaders and laggards, an advance/decline bar, a category exposure table broken out by therapeutic area, and a catalyst watchlist showing the top five names with their contributing inputs separated out.

The reason for splitting market state from catalyst state is that they answer different questions. Average move tells you the sector is up; breadth tells you whether that's broad or one name carrying it; dispersion tells you whether to trade the sector or screen individual tickers.

Every chart has an info popover explaining how to read it.

## Data sources

- **yfinance** for intraday bars (5-min interval, 180s cache), daily history, and options chains
- **NewsAPI** for headlines, with a fallback to yfinance news when no API key is set
- **VADER** for sentiment scoring on headline and description text

Data pulls happen on request with caching, and there's an auto-refresh toggle in the gear menu if you want it polling on an interval.

## Running locally

```bash
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

The app runs without a NewsAPI key. Sentiment just falls back to yfinance headlines, which are thinner.

## Configuration

On Streamlit Cloud, add these under app settings:

```toml
APP_PUBLIC_URL = "https://<your-app-name>.streamlit.app"
NEWSAPI_KEY = "<your_newsapi_key>"
```

`APP_PUBLIC_URL` feeds the copy-link button in the share popover. Without it the button falls back to a message telling you to set it.

Locally, `NEWSAPI_KEY` is read from the environment, so a `.env` file or a plain export both work.

## Layout

```
frontend/streamlit_app.py     the whole dashboard
config/categories.py          category to ticker groupings
config/keywords.py            ticker keywords, themes, competitor mappings
config/tickers.py             ticker universe, loaded by the app at startup
lambda/ingestion/             handler scaffold for batched record processing
lambda/processing/logic.py    keyword-based theme and ticker extraction
backend/s3_service.py         S3 upload/download/list wrapper
```

## Notes

Every ticker triggers an intraday pull, a 60-day history pull, and an options chain lookup, so first load on a cold cache takes a few seconds. Caching is set at 180s for intraday and 600s for daily history, which keeps repeat interactions fast without going stale during a session.

The `lambda/` and `backend/` modules are standalone utilities rather than deployed infrastructure. The keyword extraction in `lambda/processing/logic.py` runs fine on its own and the S3 wrapper works if you point it at a bucket, but nothing is scheduled or triggered.

## What's next

- **ML-based catalyst classification.** Replace the keyword matching with a trained classifier that can tell an FDA approval from a complete response letter from an earnings beat, and weight the catalyst type into SurgeScore instead of treating all news the same.
- **LLM-powered summaries and a chat window.** Instead of the rule-based interpretation strings, generate a real summary of why a ticker is moving from the headlines and price action, plus a chat panel for follow-up questions against the current dashboard state.
