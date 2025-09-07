import random
import uuid
import json
from IPython.display import display, Markdown
from typing import List, Dict, Optional

try:
    from sentence_transformers import SentenceTransformer, util
    _HAS_ST = True
except ImportError:
    _HAS_ST = False


class InterviewPractice:
    def __init__(self, questions: Optional[List[Dict]] = None, model_name="all-MiniLM-L6-v2"):
        """
        Initialize with an optional list of question dicts:
        {"question": str, "answer": str, "category": str}
        """
        self.questions = questions if questions else []
        self.current_qid = None
        self.scores = {}  # track results by question id

        if _HAS_ST:
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None

    def add_question(self, question: str, answer: str, category: Optional[str] = None):
        qid = str(uuid.uuid4())[:8]
        self.questions.append({
            "id": qid,
            "question": question,
            "answer": answer,
            "category": category or "general"
        })

    def list_questions(self, category: Optional[str] = None):
        if category:
            return [q for q in self.questions if q["category"] == category]
        return self.questions

    def get_question(self, idx: Optional[int] = None, randomize=False, category: Optional[str] = None):
        if not self.questions:
            raise ValueError("No questions in the bank.")

        candidates = self.list_questions(category)
        if not candidates:
            raise ValueError(f"No questions available in category '{category}'.")

        if randomize:
            q = random.choice(candidates)
        else:
            if idx is None or idx >= len(candidates):
                raise ValueError("Invalid index.")
            q = candidates[idx]

        self.current_qid = q["id"]
        display(Markdown(f"### ❓ Question\n{q['question']}"))
        return q["question"]

    def check_answer(self, user_answer: str, method="semantic", threshold=0.6):
        if self.current_qid is None:
            raise ValueError("No question has been asked.")

        q = next(q for q in self.questions if q["id"] == self.current_qid)
        ref = q["answer"]
        category = q["category"]

        result = False
        score = None

        if method == "exact":
            result = (user_answer.strip().lower() == ref.strip().lower())
            score = 1.0 if result else 0.0
        elif method == "substring":
            result = (ref.lower() in user_answer.lower() or user_answer.lower() in ref.lower())
            score = 1.0 if result else 0.0
        elif method == "semantic":
            if not self.model:
                raise ImportError("sentence-transformers not installed. Install with `pip install sentence-transformers`")
            emb1 = self.model.encode(user_answer, convert_to_tensor=True)
            emb2 = self.model.encode(ref, convert_to_tensor=True)
            score = float(util.cos_sim(emb1, emb2))
            result = score >= threshold
        else:
            raise ValueError("Unsupported comparison method.")

        # Store result
        self.scores.setdefault(self.current_qid, []).append({"user": user_answer, "score": score, "result": result})

        # Display feedback
        display(Markdown(f"### 📝 Your Answer\n{user_answer}"))
        display(Markdown(f"### ✅ Reference Answer\n{ref}"))
        display(Markdown(f"**Category:** {category}"))
        if method == "semantic":
            display(Markdown(f"**Semantic similarity score:** {score:.2f}"))
        display(Markdown(f"**Result:** {'✔️ Correct' if result else '❌ Needs improvement'}"))

        return result, score

    def summary(self):
        """Show performance summary across all answered questions."""
        total = sum(len(v) for v in self.scores.values())
        correct = sum(1 for v in self.scores.values() for r in v if r["result"])
        accuracy = correct / total if total > 0 else 0.0
        display(Markdown(f"### 📊 Performance Summary\n- Total answered: {total}\n- Correct: {correct}\n- Accuracy: {accuracy:.1%}"))
        return {"total": total, "correct": correct, "accuracy": accuracy}

    # 🔹 Persistence Methods
    def save(self, filepath="data/questions.json"):
        with open(filepath, "w") as f:
            json.dump(self.questions, f, indent=2)

    def load(self, filepath="data/questions.json"):
        with open(filepath, "r") as f:
            self.questions = json.load(f)
