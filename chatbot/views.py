from django.shortcuts import render
from django.http import JsonResponse
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

knowledge_base = {
    "math": "Mathematics is the study of numbers, quantities, and shapes.",
    "algebra": "Algebra is a branch of mathematics dealing with symbols and equations.",
    "geometry": "Geometry studies shapes and space.",
    "science": "Science studies the natural world.",
    "physics": "Physics studies matter and energy.",
    "chemistry": "Chemistry studies substances and reactions.",
    "biology": "Biology studies living organisms.",
    "history": "History studies past events.",
    "python": "Python is a simple and powerful programming language."
}

greetings = ["hello", "hi", "hey"]
greeting_responses = [
    "Hello! Ask me an educational question.",
    "Hi there! What would you like to learn?",
    "Hey! I'm ready to help you learn."
]

def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    return [lemmatizer.lemmatize(word) for word in tokens]

def chatbot_response(user_input):
    tokens = preprocess(user_input)

    for word in tokens:
        if word in greetings:
            return random.choice(greeting_responses)

    for word in tokens:
        if word in knowledge_base:
            return knowledge_base[word]

    return "Sorry, I don't have information on that topic yet."

def home(request):
    return render(request, "chatbot/home.html")

def get_response(request):
    user_message = request.GET.get("message")
    response = chatbot_response(user_message)
    return JsonResponse({"response": response})