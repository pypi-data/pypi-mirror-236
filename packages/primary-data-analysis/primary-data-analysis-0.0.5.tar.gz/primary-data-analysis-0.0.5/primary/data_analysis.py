import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance


def convert_plotly_plots_to_html(fig, no, path):
    fig.write_html(path + '/file'+str(no)+'.html')
    return (no+1)


def convert_df_to_plotly_table(df, title=""):

    rowEvenColor = '#7094db'
    rowOddColor = '#adc2eb'
    n = len(list(df.columns))
    fig = go.Figure(data=[go.Table(
        columnwidth=[1000]*n,
        header=dict(values=list(df.columns),
                    line_color='white',
                    fill_color='#24478f',
                    align=['left', 'center'],
                    font=dict(color='seashell', size=15),
                    height=50),

        cells=dict(values=df.transpose().values.tolist(),
                   line_color='white',
                   fill_color=[[rowOddColor, rowEvenColor]*1000],
                   align=['left', 'center'],
                   font=dict(color='black', size=15),
                   height=40
                   ))])

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="#feffe7",
        title=title
    )
    return fig


def dataframe_describe(df):
    describe = df.describe()
    describe = describe.T
    describe = describe.reset_index()
    describe = describe.round(2)
    return describe


def numerical_analysis(df):
    count_columns = df.count().reset_index()
    count_columns.rename({0: 'Total_count'}, axis=1, inplace=True)
    unique_values_columns = df.nunique().reset_index()
    unique_values_columns.rename({0: 'Unique_count'}, axis=1, inplace=True)
    duplicate_values = (df.count()-df.nunique()).reset_index()
    duplicate_values.rename({0: 'Duplicate_count'}, axis=1, inplace=True)
    missing_values = df.isnull().sum().reset_index()
    missing_values.rename({0: 'Missing_values'}, axis=1, inplace=True)
    non_missing_values = df.notnull().sum().reset_index()
    non_missing_values.rename({0: 'Non_missing_values'}, axis=1, inplace=True)
    fill_rate = ((1-((df.isnull().sum())/len(df)))*100).reset_index()
    fill_rate.rename({0: "Fill_rate_percent"}, axis=1, inplace=True)
    data_types = df.dtypes.astype("string").reset_index()
    data_types.rename({0: "Data_types"}, axis=1, inplace=True)
    numerical_analyis = count_columns.merge(unique_values_columns).merge(duplicate_values).merge(
        missing_values).merge(non_missing_values).merge(fill_rate).merge(data_types)
    return numerical_analyis


def correlation_matrix(df):
    df_corr = df.corr()
    x = list(df_corr.columns)
    y = list(df_corr.index)
    z = np.array(df_corr)

    fig = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=np.around(z, decimals=2),
        hoverinfo='z',
        colorscale='Agsunset'
    )
    fig.layout.margin.update({'t': 200})
    fig.layout.update({'title': 'Correlation Matrix'})
    return fig


def stastical_summary(df, target):
    cols = list(df._get_numeric_data().columns)
    x = df[cols]
    y = df[target]
    x = sm.add_constant(x)
    x = x.fillna(0)
    df = df.fillna(0)
    model = sm.OLS(y, x)
    results = model.fit()
    results_as_html = results.summary().tables[1].as_html()
    stat_result = pd.read_html(results_as_html, header=0, index_col=0)[0]
    stat_result = stat_result.reset_index()
    stat_result = stat_result.round(2)
    return stat_result


def general_data_statistics(df):
    no_of_rows = len(df)
    num_cols = len(list(df.columns))
    duplicate = len(df)-len(df.drop_duplicates())
    duplicate_percent = duplicate*100/len(df)
    non_duplicate = len(df.drop_duplicates())
    missing_cells = df.isnull().sum().sum()
    missing_cells_percent = missing_cells*100/(len(df)*num_cols)
    D = {"No_of_rows": no_of_rows,
         "No_of_columns": num_cols,
         "Duplicate_rows_count": duplicate,
         "Duplicate_rows_percent": duplicate_percent,
         "Unique_rows_count": non_duplicate,
         "Missing_cells_count": missing_cells,
         "Missing_cells_percent": missing_cells_percent
         }
    general_info = pd.DataFrame(D, index=["0"])
    general_info = general_info.T
    general_info = general_info.reset_index()
    general_info = general_info.round()
    general_info.rename({"index": 'Dataset_statistics'}, axis=1, inplace=True)
    general_info.rename({"0": 'Values'}, axis=1, inplace=True)
    return general_info


def Feature_Importance(df_train, df_test, model):
    p = model.feature_importances_
    # Create a dataframe to store the featues and their corresponding importances
    feature_rank = pd.DataFrame({'feature_name': df_train.columns,
                                 'feature_importance': model.feature_importances_})
    feature_rank = feature_rank.sort_values(
        'feature_importance', ascending=True)
    fig = px.bar(feature_rank, x="feature_importance", y="feature_name", orientation='h',
                 color="feature_importance", color_continuous_scale='Plotly3',  title="Feature Importance")
    return fig


def Permutation_Importance(df_train, df_test, model):
    result = permutation_importance(model, df_train, df_test)
    # Create a dataframe to store the featues and their corresponding importances
    feature_rank = pd.DataFrame({'feature_name': df_train.columns,
                                 'permutation_importance': result.importances_mean})
    feature_rank = feature_rank.sort_values(
        'permutation_importance', ascending=True)
    fig = px.bar(feature_rank, x="permutation_importance", y="feature_name", orientation='h',
                 color="permutation_importance", color_continuous_scale='Plotly3', title="Permutation Importance")
    return fig


def Correlation_With_Target(df, target):
    corr = df.corrwith(df[target], axis=0)
    val = [str(round(v, 2) * 100) + '%' for v in corr.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(y=corr.index, x=corr.values,
                         orientation='h',
                         marker_color='#9900cc',
                         text=val,
                         textposition='outside',
                         textfont_color='black'))
    fig.update_layout(title="Correlation with Target",
                      width=800,
                      height=3000)
    fig.update_xaxes(range=[-2, 2])
    return fig


def preprocessing_df(df):
    cols = list(df._get_numeric_data().columns)
    object_cols = [col for col in list(df.columns) if col not in cols]
    df[cols] = df[cols].fillna(0)
    df[object_cols] = df[object_cols].apply(
        lambda x: x.fillna(x.value_counts().index[0]))
    labelencoder = LabelEncoder()
    for i in object_cols:
        df[i] = labelencoder.fit_transform(df[i])
    return df


html_string_start = '''
<html>
  <head>
      <title>PRIMARY DATA ANALYSIS REPORT</title>
      <link rel="stylesheet" type="text/css" href="../mystyle.css"/>

      <style>
            body {
  background-color: #feffe7;
}
iframe {
  margin: 0 10%;
  border: none;
  width: 80%;
  height: 600px;
  background-color: #feffe7;
}

.title {
  color: #072292;
  font-family: sans-serif;
  text-align: center;
  font-size: 35px;
  font-family: fantasy;
}

.iframe-container {
  overflow: hidden;
  /* Calculated from the aspect ration of the content (in case of 16:9 it is 9/16= 
    0.5625) */
  padding-top: 56.25%;
  position: relative;
}
.iframe-container iframe {
  border: 0;
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}
      </style>


  </head>
  <body>
      <div class='title'>DATA ANALYSIS REPORT</div>
'''

html_string_end = '''
  </body>
</html>
'''


def get_all_data_analysis_classification(df, target, path="."):
    no = 1

    if not os.path.exists(path):
        os.makedirs(path)

    # sample values for each column of dataframe
    sample_top = df.head(5)
    sample_top = sample_top.T
    sample_top = sample_top.reset_index()
    sample_top.rename({'index': 'Column_name'}, axis=1, inplace=True)
    fig_sample_top = convert_df_to_plotly_table(
        sample_top, title="Data samples for each column")
    no = convert_plotly_plots_to_html(fig_sample_top, no, path)

    # general data stats
    data_stats = general_data_statistics(df)
    fig_data_stats = convert_df_to_plotly_table(
        data_stats, title="General Data Statistics")
    no = convert_plotly_plots_to_html(fig_data_stats, no, path)

    # Describe dataset
    describe = dataframe_describe(df)
    fig_desc = convert_df_to_plotly_table(
        describe, title="Dataset Description")
    no = convert_plotly_plots_to_html(fig_desc, no, path)

    # Numerical analyis for dataset
    numerical_analyis = numerical_analysis(df)
    fig_num_analyis = convert_df_to_plotly_table(
        numerical_analyis, title='Numerical Analysis for Dataset')
    no = convert_plotly_plots_to_html(fig_num_analyis, no, path)

    # Distribution of target value
    pie = df[target].value_counts().reset_index()
    fig = px.pie(pie, values=target, names="index",
                 title='Distribution of target Value')
    no = convert_plotly_plots_to_html(fig, no, path)

    # box plot for outlier detection
    cols = list(df._get_numeric_data().columns)
    for col in cols:
        fig = px.box(df, x=col, color=target, title='Box plot for ' +
                     col + ' outlier detection w.r.t target Value ')
        fig.update_traces(boxpoints='all', jitter=.3)
        no = convert_plotly_plots_to_html(fig, no, path)

    # histogram for distribution check
    for col in list(df.columns):
        fig = px.histogram(df, x=col, color=target, marginal="violin", title='Histogram for ' +
                           col + ' Distribution w.r.t target Value')
        no = convert_plotly_plots_to_html(fig, no, path)

    # correlation heatmap plotly
    fig = correlation_matrix(df)
    no = convert_plotly_plots_to_html(fig, no, path)

    # preprocess data
    df = preprocessing_df(df)

    # Stastical summary for classification problem showing many p-value for statastical significance of variables
    stat_result = stastical_summary(df, target)
    stat_result_fig = convert_df_to_plotly_table(
        stat_result, title="p-value For Statastical Significance of Variables")
    no = convert_plotly_plots_to_html(stat_result_fig, no, path)

    # classifier
    X = df[[col for col in list(df.columns) if col not in [target]]]
    y = df[target]
    model = RandomForestClassifier()
    model.fit(X, y)

    # feature importance
    fig = Feature_Importance(X, y, model)
    no = convert_plotly_plots_to_html(fig, no, path)

    # permutation importance
    fig = Permutation_Importance(X, y, model)
    no = convert_plotly_plots_to_html(fig, no, path)

    # correlation with target variable
    fig = Correlation_With_Target(df, target)
    no = convert_plotly_plots_to_html(fig, no, path)

    # pair plot
    fig = ff.create_scatterplotmatrix(df, diag='histogram', index=target, colormap='Rainbow',
                                      colormap_type='cat', height=1500, width=1500)
    no = convert_plotly_plots_to_html(fig, no, path)

    with open(path+'/CLASSIFICATION_DATA_ANALYSIS_REPORT.html', 'w') as f:
        f.write(html_string_start)
        for n in range(no-1):
            i = (n+1)
            s = f'<iframe id="iframe{i}" sandbox="allow-scripts allow-same-origin allow-modals"  src="file{i}.html"></iframe>\n'
            f.write(s)

        f.write(html_string_end)


def get_all_data_analysis_regression(df, target, path="."):
    no = 1

    if not os.path.exists(path):
        os.makedirs(path)

    # first sample of dataset
    sample_top = df.head(5)
    sample_top = sample_top.T
    sample_top = sample_top.reset_index()
    sample_top.rename({'index': 'Column_name'}, axis=1, inplace=True)
    fig_sample_top = convert_df_to_plotly_table(
        sample_top, title="Data samples for each column")
    no = convert_plotly_plots_to_html(fig_sample_top, no, path)

    # general data stats
    data_stats = general_data_statistics(df)
    fig_data_stats = convert_df_to_plotly_table(
        data_stats, title="General Data Statistics")
    no = convert_plotly_plots_to_html(fig_data_stats, no, path)

    # Describe dataset
    describe = dataframe_describe(df)
    fig_desc = convert_df_to_plotly_table(
        describe, title="Dataset Description")
    no = convert_plotly_plots_to_html(fig_desc, no, path)

    # Numerical analyis for dataset
    numerical_analyis = numerical_analysis(df)
    fig_num_analyis = convert_df_to_plotly_table(
        numerical_analyis, title='Numerical Analysis for Dataset')
    no = convert_plotly_plots_to_html(fig_num_analyis, no, path)

    # Distribution of target value
    fig = px.histogram(df, x=target, marginal="violin",
                       title='Histogram for ' + target + ' Distribution')
    no = convert_plotly_plots_to_html(fig, no, path)

    # box plot for outlier detection
    cols = list(df._get_numeric_data().columns)
    for col in cols:
        fig = px.box(df, x=col, title='Box plot for ' +
                     col + ' outlier detection')
        fig.update_traces(boxpoints='all', jitter=.3)
        no = convert_plotly_plots_to_html(fig, no, path)

    # histogram for distribution check
    for col in list(df.columns):
        fig = px.histogram(df, x=col, marginal="violin",
                           title='Histogram for ' + col + ' Distribution')
        no = convert_plotly_plots_to_html(fig, no, path)

    # label encode categorical variables
    labelencoder = LabelEncoder()
    object_cols = [col for col in list(df.columns) if col not in cols]
    for i in object_cols:
        df[i] = labelencoder.fit_transform(df[i])

    # correlation heatmap plotly
    fig = correlation_matrix(df)
    no = convert_plotly_plots_to_html(fig, no, path)
    fig.show()

    # Stastical summary for classification problem showing many p-value for statastical significance of variables
    stat_result = stastical_summary(df, target)
    stat_result_fig = convert_df_to_plotly_table(
        stat_result, title="p-value For Statastical Significance of Variables")
    no = convert_plotly_plots_to_html(stat_result_fig, no, path)

    # classifier
    X = df[[col for col in list(df.columns) if col not in [target]]]
    y = df[target]
    model = RandomForestRegressor()
    model.fit(X, y)

    # feature importance
    fig = Feature_Importance(X, y, model)
    no = convert_plotly_plots_to_html(fig, no, path)

    # permutation importance
    fig = Permutation_Importance(X, y, model)
    no = convert_plotly_plots_to_html(fig, no, path)

    # correlation with target variable
    fig = Correlation_With_Target(df, target)
    no = convert_plotly_plots_to_html(fig, no, path)

    # pair plot
    fig = ff.create_scatterplotmatrix(df, diag='histogram', colormap='Rainbow',
                                      colormap_type='cat', height=1500, width=1500)
    no = convert_plotly_plots_to_html(fig, no, path)

    with open(path+'/REGRESSION_DATA_ANALYSIS_REPORT.html', 'w') as f:
        f.write(html_string_start)
        for n in range(no-1):
            i = (n+1)
            s = f'<iframe id="iframe{i}" sandbox="allow-scripts allow-same-origin allow-modals"  src="file{i}.html"></iframe>\n'
            f.write(s)

        f.write(html_string_end)
