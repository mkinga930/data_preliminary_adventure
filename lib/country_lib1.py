import glob

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



class CoutriesDataValidator:
    """
    Helper class that contains some methods to work on df with data for countries
    """

    @staticmethod
    def combine_df(folder_path):
        """Combines csv files from given location into one data frame."""
        df_list = []
        for file in glob.glob(folder_path):
            df_list.append(pd.read_csv(file))
        df = pd.concat(df_list, sort=False)
        return df

    @staticmethod
    def clean_data(data_to_be_cleaned: pd.DataFrame, series_to_convert_to_floats: list, columns_to_remove: list, ) -> pd.DataFrame:
        """Df cleaning method by removing given columns, converting str data to floats and strips country names from '*' """
        cleaned_data = data_to_be_cleaned
        #remove unwanted columns
        cleaned_data = cleaned_data.drop(columns_to_remove, axis=1)
        #convert data to floats
        cleaned_data[series_to_convert_to_floats] = \
            cleaned_data[series_to_convert_to_floats].apply(lambda col: col.replace(',', '.', regex=True))
        cleaned_data[series_to_convert_to_floats] = \
            cleaned_data[series_to_convert_to_floats].apply(lambda col: col.astype(float))
        cleaned_data['Country'] = cleaned_data['Country'].apply(lambda col: col.strip('*'))
        return cleaned_data

    @staticmethod
    def group_by_region(df: pd.DataFrame) -> pd.DataFrame:
        grouped_data = df.groupby('Region').agg([min, max, 'mean', 'median'])
        grouped_data = grouped_data.sort_values('median', ascending=False)
        return grouped_data

    @staticmethod
    def generate_correlations(df):
        sns.pairplot(df, kind="scatter")
        plt.savefig('../data/correlation_fig.png')
    
    @staticmethod
    def make_subplots_year_dependent(df):
        x = df['Year']      
        # making subplots
        fig, ax = plt.subplots(2, 3)

        # set data with subplots and plot
        ax[0, 0].plot(x, df['Happiness Score'])
        ax[0, 1].plot(x, df['Economy (GDP per Capita)'])
        ax[0, 2].plot(x, df['Family (Social Support)'])
        ax[1, 0].plot(x, df['Health (Life Expectancy)'])
        ax[1, 1].plot(x, df['Freedom'])
        ax[1, 2].plot(x, df['Trust (Government Corruption)'])

        # set the title to subplots
        ax[0, 0].set_title("Happieness")
        ax[0, 1].set_title("Economy")
        ax[0, 2].set_title("Family")
        ax[1, 0].set_title("Health")
        ax[1, 1].set_title("Freedom")
        ax[1, 2].set_title("Trust_gov")

        # set spacing
        fig.tight_layout()
        plt.show()

    @staticmethod    
    def make_multiple_lines_plot(df, name):
        x = df['Year']
        plt.plot(x, df['Happiness Score'], label = "Happieness")
        plt.plot(x, df['Economy (GDP per Capita)'], label = "Economy")
        plt.plot(x, df['Family (Social Support)'], label = "Family")
        plt.plot(x, df['Health (Life Expectancy)'], label = "Health")
        plt.plot(x, df['Freedom'], label = "Freedom")
        plt.plot(x, df['Trust (Government Corruption)'], label = "Trust_gov")
        plt.title(name)

        plt.legend()
        plt.show()