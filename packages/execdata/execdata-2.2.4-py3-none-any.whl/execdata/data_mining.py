'''
Date         : 2023-10-12 14:56:26
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-16 14:24:32
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\data_mining.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''

def column_identify(df, column_lists):
    column_indentify = {}
    for col in column_lists:
        num = len(df[col].unique().tolist())
        column_indentify[col] = num
    return column_indentify

def filtered_value_count(df, column, limit_number):
    value_counts_series = df[column].value_counts()
    filtered_value_counts = value_counts_series[value_counts_series < limit_number]
    return filtered_value_counts

def filtered_value_list(df, column, limit_number):
    value_counts_series = df[column].value_counts()
    filtered_value_counts = value_counts_series[value_counts_series < limit_number]
    filtered_value_counts_list = filtered_value_counts.index.values.tolist()
    return filtered_value_counts_list

