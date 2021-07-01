import time
import requests
# from urllib import robotparser

def download(url, user_agent='wswp', num_retries = 2):
        print("Downloading:", url)
    #if rp.can_fetch(user_agent, url):
        headers = {'User-agent': user_agent}
        try:
            html = requests.get(url, headers = headers, timeout=5)
            html.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Download error:", e)
            if num_retries > 0 and 500 <= html.status_code <= 600:
                # recursively retry 5xx HTTP errors
                time.sleep(10)
                return download(url, user_agent, num_retries - 1)
            html = None
        except requests.exceptions.Timeout as e:
            print("Download error:", e)
            time.sleep(10)
            if num_retries > 0:
                # retry when TimeOut error
                return download(url, user_agent, num_retries - 1)
            html = None
        except requests.exceptions.ConnectionError as e:
            print("Download error:", e)
            time.sleep(10)
            if num_retries > 0:
                # retry when Connection error
                return download(url, user_agent, num_retries - 1)
            html = None
        except requests.exceptions.RequestException as e:  
            print("Download error:", e)
            html = None
        return html
    #else:
    #    print("Forbidden directory")
    #    html = None
    #    return html