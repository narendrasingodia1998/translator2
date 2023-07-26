from app.models.request import Request
from app.utils.helper2 import valid_language

async def validate(request_data):
    '''
    request_data : dict
    return : Response object
    '''
    source_language = request_data.get("source_language").lower().strip()
    request = Request('language_finder')
    response = await request.async_api_call(request_data)
    #If we not able to detect then
    if response.error:
        return response
    detected_language = response.data['source_language']
    #checking if source language is given
    if len(source_language.strip()) > 0:
        # Checking for valid language
        if not valid_language(source_language):
            response.input_language_error(source_language)
            return response
        elif detected_language.lower() != source_language.lower():
            response.miss_matched_error()
            return response
    target_language = request_data.get('target_language').lower().strip() 
    if not valid_language(target_language):
        response.output_language_error(target_language)
    return response 

def split_text_into_chunks(text, chunk_size):
    chunks = []
    current_chunk = ""

    for word in text.split():
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    # Add the last chunk, if any
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def create_data(request,response):
    '''
    request_data : dict
    response : Response object
    return dict
    '''
    request_data = {
    'source_language': response.data['source_language'],
    'source_text' : request['source_text'],
    'target_language': request['target_language']}
    return request_data

