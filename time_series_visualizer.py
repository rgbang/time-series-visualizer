import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar

# Function to read and clean data
def clean_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    bottom_percentile = df['value'].quantile(0.025)
    top_percentile = df['value'].quantile(0.975)
    df_clean = df[(df['value'] >= bottom_percentile) & (df['value'] <= top_percentile)]
    return df_clean

# Read and clean data
df = clean_data('fcc-forum-pageviews.csv')

def draw_line_plot():
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()   
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)
    ax.set_title('Average Daily Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=[calendar.month_name[i] for i in range(1, 13)])
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')    
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))    
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')   
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    plt.tight_layout()
    
    fig.savefig('box_plot.png')
    return fig

