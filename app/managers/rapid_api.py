import requests

from app.Config.config import rapid_api_key
from app.utils.constants import UrlEndPoints
from app.utils.helper2 import get_code


class Rapid_translator:
    def __init__(self):
        pass

    def api_call(self, request_data):
        ans = {}
        print('rapid_api')
        ans['error'] = 0
        ans['source_language'] = request_data.get('source_language')
        target_language = get_code(request_data.get('target_language'))
        source_language = get_code(request_data.get('source_language'))
        print(f"Source Language :{source_language}")
        print(f"Target Language :{target_language}")
        try:
            url = UrlEndPoints.RAPID_URL
            payload = {
                "source_language": source_language,
                "target_language": target_language,
                "text": request_data.get('source_text')
            }
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": rapid_api_key,
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
            }

            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                response = response.json()
                ans['target_text'] = response.get('data').get('translatedText')
            else:
                ans['error'] = 1
                ans['error_message'] = 'Cannot able to translate'
        except:
            ans['error'] = 1
            ans['error_message'] = 'Cannont able to connect API'
        return ans
