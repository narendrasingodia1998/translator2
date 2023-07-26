from sanic.response import json
from app.utils.helper2 import get_language
class Response():
    def __init__(self):
        self.error = 0
        self.data = {}
        self.data['error'] = 0
    
    def build(self,response,url_type):
        '''
        response : dict
        url_type : str ('google' ,'rapid', 'lacto', 'language_finder')
        '''
        if url_type == 'google':
            self.data['target_text']=response['data']['translations'][0]['translatedText']
        
        elif url_type == 'rapid':
            self.data['target_text'] = response['data']['translatedText']
            #self.data['source_language']
        
        elif url_type == 'lacto':
            self.data['target_text'] = response['translations'][0]['translated'][0]
        
        elif url_type == 'language_finder':
            self.data['source_language'] = get_language(response.get('data').get('detections')[0][0].get('language'))
    
    def timeout_error(self):
        self.error = 1
        self.data['error_message'] = 'Request is time out'
    
    def input_language_error(self,source_language):
        '''
        source_language : str
        '''
        self.error = 1
        self.data['error_message'] = "API does not support {} language as source language".format(source_language)
    
    def output_language_error(self,output_language):
        '''
        output_language : str
        '''
        self.error = 1
        self.data['error_message'] = "API does not support {} language as output language".format(output_language)
    
    def miss_matched_error(self):
        self.error = 1
        self.data['error_message'] = 'Detected Language doesnot match with Source Language'
    
    def json(self):
        self.data['error'] = self.error
        return json(self.data)
    
    def add_source_lang(self,source_language=""):
        '''
        soucre_language : str
        '''
        self.data['source_language'] = source_language
    
    def add_source_text(self,txt):
        '''
        txt : str
        '''
        self.data['source_text'] = txt
