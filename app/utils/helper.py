from app.utils.helper2 import valid_language
from app.managers.find_language import Finder


def validate(request_data):
    ans = {'error': 0}
    source_language = request_data.get("source_language").lower().strip()

    finder = Finder()
    translated_txt = finder.api_call(request_data)
    if translated_txt['error']:
        return translated_txt
    detected_language = translated_txt['detected_language']

    # Checking if source language is given
    if len(source_language.strip()) > 0:
        # Checking for valid language
        if not valid_language(source_language):
            ans['error'] = 1
            ans["error_message"] = "API does not support {} language as source language".format(source_language)
            return ans
        elif detected_language.lower() != source_language.lower():
            ans['error'] = 1
            ans['error_message'] = 'Detected Language doesnot match with Source Language'
            return ans
    ans['source_language'] = detected_language
    request_data['source_language'] = detected_language
    target_language = request_data.get('target_language').lower().strip()
    ans['target_language'] = target_language
    # checking if target language is valid or not
    if not valid_language(target_language):
        ans['error'] = 1
        ans["error_message"] = "API does not support {} language as target language".format(target_language)
        return ans
    return ans


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

