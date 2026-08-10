from datetime import datetime
import os
import sqlite3
from flask import Flask , session

app = Flask(__name__) 

app.secret_key = "linkkiwi2026" 

# Absolute database path 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_PATH = os.path.join(BASE_DIR, "myproject.db") 

def get_db(): 
        conn = sqlite3.connect(DB_PATH) 
        conn.row_factory = sqlite3.Row 
        return conn 

def init_db():
    conn = get_db()

#=================================> Contact Table <=================================    

    conn.execute("""
    CREATE TABLE IF NOT EXISTS contact(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    rating INTEGER NOT NULL,
    message TEXT NOT NULL
    )
    """)

#=================================> Score Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS SCORE(
        Sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_name TEXT NOT NULL,
        Username TEXT NOT NULL,
        Email TEXT NOT NULL,
        Password TEXT NOT NULL,
        subject TEXT NOT NULL,
        score INTEGER NOT NULL,
        percentage INTEGER NOT NULL,
        date INTEGER NOT NULL,

        time INTEGER
    )
    """)

#=================================> USERS Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_name TEXT NOT NULL,
        Username TEXT NOT NULL UNIQUE,
        Email TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Subject TEXT NOT NULL,
        date TEXT NOT NULL,
        role TEXT DEFAULT 'student'
    )
    """)

#=================================> Students Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    course TEXT,
    semester TEXT,
    photo TEXT DEFAULT 'default.png',
    role TEXT DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

#=================================> Feedback Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating INTEGER NOT NULL,
    message TEXT NOT NULL
);
""")
    
#=================================> Notes Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,  
    pdf_link TEXT
);
""")

#=================================> Quiz History Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS QUIZ_HISTORY (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        subject TEXT,
        topic TEXT,
        question TEXT,
        correct_answer TEXT,
        user_answer TEXT,
        is_correct INTEGER,
        attempt_date TEXT
    )
    """)

#=================================> Ai History Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS ai_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    subject TEXT,
    question TEXT,
    answer TEXT,
    date TEXT
);
""")

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM notes")

   

    if cur.fetchone()[0] == 0:
        conn.execute("""
    INSERT INTO notes (subject, title, description, pdf_link)
    VALUES

    ('Python', 'Python Complete Notes', 'Complete Python theory notes...', ''),
    ('Java', 'Java Complete Notes', 'Complete Java theory notes...', ''),
    ('C', 'C Complete Notes', 'Complete C theory notes...', ''),
    ('C++', 'C++ Complete Notes', 'Complete C++ theory notes...', ''),
    ('HTML', 'HTML Complete Notes', 'Complete HTML theory notes...', ''),
    ('CSS', 'CSS Complete Notes', 'Complete CSS theory notes...', ''),
    ('JavaScript', 'JavaScript Complete Notes', 'Complete JavaScript theory notes...', ''),
    ('DBMS', 'DBMS Complete Notes', 'Complete DBMS theory notes...', ''),
    ('Web Development', 'Web Development Complete Notes', 'Complete Web Development theory notes...', ''),
    ('Artificial Intelligence', 'Artificial Intelligence Complete Notes', 'Complete Artificial Intelligence theory notes...', ''),
    ('Data Science', 'Data Science Complete Notes', 'Complete Data Science theory notes...', ''),
    ('Cyber Security', 'Cyber Security Complete Notes', 'Complete Cyber Security theory notes...', ''),
    ('Cloud Computing', 'Cloud Computing Complete Notes', 'Complete Cloud Computing theory notes...', ''),
    ('Mobile App Development', 'Mobile App Development Complete Notes', 'Complete Mobile App Development theory notes...', '');
    """)
            
    try:
        conn.execute(
            "ALTER TABLE SCORE ADD COLUMN role TEXT DEFAULT 'student'"
        )
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("""
        ALTER TABLE USERS
        ADD COLUMN score INTEGER DEFAULT 0
    """)
    except sqlite3.OperationalError:
        pass

    # Add photo column to USERS table
    try:
        conn.execute(
            "ALTER TABLE USERS ADD COLUMN photo TEXT DEFAULT 'default.png'"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    # Add photo column to SCORE table
    try:
        conn.execute(
            "ALTER TABLE SCORE ADD COLUMN photo TEXT DEFAULT 'default.png'"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    # Set default photo for existing users
    conn.execute("""
        UPDATE USERS
        SET photo = 'default.png'
        WHERE photo IS NULL OR photo = ''
    """)

    # Set default photo for existing scores
    conn.execute("""
        UPDATE SCORE
        SET photo = 'default.png'
        WHERE photo IS NULL OR photo = ''
    """)

    conn.commit()

#=================================> Questions Table <=================================   

    conn.execute("""
    CREATE TABLE IF NOT EXISTS QUESTIONS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    default_subjects = [
        'Web Development',
        'Artifitial Intellegence',
        'Data Science',
        'Cyber Security',
        'Cloud Computing',
        'Mobile App Development',
        'Python',
        'Java',
        'C',
        'C++',
        'DBMS',
        'HTML',
        'CSS',
        'JavaScript'
    ]

    for subject in default_subjects:
        try:
            conn.execute(
                "INSERT INTO subjects(name) VALUES(?)",
                (subject,)
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

init_db() # function call 
if __name__ == "__main__":
        app.run(debug=True)
