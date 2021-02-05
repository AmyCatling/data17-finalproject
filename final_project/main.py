from final_project.extract import Extract
from final_project.transform import *
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


def sparta_day_load():
    extractor = Extract('txt')
    extractor.all_data_loader()
    transformer = Transform_sparta_day_txt(extractor.sparta_day_df)
    transformer.format_date()
    #transformer.format_score()
    print(transformer.sparta_day_df.to_string())

#json_load()
#academy_load()

#applicant_load()
sparta_day_load()


