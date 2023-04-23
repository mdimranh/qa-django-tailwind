from django.shortcuts import render
from django.http import JsonResponse
from question.models import Question


import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
              

class question_data:
    def __init__(self):
        self.questions = []
        for question in Question.objects.all():
            self.questions.append({"question": question.question, "id": question.id, "user": {"first_name": question.user.first_name, "last_name": question.user.last_name}})

        self.corpus = [question['question'] for question in self.questions]
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        self.corpus_tokens = [self.tokenizer.tokenize(sent.lower()) for sent in self.corpus]
        self.corpus_clean = [' '.join(tokens) for tokens in self.corpus_tokens]
        self.vectorizer = TfidfVectorizer()
        self.document_vectores = self.vectorizer.fit_transform(self.corpus_clean)
        
    def processed(self):
        return [self.vectorizer, self.document_vectores, self.questions]
    
question_data = question_data().processed()

def question_search(query):

    # Vectorize the query
    query_vector = question_data[0].transform([query.lower()])

    # Compute cosine similarity between the query and document vectors
    similarity_scores = cosine_similarity(query_vector, question_data[1])
    
    print(similarity_scores)

    # Create a list of dictionaries containing the documents, similarity scores, and indices
    results = []
    for i, doc in enumerate(question_data[2]):
        if similarity_scores[0][i] >= 0.5:
            result = {
                "question": doc["question"],
                "id": doc["id"],
                "user": doc['user'],
                "score": similarity_scores[0][i]
            }
            results.append(result)

    # Sort the results by similarity scores in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:20]


def search_question(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        result = question_search(query)
        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        query = request.POST.get('query')
        result = question_search(query)
        return render(request, 'signin.html', {'query': query})

