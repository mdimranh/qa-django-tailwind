from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from bson import json_util
import re, json, string

db = MongoClient("mongodb://localhost:27017")


sname = '!"#$%&'+"'()*+,-./0123456789:;<=>?@aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ[\]^_`{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ"
def bangla_digit(value):
    val = str(value).replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯")
    return val

def quran_home(request):
    suras = db.quran.surah_list.find({})
    datas = json.loads(json_util.dumps(suras))
    # index = [i for i in range(1, 10)]+list(string.ascii_lowercase)[:-2]+list(string.ascii_uppercase)+['0162']
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


import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the documents
# documents = [
#     {"arabic": "الثعلب البني السريع يقفز فوق الكلب الكسول.", "bengali": "ত্বরিত বাদামী হরিণ আলস্য সারাবার.", "index": 1},
#     {"arabic": "الثعلب البني السريع حيوان ذكي.", "bengali": "ত্বরিত বাদামী হরিণ একটি চতুর প্রাণী।", "index": 2}
# ]

def replace_substring(text):
    # Define regular expression pattern for matching substrings
    pattern = r'\[.{1,2}\]'  # Matches "[" followed by 1 or 2 characters and then "]"
    
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    
    # Replace each match with an empty string
    for match in matches:
        text = text.replace(match, "")
    
    return text
              

class quran_data:
    def __init__(self):
        self.ayats = []
        for document in db.quran.surah.find({}):
            for ayat in document['ayats']:
                self.ayats.append({"arabic": ayat['arabic_text'], "bengali": replace_substring(ayat['translation']), "sura": ayat['sura'], "aya": ayat['aya']})

        self.corpus = [doc["arabic"] + " " + doc["bengali"] for doc in self.ayats]
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        self.corpus_tokens = [self.tokenizer.tokenize(sent.lower()) for sent in self.corpus]
        self.corpus_clean = [' '.join(tokens) for tokens in self.corpus_tokens]
        self.vectorizer = TfidfVectorizer()
        self.document_vectores = self.vectorizer.fit_transform(self.corpus_clean)
        
    def processed(self):
        return [self.vectorizer, self.document_vectores, self.ayats]
    
quran_data = quran_data().processed()

def quran_search(query):
    
    if len(query) < 5:
        return []

    # Vectorize the query
    query_vector = quran_data[0].transform([query.lower()])

    # Compute cosine similarity between the query and document vectors
    similarity_scores = cosine_similarity(query_vector, quran_data[1])
    
    print(similarity_scores)

    # Create a list of dictionaries containing the documents, similarity scores, and indices
    results = []
    for i, doc in enumerate(quran_data[2]):
        if similarity_scores[0][i] >= 0.5:
            result = {
                "arabic": doc["arabic"],
                "bengali": doc["bengali"],
                "sura": doc["sura"],
                "aya": doc['aya'],
                "score": similarity_scores[0][i]
            }
            results.append(result)

    # Sort the results by similarity scores in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:20]


def search_quran(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        result = quran_search(query)
        return JsonResponse(result, safe=False)

