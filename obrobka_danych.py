from os import listdir
import json


def create_comment_dict(comment):
    comment_dict = {}
    comment_dict["selftext"] = comment['body']
    comment_dict["ups"] = comment['ups']
    comment_dict["depth"] = comment['depth']
    comment_dict['author'] = comment['author']
    comment_dict["replies"] = []
    if type(comment["replies"]) is dict:
        replies = comment['replies']['data']['children']
        for replie in replies:
            try:
                comment_dict['replies'].append(create_comment_dict(replie['data']))
            except KeyError:
                pass
    return comment_dict


# lista plików z danymi
files = listdir(r'dane')

for file in files:
    print(file)
    subreddit_file = open(f'dane/{file}')
    lines = subreddit_file.readlines()
    subreddit_file.close()
    new_lines = []
    for i, line in enumerate(lines):
        whole_post_json = json.loads(line)
        comments = whole_post_json[1]['data']['children']
        post = whole_post_json[0]
        post_data = post['data']['children'][0]['data']
        post_dict = {"post": {}, "replies": []}
        post_dict["post"]["title"] = post_data['title']
        post_dict["post"]["subreddit"] = post_data['subreddit']
        post_dict["post"]["selftext"] = post_data['selftext']
        post_dict["post"]["ups"] = post_data['ups']
        post_dict["post"]["permalink"] = post_data['permalink']
        post_dict["post"]["num_comments"] = post_data['num_comments']

        for comment in comments:
            if comment['kind'] != 'more':
                post_dict['replies'].append(create_comment_dict(comment['data']))

        new_lines.append(post_dict)

    subreddit_file = open(f'obrobione_dane/{file}', 'w+')

    for line in new_lines:
        subreddit_file.write(str(json.dumps(line))+'\n')

    subreddit_file.close()