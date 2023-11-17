# skrypt pobierający 1000 nazw najpopularniejszych subredditów
# i zapisujący je do pliku subreddits.txt
# każda nazwa zapisana jest w oddzielnej linii pliku

import requests

# otwieramy plik do którego zapiszemy listę subredditów
file = open('subreddits.txt', 'w')

# pętla do pobrania 1000 nazw 10*100=1000
for i in range(10):
    # wysłanie zapytania o listę 100 nazw
    if not i:
        request = requests.get('https://www.reddit.com/subreddits/popular.json?limit=100',
                               headers={'User-agent': 'python script'})
    else:
        request = requests.get(f'https://www.reddit.com/subreddits/popular.json?limit=100&after={after}',
                               headers={'User-agent': 'python script'})

    # zamiana pobranego jsona do słownika
    json_response = request.json()
    # wybranie listy subredditów
    subreddits = json_response['data']['children']
    # wybranie id ostatniego subreddita
    after = json_response['data']['after']
    # zapisanie każdej nazwy w nowej linii pliku
    for subreddit in subreddits:
        file.write(subreddit['data']['display_name'] + '\n')
