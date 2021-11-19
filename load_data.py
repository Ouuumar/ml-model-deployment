"""
This script is to download origin data from kaggle but does not work
https://stackoverflow.com/questions/49386920/download-kaggle-dataset-by-using-python
https://www.codegrepper.com/code-examples/python/python+download+csv+from+url
https://www.kite.com/python/answers/how-to-download-a-csv-file-from-a-url-in-python
https://github.com/Kaggle/kaggle-api
https://pypi.org/project/kaggle/
"""
# from os import write
# import requests
# import os.path as path 
# import csv
# import urllib3

# # download the data origin from kaggle (> 100MB)

# url1 = 'https://www.kaggle.com/c/home-credit-default-risk/data?select=application_test.csv'
# url2 = 'https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv'

# r1 = requests.get(url1)
# url_content1 = r1.content
# csv1 = open((path.join('1_rawdata','application_test.csv')), 'wb')
# csv1.write(url_content1)


# r2 = requests.get(url2)
# url_content2 = r2.content
# csv2 = open((path.join('1_rawdata', 'application_train.csv')), 'wb')
# csv2.write(url_content2)

# other method

# with requests.Session() as s:
#     download1 = s.get(url1)
#     download2 = s.get(url2)
#     decoded_content1 = download1.content.decode('utf-8')
#     decoded_content2 = download2.content.decode('utf-8')

#     cr1 = csv.reader(decoded_content1.splitlines(), delimiter=',')
#     cr2 = csv.reader(decoded_content2.splitlines(), delimiter=',')
#     cr1 = open((path.join('1_rawdata','application_test.csv')), 'wb')
#     cr2 = open((path.join('1_rawdata','application_train.csv')), 'wb')

