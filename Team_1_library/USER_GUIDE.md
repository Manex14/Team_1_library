# User Guide

This guide explains how to use the Team_1_library with detailed descriptions of each function and its arguments.

## Automatic Preprocess

To use the functions of the the Automatic Preprocessor, you need to initialice "Automatic_Preprocess" class by passing required and optional parameters.

#### Parameters
-`df` (pandas DataFrame, required): The dataset to preprocess.
-`empty_threshold` (float,optional): Empty threshold from 0 to 1. (Default = 0.65)
-`variance_threshold` (float,optional): Variance threshold form. (Default = 0.00)
-`clustering` (Bool or list of bool, optional): Method by which the imputations are going to be made:
  - `'True'`: All columns imputed by clustering.
  - `List of booleans` (e.g., `[True,False,...]`): Selected columns imputed by clusterin, other by statistical variables.
  - `'False'`: All columns imputed by statistical variables.

- `numeric_var` (str, optional): The statistical variable  to use in numerical column imputations (opt.). Options:
  - `'mean'` (default): Replaces missing values with column mean.
  - `'median'`: Replaces missing values with column median.
  - `'mode'`: Replaces missing values with column mode.
  - `'ffill'`: Replaces missing values with previous value.
  - `'bfill'`: Replaces missing values with following value.

- `object_var` (str, optional): The statistical variable  to use in categorical column imputations. Options:
  - `'mode'` (default): Replaces missing values with column mode.
  - `'ffill'`: Replaces missing values with previous value.
  - `'bfill'`: Replaces missing values with following value.

#### Functions Overview
- `.run()`: Executes the preprocessing pipeline. 
  - **Parameters**: None.
  - **Returns**: Preprocessed dataset as a pandas DataFrame.

#### Example Usage
Included in the [text](Libreria_equipo_1/example_usage.py) file.


## Manual Preprocess

To use the functions of this the Manual prerpocesser, you need to initialice "Automatic_Preprocess" class. In this case, you only need to pass only the dataset to preprocess, the parameters are unique in each function.

#### Parameters
-`df` (pandas DataFrame, required): The dataset to preprocess.

#### Functions Overview
- `.turn_positive()`: Turns the negative values of the column in positive. 
  - **Parameters**: 
    -`selected_columns` (list, required): List of columns where the function is aplied.
  - **Returns**: Original dataset with the selected columns turned positive as a pandas DataFrame.

- `.fill_nan()`: Fills the NaN values with prefered statistical variable. 
  - **Parameters**: 
    -`selected_columns` (list, required): List of columns where the function is aplied.
    -`var` (str, optional): Name of the statistical variable to replace the NaN's. Options:
      -`'mean'` (default): Replaces missing values with column mean.
      -`'median'`: Replaces missing values with column median.
      -`'mode'`: Replaces missing values with column mode.
      -`'ffill'`: Replaces missing values with previous value.
      -`'bfill'`: Replaces missing values with following value.
  - **Returns**: Original dataset with the selected columns filled as a pandas DataFrame.

- `.correct_outliers()`: Corrects the outliers based on their zscore. 
  - **Parameters**: 
    -`selected_columns` (list, required): List of columns where the function is aplied.
  - **Returns**: Original dataset with the selected columns corrected as a pandas DataFrame.

- `.correct_string_errors()`: Corrects strings with theorical errors approximating them to the most used similar ones.
  - **Parameters**: 
    -`selected_columns` (list, required): List of columns where the function is aplied.
    -`correct_values` (list, optional): List of the correct values to approximate (if not given it is chosen automatically)
  - **Returns**: Original dataset with the selected columns corrected as a pandas DataFrame.

- `.normalize_string()`: Lowers the cases and eliminates the blank spaces of the colum's strings.
  - **Parameters**: 
    -`selected_columns` (list, required): List of columns where the function is aplied.
  - **Returns**: Original dataset with the selected columns normalized as a pandas DataFrame.


#### Example Usage
Included in the [text](Team_1_library/example_usage.py) file.

