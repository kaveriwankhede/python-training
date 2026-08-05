from flask import Flask,url_for

from app import stidents

#HTML -Haedcoded html content
'<a href = "/students">view students</a>'

#right way url_for
'<a href = " '+url_for('students') +' ">view students</a>'

#url for (student) will generate the url for the student route defined in app.py
