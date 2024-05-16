import os
import geopandas as gpd
import pandas as pd
from tkinter import Tk, messagebox  # For Python 2.x, use 'Tkinter' instead
from tkinter import filedialog


def extract_zone(prediction_name):
    # zone number is always the last two characters
    return prediction_name[-2:]

if __name__ == "__main__":
    Tk().withdraw() # Hide the main window
    #file_path = filedialog.askopenfilename()
    folder_path = filedialog.askdirectory()
    predictions = [
        "LTE_OD_",
        "LTE_ID_",
        "LTE_HB_OD_",
        "LTE_HB_ID_",
        "NR_OD_",
        "NR_ID_",
        "NR_C_OD_",
        "NR_C_ID_"
    ]
    zones = [50,51,52,53,54,55,56]
    combined_data = pd.DataFrame()
    for prediction in predictions:
        for zone in zones:
            file_name = prediction + str(zone) + '.tab'
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                data = gpd.read_file(file_path)
                # columns:LEGEND,THRESHOLD,COLOR,Prediction_name,Transmitter,Site,Site_UTMZONE
                # remove transmitter which UTMZONE is not equal to zone in Prediction_name(like LTE_OD_56)
                # Apply the function to create a new column with the extracted zone
                data['Extracted_Zone'] = data['Prediction_name'].apply(extract_zone)
                # Filter the DataFrame to keep only the rows where 'Site_UTMZONE' matches 'Extracted_Zone'
                data_filtered = data[data['Site_UTMZONE'] == data['Extracted_Zone']]
                # Drop the 'Extracted_Zone' column as it's no longer needed
                data_filtered = data_filtered.drop(columns=['Extracted_Zone'])
                # Combine the two datasets and remove duplicates
                combined_data = gpd.GeoDataFrame(pd.concat([combined_data,data_filtered], ignore_index=True))
                # combined_data = combined_data.drop_duplicates(subset='Transmitter') # remove duplicates based on transmitter
        # Save the combined dataset to a new TAB file
        output_filename = prediction + "AllSites.tab"
        output_file = os.path.join(folder_path,output_filename)
        combined_data.to_file(output_file, driver="MapInfo File")
        print("Combined file saved successfully:",output_file)
    print("All files combined!")
