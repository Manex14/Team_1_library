import pandas as pd
from scipy import stats
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import VarianceThreshold
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)  ##It disables the warnings in the monitor


def _clustering_imputations(df, col, numeric_var, object_var):
    X = df.copy()

    fill_methods = {
    'mode':  lambda: X[column].fillna(X[column].dropna().mode()[0], inplace=True),
    'ffill': lambda: X[column].ffill(inplace=True),
    'bfill': lambda: X[column].bfill(inplace=True),
}
    for column in X.columns:

        #Filling the copied matrix NaNs with desired variables
        fill_function = fill_methods.get(object_var)
        
        if fill_function:
            fill_function() 

        #Encoding objects
        if X[column].dtype == 'object':   
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column].astype(str))
    
    X = X.drop(columns=[col])  # Exclude the objective column

    # Data sacling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Number of clusters depending on unique values
    n_clusters = df[col].nunique()  
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)  #Cluster creation
    # Impute the values depending on clusters
    for cluster in df['cluster'].unique():
        cluster_rows = df[df['cluster'] == cluster]
        if not cluster_rows[col].isna().all():  # Avoid clusters with no data
            mode_value = cluster_rows[col].mode()[0]  # Cluster's mode
            df.loc[(df['cluster'] == cluster) & (df[col].isna()), col] = mode_value
        else: 
            print('Cluster not encountered for column "%s", imputing statistical variable'%(col))
            df = _statistical_imputation(df,col,numeric_var,object_var)

    # Eliminate cluster column
    df.drop(columns=['cluster'], inplace=True)

    return df

def _statistical_imputation(df,col, numeric_var, object_var):
    col_type =df[col].dtype
    fill_methods = {
        'mean': lambda: df[col].fillna(df[col].mean(),inplace=True),
        'median': lambda: df[col].fillna(df[col].median(),inplace=True),
        'mode':  lambda: df[col].fillna(df[col].mode()[0],inplace=True),
        'ffill': lambda: df[col].ffill(inplace=True),
        'bfill': lambda: df[col].bfill(inplace=True),
}
    if col_type == int  or col_type == float:
        ##FILLNA
        fill_function = fill_methods.get(numeric_var)
        
        if fill_function:
            fill_function()   
        else: print('Error with fill function')   

    elif col_type == object or col_type == bool:
        ##FILLNA

        fill_function = fill_methods.get(object_var)
        
        if fill_function:
            fill_function() 
        else: print('Error with fill function')   
        
    return df
                
def _corregir_outliers(df,col):       ##Outlier correction

    if df[col].dtype == int  or df[col].dtype == float:

        z_scores = stats.zscore(df[col])
        df[col] = df[col].where(abs(z_scores) < 2.2, df[col].mean())

    return df
import pandas as pd
import numpy as np

def _drop_column_if_low_variance(df, col, threshold):

    # only compute in numeric columns
    if pd.api.types.is_numeric_dtype(df[col]):
        col_var = df[col].var()
        if col_var <= threshold:
            df.drop(columns=[col], inplace=True)
            print(f'Column "{col}" deleted due to low variance: ({col_var:.4f}).')
    
    return df


class Automatic_Preprocess:

    def __init__(self,df_original, empty_threshold=0.65, variance_threshold=0.0 ,clustering=True, numeric_var='mean',object_var='mode'):

        pd.set_option('future.no_silent_downcasting', True)
        self.df = df_original.copy()
        self.empty_threshold = empty_threshold
        self.variance_threshold = variance_threshold
        self.numeric_var = numeric_var
        self.object_var = object_var

        if isinstance(clustering, bool):    #If is bool. fill column size array with bool
                    self.clustering = np.full(len(self.df.columns), clustering)

        elif isinstance(clustering, list):  #If list, we check size is correct
            if len(clustering) != len(self.df.columns):
                raise ValueError("List of clustering must be equal size to df columns")
            self.clustering = np.array(clustering)

        else:
            raise ValueError("Parameter 'clustering' must be boolean or array of booleans")

    def run(self):

        for col in self.df.columns:         
            nan_perc = self.df[col].isna().mean()
            ##Drop the column if empty threshold reached
            if nan_perc > self.empty_threshold:
                self.df.drop(columns=[col],inplace=True)
                print(f'Column deleted due to excess of NaN ({nan_perc*100:.2f}%).')
                continue
            ##Drop column if varience threshold surpassed
            self.df = _drop_column_if_low_variance(self.df,col, self.variance_threshold)


        for index, col in enumerate(self.df.columns):
            if self.clustering[index] == True:  #If true for that column, imput by clustering
                self.df = _clustering_imputations(self.df,col,self.numeric_var,self.object_var)
            
            else:
                self.df = _statistical_imputation(self.df,col,self.numeric_var,self.object_var)
            self.df = _corregir_outliers(self.df,col)
        return self.df