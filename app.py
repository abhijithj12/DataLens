
import streamlit as st
from main import load_csv, clean_and_detect_columns, handle_missing_values
from llm import ask_gemini, generate_insight
from engine import execute,forecast
from visualisation import visualize
import plotly.express as px

st.title("DataLens")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

file_uploaded = st.sidebar.file_uploader("UPLOAD A FILE", type=["csv"], accept_multiple_files=False)
button = st.sidebar.button("Analyze")

if button:
    if file_uploaded:
        try:
            df = load_csv(file_uploaded)
            df, metadata = clean_and_detect_columns(df)
            df, metadata = handle_missing_values(df, metadata)
            st.session_state["df"] = df

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.warning("Please upload a file")

if "df" in st.session_state:
    df = st.session_state["df"]
    st.dataframe(df.head())
    st.subheader("Dataset Summary")
    rows, columns = df.shape
    st.write(f"Rows: {rows}")
    st.write(f"Columns: {columns}")
    st.write(f"Total Missing Values: {df.isna().sum().sum()}")
    st.dataframe(df.dtypes.astype(str))

# ── Render history (single source of truth) ──────────────────
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        if message["content"]["text"]:
            st.write(message["content"]["text"])
        if message["content"]["chart"] is not None:
            st.plotly_chart(message["content"]["chart"])

# ── Handle new question ───────────────────────────────────────
question = st.chat_input("Ask about your dataset")

if question and "df" in st.session_state:
    df = st.session_state["df"]

    # Store & render user message
    st.session_state["messages"].append({
        "role": "user",
        "content": {"text": question, "chart": None}
    })
    with st.chat_message("user"):
        st.write(question)

    # Process
    instructions = ask_gemini(question, df.columns.tolist())
    
    results, fig, insights = None, None, None

    if "error" in instructions:
        insights = f"LLM error: {instructions.get('raw_output', '')}"
    else:
        if "analysis" in instructions:
            results = execute(df, instructions)
        if "chart" in instructions:
            fig = visualize(df, instructions)
            if isinstance(fig, str):  # visualize() returned an error string
                fig = None
        if 'action' in instructions:
            results = forecast(df, instructions)
            results_df= results.rename(columns={'ds': 'Date', 
                                               'yhat': f'Predicted {instructions["column"]}', 
                                               'yhat_lower': 'Minimum Expected', 
                                               'yhat_upper': 'Maximum Expected'})
            st.dataframe(results_df)  # show as table

            fig = px.line(results, x='ds',y=['yhat', 'yhat_lower', 'yhat_upper'],title='Forecast', labels={'ds': 'Date', 'value': instructions["column"], 'variable': 'Forecast'})
            newnames = {
                'yhat': f'Predicted {instructions["column"]}', 
                'yhat_lower': 'Minimum Expected',
                'yhat_upper': 'Maximum Expected'}
            fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
            insights = generate_insight(question, results.to_string())
            # for_each_trace is a builin function in plotly that loops through every line/bar/point in the chart
        
        if results is not None and insights is None:
            insights = generate_insight(question, results)

    # Store & render assistant message
    st.session_state["messages"].append({
        "role": "assistant",
        "content": {"text": insights, "chart": fig}
    })
    with st.chat_message("assistant"):
        if insights:
            st.write(insights)
        if fig is not None:
            st.plotly_chart(fig)