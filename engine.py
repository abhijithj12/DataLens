from prophet import Prophet
import pandas as pd

def apply_filters(df, instructions):
    for f in instructions.get('filter', []):
        col, op, val = f['column'], f['operator'], f['value']
        if op == 'equals': 
            df = df[df[col] == val]
        elif op == 'greater_than': 
            df = df[df[col] > val]
        elif op == 'less_than': 
            df = df[df[col] < val]
        elif op == 'contains': 
            df = df[df[col].astype(str).str.contains(val, case=False)]
    return df
def execute(df,instructions):
    df = apply_filters(df, instructions)
    results=[]

    if 'analysis' in instructions:
        for  i in instructions['analysis']:
            column=i['column']
            operation=i['operation']
            group_by=i.get('group_by',None) #sometimes json string will not have group_by
            n=i.get('n',5)
            filtered_df = apply_filters(df, i)
            try:
                if operation=='top_n':
                    if group_by is None :
                        result=filtered_df[column].sort_values(ascending=False).head(n)
                        results.append(result)       
                    else:
                        result=filtered_df.groupby(group_by)[column].sum().sort_values(ascending=False).head(n)
                        results.append(result) # i used .sum() to get the sum values per group so each group has a single total to sort and find the top n

                elif operation=='bottom_n':
                    if group_by is None:
                        result=df[column].sort_values(ascending=True).head(n)
                        results.append(result)
                    else:
                        result=df.groupby(group_by)[column].sum().sort_values(ascending=True).head(n)         
                        results.append(result)

                else:
                    if group_by is None:
                        result=df[column].agg(operation)
                    else:
                         result=df.groupby(group_by)[column].agg(operation)
                    results.append(result)
            except Exception as e:
                results.append( f"Analysis error: {e}")
                
        return results

def forecast(df,instructions):
    if 'action' in instructions:
        dates=instructions['date_column']
        column=instructions['column']
        action=instructions['action']
        periods=instructions.get('periods',5)
        if action=='forecast':
            df=df[[dates,column]]
            forecast_df=df.rename(columns={dates:'ds',column:'y'})  #for prophet we need to rename columns
        
        # detect frequency that is the difference between dates automatically
            freq=pd.infer_freq(forecast_df['ds'])
            if freq is None:
                freq='MS'  # default to monthly if can't detect
        
            p=Prophet()
            p.fit(forecast_df)
            future=p.make_future_dataframe(periods=periods,freq=freq)
            forecast_result=p.predict(future)
            forecast_result['yhat'] = forecast_result['yhat'].clip(lower=0)
            forecast_result['yhat_lower'] = forecast_result['yhat_lower'].clip(lower=0)
            return forecast_result[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)

