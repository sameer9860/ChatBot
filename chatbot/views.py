from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import difflib

lemmatizer = WordNetLemmatizer()

knowledge_base = {

# =====================================================
# 🇳🇵 NEPAL – GENERAL INFORMATION
# =====================================================

"nepal": "Nepal is a landlocked country in South Asia between India and China.",
"capital of nepal": "The capital city of Nepal is Kathmandu.",
"kathmandu": "Kathmandu is the political, cultural and economic center of Nepal.",
"population of nepal": "Nepal has a population of around 30 million people.",
"area of nepal": "Nepal covers 147,516 square kilometers.",
"currency of nepal": "The currency of Nepal is Nepalese Rupee (NPR).",
"official language": "The official language of Nepal is Nepali.",
"national flower": "The national flower of Nepal is Rhododendron.",
"national animal": "The national animal of Nepal is Cow.",
"national bird": "The national bird of Nepal is Danphe (Himalayan Monal).",
"national flag": "Nepal has a unique triangular flag.",
"time zone": "Nepal Time is UTC +5:45.",
"highest mountain": "Mount Everest is the highest mountain in the world.",
"mount everest": "Mount Everest is 8,848.86 meters tall.",
"longest river": "The Koshi River is one of the longest rivers of Nepal.",
"largest lake": "Rara Lake is the largest lake of Nepal.",
"highest lake": "Tilicho Lake is one of the highest lakes in the world.",
"major religion": "Hinduism is the major religion in Nepal.",
"birthplace of buddha": "Lumbini is the birthplace of Lord Buddha.",
"lumbini": "Lumbini is a UNESCO World Heritage Site.",

# =====================================================
# 🏛 GOVERNMENT & POLITICS
# =====================================================

"president of nepal": "The President of Nepal is Ram Chandra Poudel.",
"prime minister of nepal": "The Prime Minister of Nepal is Pushpa Kamal Dahal (Prachanda).",
"federal republic": "Nepal is a Federal Democratic Republic.",
"constitution of nepal": "Nepal adopted its constitution on September 20, 2015.",
"federalism": "Nepal became federal after the 2015 constitution.",
"number of provinces": "Nepal has 7 provinces.",
"parliament": "Nepal has a bicameral federal parliament.",
"supreme court": "The Supreme Court is the highest judicial body of Nepal.",
"election commission": "The Election Commission conducts elections in Nepal.",

# =====================================================
# 🗺 PROVINCES & CITIES
# =====================================================

"koshi province": "Koshi Province is Province No. 1 of Nepal.",
"madhesh province": "Madhesh Province is Province No. 2.",
"bagmati province": "Bagmati Province includes Kathmandu Valley.",
"gandaki province": "Gandaki Province includes Pokhara.",
"lumbini province": "Lumbini Province contains Buddha's birthplace.",
"karnali province": "Karnali is the largest province of Nepal.",
"sudurpaschim province": "Sudurpashchim is the far western province.",
"pokhara": "Pokhara is a major tourism city.",
"lalitpur": "Lalitpur is also called Patan.",
"bhaktapur": "Bhaktapur is famous for temples and culture.",
"biratnagar": "Biratnagar is an industrial city.",
"birgunj": "Birgunj is a major trade gateway to India.",
"dharan": "Dharan is known for its scenic beauty.",
"hetauda": "Hetauda is an industrial hub.",

# =====================================================
# 🏔 TOURISM & HERITAGE
# =====================================================

"pashupatinath": "Pashupatinath is a famous Hindu temple in Kathmandu.",
"chitwan national park": "Chitwan National Park is famous for wildlife safari.",
"sagarmatha national park": "Sagarmatha National Park includes Mount Everest.",
"muktinath": "Muktinath is a sacred pilgrimage site.",
"janakpur": "Janakpur is the birthplace of Goddess Sita.",
"rara lake": "Rara Lake is the largest lake of Nepal.",
"tilicho lake": "Tilicho Lake is one of the highest altitude lakes.",
"boudhanath": "Boudhanath Stupa is a UNESCO World Heritage Site.",
"swayambhunath": "Swayambhunath is also known as Monkey Temple.",

# =====================================================
# 📜 HISTORY OF NEPAL
# =====================================================

"ancient nepal": "Ancient Nepal was ruled by the Kirat dynasty.",
"kirat dynasty": "The Kirats were among the earliest rulers.",
"lichhavi dynasty": "The Lichhavi ruled from 400 to 750 AD.",
"malla dynasty": "The Malla kings ruled Kathmandu Valley.",
"prithvi narayan shah": "Prithvi Narayan Shah unified Nepal in 1768.",
"unification of nepal": "Nepal was unified by King Prithvi Narayan Shah.",
"rana regime": "The Rana regime ruled from 1846 to 1951.",
"jung bahadur rana": "Jung Bahadur Rana started Rana rule.",
"democracy 1951": "Nepal became democratic in 1951.",
"panchayat system": "The Panchayat system lasted from 1960 to 1990.",
"people movement 1990": "The 1990 movement restored democracy.",
"maoist insurgency": "The Maoist conflict lasted from 1996 to 2006.",
"people movement 2006": "The 2006 movement ended monarchy.",
"abolition of monarchy": "Nepal abolished monarchy in 2008.",
"last king": "The last king of Nepal was King Gyanendra Shah.",

# =====================================================
# 🎓 EDUCATION SYSTEM
# =====================================================

"education system": "Nepal has school level, secondary level and university level education.",
"see": "SEE stands for Secondary Education Examination.",
"neb": "NEB stands for National Examination Board.",
"plus two": "+2 is higher secondary education.",
"higher education": "Higher education includes bachelor, master and PhD degrees.",
"ctevt": "CTEVT manages technical education in Nepal.",
"moest": "Ministry of Education manages education policies.",

# =====================================================
# 🏫 UNIVERSITIES
# =====================================================

"tribhuvan university": "Tribhuvan University was established in 1959.",
"kathmandu university": "Kathmandu University was established in 1991.",
"pokhara university": "Pokhara University was established in 1997.",
"purbanchal university": "Purbanchal University is in eastern Nepal.",
"far western university": "Far Western University is in Sudurpashchim.",
"mid western university": "Mid Western University is in Surkhet.",
"agriculture university": "Agriculture and Forestry University is in Chitwan.",

# =====================================================
# 💻 ICT & BACHELOR PROGRAMS
# =====================================================

"ict": "ICT stands for Information and Communication Technology.",
"bachelor in nepal": "Bachelor degrees in Nepal typically take 4 years.",
"bsc csit": "BSc CSIT is a 4-year computer science program under TU.",
"bca": "BCA stands for Bachelor in Computer Applications.",
"bit": "BIT stands for Bachelor in Information Technology.",
"bim": "BIM stands for Bachelor in Information Management.",
"bsc it": "BSc IT focuses on software and networking.",
"computer engineering": "Computer Engineering combines hardware and software.",
"software engineering": "Software Engineering focuses on software development lifecycle.",
"cyber security": "Cyber Security focuses on protecting digital systems.",
"data science": "Data Science involves analyzing large data sets.",
"ai": "Artificial Intelligence focuses on smart machines.",
"machine learning": "Machine Learning is a branch of AI.",
"networking": "Networking involves connecting computers and devices.",
"database": "Database systems store and manage data.",
"web development": "Web development includes frontend and backend coding.",
"python course": "Python is widely used in ICT programs.",
"java course": "Java is used for enterprise and Android development.",
"internship": "ICT students often complete internships in IT companies.",
"it career": "ICT graduates can work as developer, analyst, engineer, or IT officer.",
"scope of csit": "CSIT graduates have strong career opportunities in Nepal and abroad.",
"software companies in nepal": "Nepal has growing software and outsourcing companies.",
"freelancing": "Many ICT graduates in Nepal work as freelancers.",
"government it job": "Public Service Commission conducts IT officer exams.",
}
greetings = ["hello", "hi", "hey"]
greeting_responses = [
    "Hello! Ask me something.",
    "Hi there!",
]

def chatbot_response(user_input):
    user_input_lower = user_input.lower()

    # Greeting check
    for greet in greetings:
        if greet in user_input_lower:
            return random.choice(greeting_responses)

    # Exact match first
    for key in sorted(knowledge_base.keys(), key=len, reverse=True):
        if key in user_input_lower:
            return knowledge_base[key]

    # Advanced fuzzy matching
    best_score = 0
    best_key = None

    for key in knowledge_base.keys():
        score = difflib.SequenceMatcher(None, user_input_lower, key).ratio()
        if score > best_score:
            best_score = score
            best_key = key

    if best_score > 0.6:
        return knowledge_base[best_key]

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

    # If no chat selected → create new one
    if not chat_id:
        chat = Chat.objects.create(
            user=request.user,
            title=user_message[:30]
        )
    else:
        chat = Chat.objects.get(id=chat_id, user=request.user)

    bot_reply = chatbot_response(user_message)

    # Save messages
    Message.objects.create(chat=chat, sender="user", content=user_message)
    Message.objects.create(chat=chat, sender="bot", content=bot_reply)

    return JsonResponse({
        "response": bot_reply,
        "chat_id": chat.id
    })
    
@login_required
def load_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id, user=request.user)
    messages = chat.messages.all().order_by("timestamp")

    data = []
    for msg in messages:
        data.append({
            "sender": msg.sender,
            "content": msg.content
        })

    return JsonResponse({"messages": data})    