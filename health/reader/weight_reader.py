import xml.etree.ElementTree as ET
import pandas as pd

class WeightReader:
    def __init__(self, xml_path):
        self.xml_path = xml_path

    def extract_to_csv(self, output_csv):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        records = []
        for entry in root.findall('Record'):
            if entry.attrib.get('type') == 'HKQuantityTypeIdentifierBodyMass':
                weight = float(entry.attrib['value'])
                date = entry.attrib['startDate'].split(' ')[0]
                records.append({'date': date, 'weight': weight})

        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').drop_duplicates('date')
        df.to_csv(output_csv, index=False)

        print(f"Saved: {output_csv}")