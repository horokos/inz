import requests
import json
from time import sleep

# otwarcie pliku z listą subredditów
subreddits_file = open('subreddits2.txt', 'r')

no_req = 0

# pobieranie postów dla kazdego subreddita z listy
for subreddit in subreddits_file:
    subreddit = subreddit.replace('\n', '')
    print(subreddit)

    # sprawdzenie ile postow juz pobralismy z danego subreddita
    try:

        # otwarcie pliku z postami z danego subreddita, read-only
        subreddit_file = open(f'dane/{subreddit}.txt', 'r')
        lines = subreddit_file.readlines()
        count = len(lines)
        subreddit_file.close()

        # jesli pobralismy wczesnije juz jakies posty to wybieramy ostatni pobrany
        if count > 0:
            after = json.loads(lines[-1])[0]['data']['children'][0]['data']['name']

    # gdy plik nie istnieje znaczy ze jeszcze nie pobralismy zadnego posta
    except FileNotFoundError:
        count = 0

    # otwarcie pliku z postami z danego subreddita, append
    subreddit_file = open(f'dane/{subreddit}.txt', 'a')

    # dopóki nie pobralismy 50 postow bedziemy je sciagac
    while count < 50:
        round_count = 0

        # wysłanie odpowiedniego zapytania o 100 postów
        if count > 0:
            posts_response = requests.get(f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100&after={after}',
                                          headers={'User-agent': 'script python'})
            no_req += 1
        else:
            posts_response = requests.get(f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100',
                                          headers={'User-agent': 'script python'})
            no_req += 1

        # jeśli zapytanie się powiodło bedziemy pobierac posty
        if posts_response.status_code == 200:

            # zamieniamy odpowiedz json na dictionary
            json_posts = posts_response.json()
            # wyciągmy liste postów
            posts = json_posts['data']['children']
            # id ostatniego postu
            after = json_posts['data']['after']

            # dla każdego postu w liście
            for post in posts:
                # wybieramy interesujące nas parametry
                comments = post['data']['num_comments']
                text = post['data']['selftext']
                permalink = post['data']['permalink']
                permalink = permalink[:-1]
                media = post['data']['media'] is None
                if media:
                    try:
                        media = post['data']['media_metadata'] is None
                    except:
                        media = True
                if media:
                    try:
                        media = post['data']['preview'] is None
                    except:
                        media = True
                # sprawdzamy czy są odpowiednie
                if text != "" and 10 < comments < 501 and media:

                    # jeśli tak to pobieramy dany post
                    while True:
                        post_response = requests.get(f'https://www.reddit.com{permalink}.json',
                                                     headers={'User-agent': 'script python'})
                        no_req += 1
                        # sprawdzamy czy się udało, jeśli nie to czekamy 10min i próbujemy jeszcz raz
                        if post_response.status_code == 200:
                            break
                        else:
                            print(f'limit reached, waiting 600sec, no_req {no_req}')
                            no_req = 1
                            sleep(600)
                            print('resuming')
                    json_post = post_response.json()
                    # zapisujemy tresc postu do pliku
                    text_post = post_response.text
                    subreddit_file.write(text_post + '\n')
                    count += 1
                    round_count += 1
                    if count % 5 == 0:
                        print(f'downloaded {count} posts')
                    # gdy pobralismy 50 postów przechodzimy do kolejnego subreddita
                    if count >= 50:
                        break
            # jeśli w ostatnich 100 postach było mniej niż 5 interesujących nas postów
            # przechodzimy do kolejnego subreddita
            if round_count < 5:
                break
        # gdy zapytanie nie powiodło się czekamy 10min i próbujemy jeszcze raz
        else:
            print(f'limit reached, waiting 600sec, no_req {no_req}')
            no_req = 1
            sleep(600)
            print('resuming')
    subreddit_file.close()

subreddits_file.close()
