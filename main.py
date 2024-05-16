import os
#import fiona
#print('MapInfo File' in fiona.supported_drivers)  # Should print True if ready
import geopandas as gpd
import pandas as pd

from tkinter import Tk, messagebox  # For Python 2.x, use 'Tkinter' instead
from tkinter.filedialog import askopenfilename




def extract_zone(prediction_name):
    # zone number is always the last two characters
    return prediction_name[-2:]

if __name__ == "__main__":
    Tk().withdraw()
    file_path = 'SiteSystemsByPostcodeSuburb_20240411.xlsx'
    file_path = askopenfilename()
    zones = [50,51,52,53,54,55,56]
file_path = r"C:\Users\T1603086\Downloads"
# Load the first TAB file
file1 = r"C:\Users\T1603086\Downloads\z50\LTE_OD_50.tab"
data1 = gpd.read_file(file1)
# columns:LEGEND,THRESHOLD,COLOR,Prediction_name,Transmitter,Site,Site_UTMZONE
# remove transmitter which UTMZONE is not equal to zone in Prediction_name(like LTE_OD_56)
# Apply the function to create a new column with the extracted zone
data1['Extracted_Zone'] = data1['Prediction_name'].apply(extract_zone)

# Filter the DataFrame to keep only the rows where 'Site_UTMZONE' matches 'Extracted_Zone'
data1_filtered = data1[data1['Site_UTMZONE'] == data1['Extracted_Zone']]

# Drop the 'Extracted_Zone' column as it's no longer needed
data1_filtered = data1_filtered.drop(columns=['Extracted_Zone'])


# Load the second TAB file
file2 = r"C:\Users\T1603086\Downloads\z51\LTE_OD_51.tab"
data2 = gpd.read_file(file2)

file3 = r"C:\Users\T1603086\Downloads\z52\LTE_OD_52.tab"
data3 = gpd.read_file(file3)
file4 = r"C:\Users\T1603086\Downloads\z53\LTE_OD_53.tab"
data4 = gpd.read_file(file4)
file5 = r"C:\Users\T1603086\Downloads\z54\LTE_OD_54.tab"
data5 = gpd.read_file(file5)
file6 = r"C:\Users\T1603086\Downloads\z55\LTE_OD_55.tab"
data6 = gpd.read_file(file6)
file7 = r"C:\Users\T1603086\Downloads\z56\LTE_OD_56.tab"
data7 = gpd.read_file(file7)

# Combine the two datasets and remove duplicates
combined_data = gpd.GeoDataFrame(pd.concat([data1, data2, data3, data4, data5, data6, data7], ignore_index=True),crs=data1.crs)
combined_data = combined_data.drop_duplicates(subset='Transmitter') # remove duplicates based on transmitter


# Save the combined dataset to a new TAB file
os.chdir(r"C:\Users\T1603086\Downloads")
output_file = "tpg_combined_file-removedup.tab"

combined_data.to_file(output_file, driver="MapInfo File")

print("Combined file saved successfully.")
