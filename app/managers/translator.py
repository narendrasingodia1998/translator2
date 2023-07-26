from app.models.request import Request
from app.utils.helper import validate,create_data
async def translator(request_data,url_type):
    '''
    request_data : dict
    url_type : str ('google', 'lacto', 'rapid', 'language_finder')
    Return : Request object 
    '''
    val_response = await validate(request_data)
    if val_response.error:
        return val_response.json()
    request_data = create_data(request_data,val_response)
    request = Request(url_type)
    our_response = await request.async_api_call(request_data)
    our_response.add_source_text(request_data['source_text'])
    our_response.add_source_lang(val_response.data['source_language'])
    return our_response