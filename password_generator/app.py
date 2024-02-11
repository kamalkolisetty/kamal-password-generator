from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    try:
        length = int(request.form['length'])
        include_uppercase = bool(request.form.get('include_uppercase'))
        include_digit = bool(request.form.get('include_digit'))
        alphabets_only = bool(request.form.get('alphabets_only'))
        repeat = int(request.form.get('repeat', 1))  # Use default value 1 if 'repeat' parameter is not provided
    except:
        return jsonify({'error': 'Please provide valid input'})

    if alphabets_only:
        character_string = string.ascii_letters
    else:
        character_string = string.ascii_lowercase
        if include_uppercase:
            character_string += string.ascii_uppercase
        if include_digit:
            character_string += string.digits
        character_string += string.punctuation

    # Ensure at least one uppercase letter if required
    if include_uppercase:
        password = random.choices(string.ascii_uppercase, k=1)
    else:
        password = []

    # Ensure at least one digit if required
    if include_digit:
        password.append(random.choice(string.digits))

    # Generate remaining characters
    password += random.choices(character_string, k=length - len(password))

    # Shuffle the password characters
    random.shuffle(password)

    # Repeat if necessary
    if repeat == 1:
        password = ''.join(password)
    else:
        password = ''.join(random.choices(password, k=length))

    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)
