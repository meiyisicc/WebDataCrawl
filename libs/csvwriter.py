# -*- coding: utf-8 -*-
"""
    libs.csvwriter
    ~~~~~~~~~~~~~
    define same csv opt
    active context.
    :copyright: (c) 2017 by meiyisicc.
    :license: BSD, see LICENSE for more details.
"""


import csv

def write_csv_file(file_name, rows):
    file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

