import pandas as pd
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from darts.models import NBEATSModel
#from hsml.utils.schema import Schema
#from hsml.utils.model_schema import ModelSchema


def process_data(data):
    process_df = data.copy()
    process_df = process_df.sort_values(by = 'year'); process_df['year'] = pd.to_datetime(process_df['year']).dt.strftime('%Y-%m-%d')
    process_df = process_df.set_index('year') ; process_df = process_df.drop('unique_id',axis = 1)
    
    wide_process_df = process_df.T
    wide_process_df['Country'] = wide_process_df.index ;wide_process_df = wide_process_df.reset_index()
    wide_process_df = wide_process_df.drop('index',axis = 1)
    wide_process_df.columns.name = None
    
    long_process_df = pd.melt(wide_process_df, id_vars='Country', value_vars= process_df.index, var_name='datetime', value_name='gdp_index')
    
    return long_process_df

class Model_Definition():
    # stop training when validation loss does not decrease more than 0.05 (`min_delta`) over
    # a period of 5 epochs (`patience`)
    def __init__(self):
        my_stopper = EarlyStopping(
            monitor="train_loss",
            patience=5,
            min_delta=0.001,
            mode='min',
        )

        pl_trainer_kwargs={"callbacks": [my_stopper],"accelerator": "auto", "devices": 1}
    
        self.model = NBEATSModel(
        input_chunk_length=12, output_chunk_length=2,n_epochs=100, random_state=0,pl_trainer_kwargs=pl_trainer_kwargs
)
    
#def my_model_schema(model_input,model_output):
#    input_schema = Schema(model_input[0].to_dataframe())
#    output_schema = Schema(model_output[0].to_dataframe())
#    model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)

#    return model_schema.to_dict() 
     
    
    