from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
import random
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
"prime minister of nepal": "The Prime Minister of Nepal is Sushila Karki.",
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
# 🎓 EDUCATION SYSTEM OF NEPAL
# =====================================================

"education system": "Nepal's education system includes Early Childhood Development (ECD), basic level (Grade 1–8), secondary level (Grade 9–12), and higher education (Bachelor, Master, PhD).",
"education policy": "Nepal's school education is guided by the School Education Sector Plan (SESP) under the Ministry of Education, Science and Technology.",
"moest": "The Ministry of Education, Science and Technology (MoEST) formulates and implements education policies in Nepal.",
"literacy rate": "Nepal's literacy rate is approximately 76% according to recent surveys.",
"ecd": "Early Childhood Development (ECD) covers children aged 3–5 years before formal schooling.",
"primary education": "Primary education in Nepal covers Grades 1 to 5 and is compulsory and free.",
"basic education": "Basic education in Nepal covers Grades 1 to 8.",
"secondary education": "Secondary education in Nepal covers Grades 9 to 12.",
"grade 9 10": "Grades 9 and 10 are lower secondary, ending with the SEE exam.",
"grade 11 12": "Grades 11 and 12 are higher secondary, managed by NEB.",
"see": "SEE (Secondary Education Examination) is taken after Grade 10 and is conducted by the National Examination Board.",
"neb": "NEB (National Examination Board) conducts the Grade 11 and Grade 12 board examinations in Nepal.",
"plus two": "Plus Two (+2) refers to Grades 11 and 12 of higher secondary education in Nepal, offered in streams like Science, Management, Humanities, Law, and Education.",
"science stream": "The Science stream in +2 includes Physics, Chemistry, Biology or Math, and Computer Science.",
"management stream": "The Management stream in +2 includes subjects like Accountancy, Economics, and Business Studies.",
"humanities stream": "The Humanities stream includes subjects like Sociology, Political Science, History, and Geography.",
"education stream": "The Education stream trains students for teaching professions.",
"law stream": "The Law stream at +2 level prepares students for legal studies.",
"ctevt": "CTEVT (Council for Technical Education and Vocational Training) manages diploma and vocational/technical education in Nepal.",
"technical education": "Technical education in Nepal includes programs in engineering, health, agriculture, and IT offered through CTEVT.",
"vocational training": "Vocational training programs in Nepal are managed by CTEVT and help students gain job-ready skills.",
"diploma level": "Diploma programs under CTEVT are typically 3 years long after SEE.",
"open school": "The National Open School under NEB allows out-of-school learners to continue education flexibly.",
"non formal education": "Non-formal education programs in Nepal target adult literacy and school dropouts.",
"private school": "Private schools in Nepal follow the national curriculum but charge fees; many follow Cambridge or CBSE boards.",
"public school": "Public (community) schools in Nepal are government-funded and free for students.",
"community school": "Community schools are managed by local governments and school management committees.",
"boarding school": "Boarding schools in Nepal offer residential facilities along with education.",
"cambridge board": "Some private schools in Nepal are affiliated with Cambridge International Examinations (CIE).",
"cbse nepal": "Some schools in Nepal, especially in border areas, follow CBSE (India) curriculum.",
"scholarship nepal": "The Government of Nepal offers various scholarships for higher education including Prime Minister Scholarship and IOST scholarships.",
"prime minister scholarship": "The Prime Minister Scholarship Program sends Nepali students abroad for higher studies.",
"foreign scholarship": "Nepal receives scholarships from countries like China, India, Japan, USA, and Australia for higher studies.",
"student loan": "Student loans in Nepal are offered by commercial banks under government-backed schemes.",
"tuition fee": "Tuition fees in Nepal vary: public universities charge low fees while private colleges charge higher fees.",
"higher education": "Higher education in Nepal includes bachelor, master, and PhD degree programs offered by universities.",
"grading system": "Nepal uses a GPA-based grading system: A+ (4.0), A (3.6–4.0), B+ (3.2), B (2.8), C+ (2.4), C (2.0), D (1.6), E (below 1.6).",
"see result": "SEE results are published by NEB, usually within 2–3 months of exams.",
"plus two result": "Plus Two (+2) results are published by NEB, usually mid-year.",

# =====================================================
# 🏫 UNIVERSITIES OF NEPAL
# =====================================================

"tribhuvan university": "Tribhuvan University (TU), established in 1959, is the oldest and largest university in Nepal with over 60 constituent campuses and 1,000+ affiliated colleges.",
"tu affiliated colleges": "Tribhuvan University has over 1,000 affiliated colleges across Nepal offering bachelor and master programs.",
"kathmandu university": "Kathmandu University (KU), established in 1991, is an autonomous institution known for engineering, medical, and management programs.",
"pokhara university": "Pokhara University (PU), established in 1997, is based in Gandaki Province and offers programs in engineering, management, science, and health.",
"purbanchal university": "Purbanchal University is located in Gothgaun, Morang, and serves eastern Nepal with various undergraduate and postgraduate programs.",
"far western university": "Far Western University is located in Mahendranagar, Kanchanpur, serving students of Sudurpashchim Province.",
"mid western university": "Mid-Western University is headquartered in Surkhet and serves students of Karnali and surrounding provinces.",
"agriculture university": "Agriculture and Forestry University (AFU) is located in Chitwan and focuses on agricultural, forestry, and environmental sciences.",
"nepal sanskrit university": "Nepal Sanskrit University focuses on Sanskrit language, Vedic studies, and traditional knowledge systems.",
"lumbini buddhist university": "Lumbini Buddhist University is dedicated to Buddhist philosophy, studies, and related disciplines.",
"rajarshi janak university": "Rajarshi Janak University serves Madhesh Province with programs in science, management, and education.",
"health sciences university": "Karnali Academy of Health Sciences focuses on health and medical education in Karnali Province.",
"constituent campus tu": "TU constituent campuses include Tri-Chandra, Amrit Science, Padma Kanya, and Trichandra among others.",
"iost": "IOST (Institute of Science and Technology) under TU offers BSc CSIT, BIT, and other science programs.",
"ioe": "IOE (Institute of Engineering) under TU offers BE programs in Civil, Electrical, Electronics, Computer, and Mechanical Engineering.",
"iom": "IOM (Institute of Medicine) under TU manages MBBS and other medical programs.",
"public administration campus": "Public Administration Campus under TU offers MPA and BPA programs.",

# =====================================================
# 💻 ICT & COMPUTER SCIENCE PROGRAMS
# =====================================================

"ict": "ICT stands for Information and Communication Technology, covering computer science, networking, software, and digital systems.",
"bsc csit": "BSc CSIT (Bachelor of Science in Computer Science and Information Technology) is a 4-year program under TU/IOST, one of the most popular IT programs in Nepal.",
"csit syllabus": "BSc CSIT covers subjects like C Programming, Data Structures, OOP, DBMS, Operating Systems, Networks, Web Technology, AI, and Software Engineering.",
"csit entrance": "BSc CSIT requires passing an entrance exam conducted by TU-IOST. Subjects include Physics, Chemistry, Math, and English.",
"csit colleges in nepal": "Popular BSc CSIT colleges include Deerwalk, Herald, National, ISMT, Trinity, and many others across Nepal.",
"scope of csit": "CSIT graduates have strong career opportunities in Nepal and abroad as developers, analysts, engineers, and IT officers.",
"bca": "BCA (Bachelor in Computer Application) is a 4-year program offered by TU and PU, focusing on application development.",
"bca syllabus": "BCA covers subjects like C, Java, DBMS, Web Programming, Software Engineering, and Multimedia.",
"bca colleges nepal": "BCA is offered by colleges across Nepal under TU and PU, including Prime, Samriddhi, and many others.",
"bit": "BIT (Bachelor in Information Technology) is offered by PU and focuses on networking, systems, and IT management.",
"bim": "BIM (Bachelor in Information Management) is a 4-year program under TU focusing on management and IT integration.",
"bim syllabus": "BIM includes subjects like MIS, Database, Programming, E-commerce, and Business Communication.",
"bsc it": "BSc IT is offered by various universities and focuses on software engineering, databases, and networking.",
"be computer": "BE in Computer Engineering under IOE/TU is a 4-year engineering program focusing on both hardware and software.",
"be electronics": "BE in Electronics Engineering covers digital systems, communication, and embedded systems.",
"msc csit": "MSc CSIT is a 2-year postgraduate program under TU for graduates of BSc CSIT and related fields.",
"mit": "MIT (Master of Information Technology) is a postgraduate program offered by KU and other universities.",
"mca": "MCA (Master of Computer Applications) is a 2-year postgraduate program in computer applications.",
"phd computer": "PhD programs in Computer Science are available at TU and KU for advanced research.",
"computer engineering": "Computer Engineering combines hardware and software, offered as BE under IOE-TU.",
"software engineering": "Software Engineering focuses on software development lifecycle including design, testing, and deployment.",
"cyber security": "Cyber Security focuses on protecting digital systems, networks, and data from threats and attacks.",
"data science": "Data Science involves analyzing large datasets to extract insights using statistics and machine learning.",
"ai": "Artificial Intelligence (AI) focuses on building smart machines capable of learning and decision-making.",
"machine learning": "Machine Learning is a branch of AI where systems learn from data to improve over time.",
"networking": "Networking involves connecting computers and devices to share resources and communicate.",
"database": "Database systems store, manage, and retrieve structured data efficiently.",
"web development": "Web development includes frontend (HTML, CSS, JS) and backend (Python, PHP, Node.js) coding.",
"python course": "Python is widely used in data science, AI, and web development in ICT programs in Nepal.",
"java course": "Java is used for enterprise software and Android development in ICT programs.",
"it entrance preparation": "Students prepare for IT entrance exams through coaching classes and study of Math, Physics, and English.",

# =====================================================
# 🔬 ENGINEERING & SCIENCE PROGRAMS
# =====================================================

"be civil": "BE Civil Engineering under IOE focuses on structural, transportation, and environmental engineering.",
"be electrical": "BE Electrical Engineering covers power systems, electronics, and control systems.",
"be mechanical": "BE Mechanical Engineering covers thermodynamics, manufacturing, and machine design.",
"be architecture": "BE Architecture under IOE covers design, construction, and urban planning.",
"ioe entrance": "IOE Entrance Exam is conducted by TU-IOE for admission to BE programs. It includes Physics, Chemistry, and Math.",
"pulchowk campus": "Pulchowk Campus is the leading constituent campus of IOE-TU offering BE programs in Lalitpur.",
"thapathali campus": "Thapathali Campus of IOE offers BE in Civil, Mechanical, and Industrial Engineering.",
"ku engineering": "Kathmandu University's School of Engineering offers BE programs with a focus on research and quality education.",
"bsc physics": "BSc Physics is a 4-year science program under TU covering classical and modern physics.",
"bsc chemistry": "BSc Chemistry covers organic, inorganic, and physical chemistry.",
"bsc math": "BSc Mathematics covers calculus, algebra, statistics, and discrete mathematics.",
"bsc microbiology": "BSc Microbiology is popular among students aiming for medical laboratory or research careers.",
"bsc environmental science": "BSc Environmental Science covers ecology, pollution control, and natural resource management.",

# =====================================================
# 🩺 MEDICAL & HEALTH PROGRAMS
# =====================================================

"mbbs": "MBBS (Bachelor of Medicine and Bachelor of Surgery) is a 5.5-year medical program in Nepal managed by IOM-TU and other universities.",
"mbbs entrance": "MBBS entrance is conducted by MEC (Medical Education Commission) of Nepal. It covers Physics, Chemistry, Biology, and English.",
"mec": "MEC (Medical Education Commission) regulates medical education and conducts entrance exams for health science programs in Nepal.",
"bds": "BDS (Bachelor of Dental Surgery) is a 5-year dental program offered by medical colleges in Nepal.",
"bpharma": "BPharm (Bachelor of Pharmacy) covers pharmaceutical sciences and drug management.",
"bns": "BNS (Bachelor of Nursing Science) is a 4-year nursing program in Nepal.",
"bpt": "BPT (Bachelor of Physiotherapy) focuses on rehabilitation and physical therapy.",
"bams": "BAMS (Bachelor of Ayurvedic Medicine and Surgery) is offered by some colleges in Nepal.",
"bsc nursing": "BSc Nursing is a popular health science program for students aspiring to work in hospitals and clinics.",
"health science colleges": "Nepal has several medical colleges including TUTH, BPKIHS, Manipal, Nobel, and Kathmandu Medical College.",
"bpkihs": "BP Koirala Institute of Health Sciences (BPKIHS) is a leading health science university in Dharan.",
"pahs": "PAHS (Patan Academy of Health Sciences) is a public medical institution in Lalitpur.",

# =====================================================
# 📊 MANAGEMENT & BUSINESS PROGRAMS
# =====================================================

"bbs": "BBS (Bachelor of Business Studies) is a 4-year management program under TU, one of the most popular programs in Nepal.",
"bbs syllabus": "BBS covers Accountancy, Economics, Business Studies, Finance, Marketing, and Management.",
"bba": "BBA (Bachelor of Business Administration) is offered by KU, PU, and affiliated colleges. It is a 4-year program.",
"bbm": "BBM (Bachelor of Business Management) is offered by some universities in Nepal.",
"mbs": "MBS (Master of Business Studies) is a 2-year postgraduate program under TU.",
"mba": "MBA (Master of Business Administration) is offered by KU, PU, and affiliated colleges.",
"ca nepal": "Chartered Accountancy (CA) in Nepal is managed by ICAN (Institute of Chartered Accountants of Nepal).",
"ican": "ICAN (Institute of Chartered Accountants of Nepal) manages CA education and certification.",
"acca": "ACCA (Association of Chartered Certified Accountants) is a globally recognized accounting qualification pursued by many Nepali students.",
"commerce stream": "Commerce stream at +2 includes Accountancy, Economics, and Business Mathematics.",

# =====================================================
# ⚖️ LAW & SOCIAL SCIENCE PROGRAMS
# =====================================================

"llb": "LLB (Bachelor of Laws) is a 3-year law program available after +2 at TU and other universities.",
"ba llb": "BA LLB is a 5-year integrated law program offered by KU and some TU affiliated colleges.",
"llm": "LLM (Master of Laws) is a postgraduate law program in Nepal.",
"ba": "BA (Bachelor of Arts) under TU is a 4-year program covering subjects like Sociology, Political Science, Economics, and History.",
"bsw": "BSW (Bachelor of Social Work) trains students in community development and social service.",
"bpa": "BPA (Bachelor of Public Administration) focuses on public policy, administration, and governance.",
"bpes": "BPES (Bachelor of Physical Education and Sports) trains students in sports science and physical education.",

# =====================================================
# 🌾 AGRICULTURE & FORESTRY PROGRAMS
# =====================================================

"bsc agriculture": "BSc Agriculture is a 4-year program under AFU and TU covering crop production, soil science, and agronomy.",
"bsc forestry": "BSc Forestry focuses on forest management, ecology, and environmental conservation.",
"bsc food technology": "BSc Food Technology covers food processing, preservation, and quality control.",
"agriculture education": "Agriculture education in Nepal is important given the country's farming economy.",

# =====================================================
# 🌍 STUDY ABROAD & SCHOLARSHIPS
# =====================================================

"study abroad": "Nepali students can study abroad in countries like the USA, UK, Australia, Canada, Japan, South Korea, and Germany.",
"usa study": "The USA is a top destination for Nepali students for undergraduate and graduate programs.",
"australia study": "Australia is popular among Nepali students for its quality education and post-study work rights.",
"japan study": "Japan offers MEXT scholarships for Nepali students to study at Japanese universities.",
"south korea study": "South Korea's GKS (Global Korea Scholarship) is available for Nepali students.",
"germany study": "Germany offers free or low-cost education for international students including Nepalis.",
"india study": "Many Nepali students pursue higher education in India through ICCR scholarships.",
"china study": "China offers CSC (Chinese Government Scholarship) for Nepali students.",
"sat": "SAT is a standardized test required for admission to US universities.",
"gre": "GRE (Graduate Record Examination) is required for master's programs in the USA and other countries.",
"gmat": "GMAT is required for MBA admissions abroad.",
"toefl": "TOEFL is an English proficiency test required by US and other universities.",
"ielts": "IELTS is an English proficiency test required for UK, Australia, Canada, and other countries.",
"visa for study": "Nepali students need a student visa (like F-1 for USA, Subclass 500 for Australia) to study abroad.",

# =====================================================
# 📚 ENTRANCE EXAMS
# =====================================================

"entrance exam": "Most bachelor programs in Nepal (Engineering, Medical, CSIT, BCA) require passing a competitive entrance exam.",
"ioe entrance exam": "IOE Entrance covers Physics, Chemistry, Math, and English. It is highly competitive.",
"mec entrance exam": "MEC Entrance for medical programs covers Physics, Chemistry, and Biology.",
"csit entrance exam": "CSIT Entrance covers Math, Physics, Chemistry, and English under TU-IOST.",
"entrance preparation": "Students prepare for entrance exams through coaching institutes and practice of past questions.",
"ku entrance": "Kathmandu University conducts its own entrance exams for BE, BBA, and other programs.",
"pu entrance": "Pokhara University conducts entrance exams for its affiliated programs.",

# =====================================================
# 🏫 NOTABLE COLLEGES & INSTITUTIONS
# =====================================================

"deerwalk": "Deerwalk Institute of Technology is a leading BSc CSIT college in Kathmandu.",
"herald college": "Herald College Kathmandu offers UK-affiliated bachelor programs including Computing and Business.",
"ismt college": "ISMT College offers CSIT and BCA programs affiliated with TU.",
"prime college": "Prime College in Kathmandu is affiliated with TU and offers BBA, BCA, and BBS.",
"xavier international": "Xavier International College offers UK and Australian university affiliated programs.",
"national college": "National College is a prominent CSIT and BCA college under TU.",
"kist college": "KIST College in Kathmandu offers CSIT and BCA programs.",
"softwarica college": "Softwarica College of IT and E-Commerce is affiliated with Coventry University, UK.",
"nccs": "NCCS (National College of Computer Studies) is one of Nepal's earliest IT colleges.",
"la grandee": "La Grandee International College offers programs affiliated with Pokhara University.",

# =====================================================
# 💼 CAREERS & EMPLOYMENT
# =====================================================

"it career": "ICT graduates in Nepal can pursue careers as Software Developer, Data Analyst, Network Engineer, Cybersecurity Expert, IT Officer, or System Administrator.",
"government job": "Government IT jobs are conducted through the Public Service Commission (PSC) of Nepal.",
"psc": "PSC (Public Service Commission) recruits government employees in Nepal through competitive exams.",
"loksewa": "Loksewa Aayog (PSC) conducts exams for civil service jobs including IT officer posts.",
"private sector job": "Private IT companies in Nepal like F1Soft, Leapfrog, Cotiviti, and Deerwalk hire IT graduates.",
"freelancing": "Many Nepali IT graduates earn through freelancing on platforms like Upwork, Fiverr, and Freelancer.",
"software companies in nepal": "Nepal has growing software companies like F1Soft, CloudFactory, Leapfrog Technology, Cotiviti, Deerwalk, and many startups.",
"startup nepal": "Nepal's startup ecosystem is growing, with hubs in Kathmandu supporting IT and tech ventures.",
"internship": "ICT students in Nepal typically complete a 6-week to 3-month internship in IT companies as part of their curriculum.",
"it park": "IT parks are being developed in Nepal to support the tech industry, including one in Banepa.",
"remote work": "Remote work opportunities have grown for Nepali IT professionals working for foreign companies.",
"salary it nepal": "Entry-level IT salaries in Nepal range from NPR 25,000 to 60,000 per month depending on skills and company.",
"government it job": "Public Service Commission conducts IT officer exams for government positions in Nepal.",

# =====================================================
# 🌐 NEPAL ECONOMY & TRADE
# =====================================================

"economy of nepal": "Nepal has a mixed economy based on agriculture, remittance, tourism, and hydropower.",
"gdp of nepal": "Nepal's GDP is approximately 40 billion USD, with a per capita income of around 1,300 USD.",
"remittance nepal": "Remittance contributes over 25% of Nepal's GDP, sent by Nepali workers abroad.",
"foreign employment": "Millions of Nepalis work in countries like Qatar, UAE, Saudi Arabia, Malaysia, and South Korea.",
"agriculture nepal": "Agriculture employs about 65% of Nepal's workforce. Main crops are rice, maize, wheat, and millet.",
"tourism economy": "Tourism is a major income source for Nepal, attracting trekkers, climbers, and pilgrims.",
"hydropower nepal": "Nepal has vast hydropower potential of over 40,000 MW. Several projects are operational and under construction.",
"trade nepal": "Nepal's major trading partners are India and China. Nepal imports more than it exports.",
"inflation nepal": "Nepal's inflation rate has generally been in the range of 6–8% in recent years.",
"budget nepal": "Nepal's annual government budget is around NPR 1.5 trillion.",
"poverty nepal": "Nepal's poverty rate has declined significantly, now below 20% due to remittances and development.",
"foreign aid nepal": "Nepal receives foreign aid from India, China, USA, World Bank, ADB, and UN agencies.",
"world bank nepal": "The World Bank supports many infrastructure, health, and education projects in Nepal.",
"adb nepal": "Asian Development Bank (ADB) funds major development projects in Nepal.",
"stock market nepal": "NEPSE (Nepal Stock Exchange) is Nepal's only stock exchange.",
"nepse": "NEPSE (Nepal Stock Exchange) was established in 1993 and lists banks, hydro, and insurance companies.",
"nrb": "NRB (Nepal Rastra Bank) is the central bank of Nepal, regulating monetary policy.",
"banking nepal": "Nepal has several commercial banks, development banks, and finance companies regulated by NRB.",
"cooperative nepal": "Cooperatives play a major role in rural finance and agriculture in Nepal.",
"sez nepal": "Nepal has Special Economic Zones (SEZ) in Bhairahawa and Simara to attract investment.",

# =====================================================
# 🎭 CULTURE, FESTIVALS & SOCIETY
# =====================================================

"culture of nepal": "Nepal has a rich culture influenced by Hinduism and Buddhism, with diverse ethnic groups and traditions.",
"dashain": "Dashain is the biggest Hindu festival in Nepal, celebrated for 15 days in autumn.",
"tihar": "Tihar (Diwali) is the festival of lights celebrated for 5 days in Nepal.",
"holi": "Holi is the festival of colors celebrated in Nepal, especially in Terai regions.",
"indra jatra": "Indra Jatra is a major festival celebrated in Kathmandu with chariot processions.",
"bisket jatra": "Bisket Jatra is the New Year festival of Bhaktapur celebrated with chariot pulling.",
"teej": "Teej is a women's festival in Nepal where women fast and pray for their husbands.",
"losar": "Losar is the Tibetan/Sherpa New Year celebrated by Buddhist communities in Nepal.",
"chhath": "Chhath is a Hindu festival celebrated mainly in Terai, dedicated to the Sun God.",
"maghe sankranti": "Maghe Sankranti marks the end of winter and is celebrated with traditional foods.",
"ethnic groups nepal": "Nepal has over 125 ethnic groups including Brahmin, Chhetri, Newar, Magar, Tamang, Sherpa, Tharu, and many more.",
"nepali food": "Popular Nepali foods include Dal Bhat, Momo, Sel Roti, Dhido, Gundruk, and Chow Mein.",
"dal bhat": "Dal Bhat (lentil soup with rice) is the staple food of Nepal eaten twice daily.",
"momo": "Momo is a popular Nepali dumpling dish served steamed or fried with spicy chutney.",
"newari culture": "Newars are the indigenous people of Kathmandu Valley with rich art, architecture, and food culture.",
"sherpa community": "Sherpas are an ethnic group known for their mountaineering skills and guiding expertise.",
"tharu community": "Tharus are an indigenous ethnic group from the Terai region of Nepal.",
"gurung community": "Gurungs are an ethnic group from Gandaki Province known for serving in Gurkha armies.",
"rai community": "Rais are an ethnic group from eastern Nepal known for their martial traditions.",
"limbu community": "Limbus are an ethnic group from eastern Nepal with their own Kirat culture.",
"nepali dress": "Daura Suruwal and Dhaka Topi is the national dress of Nepali men.",
"nepali language": "Nepali is the official language, written in Devanagari script.",
"maithili language": "Maithili is the second most spoken language in Nepal, spoken in Madhesh Province.",
"newari language": "Newari (Nepal Bhasha) is the language of the Newar community of Kathmandu Valley.",
"nepali music": "Traditional Nepali music includes folk songs like Deuda, Selo, and Tamang Selo.",
"nepali cinema": "Nepali cinema (Kollywood) produces Nepali-language films based in Kathmandu.",

# =====================================================
# 🏔 GEOGRAPHY & ENVIRONMENT
# =====================================================

"geography of nepal": "Nepal is divided into three geographical zones: Himalayan region, Hilly region, and Terai (plains).",
"himalayan region": "The Himalayan region covers the northern part of Nepal with high altitude mountains.",
"hilly region": "The Hilly region covers the middle zone with valleys, hills, and rivers.",
"terai region": "The Terai is the flat southern lowland region, most fertile and densely populated.",
"climate of nepal": "Nepal has five seasons: Spring, Summer, Monsoon, Autumn, and Winter.",
"monsoon nepal": "Nepal receives heavy monsoon rainfall from June to September.",
"rivers of nepal": "Major rivers include Koshi, Gandaki, Karnali, Bagmati, and Rapti.",
"bagmati river": "The Bagmati River flows through Kathmandu and is sacred to Hindus.",
"koshi river": "The Koshi River is the largest river in Nepal, originating from the Himalayas.",
"gandaki river": "The Gandaki (Narayani) River flows through Gandaki Province and joins the Ganga.",
"karnali river": "The Karnali River is the longest river in Nepal, flowing through Karnali Province.",
"national parks nepal": "Nepal has 12 national parks including Chitwan, Sagarmatha, Langtang, and Bardiya.",
"bardiya national park": "Bardiya National Park in Karnali Province is home to tigers, rhinos, and elephants.",
"langtang national park": "Langtang National Park is near Kathmandu and is popular for trekking.",
"wildlife nepal": "Nepal is home to tigers, rhinos, snow leopards, elephants, red pandas, and over 900 bird species.",
"one horned rhino": "The one-horned rhinoceros is found mainly in Chitwan National Park.",
"snow leopard": "Snow leopards are found in the high Himalayan regions of Nepal.",
"red panda": "Red pandas are found in eastern Nepal's mountain forests.",
"conservation nepal": "Nepal is globally recognized for wildlife conservation efforts, especially for tigers and rhinos.",
"climate change nepal": "Nepal is highly vulnerable to climate change, causing glacial melting, floods, and landslides.",
"earthquake 2015": "A devastating 7.8 magnitude earthquake struck Nepal on April 25, 2015, killing nearly 9,000 people.",
"natural disasters nepal": "Nepal faces natural disasters including earthquakes, floods, landslides, and droughts.",

# =====================================================
# 🚗 TRANSPORT & INFRASTRUCTURE
# =====================================================

"transport nepal": "Nepal's transport includes roadways, airways, and limited railways. Roads are the main mode of transport.",
"tribhuvan airport": "Tribhuvan International Airport (TIA) in Kathmandu is Nepal's only international airport.",
"gautam buddha airport": "Gautam Buddha International Airport in Bhairahawa is Nepal's second international airport.",
"pokhara airport": "Pokhara Regional International Airport opened in 2023 as Nepal's third international airport.",
"nepal airlines": "Nepal Airlines Corporation (NAC) is the national flag carrier of Nepal.",
"road network nepal": "Nepal has over 30,000 km of roads including highways, feeder roads, and district roads.",
"araniko highway": "Araniko Highway connects Kathmandu with the Chinese border at Kodari.",
"prithvi highway": "Prithvi Highway connects Kathmandu and Pokhara.",
"mahendra highway": "Mahendra Highway (East-West Highway) runs across the Terai from east to west Nepal.",
"fast track nepal": "The Kathmandu-Nijgadh Fast Track is a major under-construction expressway in Nepal.",
"railway nepal": "Nepal has a narrow-gauge railway in Janakpur and a cross-border rail link with India at Raxaul.",
"ropeway nepal": "Ropeways are used in hilly areas for transporting goods and passengers.",
"electric vehicle nepal": "Nepal is promoting electric vehicles (EVs) to reduce fuel imports and pollution.",
"mechi bridge": "Mechi Bridge connects eastern Nepal with India.",
"friendship bridge": "Friendship Bridge at Kodari connects Nepal with Tibet/China.",

# =====================================================
# ⚕️ HEALTH SYSTEM OF NEPAL
# =====================================================

"health system nepal": "Nepal's health system includes government hospitals, community health centers, private hospitals, and health posts.",
"ministry of health": "The Ministry of Health and Population manages healthcare in Nepal.",
"bir hospital": "Bir Hospital is one of the oldest and largest government hospitals in Kathmandu.",
"tuth": "Tribhuvan University Teaching Hospital (TUTH) is a major referral hospital in Nepal.",
"patan hospital": "Patan Hospital is a non-profit hospital in Lalitpur known for quality care.",
"health insurance nepal": "Nepal has a national Health Insurance Program providing basic coverage to citizens.",
"malnutrition nepal": "Malnutrition, especially among children, remains a public health challenge in rural Nepal.",
"hiv aids nepal": "Nepal has programs to prevent and treat HIV/AIDS through the government and NGOs.",
"maternal health": "Nepal has significantly reduced its maternal mortality rate through health programs.",
"vaccination nepal": "Nepal has a national immunization program covering children against major diseases.",
"covid nepal": "Nepal experienced multiple waves of COVID-19 and conducted a mass vaccination campaign.",
"mental health nepal": "Mental health awareness is growing in Nepal, with limited but increasing services available.",
"telemedicine nepal": "Telemedicine services have expanded in Nepal to reach rural and remote areas.",
"ayurveda nepal": "Ayurvedic medicine is practiced widely in Nepal as a traditional healthcare system.",

# =====================================================
# ⚽ SPORTS IN NEPAL
# =====================================================

"sports nepal": "Popular sports in Nepal include football, cricket, volleyball, and traditional sports like Kabaddi and Dandi Biyo.",
"football nepal": "Football is one of the most popular sports in Nepal. ANFA manages football in Nepal.",
"anfa": "ANFA (All Nepal Football Association) is the governing body of football in Nepal.",
"cricket nepal": "Nepal is an Associate Member of ICC. Nepal has participated in World Cricket League events.",
"ncc": "NCC (Cricket Association of Nepal) governs cricket in Nepal.",
"nepal cricket team": "Nepal's cricket team has performed well in Associate-level international competitions.",
"volleyball nepal": "Volleyball is Nepal's national sport and extremely popular in hilly regions.",
"kabaddi nepal": "Kabaddi is a traditional contact sport popular in Nepal's villages and schools.",
"dandi biyo": "Dandi Biyo is Nepal's traditional national game similar to stick and ball.",
"olympics nepal": "Nepal has participated in the Olympics since 1964. Nepal competes in events like athletics and shooting.",
"khel mahakumbha": "Khel Mahakumbha is a national sports festival held in Nepal to promote sports.",
"mountain biking nepal": "Mountain biking is a growing adventure sport in Nepal, especially in Mustang and Pokhara.",
"bungee jumping nepal": "Nepal offers bungee jumping in Bhote Koshi, one of the highest bungee jumps in the world.",

# =====================================================
# 📡 MEDIA & COMMUNICATION
# =====================================================

"media nepal": "Nepal has a free press with many newspapers, TV channels, FM radios, and online portals.",
"gorkhapatra": "Gorkhapatra is the oldest and official government newspaper of Nepal, established in 1901.",
"kantipur": "Kantipur is one of the leading private newspapers in Nepal.",
"the himalayan times": "The Himalayan Times is one of Nepal's popular English-language daily newspapers.",
"republica": "Republica is an English-language newspaper published in Nepal.",
"nepal television": "Nepal Television (NTV) is the government-owned national TV broadcaster.",
"kantipur tv": "Kantipur TV is one of Nepal's most-watched private TV channels.",
"image channel": "Image Channel is a popular private TV channel in Nepal.",
"sagarmatha television": "Sagarmatha Television is one of Nepal's oldest private TV channels.",
"radio nepal": "Radio Nepal is the national public radio broadcaster of Nepal.",
"fm radio nepal": "Nepal has hundreds of FM radio stations broadcasting in various local languages.",
"internet nepal": "Internet penetration in Nepal has grown rapidly, with mobile internet being most common.",
"ntc": "NTC (Nepal Telecom) is the state-owned telecom company of Nepal.",
"ncell": "Ncell is a major private telecom company providing mobile services in Nepal.",
"social media nepal": "Facebook, TikTok, YouTube, and Instagram are widely used social media platforms in Nepal.",

# =====================================================
# 🌿 NGOs, INGOs & DEVELOPMENT
# =====================================================

"ngo nepal": "Nepal has thousands of NGOs and INGOs working in education, health, disaster relief, and women's rights.",
"ingo nepal": "International NGOs like CARE, Save the Children, Oxfam, and World Vision operate in Nepal.",
"undp nepal": "UNDP Nepal supports sustainable development, governance, and disaster resilience programs.",
"unicef nepal": "UNICEF Nepal works on child health, education, and protection programs.",
"who nepal": "WHO Nepal supports health system strengthening and disease prevention programs.",
"usaid nepal": "USAID funds various development programs in Nepal covering health, agriculture, and democracy.",
"asian development bank nepal": "ADB Nepal funds infrastructure, energy, and urban development projects.",
"volunteer nepal": "Many international volunteers come to Nepal for teaching, healthcare, and community service.",
"women empowerment nepal": "Many NGOs work on women empowerment, education, and reducing gender-based violence in Nepal.",
"child rights nepal": "Nepal has laws protecting child rights including the Children's Act 2018.",
"social security nepal": "Nepal provides social security allowances to elderly citizens, widows, and disabled persons.",
"dalit rights nepal": "Nepal has constitutional provisions against caste discrimination and for Dalit rights.",

# =====================================================
# 👨‍🎓 FAMOUS PEOPLE OF NEPAL
# =====================================================

"tenzing norgay": "Tenzing Norgay Sherpa, along with Edmund Hillary, first summited Mount Everest on May 29, 1953.",
"edmund hillary": "Sir Edmund Hillary of New Zealand and Tenzing Norgay first reached the summit of Everest in 1953.",
"bhanubhakta acharya": "Bhanubhakta Acharya is called Adikavi (first poet) of Nepal for translating Ramayana into Nepali.",
"laxmi prasad devkota": "Laxmi Prasad Devkota is Nepal's greatest poet, called Mahakavi, known for Muna Madan.",
"b p koirala": "BP Koirala was the first democratically elected Prime Minister of Nepal and a renowned author.",
"girija prasad koirala": "Girija Prasad Koirala was a prominent political leader and former Prime Minister of Nepal.",
"pushpa kamal dahal": "Pushpa Kamal Dahal (Prachanda) is the Chairman of CPN (Maoist Centre) and former PM of Nepal.",
"man bahadur gurung": "Man Bahadur Gurung is a famous Nepali mountaineer who summited multiple 8000m peaks.",
"nirmal purja": "Nirmal Purja (Nims Dai) set a world record by climbing all 14 eight-thousanders in 6 months.",
"pasang lhamu sherpa": "Pasang Lhamu Sherpa was the first Nepali woman to summit Mount Everest in 1993.",
"hari bansha acharya": "Hari Bansha Acharya is a celebrated comedian and actor in Nepal.",
"paul shah": "Paul Shah is a popular Nepali actor and model known for his work in Nepali cinema.",
"priyanka karki": "Priyanka Karki is a well-known Nepali actress and social media personality.",
"yama buddha": "Yama Buddha is a prominent Nepali hip-hop artist known for Nepali rap music.",
"1974 ad": "1974 AD is one of Nepal's most popular rock bands, known for songs like Sambodhan.",

# =====================================================
# 🏗 IMPORTANT PLACES & LANDMARKS
# =====================================================

"dharahara": "Dharahara (Bhimsen Tower) is a historic tower in Kathmandu, rebuilt after the 2015 earthquake.",
"narayanhiti palace": "Narayanhiti Palace was the royal palace of Nepal, now a museum open to public.",
"hanuman dhoka": "Hanuman Dhoka is the old royal palace in Kathmandu Durbar Square.",
"patan durbar square": "Patan Durbar Square is a UNESCO heritage site with ancient Newar architecture.",
"bhaktapur durbar square": "Bhaktapur Durbar Square is famous for the 55-Window Palace and Nyatapola Temple.",
"changu narayan": "Changu Narayan is a UNESCO World Heritage temple, the oldest in the Kathmandu Valley.",
"kopan monastery": "Kopan Monastery is a famous Tibetan Buddhist monastery near Kathmandu.",
"tengboche monastery": "Tengboche Monastery is a famous Buddhist monastery near Mount Everest.",
"garden of dreams": "The Garden of Dreams is a restored historical garden in Kathmandu, popular for relaxing.",
"taudaha lake": "Taudaha Lake is a natural lake on the outskirts of Kathmandu with scenic beauty.",
"gosaikunda lake": "Gosaikunda is a sacred alpine lake in Langtang National Park, pilgrimage destination.",
"phewa lake": "Phewa Lake is a scenic lake in Pokhara, popular for boating and mountain reflections.",
"begnas lake": "Begnas Lake is a peaceful lake near Pokhara, ideal for nature visits.",
"dhorpatan": "Dhorpatan Hunting Reserve is the only hunting reserve in Nepal.",

# =====================================================
# 🧗 TREKKING & ADVENTURE
# =====================================================

"trekking nepal": "Nepal is one of the world's top trekking destinations with routes in the Himalayas.",
"everest base camp trek": "The Everest Base Camp (EBC) Trek is a famous 12–14 day trek in Khumbu region.",
"annapurna circuit": "The Annapurna Circuit is a classic trekking route around the Annapurna massif.",
"annapurna base camp": "Annapurna Base Camp (ABC) trek is a popular shorter trek in the Annapurna region.",
"langtang trek": "Langtang Valley Trek is a scenic trek near Kathmandu through rhododendron forests.",
"manaslu circuit": "Manaslu Circuit Trek is a challenging trek around Mt. Manaslu, the 8th highest peak.",
"upper mustang trek": "Upper Mustang Trek explores the ancient Tibetan Buddhist kingdom of Lo Manthang.",
"gokyo lakes trek": "Gokyo Lakes Trek is a scenic alternative to EBC, featuring high-altitude turquoise lakes.",
"trekking permit": "Most trekking areas in Nepal require trekking permits like TIMS and national park entry permits.",
"tims": "TIMS (Trekkers' Information Management System) is a mandatory permit for trekkers in Nepal.",
"eight thousanders nepal": "Nepal has 8 of the world's 14 eight-thousander peaks including Everest, Kanchenjunga, and Lhotse.",
"kanchenjunga": "Kanchenjunga (8,586m) is the third highest mountain in the world, located in eastern Nepal.",
"lhotse": "Lhotse (8,516m) is the fourth highest mountain, located next to Everest.",
"makalu": "Makalu (8,485m) is the fifth highest mountain in the world, located in eastern Nepal.",
"cho oyu": "Cho Oyu (8,188m) is the sixth highest mountain, on the Nepal-Tibet border.",
"dhaulagiri": "Dhaulagiri (8,167m) is the seventh highest mountain, located in western Nepal.",
"manaslu": "Manaslu (8,163m) is the eighth highest mountain, located in Gorkha district.",
"annapurna i": "Annapurna I (8,091m) is the tenth highest mountain and the first 8000m peak ever climbed.",
"mountaineering nepal": "Nepal is the center of world mountaineering with permits required from the government.",
"white water rafting": "White water rafting is popular in rivers like Trishuli, Bhotekoshi, and Kali Gandaki.",
"paragliding nepal": "Paragliding in Pokhara is one of the most popular adventure activities in Nepal.",
"zip line nepal": "Nepal has some of the world's longest and steepest zip lines in Pokhara.",

# =====================================================
# ⚡ ENERGY & ENVIRONMENT
# =====================================================

"hydropower projects": "Major hydropower projects in Nepal include Upper Tamakoshi, Chilime, Kali Gandaki A, and Upper Karnali.",
"upper tamakoshi": "Upper Tamakoshi (456 MW) is Nepal's largest operational hydropower project.",
"melamchi water project": "Melamchi Water Supply Project brings drinking water to Kathmandu from Sindhupalchok.",
"solar energy nepal": "Solar energy adoption is growing in Nepal especially in remote off-grid areas.",
"electricity export": "Nepal exports electricity to India and aims to increase power trade.",
"load shedding nepal": "Nepal once faced severe load shedding (power cuts) but has improved electricity supply significantly.",
"petroleum nepal": "Nepal imports all petroleum products mainly from India through oil pipelines.",
"cooking gas nepal": "LPG cooking gas is widely used in urban Nepal; rural areas use firewood and biogas.",
"biogas nepal": "Biogas from animal waste is used as an alternative cooking fuel in rural Nepal.",

# =====================================================
# 🧾 GOVERNMENT SERVICES & DOCUMENTS
# =====================================================

"citizenship nepal": "Nepali citizenship can be obtained by birth, descent, or naturalization.",
"passport nepal": "Nepal passport is issued by the Department of Immigration in Kathmandu.",
"visa nepal": "Nepal offers tourist visas on arrival to most nationalities at Tribhuvan Airport.",
"nid card": "Nepal is rolling out National Identity (NID) cards to replace citizenship certificates.",
"land registration": "Land registration in Nepal is done at local government land offices.",
"nagarikta": "Nagarikta (citizenship certificate) is the primary identity document for Nepali citizens.",
"birth registration": "Birth registration in Nepal is done at local ward offices.",
"driving license nepal": "Driving license in Nepal is issued by the Department of Transport Management (DoTM).",
"vehicle registration": "Vehicle registration is done through the Department of Transport Management.",
"tax nepal": "Nepal's tax system is managed by the Inland Revenue Department (IRD).",
"pan card nepal": "PAN (Permanent Account Number) card is required for business and tax purposes in Nepal.",
"vat nepal": "VAT (Value Added Tax) rate in Nepal is 13%.",


# =====================================================
# 🌏 ADDITIONAL NEPAL - DISTRICTS & CITIES
# =====================================================

"districts of nepal": "Nepal has 77 districts across 7 provinces.",
"kathmandu district": "Kathmandu is the capital district and most urbanized area of Nepal.",
"lalitpur district": "Lalitpur district is known for Patan city and rich Newar heritage.",
"bhaktapur district": "Bhaktapur district is famous for traditional pottery and woodwork.",
"kaski district": "Kaski district includes Pokhara, a major tourist destination.",
" Chitwan district": "Chitwan district is famous for national park and wildlife.",
"morang district": "Morang district includes Biratnagar, an industrial hub.",
"sunsari district": "Sunsari district includes Dharan, known for education.",
"jhapa district": "Jhapa district is known for tea gardens and border trade.",
"dhanusa district": "Dhanusa district includes Janakpur, a religious city.",
"mahottari district": "Mahottari is a district in Madhesh Province.",
"sarlahi district": "Sarlahi is an agricultural district in Madhesh.",
"barpak": "Barpak is a village in Gorkha district, known for the 2015 earthquake epicenter.",
"ghandruk": "Ghandruk is a Gurung village near Pokhara, popular for trekking.",
"nagarkot": "Nagarkot is a hill station near Kathmandu known for mountain sunrise views.",
"poon hill": "Poon Hill is a famous viewpoint in the Annapurna region for sunrise.",
"tamel": "Tamel is a bustling market area in Kathmandu near Thamel.",
"thamel": "Thamel is the tourist hub of Kathmandu with shops, restaurants, and hotels.",
"new road": "New Road is the commercial center of Kathmandu.",
"ason": "Ason is a busy market area in central Kathmandu.",
"freak street": "Freak Street (Jochhen Street) is a famous area in Kathmandu from hippie era.",
"boudha": "Boudha is a neighborhood in Kathmandu known for Boudhanath Stupa.",
"sankhamul": "Sankhamul is an area in Kathmandu near the Bagmati River.",
"kalanki": "Kalanki is a major intersection in Kathmandu.",
"koteshwor": "Koteshwor is a commercial area in Kathmandu.",
"balaju": "Balaju is an area in Kathmandu known for the Balaju Garden.",
"puneshwor": "Puneshwor is an area in Kathmandu near the Pashupatinath Temple.",

# =====================================================
# 🛕 MORE RELIGIOUS & HISTORICAL SITES
# =====================================================

"swyambhunath": "Swayambhunath is an ancient Buddhist stupa also known as Monkey Temple.",
"guhyeshwari": "Guhyeshwari is a sacred Hindu temple near Pashupatinath.",
"narayan temple": "Narayan Temple (Brahmakapala) is in Kathmandu Durbar Square.",
"kumbeshwor": "Kumbeshwor is a deity in Patan, associated with the famous Kumbeshwor Temple.",
"krishna temple": "Krishna Temple in Patan Durbar Square is a masterpiece of stone carvings.",
"mahendreshwor": "Mahendreshwor is a temple in Patan dedicated to Lord Shiva.",
"golden gate": "The Golden Gate (Sun Dhokha) is the entrance to the palace in Bhaktapur.",
"nyatapola temple": "Nyatapola Temple in Bhaktapur is the tallest temple in Nepal, dedicated to Goddess Siddhi Lakshmi.",
"dattatraya temple": "Dattatraya Temple is in Bhaktapur, famous for its elaborate wood carvings.",
"vasupur": "Vasupur is a historical area in Patan.",
"ratan pur": "Ratanpur is an ancient settlement near Lalitpur.",
"tilganga": "Tilganga is an area in Kathmandu known for the Pashupatinath Temple vicinity.",
"gokarna": "Gokarna is a religious forest area near Kathmandu with temples.",
"sakta": "Sakta is a pilgrimage site near Kathmandu.",
"charikot": "Charikot is the headquarters of Dolakha district, near the Charikot Bazaar.",
"dolalghat": "Dolalghat is a religious site with temples and hot springs.",
"panauti": "Panauti is an ancient Newar town known for temples and historical monuments.",
"namo buddha": "Namo Buddha is a Buddhist pilgrimage site near Dhulikhel.",
"pharping": "Pharping is a sacred valley near Kathmandu with many Buddhist caves and temples.",
"gosainkunda": "Gosainkunda is a sacred alpine lake, pilgrimage site for Hindus and Buddhists.",

# =====================================================
# 🎭 MORE FESTIVALS & TRADITIONS
# =====================================================

"festival nepal": "Nepal celebrates many Hindu and Buddhist festivals throughout the year.",
"yam purnima": "Yam Purnima (Father's Day) is celebrated on the full moon of July.",
"janai purnima": "Janai Purnima is a Hindu festival where people change their sacred thread.",
"gai jatra": "Gai Jatra is a festival in August honoring cows and remembering ancestors.",
"krishna janmashtami": "Krishna Janmashtami celebrates the birth of Lord Krishna.",
"mahashivratri": "Maha Shivaratri is a major festival dedicated to Lord Shiva.",
"guru purnima": "Guru Purnima is a day to honor teachers and gurus.",
"vijaya dashami": "Vijaya Dashami is the final day of Dasain when people receive tika.",
"chaath puja": "Chhath Puja is dedicated to the Sun God, celebrated mainly in Terai.",
"shree panchami": "Shree Panchami (Basanta Panchami) marks the arrival of spring.",
"bratabandha": "Bratabandha is a Hindu coming-of-age ceremony for boys.",
"pasni": "Pasni is a rice-feeding ceremony for babies in Nepal.",
"ritu": "Ritu is a ceremony for a woman's first menstruation in some communities.",
"marriage nepal": "Traditional Nepali weddings involve many rituals including Tilak, tied corsage, and seven steps.",
"janti": "Janti is a wedding procession in Newari culture.",
"barahi": "Barahi is a traditional drum used in Nepali folk music.",
"murchunga": "Murchunga is a traditional Nepali bamboo flute.",
"dhyangro": "Dhyangro is a traditional drum used in Buddhist rituals.",
"thali": "Thali is a traditional metal plate used for serving food in Nepal.",

# =====================================================
# 🐄 MORE WILDLIFE & NATURE
# =====================================================

"bengal tiger": "Bengal tigers are found in Nepal's Terai national parks.",
"elephant nepal": "Asian elephants are found in Chitwan and Bardia National Parks.",
"leopard nepal": "Clouded leopards and common leopards are found in Nepal's forests.",
"gaur": "Gaur (Indian bison) is found in Nepal's national parks.",
"wild buffalo": "Wild water buffalo is found in Nepal's protected areas.",
"musk deer": "Musk deer is found in the high altitude regions of Nepal.",
"monkey nepal": "Rhesus macaques and Hanuman langurs are common monkeys in Nepal.",
"cheetah nepal": "The cheetah was historically found in Nepal but is now extinct.",
"birds nepal": "Over 900 bird species are found in Nepal including spiny babbler and Danphe.",
"danphe": "Danphe (Himalayan monal) is Nepal's national bird.",
"crane nepal": "Sarus cranes are found in Nepal's wetlands.",
"vulture nepal": "Vultures in Nepal include white-rumped and Himalayan griffon.",
"butterfly nepal": "Nepal has over 600 species of butterflies.",
"snake nepal": "Nepal has over 80 species of snakes including cobras and pythons.",
"crocodile nepal": "Marsh mugger crocodiles are found in Chitwan National Park.",
"flora nepal": "Nepal's flora includes rhododendrons, orchids, pines, and medicinal plants.",
"rhododendron": "Rhododendron is Nepal's national flower with many species in the Himalayas.",
"orchid nepal": "Nepal has over 500 species of orchids.",
"bamboo nepal": "Bamboo forests are found in the mid-hills of Nepal.",
"pine forest": "Pine forests are found in the hilly regions of Nepal.",

# =====================================================
# 🌍 WORLD KNOWLEDGE - COUNTRIES & CAPITALS
# =====================================================

"india": "India is a country in South Asia with New Delhi as its capital.",
"china": "China is the world's most populous country with Beijing as its capital.",
"usa": "United States of America has Washington D.C. as its capital.",
"uk": "United Kingdom has London as its capital.",
"japan": "Japan has Tokyo as its capital.",
"germany": "Germany has Berlin as its capital.",
"france": "France has Paris as its capital.",
"italy": "Italy has Rome as its capital.",
"russia": "Russia has Moscow as its capital.",
"brazil": "Brazil has Brasilia as its capital.",
"australia": "Australia has Canberra as its capital.",
"canada": "Canada has Ottawa as its capital.",
"south korea": "South Korea has Seoul as its capital.",
"india capital": "New Delhi is the capital of India.",
"china capital": "Beijing is the capital of China.",
"usa capital": "Washington D.C. is the capital of United States.",
"uk capital": "London is the capital of United Kingdom.",
"japan capital": "Tokyo is the capital of Japan.",
"pakistan": "Pakistan has Islamabad as its capital.",
"bangladesh": "Bangladesh has Dhaka as its capital.",
"sri lanka": "Sri Lanka has Sri Jayawardenepura Kotte as its capital.",
"afghanistan": "Afghanistan has Kabul as its capital.",
"iran": "Iran has Tehran as its capital.",
"iraq": "Iraq has Baghdad as its capital.",
"saudi arabia": "Saudi Arabia has Riyadh as its capital.",
"uae": "United Arab Emirates has Abu Dhabi as its capital.",
"qatar": "Qatar has Doha as its capital.",
"thailand": "Thailand has Bangkok as its capital.",
"vietnam": "Vietnam has Hanoi as its capital.",
"indonesia": "Indonesia has Jakarta as its capital.",
"malaysia": "Malaysia has Kuala Lumpur as its capital.",
"philippines": "Philippines has Manila as its capital.",
"singapore": "Singapore is a city-state and the capital of Singapore.",
"myanmar": "Myanmar has Naypyidaw as its capital.",
"maldives": "Maldives has Male as its capital.",
"bhutan": "Bhutan has Thimphu as its capital.",
"africa": "Africa is the second largest continent with 54 countries.",
"europe": "Europe has 44 countries with diverse cultures and history.",
"asia": "Asia is the largest continent with over 40 countries.",
"north america": "North America includes USA, Canada, Mexico and Central American countries.",
"south america": "South America includes countries like Brazil, Argentina, Peru, Colombia.",
"australia continent": "Australia is both a country and a continent in the Pacific Ocean.",
"antarctica": "Antarctica is the southernmost continent, covered in ice.",
"atlantic ocean": "The Atlantic Ocean is the second largest ocean.",
"pacific ocean": "The Pacific Ocean is the largest ocean.",
"indian ocean": "The Indian Ocean is the third largest ocean.",

# =====================================================
# 🏛 WORLD ORGANIZATIONS & LEADERS
# =====================================================

"united nations": "United Nations (UN) is an international organization promoting peace and cooperation.",
"un": "UN (United Nations) has headquarters in New York City.",
"who": "WHO (World Health Organization) is a UN agency for health.",
"unicef": "UNICEF is a UN agency for children's rights and welfare.",
"world bank": "World Bank provides loans for development projects globally.",
"imf": "IMF (International Monetary Fund) provides financial assistance to countries.",
"nato": "NATO is a military alliance of North American and European countries.",
"eu": "European Union is a political and economic union of 27 European countries.",
"saarc": "SAARC is an organization of South Asian countries including Nepal.",
"saff": "SAFF (South Asian Football Federation) governs football in South Asia.",
"bimstec": "BIMSTEC is an organization of Bay of Bengal countries.",
"asean": "ASEAN is an organization of Southeast Asian countries.",
"president usa": "The President of United States is the head of state and government.",
"prime minister india": "The Prime Minister of India is the head of government.",
"prime minister uk": "The Prime Minister of UK is the head of government.",
"chancellor germany": "The Chancellor of Germany is the head of government.",
"president france": "The President of France is the head of state.",
"king saudi": "The King of Saudi Arabia is the head of state.",
"emperor japan": "The Emperor of Japan is the ceremonial head of state.",

# =====================================================
# 🌋 NATURAL PHENOMENA & SCIENCE
# =====================================================

"volcano": "A volcano is an opening in Earth's crust through which lava and gases escape.",
"earthquake": "Earthquake is the shaking of Earth's surface caused by seismic waves.",
"tsunami": "Tsunami is a large ocean wave caused by earthquakes or volcanic eruptions.",
"hurricane": "Hurricane is a tropical cyclone with strong winds and rain.",
"cyclone": "Cyclone is a large rotating storm system.",
"climate change": "Climate change refers to long-term changes in global temperature and weather patterns.",
"global warming": "Global warming is the increase in Earth's average temperature.",
"greenhouse effect": "Greenhouse effect is the trapping of heat by gases in Earth's atmosphere.",
"ozone layer": "Ozone layer protects Earth from harmful ultraviolet radiation.",
"rainbow": "Rainbow appears when sunlight refracts through water droplets.",
"lightning": "Lightning is an electrical discharge during thunderstorms.",
"avalanche": "Avalanche is a mass of snow sliding down a mountain.",
"glacier": "Glacier is a large mass of ice that moves slowly.",
"fossil fuel": "Fossil fuels include coal, oil, and natural gas.",
"renewable energy": "Renewable energy includes solar, wind, hydro, and geothermal energy.",
"solar power": "Solar power uses energy from the sun to generate electricity.",
"wind energy": "Wind energy uses wind turbines to generate electricity.",
"nuclear energy": "Nuclear energy is generated through nuclear fission reactions.",

# =====================================================
# 💻 PROGRAMMING & COMPUTER SCIENCE
# =====================================================

"programming": "Programming is the process of creating instructions for computers.",
"python": "Python is a high-level programming language known for readability and versatility.",
"javascript": "JavaScript is a programming language for web development.",
"java": "Java is a widely-used object-oriented programming language.",
"c programming": "C is a foundational programming language for system programming.",
"c++": "C++ is an extension of C used for games and high-performance applications.",
"c sharp": "C# is a Microsoft language for Windows applications and game development.",
"ruby": "Ruby is known for elegant syntax and web development with Rails.",
"php": "PHP is a server-side scripting language for web development.",
"swift": "Swift is Apple's programming language for iOS and macOS apps.",
"kotlin": "Kotlin is a modern language for Android development.",
"go golang": "Go (Golang) is by Google for efficient and concurrent programming.",
"rust": "Rust is a systems programming language focused on safety.",
"typescript": "TypeScript adds type checking to JavaScript.",
"html": "HTML (HyperText Markup Language) is for creating web pages.",
"css": "CSS (Cascading Style Sheets) is for styling web pages.",
"sql": "SQL (Structured Query Language) is for database management.",
"react": "React is a JavaScript library for building user interfaces.",
"angular": "Angular is a TypeScript-based web application framework.",
"vue": "Vue is a progressive JavaScript framework for UI.",
"nodejs": "Node.js allows JavaScript to run on servers.",
"django": "Django is a Python web framework.",
"flask": "Flask is a lightweight Python web framework.",
"laravel": "Laravel is a PHP web framework.",
"spring": "Spring is a Java application framework.",
"git": "Git is a version control system for tracking code changes.",
"github": "GitHub is a platform for hosting and collaborating on code.",
"gitlab": "GitLab is a DevOps platform for code management.",
"vscode": "VSCode (Visual Studio Code) is a popular code editor.",
"algorithm": "Algorithm is a step-by-step procedure for solving problems.",
"data structure": "Data structure is a way of organizing and storing data.",
"oop": "OOP (Object-Oriented Programming) uses objects and classes.",
"api": "API (Application Programming Interface) allows software to communicate.",
"rest api": "REST is an architectural style for web services.",
"json": "JSON (JavaScript Object Notation) is a data format.",
"xml": "XML is a markup language for storing and transporting data.",
"frontend": "Frontend development deals with user interface and user experience.",
"backend": "Backend development deals with server-side logic and databases.",
"full stack": "Full stack developers work on both frontend and backend.",
"devops": "DevOps combines development and operations for faster delivery.",
"docker": "Docker is a platform for containerization.",
"kubernetes": "Kubernetes manages containerized applications.",
"cloud computing": "Cloud computing delivers computing services over the internet.",
"aws": "AWS (Amazon Web Services) offers cloud computing services.",
"azure": "Microsoft Azure is a cloud computing platform.",
"google cloud": "Google Cloud offers cloud computing services.",
"saas": "SaaS (Software as a Service) delivers software over the internet.",
"paas": "PaaS (Platform as a Service) provides development platforms.",
"iaas": "IaaS (Infrastructure as a Service) provides computing infrastructure.",

# =====================================================
# 🤖 AI & MACHINE LEARNING
# =====================================================

"artificial intelligence": "AI (Artificial Intelligence) enables machines to mimic human intelligence.",
"deep learning": "Deep Learning uses neural networks with multiple layers.",
"neural network": "Neural Network is a computing system inspired by biological brains.",
"chatgpt": "ChatGPT is an AI chatbot by OpenAI.",
"openai": "OpenAI is an AI research organization.",
"natural language processing": "NLP enables computers to understand human language.",
"computer vision": "Computer Vision enables computers to understand images and videos.",
"robotics": "Robotics combines AI, engineering, and computer science.",
"automation": "Automation uses technology to perform tasks without human intervention.",
"big data": "Big Data refers to large and complex datasets.",
"data analysis": "Data Analysis examines data to draw conclusions.",
"data visualization": "Data Visualization represents data in graphical formats.",
"blockchain": "Blockchain is a decentralized digital ledger technology.",
"cryptocurrency": "Cryptocurrency is a digital currency using cryptography.",
"bitcoin": "Bitcoin is the first and most valuable cryptocurrency.",
"ethereum": "Ethereum is a blockchain platform for smart contracts.",
"iot": "IoT (Internet of Things) connects everyday objects to the internet.",
"vr": "VR (Virtual Reality) creates simulated environments.",
"ar": "AR (Augmented Reality) overlays digital content on real world.",
"metaverse": "Metaverse is a virtual reality space for social interaction.",
"quantum computing": "Quantum Computing uses quantum mechanics for computation.",
"cybersecurity": "Cybersecurity protects systems from digital attacks.",
"hacking": "Hacking is unauthorized access to computer systems.",
"malware": "Malware is malicious software designed to harm computers.",
"phishing": "Phishing is a cyber attack to steal sensitive information.",
"encryption": "Encryption converts data into a secure format.",

# =====================================================
# 📱 MOBILE & SOFTWARE
# =====================================================

"android": "Android is a mobile operating system by Google.",
"ios": "iOS is Apple's mobile operating system for iPhones and iPads.",
"mobile app": "Mobile app is software designed for mobile devices.",
"ios development": "iOS development uses Swift and Xcode.",
"android development": "Android development uses Kotlin and Android Studio.",
"flutter": "Flutter is Google's UI toolkit for cross-platform apps.",
"react native": "React Native is Facebook's framework for mobile apps.",
"app store": "App Store is Apple's marketplace for iOS apps.",
"play store": "Google Play Store is for Android apps.",
"whatsapp": "WhatsApp is a messaging app owned by Meta.",
"facebook": "Facebook is a social media platform.",
"instagram": "Instagram is a photo and video sharing platform.",
"twitter": "Twitter is a microblogging platform.",
"youtube": "YouTube is a video sharing platform.",
"tiktok": "TikTok is a short video platform.",
"linkedin": "LinkedIn is a professional networking platform.",
"reddit": "Reddit is a social news and discussion platform.",
"zoom": "Zoom is a video conferencing platform.",
"teams": "Microsoft Teams is for collaboration and video calls.",
"slack": "Slack is a business communication platform.",

# =====================================================
# 🧮 MATHEMATICS & GENERAL FACTS
# =====================================================

"mathematics": "Mathematics is the study of numbers, quantities, and shapes.",
"algebra": "Algebra uses variables and equations to solve problems.",
"geometry": "Geometry studies shapes, sizes, and positions of objects.",
"calculus": "Calculus studies rates of change and accumulation.",
"statistics": "Statistics collects and analyzes numerical data.",
"pi": "Pi (π) is approximately 3.14159, the ratio of circumference to diameter.",
"prime number": "Prime number is divisible only by 1 and itself.",
"fibonacci": "Fibonacci sequence is a series where each number is the sum of previous two.",
"binary": "Binary is a number system using only 0 and 1.",
"hexadecimal": "Hexadecimal is a base-16 number system.",
"internet": "Internet is a global network of connected computers.",
"www": "World Wide Web is an information system on the internet.",
"browser": "Browser is software for accessing websites.",
"搜索引擎": "Search engine helps find information on the internet.",
"google": "Google is the most popular search engine.",
"yahoo": "Yahoo is a web services company.",
"bing": "Bing is Microsoft's search engine.",
"dns": "DNS (Domain Name System) translates domain names to IP addresses.",
"ip address": "IP Address is a unique number assigned to each device on a network.",
"wifi": "WiFi is wireless technology for internet connectivity.",
"bluetooth": "Bluetooth is short-range wireless communication.",
"usb": "USB (Universal Serial Bus) connects devices to computers.",
"hdmi": "HDMI (High-Definition Multimedia Interface) connects devices to displays.",

# =====================================================
# 📚 EDUCATION & LEARNING
# =====================================================

"online learning": "Online learning is education over the internet.",
"e-learning": "E-learning uses electronic media for education.",
"mooc": "MOOC (Massive Open Online Course) offers free online courses.",
"coursera": "Coursera offers online courses from universities.",
"udemy": "Udemy is an online learning platform.",
"edx": "EdX offers free courses from MIT, Harvard, and other universities.",
"khan academy": "Khan Academy provides free educational videos and exercises.",
"duolingo": "Duolingo is a language learning app.",
"skillshare": "Skillshare is an online learning community for creative skills.",
"pluralsight": "Pluralsight offers technology courses.",
"codecademy": "Codecademy offers interactive coding lessons.",
"freecodecamp": "FreeCodeCamp teaches coding for free.",
"stackoverflow": "Stack Overflow is a Q&A platform for programmers.",
"medium": "Medium is a platform for articles and ideas.",
"wikipedia": "Wikipedia is a free online encyclopedia.",
"google scholar": "Google Scholar searches academic papers and citations.",
"research paper": "Research paper is an academic document presenting original findings.",
"thesis": "Thesis is a long academic document for degree completion.",
"dissertation": "Dissertation is a research document for doctoral degree.",

# =====================================================
# 🏥 HEALTH & MEDICINE
# =====================================================

"health": "Health is a state of physical, mental, and social well-being.",
"medicine": "Medicine is the science of diagnosing and treating diseases.",
"doctor": "Doctor is a trained medical professional.",
"hospital": "Hospital provides medical treatment and care.",
"surgery": "Surgery is a medical procedure involving instruments.",
"vaccine": "Vaccine provides immunity against diseases.",
"antibiotic": "Antibiotic fights bacterial infections.",
"virus": "Virus is a microscopic infectious agent.",
"bacteria": "Bacteria are single-celled microorganisms.",
"disease": "Disease is a pathological condition affecting the body.",
"diabetes": "Diabetes is a metabolic disease with high blood sugar.",
"hypertension": "Hypertension is high blood pressure.",
"cancer": "Cancer is a disease with abnormal cell growth.",
"coronavirus": "Coronavirus caused COVID-19 pandemic.",
"covid": "COVID-19 is a respiratory disease caused by SARS-CoV-2.",
"mental health": "Mental health affects emotional and psychological well-being.",
"depression": "Depression is a mental health disorder with persistent sadness.",
"anxiety": "Anxiety is a feeling of worry and fear.",
"yoga": "Yoga combines physical postures and breathing exercises.",
"meditation": "Meditation is practice for mental clarity and relaxation.",
"exercise": "Exercise improves physical health and fitness.",
"nutrition": "Nutrition is the process of consuming and utilizing food.",
"protein": "Protein is essential for muscle building and repair.",
"vitamin": "Vitamin is essential for body functions.",
"immune system": "Immune system protects the body from diseases.",

# =====================================================
# 💰 ECONOMICS & BUSINESS
# =====================================================

"economics": "Economics studies how people make decisions about resources.",
"business": "Business is commercial activity for profit.",
"stock market": "Stock market is where shares of companies are traded.",
"stock": "Stock represents ownership in a company.",
"share": "Share is a unit of ownership in a company.",
"investment": "Investment is putting money for future returns.",
"bank": "Bank provides financial services like deposits and loans.",
"loan": "Loan is borrowed money to be repaid with interest.",
"interest rate": "Interest rate is the cost of borrowing money.",
"inflation": "Inflation is the rate at which prices rise.",
"gdpp": "GDP (Gross Domestic Product) measures a country's economic output.",
"trade": "Trade is exchange of goods and services.",
"export": "Export is sending goods to other countries.",
"import": "Import is receiving goods from other countries.",
"tax": "Tax is money collected by government from income and goods.",
"company": "Company is a business organization for profit.",
"startup": "Startup is a newly founded business venture.",
"entrepreneur": "Entrepreneur starts and manages a business.",
"marketing": "Marketing promotes products and services.",
"advertising": "Advertising publicizes products to attract customers.",
"brand": "Brand is the identity of a product or company.",
"customer": "Customer is a person who buys goods or services.",
"profit": "Profit is the financial gain from business.",
"loss": "Loss is when expenses exceed revenue.",
"salary": "Salary is fixed payment for work.",
"income": "Income is money received for work or investment.",

# =====================================================
# 🔧 GENERAL KNOWLEDGE
# =====================================================

"science": "Science is the systematic study of the natural world.",
"physics": "Physics studies matter, energy, and their interactions.",
"chemistry": "Chemistry studies substances and their transformations.",
"biology": "Biology studies living organisms.",
"geography": "Geography studies Earth's surface and human activities.",
"history": "History is the study of past events.",
"philosophy": "Philosophy studies fundamental questions about existence and knowledge.",
"psychology": "Psychology studies the human mind and behavior.",
"sociology": "Sociology studies society and human relationships.",
"astronomy": "Astronomy studies celestial objects and phenomena.",
"space": "Space is the vast universe beyond Earth's atmosphere.",
"moon": "Moon is Earth's natural satellite.",
"sun": "Sun is the star at the center of our solar system.",
"planet": "Planet is a celestial body orbiting a star.",
"star": "Star is a luminous celestial body.",
"galaxy": "Galaxy is a large system of stars and gravity.",
"universe": "Universe contains all matter, energy, and space.",
"earth": "Earth is the third planet from the Sun and our home.",
"mars": "Mars is the fourth planet from the Sun, known as the Red Planet.",
"jupiter": "Jupiter is the largest planet in our solar system.",
"saturn": "Saturn is known for its beautiful rings.",
"black hole": "Black hole is a region of extreme gravity.",
"time": "Time is the continuous progression of events.",
"gravity": "Gravity is the force attracting objects toward each other.",
"electricity": "Electricity is the flow of electrical power.",
"magnet": "Magnet attracts iron and produces magnetic fields.",
"sound": "Sound is a vibration that travels through air or water.",
"light": "Light is electromagnetic radiation visible to the eye.",
"heat": "Heat is a form of energy transfer.",
"water": "Water is essential for life, formula H2O.",
"air": "Air is the mixture of gases surrounding Earth.",
"fire": "Fire is the rapid oxidation of materials producing heat and light.",

# CLASS 1 - NEPALI
"class 1 nepali vowels": "Class 1 Nepali vowels (Swar Barna): अ, आ, इ, ई, उ, ऊ, ए, ऐ, ओ, औ, अं, अः — these 12 vowels are the foundation of the Devanagari alphabet.",
"class 1 nepali consonants": "Class 1 Nepali consonants (Vyanjan Barna) include क, ख, ग, घ, ङ (Ka group), च, छ, ज, झ, ञ (Cha group), ट, ठ, ड, ढ, ण (Ta group), त, थ, द, ध, न (Ta group), प, फ, ब, भ, म (Pa group), य, र, ल, व, श, ष, स, ह, क्ष, त्र, ज्ञ.",
"class 1 nepali barakhadi": "Barakhadi in Class 1 teaches how vowel signs combine with consonants. Example: क + आ = का, क + इ = कि, क + ई = की, क + उ = कु, क + ऊ = कू.",
"class 1 nepali words": "Class 1 Nepali word practice includes simple 2–3 letter words like: घर (house), जल (water), फल (fruit), मन (mind), बल (strength), कमल (lotus).",
"class 1 nepali sentences": "Class 1 Nepali simple sentences: यो घर हो। (This is a house.) त्यो फूल हो। (That is a flower.) म बालक हुँ। (I am a child.)",
"class 1 nepali numbers words": "Class 1 Nepali number words: एक (1), दुई (2), तीन (3), चार (4), पाँच (5), छ (6), सात (7), आठ (8), नौ (9), दस (10).",

# CLASS 1 - ENGLISH
"class 1 english alphabet": "Class 1 English alphabet: A-Apple, B-Ball, C-Cat, D-Dog, E-Egg, F-Fish, G-Goat, H-Hat, I-Ink, J-Jug, K-Kite, L-Lion, M-Mango, N-Nest, O-Orange, P-Pen, Q-Queen, R-Rose, S-Sun, T-Tree, U-Umbrella, V-Van, W-Watch, X-X-ray, Y-Yak, Z-Zebra.",
"class 1 english vowels consonants": "Class 1 English: Vowels are A, E, I, O, U. All other letters are consonants. Vowels can form syllables on their own.",
"class 1 english words": "Class 1 English simple words (CVC pattern): cat, bat, hat, mat / hen, pen, ten / big, pig, dig / hot, pot, dot / bug, mug, hug.",
"class 1 english sentences": "Class 1 English simple sentences: This is a cat. I am a boy. She is a girl. The sun is hot. I like to play.",
"class 1 english greetings": "Class 1 English greetings: Good morning. Good afternoon. Good evening. Good night. Hello. How are you? I am fine, thank you.",
"class 1 english colors": "Class 1 English colors: red, blue, green, yellow, orange, purple, black, white, pink, brown.",
"class 1 english numbers": "Class 1 English number words: one, two, three, four, five, six, seven, eight, nine, ten.",
"class 1 english body parts": "Class 1 English body parts: head, eyes, ears, nose, mouth, teeth, neck, shoulder, hand, finger, leg, foot.",
"class 1 english fruits vegetables": "Class 1 English fruits: apple, mango, banana, orange, grapes. Vegetables: potato, tomato, onion, carrot, cabbage.",

# CLASS 1 - MATHEMATICS
"class 1 math counting": "Class 1 Math counting: Students learn to count from 1 to 100. Forward counting: 1, 2, 3...100. Backward counting: 10, 9, 8...1.",
"class 1 math addition": "Class 1 Math addition: Adding numbers within 20. Examples: 2 + 3 = 5, 4 + 6 = 10, 7 + 8 = 15. Addition means putting together.",
"class 1 math subtraction": "Class 1 Math subtraction: Subtracting numbers within 20. Examples: 5 - 2 = 3, 10 - 4 = 6, 15 - 7 = 8. Subtraction means taking away.",
"class 1 math shapes": "Class 1 Math shapes: Circle (गोलो), Square (वर्ग), Triangle (त्रिभुज), Rectangle (आयत). Students identify these shapes in real objects.",
"class 1 math before after between": "Class 1 Math: Before, After, Between. Example: Before 5 is 4. After 5 is 6. Between 4 and 6 is 5.",
"class 1 math greater lesser": "Class 1 Math: Greater than (>) and Less than (<). Example: 7 > 4 (7 is greater than 4), 3 < 8 (3 is less than 8).",
"class 1 math number names": "Class 1 Math number names: 1-One, 2-Two, 3-Three, 4-Four, 5-Five, 6-Six, 7-Seven, 8-Eight, 9-Nine, 10-Ten, 11-Eleven, 12-Twelve, 20-Twenty, 100-Hundred.",

# CLASS 1 - ENVIRONMENTAL STUDIES (HAMRO SEROFERO)
"class 1 evs family": "Class 1 EVS - Family: A family has father (बुबा), mother (आमा), sister (दिदी/बहिनी), brother (दाइ/भाइ). Joint family and nuclear family. Family members love and care for each other.",
"class 1 evs school": "Class 1 EVS - School: School has classroom, teacher, blackboard, books, desk, bench. We go to school to learn. We respect our teachers.",
"class 1 evs animals": "Class 1 EVS - Animals: Domestic animals: cow, buffalo, goat, dog, cat, hen. Wild animals: lion, tiger, elephant, deer. Animals give us milk, eggs, and help in work.",
"class 1 evs plants": "Class 1 EVS - Plants: Plants have roots, stem, leaves, flowers, and fruits. Plants need water, sunlight, and air to grow. Trees give us oxygen, fruits, and shade.",
"class 1 evs body hygiene": "Class 1 EVS - Hygiene: We must wash hands before eating, brush teeth twice daily, take bath regularly, cut nails, and keep surroundings clean.",
"class 1 evs seasons": "Class 1 EVS - Seasons in Nepal: Summer (गर्मी), Rainy/Monsoon (वर्षा), Autumn (शरद), Winter (जाडो), Spring (बसन्त). Nepal has 5 main seasons.",

# ==================== CLASS 2 ====================

"class 2 nepali matra": "Class 2 Nepali Matra (vowel signs): आ-matra (ा), इ-matra (ि), ई-matra (ी), उ-matra (ु), ऊ-matra (ू), ए-matra (े), ओ-matra (ो). Example: क + ा = का, क + ि = कि, क + ी = की.",
"class 2 nepali half letters": "Class 2 Nepali half letters (Aadha Akshyar): Some consonants take a half form when combined. Example: क् + ष = क्ष, त् + र = त्र, ज् + ञ = ज्ञ.",
"class 2 nepali poem": "Class 2 Nepali poems (Kavita) include simple rhyming poems about nature, animals, and daily life. Students read, memorize, and recite short poems.",
"class 2 nepali grammar noun": "Class 2 Nepali introduces Sangya (Noun): Names of persons (राम), places (नेपाल), things (किताब). Learning to identify nouns in sentences.",
"class 2 english nouns": "Class 2 English - Noun: A noun is a naming word. Names of persons (Ram, Sita), places (Nepal, Kathmandu), things (book, pen). Singular: cat. Plural: cats (add s or es).",
"class 2 english singular plural": "Class 2 English - Singular and Plural: Add 's': cat-cats, dog-dogs. Add 'es': box-boxes, bus-buses, mango-mangoes. Irregular: child-children, man-men, mouse-mice.",
"class 2 english pronouns": "Class 2 English - Pronouns: I, you, he, she, it, we, they replace nouns. Example: Ram is a boy. He is a boy. Sita is a girl. She is a girl.",
"class 2 english is am are": "Class 2 English - Is, Am, Are: I am a student. He/She/It is happy. We/You/They are friends. These are linking verbs in present tense.",
"class 2 math place value": "Class 2 Math - Place Value: In the number 35, 3 is in the tens place (value = 30) and 5 is in the ones place (value = 5). Expanded form: 35 = 30 + 5.",
"class 2 math addition 2 digit": "Class 2 Math - 2-digit addition: 23 + 14 = 37. With carrying: 45 + 38 = 83 (5+8=13, write 3 carry 1; 4+3+1=8).",
"class 2 math subtraction 2 digit": "Class 2 Math - 2-digit subtraction: 57 - 23 = 34. With borrowing: 52 - 28 = 24 (borrow from tens place).",
"class 2 math multiplication tables": "Class 2 Math multiplication tables: Table of 2 (2,4,6,8,10,12,14,16,18,20) and Table of 5 (5,10,15,20,25,30,35,40,45,50).",
"class 2 math time": "Class 2 Math - Time: Clock reading (hour and half hour). AM (morning) and PM (afternoon/evening). 7 days in a week: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.",
"class 2 math money": "Class 2 Math - Money: Nepal uses Rupee and Paisa. 100 Paisa = 1 Rupee. Adding money amounts. Simple shopping problems.",
"class 2 evs community": "Class 2 EVS - Community: Our community has houses, roads, school, market, hospital, temple. Community helpers: doctor, teacher, police, farmer, shopkeeper.",
"class 2 evs food": "Class 2 EVS - Food: Food gives us energy. Cereals (rice, wheat, maize), Pulses (dal), Vegetables, Fruits, Milk and dairy products. We should eat balanced food.",
"class 2 evs water": "Class 2 EVS - Water: We get water from rivers, ponds, wells, taps. Uses: drinking, cooking, bathing, farming. We should not waste water. Always drink clean water.",
"class 2 evs transport": "Class 2 EVS - Transport: Land (bus, car, bicycle, truck), Water (boat, ship), Air (aeroplane, helicopter). Transport helps us travel to far places.",

# ==================== CLASS 3 ====================

"class 3 nepali gender": "Class 3 Nepali Gender (Linga): Purush Linga (Masculine): राजा, बाबु, केटा, घोडा. Stri Linga (Feminine): रानी, आमा, केटी, घोडी. Some change with suffix: राजा→रानी, शेर→शेर्नी.",
"class 3 nepali tense": "Class 3 Nepali Tense (Kaal): Bhoot Kaal (Past): म गएँ (I went). Bartaman Kaal (Present): म जान्छु (I go/I am going). Bhabishyat Kaal (Future): म जानेछु (I will go).",
"class 3 nepali letter writing": "Class 3 Nepali letter writing: Informal letter to a friend or relative. Format includes: date (मिति), salutation (प्रिय मित्र), body (मुख्य कुरा), closing (तिम्रो मित्र), and name.",
"class 3 nepali essay": "Class 3 Nepali essay (Nibandha): Short essays (5–8 lines) on topics like My Country Nepal, My School, My Favourite Animal, The Cow.",
"class 3 english adjectives": "Class 3 English - Adjectives: Adjective describes a noun. Examples: big house, red flower, sweet mango, clever boy, tall tree. Degrees: big-bigger-biggest, good-better-best, bad-worse-worst.",
"class 3 english verbs": "Class 3 English - Verbs: Action words. Run, jump, eat, sleep, write, read, play, sing. Present: He eats. Past: He ate. Future: He will eat.",
"class 3 english prepositions": "Class 3 English - Prepositions: in, on, under, over, behind, beside, between, in front of. The book is on the table. The cat is under the chair. She is standing between Ram and Hari.",
"class 3 math multiplication": "Class 3 Math - Multiplication: Tables 1–10. Multiplication of 3-digit by 1-digit: 234 × 3 = 702. Multiplication is repeated addition: 4 × 3 = 4+4+4 = 12.",
"class 3 math division": "Class 3 Math - Division: 20 ÷ 4 = 5. Long division of 2-digit by 1-digit: 48 ÷ 6 = 8. Remainder concept: 25 ÷ 4 = 6 remainder 1.",
"class 3 math fractions": "Class 3 Math - Fractions: Half (1/2), Quarter (1/4), Three-quarter (3/4), One-third (1/3). Numerator (top number) and Denominator (bottom number). 1/2 means 1 part out of 2 equal parts.",
"class 3 math calendar": "Class 3 Math - Calendar: 7 days in a week, approximately 4 weeks in a month, 12 months in a year. Nepali months: Baisakh, Jestha, Ashadh, Shrawan, Bhadra, Ashwin, Kartik, Mangsir, Poush, Magh, Falgun, Chaitra.",
"class 3 evs nepal": "Class 3 EVS - Our Country Nepal: Nepal is in South Asia. Capital: Kathmandu. National flag is triangular. National animal: Cow, National bird: Danphe, National flower: Rhododendron (Laliguras).",
"class 3 evs food crops": "Class 3 EVS - Food and Farming: Rice, maize, wheat, millet are main food crops of Nepal. Farmers grow food in fields. Irrigation is needed in dry seasons.",
"class 3 evs health": "Class 3 EVS - Good Health Habits: Eat balanced diet, drink clean water, exercise daily, sleep 8 hours, wash hands before meals, keep environment clean, visit doctor when sick.",

# ==================== CLASS 4 ====================

"class 4 nepali sandhi": "Class 4 Nepali - Sandhi (Word joining): When two words join, letters may change. Example: सूर्य + उदय = सूर्योदय, हिम + आलय = हिमालय. Swar Sandhi joins vowels.",
"class 4 nepali karak": "Class 4 Nepali - Karak (Case): Karta (Subject: -ले), Karma (Object: -लाई), Karan (Instrument: -ले/-बाट), Sampradaan (Receiver: -लाई), Apaadaan (Separation: -बाट), Adhikarana (Location: -मा).",
"class 4 nepali essay types": "Class 4 Nepali - Essay types: Descriptive (वर्णनात्मक), Narrative (कथात्मक). Topics: Cow (गाई), My Country (मेरो देश), A Festival (एउटा चाड).",
"class 4 english tenses": "Class 4 English - Tenses: Simple Present (He plays every day), Present Continuous (He is playing now), Simple Past (He played yesterday), Simple Future (He will play tomorrow). Use correct time signals.",
"class 4 english articles": "Class 4 English - Articles: 'A' before consonant sounds (a book, a cat). 'An' before vowel sounds (an apple, an egg, an hour). 'The' for specific/unique things (the sun, the President).",
"class 4 english conjunctions": "Class 4 English - Conjunctions: and (addition), but (contrast), or (choice), because (reason), so (result), although (concession), while (simultaneous). Join two sentences into one.",
"class 4 math large numbers": "Class 4 Math - Large Numbers: Ones, Tens, Hundreds, Thousands, Ten-Thousands, Lakhs. 1 lakh = 1,00,000. Expanded form: 45,678 = 40,000 + 5,000 + 600 + 70 + 8.",
"class 4 math lcm hcf": "Class 4 Math - LCM and HCF: HCF is the largest number that divides given numbers (HCF of 12 and 18 = 6). LCM is the smallest number divisible by given numbers (LCM of 4 and 6 = 12).",
"class 4 math area perimeter": "Class 4 Math - Area and Perimeter: Perimeter = sum of all sides. Area of rectangle = length × breadth. Area of square = side × side. Example: Rectangle 5cm × 3cm: Perimeter=16cm, Area=15 sq cm.",
"class 4 math profit loss": "Class 4 Math - Profit and Loss: Cost Price (CP) is buying price. Selling Price (SP) is selling price. Profit = SP - CP (when SP > CP). Loss = CP - SP (when CP > SP).",
"class 4 science living nonliving": "Class 4 Science - Living and Non-living: Living things grow, breathe, reproduce, need food and water. Non-living things do not have life. Plants and animals are living. Stones, water, air are non-living.",
"class 4 science food chain": "Class 4 Science - Food Chain: Plants (Producers) → Herbivores → Carnivores → Top Carnivores. Example: Grass → Grasshopper → Frog → Snake → Eagle. Sun is the energy source.",
"class 4 science human body organs": "Class 4 Science - Human Body Organs: Brain (controls body), Heart (pumps blood), Lungs (breathing), Stomach (digests food), Liver (filters blood), Kidneys (filter waste), Bones form the skeleton.",
"class 4 science simple machines": "Class 4 Science - Simple Machines: Lever (seesaw, scissors), Wheel and Axle (bicycle), Pulley (well bucket), Inclined Plane (ramp), Screw (jar lid), Wedge (axe). Machines make work easier.",
"class 4 science photosynthesis": "Class 4 Science - Photosynthesis: Plants make food using sunlight, water, and carbon dioxide. Chlorophyll (green pigment) in leaves absorbs sunlight. Oxygen is released as a byproduct.",
"class 4 social nepal regions": "Class 4 Social Studies - Nepal's Geographic Regions: Himalayan (Mountain) region in the north (includes Everest), Hilly region in the middle (valleys and rivers), Terai (Plain) region in the south (flat, fertile, most populated).",

# ==================== CLASS 5 ====================

"class 5 nepali alankar": "Class 5 Nepali - Alankar (Figures of Speech): Upama (Simile: comparing using जस्तो/सरि — 'उसको अनुहार चन्द्रमा जस्तो छ'), Rupak (Metaphor: direct comparison), Anupras (Alliteration: repeated consonant sounds).",
"class 5 nepali samasa": "Class 5 Nepali - Samasa (Compound Words): Joining of two or more words to create a new meaning. Tatpurusha: घरमालिक, Dvanda: राम-सिता, Karmadharaya: नीलाकाश, Dwigu: त्रिकोण.",
"class 5 english passive voice": "Class 5 English - Active and Passive Voice: Active: The cat eats the rat. Passive: The rat is eaten by the cat. Formula: Object + is/are/was/were + past participle + by + subject.",
"class 5 english essay writing": "Class 5 English - Essay Writing: Three parts: Introduction (introduce topic), Body (main points with examples), Conclusion (summary and opinion). Topics: My School, Importance of Trees, My Country Nepal.",
"class 5 math decimals": "Class 5 Math - Decimals: 0.1 = 1/10, 0.01 = 1/100, 0.001 = 1/1000. Adding: 3.5 + 2.7 = 6.2. Multiplying: 2.5 × 4 = 10. Dividing: 7.5 ÷ 5 = 1.5. Comparing decimals.",
"class 5 math percentage": "Class 5 Math - Percentage: Percent means per 100. 25% = 25/100 = 1/4. Finding percentage: 20% of 150 = 30. Converting fraction to percent: 3/4 = 75%. Percentage increase and decrease.",
"class 5 math unitary method": "Class 5 Math - Unitary Method: If 5 pens cost Rs.25, cost of 1 pen = 25÷5 = Rs.5. Cost of 8 pens = 5×8 = Rs.40. Find value of one unit, then multiply for required units.",
"class 5 science matter states": "Class 5 Science - States of Matter: Solid (fixed shape and volume: ice), Liquid (fixed volume, takes shape of container: water), Gas (no fixed shape or volume: steam). Changes: melting, freezing, evaporation, condensation.",
"class 5 science force motion": "Class 5 Science - Force and Motion: Force is a push or pull. Types: Gravitational (pulls downward), Magnetic, Frictional (opposes motion), Muscular. Speed = Distance ÷ Time.",
"class 5 science human systems": "Class 5 Science - Human Body Systems: Digestive (mouth→stomach→intestines), Respiratory (nose→trachea→lungs), Circulatory (heart pumps blood through arteries and veins to all body parts).",
"class 5 social prithvi narayan shah": "Class 5 Social Studies - Prithvi Narayan Shah: Born in Gorkha in 1723. Began unification of Nepal in 1743 and completed it in 1768 by capturing Kathmandu. Called Father of Modern Nepal.",
"class 5 social nepal government": "Class 5 Social Studies - Nepal's Government: Nepal is a Federal Democratic Republic with three levels: Federal (central), Provincial (7 provinces), and Local (753 units). Parliament makes laws.",

# ==================== CLASS 6 ====================

"class 6 nepali samas types": "Class 6 Nepali - Types of Samasa: Tatpurush (राजमहल=राजाको महल), Karmadharaya (महापुरुष=महान पुरुष), Dwigu (त्रिकोण=तीन कोण), Dvandva (दाल-भात), Bahuvrihi (दशमुख=Ravana who has 10 heads).",
"class 6 nepali sandhi rules": "Class 6 Nepali - Sandhi rules: अ+अ=आ (हिम+आलय=हिमालय), अ+इ=ए (नर+इंद्र=नरेंद्र), आ+आ=आ (विद्या+आलय=विद्यालय). Byanjan Sandhi: consonant changes when joining.",
"class 6 nepali vaakya bhed": "Class 6 Nepali - Types of Sentences: Assertive (सरल: म पढ्छु), Negative (नकारात्मक: म पढ्दिनँ), Interrogative (प्रश्न: के तिमी पढ्छौ?), Imperative (आदेश: पढ), Exclamatory (विस्मय: वाह!).",
"class 6 english parts of speech": "Class 6 English - 8 Parts of Speech: Noun (naming word), Pronoun (replaces noun), Adjective (describes noun), Verb (action/state), Adverb (modifies verb/adjective), Preposition (shows relation), Conjunction (joins), Interjection (emotion).",
"class 6 english tenses all": "Class 6 English - All 12 Tenses overview: 4 Present (Simple, Continuous, Perfect, Perfect Continuous), 4 Past, 4 Future. Each has affirmative, negative, and interrogative forms.",
"class 6 english clauses": "Class 6 English - Clauses: Main clause (can stand alone: She sings), Subordinate clause (depends: because she is happy). Types: Noun clause (what he said), Adjective clause (who came), Adverb clause (when he arrived).",
"class 6 math integers": "Class 6 Math - Integers: Positive (...1,2,3), Zero (0), Negative (...-3,-2,-1). Number line. Adding: 5+(-3)=2, (-4)+(-2)=-6. Subtracting: 3-(-2)=5. Multiplying: (-3)×(-4)=+12, (-3)×(4)=-12.",
"class 6 math rational numbers": "Class 6 Math - Rational Numbers: Numbers in form p/q where q≠0. All integers are rational (5=5/1). Operations: addition (find common denominator), subtraction, multiplication (multiply numerators and denominators), division.",
"class 6 math algebra intro": "Class 6 Math - Algebra: Variables (x, y) represent unknowns. Algebraic expressions: 2x+3, 5y-2. Like terms: 3x+4x=7x. Unlike terms cannot be added: 3x+4y. Substitution: if x=2, then 2x+3=7.",
"class 6 math ratio proportion": "Class 6 Math - Ratio and Proportion: Ratio compares quantities: 3:4. Proportion: two equal ratios: 3:4 = 6:8. Direct proportion (more goods, more cost). Inverse proportion (more workers, less time). Unitary method.",
"class 6 science cell": "Class 6 Science - Cell: Cell is the basic unit of life (discovered by Robert Hooke 1665). Cell membrane, Cytoplasm, Nucleus (control center). Plant cell has extra: cell wall and chloroplast. Animal cell has no cell wall.",
"class 6 science classification": "Class 6 Science - Classification of Organisms: Five kingdoms: Monera (bacteria), Protista (amoeba), Fungi (mushroom), Plantae, Animalia. Vertebrates (backbone): Fish, Amphibians, Reptiles, Birds, Mammals. Invertebrates: insects, worms, crabs.",
"class 6 science physical chemical change": "Class 6 Science - Changes: Physical change: substance remains same, only form changes (cutting paper, melting ice, dissolving sugar). Chemical change: new substance forms (burning wood, rusting iron, cooking food, curdling milk).",
"class 6 social nepal geography": "Class 6 Social Studies - Nepal's Geography: Area: 147,181 sq km. Coordinates: 26°22'N to 30°27'N, 80°4'E to 88°12'E. Highest point: Everest (8848.86m). Three main river systems: Koshi, Gandaki, Karnali.",
"class 6 social nepal history lichhavi": "Class 6 Social Studies - Lichhavi Period (400–750 AD): Fine art and architecture. Changu Narayan temple built. Trade with Tibet and India. Famous kings: Manadev, Amsuvarman. Called golden age of Nepali art.",

# ==================== CLASS 7 ====================

"class 7 nepali vaakya rachana": "Class 7 Nepali - Sentence Construction: Subject + Object + Verb (SOV) order in Nepali (unlike English SVO). Pratyaksha Ukti (Direct Speech): राम भन्छ, 'म जान्छु।' Paroksha Ukti (Indirect): राम भन्छ कि ऊ जान्छ।",
"class 7 nepali application": "Class 7 Nepali - Application Writing (Aavedan Patra): Format: श्रीमान् प्रधानाध्यापक ज्यू (To the Principal), Subject: (विषय), Salutation: महोदय, Body: विनम्र निवेदन गर्दछु..., Date, Name.",
"class 7 english conditional": "Class 7 English - Conditional Sentences: Zero (fact): If water reaches 100°C, it boils. First (possible): If it rains, I will stay home. Second (unreal present): If I had money, I would buy it. Third (unreal past): If I had studied, I would have passed.",
"class 7 english modal verbs": "Class 7 English - Modal Verbs: Can (ability: I can swim), Could (past ability/polite: Could you help?), May (permission: May I go?), Might (weaker possibility: It might rain), Must (obligation: You must come), Should (advice: You should study), Will/Shall (future).",
"class 7 english relative clauses": "Class 7 English - Relative Clauses: who (people: the man who called), which (things: the book which you read), that (both), whose (possession: the girl whose bag is red), where (place: the school where I study).",
"class 7 math linear equations": "Class 7 Math - Linear Equations: One variable. Solve: 2x + 5 = 13 → 2x = 8 → x = 4. Check: 2(4)+5=13 ✓. Word problem: A number added to 7 equals 15 → x+7=15 → x=8.",
"class 7 math pythagoras": "Class 7 Math - Pythagoras Theorem: In right triangle: hypotenuse² = base² + perpendicular². c² = a² + b². Example: a=3, b=4, c=5. Pythagorean triplets: (3,4,5), (5,12,13), (8,15,17).",
"class 7 math profit loss discount": "Class 7 Math - Profit, Loss and Discount: Profit% = (Profit÷CP)×100. Loss% = (Loss÷CP)×100. Discount = Marked Price - Selling Price. VAT (Value Added Tax) = 13% in Nepal added to selling price.",
"class 7 math geometry circle": "Class 7 Math - Circle: Radius (r), Diameter (d=2r), Circumference (C=2πr), Area=πr². π≈3.14159. Arc, chord, tangent. Central angle = double inscribed angle.",
"class 7 science nutrition humans": "Class 7 Science - Human Nutrition: Carbohydrates (energy: rice, bread), Proteins (growth/repair: dal, meat, egg), Fats (energy store: butter, oil), Vitamins (A,B,C,D,E,K - protection), Minerals (calcium, iron), Water, Dietary Fibre.",
"class 7 science respiration": "Class 7 Science - Respiration: Aerobic: Glucose + Oxygen → CO2 + Water + Energy (38 ATP). Anaerobic (no oxygen): Glucose → Lactic acid + Energy (muscles during exercise) OR Glucose → Ethanol + CO2 + Energy (yeast fermentation).",
"class 7 science electricity": "Class 7 Science - Electricity: Current (I) in Amperes, Voltage (V) in Volts, Resistance (R) in Ohms. Ohm's Law: V = IR. Series circuit: same current flows, voltages add. Parallel circuit: same voltage, currents add. Power P=VI.",
"class 7 science light": "Class 7 Science - Light: Reflection: angle of incidence = angle of reflection. Refraction: light bends when changing medium (straw in water looks bent). Total internal reflection. Dispersion by prism: VIBGYOR.",
"class 7 social medieval nepal": "Class 7 Social Studies - Medieval Nepal (Malla Period 12th-18th c): Built Pashupatinath, Swayambhunath, Boudhanath. Valley divided into 3 kingdoms: Kathmandu, Patan, Bhaktapur. Famous for art, architecture, and trade.",
"class 7 social human rights": "Class 7 Social Studies - Human Rights: Right to life, equality, free speech, education, health. Universal Declaration of Human Rights (UDHR) adopted by UN on December 10, 1948. Human Rights Day = December 10.",
"class 7 social natural resources": "Class 7 Social Studies - Natural Resources: Renewable (solar, wind, water, forests — replenish naturally) and Non-renewable (petroleum, coal, minerals — cannot replenish quickly). Nepal has vast hydropower (83,000 MW potential).",

# ==================== CLASS 8 ====================

"class 8 nepali nibandha types": "Class 8 Nepali - Types of Essays: Varnanaatmak (Descriptive: describes a person/place/thing), Vicharaatmak (Analytical: discusses ideas/issues), Aatmakathanaatmak (Autobiographical: first person experience), Sahityik (Literary: about literature), Samajik (Social issues).",
"class 8 nepali summary writing": "Class 8 Nepali - Saar Lekhan (Summary Writing): Read passage, identify main points, write in own words in about 1/3 original length, no personal opinions, maintain original meaning. Begin: 'यस अनुच्छेदमा ...'",
"class 8 english report writing": "Class 8 English - Report Writing: Headline, Byline (reporter name), Dateline (place and date), Lead paragraph (who, what, when, where, why, how), Body (details), Closing quote. Use past tense and third person.",
"class 8 english notice writing": "Class 8 English - Notice Writing: Box format. Name of institution, NOTICE (heading), Date, Title, Body (what/when/where/who), Issuing authority. Keep brief and formal.",
"class 8 english literary devices": "Class 8 English - Literary Devices: Simile (like/as: brave as a lion), Metaphor (direct comparison: life is a journey), Personification (non-human acts human: the wind whispered), Hyperbole (exaggeration), Irony (saying opposite), Alliteration, Onomatopoeia.",
"class 8 math quadratic equations": "Class 8 Math - Quadratic Equations: ax²+bx+c=0. Factorization: x²+5x+6=0 → (x+2)(x+3)=0 → x=-2 or x=-3. Quadratic formula: x = [-b ± √(b²-4ac)] / 2a. Discriminant D=b²-4ac: D>0 (two roots), D=0 (equal roots), D<0 (no real roots).",
"class 8 math mensuration": "Class 8 Math - Mensuration 3D: Volume of cuboid = l×b×h. Volume of cube = a³. Volume of cylinder = πr²h. Curved surface area of cylinder = 2πrh. Total surface area of cylinder = 2πr(r+h). Volume of cone = (1/3)πr²h.",
"class 8 math trigonometry intro": "Class 8 Math - Trigonometry Introduction: In right triangle: sin θ = opposite/hypotenuse (O/H), cos θ = adjacent/hypotenuse (A/H), tan θ = opposite/adjacent (O/A). Memory: SOHCAHTOA. sin30°=1/2, cos60°=1/2, tan45°=1.",
"class 8 math statistics advanced": "Class 8 Math - Statistics: Mean of grouped data using midpoints. Cumulative frequency. Quartiles (Q1=lower quartile, Q2=median, Q3=upper quartile). Inter-quartile range = Q3-Q1. Standard deviation (basic concept).",
"class 8 science reproduction": "Class 8 Science - Reproduction: Asexual (one parent): Binary fission (amoeba), Budding (yeast, hydra), Fragmentation (Spirogyra), Spore formation (mucor). Sexual reproduction produces genetically diverse offspring. Fertilization = fusion of gametes.",
"class 8 science genetics basic": "Class 8 Science - Basic Genetics: DNA is the genetic material. Chromosomes carry genes. Mendel's Laws: Dominance (D masks d), Segregation (Dd separates in gametes). Punnett square: Tt×Tt gives 1TT:2Tt:1tt. Phenotype ratio 3:1.",
"class 8 science chemical reactions": "Class 8 Science - Chemical Reactions: Types: Combination (A+B→AB: C+O2→CO2), Decomposition (AB→A+B: 2H2O→2H2+O2), Displacement (A+BC→AC+B: Zn+H2SO4→ZnSO4+H2), Double Displacement, Combustion. Exothermic (releases heat) and Endothermic (absorbs heat).",
"class 8 science acids bases salts": "Class 8 Science - Acids, Bases and Salts: Acid: sour, pH<7, red litmus (HCl, H2SO4, vinegar/acetic acid, lemon/citric acid). Base: bitter, pH>7, blue litmus (NaOH, Ca(OH)2, baking soda). Neutralization: Acid + Base → Salt + Water. pH scale 0-14.",
"class 8 science magnetism electromagnetism": "Class 8 Science - Magnetism: Magnetic field lines go N to S outside magnet. Earth is a giant magnet. Electromagnet: current in coil creates magnetic field. Uses: electric bell, motor, generator, MRI scanner.",
"class 8 social modern nepal": "Class 8 Social Studies - Modern Nepal: 1951 end of Rana regime, BP Koirala's democratic government. 1960 King Mahendra's coup, Panchayat system. 1990 Jana Andolan I restores multiparty democracy. 1996-2006 Maoist insurgency. 2006 Jana Andolan II ends monarchy. 2008 Republic declared.",
"class 8 social globe map": "Class 8 Social Studies - Globe and Map: Earth rotates on axis in 24 hours (day/night). Revolves around Sun in 365.25 days (seasons). Latitudes (horizontal lines). Longitudes (vertical lines, meridians). Prime Meridian = 0°. Nepal is approx. 84°E longitude.",

# ==================== CLASS 9 ====================

"class 9 nepali grammar detail": "Class 9 Nepali Grammar: Sandhi (16 rules for vowel and consonant joining), Samas (6 types), 8 Karak cases (Karta-ले, Karma-लाई, Karan-ले/बाट, Sampradaan-लाई, Apaadaan-बाट, Sambandha-को/का/की, Adhikarana-मा, Sambodhan-हे/ओ), 20+ Alankar figures of speech.",
"class 9 nepali nibandha": "Class 9 Nepali Essay (Nibandha): Structure: Prathamik Parichaya (Intro 1 para), Vikas (Development 2-3 paras with sub-points), Nishkarsha (Conclusion). Analytical essays on social, cultural, environmental topics. 250–300 words minimum.",
"class 9 nepali patra lekhan": "Class 9 Nepali Letter Writing types: Sarkari Patra (Official/Formal — to government offices), Ardhsarkari (Semi-formal — to newspaper editor), Vaiyaktik (Personal — to friends/family), Aavedan Patra (Application — job/leave/scholarship).",
"class 9 english grammar full": "Class 9 English Grammar: Tenses (all 12 with passive forms), Modal verbs, All conditionals (0,1,2,3), Reported speech (statements, questions, commands, exclamations), Gerunds and infinitives, Participles, Relative clauses.",
"class 9 english narration": "Class 9 English Narration: Direct→Indirect changes: Reporting verb (says→said), Pronouns (I→he, we→they), Tenses backshift (is→was, has→had, will→would), Time expressions (now→then, today→that day, tomorrow→the next day, yesterday→the previous day).",
"class 9 math sets": "Class 9 Math - Sets: Set is a well-defined collection. Types: Empty set ({}), Finite, Infinite, Universal (U), Subset (⊆). Operations: Union (A∪B = in A or B), Intersection (A∩B = in both), Difference (A-B = in A not B), Complement (A' = not in A). Formula: n(A∪B)=n(A)+n(B)-n(A∩B).",
"class 9 math real numbers": "Class 9 Math - Real Numbers: Natural (1,2,3...) ⊂ Whole (0,1,2...) ⊂ Integers (...-2,-1,0,1,2...) ⊂ Rational (p/q) ⊂ Real. Irrational numbers: √2, √3, π (cannot be expressed as p/q). Together form Real numbers.",
"class 9 math algebraic expressions": "Class 9 Math - Algebraic Identities: (a+b)²=a²+2ab+b², (a-b)²=a²-2ab+b², (a+b)(a-b)=a²-b², (a+b)³=a³+3a²b+3ab²+b³. Factorization methods: common factor, grouping, difference of squares, perfect square trinomial.",
"class 9 math linear equations two variables": "Class 9 Math - Simultaneous Equations: Methods: Substitution (express one variable from one equation, substitute in other), Elimination (multiply equations to cancel one variable), Cross-multiplication, Graphical (intersection of two lines).",
"class 9 math trigonometry": "Class 9 Math - Trigonometric Ratios: sin θ = P/H, cos θ = B/H, tan θ = P/B, cosec θ = H/P, sec θ = H/B, cot θ = B/P. Standard values at 0°, 30°, 45°, 60°, 90°. Identities: sin²θ+cos²θ=1, 1+tan²θ=sec²θ, 1+cot²θ=cosec²θ.",
"class 9 math geometry euclid": "Class 9 Math - Geometry: Congruence criteria: SSS (three sides), SAS (two sides, included angle), ASA (two angles, included side), AAS, RHS (right angle, hypotenuse, side). Mid-point theorem: line joining midpoints of two sides is parallel and half the third side.",
"class 9 science cell biology": "Class 9 Science - Cell Biology: Prokaryotic (no membrane-bound nucleus: bacteria, blue-green algae) vs Eukaryotic (membrane-bound nucleus: plants, animals, fungi). Cell organelles: Mitochondria (powerhouse/ATP), Ribosome (protein synthesis), Golgi body (packaging), Vacuole (storage), Chloroplast (photosynthesis).",
"class 9 science plant physiology": "Class 9 Science - Plant Physiology: Photosynthesis equation: 6CO2+6H2O+light energy → C6H12O6+6O2. Factors: light, CO2, water, temperature, chlorophyll. Transpiration = water loss from stomata. Osmosis = water movement through semi-permeable membrane (high concentration to low).",
"class 9 science human biology": "Class 9 Science - Human Body Systems: Digestive (saliva, pepsin, bile, pancreatic juice break down food), Respiratory (alveoli for gaseous exchange: O2 in, CO2 out), Circulatory (4-chambered heart, double circulation), Excretory (kidneys filter 180L/day, produce 1-2L urine), Nervous (brain, spinal cord, 31 pairs spinal nerves).",
"class 9 science atoms molecules": "Class 9 Science - Atoms and Molecules: Atom = smallest unit of element (cannot be divided by chemical means). Molecule = 2+ atoms. Atomic mass unit (amu). Avogadro's number = 6.022×10²³. Mole = 6.022×10²³ particles = gram-atomic mass. Molecular formula: H2O, CO2, H2SO4.",
"class 9 science force energy": "Class 9 Science - Force and Energy: Newton's 1st Law (Inertia), 2nd Law (F=ma), 3rd Law (action-reaction). Work W=Fs cosθ (Joules). Power P=W/t (Watts). Kinetic Energy KE=½mv². Potential Energy PE=mgh. Conservation: Total energy remains constant.",
"class 9 social nepal geography full": "Class 9 Social Studies - Nepal's Detailed Geography: 5 physiographic zones: Terai, Siwalik (Churia), Middle Hills, High Himalayas, Trans-Himalaya. River systems: Koshi (7 tributaries), Gandaki (Kali Gandaki, Marsyangdi), Karnali (longest). 12 national parks, 1 wildlife reserve, 6 conservation areas.",
"class 9 social nepal history": "Class 9 Social Studies - Nepal's History: Kirat rule (800BC-400AD), Lichhavi (400-750AD), Malla (10th-18th c), Prithvi Narayan Shah unification (1768), Rana rule (1846-1951), Democracy (1951), Panchayat (1960-1990), Jana Andolan 1990, Maoist war (1996-2006), Republic (2008).",

# ==================== CLASS 10 ====================

"class 10 nepali full grammar": "Class 10 Nepali Full Grammar: Complete Sandhi (Swar, Byanjan, Visarga types), All Samas (Tatpurush, Karmadharaya, Dwigu, Dvandva, Bahuvrihi, Avyayibhav), All 8 Karak cases, 20+ Alankar, Pratyaksha-Paroksha Ukti, Kriya bhed (verb types), Visheshana bhed (adjective types).",
"class 10 nepali debate writing": "Class 10 Nepali Debate (Bahas Lekhan): State topic, Argue in favor (पक्षमा): give 3-4 strong arguments with examples, Argue against (विपक्षमा): counterarguments, Conclusion: state own side. Formal language, logical flow.",
"class 10 english grammar see": "Class 10 English Grammar for SEE: All 12 tenses with passive voice, All 3 conditional types, Direct-indirect speech all forms (statement, question, request, command, exclamation), Modals, Gerunds and infinitives, Phrasal verbs, Sentence transformation.",
"class 10 english writing see": "Class 10 English Writing for SEE: Argumentative Essay (200-300 words, intro+body+conclusion), Formal Letter (job/official), Notice (box format), Newspaper Report (headline+lead+body), Email (formal), Speech writing, Dialogue writing.",
"class 10 math quadratic equations see": "Class 10 Math - Quadratic Equations: ax²+bx+c=0. Three methods: (1) Factorization, (2) Completing the square, (3) Formula: x=(-b±√D)/2a where D=b²-4ac. Word problems: age problems, area problems, number problems.",
"class 10 math sequence series": "Class 10 Math - Sequences: AP: nth term = a+(n-1)d. Sum of n terms Sn = n/2[2a+(n-1)d] = n/2[first+last]. GP: nth term = ar^(n-1). Sum Sn = a(rⁿ-1)/(r-1) for r≠1. Geometric mean = √(ab). Arithmetic mean = (a+b)/2.",
"class 10 math matrices": "Class 10 Math - Matrices: Order m×n (rows×columns). Transpose: swap rows and columns. Determinant of 2×2: |A|=ad-bc. Inverse: A⁻¹=(1/|A|)×adj(A). Solving simultaneous equations: AX=B → X=A⁻¹B.",
"class 10 math coordinate geometry": "Class 10 Math - Coordinate Geometry: Distance = √[(x₂-x₁)²+(y₂-y₁)²]. Midpoint = ((x₁+x₂)/2, (y₁+y₂)/2). Section formula (internal): x=(m₁x₂+m₂x₁)/(m₁+m₂). Slope m=(y₂-y₁)/(x₂-x₁). Equation of line: y=mx+c.",
"class 10 math trigonometry see": "Class 10 Math - Advanced Trigonometry: Compound angles: sin(A+B)=sinAcosB+cosAsinB, cos(A+B)=cosAcosB-sinAsinB, tan(A+B)=(tanA+tanB)/(1-tanAtanB). Heights and distances: angle of elevation (looking up), angle of depression (looking down). Sine rule and cosine rule.",
"class 10 math probability": "Class 10 Math - Probability: P(E)=n(E)/n(S). P(A∪B)=P(A)+P(B)-P(A∩B). Mutually exclusive: P(A∩B)=0. Independent events: P(A∩B)=P(A)×P(B). Conditional probability: P(A|B)=P(A∩B)/P(B). Tree diagrams.",
"class 10 science genetics see": "Class 10 Science - Genetics: Mendel's laws. Monohybrid cross Tt×Tt: TT(25%):Tt(50%):tt(25%) genotype; Tall:short = 3:1 phenotype. Dihybrid cross TtRr×TtRr: 9:3:3:1 ratio. Incomplete dominance: red(RR)×white(rr)=pink(Rr). Blood groups: A(I^AI^A/I^Ai), B(I^BI^B/I^Bi), AB(I^AI^B), O(ii).",
"class 10 science nervous system": "Class 10 Science - Human Nervous System: CNS (brain + spinal cord). PNS (12 cranial nerves, 31 spinal nerves). Neuron parts: dendrites (receive), cell body (process), axon (transmit), myelin sheath (insulation), synapse (junction). Reflex arc: stimulus→receptor→sensory nerve→spinal cord→motor nerve→effector→response.",
"class 10 science electricity see": "Class 10 Science - Electricity: Ohm's Law V=IR. Series: same I, Rtotal=R1+R2, V divides. Parallel: same V, 1/Rtotal=1/R1+1/R2, I divides. Power P=VI=I²R=V²/R. Energy=Pt. Joule's law: H=I²Rt. Household circuit: live (brown), neutral (blue), earth (green/yellow).",
"class 10 science optics see": "Class 10 Science - Optics: Mirror formula: 1/v+1/u=1/f. Concave mirror: real inverted images (uses: torch, solar cooker, doctor's mirror). Convex mirror: virtual erect images (uses: rear-view mirror). Lens formula: 1/v-1/u=1/f. Power of lens P=1/f(meters) in Dioptre. Eye defects: Myopia (concave lens), Hypermetropia (convex lens), Astigmatism (cylindrical lens).",
"class 10 social nepal constitution": "Class 10 Social Studies - Nepal Constitution 2072 (2015): Nepal declared Federal Democratic Republic. 35 parts, 308 articles. Fundamental rights: equality, freedom, education, health, employment, environment, justice. Three tiers: Federal, Provincial (7), Local (753). Secularism, Inclusiveness.",
"class 10 social sustainable development": "Class 10 Social Studies - SDGs: 17 Sustainable Development Goals by UN (2015-2030): No poverty, Zero hunger, Good health, Quality education, Gender equality, Clean water, Clean energy, Decent work, Industry, Reduced inequalities, Sustainable cities, Responsible consumption, Climate action, Life below water, Life on land, Peace and justice, Partnerships.",

# ==================== CLASS 11 ====================

"class 11 physics vectors": "Class 11 Physics - Vectors: Scalar (mass, speed, temperature — magnitude only) vs Vector (displacement, velocity, force — magnitude and direction). Vector addition: Triangle law, Parallelogram law. Resultant R=√(A²+B²+2AB cosθ). Dot product A·B=AB cosθ (scalar). Cross product |A×B|=AB sinθ (vector).",
"class 11 physics kinematics": "Class 11 Physics - Kinematics: Equations of motion: v=u+at, s=ut+½at², v²=u²+2as. Projectile: horizontal velocity ux=u cosθ (constant), vertical velocity uy=u sinθ-gt. Range R=u²sin2θ/g, Max height H=u²sin²θ/2g, Time of flight T=2u sinθ/g.",
"class 11 physics laws of motion": "Class 11 Physics - Newton's Laws: 1st (Inertia): body continues in state of rest/uniform motion unless external force acts. 2nd: F=ma (rate of change of momentum). 3rd: Every action has equal and opposite reaction. Momentum p=mv. Impulse=Ft=Δp. Friction: f=μN.",
"class 11 physics work energy power": "Class 11 Physics - Work, Energy, Power: Work W=Fs cosθ (Joules). KE=½mv². PE=mgh. Conservation: KE+PE=constant. Power P=W/t=Fv (Watts). Elastic collision: both KE and momentum conserved. Inelastic: only momentum conserved. e=relative velocity after/before collision.",
"class 11 physics thermodynamics": "Class 11 Physics - Thermodynamics: Specific heat c=Q/mΔT. Linear expansion: ΔL=αLΔT. Volumetric: ΔV=γVΔT. Gas laws: Boyle's PV=constant (T fixed), Charles's V/T=constant (P fixed), Gay-Lussac's P/T=constant (V fixed). Ideal gas: PV=nRT. 1st law: ΔU=Q-W (heat added minus work done).",
"class 11 physics waves": "Class 11 Physics - Waves: Wave equation: v=fλ. Transverse (rope, EM waves) and Longitudinal (sound, slinky). Speed of sound in air=340m/s (20°C). Resonance: standing waves. Doppler effect: f'=f(v±vo)/(v∓vs) — frequency changes with motion. Beats: fb=|f1-f2|.",
"class 11 physics optics": "Class 11 Physics - Wave Optics: Interference: Young's Double Slit fringe width β=λD/d (bright and dark fringes). Diffraction: bending of waves around obstacles. Polarization: transverse waves only. Brewster's law: tan ip=n (angle at which reflected light is completely polarized).",
"class 11 chemistry atomic structure": "Class 11 Chemistry - Atomic Structure: Rutherford model (nuclear model, α-particle scattering). Bohr model: electrons in fixed orbits, En=-13.6/n² eV, rn=0.529n² Å. Quantum numbers: n (shell), l (subshell), m (orbital), s (spin). Electron config: 1s²2s²2p⁶3s²... Aufbau, Hund's, Pauli's rules.",
"class 11 chemistry periodic table": "Class 11 Chemistry - Periodic Table: 18 groups, 7 periods. s-block (groups 1-2), p-block (groups 13-18), d-block (transition metals, groups 3-12), f-block (lanthanides and actinides). Periodic trends: atomic radius increases down a group, decreases across a period. Ionization energy and electronegativity: opposite trends.",
"class 11 chemistry chemical bonding": "Class 11 Chemistry - Chemical Bonding: Ionic (electron transfer, Na→Na⁺, Cl+e⁻→Cl⁻: NaCl). Covalent (electron sharing: H-H, O=O). VSEPR theory determines shape. Hybridization: sp (linear: BeCl2), sp² (trigonal planar: BF3), sp³ (tetrahedral: CH4, bent: H2O, pyramidal: NH3).",
"class 11 chemistry states of matter": "Class 11 Chemistry - States of Matter: Kinetic theory: molecules in constant motion, elastic collisions, no intermolecular forces (ideal gas). Real gas deviates at high pressure, low temperature. van der Waals equation: (P+a/V²)(V-b)=nRT. Intermolecular forces: H-bonding (strongest), dipole-dipole, van der Waals/London dispersion.",
"class 11 chemistry organic chemistry": "Class 11 Chemistry - Organic Chemistry: Functional groups: -OH (alcohol), -CHO (aldehyde), -CO- (ketone), -COOH (carboxylic acid), -NH2 (amine), -X (halide), -COOR (ester). IUPAC naming. Isomerism: structural (chain, position, functional) and stereoisomerism (cis-trans, optical).",
"class 11 biology cell division": "Class 11 Biology - Cell Division: Mitosis: PMAT (Prophase: chromosomes condense, Metaphase: line up at equator, Anaphase: chromatids pull apart, Telophase: new nuclei form) → 2 diploid identical cells. Meiosis I and II → 4 haploid cells. Crossing over in Prophase I creates variation.",
"class 11 biology classification": "Class 11 Biology - Classification: Five Kingdoms: Monera (no nucleus: bacteria, cyanobacteria), Protista (unicellular eukaryotes: amoeba, paramecium, algae), Fungi (multicellular, absorptive: mushroom, yeast), Plantae, Animalia. Binomial nomenclature: Homo sapiens. Taxonomy ranks: Kingdom→Phylum→Class→Order→Family→Genus→Species.",
"class 11 biology genetics mendel": "Class 11 Biology - Mendel's Laws: Monohybrid Tt×Tt → 1TT:2Tt:1tt (genotype 1:2:1), Tall:short 3:1 (phenotype). Dihybrid TtYy×TtYy → 9:3:3:1 ratio. Law of Dominance, Segregation, Independent Assortment. Incomplete dominance: RR(red)×rr(white)=Rr(pink), ratio 1:2:1. Codominance: AB blood group.",
"class 11 biology ecology": "Class 11 Biology - Ecology: Biotic (living: producers, consumers, decomposers) and Abiotic (non-living: sunlight, temperature, water, soil). Food chain: Grass→Grasshopper→Frog→Snake→Eagle. Energy flow: 10% law (only 10% energy transfers to next level). Nutrient cycles: Carbon cycle, Nitrogen cycle.",
"class 11 math sets functions": "Class 11 Math - Functions: Types: one-one (injective: different inputs, different outputs), onto (surjective: every output has input), bijective (both). Composite: (fog)(x)=f(g(x)). Inverse: f⁻¹(x) exists only for bijective functions. Domain and Range. Even f(-x)=f(x), Odd f(-x)=-f(x).",
"class 11 math trigonometry neb": "Class 11 Math - Trigonometry: Compound angles: sin(A±B), cos(A±B), tan(A±B). Multiple angles: sin2A=2sinAcosA, cos2A=cos²A-sin²A=1-2sin²A=2cos²A-1. t-substitution: if t=tan(A/2), sinA=2t/(1+t²), cosA=(1-t²)/(1+t²). Sum-product: 2sinAcosB=sin(A+B)+sin(A-B).",
"class 11 math limits continuity": "Class 11 Math - Limits: Limit = value function approaches (may not equal function value). Standard: lim(x→0)sinx/x=1, lim(x→0)(eˣ-1)/x=1, lim(x→a)(xⁿ-aⁿ)/(x-a)=naⁿ⁻¹. L'Hopital's rule for 0/0 or ∞/∞. Continuity: f(x) continuous at a if f(a)=lim(x→a)f(x).",
"class 11 math derivatives": "Class 11 Math - Differentiation: From first principles: f'(x)=lim[f(x+h)-f(x)]/h. Rules: d/dx(xⁿ)=nxⁿ⁻¹, d/dx(sinx)=cosx, d/dx(cosx)=-sinx, d/dx(eˣ)=eˣ, d/dx(ln x)=1/x. Product rule: (uv)'=u'v+uv'. Quotient: (u/v)'=(u'v-uv')/v². Chain rule: dy/dx=(dy/du)(du/dx).",
"class 11 math coordinate geometry": "Class 11 Math - Conics: Circle: x²+y²=r² (center origin), (x-h)²+(y-k)²=r² (center h,k). Parabola: y²=4ax (focus at a,0). Ellipse: x²/a²+y²/b²=1 (a>b>0). Hyperbola: x²/a²-y²/b²=1. General second degree equation ax²+2hxy+by²+2gx+2fy+c=0.",
"class 11 accountancy basics": "Class 11 Accountancy - Accounting Concepts: Business entity (business≠owner), Money measurement (only monetary items), Going concern (business continues), Accrual (record when incurred not when paid), Consistency, Conservatism (anticipate losses, not gains), Materiality.",
"class 11 accountancy journal": "Class 11 Accountancy - Journal Entry Rules: Real accounts: Debit what comes in, Credit what goes out. Personal accounts: Debit the receiver, Credit the giver. Nominal accounts: Debit all expenses and losses, Credit all incomes and gains. Every transaction has two effects (double entry).",
"class 11 accountancy financial statements": "Class 11 Accountancy - Financial Statements: Trading Account: Gross Profit = Sales - (Opening Stock + Purchases + Direct Expenses - Closing Stock). P&L Account: Net Profit = Gross Profit - Indirect Expenses + Other Incomes. Balance Sheet: Assets = Liabilities + Owner's Capital.",
"class 11 economics microeconomics": "Class 11 Economics - Demand: Law: price↑→demand↓ (inverse relationship). Factors shifting demand: income, taste, price of substitutes/complements, expectations, population. PED = %ΔQd / %ΔP. Types: elastic (PED>1), inelastic (PED<1), unit elastic (PED=1), perfectly elastic/inelastic.",
"class 11 economics market structure": "Class 11 Economics - Market Structures: Perfect competition: many firms, identical products, price takers, free entry/exit. Monopoly: single firm, unique product, price maker, barriers to entry, P>MR=MC. Monopolistic competition: many firms, differentiated products. Oligopoly: few large firms, interdependence.",
"class 11 computer c programming": "Class 11 Computer Science - C Programming: Structure: #include<stdio.h>, main(){ }, printf(), scanf(). Data types: int, float, double, char. Operators: arithmetic(+,-,*,/,%), relational(>,<,==,!=), logical(&&,||,!). Control: if-else, switch-case. Loops: for(init;condition;update), while(condition), do-while.",
"class 11 computer number systems": "Class 11 Computer Science - Number Systems: Binary to Decimal: 1011₂ = 1×2³+0×2²+1×2¹+1×2⁰ = 8+0+2+1 = 11₁₀. Decimal to Binary: 25÷2=12r1, 12÷2=6r0, 6÷2=3r0, 3÷2=1r1, 1÷2=0r1 → 11001₂. Binary addition: 0+0=0, 0+1=1, 1+1=10 (carry 1).",
"class 11 computer database": "Class 11 Computer Science - Database: DBMS advantages: data sharing, security, integrity, no redundancy. Relational model: tables (relations), rows (tuples), columns (attributes). SQL: SELECT name FROM students WHERE marks>80 ORDER BY marks DESC. Primary key (unique identifier), Foreign key (references primary key of another table).",

# ==================== CLASS 12 ====================

"class 12 physics electrostatics": "Class 12 Physics - Electrostatics: Coulomb's law: F=kq₁q₂/r² (k=9×10⁹ Nm²/C²). Electric field E=F/q=kq/r² (N/C). Electric potential V=W/q=kq/r (Volts). Capacitance C=Q/V (Farads). Parallel plate: C=ε₀A/d. Energy U=½CV²=Q²/2C. Gauss's law: total flux = Q_enclosed/ε₀.",
"class 12 physics current electricity": "Class 12 Physics - Current Electricity: Drift velocity: I=nAeVd. Resistivity: R=ρL/A. Temperature: Rt=R₀(1+αt). Kirchhoff's laws: KCL (sum of currents at junction=0), KVL (sum of EMF = sum of IR in loop). Wheatstone bridge balanced: P/Q=R/S. Potentiometer: null deflection method.",
"class 12 physics electromagnetism": "Class 12 Physics - Electromagnetism: Biot-Savart: dB=μ₀Idl sinθ/4πr². Field of long wire: B=μ₀I/2πr. Solenoid: B=μ₀nI. Force on conductor: F=BIl sinθ. EMF by induction: ε=-dΦ/dt (Faraday). Lenz's law: induced current opposes change. Self-inductance: ε=-L dI/dt. Transformer: V₁/V₂=N₁/N₂=I₂/I₁.",
"class 12 physics modern physics": "Class 12 Physics - Modern Physics: Photoelectric effect: KE_max=hf-φ (Einstein, 1905). Matter waves: λ=h/mv (de Broglie). Bohr's hydrogen: En=-13.6/n² eV, rn=0.529n² Å. Nuclear fission: U-235+n → Ba+Kr+3n+energy. Nuclear fusion: 4H→He+2e⁺+energy. Mass-energy: E=mc². Half-life: t₁/₂=0.693/λ.",
"class 12 physics semiconductor": "Class 12 Physics - Semiconductors: Band theory (valence band, conduction band, band gap). n-type (pentavalent donor: As, P) and p-type (trivalent acceptor: B, Al). p-n junction: depletion layer. Forward bias: current flows. Reverse bias: no current. Half-wave rectifier: 1 diode. Full-wave: 2 diodes or bridge (4 diodes). Transistor as amplifier and switch. Logic gates: AND, OR, NOT, NAND, NOR truth tables.",
"class 12 chemistry electrochemistry": "Class 12 Chemistry - Electrochemistry: Galvanic cell converts chemical→electrical energy. Electrolytic cell: electrical→chemical. Standard hydrogen electrode (SHE): E°=0V (reference). Nernst equation: E=E°-(RT/nF)lnQ = E°-(0.0591/n)logQ at 25°C. Faraday's laws: mass deposited ∝ charge passed ∝ equivalent weight.",
"class 12 chemistry reaction kinetics": "Class 12 Chemistry - Chemical Kinetics: Rate = k[A]^m[B]^n. Order (m+n): 0,1,2. Half-life: t₁/₂=0.693/k (1st order). Arrhenius: k=Ae^(-Ea/RT), ln(k₂/k₁)=(Ea/R)(1/T₁-1/T₂). Catalysts lower activation energy. Enzyme kinetics (Michaelis-Menten). Transition state theory.",
"class 12 chemistry organic reactions": "Class 12 Chemistry - Organic Reactions: Electrophilic addition (HX to alkenes: Markovnikov's rule: H adds to C with more H). Nucleophilic substitution SN1 (tertiary, racemisation) and SN2 (primary, inversion). Elimination. Benzene: electrophilic aromatic substitution. Aldol condensation. Claisen condensation. Polymerization.",
"class 12 biology human physiology": "Class 12 Biology - Human Physiology: Digestion enzymes: salivary amylase (starch), pepsin (protein in stomach), trypsin (protein in intestine), lipase (fats), bile (emulsifies fat). Heart: SA node (pacemaker), AV node, Bundle of His, Purkinje fibres. Blood pressure: systolic/diastolic. Nephron: glomerular filtration, tubular reabsorption, tubular secretion.",
"class 12 biology biotechnology": "Class 12 Biology - Biotechnology: Recombinant DNA: restriction endonucleases cut DNA at specific sites, DNA ligase joins. Vectors (plasmids, bacteriophage) carry foreign DNA into host. PCR: denaturation (95°C), annealing (55°C), extension (72°C) — amplifies DNA. Applications: insulin (E.coli), Bt crops (Bacillus thuringiensis toxin gene), hepatitis B vaccine, gene therapy.",
"class 12 biology evolution": "Class 12 Biology - Evolution: Lamarck (use and disuse, acquired characters — disproved). Darwin: Natural selection, survival of fittest, descent with modification. Evidence: Fossils (Archaeopteryx), Homologous organs (forelimbs of mammals), Analogous organs (wings of birds and insects), Biochemical (cytochrome c), Embryological. Hardy-Weinberg equilibrium: p²+2pq+q²=1.",
"class 12 math integration": "Class 12 Math - Integration: Standard: ∫xⁿdx=xⁿ⁺¹/(n+1)+C, ∫sinx dx=-cosx+C, ∫eˣdx=eˣ+C, ∫(1/x)dx=ln|x|+C. Methods: Substitution (u-substitution), Integration by parts: ∫u dv=uv-∫v du (ILATE: Inverse, Log, Algebraic, Trigonometric, Exponential). Definite integral=area under curve. ∫ₐᵇf(x)dx=[F(b)-F(a)].",
"class 12 math differential equations": "Class 12 Math - Differential Equations: Order = highest derivative. Degree = power of highest derivative. Variable separable: dy/dx=f(x)g(y) → ∫dy/g(y) = ∫f(x)dx. Linear 1st order: dy/dx+Py=Q → solution: ye^∫P dx = ∫Qe^∫P dx dx. Applications: population growth dP/dt=kP → P=P₀eᵏᵗ.",
"class 12 math vectors 3d": "Class 12 Math - 3D Vectors: Position vector r̄=xî+yĵ+zk̂. Direction cosines: l=cosα, m=cosβ, n=cosγ; l²+m²+n²=1. Dot product: a⃗·b⃗=|a||b|cosθ=a₁b₁+a₂b₂+a₃b₃. Cross product: |a⃗×b⃗|=|a||b|sinθ. Equation of line: (x-x₁)/l=(y-y₁)/m=(z-z₁)/n. Plane: lx+my+nz=d.",
"class 12 accountancy partnership": "Class 12 Accountancy - Partnership: Appropriation account before sharing profits: Interest on Capital (dr appropriation), Partner's salary (dr appropriation), Commission, then remaining profit shared in ratio. Goodwill on admission: valued and credited to old partners. Revaluation account for asset/liability reassessment.",
"class 12 accountancy company accounts": "Class 12 Accountancy - Company Accounts: Share capital: Authorized > Issued > Subscribed > Called-up > Paid-up. Issue at premium: Securities Premium Reserve (SPA section 52). Forfeiture: debit share capital (called-up), credit calls in arrears, credit forfeited shares account. Reissue of forfeited shares.",
"class 12 accountancy ratio analysis": "Class 12 Accountancy - Ratio Analysis: Liquidity: Current ratio=CA/CL (ideal 2:1), Quick/Acid-test=(CA-Stock)/CL (ideal 1:1). Profitability: GP%=(GP/Net Sales)×100, NP%=(NP/Net Sales)×100, ROE=NP/Equity×100. Activity: Inventory turnover=COGS/Avg Inventory. Debt-equity=Long term debt/Equity.",
"class 12 economics macroeconomics": "Class 12 Economics - Macroeconomics: GDP=C+I+G+(X-M) (Expenditure method). National Income = GDP - Depreciation - Indirect taxes + Subsidies. Multiplier k=1/(1-MPC)=1/MPS. Aggregate Demand (AD=C+I+G+NX) and Aggregate Supply. Inflationary gap (AD>AS) and Deflationary gap (AD<AS). Keynesian vs Classical.",
"class 12 economics monetary fiscal policy": "Class 12 Economics - Economic Policies: Monetary policy (NRB): CRR, SLR, Bank rate, OMO, Moral suasion. Fiscal policy (government): Tax and spending. Expansionary (recession: ↑G, ↓T). Contractionary (inflation: ↓G, ↑T). Crowding out effect. Supply-side economics. Nepal's budget: revenue and capital expenditure.",
"class 12 computer data structures": "Class 12 Computer Science - Data Structures: Array: O(1) access, O(n) search. Linked list: O(n) access, O(1) insert/delete. Stack (LIFO): push(), pop(), peek(). Queue (FIFO): enqueue(), dequeue(). Binary Tree: left < root < right (BST). Traversal: Inorder(LNR), Preorder(NLR), Postorder(LRN). Sorting: Bubble O(n²), Merge O(n log n), Quick O(n log n) average.",
"class 12 computer networking": "Class 12 Computer Science - Networking: OSI 7 layers (Physical→Data Link→Network→Transport→Session→Presentation→Application). TCP/IP (4 layers). IPv4: 32-bit (4 octets: 192.168.1.1). Subnet mask. Protocols: HTTP(80), HTTPS(443), FTP(21), SMTP(25), DNS(53), DHCP(67/68). Topologies: Star (hub/switch center), Bus (single cable), Ring, Mesh.",
"class 12 computer web technology": "Class 12 Computer Science - Web Technology: HTML5 semantic: <header>, <nav>, <section>, <article>, <aside>, <footer>. CSS3: flexbox (display:flex), grid (display:grid), media queries (@media). JavaScript: DOM (document.getElementById), events (addEventListener), fetch API, JSON.parse/stringify. Node.js: server-side JS. React: component-based UI.",

# ==================== EXAM PREPARATION ====================

"see preparation tips": "SEE Preparation Tips: Start 3 months before. Practice last 10 years question papers (very important). Maths: practice daily, memorize formulas. Science: understand concepts + draw diagrams. Nepali: memorize grammar rules (sandhi, samas, karak, alankar). English: practice all writing formats. Social: read Constitution and history dates.",
"see important chapters math": "SEE Important Chapters - Maths: Sets (Venn diagram problems), Quadratic equations, AP and GP, Matrices, Trigonometry (standard angles and identities), Coordinate geometry, Statistics (mean/median/mode), Mensuration (area and volume), Probability.",
"see important chapters science": "SEE Important Chapters - Science: Genetics (Mendel's laws, Punnett square), Human nervous system (neuron, reflex arc), Acids/bases/salts (pH, neutralization), Electricity (Ohm's law, circuits, power), Optics (mirror and lens formula, eye defects), Carbon compounds, Balancing chemical equations.",
"neb preparation tips": "NEB Grade 12 Preparation Tips: Solve last 10 years NEB papers thoroughly (pattern repeats). Science practical marks (25%) are easy marks — don't miss. Physics: derivations carry marks. Chemistry: write balanced equations. Biology: labeled diagrams important. Accountancy: practice Journal+Ledger+Final Accounts daily.",
"neb important topics physics": "NEB Important Topics - Physics: Electrostatics (capacitor, Gauss law), Current electricity (Kirchhoff's laws, meter bridge), Electromagnetic induction (Faraday, transformer), Photoelectric effect, Bohr model, Semiconductor devices (diode rectifier, transistor), Projectile motion, Young's double slit.",
"neb important topics chemistry": "NEB Important Topics - Chemistry: Atomic structure (quantum numbers, electronic config), Periodic trends, Hybridization and molecular shape, Electrochemistry (Nernst equation, electrolysis), Chemical kinetics (Arrhenius), Organic reactions (addition, substitution), Polymers, Coordination compounds.",
"neb important topics biology": "NEB Important Topics - Biology: Cell division (mitosis and meiosis with diagrams), Mendel's genetics (all types of crosses), Human physiology (all systems with diagrams), Biotechnology (PCR, recombinant DNA, applications), Evolution (Darwin, evidence), Ecology (energy flow, cycles), Biodiversity and conservation.",


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