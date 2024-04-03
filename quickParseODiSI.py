# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 13:41:57 2023

@author: cjako
"""

import re
import os
from datetime import datetime

def parse_data(file_path=None): #function to run
    MAX_HEADER_ROWS = 35 #defines the maximum number of lines to check for header values
    output = {} #returns output as a DICTIONARY
    format_str = r'(\d+-\d+-\d+ \d+:\d+:\d+\.\d+)\t+(\S+)'
    # Choose the file
    if file_path is None: #checks if a file path is supplied
        file_path = input("Enter the path to the ODiSI data file: ")
    file_name, file_ext = os.path.splitext(file_path) #splits file name from the path
    output['File'] = { #breaks the File section of the dictionary into two strings, one File Name and one File path
        'Name': os.path.basename(file_name),
        'path': os.path.dirname(file_path)
    }
    
    with open(file_path, 'r') as file: #this code chunk finds how many lines of data there are by checking for how
    #many lines there are after the first time stamp
        for line in file:
            match = re.search(format_str, line)
            if match:
                break
        line_count = len(file.readlines())+1
    
    with open(file_path, 'r') as file: #opens file path as a raw string
        # Load the header
        header = {}
        for _ in range(MAX_HEADER_ROWS):
            line = file.readline()
            if not line or line.startswith('-'): #checks to make sure we are in the header section
                break
            parts = line.split('\t') #splits up all the names to make each an individual row
            if len(parts) == 2:
                header[parts[0].replace(':', '').replace(' ', '_')] = parts[1].strip()
        output['Header'] = header

        # Parse the x-axis values (location values),and the tare values
        labels = {}
        tare = []
        line = file.readline() #this assumes the first item AFTER the header is the tare
        tare = [float(t) for t in line.split('\t')[3:]]
        if '.tsv' in file_ext:
            for _ in range(8):
                line = file.readline() #reads first line of the file
                if re.match(r'\d', line[0]): #checks if there is a dash (data is seperated from headers by dashes), which indicates we are at the start of the data
                    file.seek(file.tell() - len(line))  # Rewind to the start of data
                    break
                parts = line.split('\t')
                if header['Tare_Name'] in line: #check if tare line
                    data = [float(val) if val else 0.0 for val in parts[3:]]
                    labels['Location_Values'] = data #### CHANGED FROM 'Tare'
                elif 'x-axis' in parts[0]:
                    data = [float(val) if val else 0.0 for val in parts[3:]] #can modify the 3 in parts to determine where to start collecting data in the x-axis array
                    labels['Location_Values'] = data #check if x-axis values
                elif 'Gage/segment name' in parts[0]:
                    labels['Location_RangeLabels'] = parts[1:]
        else:
            labels['Location_RangeLabels'] = line.split('\t')[1:]
            labels['Location_Values'] = [float(val) if val else 0.0 for val in labels['Location_RangeLabels']]
        output['Location'] = labels #displays the location dictionary

        # Load the timestamps and data
        data = {'Values': [], 'Tare': [], 'QualityFactor': [],}
        time = []
        data['Tare'] = tare
        if '.tsv' in file_ext:
            format_str = r'(\d+-\d+-\d+ \d+:\d+:\d+\.\d+)\t+(\S+)' #checks for start of time stamps
            data_labels = ['measurement', 'quality factor'] #labels that may be at the start of each data section
            for _ in range(line_count):
                line = file.readline() #line is the current line you are reading
                if not line:#see below comment
                    break #if there is no data in the line, we are at the end of the file
                match = re.search(format_str, line) #creates a regular expression match object that checks the whole line for a timestamp
                if match: #if the match from earlier exists...this might be redundant
                    timestamp, label = match.groups() #groups the items in the match into a timestamp and a label
                    if label in data_labels:
                        line_values = [float(val) if val else 0.0 for val in line.split('\t')[3:]] #starts reading after the third tab
                        if label == 'measurement':
                            data['Values'].append(line_values)
                            time.append(timestamp)
                        elif label == 'quality factor':
                            data['QualityFactor'] = line_values
                else:
                    break
        else:
            format_str = r'(\d+-\d+-\d+ \d+:\d+:\d+\.\d+)\t+(\S+)' #checks format of time
            for line in file:
                match = re.match(format_str, line)
                if match:
                    timestamp = match.group(1)
                    line_values = [float(val) if val else 0.0 for val in line.split('\t')[1:]]
                    data['Values'].append(line_values)
                    
        #Find the delta time values so our times starts at zero at the time testing is initiated
        first_time = datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S.%f')
        time_differences = [(datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f') - first_time).total_seconds() for dt in time]
        output['Data'] = data
        output['Time'] = time_differences


    return output

# example usage
#FO_dict = parse_data(r'G:\Shared drives\GeoD\research\fiber_data\steeldeck_data\121523 test\121523_test_2023-12-15_18-24-10_ch1_full.tsv')