# Smart Quiz App 🎯

A Python-based desktop quiz application developed as part of the **Python Programming for AI & Data Science** industrial training through YBI Foundation.

Smart Quiz App provides an interactive learning experience with multiple quiz categories, difficulty levels, automatic scoring, timer-based quizzes, quiz history, and performance analysis.

---

## 🚀 Features

- Multiple quiz categories: Python, Data Science, Artificial Intelligence, and Aptitude.
- Easy and Medium difficulty levels.
- Timer-based quizzes.
- Automatic answer checking and score calculation.
- Answer explanations.
- Quiz history tracking.
- Performance summaries and analytics.
- Weak-topic analysis based on previous quiz results.
- Export quiz results to CSV.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.14 | Core application development |
| Tkinter | Graphical User Interface |
| JSON | Local data storage |
| CSV | Exporting quiz results |
| VS Code | Code editing and development |

The application uses Python's standard library and does not require paid APIs or external Python packages.

---

## 📋 Prerequisites

Before installing the project, make sure you have:

1. Windows 10 or Windows 11.
2. Python 3.14 installed.
3. Visual Studio Code installed.
4. Git installed (optional, for cloning the repository).

## 💻 Installation and Setup

### Step 1: Install Python

1. Visit https://www.python.org/downloads/
2. Download Python 3.14.
3. Run the installer.
4. Make sure to enable **Add Python to PATH** during installation.
5. Complete the installation.

Verify Python installation by opening Command Prompt and running:

```bash
py --version
```

### Step 2: Install Visual Studio Code

1. Visit https://code.visualstudio.com/
2. Download Visual Studio Code for Windows.
3. Install and open VS Code.
4. Open the Extensions section.
5. Search for **Python**.
6. Install the official Python extension by Microsoft.

### Step 3: Download the Project

**Option A: Download ZIP**

1. Open this GitHub repository.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted project folder.

**Option B: Clone using Git**

Open Command Prompt or the VS Code terminal and run:

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Quiz-App.git
```

Navigate into the downloaded folder:

```bash
cd Smart-Quiz-App
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 4: Open the Project in VS Code

1. Open Visual Studio Code.
2. Click **File → Open Folder**.
3. Select the extracted `Smart-Quiz-App` project folder.
4. Click **Select Folder**.
5. If VS Code asks whether you trust the folder, select **Trust** if it is your downloaded project.

You should now see the project files in the Explorer panel.

### Step 5: Open the VS Code Terminal

1. Click **Terminal** in the top menu.
2. Select **New Terminal**.
3. Make sure the terminal is opened in the folder containing `app.py`.

Alternatively, use the shortcut:

```text
Ctrl + Shift + `
```

### Step 6: Run the Application

Run the following command:

```bash
py app.py
```

Alternatively:

```bash
python app.py
```

The Smart Quiz App graphical interface should open in a separate window.

---

## 📂 Project Structure

```text
Smart-Quiz-App/
│
├── app.py
├── data/
│   └── quiz_history.json
├── PROJECT_REPORT.md
├── README.md
└── requirements.txt
```

**File descriptions:**

- `app.py` – Main Python application containing the quiz logic and GUI.
- `data/` – Stores local quiz history and related data.
- `PROJECT_REPORT.md` – Project documentation.
- `README.md` – Project overview and installation guide.
- `requirements.txt` – Dependency information.

## 📊 Performance Analysis

The application uses saved quiz history to review previous attempts, summarise performance, and identify topics where users need more practice.

Weak-topic analysis is based on recorded quiz performance using rule-based logic.

## 🔮 Future Scope

- Add more quiz categories and questions.
- Introduce additional difficulty levels.
- Add user accounts and personalised dashboards.
- Integrate a database for improved data management.
- Introduce more advanced personalised learning recommendations.

## 👨‍💻 Developer

**Lavanya**  
B.Tech – Artificial Intelligence and Data Science

## 🙏 Acknowledgement

Developed as part of the Python Programming for AI & Data Science industrial training through YBI Foundation.

---

⭐ If you find this project useful, feel free to explore the repository!
