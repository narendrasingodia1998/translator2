import json
from requests_cache import CachedSession
from app.Config.config import lacto_api_key
from app.utils.constants import UrlEndPoints
from app.utils.helper2 import get_code


class Lacto_translator:

    def __init__(self):
        pass

    def api_call(self, request_data):
        ans = {}
        ans['error'] = 0
        ans['source_language'] = request_data.get('source_language')
        target_language = get_code(request_data.get('target_language'))
        source_language = get_code(request_data.get('source_language'))
        # Add code for try and except and also for respone not getting because of limited trail
        try:
            headers = {
                'X-API-Key': lacto_api_key,
                'Content-Type': 'json',
                'Accept': 'json'}
            url = UrlEndPoints.LACTO_URL
            data = {'texts': [request_data.get('source_text')],
                    "to": [target_language],
                    "from": source_language}
            session = CachedSession(cache_name='cache/translator')
            response = session.post(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response_dict = response.json()
                # print (response_dict)
                ans['target_text'] = response_dict.get('translations')[0].get('translated')[0]
            else:
                ans['error'] = 1
                ans['error_message'] = 'Free Limit is expried for Lacto API'
        except:
            ans['error'] = 1
            ans['error_message'] = 'Cannont able to connect Lacto API'
        return ans
