import os
from pathlib import Path
import csv
import re
import matplotlib.pyplot as plt
from datetime import date, datetime

def is_number(value):
    """Returns True if the value can be converted to a float, False otherwise."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

class DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.dictionaries = {}

    def load_data(self, pattern="*_METRICS.csv"):

        #data = []
        dirs = os.listdir(self.data_dir)
        print(f"Found {len(dirs)} directories")

        for sub_dir in dirs:
            date_from_folder = re.search(r'(\d{4})-(\d{2})-(\d{2})', sub_dir)
            for filename in Path(os.path.join(self.data_dir, sub_dir)).glob(pattern):
             
                with open(filename, 'r') as file:
                    csv_data = file.read()
                    file_rows = self.parse_simple(csv_data, date_from_folder)
                    self.add_to_dict(file_rows)
        
        #return data
 
    def parse_simple(self, csv_text, date_from_folder):
        definitions = {}
        entries = []
        reader = csv.reader(csv_text.strip().splitlines())
        next(reader, None) # Skip header

        for row in reader:
            if not row: continue
            
            row_type, local_num, message = row[0], row[1], row[2]

            if row_type == 'Definition':
                # Store the field names for this local number
                definitions[local_num] = row[3::3] # Gets every 3rd item starting at index 3 (The Fields)

            elif row_type == 'Data' and local_num in definitions and message != 'unknown':
                # Create the entry
                entry = {'message': message, 'properties': {}}

                year, month, day = date_from_folder.groups()
                entry['properties']['date'] = {'year': year, 'month': month, 'day': day}
                
                # Zip pairs up the fields, values, and units automatically
                fields = definitions[local_num]
                values = row[4::3] # Gets every 3rd item starting at index 4 (The Values)
                units  = row[5::3] # Gets every 3rd item starting at index 5 (The Units)

                for f, v, u in zip(fields, values, units):
                    if f == None or f == 'unknown' or f == '' or v == None or v == '':
                        continue

                    if u: # Only add if field name exists
                        entry['properties'][f] = {'value': v, 'unit': u}
                        continue

                    entry['properties'][f] = v
                
                entries.append(entry)

        return entries
    
    def add_to_dict(self, data):
       
        for entry in data:
            # Get the message type (e.g., 'hrv_value', 'file_id')
            msg_key = entry['message']
            
            # If we haven't seen this message type yet, create a new list for it
            if msg_key not in self.dictionaries:
                self.dictionaries[msg_key] = []
            
            # Add the properties to the list for this message type
            self.dictionaries[msg_key].append(entry['properties'])
            
    def plot_time_data(self, rows_to_plot=None, cols_to_plot=None, title='Metrics'):
        
        # 1. Start the figure BEFORE the loop
        plt.figure(figsize=(12, 8)) 

        for key, data in self.dictionaries.items():

            # 'sleep_level'
            if rows_to_plot is not None and key not in rows_to_plot:
                continue

            # Sort data chronologically
            data.sort(key=lambda x: x['date']['year'] + x['date']['month'] + x['date']['day'])

            if cols_to_plot is None:
                current_keys = list(data[0].keys())
                if 'date' in current_keys:
                    current_keys.remove('date')
            else:
                current_keys = cols_to_plot

            # Prepare X-axis (Dates)
            dates = []
            for entry in data:
                d = entry['date']
                dates.append(date(int(d['year']), int(d['month']), int(d['day'])))

            # Plotting (Adds lines to the existing figure created above)
            for k in current_keys:
                # Create list of values for this specific key
                values = [float(entry[k]) if k in entry and is_number(entry[k]) and float(entry[k]) > 0 else None for entry in data]
                
                # Added the main key to the label so you know which dataset it belongs to
                # e.g., "sleep_level: deep" vs "sleep_assessment: combined"
                plt.plot(dates, values, marker='.', label=f"{key}: {k}")

        plt.title(title)
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
        plt.tight_layout()

        plt.show()

    def plot_with_timestamp(self, row_key):
        data = self.dictionaries[row_key]
        
        # 1. Prepare lists for X and Y data
        x_timestamps = []
        y_values = []

        # 2. Extract and convert data
        for entry in data:
            if 'value' not in entry:
                continue

            # X-Axis: Convert Unix timestamp string to integer, then to a datetime object
            timestamp_sec = int(entry['timestamp'])
            dt_object = datetime.fromtimestamp(timestamp_sec)
            x_timestamps.append(dt_object)
            
            # Y-Axis: Extract the nested value string and convert to float
            value_float = float(entry['value']['value'])
            y_values.append(value_float)

        # Determine the Y-axis unit
        unit = data[0]['value']['unit']

        # 3. Plotting
        plt.figure(figsize=(10, 6))

        plt.plot(x_timestamps, y_values, marker='o', linestyle='-')

        # Formatting
        plt.title('Value Over Time (by Timestamp)')
        plt.xlabel(f"Time on {x_timestamps[0].strftime('%Y-%m-%d')}") # Show the date clearly
        plt.ylabel(f"Value ({unit})")
        plt.grid(True, alpha=0.5)

        # Matplotlib function to automatically rotate and format time labels
        plt.gcf().autofmt_xdate()

        plt.show()


if __name__ == "__main__":
    data_loader = DataLoader(data_dir='fit_data')
    data_loader.load_data("*_HRV_STATUS.csv")
    data_loader.load_data("*_SLEEP_DATA.csv")
    #data_loader.load_data("*_WELLNESS.csv")
    #data_loader.load_data()
    #data_loader.plot_time_data(rows_to_plot="hrv_value")#rows_to_plot=['sleep_assessment'], cols_to_plot=['rem_sleep_score', 'sleep_quality_score'])# rows_to_plot=['sleep_level'], cols_to_plot=['rem_sleep_score', 'sleep_quality_score'])
    data_loader.plot_with_timestamp('hrv_value')