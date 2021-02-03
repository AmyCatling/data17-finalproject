from final_project.extract import Extract
from final_project.transform import Transform_csv, Transform_json
from final_project.load import LoadData

#load = LoadData()

def csv_load():

    extractor = Extract('csv')
    extractor.all_data_loader()
    transformer = Transform_csv(extractor.academy_df)
    loader = LoadData(load_choice='academy', df=transformer.academy_df)

def json_load():
    extractor = Extract('json', devcounter=True)
    extractor.all_data_loader()
    transformer = Transform_json(extractor.talent_df)
    print(transformer.talent_df.dtypes)
    loader = LoadData(load_choice='talent', df=transformer.talent_df)

#print(self.academy_df.loc[self.talent_df[', "Active"])



#csv_load()
json_load()