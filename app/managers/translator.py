from app.models.request import Request
from app.models.response import Response
async def translator(request_data,url_type):
    '''
    request_data : dict
    url_type = str ('google', 'lacto', 'rapid', 'language_finder')
    '''
    request = Request(url_type)
    our_response  =   await request.async_api_call(request_data)
    return our_response
    our_response.add_source_text(request_data['source_text'])
    return our_response
