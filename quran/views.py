from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from pymongo import MongoClient
from bson import json_util
import json, re, convert_numbers

db = MongoClient("mongodb://localhost:27017")


sname = '!"#$%&'+"'()*+,-./0123456789:;<=>?@aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ[\]^_`{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ"
def bangla_digit(value):
    val = str(value).replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯")
    return val

def replace_substring(text):
    # Define regular expression pattern for matching substrings
    pattern = r'\[.{1,2}\]'  # Matches "[" followed by 1 or 2 characters and then "]"
    
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    
    # Replace each match with an empty string
    for match in matches:
        text = text.replace(match, "")
    
    return text

def quran_home(request):
    suras = db.quran.surah_list.find({})
    datas = json.loads(json_util.dumps(suras))
    i = 0
    for data in datas:
        data['index'] = sname[i]
        data['sid'] = bangla_digit(data['id'])
        data['total_verses'] = bangla_digit(data['total_verses'])
        i+=1
    context = {
        "suras": datas
    }
    return render(request, 'quran-home.html', context)

def sura_details(request, id):
    get_sura = db.quran.surah_list.find_one({"id": id})
    sura_list = db.quran.surah_list.find({}, {"bn_name": 1, "id": 1})
    sura = json.loads(json_util.dumps(get_sura))
    sura['index'] = sname[int(sura['id'])-1]
    if sura['bn_type'] == 'মক্কা':
        sura['bn_type'] = 'মাক্কী'
    else:
        sura['bn_type'] = 'মাদানী'
    ayats = db.quran.surah.find_one({"index": id})['ayats']
    sura['ayats'] = ayats
    sura['translate_by'] = 'আবু বকর মুহাম্মাদ যাকারিয়া'
    sura['language'] = 'Bengali'
    pipeline = [
        {"$match": {"surah_id": id}},
        {"$group": {"_id": "$verse_id", "words": {"$push": {"ar": "$words_ar", "id": "$_id", "wid": "$words_id", "bn": "$translate_bn"}}}}
    ]
    words = db.quran.bywords.aggregate(pipeline)
    sorted_data = [(item['_id'], item['words']) for item in words]
    sorted_data = sorted(sorted_data, key=lambda x: x[0])
    verses = [{'id': item[0], 'words': item[1], "arabic_text": ayats[item[0]-1]['arabic_text'], "translation": ayats[item[0]-1]['translation'], "footnotes": ayats[item[0]-1]['footnotes']} for item in sorted_data]
    
    context = {
        "sura": sura,
        "verses": verses,
        "sura_list": sura_list
    }
    return render(request, 'sura.html', context)

def verses(request, id):
    page = request.GET.get('page', 2)
    start_id = ((int(page)-1)*20)+1
    end_id = int(page)*20
    get_sura = db.quran.surah_list.find_one({"id": id})
    sura = json.loads(json_util.dumps(get_sura))
    ayats = db.quran.surah.find_one({"index": id})['ayats']
    sura['ayats'] = ayats[start_id-1:end_id]
    sura['translate_by'] = 'আবু বকর মুহাম্মাদ যাকারিয়া'
    sura['language'] = 'Bengali'
    pipeline = [
        {"$match": {"surah_id": id, "verse_id": {"$gte": start_id, "$lte": end_id}}},
        {"$group": {"_id": "$verse_id", "words": {"$push": {"ar": "$words_ar", "id": "$_id", "wid": "$words_id", "bn": "$translate_bn"}}}}
    ]
    words = db.quran.bywords.aggregate(pipeline)
    sorted_data = [(item['_id'], item['words']) for item in words]
    sorted_data = sorted(sorted_data, key=lambda x: x[0])
    verses = [{'id': item[0], 'words': item[1], "arabic_text": ayats[item[0]-1]['arabic_text'], "translation": ayats[item[0]-1]['translation'], "footnotes": ayats[item[0]-1]['footnotes']} for item in sorted_data]
    
    context = {
        "sura": sura,
        "verses": verses
    }
    return JsonResponse(context)
    

def sura_translate(request, id):
    get_sura = db.quran.surah_list.find_one({"id": id})
    sura = json.loads(json_util.dumps(get_sura))
    ayats = db.quran.surah.find_one({"index": id})['ayats']
    sura['ayats'] = ayats
    sura['translate_by'] = 'আবু বকর মুহাম্মাদ যাকারিয়া'
    sura['language'] = 'Bengali'
    pipeline = [
        {"$match": {"surah_id": id}},
        {"$group": {"_id": "$verse_id", "words": {"$push": {"ar": "$words_ar", "id": "$_id", "wid": "$words_id", "bn": "$translate_bn"}}}}
    ]
    words = db.quran.bywords.aggregate(pipeline)
    sorted_data = [(item['_id'], item['words']) for item in words]
    sorted_data = sorted(sorted_data, key=lambda x: x[0])
    verses = [{'id': item[0], 'words': item[1], "arabic_text": sura['ayats'][item[0]-1]['arabic_text'], "translation": sura['ayats'][item[0]-1]['translation'], "footnotes": sura['ayats'][item[0]-1]['footnotes']} for item in sorted_data]
    
    context = {
        "sura": sura,
        "verses": verses
    }
    return render(request, 'sura/translate.html', context)

def sura_tafseer(request, id):
    get_sura = db.quran.surah_list.find_one({"id": id})
    sura = json.loads(json_util.dumps(get_sura))
    ayats = db.quran.surah.find_one({"index": id})['ayats']
    sura['ayats'] = ayats
    sura['translate_by'] = 'আবু বকর মুহাম্মাদ যাকারিয়া'
    sura['language'] = 'Bengali'
    pipeline = [
        {"$match": {"surah_id": id}},
        {"$group": {"_id": "$verse_id", "words": {"$push": {"ar": "$words_ar", "id": "$_id", "wid": "$words_id", "bn": "$translate_bn"}}}}
    ]
    words = db.quran.bywords.aggregate(pipeline)
    sorted_data = [(item['_id'], item['words']) for item in words]
    sorted_data = sorted(sorted_data, key=lambda x: x[0])
    verses = [{'id': item[0], 'words': item[1], "arabic_text": sura['ayats'][item[0]-1]['arabic_text'], "translation": sura['ayats'][item[0]-1]['translation'], "footnotes": sura['ayats'][item[0]-1]['footnotes']} for item in sorted_data]
    
    context = {
        "sura": sura,
        "verses": verses
    }
    return render(request, 'sura/tafseer.html', context)

def sura_reading(request, id):
    get_sura = db.quran.surah_list.find_one({"id": id})
    sura = json.loads(json_util.dumps(get_sura))
    ayats = db.quran.surah.find_one({"index": id})['ayats']
    sura['ayats'] = ayats
    sura['translate_by'] = 'আবু বকর মুহাম্মাদ যাকারিয়া'
    sura['language'] = 'Bengali'
    pipeline = [
        {"$match": {"surah_id": id}},
        {"$group": {"_id": "$verse_id", "words": {"$push": {"ar": "$words_ar", "id": "$_id", "wid": "$words_id", "bn": "$translate_bn"}}}}
    ]
    words = db.quran.bywords.aggregate(pipeline)
    sorted_data = [(item['_id'], item['words']) for item in words]
    sorted_data = sorted(sorted_data, key=lambda x: x[0])
    verses = [{'id': item[0], 'words': item[1], "arabic_text": sura['ayats'][item[0]-1]['arabic_text'], "translation": sura['ayats'][item[0]-1]['translation'], "footnotes": sura['ayats'][item[0]-1]['footnotes']} for item in sorted_data]
    
    context = {
        "sura": sura,
        "verses": verses
    }
    return render(request, 'sura/reading.html', context)