import requests
import pandas as pd
from time import sleep
import json


def main(total_data):
    url = "https://kitsu.io/api/edge/anime"

    offset = len(total_data)

    while offset < 15000:
        params = {
            "page[limit]": 20,
            "page[offset]": offset,
            "sort": "-average_rating",
            "fields[anime]": "titles,averageRating,episodeCount,userCount,favoritesCount,popularityRank,ageRating,nsfw",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()["data"]
        total_data.extend(data)
        offset = len(total_data)
        print("total: ", offset)

        sleep(1.5)

    print("Done!")


if __name__ == "__main__":

    result = []
    try:
        with open("dataset.json", mode="r") as f:
            result = json.load(f)
    except:
        pass

    try:
        main(result)
    except Exception as ex:
        print(str(ex))
    finally:
        df = pd.json_normalize(result)
        df.to_json("dataset.json", indent=4, orient="records")
