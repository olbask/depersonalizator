# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:28:33 2023
Runs through all the files in specified directory and hashes all personal data inside.
ATM only csv, excel and text files supported.
Word not supported yet.
@author: obaskaev
"""

import hashlib
import pandas as pd
import glob
import re
import csv


email_regex = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', re.S)
mobile_regex = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', re.S)


PATH = '<path-to-your-directory>**\*.*'
SALT = '<chosen-salt>'


textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars)) # Checks if the file is bytes or text


def hashValue(value): # Hashes a value+salt with md5
    hashed_value = hashlib.md5((str(value)+SALT).encode('utf-8')).hexdigest()    
    return hashed_value


def hashValidContactData(value): # Checks if data in the value contains mobile or email and hashes it
        hashed_email = re.sub((email_regex), hashValue, str(value))
        hashed_mobile = re.sub((mobile_regex), hashValue, str(hashed_email))
        return hashed_mobile


def hashExcelFile(file_name): # Hashes personal data in an excel file
    df = pd.read_excel(file_name, index_col=0, sheet_name=None)
    with pd.ExcelWriter(file_name) as writer:
        for key, value in df.items():
            value = value.applymap(hashValidContactData, na_action='ignore')
            value.to_excel(writer, sheet_name = key)
            
            
"""          
def hashWordFile(file_name): #hashes personal data in a word file
    doc = docx.Document(file_name)
    print(doc.text)
    for para in doc.paragraphs:
        print(para.text)
"""        


def hashCSVFile(file_name): # Hashes personal data in a csv file
    with open(file_name, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
        df = pd.read_csv(file_name, index_col=0, on_bad_lines='skip', delimiter = dialect.delimiter)
        df = df.applymap(hashValidContactData, na_action='ignore')
        df.to_csv(file_name, sep = dialect.delimiter)

        
def hashTextFile(file_name): # Hashes personal data in a text file
    with open(file_name, 'r') as f:
        text = f.read()
        text = hashValidContactData(text)
    with open(file_name, 'w') as f:
        f.write(text)   


if __name__ == '__main__':
    files = [file for file in glob.glob(PATH, recursive=True)]
    for file_name in files:
        if file_name.endswith('csv'):
            hashCSVFile(file_name)    
        elif file_name.endswith(('xls','xlsx')):
            hashExcelFile(file_name)
#        elif file_name.endswith(('doc','docx')):
#            hashWordFile(file_name)
        else:
            if is_binary_string(open (file_name, 'rb').read(1024)):
                pass
            else:
                hashTextFile(file_name)
