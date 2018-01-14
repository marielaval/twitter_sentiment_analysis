import csv
from textblob import TextBlob

infile = '/Users/shallomigbre/Desktop/Workbook2.csv'

with open(infile, 'r') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        sentence = row[0]
        blob = TextBlob(sentence)
        print (blob.sentiment)
 
