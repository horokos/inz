from os import listdir
import json


# lista plików z danymi
files = listdir(r'ocenione_dane')

dataset_file = open(f'datasets/reddit_posts_1_10_dataset.json', 'w+')

for file in files:
    print(file)
    subreddit_file = open(f'ocenione_dane_1_10/{file}')
    lines = subreddit_file.readlines()
    subreddit_file.close()
    for line in lines:
        json_file = json.loads(line)
        replie_dict = {}
        replie_dict['title'] = json_file['post']['title']
        replie_dict['post_text'] = json_file['post']['selftext']
        for replie in json_file['replies']:
            replie_dict['grade'] = replie['grade']
            replie_dict['selftext'] = replie['selftext']
            dataset_file.write(str(json.dumps(replie_dict))+'\n')

dataset_file.close()
