from final_project.extract import Extract
from final_project.transform import *
from final_project.load import LoadData
import logging

logging.basicConfig(filename='logtest.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("========  Initialised log file  ========")
# load = LoadData()


def almighty_method():
    extractor = Extract('all')
    extractor.all_data_extractor()
    transformer1 = Transform_academy_csv(extractor.academy_df)
    transformer2 = Transform_json(extractor.talent_df)
    transformer3 = Transform_applicant_csv(extractor.applicant_df)
    transformer4 = Transform_sparta_day_txt(extractor.sparta_day_df)
    loader1 = LoadData(load_choice='academy_df', df=transformer1.academy_df)
    loader2 = LoadData(load_choice='talent_df', df=transformer2.talent_df)
    loader3 = LoadData(load_choice='applicant_df', df=transformer3.applicant_df)
    loader4 = LoadData(load_choice='sparta_day_df', df=transformer4.sparta_day_df)


# def academy_load():
#     extractor1 = Extract('academy_csv')
#     extractor1.all_data_extractor()
#     transformer1 = Transform_academy_csv(extractor1.academy_df)
#     loader = LoadData(load_choice='academy', df=transformer1.academy_df)
#
# def json_load():
#     extractor2 = Extract('json')
#     extractor2.all_data_extractor()
#     transformer2 = Transform_json(extractor2.talent_df)
#     #print(transformer.talent_df.to_string())
#     loader = LoadData(load_choice='talent', df=transformer2.talent_df)
#
# def applicant_load():
#     extractor3 = Extract('applicant_csv')
#     extractor3.all_data_extractor()
#     transformer3 = Transform_applicant_csv(extractor3.applicant_df)
#     loader = LoadData(load_choice='applicant', df=transformer3.applicant_df)
#
# def sparta_day_load():
#     extractor4 = Extract('txt')
#     extractor4.all_data_extractor()
#     transformer4 = Transform_sparta_day_txt(extractor4.sparta_day_df)
#     loader = LoadData(load_choice='sparta_day', df=transformer4.sparta_day_df)

almighty_method()
# try:
# except:
#     print("dosent work")
# try:
#     academy_load()
#     json_load()
#     # applicant_load()
#     # sparta_day_load()
# except:
#     logging.error("Code is broke lol")
#     raise


