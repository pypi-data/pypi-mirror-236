#### This Package is designed to get overall understanding of dataframe.

## Installation

    pip install primary-data-analysis

## Package Import

    from primary import get_all_data_analysis_classification
    from primary import get_all_data_analysis_regression

## Function

    get_all_data_analysis_classification(dataframe, target="target_class_label", path="./desired_folder_name")

### Arguments

    1. Dataframe name (required)
    2. Target label or any categorical variable label (required)
    3. path = name of folder (optional)

## Function

    get_all_data_analysis_regression(dataframe, target="target_continious", path="./desired_folder_name")

### Arguments

    1. Dataframe name (required)
    2. Target continious feature name (required)
    3. path = name of folder (optional)

### Example

    df = pd.read_csv('Iris.csv')
    get_all_data_analysis(df, target="Species", path="iris_analysis")

## Output

    1. Output is in the form of html file which will be saved in the current folder or given path.
    2. All plotly graphs will saved in the current folder or given path.
