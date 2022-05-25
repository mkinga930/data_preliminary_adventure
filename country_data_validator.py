import glob
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



class CoutriesDataValidator:
    """
    Helper class that contains some methods to work on df with data for countries
    """

    @staticmethod
    def combine_dfs_from_selected_dir(folder_path: str)  -> pd.DataFrame:
        """
        Combines csv files from given location into one data frame.
        """
        df_list = []
        for file in glob.glob(folder_path):
            df_list.append(pd.read_csv(file))
        df = pd.concat(df_list, sort=False)
        return df

    @staticmethod
    def clean_data(data_to_be_cleaned: pd.DataFrame, series_to_convert_to_floats: list, columns_to_remove: list, ) -> pd.DataFrame:
        """
        Df cleaning method by removing given columns, converting str data to floats, enusres year is int
        and strips country names from '*' 
        """
        cleaned_data = data_to_be_cleaned
        cleaned_data = cleaned_data.drop(columns_to_remove, axis=1)
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
    def generate_correlations(df: pd.DataFrame) -> pd.DataFrame:
        sns.pairplot(df, kind="scatter")
        plt.savefig('../data/correlation_fig.png')
    
    @staticmethod
    def make_subplots_year_dependent(df: pd.DataFrame) -> pd.DataFrame:
        x = df['Year']      

        fig, ax = plt.subplots(2, 3)

        ax[0, 0].plot(x, df['Happiness Score'])
        ax[0, 1].plot(x, df['Economy (GDP per Capita)'])
        ax[0, 2].plot(x, df['Family (Social Support)'])
        ax[1, 0].plot(x, df['Health (Life Expectancy)'])
        ax[1, 1].plot(x, df['Freedom'])
        ax[1, 2].plot(x, df['Trust (Government Corruption)'])

        ax[0, 0].set_title("Happieness")
        ax[0, 1].set_title("Economy")
        ax[0, 2].set_title("Family")
        ax[1, 0].set_title("Health")
        ax[1, 1].set_title("Freedom")
        ax[1, 2].set_title("Trust_gov")

        fig.tight_layout()
        plt.show()

    @staticmethod    
    def make_multiple_lines_plot(df: pd.DataFrame, name: str) -> pd.DataFrame:
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
        
    @staticmethod
    def choose_your_country(most_important_rate: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Allows you to generate a data frame of the country with the best rate for the paramaeter that was given
        """
        
        df = df[df['Year'] == df['Year'].max()]
        if re.match(most_important_rate, 'Happiness Rank'):
            return df[df['Happiness Rank'] == df['Happiness Rank'].min()]

        for column in df.columns:
            if re.match(most_important_rate, column):
                return df[df[column] == df[column].max()]

    @staticmethod
    def compare_two_countries(df: pd.DataFrame, your_country: str, country_to_compare: str, year=None) -> pd.DataFrame:
        """
        This method generates df of two countries that was chosen to compare 
        with data for all years from the report if year is None, or for given year
        """
        
        if year is not None and year not in df['Year'].values:
            raise ValueError(f'No data for year {year} ')
        if year != None:
            df = df[df['Year'] == year]
        return df[(df['Country'] == your_country) | (df['Country'] == country_to_compare)]