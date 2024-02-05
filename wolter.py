import os
import requests
import time
from typing import List

SEARCH_URL = "https://restaurant-api.wolt.com/v1/pages/search"
INTERVAL_TIME_SEC = 10
VOICE_FREQUENCY = 2500  # Set Frequency To 2500 Hertz
VOICE_DURATION = 500  # Set Duration To 1000 ms == 1 second


def search_restaurant(name: str) -> List:
    response = requests.get(SEARCH_URL, params=dict(sort='relevancy',
                                                    q=name,
                                                    limit=50,
                                                    lat=32.087236876497585,
                                                    lon=34.78698525756491))
    json_response = response.json()
    sections = json_response.get('sections', [])
    if len(sections) == 0:
        return []

    return sections[0]["items"]


def is_opened(name: str, public_url: str) -> bool:
    results = search_restaurant(name)

    relevant = None

    for result in results:
        if public_url == result['link']['target']:
            relevant = result
            break
        
    if relevant is None:
        print('Restaurant name disappeared (may due to brute force restrictions)!')
        return False

    return relevant.get('venue', {}).get('online', False)


if __name__ == '__main__':
    restaurant_name = input("Enter the restaurant name: ")
    results = search_restaurant(restaurant_name)

    if not results:
        print('Search returned 0 restaurant!')
        exit(1)

    for i, result in enumerate(results, start=1):
        title = result['title']
        print(f'[{i}]\t{title}')

    restaurant_index = int(input("Enter the requested restaurant id: "))

    restaurant_data = results[restaurant_index - 1]
    public_url = restaurant_data['link']['target']

    while not is_opened(restaurant_name, public_url):
        print(f"Restaurant is closed, sleeping for {INTERVAL_TIME_SEC} seconds!")
        time.sleep(INTERVAL_TIME_SEC)

    print(f"Restaurant is open! visit: {public_url}")
    while True:
        os.system('say "Ready to order!"')
        time.sleep(1)
