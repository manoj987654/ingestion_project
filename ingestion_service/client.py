import time
import requests


def fetch_data(url, params=None, headers=None, retries=3, delay=2):
    """
    Fetch data from an API with retry logic.

    Args:
        url: API URL
        params: Query parameters
        headers: HTTP headers
        retries: Number of retry attempts
        delay: Delay (seconds) between retries
    """

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:

            print(f"Attempt {attempt} failed: {e}")

            if attempt == retries:
                raise Exception(
                    f"Failed to fetch data after {retries} attempts."
                )

            print(f"Retrying in {delay} seconds...\n")

            time.sleep(delay)