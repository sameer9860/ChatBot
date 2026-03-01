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