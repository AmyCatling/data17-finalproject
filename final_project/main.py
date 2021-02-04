from final_project.extract import Extract
from final_project.transform import Transform_csv, Transform_json
from final_project.load import LoadData

#load = LoadData()

def csv_load():

    extractor = Extract('csv')
    extractor.all_data_loader()
    transformer = Transform_csv(extractor.academy_df)
    #oader = LoadData(load_choice='academy', df=transformer.academy_df)

def json_load():
    extractor = Extract('json', devcounter=True)
    extractor.all_data_loader()
    transformer = Transform_json(extractor.talent_df)
    #print(transformer.talent_df.to_string())
    loader = LoadData(load_choice='talent', df=transformer.talent_df)




#json_load()
csv_load()



