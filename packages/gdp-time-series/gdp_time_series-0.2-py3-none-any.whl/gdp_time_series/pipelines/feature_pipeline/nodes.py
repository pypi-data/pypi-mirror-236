import pandas as pd
from .data_extraction import Data_Extraction
from .auxiliary_functions import preprocess_string, process_dict_with_preprocess
from .ft_store_functions import feature_store_creation, feature_view_training_create
import re
import json
import miceforest as mf
import numpy as np

def column_preprocessing():
    data_agent = Data_Extraction()
    data_agent.data_extraction()
    data_agent.data_storing()
    data_agent.update_data()
    df = data_agent.dataframe_rename()
    
    transformed_columns = {c: preprocess_string(c) for c in df.columns}
    df = df.rename(columns=transformed_columns)
    
    for c in df.columns:
        pattern =  r'(_{2,})'
    # Use re.findall() to find all consecutive duplicate words
        consecutive_duplicates = re.findall(pattern, c)
        if consecutive_duplicates:
    # Print the consecutive duplicate words
            transform_string = re.sub(pattern,'_',c)
            df = df.rename(columns = {c:transform_string})
    
    return df

def dataframe_preprocessing(df):
    
    intermediate_df = df.copy()
    
    intermediate_df.reset_index(inplace = True)
    
    intermediate_df.year = pd.to_datetime(intermediate_df.year,format='%Y').apply(lambda date: date.replace(month=12, day=31))

    final_df = intermediate_df.sort_values(by=['year'])
    final_df['unique_id'] = final_df.index
    
    return final_df

def feature_engineering(final_df):
    new_df = final_df.copy()
    #new_df = new_df.astype(float)
    rel_path = 'src/gdp_time_series/pipelines/feature_pipeline/json_files/'
    
    with open(rel_path + 'mice_groups.json', 'r') as j:
     mice_groups = json.loads(j.read())
     
    with open(rel_path + 'economic_groups.json', 'r') as j:
     economic_groups = json.loads(j.read())
     
    with open(rel_path + 'missing_countries.json', 'r') as j:
     missing_countries = json.loads(j.read())
     
    with open(rel_path + 'continents_regions.json', 'r') as j:
     continents_regions = json.loads(j.read())
     
    
    process_dict_with_preprocess(mice_groups)
    process_dict_with_preprocess(economic_groups)
    process_dict_with_preprocess(continents_regions)
    process_dict_with_preprocess(missing_countries)
    
    
    major_advanced_economies =  economic_groups['major_advanced_economies']
    other_advanced_economies =  economic_groups['other_advanced_economies']
    european_union = economic_groups['european_union']
    asean_5 = economic_groups['asean_5']
    euro_area = economic_groups['euro_area']
    emerging_developing_asia = economic_groups['emerging_developing_asia']
    emerging_developing_europe = economic_groups['emerging_developing_europe']
    latin_american_caribean = economic_groups['latin_american_caribean']
    middle_east_central_asia = economic_groups['middle_east_central_asia']
    sub_saharan_africa =  economic_groups['sub_saharan_africa']
    
    african_groups = mice_groups['african_groups']
    african_group_names = mice_groups['african_group_names']

    middle_east_groups = mice_groups['middle_east_groups']
    middle_east_group_names = mice_groups['middle_east_group_names']
    

    missing_african_countries = missing_countries['missing_african_countries']
    missing_middle_east_countries = missing_countries['missing_middle_east_countries']
    remaining_missing_countries = missing_countries['remaining_missing_countries']
    africa = continents_regions['africa']
    central_asia_causasus_countries = continents_regions['central_asia_causasus_countries']
    
    
    def avg_neigh_imputation(neighbours,country):
        return lambda row:np.mean([row[n] for n in neighbours]) if np.isnan(row[country]) else row[country]
    
    def mice_imputation(df,groups,group_names):
        
        df_dict = {str(key):None for key in group_names}
        i = 0
        for group in groups:
            kds = mf.ImputationKernel(
          df[group],
          save_all_iterations=True,
          random_state=42
        )
        
        # Run the MICE algorithm for 5 iterations
            kds.mice(5)

            # Return the completed dataset.
            df_imputed = kds.complete_data()
            df_imputed['year'] = np.arange(1980,2029,1)
            df_dict[group_names[i]] = df_imputed
            i+=1
        
    
        return df_dict
    
     
    sub_saharan_dict = mice_imputation(new_df,african_groups,african_group_names)
    
    i = 0
    for country in missing_african_countries:
        new_df[country] = sub_saharan_dict[african_group_names[i]][country]
        i+=1

    middle_east_dict = mice_imputation(new_df,middle_east_groups,middle_east_group_names)
    
    j = 0
    for country in missing_middle_east_countries:
        new_df[country] = middle_east_dict[middle_east_group_names[j]][country]
        j+=1
    
    
    new_df['africa_region'] = new_df.apply(avg_neigh_imputation([africa],'africa_region'),axis = 1)
    
    new_df['central_asia_and_the_caucasus'] = new_df.apply(avg_neigh_imputation([central_asia_causasus_countries],'central_asia_and_the_caucasus'),axis = 1)
    
    new_df['sub_saharan_africa_region'] = new_df.apply(avg_neigh_imputation([sub_saharan_africa],'sub_saharan_africa_region'),axis = 1)
    
    new_df['sub_saharan_africa'] = new_df.apply(avg_neigh_imputation([sub_saharan_africa],'sub_saharan_africa'),axis = 1)
    
    
    other_advanced_economies.extend(['western_europe','eastern_europe','southeast_asia','south_america'])
    european_union.extend(['western_europe'])
    euro_area.extend(['western_europe'])
    emerging_developing_asia.extend(['south_asia','southeast_asia','pacific_islands'])
    emerging_developing_europe.extend(['western_europe', 'eastern_europe'])
    latin_american_caribean.extend(['south_america'])
    
    remaining_groups = [
    other_advanced_economies,
    european_union,
    euro_area,
    emerging_developing_asia,
    emerging_developing_europe,
    latin_american_caribean]

    remaining_group_names = [
    'other_advanced_economies',
    'european_union',
    'euro_area',
    'emerging_developing_asia',
    'emerging_developing_europe',
    'latin_american_caribean']
    
    remaining_groups_dict = mice_imputation(new_df,remaining_groups,remaining_group_names)
    
    #for group in remaining_groups:
    for group,country_list in remaining_missing_countries.items():
        for k in range(len(country_list)):
            new_df[country_list[k]] = remaining_groups_dict[group][country_list[k]]
    
    new_df['euro_area'] = new_df.apply(avg_neigh_imputation([euro_area],'euro_area'),axis = 1)
    
    return new_df
    
def feature_store(new_df):
    new_df.year = pd.to_datetime(new_df.year)
    start_datetime = new_df.year.iloc[0]
    end_datetime = new_df.year.iloc[new_df[new_df.year.dt.year == 2023].index[0]]
    feature_store_creation(new_df,1)
    feature_view_training_create(1,start_datetime,end_datetime)
    
        
    