from langchain_google_genai import ChatGoogleGenerativeAI  
import json
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def ask_gemini(question,columns):
    prompt=f''' You are a senior Data Analyst AI.
    Dataset columns:{columns}
    User question:{question}

    Your task is to analyze the user question and convert it into JSON instructions.

    RULES:
    1. All calculations must be returned inside "analysis".
    Example:

    {{"analysis":[
    {{"operation":"sum",
    "column":"sales",
    "group_by":null}}
    ]}}

    Allowed Operations: sum, mean, max, min, count, median, mode

    2.If the user asks for top or highest values then return JSON like:

    {{"analysis":[
    {{"operation":"top_n",
    "column":"sales",
    "group_by":null,
    "n":5 }}
    ]}}

    3.If the user asks for lowest, bottom, or least values, return JSON like:

    {{"analysis":[
    {{"operation":"bottom_n",
    "column":"sales",
    "group_by":null,
    "n":5 }}
    ]}}
    

    4. If the user asks for visualization return JSON like:
    {{"chart":"line",
    "x_axis" :"date",
    "y_axis" :"sales",
    "group_by":null
    }}

    Allowed charts: line, bar, histogram, scatter, pie, box

    Chart selection rules:
    line → trends over time  
    bar → compare categories  
    histogram → distribution of a single numeric column 
    scatter → relationship between 2 numeric columns  
    pie → part of whole comparison
    box → compare distribution of a numeric column across categories and detect outliers
    
     5. If the user wants to filter data, add a "filter" key:
    {{"filter":[{{"column":"region","operator":"equals","value":"North"}}]}}
    Operators: equals, greater_than, less_than, contains
    Filter can combine with analysis or chart keys.
    IMPORTANT: When the user mentions a specific value to narrow down the data, use filter. When the user mentions a column name to group or compare, use group_by or analysis.
    Examples:
    - "sales in North" → filter (North is a specific value)
    - "sales by region" → group_by (region is a column name)
    - "profit for VIP customers" → filter (VIP is a specific value)
    - "profit by customer segment" → group_by (customer segment is a column name)
    RETURN only valid JSON instructions. Do not add any explanations.

    6. If the user asks for forecast or predict or future values, return JSON like:
    {{"action":"forecast",        
    "column":"sales",
    "date_column":"date",
    "periods":3}}

    IMPORTANT: Only use column names from the dataset columns listed.Strictly do not invent any new columns or column names.

    '''
    response=llm.invoke(prompt)
    text=response.content.strip()
    text = text.replace("```json", "").replace("```", "").strip() #to remove the markdown formatting 
    try:
        return json.loads(text) #converts the json string to a python dictionary
    except Exception as e:
        return {"error": "Invalid JSON", "raw_output": text}
 #Forecast is a single action, not multiple operations like analysis. You'll never forecast two columns at the same time, so a list is unnecessary complexity. A flat dictionary is simpler to read in engine.py
 
def generate_insight(question,results):
    prompt = f"""
    User question: {question}

    Analysis results:
    {results}

    Explain the results in simple plain English.
    Provide a short insight for a business user.
     Do not assume any currency symbol. If the dataset contains city or country names, infer the appropriate currency symbol from context. If currency cannot be determined, just use the plain number without any symbol
    """

    response = llm.invoke(prompt)
    return response.content