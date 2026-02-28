"""
Educational Chatbot using NLTK
================================
Lightweight chatbot using NLTK for tokenization, lemmatization,
TF-IDF similarity matching, and intent classification.

Requirements:
    pip install nltk flask flask-cors

Run:
    python edu_chatbot_nltk.py          # Flask API server
    python edu_chatbot_nltk.py --cli    # Terminal mode
"""

import re
import sys
import json
import random
import string
import warnings
warnings.filterwarnings("ignore")

# ── NLTK Setup ────────────────────────────────────────────────────────────────
import nltk
for pkg in ["punkt", "wordnet", "stopwords", "punkt_tab", "averaged_perceptron_tagger"]:
    nltk.download(pkg, quiet=True)

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words("english")) - {"what", "how", "why", "when", "who", "where", "is", "are", "was"}

# ── Knowledge Base ─────────────────────────────────────────────────────────────
# Each entry: { "patterns": [...keywords...], "response": "...", "tag": "..." }
KNOWLEDGE_BASE = [

    # ── Greetings ──────────────────────────────────────────────────────────────
    {
        "tag": "greeting",
        "patterns": ["hello", "hi", "hey", "howdy", "greetings", "good morning", "good evening", "sup"],
        "responses": [
            "Hello! 👋 I'm EduBot, your NLTK-powered learning assistant. Ask me anything about Math, Science, History, or CS!",
            "Hi there! Ready to learn something new today? 📚",
            "Hey! What topic would you like to explore?"
        ]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "goodbye", "see you", "quit", "exit", "later"],
        "responses": ["Goodbye! Keep learning! 🎓", "See you next time! Stay curious! 🔭"]
    },
    {
        "tag": "thanks",
        "patterns": ["thank", "thanks", "thank you", "appreciate", "helpful"],
        "responses": ["You're welcome! 😊 Any other questions?", "Happy to help! Keep asking!"]
    },
    {
        "tag": "capabilities",
        "patterns": ["what can you do", "help", "topics", "teach", "what do you know", "capabilities"],
        "responses": [
            "I can teach you about:\n📐 Mathematics — algebra, calculus, geometry, statistics\n⚗️ Physics — mechanics, gravity, quantum, thermodynamics\n🧪 Chemistry — atoms, periodic table, reactions\n🧬 Biology — cells, DNA, evolution, photosynthesis\n💻 Computer Science — algorithms, OOP, ML, data structures\n📜 History — world wars, civilizations, revolutions"
        ]
    },

    # ── Mathematics ────────────────────────────────────────────────────────────
    {
        "tag": "calculus",
        "patterns": ["calculus", "derivative", "integral", "differentiation", "integration", "limit", "limits"],
        "responses": [
            "📐 Calculus is the mathematics of continuous change.\n\n• Differential Calculus: deals with rates of change (derivatives). e.g., velocity = d(position)/dt\n• Integral Calculus: deals with accumulation (integrals). e.g., area under a curve\n\nKey rule: d/dx(xⁿ) = nxⁿ⁻¹\nDeveloped by Newton and Leibniz in the 17th century."
        ]
    },
    {
        "tag": "pythagorean",
        "patterns": ["pythagorean", "pythagoras", "right triangle", "hypotenuse", "a squared b squared"],
        "responses": [
            "📐 Pythagorean Theorem: a² + b² = c²\n\nIn any right-angled triangle, the square of the hypotenuse (c) equals the sum of squares of the other two sides.\n\nExample: a=3, b=4 → c = √(9+16) = √25 = 5 ✓\n\nNamed after the Greek mathematician Pythagoras (~570 BC)."
        ]
    },
    {
        "tag": "prime_numbers",
        "patterns": ["prime", "prime number", "prime numbers", "primes", "composite"],
        "responses": [
            "🔢 A prime number is a natural number > 1 with no divisors except 1 and itself.\n\nFirst primes: 2, 3, 5, 7, 11, 13, 17, 19, 23...\n\nKey facts:\n• 2 is the only even prime\n• There are infinitely many primes (Euclid's proof)\n• Largest known prime (2024): 2^136,279,841 − 1 (41 million digits!)"
        ]
    },
    {
        "tag": "algebra",
        "patterns": ["algebra", "equation", "variable", "polynomial", "quadratic", "linear equation"],
        "responses": [
            "📐 Algebra uses symbols (variables) to represent unknowns and express relationships.\n\nTypes:\n• Linear: ax + b = 0 → x = -b/a\n• Quadratic: ax² + bx + c = 0 → x = (-b ± √(b²-4ac)) / 2a\n• Polynomial: expressions with multiple terms\n\nAlgebra is the foundation of all advanced mathematics!"
        ]
    },
    {
        "tag": "statistics",
        "patterns": ["statistics", "mean", "median", "mode", "standard deviation", "variance", "probability"],
        "responses": [
            "📊 Key Statistics Concepts:\n\n• Mean: sum of values ÷ count\n• Median: middle value when sorted\n• Mode: most frequent value\n• Variance: average of squared deviations from mean\n• Std Deviation: √variance — measures spread\n• Probability: P(event) = favorable outcomes / total outcomes"
        ]
    },
    {
        "tag": "pi",
        "patterns": ["pi", "3.14", "circumference", "circle formula"],
        "responses": [
            "⭕ Pi (π) ≈ 3.14159265358979...\n\nIt's the ratio of a circle's circumference to its diameter.\n\nFormulas using π:\n• Circumference = 2πr\n• Area of circle = πr²\n• Volume of sphere = (4/3)πr³\n\nπ is irrational — its decimal never ends or repeats!"
        ]
    },

    # ── Physics ────────────────────────────────────────────────────────────────
    {
        "tag": "newton_laws",
        "patterns": ["newton", "newton law", "laws of motion", "inertia", "force mass acceleration", "action reaction"],
        "responses": [
            "⚙️ Newton's Three Laws of Motion:\n\n1️⃣ Inertia: An object stays at rest (or in motion) unless acted on by an external force.\n\n2️⃣ F = ma: Force = Mass × Acceleration. Bigger force → bigger acceleration.\n\n3️⃣ Action-Reaction: For every action there is an equal and opposite reaction.\n\nPublished in 'Principia Mathematica' (1687)."
        ]
    },
    {
        "tag": "gravity",
        "patterns": ["gravity", "gravitation", "gravitational", "weight", "free fall", "g force"],
        "responses": [
            "🌍 Gravity is the attractive force between objects with mass.\n\n• On Earth: g = 9.8 m/s² (acceleration of free fall)\n• Newton's Law: F = Gm₁m₂/r²\n• Einstein's view: gravity is the curvature of spacetime caused by mass\n\nGravity keeps planets in orbit and holds our atmosphere in place!"
        ]
    },
    {
        "tag": "speed_of_light",
        "patterns": ["speed of light", "light speed", "c constant", "299792458"],
        "responses": [
            "💡 Speed of Light: c = 299,792,458 m/s ≈ 3×10⁸ m/s\n\n• Light travels ~186,000 miles per second\n• Takes ~8 minutes to travel from Sun to Earth\n• Einstein showed c is the universe's speed limit (Special Relativity)\n• Nothing with mass can reach or exceed c"
        ]
    },
    {
        "tag": "quantum",
        "patterns": ["quantum", "quantum mechanics", "quantum physics", "wave particle", "superposition", "uncertainty principle", "heisenberg"],
        "responses": [
            "⚛️ Quantum Mechanics describes nature at atomic/subatomic scales.\n\nKey principles:\n• Wave-particle duality: particles behave as both waves and particles\n• Heisenberg Uncertainty: can't know position AND momentum precisely simultaneously\n• Superposition: particles exist in multiple states until measured\n• Entanglement: particles can be linked regardless of distance\n\nThe most accurate physical theory ever tested!"
        ]
    },
    {
        "tag": "thermodynamics",
        "patterns": ["thermodynamics", "entropy", "heat", "temperature", "energy conservation", "laws of thermodynamics"],
        "responses": [
            "🌡️ Laws of Thermodynamics:\n\n0th: If A=B and B=C in temperature, then A=C (thermal equilibrium)\n1st: Energy cannot be created or destroyed, only converted (conservation)\n2nd: Entropy (disorder) of an isolated system always increases\n3rd: Absolute zero (0 Kelvin = -273.15°C) cannot be reached\n\nThese laws govern all engines, refrigerators, and energy systems!"
        ]
    },

    # ── Chemistry ──────────────────────────────────────────────────────────────
    {
        "tag": "atom",
        "patterns": ["atom", "atomic", "atomic structure", "proton", "neutron", "electron", "nucleus"],
        "responses": [
            "⚛️ Atomic Structure:\n\nAn atom consists of:\n• Nucleus: protons (+) and neutrons (0) — very dense\n• Electron cloud: electrons (-) orbiting nucleus in shells\n\nFun fact: atoms are 99.99% empty space!\nIf the nucleus were a marble, the atom would be the size of a football stadium.\n\nAtomic number = number of protons (defines the element)"
        ]
    },
    {
        "tag": "periodic_table",
        "patterns": ["periodic table", "elements", "mendeleev", "chemical element", "atomic number", "atomic mass"],
        "responses": [
            "🧪 The Periodic Table organizes 118 known elements by atomic number.\n\n• Rows = Periods (same number of electron shells)\n• Columns = Groups (same number of valence electrons → similar properties)\n• Metals (left), Metalloids (middle), Non-metals (right)\n\nCreated by Dmitri Mendeleev in 1869. He even predicted undiscovered elements based on gaps!"
        ]
    },
    {
        "tag": "photosynthesis",
        "patterns": ["photosynthesis", "chlorophyll", "chloroplast", "plant food", "carbon dioxide oxygen plant"],
        "responses": [
            "🌿 Photosynthesis — How plants make food:\n\n6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂\n\nProcess:\n1. Chlorophyll in leaves absorbs sunlight\n2. Light splits water molecules (H₂O)\n3. CO₂ from air is converted into glucose\n4. Oxygen released as a byproduct\n\nPhotosynthesis produces the oxygen we breathe and is the base of most food chains!"
        ]
    },

    # ── Biology ────────────────────────────────────────────────────────────────
    {
        "tag": "dna",
        "patterns": ["dna", "deoxyribonucleic", "gene", "genes", "chromosome", "genetics", "genome"],
        "responses": [
            "🧬 DNA (Deoxyribonucleic Acid) carries genetic information.\n\nStructure: Double helix — two strands of nucleotides.\nBase pairs (always paired):\n• Adenine (A) ↔ Thymine (T)\n• Guanine (G) ↔ Cytosine (C)\n\nFacts:\n• Human genome: ~3 billion base pairs\n• If uncoiled, DNA in one cell = ~2 meters long\n• Genes are segments of DNA that encode proteins\n• 99.9% of DNA is identical between all humans!"
        ]
    },
    {
        "tag": "evolution",
        "patterns": ["evolution", "natural selection", "darwin", "species", "adaptation", "survival of fittest"],
        "responses": [
            "🦕 Evolution by Natural Selection (Charles Darwin, 1859):\n\n1. Variation: individuals differ in traits\n2. Heredity: traits are passed to offspring\n3. Selection: those with favorable traits survive and reproduce more\n4. Over millions of years → new species emerge\n\nEvidence: fossil record, DNA comparisons, observed changes in bacteria, homologous structures in different species."
        ]
    },
    {
        "tag": "cell",
        "patterns": ["cell", "cells", "cell structure", "organelle", "mitochondria", "nucleus cell", "prokaryote", "eukaryote"],
        "responses": [
            "🔬 Cell Biology:\n\nTwo main types:\n• Prokaryotes: No membrane-bound nucleus (bacteria)\n• Eukaryotes: Have a nucleus (plants, animals, fungi)\n\nKey organelles:\n• Nucleus: contains DNA, controls cell\n• Mitochondria: produces energy (ATP) — 'powerhouse of the cell'\n• Ribosome: builds proteins\n• Cell membrane: controls what enters/exits\n• Chloroplast (plants): site of photosynthesis"
        ]
    },

    # ── Computer Science ───────────────────────────────────────────────────────
    {
        "tag": "algorithm",
        "patterns": ["algorithm", "sorting", "searching", "binary search", "bubble sort", "time complexity", "big o"],
        "responses": [
            "💻 Algorithms are step-by-step procedures to solve problems.\n\nCommon sorting algorithms:\n• Bubble Sort: O(n²) — simple but slow\n• Merge Sort: O(n log n) — divide and conquer\n• Quick Sort: O(n log n) average — very fast in practice\n\nSearching:\n• Linear Search: O(n)\n• Binary Search: O(log n) — requires sorted data\n\nBig O notation describes how runtime scales with input size."
        ]
    },
    {
        "tag": "oop",
        "patterns": ["oop", "object oriented", "class", "object", "inheritance", "encapsulation", "polymorphism", "abstraction"],
        "responses": [
            "💻 Object-Oriented Programming (OOP) — 4 Pillars:\n\n1️⃣ Encapsulation: bundle data + methods; hide internal details\n2️⃣ Inheritance: child class reuses parent class code\n3️⃣ Polymorphism: same method name, different behavior\n4️⃣ Abstraction: hide complexity, show only what's needed\n\nLanguages: Python, Java, C++, C#\nReal-world analogy: A 'Car' class has attributes (color, speed) and methods (drive(), brake())."
        ]
    },
    {
        "tag": "machine_learning",
        "patterns": ["machine learning", "ml", "neural network", "deep learning", "artificial intelligence", "ai", "model training"],
        "responses": [
            "🤖 Machine Learning — computers learn from data!\n\nTypes:\n• Supervised Learning: learns from labeled examples (e.g., spam detection)\n• Unsupervised Learning: finds hidden patterns (e.g., customer clustering)\n• Reinforcement Learning: learns by trial & reward (e.g., game-playing AI)\n\nPopular algorithms: Linear Regression, Decision Trees, Neural Networks, SVM\n\nDeep Learning uses multi-layered neural networks inspired by the brain."
        ]
    },
    {
        "tag": "data_structures",
        "patterns": ["data structure", "array", "linked list", "stack", "queue", "tree", "graph", "hash table"],
        "responses": [
            "💻 Common Data Structures:\n\n• Array: indexed collection, O(1) access\n• Linked List: nodes with pointers, O(1) insert/delete\n• Stack: Last-In-First-Out (LIFO) — like a stack of plates\n• Queue: First-In-First-Out (FIFO) — like a line\n• Tree: hierarchical structure (e.g., file systems)\n• Graph: nodes + edges (e.g., social networks, maps)\n• Hash Table: key-value pairs, O(1) average lookup"
        ]
    },

    # ── History ────────────────────────────────────────────────────────────────
    {
        "tag": "ww2",
        "patterns": ["world war 2", "world war ii", "second world war", "ww2", "wwii", "hitler", "nazi", "holocaust"],
        "responses": [
            "📜 World War II (1939–1945):\n\nCauses: Rise of fascism, Nazi Germany's expansionism, appeasement failure\n\nKey events:\n• 1939: Germany invades Poland → war begins\n• 1941: Japan attacks Pearl Harbor → USA enters\n• 1944: D-Day — Allied invasion of Normandy\n• 1945: Germany surrenders (May), Japan surrenders after atomic bombs (Aug)\n\nDeadliest conflict in history: ~70–85 million deaths. Led to formation of the United Nations."
        ]
    },
    {
        "tag": "ww1",
        "patterns": ["world war 1", "world war i", "first world war", "ww1", "wwi", "great war", "archduke franz ferdinand"],
        "responses": [
            "📜 World War I (1914–1918) — 'The Great War':\n\nTrigger: Assassination of Archduke Franz Ferdinand (June 1914)\nAlliances: Allied Powers vs. Central Powers\n\nKey events:\n• Trench warfare on the Western Front\n• USA joins in 1917\n• Armistice signed November 11, 1918\n\nResult: ~20 million deaths, fall of four empires, Treaty of Versailles — which set conditions leading to WWII."
        ]
    },
    {
        "tag": "french_revolution",
        "patterns": ["french revolution", "bastille", "marie antoinette", "reign of terror", "napoleon", "robespierre"],
        "responses": [
            "📜 The French Revolution (1789–1799):\n\nCauses: Financial crisis, social inequality (Three Estates), Enlightenment ideas\n\nKey events:\n• 1789: Storming of the Bastille (July 14 — now France's national day)\n• Declaration of Rights of Man\n• Execution of King Louis XVI and Marie Antoinette\n• Reign of Terror (1793–94) under Robespierre\n• Rise of Napoleon Bonaparte\n\nLasting impact: spread of democratic ideals across Europe."
        ]
    },
    {
        "tag": "ancient_rome",
        "patterns": ["rome", "roman", "roman empire", "julius caesar", "roman republic", "gladiator", "colosseum"],
        "responses": [
            "🏛️ Ancient Rome:\n\n• Founded: ~753 BC (traditionally by Romulus)\n• Roman Republic: 509–27 BC (Senate, consuls)\n• Roman Empire: 27 BC–476 AD (Emperors like Augustus, Nero, Marcus Aurelius)\n• Julius Caesar: general/dictator, assassinated 44 BC → led to rise of Augustus\n• Fall: 476 AD (Western Empire) — barbarian invasions, overextension\n\nLegacy: law systems, Latin language, Christianity's spread, architecture."
        ]
    },
]

# ── NLTK Preprocessing ─────────────────────────────────────────────────────────
def preprocess(text: str) -> list[str]:
    """Tokenize, lowercase, remove punctuation, lemmatize, remove stopwords."""
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in STOPWORDS and len(t) > 1]
    return tokens

def bag_of_words_score(user_tokens: list[str], pattern_tokens: list[str]) -> float:
    """Score = number of matching tokens / total pattern tokens."""
    if not pattern_tokens:
        return 0.0
    matches = sum(1 for t in user_tokens if t in pattern_tokens)
    return matches / len(pattern_tokens)

# ── Core Chatbot ───────────────────────────────────────────────────────────────
def get_response(user_input: str) -> dict:
    """Match user input to the best knowledge base entry using NLTK."""
    if not user_input.strip():
        return {"response": "Please ask a question!", "tag": "empty", "score": 0}

    user_tokens = preprocess(user_input)

    best_score = 0.0
    best_entry = None

    for entry in KNOWLEDGE_BASE:
        # Build token set from all patterns in this entry
        pattern_tokens = []
        for pattern in entry["patterns"]:
            pattern_tokens.extend(preprocess(pattern))
        pattern_tokens = list(set(pattern_tokens))

        score = bag_of_words_score(user_tokens, pattern_tokens)

        # Bonus: direct substring match in original text
        for pattern in entry["patterns"]:
            if pattern.lower() in user_input.lower():
                score += 0.4
                break

        if score > best_score:
            best_score = score
            best_entry = entry

    THRESHOLD = 0.12
    if best_entry and best_score >= THRESHOLD:
        responses = best_entry.get("responses", [best_entry.get("response", "")])
        return {
            "response": random.choice(responses) if isinstance(responses, list) else responses,
            "tag": best_entry["tag"],
            "score": round(best_score, 3)
        }

    # Fallback suggestions
    suggestions = random.sample([e["tag"].replace("_", " ") for e in KNOWLEDGE_BASE], 4)
    return {
        "response": f"I'm not sure about that. Try asking about: {', '.join(suggestions)}.\n\nOr type 'help' to see all topics!",
        "tag": "unknown",
        "score": 0
    }

# ── Flask API ──────────────────────────────────────────────────────────────────
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from datetime import datetime

    app = Flask(__name__)
    CORS(app)

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        user_msg = data.get("message", "")
        result = get_response(user_msg)
        return jsonify({
            "response": result["response"],
            "tag": result["tag"],
            "score": result["score"],
            "timestamp": datetime.now().isoformat()
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "engine": "NLTK", "topics": len(KNOWLEDGE_BASE)})

    @app.route("/topics", methods=["GET"])
    def topics():
        return jsonify({"topics": [e["tag"] for e in KNOWLEDGE_BASE]})

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "name": "EduBot — NLTK Educational Chatbot",
            "endpoints": {
                "POST /chat": "Body: {'message': 'your question'}",
                "GET /topics": "List all available topics",
                "GET /health": "API status"
            }
        })

    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

# ── CLI Mode ────────────────────────────────────────────────────────────────────
def run_cli():
    print("\n" + "═"*58)
    print("  🎓  EduBot — NLTK Educational Chatbot")
    print("  Type 'topics' to list topics, 'quit' to exit")
    print("═"*58)

    while True:
        try:
            user_input = input("\n You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n Bot: Goodbye! Keep learning! 🎓")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print(" Bot: Goodbye! Keep learning! 🎓")
            break
        if user_input.lower() == "topics":
            tags = [e["tag"].replace("_", " ") for e in KNOWLEDGE_BASE]
            print(f" Bot: Topics: {', '.join(tags)}")
            continue

        result = get_response(user_input)
        print(f"\n Bot [{result['tag']} | score: {result['score']}]:")
        print(f" {result['response']}")

# ── Entry Point ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    elif HAS_FLASK:
        print("🚀 EduBot (NLTK) running at http://localhost:5000")
        app.run(debug=True, port=5000)
    else:
        print("Flask not installed. Running in CLI mode instead.")
        print("Install with: pip install flask flask-cors")
        run_cli()