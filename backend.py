from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from clients import Registrant
from admin_login import AdminLogin
from enquiry import insert_enquiry_data  # Corrected import based on your provided snippet

app = Flask(__name__)
app.secret_key = '123456'  # Replace with your actual secret key


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        fullname = request.form['enquiry-fullname']
        email = request.form['enquiry-email']
        message = request.form['enquiry-message']

        try:
            insert_enquiry_data(fullname, email, message)
            return jsonify(
                {"status": "success", "message": "Thank You For Reaching Out, We Will Get Back To You Shortly"})
        except Exception as e:
            return jsonify({"status": "error", "message": "An error occurred. Please try again."})
    return render_template('landing.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        registration_type = request.form['registration_type']
        snack_preferences = ', '.join(request.form.getlist('snack_preferences'))
        extra_services = 'Yes' if 'Extra Services' in request.form.getlist('extra_services') else 'No'

        new_person = Registrant(firstname, lastname, email, phone, registration_type, snack_preferences, extra_services)
        new_person.create_user_table()

        try:
            if new_person.register(email, phone):
                return jsonify({"status": "error", "message": "Sorry, Email or Phone Number Already Registered."})
            else:
                new_person.insert_data(firstname, lastname, email, phone, registration_type, snack_preferences,
                                       extra_services)
                return jsonify({"status": "success", "message": "Congrats!!! You Have Registered, Hope To See You"})
        except Exception as e:
            return jsonify({"status": "error", "message": "An error occurred. Please try again."})
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = AdminLogin(username, password)
        if not admin.authentication(username, password):
            return jsonify({"status": "error", "message": "Please Check Your Credentials. This Is For Admin Only."})
        else:
            session['username'] = username  # Set the session variable
            return jsonify({"status": "success", "message": "Welcome Admin", "redirect_url": "/view"})
    return render_template('login.html')


# Dummy authentication check
def is_authenticated():
    return 'username' in session


@app.route('/view', methods=['GET', 'POST'])
def view():
    if not is_authenticated():
        return redirect(url_for('admin_login'))
    else:
        if request.method == 'POST':
            registration_type = request.form.get('registration_type')
            registrations = AdminLogin.fetch_data(registration_type)

            if registrations:
                return jsonify({'registrations': registrations})
            else:
                return jsonify({'error': f'Sorry, No Registrations Found For {registration_type}s'})
    return render_template('view.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session variable
    return redirect(url_for('admin_login'))


@app.route('/about_us')
def about_us():
    return render_template('aboutUs.html')


if __name__ == '__main__':
    app.run(debug=True)
