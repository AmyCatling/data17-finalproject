from final_project.extract import Extract
from final_project.transform import Transform_academy_csv, Transform_json, Transform_applicant_csv
from final_project.load import LoadData

#load = LoadData()

def academy_load():

    extractor = Extract('academy_csv')
    extractor.all_data_loader()
    transformer = Transform_academy_csv(extractor.academy_df)
    loader = LoadData(load_choice='academy', df=transformer.academy_df)

def json_load():
    extractor = Extract('json', devcounter=True)
    extractor.all_data_loader()
    transformer = Transform_json(extractor.talent_df)
    #print(transformer.talent_df.to_string())
    #loader = LoadData(load_choice='talent', df=transformer.talent_df)

def applicant_load():
    extractor = Extract('applicant_csv')
    extractor.all_data_loader()
    transformer = Transform_applicant_csv(extractor.applicant_df)




#json_load()
academy_load()

#applicant_load()



