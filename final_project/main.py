from final_project.extract import Extract
from final_project.transform import *
from final_project.load import LoadData
import logging

logging.basicConfig(filename='logtest.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("========  Initialised log file  ========")

def almighty_method():
    extractor = Extract()
    transformer1 = Transform_academy_csv(extractor.academy_df)
    transformer2 = Transform_json(extractor.talent_df)
    transformer3 = Transform_applicant_csv(extractor.applicant_df)
    transformer4 = Transform_sparta_day_txt(extractor.sparta_day_df)
    loader3 = LoadData(load_choice='applicant_df', df=transformer3.applicant_df)
    loader1 = LoadData(load_choice='academy_df', df=transformer1.academy_df)
    loader2 = LoadData(load_choice='talent_df', df=transformer2.talent_df)
    loader4 = LoadData(load_choice='sparta_day_df', df=transformer4.sparta_day_df)


# extract_test = Extract()
# print(extract_test.file_names_list)
# print(extract_test.files_to_extract)
# print(extract_test.academy_df)
# print(extract_test.applicant_df)
# print(extract_test.talent_df)
# print(extract_test.sparta_day_df)
    
almighty_method()


