import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path
import csv

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
HISTORY_FILE = DATA_DIR / "quiz_history.json"

QUESTIONS = [
    ("Python", "Python Basics", "Easy", "Which keyword defines a function in Python?", ["func", "def", "function", "define"], "def", "Python functions are declared with def."),
    ("Python", "Python Basics", "Easy", "Which type stores an ordered, changeable collection?", ["tuple", "set", "list", "frozenset"], "list", "Lists preserve order and can be modified."),
    ("Python", "Python Basics", "Easy", "What is len('data')?", ["3", "4", "5", "Error"], "4", "The word data has four characters."),
    ("Python", "Python Basics", "Medium", "Which expression creates a dictionary?", ["['a', 1]", "('a', 1)", "{'a': 1}", "{'a', 1}"], "{'a': 1}", "Dictionaries use key:value pairs inside braces."),
    ("Python", "Python Basics", "Medium", "What values are produced by range(2, 5)?", ["2, 3, 4", "2, 3, 4, 5", "1, 2, 3, 4", "3, 4, 5"], "2, 3, 4", "The stop value 5 is excluded."),
    ("Data Science", "Data Analysis", "Easy", "Which Python library is widely used for tabular data analysis?", ["Pandas", "Turtle", "Pygame", "Tkinter"], "Pandas", "Pandas provides Series and DataFrame structures."),
    ("Data Science", "Data Analysis", "Easy", "What does a row in a data table usually represent?", ["An observation or record", "Only a column name", "A Python package", "A chart style"], "An observation or record", "Rows typically represent records and columns represent variables."),
    ("Data Science", "Statistics", "Easy", "What is the mean of 2, 4, and 6?", ["3", "4", "5", "6"], "4", "(2 + 4 + 6) / 3 = 4."),
    ("Data Science", "Statistics", "Medium", "Which statistic is generally less affected by extreme outliers?", ["Mean", "Median", "Range", "Maximum"], "Median", "The median is often more robust to extreme values."),
    ("Data Science", "Data Analysis", "Medium", "Why handle missing values before analysis?", ["Improve data completeness", "Always increase row count", "Convert numbers to text", "Remove every column"], "Improve data completeness", "Missing values can affect analysis and should be handled appropriately."),
    ("Artificial Intelligence", "Machine Learning", "Easy", "Supervised learning examples usually include:", ["Only unlabeled inputs", "Inputs and target labels", "Only file names", "No examples"], "Inputs and target labels", "Supervised learning uses examples with known target values or labels."),
    ("Artificial Intelligence", "Machine Learning", "Easy", "Which task predicts a continuous numeric value?", ["Regression", "Clustering", "Sorting", "Tokenization"], "Regression", "Regression estimates numeric quantities."),
    ("Artificial Intelligence", "Machine Learning", "Medium", "What is overfitting?", ["Learning training details too closely and generalizing poorly", "Having no training data", "A dataset with no columns", "A chart with many colors"], "Learning training details too closely and generalizing poorly", "An overfit model can perform poorly on unseen data."),
    ("Artificial Intelligence", "Machine Learning", "Medium", "Which method groups similar points without target labels?", ["Clustering", "Regression", "Supervised classification", "Manual sorting only"], "Clustering", "Clustering is an unsupervised learning task."),
    ("Artificial Intelligence", "Machine Learning", "Medium", "Why test a model on data not used for training?", ["Estimate performance on unseen data", "Automatically enlarge training data", "Guarantee perfect accuracy", "Remove the need for labels"], "Estimate performance on unseen data", "Held-out data helps estimate generalization."),
    ("Aptitude", "Numerical Reasoning", "Easy", "A notebook costs ₹20. What do 3 notebooks cost?", ["₹40", "₹50", "₹60", "₹80"], "₹60", "3 × ₹20 = ₹60."),
    ("Aptitude", "Numerical Reasoning", "Easy", "What is 25% of 200?", ["25", "40", "50", "75"], "50", "25% is one quarter; 200 / 4 = 50."),
    ("Aptitude", "Numerical Reasoning", "Medium", "A car travels 120 km in 3 hours. Average speed?", ["30 km/h", "40 km/h", "60 km/h", "90 km/h"], "40 km/h", "Speed = distance / time = 120 / 3 = 40 km/h."),
    ("Aptitude", "Logical Reasoning", "Easy", "Complete the sequence: 2, 4, 6, 8, __", ["9", "10", "11", "12"], "10", "The sequence increases by 2 each time."),
    ("Aptitude", "Logical Reasoning", "Medium", "If all roses are flowers, which statement must be true?", ["All roses fade quickly", "No roses are flowers", "All roses are flowers", "All flowers are roses"], "All roses are flowers", "This is exactly what the premise states."),
]


def read_history():
    DATA_DIR.mkdir(exist_ok=True)
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8")) if HISTORY_FILE.exists() else []
    except (json.JSONDecodeError, OSError):
        return []


def write_history(history):
    DATA_DIR.mkdir(exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")


class QuizMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster - Smart Quiz App")
        self.root.geometry("900x680")
        self.root.minsize(760, 560)
        self.root.configure(bg="#f3f5fb")
        self.history = read_history()
        self.questions = []
        self.answers = {}
        self.index = 0
        self.seconds_left = 0
        self.timer_job = None
        self.quiz_started = None
        self.player = "Guest"
        self.build_shell()
        self.show_home()

    def build_shell(self):
        header = tk.Frame(self.root, bg="#3730a3", height=92)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🧠 QuizMaster", bg="#3730a3", fg="white",
                 font=("Segoe UI", 23, "bold")).pack(anchor="w", padx=24, pady=(14, 0))
        tk.Label(header, text="Learn smarter • Track progress • Improve weak topics",
                 bg="#3730a3", fg="#e0e7ff", font=("Segoe UI", 10)).pack(anchor="w", padx=26)
        nav = tk.Frame(self.root, bg="#e5e7eb")
        nav.pack(fill="x")
        for label, command in [
            ("Home / Start Quiz", self.show_home),
            ("Analytics", self.show_analytics),
            ("Quiz History", self.show_history),
            ("About", self.show_about),
        ]:
            ttk.Button(nav, text=label, command=command).pack(side="left", padx=7, pady=8)
        self.body = tk.Frame(self.root, bg="#f3f5fb")
        self.body.pack(fill="both", expand=True, padx=22, pady=18)
        self.status = tk.Label(self.root, text=" ",
                               bg="#e5e7eb", fg="#374151", anchor="w", padx=12, pady=6)
        self.status.pack(fill="x", side="bottom")

    def clear_body(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        for child in self.body.winfo_children():
            child.destroy()

    def heading(self, title, subtitle=""):
        tk.Label(self.body, text=title, bg="#f3f5fb", fg="#111827",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(0, 4))
        if subtitle:
            tk.Label(self.body, text=subtitle, bg="#f3f5fb", fg="#6b7280",
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 16))

    def show_home(self):
        self.clear_body()
        self.heading("Welcome to QuizMaster", "Choose your quiz settings and test your knowledge.")
        form = tk.Frame(self.body, bg="white", padx=22, pady=20,
                        highlightbackground="#dbe1ee", highlightthickness=1)
        form.pack(fill="x", pady=8)
        self.name_var = tk.StringVar(value="")
        self.category_var = tk.StringVar(value="All categories")
        self.level_var = tk.StringVar(value="All levels")
        self.count_var = tk.IntVar(value=5)
        self.minutes_var = tk.IntVar(value=5)
        categories = ["All categories"] + sorted({q[0] for q in QUESTIONS})
        self.form_row(form, 0, "Your name (optional)", ttk.Entry(form, textvariable=self.name_var, width=36))
        self.form_row(form, 1, "Category", ttk.Combobox(form, textvariable=self.category_var, values=categories, state="readonly", width=33))
        self.form_row(form, 2, "Difficulty", ttk.Combobox(form, textvariable=self.level_var, values=["All levels", "Easy", "Medium"], state="readonly", width=33))
        self.form_row(form, 3, "Number of questions", ttk.Spinbox(form, from_=3, to=10, textvariable=self.count_var, width=8))
        self.form_row(form, 4, "Time limit (minutes)", ttk.Spinbox(form, from_=1, to=20, textvariable=self.minutes_var, width=8))
        ttk.Button(form, text="Start Quiz", command=self.start_quiz).grid(row=5, column=1, sticky="w", pady=(18, 2))
        tk.Label(self.body, text=f" ",
                 bg="#f3f5fb", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w", pady=14)

    def form_row(self, parent, row, label, widget):
        tk.Label(parent, text=label, bg="white", fg="#374151",
                 font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 22), pady=8)
        widget.grid(row=row, column=1, sticky="w", pady=8)

    def start_quiz(self):
        category = self.category_var.get()
        level = self.level_var.get()
        pool = [q for q in QUESTIONS if (category == "All categories" or q[0] == category)
                and (level == "All levels" or q[2] == level)]
        if len(pool) < 3:
            messagebox.showerror("Not enough questions", "Choose another category or difficulty.")
            return
        try:
            count = max(3, min(int(self.count_var.get()), 10, len(pool)))
            minutes = max(1, min(int(self.minutes_var.get()), 20))
        except (ValueError, tk.TclError):
            messagebox.showerror("Invalid settings", "Enter a valid number of questions and minutes.")
            return
        self.questions = random.sample(pool, count)
        self.answers = {}
        self.index = 0
        self.seconds_left = minutes * 60
        self.player = self.name_var.get().strip() or "Guest"
        self.quiz_started = datetime.now()
        self.show_question()
        self.tick()

    def show_question(self):
        self.clear_body()
        q = self.questions[self.index]
        top = tk.Frame(self.body, bg="#f3f5fb")
        top.pack(fill="x")
        tk.Label(top, text=f"Question {self.index + 1} of {len(self.questions)}",
                 bg="#f3f5fb", fg="#4f46e5", font=("Segoe UI", 11, "bold")).pack(side="left")
        self.timer_label = tk.Label(top, text=self.time_text(), bg="#f3f5fb",
                                    fg="#b91c1c", font=("Segoe UI", 12, "bold"))
        self.timer_label.pack(side="right")
        tk.Label(self.body, text=f"Category: {q[0]}  •  Topic: {q[1]}  •  Difficulty: {q[2]}",
                 bg="#f3f5fb", fg="#6b7280", font=("Segoe UI", 10)).pack(anchor="w", pady=(16, 8))
        card = tk.Frame(self.body, bg="white", padx=22, pady=22,
                        highlightbackground="#dbe1ee", highlightthickness=1)
        card.pack(fill="x", pady=5)
        tk.Label(card, text=q[3], bg="white", fg="#111827", wraplength=760,
                 justify="left", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 18))
        self.answer_var = tk.StringVar(value=self.answers.get(self.index, ""))
        for option in q[4]:
            ttk.Radiobutton(card, text=option, variable=self.answer_var, value=option).pack(anchor="w", pady=7)
        controls = tk.Frame(self.body, bg="#f3f5fb")
        controls.pack(fill="x", pady=18)
        if self.index > 0:
            ttk.Button(controls, text="Previous", command=self.previous_question).pack(side="left")
        if self.index < len(self.questions) - 1:
            ttk.Button(controls, text="Save & Next", command=self.next_question).pack(side="right")
        else:
            ttk.Button(controls, text="Submit Quiz", command=self.submit_quiz).pack(side="right")
        ttk.Button(controls, text="Submit Now", command=self.submit_quiz).pack(side="right", padx=8)

    def store_answer(self):
        selected = self.answer_var.get()
        if selected:
            self.answers[self.index] = selected

    def previous_question(self):
        self.store_answer()
        self.index -= 1
        self.show_question()

    def next_question(self):
        self.store_answer()
        self.index += 1
        self.show_question()

    def time_text(self):
        return f"Time left: {self.seconds_left // 60:02d}:{self.seconds_left % 60:02d}"

    def tick(self):
        if not self.questions:
            return
        if self.seconds_left <= 0:
            self.submit_quiz(auto=True)
            return
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.config(text=self.time_text())
        self.seconds_left -= 1
        self.timer_job = self.root.after(1000, self.tick)

    def submit_quiz(self, auto=False):
        self.store_answer()
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        details = []
        topic_stats = {}
        correct = 0
        for i, q in enumerate(self.questions):
            selected = self.answers.get(i, "Not answered")
            is_correct = selected == q[5]
            correct += int(is_correct)
            stat = topic_stats.setdefault(q[1], {"correct": 0, "total": 0})
            stat["correct"] += int(is_correct)
            stat["total"] += 1
            details.append({
                "question": q[3], "topic": q[1], "selected": selected,
                "correct_answer": q[5], "is_correct": is_correct, "explanation": q[6]
            })
        total = len(self.questions)
        elapsed = max(0, int((datetime.now() - self.quiz_started).total_seconds()))
        attempt = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "name": self.player, "category": self.category_var.get(),
            "difficulty": self.level_var.get(), "score": correct, "total": total,
            "percentage": round(correct / total * 100, 1), "elapsed_seconds": elapsed,
            "auto_submitted": auto, "topics": topic_stats, "details": details
        }
        self.history.append(attempt)
        write_history(self.history)
        self.show_result(attempt)

    def show_result(self, result):
        self.clear_body()
        self.heading("Quiz Results", "Review your score and learn from each answer.")
        cards = tk.Frame(self.body, bg="#f3f5fb")
        cards.pack(fill="x", pady=8)
        for title, value in [
            ("Score", f'{result["score"]}/{result["total"]}'),
            ("Accuracy", f'{result["percentage"]}%'),
            ("Time taken", f'{result["elapsed_seconds"] // 60:02d}:{result["elapsed_seconds"] % 60:02d}')
        ]:
            box = tk.Frame(cards, bg="white", padx=20, pady=15, highlightbackground="#dbe1ee", highlightthickness=1)
            box.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(box, text=title, bg="white", fg="#6b7280", font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(box, text=value, bg="white", fg="#3730a3", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        if result["auto_submitted"]:
            tk.Label(self.body, text="Time ran out; your answers were submitted automatically.",
                     bg="#fef3c7", fg="#92400e", padx=8, pady=6).pack(anchor="w", pady=6)
        canvas = tk.Canvas(self.body, bg="#f3f5fb", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.body, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="#f3f5fb")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, pady=8)
        scrollbar.pack(side="right", fill="y", pady=8)
        for n, item in enumerate(result["details"], 1):
            label = f'{n}. {item["question"]}\nYour answer: {item["selected"]}\nCorrect answer: {item["correct_answer"]}\n{"✓ Correct" if item["is_correct"] else "✗ Practise this"}\nExplanation: {item["explanation"]}'
            tk.Label(inner, text=label, bg="white", fg="#111827", justify="left",
                     wraplength=790, padx=12, pady=10, anchor="w",
                     font=("Segoe UI", 10)).pack(fill="x", pady=4)
        ttk.Button(self.body, text="Back to Home", command=self.show_home).pack(anchor="w", pady=8)

    def show_analytics(self):
        self.clear_body()
        self.heading("Performance Analytics", "Simple summaries from your saved quiz attempts.")
        if not self.history:
            tk.Label(self.body, text="Complete a quiz first to see analytics.",
                     bg="#f3f5fb", fg="#6b7280", font=("Segoe UI", 12)).pack(anchor="w")
            return
        attempts = len(self.history)
        avg = sum(x["percentage"] for x in self.history) / attempts
        best = max(x["percentage"] for x in self.history)
        summary = tk.Frame(self.body, bg="#f3f5fb")
        summary.pack(fill="x", pady=8)
        for title, value in [("Quiz attempts", str(attempts)), ("Average accuracy", f"{avg:.1f}%"), ("Best accuracy", f"{best:.1f}%")]:
            box = tk.Frame(summary, bg="white", padx=16, pady=14, highlightbackground="#dbe1ee", highlightthickness=1)
            box.pack(side="left", expand=True, fill="x", padx=(0, 8))
            tk.Label(box, text=title, bg="white", fg="#6b7280").pack(anchor="w")
            tk.Label(box, text=value, bg="white", fg="#3730a3", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(self.body, text="Accuracy by attempt", bg="#f3f5fb", fg="#111827",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(18, 6))
        for i, h in enumerate(self.history[-10:], max(1, len(self.history) - 9)):
            row = tk.Frame(self.body, bg="#f3f5fb")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f'Attempt {i} — {h["date"]}', bg="#f3f5fb", width=27, anchor="w").pack(side="left")
            bar = ttk.Progressbar(row, maximum=100, value=h["percentage"])
            bar.pack(side="left", fill="x", expand=True, padx=8)
            tk.Label(row, text=f'{h["percentage"]}%', bg="#f3f5fb", width=8).pack(side="right")
        all_topics = {}
        for h in self.history:
            for topic, stats in h.get("topics", {}).items():
                item = all_topics.setdefault(topic, {"correct": 0, "total": 0})
                item["correct"] += stats["correct"]
                item["total"] += stats["total"]
        tk.Label(self.body, text="Weak-topic analysis (lowest accuracy first)", bg="#f3f5fb",
                 fg="#111827", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(20, 6))
        if not all_topics:
            tk.Label(self.body, text="No topic data yet.", bg="#f3f5fb").pack(anchor="w")
        else:
            sorted_topics = sorted(all_topics.items(), key=lambda pair: pair[1]["correct"] / pair[1]["total"])
            for topic, stats in sorted_topics:
                accuracy = stats["correct"] / stats["total"] * 100
                message = " • Practise this topic" if accuracy < 60 else ""
                tk.Label(self.body, text=f'{topic}: {accuracy:.1f}% ({stats["total"]} questions){message}',
                         bg="#fef3c7" if accuracy < 60 else "#f3f5fb",
                         fg="#92400e" if accuracy < 60 else "#374151",
                         anchor="w", padx=8, pady=5).pack(fill="x", pady=2)
        ttk.Button(self.body, text="Export summary to CSV", command=self.export_csv).pack(anchor="w", pady=14)

    def export_csv(self):
        if not self.history:
            messagebox.showinfo("No data", "Complete a quiz before exporting.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="quiz_history.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Name", "Category", "Difficulty", "Score", "Total", "Accuracy (%)", "Time (seconds)"])
            for h in self.history:
                writer.writerow([h["date"], h["name"], h["category"], h["difficulty"], h["score"], h["total"], h["percentage"], h["elapsed_seconds"]])
        messagebox.showinfo("Export complete", f"Saved to:\n{path}")

    def show_history(self):
        self.clear_body()
        self.heading("Quiz History", "Your previous attempts are saved on this laptop.")
        if not self.history:
            tk.Label(self.body, text="No quiz attempts saved yet.", bg="#f3f5fb",
                     fg="#6b7280", font=("Segoe UI", 12)).pack(anchor="w")
            return
        frame = tk.Frame(self.body, bg="#f3f5fb")
        frame.pack(fill="both", expand=True)
        cols = ("date", "name", "category", "score", "accuracy")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for col, label, width in [
            ("date", "Date", 140), ("name", "Name", 110), ("category", "Category", 180),
            ("score", "Score", 90), ("accuracy", "Accuracy", 100)
        ]:
            tree.heading(col, text=label)
            tree.column(col, width=width, anchor="w")
        for h in reversed(self.history):
            tree.insert("", "end", values=(h["date"], h["name"], h["category"],
                                           f'{h["score"]}/{h["total"]}', f'{h["percentage"]}%'))
        tree.pack(fill="both", expand=True)
        buttons = tk.Frame(self.body, bg="#f3f5fb")
        buttons.pack(fill="x", pady=12)
        ttk.Button(buttons, text="Export summary to CSV", command=self.export_csv).pack(side="left")
        ttk.Button(buttons, text="Clear History", command=self.clear_history).pack(side="left", padx=8)

    def clear_history(self):
        if messagebox.askyesno("Clear history", "Delete all saved quiz attempts?"):
            self.history = []
            write_history(self.history)
            self.show_history()

    def show_about(self):
        self.clear_body()
        self.heading("About QuizMaster", "Project for Python Programming for AI & Data Science")
        content = (
            "OBJECTIVE\n"
            "QuizMaster helps learners practise quizzes and review their performance.\n\n"
            "TECHNOLOGIES\n"
            "Python 3.14, Tkinter (built into standard Python), JSON, and CSV.\n\n"
            "FEATURES\n"
            "• Multiple categories and difficulty levels\n"
            "• Random questions and timed quiz\n"
            "• Automatic scoring and answer explanations\n"
            "• Saved quiz history\n"
            "• Accuracy summaries and weak-topic analysis\n"
            "• CSV export\n\n"
            "WEAK-TOPIC METHOD\n"
            "The app calculates the percentage of correct answers for each topic. "
            "Topics below 60% are suggested for extra practice. This is a rule-based "
            "heuristic, not a trained AI model.\n\n"
            "PRIVACY\n"
            "Quiz history is saved in data/quiz_history.json on this computer. "
            "No paid API, login, or internet connection is required after setup.\n\n"
            "NOTE\n"
            "This is an educational prototype. Expand and review the question bank "
            "before using it for formal assessments."
        )
        box = tk.Label(self.body, text=content, bg="white", fg="#1f2937",
                       justify="left", anchor="nw", padx=20, pady=18,
                       font=("Segoe UI", 11), wraplength=800)
        box.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizMaster(root)
    root.mainloop()
