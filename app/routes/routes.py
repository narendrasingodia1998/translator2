import os
from sanic import Sanic
from sanic.response import json
from sanic import response
from app.utils.helper import validate
from app.utils.lang_code import lang_code
from app.managers.find_language import Finder
from app.managers.lacto_api import Lacto_translator
from app.managers.rapid_api import Rapid_translator
from app.managers.google_api import Google_translator

app = Sanic("Translator")


@app.route('/')
async def index(request):
    with open(os.path.join(os.getcwd(), 'app/html/translator.html')) as f:
        a = f.read()
    return response.html(a)


@app.route('/find')
async def finding(request):
    with open(os.path.join(os.getcwd(), 'app/html/detector.html')) as f:
        a = f.read()
    return response.html(a)


@app.post('/finder')
async def find(request):
    finder = Finder()
    request_data = request.json
    translated_txt = finder.api_call(request_data)
    return json(translated_txt)


@app.post('/google_api')
async def google(request):
    translator = Google_translator()
    request_data = request.json
    ans = validate(request_data)
    if ans['error']:
        return json(ans)
    translated_txt = translator.api_call(request_data)
    return json(translated_txt)


@app.post('/lacto_ai_api')
async def lacto(request):
    translator = Lacto_translator()
    request_data = request.json
    ans = validate(request_data)
    if ans['error']:
        return json(ans)
    translated_txt = translator.api_call(request_data)
    return json(translated_txt)


@app.post('/rapid_api')
async def rapid(request):
    translator = Rapid_translator()
    request_data = request.json
    ans = validate(request_data)
    if ans['error']:
        return json(ans)
    translated_txt = translator.api_call(request_data)
    print(translated_txt)
    return json(translated_txt)


@app.post('/file_google_api')
async def file_translate(request):
    translator = Google_translator()
    request_data = request.json
    print(request_data)
    input_file = request_data['input_file']
    output_language = request_data['output_language']
    output_file = input_file.split('.')[0] + '_' + output_language + '.' + input_file.split('.')[1]
    ans = await translator.translate_file(input_file, output_file, output_language)
    print(ans)
    return json(ans)
    pass


@app.post('/suggestion')
async def suggest(request):
    request_data = request.json
    suggestions = []
    print("Suggestion is called")
    target_string = request_data.get('text')
    n = len(target_string)
    if not n:
        return suggestions
    for word in lang_code.keys():
        if target_string.lower() == word[:n].lower():
            suggestions.append(word)
    if len(suggestions) > 10:
        suggestions = suggestions[:10]
    ans = {'suggestion': suggestions}
    return json(ans)
