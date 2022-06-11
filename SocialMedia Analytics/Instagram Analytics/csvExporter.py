import pandas as pd
import csv
import os.path

def export(names, comments):
    fname = 'comments.csv'
    temp = {}
    temp_names = []
    temp_comments = []
    if os.path.isfile(fname):
        saved = pd.read_csv(fname)
        temp_names.extend(saved['name'])
        temp_comments.extend(saved['comment'])
    temp_names.extend(names)
    temp_comments.extend(comments)
    temp.update({'name': temp_names, 'comment': temp_comments})
    df = pd.DataFrame(temp)
    writer = csv.writer(fname)
    df.to_csv(writer, 'comments', index=False)
    writer.save()
