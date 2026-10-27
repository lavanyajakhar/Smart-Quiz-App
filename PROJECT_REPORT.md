# Project Report: QuizMaster — Smart Quiz Application

## Abstract
QuizMaster is a desktop quiz application implemented in Python. It supports multiple-choice quizzes, a timer, automatic scoring, answer explanations, quiz history, performance summaries, and weak-topic analysis. It is designed to run with Python 3.14 and the standard library, without third-party package installation or paid APIs.

## Problem Statement
Learners often practise questions without recording progress or identifying topics that require more practice. QuizMaster provides quiz practice and stores results so learners can review performance over time.

## Objectives
- Offer quizzes in multiple categories and difficulty levels.
- Track time and calculate quiz results.
- Explain correct answers after submission.
- Store and review earlier attempts.
- Summarize accuracy and identify lower-performing topics.
- Keep installation simple for beginner users.

## Technology Used
- Python 3.14: application logic and data structures.
- Tkinter: graphical user interface.
- JSON: local storage for quiz history.
- CSV: export quiz summaries.

## Modules
1. Quiz setup and filtering.
2. Question bank and random question selection.
3. Timer and answer collection.
4. Scoring and answer review.
5. Local quiz history.
6. Performance analytics.
7. Weak-topic analysis and CSV export.

## Methodology
The app filters questions by category and difficulty, randomly selects a set, and records the user's answers. After submission, selected answers are compared with the answer key. Results are saved to a local JSON file. Accuracy for each topic is calculated as correct answers divided by attempted questions multiplied by 100. Topics below 60% are suggested for extra practice.

## Testing Checklist
- [ ] Start a quiz in each category.
- [ ] Check that answers can be selected and changed.
- [ ] Submit a quiz and manually verify the score.
- [ ] Confirm explanations appear after submission.
- [ ] Complete multiple attempts and check history.
- [ ] Confirm weak-topic statistics update.
- [ ] Export a CSV summary.
- [ ] Restart the app and confirm history remains.

## Limitations
The question bank is small and intended for demonstration. The application is a local single-user prototype, not a secure examination platform. The weak-topic rule is a simple heuristic and not a trained machine-learning model.

## Future Scope
A larger question bank, user profiles, a database, additional question formats, and optional ML-based personalization could be added later.

## Conclusion
QuizMaster demonstrates a practical Python application using a graphical interface, file handling, timers, scoring, and simple learning analytics. Its standard-library implementation makes it easy to run on Python 3.14.
