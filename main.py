from flask import Flask, render_template_string, session, redirect, url_for
from flask import request

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define question flow
questions = {
    1: {"text": "Do you like programming?", "yes": 2, "no": 3},
    2: {"text": "Do you prefer Python?", "yes": 4, "no": 5},
    3: {"text": "Do you like working with data?", "yes": 4, "no": 6},
    4: {"text": "Would you like to learn Flask?", "yes": None, "no": None},
    5: {"text": "Would you prefer JavaScript?", "yes": None, "no": None},
    6: {"text": "Do you prefer UI design?", "yes": None, "no": None},
}

# Define a route to start the question flow
@app.route('/')
def start():
    session['current_question'] = 1  # Start with question 1
    return redirect(url_for('question'))

# Define a route to show questions dynamically
@app.route('/question', methods=['GET', 'POST'])
def question():
    current_question_id = session.get('current_question')

    # Fetch current question based on ID
    question_data = questions.get(current_question_id)

    # Check if we reached the end of the questionnaire
    if question_data is None:
        return "You have completed the questionnaire. Thank you!"

    if request.method == 'POST':
        answer = request.form.get('answer')

        # Update to the next question based on user's answer
        if answer == 'yes':
            session['current_question'] = question_data['yes']
        elif answer == 'no':
            session['current_question'] = question_data['no']

        return redirect(url_for('question'))

    # Render the current question with Yes and No buttons
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Questionnaire</title>
    </head>
    <body>
        <h1>{question_data['text']}</h1>
        <form method="post">
            <button type="submit" name="answer" value="yes">Yes</button>
            <button type="submit" name="answer" value="no">No</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_content)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
