from os import listdir
from matplotlib import pyplot as plt
from numpy import interp, log, seterr
import json

# lista plików z danymi
files = listdir(r'obrobione_dane')


for file in files:
    print(file)
    subreddit_file = open(f'obrobione_dane/{file}')
    lines = subreddit_file.readlines()
    subreddit_file.close()
    new_lines = []
    for i, line in enumerate(lines):
        whole_post_json = json.loads(line)
        ups_min = 100000
        ups_max = 0
        ups_min2 = 100000
        for replie in whole_post_json['replies']:
            replie_ups = replie['ups']
            if replie_ups <= 0:
                ups_min = 0
            elif ups_min > replie_ups:
                ups_min = replie_ups
            if ups_max < replie_ups:
                ups_max = replie_ups
            if ups_min2 > replie_ups:
                ups_min2 = replie_ups
        for replie in whole_post_json['replies']:
            x = replie['ups']
            if ups_min2 > 0 and ups_max > 0:
                grade = round(interp(log(x), [log(ups_min2), log(ups_max)], [1, 10]))
            elif ups_min2 == 0 and ups_max > 0:
                if x > 0:
                    grade = round(interp(log(x), [0, log(ups_max)], [1, 10]))
                else:
                    grade = round(interp(0, [0, log(ups_max)], [1, 10]))
            elif ups_min2 < 0 and ups_max > 0:
                if x > 0:
                    grade = round(interp(log(x), [-log(-ups_min2), log(ups_max)], [1, 10]))
                elif x == 0:
                    grade = round(interp(0, [-log(-ups_min2), log(ups_max)], [1, 10]))
                else:
                    grade = round(interp(-log(-x), [-log(-ups_min2), log(ups_max)], [1, 10]))
            elif ups_min2 == 0 and ups_max == 0:
                grade = round(interp(x, [0, 0], [1, 10]))
            elif ups_min2 < 0 and ups_max == 0:
                if x == 0:
                    grade = round(interp(0, [-log(-ups_min2), 0], [1, 10]))
                else:
                    grade = round(interp(-log(-x), [-log(-ups_min2), 0], [1, 10]))
            elif ups_min2 < 0 and ups_max < 0:
                grade = round(interp(-log(-x), [-log(-ups_min2), -log(-ups_max)], [1, 10]))
            replie['grade'] = grade
        new_lines.append(whole_post_json)

    subreddit_file = open(f'ocenione_dane_1_10/{file}', 'w+')

    for line in new_lines:
        subreddit_file.write(str(json.dumps(line))+'\n')

    subreddit_file.close()
