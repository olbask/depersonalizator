# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:28:33 2023

@author: obaskaev
"""

import hashlib
import pandas as pd
import glob
import re


email_regex = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', re.S)
mobile_regex = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', re.S)


PATH = '<path-to-your-directory>**\*.csv'
SALT = '<chosen-salt>'


def hashValue(value): #hashes some value with md5
    hashed_value = hashlib.md5((str(value)+SALT).encode('utf-8')).hexdigest()    
    return hashed_value

def hashValidContactData(value): #checks if data in the cell is mobile or email and hashes it
        hashed_email = re.sub((email_regex), hashValue, str(value))
        hashed_mobile = re.sub((mobile_regex), hashValue, str(hashed_email))
        return hashed_mobile


if __name__ == '__main__': #runs through all the csv files in specified directory and hashes all personal data inside
    files = [file for file in glob.glob(PATH, recursive=True)]
    for file_name in files:
        print(file_name)
        df = pd.read_csv(file_name, index_col=0, on_bad_lines='skip', delimiter = ';')
        df = df.applymap(hashValidContactData, na_action='ignore')
        df.to_csv(file_name, sep = ';')
        