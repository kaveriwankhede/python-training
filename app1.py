from click import core, prompt
from unicodedata import name
from flask.cli import load_dotenv
from flask import Flask, abort , render_template ,request ,flash ,redirect ,url_for ,session
from Database import DB_PATH, get_db, init_db
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import sqlite3
import time

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))  # Load environment variables from .env file

app = Flask(__name__) # create a flask application

app.secret_key='linkkiwi2026' #needed for flashing message

#path of database for photo upload
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist

def allowed_file(filename):
    #only allow certain file extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#=================================> Dictionary for Web Development <=================================

QUESTIONS = [
    {
        "q": "Q1. What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Transfer Markup Language",
            "Home Tool Markup Language"
        ],
        "answer": "Hyper Text Markup Language"
    },
    {
        "q": "Q2. Which HTML tag is used to create a hyperlink?",
        "options": ["<a>", "<link>", "<href>", "<url>"],
        "answer": "<a>"
    }
]

#=================================> Dictionary for AI <=================================

QUESTIONS1 = [
    {
        "q": "Q1. What does AI stand for?",
        "options": [
            "Artificial Intelligence",
            "Automatic Intelligence",
            "Advanced Internet",
            "Artificial Internet"
        ],
        "answer": "Artificial Intelligence"
    },
    {
        "q": "Q2. Which of the following is a branch of AI?",
        "options": [
            "Machine Learning",
            "Web Hosting",
            "Networking",
            "Cloud Storage"
        ],
        "answer": "Machine Learning"
    }
]

#=================================> Dictionary for Data Science <=================================

QUESTIONS2 = [
    {
        "q": "Q1. What is Data Science?",
        "options": [
            "Study of data to gain insights",
            "Web Development",
            "Computer Networking",
            "Operating System"
        ],
        "answer": "Study of data to gain insights"
    },
    {
        "q": "Q2. Which language is most popular in Data Science?",
        "options": [
            "Python",
            "HTML",
            "CSS",
            "PHP"
        ],
        "answer": "Python"
    }
]

#=================================> Dictionary for Cloud Computing <=================================

QUESTIONS3 = [
    {
        "q": "Q1. What is Cloud Computing?",
        "options": [
            "Delivering computing services over the Internet",
            "Building websites",
            "Creating databases",
            "Computer repair"
        ],
        "answer": "Delivering computing services over the Internet"
    },
    {
        "q": "Q2. Which of the following is a Cloud Service Provider?",
        "options": [
            "AWS",
            "HTML",
            "CSS",
            "Bootstrap"
        ],
        "answer": "AWS"
    }
]

#=================================> Dictionary for Cyber Security <=================================

QUESTIONS4 = [
    {
        "q": "Q1. What is Cyber Security?",
        "options": [
            "Protecting systems and data from cyber attacks",
            "Creating websites",
            "Building databases",
            "Computer manufacturing"
        ],
        "answer": "Protecting systems and data from cyber attacks"
    },
    {
        "q": "Q2. What is a Virus?",
        "options": [
            "A malicious software",
            "A programming language",
            "A web browser",
            "A database"
        ],
        "answer": "A malicious software"
    }
]

#=================================> Dictionary for Mobile App Development <=================================

QUESTIONS5 = [
    {
        "q": "Q1. What is Mobile App Development?",
        "options": [
            "Creating applications for mobile devices",
            "Building computer hardware",
            "Managing databases",
            "Creating networks"
        ],
        "answer": "Creating applications for mobile devices"
    },
    {
        "q": "Q2. Which operating system is used by Android devices?",
        "options": [
            "Android",
            "iOS",
            "Windows",
            "Linux"
        ],
        "answer": "Android"
    }
]

#=================================> Dictionary for C <=================================

QUESTIONS_C = [
    {
        "q": "Q1. Who is known as the father of C language?",
        "options": [
            "Dennis Ritchie",
            "Bjarne Stroustrup",
            "James Gosling",
            "Guido van Rossum"
        ],
        "answer": "Dennis Ritchie"
    },
    {
        "q": "Q2. In which year was C language developed?",
        "options": [
            "1972",
            "1985",
            "1995",
            "2000"
        ],
        "answer": "1972"
    }
]

#=================================> Dictionary for C++ <=================================

QUESTIONS_CPP = [
    {
        "q": "Q1. Who developed C++ language?",
        "options": [
            "Bjarne Stroustrup",
            "Dennis Ritchie",
            "James Gosling",
            "Guido van Rossum"
        ],
        "answer": "Bjarne Stroustrup"
    },
    {
        "q": "Q2. C++ is an extension of which language?",
        "options": [
            "C",
            "Java",
            "Python",
            "Assembly"
        ],
        "answer": "C"
    }
]

#=================================> Dictionary for Java <=================================

QUESTIONS_JAVA = [
    {
        "q": "Q1. Who developed Java programming language?",
        "options": [
            "James Gosling",
            "Dennis Ritchie",
            "Bjarne Stroustrup",
            "Guido van Rossum"
        ],
        "answer": "James Gosling"
    },
    {
        "q": "Q2. Java was developed at which company?",
        "options": [
            "Sun Microsystems",
            "Microsoft",
            "Google",
            "Apple"
        ],
        "answer": "Sun Microsystems"
    }
]

#=================================> Dictionary for Python <=================================

QUESTIONS_PYTHON = [
    {
        "q": "Q1. Who developed Python language?",
        "options": [
            "Guido van Rossum",
            "Dennis Ritchie",
            "James Gosling",
            "Bjarne Stroustrup"
        ],
        "answer": "Guido van Rossum"
    },
    {
        "q": "Q2. Python is which type of language?",
        "options": [
            "Interpreted language",
            "Compiled language",
            "Machine language",
            "Assembly language"
        ],
        "answer": "Interpreted language"
    }

]

#=================================> Dictionary for Mobile Operating System <=================================

QUESTIONS_OS = [
    {
        "q": "Q1. What is an Operating System?",
        "options": [
            "System software that manages hardware and software",
            "A programming language",
            "A web browser",
            "A database system"
        ],
        "answer": "System software that manages hardware and software"
    },
    {
        "q": "Q2. Which of the following is an Operating System?",
        "options": [
            "Windows",
            "Java",
            "HTML",
            "MySQL"
        ],
        "answer": "Windows"
    }
]

#=================================> Dictionary for DBMS <=================================

QUESTIONS_DBMS = [
    {
        "q": "Q1. What is DBMS?",
        "options": [
            "Software to manage and store data",
            "Programming language",
            "Operating system",
            "Web browser"
        ],
        "answer": "Software to manage and store data"
    },
    {
        "q": "Q2. Which of the following is a DBMS?",
        "options": [
            "MySQL",
            "Java",
            "Linux",
            "HTML"
        ],
        "answer": "MySQL"
    }
]

#=================================> Dictionary for Computer Network <=================================

QUESTIONS_CN = [
    {
        "q": "Q1. What is a computer network?",
        "options": [
            "A system of connected computers to share data",
            "A type of software",
            "A programming language",
            "A database system"
        ],
        "answer": "A system of connected computers to share data"
    },
    {
        "q": "Q2. What does LAN stand for?",
        "options": [
            "Local Area Network",
            "Large Area Network",
            "Light Access Network",
            "Logical Area Network"
        ],
        "answer": "Local Area Network"
    }
]

#=================================> Dictionary for Data Structure <=================================

QUESTIONS_DS = [
    {
        "q": "Q1. What is a data structure?",
        "options": [
            "A way to organize and store data",
            "A programming language",
            "An operating system",
            "A database software"
        ],
        "answer": "A way to organize and store data"
    },
    {
        "q": "Q2. Which data structure follows LIFO principle?",
        "options": [
            "Stack",
            "Queue",
            "Array",
            "Tree"
        ],
        "answer": "Stack"
    }
]

#=================================> Dictionary for Student  <=================================

stud = [
    {
        'Sr_no':1,
        'Name':'John Doe',
        'username':'John',
        'email':'John@gmail.com',
        'password':'John@1234'
    },
    {
        'Sr_no':2,
        'Name':'Jane smith',
        'username':'Jone',
        'email':'Jane@gmail.com',
        'password':'Jone@1234'
    }
]

#==================================> Home Route <=================================

@app.route('/')
def Home():
    return render_template('Home.html',students=stud)
    
#==================================> Login Route <=================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db()

        user = conn.execute(
            """
            SELECT * FROM USERS
            WHERE Username = ?
            """,
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["Password"], password):

            session["Student_name"] = user["Student_name"]
            session["Username"] = user["Username"]
            session["Email"] = user["Email"]
            session["Password"] = user["Password"]
            session["role"] = user["role"]

            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))

        else:
            flash("Invalid Username or Password!", "danger")

    return render_template("login.html")

#==================================> Forget Password Route <=================================

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM USERS WHERE Username=? AND Email=?",
            (username, email)
        ).fetchone()

        if user:

            hashed_password = generate_password_hash(new_password)

            conn.execute(
                "UPDATE USERS SET Password=? WHERE Username=?",
                (hashed_password, username)
            )

            conn.commit()

            flash('Password Updated Successfully!', 'success')

            conn.close()

            return redirect(url_for('login'))

        else:

            conn.close()

            flash('Invalid Username or Email!', 'danger')

            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

#==================================> Explore Technology Route <=================================

@app.route('/explore_technology')
def explore_technology():
    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    if 'sr_no' in session:
        return redirect(url_for('explore_technology'))

    
    return render_template('explore_technology.html')

#==================================> Technology Route <=================================

@app.route('/technology')
def technology():
    return render_template('technology.html')

#==================================> Web Development Route  <=================================

@app.route('/web_development/<int:qno>', methods=['GET', 'POST'])
def web_development(qno):

    session["Subject"] = "Web Development"

    # New timer for every new quiz
    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM QUESTIONS
        WHERE subject = ?
        """,
        ("Web Development",)
    ).fetchall()

    conn.close()

    # Dictionary questions
    all_questions = QUESTIONS.copy()

    # Database questions
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Web Development Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")

        # Save selected answer
        session[f"q{qno}"] = selected

        # Next Question
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("web_development", qno=qno + 1))

        # Previous Question
        if "prev" in request.form and qno > 0:
            return redirect(url_for("web_development", qno=qno - 1))

        # Submit Quiz
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score


            # Calculate Time Taken
            end_time = time.time()
            elapsed = int(end_time - session["start_time"])

            minutes = elapsed // 60
            seconds = elapsed % 60

            session["time_taken"] = f"{minutes} min {seconds} sec"

            return redirect(url_for("Result"))

    return render_template(
        "web_development.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session["start_time"]
    )

#==================================> Artificial Intelligrnce Route  <=================================

@app.route('/Artificial_Intelligence/<int:qno>', methods=['GET', 'POST'])
def Artificial_Intelligence(qno):

    session["Subject"] = "Artificial Intelligence"   # Subject nusar change kara

    if qno == 0:
        session["start_time"] = time.time()
    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM QUESTIONS
        WHERE subject = ?
        """,
        ("Artificial Intelligence",)
    ).fetchall()

    conn.close()

    # Dictionary questions
    all_questions = QUESTIONS1.copy()

    # Database questions
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Artificial Intelligence Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")

        # Save selected answer
        session[f"q{qno}"] = selected

        # Next Question
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("Artificial_Intelligence", qno=qno + 1))

        # Previous Question
        if "prev" in request.form and qno > 0:
            return redirect(url_for("Artificial_Intelligence", qno=qno - 1))

        # Submit Quiz
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "Artificial_Intelligence.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session["start_time"]
    )

#==================================> Data Science Route  <=================================

@app.route('/data_science/<int:qno>', methods=['GET', 'POST'])
def data_science(qno):

    # Subject save
    session["Subject"] = "Data Science"

    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM QUESTIONS
        WHERE subject = ?
        """,
        ("Data Science",)
    ).fetchall()

    conn.close()

    # Dictionary questions
    all_questions = QUESTIONS2.copy()

    # Database questions
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Data Science Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")

        # Save selected answer
        session[f"q{qno}"] = selected

        # Next Question
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("data_science", qno=qno + 1))

        # Previous Question
        if "prev" in request.form and qno > 0:
            return redirect(url_for("data_science", qno=qno - 1))

        # Submit Quiz
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "data_science.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session["start_time"]
    )

#==================================> Cloude Computing Route  <=================================

@app.route('/cloud_computing/<int:qno>', methods=['GET', 'POST'])
def cloud_computing(qno):

    session["Subject"] = "Cloud Computing"   # Subject nusar change kara

    # New timer for every new quiz
   
    if qno == 0:
        session["start_time"] = time.time()
    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM QUESTIONS
        WHERE subject = ?
        """,
        ("Cloud Computing",)
    ).fetchall()

    conn.close()

    # Dictionary questions
    all_questions = QUESTIONS3.copy()

    # Database questions
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Cloud Computing Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")

        # Save selected answer
        session[f"q{qno}"] = selected

        # Next Question
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("cloud_computing", qno=qno + 1))

        # Previous Question
        if "prev" in request.form and qno > 0:
            return redirect(url_for("cloud_computing", qno=qno - 1))

        # Submit Quiz
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "cloud_computing.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session["start_time"]
    )

#==================================> Cyber Security Route  <=================================

@app.route('/cyber_security/<int:qno>', methods=['GET', 'POST'])
def cyber_security(qno):

    # Subject save
    session["Subject"] = "Cyber Security"

    # Timer start only once
    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Cyber Security",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS4.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Cyber Security Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("cyber_security", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("cyber_security", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "cyber_security.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Mobile App Development Route  <=================================

@app.route('/mobile_app_development/<int:qno>', methods=['GET', 'POST'])
def Mobile_App_Development(qno):

    # Subject save
    session["Subject"] = "Mobile App Development"

    if "start_time" not in session:
        session["start_time"] = time.time() 

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Mobile_App_Development",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS5.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Mobile App Development Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")

        session[f"q{qno}"] = selected

        # NEXT
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("Mobile_App_Development", qno=qno + 1))

        # PREVIOUS
        if "prev" in request.form and qno > 0:
            return redirect(url_for("Mobile_App_Development", qno=qno - 1))

        # SUBMIT
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "Mobile_App_Development.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Explore Programming Language Route  <=================================

@app.route('/explore_programing_lang')
def explore_programing_lang():

    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    
    if 'sr_no' in session:
        return redirect(url_for('programing_lang'))
    
        
    return render_template('programing_lang.html')

#==================================> C Language Route  <=================================

@app.route('/c_lang/<int:qno>', methods=['GET', 'POST'])
def c_lang(qno):

    # Subject save
    session["Subject"] = "C"

    if qno== 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("C",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_C.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No C Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("c_lang", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("c_lang", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "c_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> CPP Language Route  <=================================

@app.route('/cpp_lang/<int:qno>', methods=['GET', 'POST'])
def cpp_lang(qno):

    # Subject save
    session["Subject"] = "C++"      

    # Timer start only once
    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("C++",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_CPP.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No C++ Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("cpp_lang", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("cpp_lang", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "cpp_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Java Language Route  <=================================

@app.route('/java_lang/<int:qno>', methods=['GET', 'POST'])
def java_lang(qno):

    # Subject save
    session["Subject"] = "Java"

    # Timer start only once
    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Java",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_JAVA.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Java Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("java_lang", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("java_lang", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "java_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Python Language Route  <=================================

@app.route('/python_lang/<int:qno>', methods=['GET', 'POST'])
def python_lang(qno):

    # Subject save
    session["Subject"] = "Python"

    if qno == 0:
        session["start_time"] = time.time()

    # Database madhun Python questions ghya
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Python",)
    ).fetchall()

    conn.close()

    # Pahile dictionary madhle questions
    all_questions = QUESTIONS_PYTHON.copy()

    # Database madhle questions add kara
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    # Questions nasel tar
    if len(all_questions) == 0:
        return "<h2>No Python Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    # POST Request
    if request.method == "POST":

        selected = request.form.get("answer")

        # User answer save kara
        session[f"q{qno}"] = selected

        # Next button
        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("python_lang", qno=qno + 1))

        # Previous button
        if "prev" in request.form and qno > 0:
            return redirect(url_for("python_lang", qno=qno - 1))

        # Submit button
        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "python_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Explore Computer Science Route  <=================================

@app.route('/explore_computer_science')
def explore_computer_science():

    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
        
    if 'sr_no' in session:
        return redirect(url_for('computer_science'))
        
            
    return render_template('computer_science.html')

#==================================> Operating System Route  <=================================

@app.route('/operating_system/<int:qno>', methods=['GET', 'POST'])
def operating_system(qno):
    # Subject save  
    session["Subject"] = "Operating System"

    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Operating System",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_OS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Operating System Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("operating_system", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("operating_system", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "operating_system.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> DBMS Route  <=================================

@app.route('/dbms_lang/<int:qno>', methods=['GET', 'POST'])
def dbms_lang(qno):

    # Subject save
    session["Subject"] = "DBMS"

    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("DBMS",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_DBMS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No DBMS Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("dbms_lang", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("dbms_lang", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "dbms_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),   
        start_time=session.get("start_time")
    )

#==================================> Computer Network Route  <=================================

@app.route('/computer_network/<int:qno>', methods=['GET', 'POST'])
def computer_network(qno):
    # Subject save
    session["Subject"] = "Computer Network"

    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Computer Network",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_CN.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Computer Network Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("computer_network", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("computer_network", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "computer_network.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Data Structure Route  <=================================

@app.route('/data_structure/<int:qno>', methods=['GET', 'POST'])
def data_structure(qno):
    # Subject save
    session["Subject"] = "Data Structure"

    if qno == 0:
        session["start_time"] = time.time()

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Data Structure",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_DS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Data Structure Questions Found!</h2>"

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("data_structure", qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("data_structure", qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "data_structure.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        start_time=session.get("start_time")
    )

#==================================> Logout Route  <=================================

@app.route('/logout')
def logout():

    session.clear()
    session.pop('username', None) 
    session.pop('role', None)
    flash("You have been logged out.", "info")

    return redirect(url_for("Home"))

#==================================> Subjects Route  <=================================

@app.route('/subjects')
def subjects():
    conn = get_db()

    rows = conn.execute("""
        SELECT subjects.name AS subject_name,
               COUNT(SCORE.Sr_no) AS student_count
        FROM subjects
        LEFT JOIN SCORE
            ON subjects.name = SCORE.subject
        GROUP BY subjects.name
        ORDER BY subjects.name
    """).fetchall()

    conn.close()
    return render_template("subjects.html", rows=rows)

#==================================> Update Leaderboard function  <=================================

def update_leaderboard(student_name, score, time):

    conn = get_db()

    old = conn.execute(
        "SELECT * FROM leaderboard WHERE Student_name=?",
        (student_name,)
    ).fetchone()

    if old is None:
        conn.execute(
            "INSERT INTO leaderboard(Student_name, score, time) VALUES (?, ?, ?)",
            (student_name, score, time)
        )
    else:
        
        if score > old["score"] or (score == old["score"] and time < old["time"]):
            conn.execute(
                """
                UPDATE leaderboard
                SET score=?, time=?
                WHERE Student_name=?
                """,
                (score, time, student_name)
            )

    conn.commit()
    conn.close()

#==================================> Rank Leaderboard function  <=================================

def ranked_leaderboard():

    conn = get_db()

    rows = conn.execute("""
     SELECT Student_name,
            MAX(score) AS score,
            MIN(time) AS time
     FROM SCORE
     GROUP BY Student_name
     ORDER BY score DESC, time ASC
     LIMIT 5
     """).fetchall()
    for row in rows:
         print(dict(row))

    conn.close()

    return rows

#==================================> Leaderboard Route  <=================================

@app.route("/leaderboard")
def leaderboard():

    rows = ranked_leaderboard()

    leaderboard_entries = []

    for idx, row in enumerate(rows, start=1):
        leaderboard_entries.append({
            "rank": idx,
            "name": row["Student_name"],
            "score": row["score"],
            "time": row["time"]
        })

    return render_template(
        "leaderboard.html",
        leaderboard_entries=leaderboard_entries,
        students=students
    )

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    
    if request.method == 'POST':

        Student_name = request.form.get('student_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        subject = request.form.get('subject')

        if not Student_name or not username or not email or not password or not subject:
            flash('Please provide all details!', 'danger')
            return redirect(url_for('Register'))

        # Password Hashing
        hashed_password = generate_password_hash(password)
        #Add: handle photo upload
        file = request.files.get('photo')
        filename = 'default.png'  # Default photo
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        

        conn = get_db()

        conn.execute(
        '''
        INSERT INTO USERS
        (Student_name, username, email, password, subject)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (Student_name, username, email, hashed_password, subject)
        )

        conn.commit()
        conn.close()

        flash('Registration Successful!', 'success')
        return redirect(url_for('Register'))

    return render_template('Register.html')


@app.route('/search')
def search():

    q = request.args.get('q', '')
    conn = get_db()

    if q:
        students = conn.execute("""
            SELECT
                MIN(Sr_no) AS Sr_no,
                Student_name,
                Username,
                Email,
                COUNT(*) AS total_attempts
            FROM SCORE
            WHERE Student_name LIKE ?
               OR Username LIKE ?
            GROUP BY Student_name, Username, Email
            ORDER BY Student_name
        """, (f'%{q}%', f'%{q}%')).fetchall()

    else:
        students = conn.execute("""
            SELECT
                MIN(Sr_no) AS Sr_no,
                Student_name,
                Username,
                Email,
                COUNT(*) AS total_attempts
            FROM SCORE
            GROUP BY Student_name, Username, Email
            ORDER BY Student_name
        """).fetchall()

    conn.close()

    return render_template(
        "search.html",
        students=students,
        query=q
    )



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/Add_Question', methods=['GET', 'POST'])
def Add_Question():
    
    if request.method == "POST":

        subject = request.form.get('subject')
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        answer = request.form.get('answer')

        if not subject or not question or not option1 or not option2 or not option3 or not option4 or not answer:
            flash('Please fill all fields!', 'danger')
            return render_template("Add_Question.html")

        conn = get_db()

        conn.execute(
            '''
            INSERT INTO QUESTIONS
            (subject,question, option1, option2, option3, option4, answer)
            VALUES (?,?, ?, ?, ?, ?, ?)
            ''',
            (subject,question, option1, option2, option3, option4, answer)
        )

        conn.commit()
        conn.close()

        flash("Question Added Successfully!", "success")

        return redirect(url_for('Add_Question'))

    return render_template('Add_Question.html')



@app.route("/students")
def students():

    page = request.args.get('page', 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db()

    # Total Students
    total = conn.execute("""
        SELECT COUNT(*)
        FROM USERS
    """).fetchone()[0]

    total_page = (total + per_page - 1) // per_page

    # Current Page Students
    db_students = conn.execute("""
        SELECT *
        FROM USERS
        ORDER BY id ASC
        LIMIT ? OFFSET ?
    """, (per_page, offset)).fetchall()

    combined_students = []

    for s in db_students:

        score_data = conn.execute("""
            SELECT
                MAX(score) AS score,
                COUNT(*) AS total_attempts
            FROM SCORE
            WHERE Username = ?
        """, (s["Username"],)).fetchone()

        combined_students.append({

            "id": s["id"],
            "Name": s["Student_name"],
            "username": s["Username"],
            "email": s["Email"],
            "photo": s["photo"] if "photo" in s.keys() else "default.png",

            "score": score_data["score"] if score_data and score_data["score"] else 0,

            "total_attempts": score_data["total_attempts"] if score_data else 0

        })

    conn.close()

    return render_template(
        "students.html",
        students=combined_students,
        page=page,
        total_page=total_page
    )

@app.route('/filter_result')
def filter_result():

    q = request.args.get('q', '')
    conn = get_db()

    if q:
        students = conn.execute("""
            SELECT
                MIN(Sr_no) AS Sr_no,
                Student_name,
                Username,
                Email,
                MAX(score) AS score,
                COUNT(*) AS total_attempts,
                'score' AS source
            FROM SCORE
            WHERE Student_name LIKE ?
               OR Username LIKE ?
            GROUP BY Student_name, Username, Email
            ORDER BY Student_name
        """, (f'%{q}%', f'%{q}%')).fetchall()

    else:
        students = conn.execute("""
            SELECT
                MIN(Sr_no) AS Sr_no,
                Student_name,
                Username,
                Email,
                MAX(score) AS score,
                COUNT(*) AS total_attempts,
                'score' AS source
            FROM SCORE
            GROUP BY Student_name, Username, Email
            ORDER BY Student_name
        """).fetchall()

    conn.close()

    return render_template(
        "filter_result.html",
        students=students,
        query=q
    )
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    conn= get_db()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    # subjects list - needed to populate the dropdown in the form
    if request.method == 'POST':

        Student_name = request.form.get('student_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        subject = request.form.get('subject')

        if not Student_name or not username or not email or not password or not subject:
            flash('Please provide all details!', 'danger')
            return redirect(url_for('add_student'))

        # Password Hashing
        hashed_password = generate_password_hash(password)

        #Add: handle photo upload
        file = request.files.get('photo')
        filename = 'default.png'  # Default photo
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn.execute(
                '''
                INSERT INTO SCORE
                (Student_name, username, email, password, subject, score, time, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (Student_name, username, email, hashed_password, subject, 0, time.time(), filename)
                )


        conn.execute(
        '''
        INSERT INTO USERS
        (Student_name, username, email, password, subject, score, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (Student_name, username, email, hashed_password, subject, 0, filename)
        )

        conn.commit()
        conn.close()

        flash('Registration Successful!', 'success')
        return redirect(url_for('add_student'))

    return render_template("add_student.html", subjects=subjects)
    

@app.route('/view_student/<int:Sr_no>')
def view_student(Sr_no):
    conn = get_db()
    student = conn.execute("""
            SELECT *
            FROM SCORE
            WHERE Sr_no = ?
        """, (Sr_no,)).fetchone()
    
    highest_score = conn.execute("""
    SELECT MAX(score)
    FROM SCORE
    WHERE Username=?
    """,(student['Username'],)).fetchone()[0]

    total_attempts = conn.execute("""
    SELECT COUNT(*)
    FROM SCORE
    WHERE Username=?
    """,(student['Username'],)).fetchone()[0]
    performance = conn.execute("""

SELECT

subject,

MAX(score) AS highest_score,

COUNT(*) AS attempts

FROM SCORE

WHERE Username=?

GROUP BY subject

ORDER BY highest_score DESC

""",(student['Username'],)).fetchall()
    average_score = conn.execute("""

SELECT ROUND(AVG(score),1)

FROM SCORE

WHERE Username=?

""",(student['Username'],)).fetchone()[0]

    

    
    conn.close()

    return render_template(
        "view_student.html",
        student=student,
        highest_score=highest_score,
        total_attempts=total_attempts,
        tip=None,
        performance=performance,
        average_score=average_score
        )

@app.route('/edit_student/<source>/<int:id>', methods=['GET','POST'])
def edit_student(source, id):

    conn = get_db()

    # ---------------- POST ----------------

    if request.method == "POST":

        student_name = request.form['student_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        subject = request.form['subject']

        if source == "users":

            conn.execute("""
                UPDATE USERS
                SET Student_name=?,
                    Username=?,
                    Email=?,
                    Password=?,
                    Subject=?
                WHERE id=?
            """,
            (
                student_name,
                username,
                email,
                password,
                subject,
                id
            ))

        else:

            conn.execute("""
                UPDATE SCORE
                SET Student_name=?,
                    Username=?,
                    Email=?,
                    Password=?,
                    Subject=?
                WHERE Sr_no=?
            """,
            (
                student_name,
                username,
                email,
                password,
                subject,
                id
            ))

        conn.commit()
        conn.close()

        flash("Student updated successfully!", "success")

        return redirect(url_for("students"))

    # ---------------- GET ----------------

    if source == "users":

        student = conn.execute("""
            SELECT *
            FROM USERS
            WHERE id=?
        """, (id,)).fetchone()

    else:

        student = conn.execute("""
            SELECT *
            FROM SCORE
            WHERE Sr_no=?
        """, (id,)).fetchone()

    conn.close()

    if student is None:

        flash("Student not found!", "danger")

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student,
        source=source
    )

@app.route('/Result')
def Result():

    # Score
    score = session.get("score", 0)

    start = session.get("start_time")

    if start:
        time_taken = int(time.time() - start)
    else:
        time_taken = 0

    print("Start Time :", start)
    print("Current Time:", time.time())
    print("Time Taken :", time_taken)

    # Subject
    subject = session.get("Subject")

    # Dictionary Questions
    if subject == "Artificial Intelligence":
        dictionary_questions = QUESTIONS1
    elif subject == "Web Development":
        dictionary_questions = QUESTIONS
    elif subject == "Data Science":
        dictionary_questions = QUESTIONS2
    elif subject == "Cyber Security":
        dictionary_questions = QUESTIONS3
    elif subject == "Cloud Computing":
        dictionary_questions = QUESTIONS4
    elif subject == "Mobile App Development":
        dictionary_questions = QUESTIONS5
    elif subject == "C":
        dictionary_questions = QUESTIONS_C
    elif subject == "C++":
        dictionary_questions = QUESTIONS_CPP
    elif subject == "Java":
        dictionary_questions = QUESTIONS_JAVA
    elif subject == "Python":
        dictionary_questions = QUESTIONS_PYTHON
    elif subject == "Operating System":
        dictionary_questions = QUESTIONS_OS 
    elif subject == "DBMS":
        dictionary_questions = QUESTIONS_DBMS
    elif subject == "Computer Network":
        dictionary_questions = QUESTIONS_CN
    elif subject == "Data Structure":
        dictionary_questions = QUESTIONS_DS
    else:
        dictionary_questions = []

    all_answers = []

    for q in dictionary_questions:
        all_answers.append({
            "question": q["q"],
            "answer": q["answer"]
        })

    conn = get_db()

    # Save Result
    conn.execute("""
INSERT INTO SCORE
(Student_name, Username, Email, Password, subject, score, time)
VALUES (?, ?, ?, ?, ?, ?, ?)
""",(
    session.get("Student_name"),
    session.get("Username"),
    session.get("Email"),
    session.get("Password"),
    subject,
    score,
    time_taken
))

    conn.commit()

    student = conn.execute(
        "SELECT * FROM SCORE WHERE Username=? ORDER BY Sr_no DESC LIMIT 1",
        (session.get("Username"),)
    ).fetchone()

    # Database Answers
    rows = conn.execute("""
        SELECT question, answer
        FROM QUESTIONS
        WHERE subject=?
    """, (subject,)).fetchall()

    for row in rows:
        all_answers.append({
            "question": row["question"],
            "answer": row["answer"]
        })

    # Leaderboard
    rows = ranked_leaderboard()

    leaderboard_entries = []

    for idx, row in enumerate(rows, start=1):
        leaderboard_entries.append({
            "rank": idx,
            "name": row["Student_name"],
            "score": row["score"],
            "time": row["time"]
        })

    total = len(all_answers)
    if total == 0:
        total = 1

    percentage = round((score / total) * 100, 1)

    conn.close()

    # Quiz khatam hone ke baad timer remove kar do
    session.pop("start_time", None)
    attempt_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        "Result.html",
        student=student,
        score=score,
        total=total,
        percentage=percentage,
        time_taken=time_taken,
        answers=all_answers,
        leaderboard_entries=leaderboard_entries,
        attempt_date=attempt_date
    )

@app.route("/delete/<int:sr_no>")
def delete_student(sr_no):

    conn = get_db()

    conn.execute(
        "DELETE FROM SCORE WHERE Sr_no = ?",
        (sr_no,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("filter_result"))


@app.route("/Theory")
def Theory():
    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
        
    if 'sr_no' in session:
        return redirect(url_for('Theory'))

    search = request.args.get("search", "")
    return render_template("Theory.html", search=search)



@app.route("/students/<int:Sr_no>/tip")
def get_ai_tip(Sr_no):

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM SCORE WHERE Sr_no = ?",
        (Sr_no,)
    ).fetchone()

    conn.close()

    if students is None:
        abort(404)

    prompt = f"""
Student Name: {students['Student_name']}
Marks: {students['score']}/100
Subject: {students['subject']}

Please provide practical study tips.
The response should not be more than 3 lines.
"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    tip = response.choices[0].message.content
    
    return render_template(
        "get_ai_tip.html",
        student=students,
        tip=tip
    )

@app.route("/ai_doubt_solver", methods=["GET", "POST"])
def ai_doubt_solver():

    answer = ""

    if request.method == "POST":

        subject = request.form["subject"]
        question = request.form["question"]

        prompt = f"""
Subject: {subject}

Question: {question}

Explain for a beginner.

Rules:
- Use short points.
- Use headings.
- Keep each point on a new line.
- Do NOT write long paragraphs.
- Use bullets.
- Give one example.
- If programming, include code and output.
"""

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content
            
            

            conn = sqlite3.connect("/home/kaveriwankhede/python-training/myproject.db")
            print("Current Directory:", os.getcwd())
            print("Database Used:", os.path.abspath("myproject.db"))

            cur = conn.cursor()

            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            print("Tables:", cur.fetchall())

            cur.execute("""
            INSERT INTO ai_history(username, subject, question, answer, date)
            VALUES (?, ?, ?, ?, ?)
            """, (
                session.get("username", "Guest"),
                subject,
                question,
                answer,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            answer = str(e)
    
    return render_template(
        "ai_doubt_solver.html",
        answer=answer
    )

@app.route("/ai_history")
def ai_history():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM ai_history
        WHERE username=?
        ORDER BY id DESC
    """, (session.get("username", "Guest"),))

    history = cur.fetchall()

    conn.close()

    return render_template(
        "ai_history.html",
        history=history
    )

@app.route("/website_guide")
def website_guide():

    WEBSITE_GUIDE_PROMPT = """
You are the AI Assistant of Study Quiz Hub.

Explain this website to a first-time visitor in detail.

Include:
- Welcome message
- Purpose of the website
- All main features
- Step-by-step roadmap (Register → Login → Explore Technology → Read Notes → Quiz → AI Quiz → Result → AI Tips → Leaderboard → Dashboard)
- Explain each step clearly.
- Give study tips and motivational advice.
- Answer common beginner questions.
- Use attractive headings, emojis, and simple English.

Generate a detailed, professional response of about 700-1000 words.
"""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": WEBSITE_GUIDE_PROMPT
            }
        ]
    )

    guide = response.choices[0].message.content

    return render_template(
        "website_guide.html",
        guide=guide
    )

@app.route("/dashboard")
def dashboard():

    conn = get_db()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM USERS"
    ).fetchone()[0]

    total_subjects = conn.execute(
        "SELECT COUNT(DISTINCT subject) FROM notes"
    ).fetchone()[0]

    total_quiz = conn.execute(
        "SELECT COUNT(*) FROM SCORE"
    ).fetchone()[0]

    highest = conn.execute(
        "SELECT MAX(score) FROM SCORE"
    ).fetchone()[0]

    average = conn.execute(
        "SELECT ROUND(AVG(score),2) FROM SCORE"
    ).fetchone()[0]

    recent = conn.execute("""
SELECT s.Student_name,
       s.subject,
       s.score,
       s.time
FROM SCORE s
INNER JOIN (
    SELECT Student_name, MAX(Sr_no) AS last_id
    FROM SCORE
    GROUP BY Student_name
) latest
ON s.Student_name = latest.Student_name
AND s.Sr_no = latest.last_id
ORDER BY s.Sr_no DESC
LIMIT 5
""").fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_subjects=total_subjects,
        total_quiz=total_quiz,
        highest=highest,
        average=average,
        recent=recent
    )



@app.route("/profile")
def profile():

    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM USERS
        WHERE Username = ?
    """, (session["Username"],)).fetchone()

    conn.close()

    if user is None:
        flash("User not found!", "danger")
        return redirect(url_for("login"))

    return render_template("profile.html", student=user)


@app.route("/certificate")
def certificate():

    conn = get_db()

    student = conn.execute("""
        SELECT Student_name, subject, score
        FROM score
        ORDER BY Sr_no DESC
        LIMIT 1
    """).fetchone()

    conn.close()

    return render_template("certificate.html", student=student)

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db()

        conn.execute("""
            INSERT INTO contact(name, email, message)
            VALUES (?, ?, ?)
        """, (name, email, message))

        conn.commit()
        conn.close()

        flash("Message sent successfully!", "success")

        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/contact_messages")
def contact_messages():

    conn = get_db()

    messages = conn.execute(
        "SELECT * FROM contact ORDER BY id DESC"
    ).fetchall()

    feedbacks = conn.execute(
        "SELECT * FROM feedback ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "contact_messages.html",
        messages=messages,
        feedbacks=feedbacks
    )

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":

        name = request.form.get("name")
        rating = request.form.get("rating")
        message = request.form.get("message")

        conn = get_db()

        conn.execute("""
            INSERT INTO feedback (name, rating, message)
            VALUES (?, ?, ?)
        """, (name, rating, message))

        conn.commit()
        conn.close()

        flash("Thank you for your feedback!", "success")

        return redirect(url_for("feedback"))

    return render_template("feedback.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/interview")
def interview():
    # Login check
    if "Username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    
    if 'sr_no' in session:
        return redirect(url_for('interview'))

    conn = get_db()

    category = request.args.get("category")
    subject = request.args.get("subject")
    difficulty = request.args.get("difficulty")
    search = request.args.get("search")

    query = "SELECT * FROM interview_questions WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if subject:
        query += " AND subject = ?"
        params.append(subject)

    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)

    if search:
        query += " AND question LIKE ?"
        params.append("%" + search + "%")

    questions = conn.execute(query, params).fetchall()

    conn.close()

    return render_template(
        "interview.html",
        questions=questions
    )

@app.route("/add_interview_question", methods=["GET", "POST"])
def add_interview_question():

    if request.method == "POST":

        category = request.form["category"]
        subject = request.form["subject"]
        difficulty = request.form["difficulty"]
        question = request.form["question"]
        answer = request.form["answer"]

        conn = get_db()

        conn.execute("""
        INSERT INTO interview_questions
        (category, subject, difficulty, question, answer)
        VALUES (?, ?, ?, ?, ?)
        """, (
            category,
            subject,
            difficulty,
            question,
            answer
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("interview"))

    return render_template("add_interview_question.html")
import json
@app.route("/Settings", methods=["GET", "POST"])
def Settings():

    if "Username" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM USERS
        WHERE Username = ?
    """, (session["Username"],)).fetchone()

    if request.method == "POST":

        student_name = request.form["Student_name"]
        email = request.form["Email"]

        conn.execute("""
            UPDATE USERS
            SET Student_name = ?, Email = ?
            WHERE Username = ?
        """, (
            student_name,
            email,
            session["Username"]
        ))

        conn.commit()

        session["Student_name"] = student_name
        session["Email"] = email

        return redirect(url_for("Settings"))

    conn.close()
    return render_template(
        "Settings.html"
    )




@app.route("/ai_quiz/<subject>/<int:qno>", methods=["GET", "POST"])
def ai_quiz(subject, qno):

   
    if "start_time" not in session:
        session["start_time"] = int(time.time())

    all_questions = session.get("ai_questions", [])

    if len(all_questions) == 0:
        return redirect(url_for("generate_ai_quiz", subject=subject))

    if request.method == "POST":

        selected = request.form.get("answer")
        session[f"q{qno}"] = selected

        if "next" in request.form and qno < len(all_questions) - 1:
            return redirect(url_for("ai_quiz",
                                    subject=subject,
                                    qno=qno + 1))

        if "prev" in request.form and qno > 0:
            return redirect(url_for("ai_quiz",
                                    subject=subject,
                                    qno=qno - 1))

        if "submit" in request.form:

            score = 0

            for i in range(len(all_questions)):
                if session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            session["score"] = score

            return redirect(url_for("Result"))

    return render_template(
        "ai_quiz.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions),
        subject=subject,
        start_time=session["start_time"]
    )

@app.route("/generate_ai_quiz/<subject>", methods=["GET", "POST"])
def generate_ai_quiz(subject):

    prompt = f"""
Generate exactly 10 multiple choice questions on "{subject}".

Rules:
1. Return ONLY valid JSON.
2. Do NOT write explanations.
3. Do NOT use markdown.
4. Do NOT use ```json.
5. Do NOT add any text before or after the JSON.
6. Escape any double quotes inside strings.
7. Each question must have exactly 4 options.

Return in this exact format:

[
  {{
    "q": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }}
]
"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    ai_response = response.choices[0].message.content.strip()

    ai_response = ai_response.replace("```json","").replace("```","").strip()

    try:
        session["ai_questions"] = json.loads(ai_response)

    except json.JSONDecodeError as e:
        print("JSON ERROR:", e)
        print("AI Response:")
        print(ai_response)

        return f"""
        <h2>Invalid JSON Returned by AI</h2>
        <pre>{ai_response}</pre>

    session["ai_questions"] = json.loads(ai_response)
    session["Subject"] = subject
    session["score"] = 0
    session["start_time"] = time.time()
    """

    return redirect(url_for("ai_quiz", qno=0, subject=subject))

@app.route("/quiz_history")
def quiz_history():

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect("/")

    conn = get_db()

    history = conn.execute("""
        SELECT username,
               subject,
               topic,
               question,
               user_answer,
               correct_answer,
               is_correct
        FROM QUIZ_HISTORY
        ORDER BY id DESC
    """).fetchall()

    total = len(history)
    correct = sum(row["is_correct"] for row in history)
    wrong = total - correct

    conn.close()

    return render_template(
        "quiz_history.html",
        history=history,
        total=total,
        correct=correct,
        wrong=wrong
    )

@app.route("/wrong_questions/<attempt_date>")
def wrong_questions(attempt_date):

    Username = session["Username"]

    conn = get_db()

    wrong_questions = conn.execute("""
        SELECT question,
               user_answer,
               correct_answer,
               attempt_date
        FROM QUIZ_HISTORY
        WHERE username=?
        AND attempt_date=?
        AND is_correct=0
    """,(Username,attempt_date)).fetchall()

    conn.close()

    return render_template(
        "wrong_questions.html",
        wrong_questions=wrong_questions
    )

@app.route("/personalized_quiz")
def personalized_quiz():

    

    if "Username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    conn = get_db()

    wrong = conn.execute("""
        SELECT question
        FROM QUIZ_HISTORY
        WHERE username = ?
        AND is_correct = 0
    """, (session["Username"],)).fetchall()

    conn.close()

    if not wrong:
        return "<h2>No Wrong Questions Found!</h2>"

    questions = "\n".join([row["question"] for row in wrong])

    prompt = f"""
Student answered these questions incorrectly:

{questions}

Generate 10 NEW MCQs related to these questions.

Return only JSON.

Format:

[
  {{
    "question":"",
    "options":["","","",""],
    "answer":""
  }}
]
"""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
    ai_response = response.choices[0].message.content.strip()

    return render_template(
        "personalized_quiz.html",
        quiz=ai_response
    )

@app.route("/ai_roadmap")
def ai_roadmap():

    conn = get_db()

    wrong = conn.execute("""
    SELECT question
    FROM QUIZ_HISTORY
    WHERE username = ?
    AND is_correct = 0
    """, (session["Username"],)).fetchall()

    conn.close()

    # -----------------------------
    # AI Prompt
    # -----------------------------
    if not wrong:

        prompt = """
The student answered all quiz questions correctly.

Create an Advanced 7-Day Study Roadmap.

For each day include:

- Day Number
- Advanced Topic
- Study Time
- Practice MCQs
- Coding Task
- Mini Project
- Revision

Motivate the student.

Return in simple text.
"""

    else:

        wrong_questions = "\n".join([row["question"] for row in wrong])

        prompt = f"""
The student answered these questions incorrectly:

{wrong_questions}

Create a personalized 7-day study roadmap.

For each day include:

- Day Number
- Topic to Study
- Study Time
- Practice MCQs
- Coding Task
- Revision Task

At the end give motivational tips.

Return in simple text.
"""

    # -----------------------------
    # AI Response
    # -----------------------------
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    ai_response = response.choices[0].message.content.strip()
    return render_template(
        "ai_roadmap.html",
        roadmap=ai_response
    )





































@app.route('/quiz_race')
def quiz_race():
    

    return render_template(
        "quiz_race_home.html",
        Username=session["Username"]
    )
@app.route("/save_race_score", methods=["POST"])
def save_race_score():

    if "username" not in session:
        return {"status": "error"}

    from flask import request

    score = request.json["score"]

    conn = get_db()

    conn.execute("""
        INSERT INTO GAME_SCORE
        (
            username,
            subject,
            score,
            created_at
        )
        VALUES
        (
            ?,
            'Quiz Race',
            ?,
            datetime('now')
        )
    """,
    (
        session["username"],
        score
    ))

    conn.commit()

    conn.close()

    return {"status":"success"}

@app.route("/start_race")
def start_race():


    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM quiz_race_questions
        ORDER BY RANDOM()
        LIMIT 10
    """)

    questions = [dict(row) for row in cur.fetchall()]

    conn.close()

    return render_template(
        "quiz_race.html",
        questions=questions
    )

init_db()

if __name__ == '__main__':
    
    app.run(debug=True)








    #python deployement
    #pip freeze > requirements.txt
    #
    #for deployement
    #http://www.pythonanywhere.com
    #command to use in python any where
    #







#python
#import sqlite3
#conn = sqlite3.connect('myproject.db')
#conn.execute("UPDATE USERS SET role='admin' WHERE username='Kaveri'")
#conn.commit()
#conn.close()
#exit(0)
