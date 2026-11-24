import pandas as pd
import os
from PIL import Image
import pytesseract
from src_code.regex_helper import extract_discharge_summary


BASE = 'data'

def read_data(path = BASE):

    # bills_df = pd.read_csv(os.path.join(BASE, 'medical_bills_ground_truth.csv'))
    discharge_df = pd.read_csv(os.path.join(BASE, 'discharge_summaries_ground_truth.csv'))

    # print(f'Hospital Bills: {len(bills_df)} rows')
    print(f'Discharge Summaries: {len(discharge_df)} rows')
    # print(f'Total Document: {len(bills_df) + len(discharge_df)}')

    return discharge_df



def do_ocr(data_frame):
    try:
        patient = []
        for i in data_frame['filename']:
            img1 = Image.open(os.path.join(BASE, 'discharge_summaries', i))
            ocr_text = pytesseract.image_to_string(img1)
            patient.append(extract_discharge_summary(ocr_text))
            
            
        return patient    

    except Exception as e:
        print('pytesseract not installed. Uncomment the install lines above to enable OCR', e)    

