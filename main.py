import pandas as pd



def load_csv(file_uploaded):
    df = pd.read_csv(file_uploaded)
    return df

def clean_and_detect_columns(df):
    ''' Function to clean and detect columns '''
    df=df.drop_duplicates()

    numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    datetime_columns = []

    for column_name in categorical_columns.copy():
        converted=pd.to_datetime(df[column_name], errors='coerce') #Try to convert text column to datetime
        valid_percentage=converted.notna().mean()                   #Calculate percentage of valid values
        if valid_percentage>0.8:                                    #If more than 80% of values are valid dates
            df[column_name]=converted                               #Replace original column with datetime version
            datetime_columns.append(column_name)
            categorical_columns.remove(column_name)                 #Remove that column from categorical columns
        
    metadata={
        'numerical_columns':numerical_columns,
        'categorical_columns':categorical_columns,
        'datetime_columns':datetime_columns
    }
    return df,metadata


def handle_missing_values(df,metadata):
    ''' Function to handle missing values '''
    numerical_columns=metadata['numerical_columns']
    categorical_columns=metadata['categorical_columns'] 
    datetime_columns=metadata['datetime_columns']   

    for column_name in numerical_columns:
        df[column_name]=df[column_name].fillna(df[column_name].mean())

    for column_name in categorical_columns:
        df[column_name]=df[column_name].fillna(df[column_name].mode()[0])

    for column_name in datetime_columns:
        if df[column_name].isna().sum()>0:
            df=df.dropna(subset=[column_name])

    return df,metadata