from os import listdir
from matplotlib import pyplot as plt
from numpy import interp, log, seterr
import json

seterr(all='raise')
# lista plików z danymi
files = listdir(r'obrobione_dane')

grades = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
grades2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
grades3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
grades4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
                grade = round(interp(log(x), [log(ups_min2), log(ups_max)], [1, 11]))
            elif ups_min2 == 0 and ups_max > 0:
                if x > 0:
                    grade = round(interp(log(x), [0, log(ups_max)], [1, 11]))
                else:
                    grade = round(interp(0, [0, log(ups_max)], [1, 11]))
            elif ups_min2 == 0 and ups_max == 0:
                grade = round(interp(x, [0, 0], [1, 11]))

            grade2 = round(interp(x, [ups_min, ups_max], [1, 11]))

            grade4 = round(interp(x, [ups_min2, ups_max], [1, 11]))

            if ups_min2 > 0 and ups_max > 0:
                grade3 = round(interp(log(x), [log(ups_min2), log(ups_max)], [1, 11]))
            elif ups_min2 == 0 and ups_max > 0:
                if x > 0:
                    grade3 = round(interp(log(x), [0, log(ups_max)], [1, 11]))
                else:
                    grade3 = round(interp(0, [0, log(ups_max)], [1, 11]))
            elif ups_min2 < 0 and ups_max > 0:
                if x > 0:
                    grade3 = round(interp(log(x), [-log(-ups_min2), log(ups_max)], [1, 11]))
                elif x == 0:
                    grade3 = round(interp(0, [-log(-ups_min2), log(ups_max)], [1, 10]))
                else:
                    grade3 = round(interp(-log(-x), [-log(-ups_min2), log(ups_max)], [1, 11]))
            elif ups_min2 == 0 and ups_max == 0:
                grade3 = round(interp(x, [0, 0], [1, 11]))
            elif ups_min2 < 0 and ups_max == 0:
                if x == 0:
                    grade3 = round(interp(0, [-log(-ups_min2), 0], [1, 11]))
                else:
                    grade3 = round(interp(-log(-x), [-log(-ups_min2), 0], [1, 11]))
            elif ups_min2 < 0 and ups_max < 0:
                grade3 = round(interp(-log(-x), [-log(-ups_min2), -log(-ups_max)], [1, 11]))

            grades[grade - 1] += 1
            grades2[grade2 - 1] += 1
            grades3[grade3 - 1] += 1
            grades4[grade4 - 1] += 1
            replie['grade'] = grade
        # new_lines.append(whole_post_json)

    # subreddit_file = open(f'ocenione_dane/{file}', 'w+')
    #
    # for line in new_lines:
    #     subreddit_file.write(str(json.dumps(line))+'\n')
    #
    # subreddit_file.close()

plt.plot(range(0, 11), grades, 'r.')
plt.plot(range(0, 11), grades2, 'bx')
plt.plot(range(0, 11), grades3, 'go')
plt.plot(range(0, 11), grades4, 'yv')
plt.show()
