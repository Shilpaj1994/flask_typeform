"""
Flask Application
Author: Shilpaj Bhalerao
Date: Aug 24, 2021
"""
# Standard Library Imports
import os
from collections import namedtuple

# Third-Party Imports
import SharedArray as sa
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Local Imports
from source_code.utilities.forms import LoginForm, QuestionForm
from source_code.utilities.custom_exceptions import ValidationError
from source_code.login import validate_credentials as checker
from source_code.utilities.decorators import login_required

# Crate instance of flask for the app
application = Flask(__name__)
application.config['SECRET_KEY'] = "TheTopSecretKeyThatNoOneShouldKnow"
application.config['UPLOAD_FOLDER'] = './static/'

# NamedTuples for the Application
UserInfo = namedtuple("UserInfo", "first_name last_name use_case industry org_size role main_use_case discovery_source")
Question = namedtuple("Question", "question question_type description correct_answer")
PageInfo = namedtuple("PageInfo", "question question_type description correct_answer, layout_type, detail_type")

# Create an array in shared memory.
# share_question_info = sa.create("shm://test", 10)

# Global Variables needed across pages
username = None
questions = []
answers = []
count = -1
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'md'}
dictionary = {
    1: "Multiple Choice",
    2: "Multiple Answer",
    3: "Phone Number",
    4: "Short Text",
    5: "Long Text",
    6: "Picture Multiple Choice",
    7: "Picture Multiple Answers",
    8: "Statement",
    9: "Yes / No",
    10: "Email",
    11: "Likert",
    12: "Rating",
    13: "Date",
    14: "Number",
    15: "Single Blanks",
    16: "Multiple Blanks",
    17: "Dropdown",
    18: "File Upload",
    19: "Website Link"
}
question_layout_options = {
    "card-vertical": "question-vertical",
    "card-main": "question-body"
}
_value = None
layout_dropdown_value = None
details_dropdown_value = None
current_form = []


@application.route('/login', methods=["GET", "POST"])
def login():
    """
    Logic for the Login page
    """
    session['login'] = False
    global username
    message = None
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            checker.validate_username(username)
            checker.validate_password(password)
            session['logged_in'] = True
            return redirect(url_for('workspace'))
        except ValidationError as error_message:
            session['logged_in'] = False
            message = error_message
            return render_template("login.html", form=form, username=username, message=message)
    else:
        session['logged_in'] = False
        return render_template("login.html", form=form, username=username, message=message)


# TODO: Pass data to HTML page based on the Datafield like Stringfield
@application.route('/dashboard', methods=["GET", "POST"])
@login_required
def workspace():
    """

    """
    global username, questions
    try:
        with open('./source_code/setup/{}.txt'.format(username)) as file:
            print(file.readlines())
        if request.method == "POST":
            print("form page")
            return render_template("base_new_form.html", message="New form creation started")
        else:
            print("else error_statement")
            print(session['logged_in'])
            return render_template("dashboard.html", message="Welcome Back!")
    except IOError:
        with open('./source_code/setup/setup_questions.txt') as setup_iterator:
            for _question in setup_iterator:
                questions.append(_question)
        return redirect(url_for('dash_setup'))


@application.route('/setup', methods=["GET", "POST"])
@login_required
def dash_setup():
    global answers, count
    answer = request.form.get("FirstName")
    if answer is not None:
        answers.append(answer)
    count += 1
    if count < len(questions):
        return render_template("setup.html", question=questions[count], answer_type="string", placeholder_data="FirstName")
    else:
        with open('./source_code/setup/{}.txt'.format(username), 'w') as file:
            for question, answer in zip(questions, answers):
                file.write(question + '\t' + answer + '\n')
        return render_template("dashboard.html", message="Welcome Back!")


@application.route('/')
def home():
    """
    Logic for the Home page
    """
    session['logged_in'] = False
    # Point the app to the HTML file containing website
    return render_template("home.html")


# @application.route('/answers')
# @login_required
# def disp_ans():
#     global answers
#     return render_template("setup_answers.html", answers=answers)


# @application.route('/new_form', methods=["GET", "POST"])
# @login_required
# def new_form():
#     _value = request.form['question_type']
#
#     if request.method == 'POST':
#         _value = request.form['question_type']
#         print(_value)
#         return render_template("new_form.html", value=_value)
#     else:
#         print("Input Ignored")
#         return render_template("new_form.html", value=_value)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('upload_file.html')


def plagiarism_check(file_to_compare):
    student_files = file_to_compare

    plagiarism_results = set()

    vectorize = lambda text: TfidfVectorizer().fit_transform(text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

    file_notes = open(file_to_compare).read()

    vectors = vectorize(file_notes)
    s_vectors = list(zip(student_files, vectors))


@application.route('/deque', methods=['POST', 'GET'])
def deque():
    return render_template("deque.html")


@application.route('/base_new_form', methods=['POST', 'GET'])
def base_new_form():
    global dictionary, _value, layout_dropdown_value, details_dropdown_value
    layout_type = "card-main"
    _lay = []
    question_form = QuestionForm()

    if request.method == 'POST':
        if request.form.get('question_type', False):
            _value = request.form['question_type']
            print(dictionary[int(_value)])
            # share_question_info[0] = dictionary[int(_value)]
        elif request.form.get('question_layout_type', False):
            layout_dropdown_value = request.form['question_layout_type']
            print(layout_dropdown_value)
        elif request.form.get('details_type', False):
            details_dropdown_value = request.form['details_type']
            print(details_dropdown_value)
        elif request.form.get('new_page_button', False):
            details_dropdown_value = request.form['new_page_button']
            print(details_dropdown_value)
        elif request.form.get('submit_button', False):
            details_dropdown_value = request.form['submit_button']
            print("Okay Pressed. Got data: ", details_dropdown_value)

            # question_form = QuestionForm(dictionary[int(_value)])
            try:
                if question_form.validate_on_submit():
                    print(question_form.question.data)
                    print(question_form.question_description.data)
                    print(question_form.correct_answer.data)
            except ValidationError as error:
                error_message = error
                # Print the validation error on the webpage
                return render_template("base_new_form.html", value=_value, dictionary=dictionary,
                                       layout_type=layout_type, error_message=error_message,
                                       question_layout_type=question_layout_options[layout_type],
                                       layout_dropdown_value=layout_dropdown_value,
                                       details_dropdown_value=details_dropdown_value,
                                       question_form=question_form)

            # print(request.form['question'])
            # print(request.form['question_description'])
            # print(request.form['correct_answer'])

                # current_form.append(Question(question=request.form['question'],
                #                              description=request.form['question_description'],
                #                              question_type=dictionary[int(_value)],
                #                              correct_answer=request.form['correct_answer']))

            # print(current_form)
            # print(len(current_form))

        layout_type = "card-main" if layout_dropdown_value == '1' else "card-vertical"
        print(_value, layout_type)
        return render_template("base_new_form.html", value=_value, dictionary=dictionary, layout_type=layout_type,
                               question_layout_type=question_layout_options[layout_type],
                               layout_dropdown_value=layout_dropdown_value,
                               details_dropdown_value=details_dropdown_value,  # )
                               question_form=question_form)
    else:
        print("Input Ignored")
        return render_template("base_new_form.html", value=_value, dictionary=dictionary, layout_type=layout_type,
                               question_layout_type=question_layout_options[layout_type])


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8888, debug=True)
