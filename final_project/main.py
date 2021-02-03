from final_project.extract import Extract
from final_project.transform import Transform_csv
from final_project.load import LoadData

#load = LoadData()


extractor = Extract()
extractor.all_data_loader()
transformer = Transform_csv(extractor.academy_df)

print(transformer.academy_df.to_string())
