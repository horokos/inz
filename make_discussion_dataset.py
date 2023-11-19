from os import listdir
import json


# lista plików z danymi
files = listdir(r'obrobione_dane')

dataset_file = open(f'dataset_discussions.json', 'w+')

for file in files:
    print(file)
    subreddit_file = open(f'obrobione_dane/{file}')
    lines = subreddit_file.readlines()
    subreddit_file.close()
    for line in lines:
        json_file = json.loads(line)
        for replie in json_file['replies']:
            post = json_file['post']


dataset_file.close()