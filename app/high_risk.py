# import xlrd
# import json
# from collections import OrderedDict
#
# excelDoc = xlrd.open_workbook('High Risk Ranges v48_0 190621.xls')
#
# HighRiskRanges = excelDoc.sheet_by_index(2)
#
# temp=[]
# high_risk_ranges={}
# high_risk_ranges['data']=temp
#
# for rows in range(1, HighRiskRanges.nrows):
#     phone_instance = OrderedDict()
#     row_data = HighRiskRanges.row_values(rows)
#     phone_instance['Number'] = row_data[0]
#     phone_instance['Range (CC+4/5 digits)'] = row_data[1]
#     phone_instance['Country'] = row_data[2]
#     phone_instance['Fraud Type'] = row_data[3]
#     phone_instance['Source TADIG code (most recent)'] = row_data[4]
#     phone_instance['Source org'] = row_data[5]
#     phone_instance['Source country'] = row_data[6]
#     phone_instance['Date Added'] = row_data[7]
#
#     temp.append(phone_instance)
#
#