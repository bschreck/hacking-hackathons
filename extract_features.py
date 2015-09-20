import util
import pandas as pd
import numpy as np
import sys

pf = 'projects.p'
projects = util.loadObjectsFromPickleFile(['projects'], pf)[0]
print projects
df = pd.DataFrame(projects)
print df
sys.exit()
tags = set()
for tag_group in df['tags'].values:
    if tag_group:
        for tag in tag_group:
            tags.add(tag)
tags = list(tags)
tag_dict = {}
for i,t in enumerate(tags):
    tag_dict[t] = i
def convert_tags_to_cat(x):
    if x:
        return [tag_dict[y] for y in x]
    else:
        return [None]
df['tags'] = df['tags'].apply(convert_tags_to_cat)
#print df['tags']
for team in df['members'].values:
    for m in team:
        print m['url']
        print m['name']
