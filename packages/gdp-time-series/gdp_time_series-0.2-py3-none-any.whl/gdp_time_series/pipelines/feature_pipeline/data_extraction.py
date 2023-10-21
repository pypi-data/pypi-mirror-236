import requests
import pandas as pd
from .utils import get_logger

logger = get_logger(__name__)

class Data_Extraction:
    def __init__(self):
        self.url_list = [
            'https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH'
            ,'https://www.imf.org/external/datamapper/api/v1/countries'
            ,'https://www.imf.org/external/datamapper/api/v1/regions'
            ,'https://www.imf.org/external/datamapper/api/v1/groups']
        
        self.data_list = []
        self.pre_df = None
        self.pre_countries = None
        self.pre_regions = None
        self.pre_groups = None
        
    def data_extraction(self):
  
        for url in self.url_list:
            try:
                response = requests.get(url)
                response.raise_for_status()
                logger.info("Successful connection with API.")
                logger.info('-------------------------------')
                data = response.json()
                self.data_list.append(data)
            except requests.exceptions.RequestException as e:
                logger.info(f"Error connecting to {url}: {e}")
            except ValueError as e:
                logger.info(f"Error parsing JSON from {url}: {e}")
                
    def data_storing(self):   
        self.pre_df = pd.DataFrame.from_dict(self.data_list[0].get('values').get('NGDP_RPCH'))       
        self.pre_countries = self.data_list[1].get('countries')
        self.pre_regions = self.data_list[2].get('regions')
        self.pre_groups = self.data_list[3].get('groups')
    
    def update_data(self):
        c_list = list(self.pre_countries.keys())
        r_list = list(self.pre_regions.keys())
        g_list = list(self.pre_groups.keys())
        
        self.new_c_list = [country for country in c_list if country in self.pre_df.columns]
        self.new_r_list = [region for region in r_list if region in self.pre_df.columns]
        self.new_g_list = [group for group in g_list if group in self.pre_df.columns]
        
        self.countries = {k:v for (k,v) in zip(self.pre_countries.keys(),self.pre_countries.values()) if k in self.new_c_list}
        self.regions = {k:v for (k,v) in zip(self.pre_regions.keys(),self.pre_regions.values()) if k in self.new_r_list}
        self.groups = {k:v for (k,v) in zip(self.pre_groups.keys(),self.pre_groups.values()) if k in self.new_g_list}
        
    def dataframe_rename(self):
        df = self.pre_df.copy()
        
        rename_cols = lambda df, name_list, name_dict: df.rename(columns={name: name_dict.get(name)['label'] for name in name_list})
        
        iteration_list = [(self.new_c_list,self.countries),(self.new_r_list,self.regions),(self.new_g_list,self.groups)]
        for el in iteration_list:
            df = rename_cols(df,el[0],el[1])
        
        return df