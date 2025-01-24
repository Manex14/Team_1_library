from Team_1_library import Automatic_Preprocess, Manual_Preprocess
import pandas as pd
import numpy as np


##Example automatic preprocess

data = {'Name':['Hodei','Mikel','Oier','Iraitz','Paul','Enaut'],
        'Age':[35,70,23,68,19,69],
        'Retired':[False,True,False,True,False,np.nan],
        'car_amount': [1,2,0,1,1,np.nan],
        'salary': [2200.,1200.,1700.,10000.,800.,1000.],
        'low_variance':[1.,1.,1.,1.,1.,1],
        'empty':[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
}

df = pd.DataFrame(data)

print("\n\nOriginal dataframe")
print(df)

# Class instance with personaliced parameters
preprocessor = Automatic_Preprocess(df_original=df, empty_threshold=0.5, clustering=[False,False,True,False,False,False,False],numeric_var='mode',object_var='ffill')

# Run th preprocessing
df_preprocessed_a = preprocessor.run()

print("\nAutomatically preprocessed dataframe")
print(df_preprocessed_a)

##Example manual preprocess

data = {'Uni':['Mondra','Mondragon','Mondragon','Mondrogon','Mondra','Mondragon'],
        'Name':[' Haritz','Ainara','Jose Miguel',' Luis','Oier','Urko'],
        'Age':[40,50,-70,1000,2,65],
        'Salary': [np.nan,1500,2000,1300,650,1800]
        }

df = pd.DataFrame(data)

print("Original dataframe")
print(df)

preprocessor = Manual_Preprocess(df)

preprocessor.turn_positive(['Age'])
preprocessor.fill_nan(['Salary'])
preprocessor.correct_outliers(['Age'])
preprocessor.correct_string_errors(['Uni','Name'])
df_preprocessed_m = preprocessor.normalize_string(['Uni','Name'])     ##Note that to return the dataset you need to asign it to a variable

print("\nManualy prerpocessed dataframe")
print(df_preprocessed_m)