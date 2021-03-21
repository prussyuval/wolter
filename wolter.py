import requests
import time
import winsound
from typing import List

SEARCH_URL = "https://restaurant-api.wolt.com/v1/search"
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
    return json_response.get('results', [])


def is_opened(name: str, identifier: str) -> bool:
    results = search_restaurant(name)

    for result in results:
        if result['value']['id']['$oid'] == identifier:
            return result.get['value']['online']

    print('Restaurant name disappeared (may due to brute force restrictions)!')
    return False


if __name__ == '__main__':
    restaurant_name = input("Enter the restaurant name: ")
    results = search_restaurant(restaurant_name)

    if not results:
        print('Search returned 0 restaurant!')
        exit(1)

    for i, result in enumerate(results, start=1):
        result_value = result['value']
        full_name = result_value['name'][0]['value']
        address = result_value['address']
        print(f'[{i}]\t{full_name}\t{address}')

    restaurant_index = int(input("Enter the requested restaurant id: "))

    restaurant_data = results[restaurant_index - 1]
    restaurant_id = restaurant_data['value']['id']['$oid']
    public_url = restaurant_data['value']['public_url']

    while not is_opened(restaurant_name, restaurant_id):
        print("Restaurant is closed, sleeping for seconds!")
        time.sleep(INTERVAL_TIME_SEC)

    print(f"Restaurant is open! visit: {public_url}")
    while True:
        winsound.Beep(VOICE_FREQUENCY, VOICE_DURATION)
        time.sleep(1)
