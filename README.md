# Interview Practice Tool

A lightweight Jupyter-based tool for practicing data science, ML, SQL, and behavioral interview questions.  
You can add questions, practice answering them in a notebook, and check your answers against reference solutions using exact, substring, or semantic similarity.

---

## 🚀 Features
- Question bank stored in **JSON** for persistence.
- Practice questions by category (`ML`, `SQL`, `Stats`, `Leadership`, etc.).
- Multiple answer checking modes:
  - Exact match
  - Substring match
  - Semantic similarity (via embeddings)
- Performance tracking (accuracy across sessions).
- Organized repo structure for easy extension.

---

## 📂 Repo Structure
```
interview-practice/
│
├── notebooks/
│   └── practice.ipynb          # Jupyter notebook for practicing
│
├── src/
│   └── interview_practice.py   # Main InterviewPractice class
│
├── data/
│   └── questions.json          # Persistent Q&A bank
│
├── tests/
│   └── test_interview_practice.py   # Optional unit tests
│
├── requirements.in             # Editable dependency list
├── requirements.txt            # Locked, compiled dependencies
├── README.md                   # Instructions & usage
└── .gitignore                  # Ignore .venv, __pycache__, etc.
```

---

## ⚙️ Installation

1. Clone this repo:
```bash
git clone https://github.com/yourname/interview-practice.git
cd interview-practice
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Mac/Linux
.venv\Scripts\activate      # On Windows
```

3. Install dependencies with `pip-tools`:
```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

---

## 🧑‍💻 Usage

1. Start Jupyter Lab:
```bash
jupyter lab
```

2. Open `notebooks/practice.ipynb`.

3. Example workflow:

```python
from src.interview_practice import InterviewPractice

# Load existing question bank
practice = InterviewPractice()
practice.load("data/questions.json")

# Get a random ML question
practice.get_question(randomize=True, category="ML")

# (Write your answer in the next cell)
my_answer = "Supervised learning uses labels, unsupervised finds patterns."

# Check your answer semantically
practice.check_answer(my_answer, method="semantic")

# Track progress
practice.summary()

# Add a new question
practice.add_question("What is logistic regression?", "A classification algorithm using sigmoid.", "ML")
practice.save("data/questions.json")
```

---

## ✅ Requirements

See `requirements.in` for editable dependencies and `requirements.txt` for pinned versions.

---

## 📌 Roadmap
- Add spaced repetition mode (revisit missed questions).
- Add CLI version (run quizzes outside Jupyter).
- Expand categories and sample banks.