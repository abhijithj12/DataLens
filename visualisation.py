import plotly.express as px
from engine import apply_filters

def visualize(df,instructions):
    df=apply_filters(df,instructions)
    if 'chart' in instructions:
        chart=instructions.get('chart')
        x_axis=instructions.get('x_axis')
        y_axis=instructions.get('y_axis')
        group_by=instructions.get('group_by',None) #sometimes json string will not have group_by
        try:
            if chart=='line':
                fig=px.line(df,x=x_axis,y=y_axis,color=group_by)
            elif chart =='bar':
                fig=px.bar(df,x=x_axis,y=y_axis,color=group_by)
            elif chart=='scatter':
                fig=px.scatter(df,x=x_axis,y=y_axis,color=group_by)
            elif chart=='histogram':
                fig=px.histogram(df,x=x_axis)
            elif chart=='pie':
                fig=px.pie(df,names=x_axis,values=y_axis)
            elif chart=='box':
                fig=px.box(df,x=x_axis,y=y_axis,color=group_by)

            else:
                return "Unsupported chart type"
        
        except Exception as e:
            return f"Visualization error: {e}"
        return fig