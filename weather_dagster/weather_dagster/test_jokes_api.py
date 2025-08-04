"""Example of a simple API client to fetch jokes from JokeAPI."""
import requests

def get_jokes(jokes_amount: int=1) -> list[dict]:
    """Fetches a specified number of jokes from the JokeAPI."""
    url = f"https://v2.jokeapi.dev/joke/Any?amount={jokes_amount}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data.get('jokes', [])
    return []

if __name__ == "__main__":
    jokes = get_jokes(5)
    for joke in jokes:
        print(joke)
