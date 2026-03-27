# DataLens

A GenAI powered data analysis tool where you just upload a CSV and ask questions in plain English. It analyzes, visualizes and even forecasts your data.

Built with Python, Streamlit and Google Gemini.

---

## Why I Built This

I wanted to build something that solves a real problem. Most people who work with data aren't developers — they don't know pandas or SQL. They just want answers from their data without writing a single line of code.

So I built DataLens. You upload a CSV, ask a question like *"what are the top 5 products by sales in the North region?"* and it gives you the answer, a chart and a plain English explanation — all in seconds.

---

## What It Can Do

- **Ask anything about your data** — total sales, averages, top performers, bottom performers
- **Filter your data** — *"show me sales only in the South region"*
- **Group and compare** — *"total profit by category"*
- **Visualize** — line charts, bar charts, pie charts, scatter plots, histograms, box plots
- **Forecast future trends** — *"forecast sales for the next 3 months"*
- **Plain English insights** — every result comes with a simple business explanation
- **Chat history** — your entire conversation stays on screen as you keep asking questions

---

## How It Works

This is the part I'm most proud of. Instead of hardcoding analysis logic for every possible question, I used Google Gemini to act as a translator.

Here's the flow:

```
User Question (natural language)
        ↓
Google Gemini converts it to JSON instructions
        ↓
Python engine executes the instructions on the dataframe
        ↓
Results displayed as text + chart + insight
```

For example, when you ask *"show me top 5 products by sales in North region"*, Gemini returns:

```json
{
  "filter": [{"column": "region", "operator": "equals", "value": "North"}],
  "analysis": [{"operation": "top_n", "column": "sales", "group_by": null, "n": 5}]
}
```

Then my Python engine takes that JSON and runs it on the actual dataframe. The LLM never touches the data directly — it just figures out what to do, and Python does the actual work.

---

## Forecasting

For forecasting I used Meta's Prophet library. When you ask something like *"forecast sales for next 3 months"*, it:

1. Takes your historical date and sales columns
2. Detects the frequency of your data automatically (daily, monthly, yearly)
3. Trains a Prophet model on your historical data
4. Predicts future values with upper and lower confidence bounds
5. Shows the result as a line chart with a plain English explanation

---

## Project Structure

```
DataLens/
│
├── app.py              # Streamlit UI and session management
├── main.py             # CSV loading, cleaning, column detection
├── llm.py              # Google Gemini integration and prompt
├── engine.py           # Analysis logic, filtering, forecasting
├── visualisation.py    # Chart generation using Plotly
├── pyproject.toml      # Dependencies managed by uv
└── .env                # API keys (not committed to GitHub)
```

Each file has one clear job. I kept them separate so the code stays readable and easy to debug.

---

## Data Cleaning (happens automatically)

Before any analysis runs, the data goes through automatic cleaning:

- **Duplicates** are removed
- **Column types** are auto detected — numerical, categorical, datetime
- **Missing values** are handled smartly:
  - Numerical columns → filled with column mean
  - Categorical columns → filled with most frequent value
  - Datetime columns → rows with missing dates are dropped

None of this requires any input from the user. It all happens in the background when you click Analyze.

---

## Tech Stack

| Tool | What I used it for |
|---|---|
| Python | Core language |
| Streamlit | Web UI and chat interface |
| Google Gemini (gemini-2.5-flash) | Natural language to JSON conversion |
| LangChain | Gemini API integration |
| Pandas | Data manipulation |
| Plotly | Interactive charts |
| Prophet | Time series forecasting |
| uv | Dependency management |
| python-dotenv | API key management |

---

## How To Run It Locally

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/datalens.git
cd datalens
```

**2. Install uv (if you don't have it)**
```bash
pip install uv
```

**3. Install dependencies**
```bash
uv sync
```

**4. Add your Gemini API key**

Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your_api_key_here
```

You can get a free API key from [Google AI Studio](https://aistudio.google.com)

**5. Run the app**
```bash
uv run streamlit run app.py
```

---

## Requirements

Dependencies are managed using `uv`. See `pyproject.toml` for the full list.

---

## Example Questions To Try

Once you upload a CSV with sales data, try asking:

- *What is the total sales?*
- *Show me average profit by category*
- *Top 5 products by sales*
- *Show a bar chart of sales by region*
- *Total sales in North region*
- *Forecast sales for the next 3 months*
- *Show me top 3 products in the Electronics category*

---

## What I Learned Building This

The biggest thing I learned is that in a GenAI project, the LLM is just one piece. The real work is everything around it — the data pipeline, the execution engine, the UI, the error handling. Anyone can call an API. The skill is in building a complete system around it.

I also learned that prompt engineering matters a lot. Getting Gemini to return consistent, parseable JSON required a lot of iteration on the prompt rules. Small changes in wording change the output significantly.

---

## Limitations

- Works only with CSV files for now
- Forecasting works best when you have at least 12-24 data points
- Complex multi-step questions might not always parse correctly
- Free tier Gemini API has rate limits

---

*Built by Abhijith — open to GenAI and Data Engineer fresher roles*