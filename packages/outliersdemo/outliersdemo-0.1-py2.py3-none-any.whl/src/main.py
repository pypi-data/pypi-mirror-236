# src/main.py 

def find_outliers(df):
    outlier_cols = {}
    
    for col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        
        if not outliers.empty:
            outlier_cols[col] = outliers.tolist()
            
    if not outlier_cols:
        print("There are no outliers")
        
    return outlier_cols