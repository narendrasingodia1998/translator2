import asyncio
import aiohttp
from app.models.response import Response
from async_timeout import timeout
from app.Config import config
from app.utils.helper2 import get_code
from app.utils.constants import UrlEndPoints
from aiohttp_client_cache import CachedSession, SQLiteBackend

class Request():
    def __init__(self,url_type):
        self.url = ""
        self.params =None
        self.data = None
        self.headers = None
        self.url_type = url_type
        self.response = Response()

    def build(self,request_data):
        '''
        request_data : dict
        '''
        if self.url_type == 'google':
            self.url = UrlEndPoints.GOOGLE_URL
            self.params = {
                "q": request_data.get('source_text'),
                "target": get_code(request_data.get('target_language')),
                "key": config.google_api_key}
        
        elif self.url_type == 'language_finder':
            self.url = UrlEndPoints.GOOGLE_URL + '/detect'
            self.params = {
                "q": request_data.get('source_text'),
                "key": config.google_api_key,
            }

        elif self.url_type == 'rapid':
            self.url = UrlEndPoints.RAPID_URL
            self.data = {
                "source_language": get_code(request_data.get('source_language')),
                "target_language": get_code(request_data.get('target_language')),
                "text": request_data.get('source_text')
            }
            self.headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": config.rapid_api_key,
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
            }
        
        elif self.url_type == 'lacto':
            self.url = UrlEndPoints.LACTO_URL
            self.headers = {
                'X-API-Key': config.lacto_api_key,
                'Content-Type': 'json',
                'Accept': 'json'}
            self.data = {'texts': [request_data.get('source_text')],
                    "to": [get_code(request_data.get('target_language'))],
                    "from": get_code(request_data.get('source_language'))}

    async def  async_api_call(self,request_data):
        '''
        request_data :  dict
        our_response : Response
        '''
        self.build(request_data)
        timeout = aiohttp.ClientTimeout(total=1)
        our_response = Response()
        try:
            async with CachedSession(cache=SQLiteBackend('cache/demo_cache',allowed_methods=('GET', 'POST')),allowable_methods = ['GET','POST']) as session:
                async with session.post(self.url,headers=self.headers,
                                        params=self.params,data=self.data,timeout=timeout) as response:                
                        response = await response.json()
                        return response
                        #print(f"request output is {response}")
                        our_response.build(response,self.url_type)
                        return  our_response
        except asyncio.TimeoutError:
            our_response.timeout_error()
        return our_response
    

