from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

knowledge_base = {
    "math": "Mathematics is the study of numbers.",
    "python": "Python is a programming language.",
}

greetings = ["hello", "hi", "hey"]
greeting_responses = [
    "Hello! Ask me something.",
    "Hi there!",
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

    return "I don't know that yet."

# -------- SIGNUP --------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/signup.html', {'form': form})

# -------- HOME --------
@login_required
def home(request):
    chats = Chat.objects.filter(user=request.user)
    return render(request, "chatbot/home.html", {"chats": chats})

# -------- GET RESPONSE --------
@login_required
def get_response(request):
    user_message = request.GET.get("message")
    chat_id = request.GET.get("chat_id")

    chat = Chat.objects.get(id=chat_id, user=request.user)

    bot_reply = chatbot_response(user_message)

    Message.objects.create(chat=chat, sender="user", content=user_message)
    Message.objects.create(chat=chat, sender="bot", content=bot_reply)

    return JsonResponse({"response": bot_reply})