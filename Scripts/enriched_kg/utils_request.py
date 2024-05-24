from datetime import datetime
import time
import requests

def make_request_with_retry(url, headers=None, params = None):
    while True:
        try:
            response = requests.get(url, headers= headers, params = params)
            if response.status_code == 403:
                retry_after = response.headers.get('Retry-After')
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        retry_time = datetime.strptime(retry_after, '%a, %d %b %Y %H:%M:%S %Z')
                        wait_time = (retry_time - datetime.utcnow()).total_seconds()

                    if wait_time > 0:
                        print(f"Access forbidden. Retrying after {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                else:
                    print("Access forbidden but no Retry-After header present. Cannot retry.")
                    print(response.text, response.status_code)
                    print(response.headers)
                    print(response.content)
                    return None

            response.raise_for_status()

            if response.headers.get('Content-Type') == 'application/json':
                try:
                    data = response.json()
                    return data
                except requests.exceptions.JSONDecodeError:
                    print("Error: Unable to parse JSON. Response content is not valid JSON.")
                    return None
            else:
                return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred: {e}")
            return None