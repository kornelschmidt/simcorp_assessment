import pandas as pd

#static input, would be passed through if not for demonstration purposes
filename_sept = "universe_2023_09_28.csv"
filename_oct = "universe_2023_10_04.csv"

class model_universe:
    def __init__(self, filename):
        self.model_universe_df = pd.read_csv(filename)
    def find_largest_smallest_rows(self, df, n, market_cap=False):
        #finds largest or smallest rows based on a particular column
        if market_cap == True:
            return df.nlargest(n, 'MARKET CAP')
        if df.shape[0] < n * 2:
            return df
        return pd.concat([df.nlargest(n, 'RETURN'), df.nsmallest(n, 'RETURN')])
    def compare_df(self, comparison_file):
        #return the number of positions present in comparison_file that are not in self.model_universe_df
        comparison_df = pd.read_csv(comparison_file)
        ID = 'AXIOMA_ID'
        compare_against = self.model_universe_df[ID].tolist()
        not_found = ~comparison_df[ID].isin(compare_against)
        return comparison_df[not_found].shape[0]
    def filtered_rows_country(self, n, market_cap=False):
        #return either the n top and bottom returns by country, or n largest market caps if market_cap = True
        if market_cap == True:
            self.model_universe_df['MARKET CAP'] = self.model_universe_df['PRICE'] * self.model_universe_df['TSO']
            filtered_df = self.model_universe_df.groupby('COUNTRY', group_keys=False).apply(lambda x: self.find_largest_smallest_rows(x, n=n, market_cap=market_cap))
            return filtered_df
        top_and_bot_df = self.model_universe_df.groupby('COUNTRY', group_keys=False).apply(lambda x: self.find_largest_smallest_rows(x, n=n))
        return top_and_bot_df
    
def test_compare_df():
    file1 = 'test_model_universe.csv' #september file above
    file2 = 'test_compare_df_file2.csv' #october file above
    test_model_universe = model_universe(file1)
    assert test_model_universe.compare_df(file2) == 4955

def test_filtered_rows_country_return():
    test_file = 'test_model_universe.csv'
    test_model_universe = model_universe(test_file)
    comparison_df = pd.read_csv('test_filtered_rows_country_return_comp.csv', index_col=0)
    assert test_model_universe.filtered_rows_country(3, False).equals(comparison_df)