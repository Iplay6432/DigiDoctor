from flask import Flask, render_template, request,make_response,send_from_directory
from backend import refer, Symptom,gmap,Price
import json
import os
api_key = os.environ.get('API_KEY')
app = Flask(__name__)

database = None
with open('userinfo/database.json', 'r') as f:
    database = json.load(f)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/signup', methods=["GET"])
def signup_get():
    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def signup_post():
    # Read data from the POST request
    username = request.form.get('username')
    password = request.form.get('password')
    firstName = request.form.get('firstname')
    lastName = request.form.get('lastname')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    birthdate = request.form.get('birthdate')
    healthInfo = request.form.get('healthInfo')
    print(request.form)
    # Process the data (e.g., save to database, validate, etc.)
    # For now, just print it to the console
    print(f"Username: {username}, Password: {password}")
    if username in database:
        return render_template('signup.html', error="Username already exists")
    else:
        database[username] = {
            "password": password,
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
            "birthdate": birthdate,
            "healthInfo": healthInfo
        }
        with open('userinfo/database.json', 'w') as f:
            json.dump(database, f)
        return render_template('login.html', message="Account created successfully")

@app.route('/login',  methods=["GET"])
def login_get():
    return render_template('login.html')
@app.route('/login', methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password') 
    response = make_response(render_template('dashboard.html'))
    response.set_cookie('username', username)
    response.set_cookie('password', password)
    
    if username in database and database[username]['password'] == password:
        return response
    else:
        return render_template('login.html', error="Invalid credentials")
@app.route('/profile', methods=["GET"])
def profile_get():
    return render_template('profile.html', user = database[request.cookies.get('username')])

@app.route('/profile', methods=["POST"])
def profile_post():
    response = make_response()
    username = request.cookies.get('username')
    password = request.cookies.get('password')
                                   
    password2 = request.form.get('password')
    firstName = request.form.get('firstname')
    lastName = request.form.get('lastname')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    birthdate = request.form.get('birthdate')
    healthInfo = request.form.get('healthInfo')
    
    response = make_response(render_template('dashboard.html'))
    if password2 != None or password2 != "":
        database[username][password] = password
        response.set_cookie('password', password2)
    if firstName != None or firstName != "":
        database[username][firstName] = firstName
    if lastName != None or lastName != "":
        database[username][lastName] = lastName
    if email != None or email != "":
        database[username][email] = email
    if address != None or address != "":
        database[username][address] = address
    if city != None or city != "":
        database[username][city] = city
    if state != None or state != "":
        database[username][state] = state
    if zip_code != None or zip_code != "":
        database[username][zip_code] = zip_code
    if birthdate != None or birthdate != "":
        database[username][birthdate] = birthdate
    if healthInfo != None or healthInfo != "":
        database[username][healthInfo] = healthInfo
        with open('userinfo/database.json', 'w') as f:
            json.dump(database, f)
    return response

@app.route('/delete', methods=["GET"])
def delete_get():
    return render_template('delete.html')
@app.route('/delete', methods=["POST"])
def delete_post():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username in database and database[username]['password'] == password:
        del database[username]
        with open('userinfo/database.json', 'w') as f:
            json.dump(database, f)
        return render_template('homepage.html', message="Account deleted successfully")
    else:
        return render_template('delete.html', error="Invalid credentials")
@app.route('/logout', methods=["POST"])
def logout_post():
    response = make_response(render_template('homepage.html', message="Logged out successfully"))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response
@app.route('/refer', methods=["GET"])
def refer_get():
    return render_template('refer.html')

@app.route('/hacks', methods=["GET"])
def hacks_get():
    return render_template('hacks.html')

@app.route('/hacks', methods=["POST"])
def hacks_post():
    symptoms = request.form.getlist('symptoms')
    solutions = Symptom.Symptom(symptoms)  # Instantiate the Symptom class
    solutions_info = solutions.info()  # Call the info method
    print(solutions_info)
    return render_template('hacks.html', recommendations=solutions_info)
    
    
@app.route('/refer', methods=["POST"])
def refer_post():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    
    if username in database and database[username]['password'] == password:
        symptom = request.form.get('symptom')
        location = request.form.get('location')
        text = refer(database[username]["firstName"], symptom).gen()
        text = text.lower()
        if text == "yes":
            pass
        else:
            pass
@app.route('/dashboard', methods=["GET"])
def dashboard_get():
    return render_template('dashboard.html')

@app.route('/hospital', methods=["GET"])
def hospitals_get():
    return render_template('hospitals.html')
@app.route('/hospital', methods=["POST"])
def hospitals_post():
    job = request.form.get('operation')
    pricecompare = Price.Price(job)
    priceinfo = pricecompare.info()
    print(priceinfo)
        
    return render_template('hospitals.html', jobs=priceinfo)

@app.route('/severity', methods=["GET"])
def severity_get():
    return render_template('severity.html')

@app.route('/severity', methods=['POST'])
def severity_post():
    badthings = request.form.get('symptoms')
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username in database and database[username]['password'] == password:
        goto = refer.Refer(username, badthings).gen()
        info = str(goto["content"])
        info= info.replace(".", "")
        print(info.lower())
        print("test!")
        if info.lower() == "yes":
            print("You should go to the emergency room")
            places = gmap.FindHealth(database[username]["address"] + " "+ database[username]["city"] + " "+database[username]["state"]+ " "+ database[username]["zip"]).find()
            print(places)
        else:
            places = gmap.FindHealth(database[username]["address"] + " "+ database[username]["city"] + " "+database[username]["state"]+ " "+ database[username]["zip"], 16,"clincs").find()
            print(places)
        data = {}
        for place in places:
            data[place["name"]] = f"https://www.google.com/maps/embed/v1/place?q={place["latitude"]},{place["longitude"]}&key={api_key}"
        print(data)
        return render_template('severity.html', links=data)
    else:
        return render_template('login.html', error="Invalid credentials")
    
if __name__ == '__main__': 
    app.run(debug=True,  host='localhost', port=8080)