from flask import Flask, make_response, jsonify, request, session as browser_session, render_template
from flask_migrate import Migrate
from models import db, Boats, Times, BoatTimes, User
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boatrentals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

migrate = Migrate(app, db)
db.init_app(app)

EXCLUDED_ENDPOINTS = ['login', 'root']

# route to check if user is logged in
@app.before_request
def check_if_logged_in():
    if request.endpoint not in EXCLUDED_ENDPOINTS:
        user_id = browser_session.get('user_id')
        user_verified = User.query.filter(User.id == user_id).first()

        if not user_verified:
            return jsonify({"error": "not authorized"}, 401) 


# route for LOGIN
@app.route("/login", methods = ['POST'])
def login():
    username = request.get_json().get('username')
    user_exists = User.query.filter(User.username == username).first()
    if not user_exists: 
        return jsonify({"error": "user not found"}), 404
    elif user_exists:
        browser_session['user_id'] = user_exists.id
        print(user_exists.username)
        return jsonify(username)

# default route
@app.route("/")
def root():
        return render_template('index.html')

# route for all boats
@app.route("/boats", methods = ['GET', 'POST'])
def boats():
    # GET for all BOATS
    if request.method == 'GET':
        boats = Boats.query.all()
        boats_dict = [boat.to_dict_with_times() for boat in boats]
        return make_response(jsonify(boats_dict), 200)
        # POST for all BOATS
    elif request.method == 'POST':
        body = request.get_json()
        new_boat = Boats()
        for key, value in body.items():
            setattr(new_boat, key, value)
        db.session.add(new_boat)
        db.session.commit()
        return make_response(jsonify(new_boat.to_dict_with_times()), 201)   


# route for BOAT by ID
@app.route('/boats/<id>', methods = ['GET', 'DELETE', 'PATCH'])  
def boat_by_id(id):
    boat_exists = Boats.query.get(id)
    # validates if boat exists  
    if not boat_exists:
        return jsonify({"error": "boat not found"}), 404
    if boat_exists:
        # GET for BOAT by ID
        if request.method == 'GET':
            return jsonify(boat_exists.to_dict_with_times()), 200
        # DELETE for BOAT by ID
        elif request.method == 'DELETE':
            db.session.delete(boat_exists)
            db.session.commit()
            return jsonify({"status": "DELETE successful"}), 200
        #  PATCH for BOAT by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(boat_exists, key, value)
            db.session.add(boat_exists)
            db.session.commit()   
            return jsonify(boat_exists.to_dict_with_times()), 200 

# route for all TIMES   
@app.route("/times", methods = ['GET', 'POST']) 
def times():
    if request.method == 'GET':
        times = Times.query.all()
        times_dict = [time.to_dict_with_boats() for time in times]
        return make_response(jsonify(times_dict), 200)
    elif request.method == 'POST':
        body = request.get_json()
        new_time = Times()
        for key, value in body.items():
            setattr(new_time, key, value)
        db.session.add(new_time)
        db.session.commit()
        return make_response(jsonify(new_time.to_dict()), 201)  

# route for TIMES by ID
@app.route("/times/<id>", methods = ['GET', 'DELETE', 'PATCH'])
def times_by_id(id):
    time_exists = Times.query.get(id)    
     # validates if time exists  
    if not time_exists:
        return jsonify({"error": "time not found"}), 404
    if time_exists:
        # GET for TIME by ID
        if request.method == 'GET':
            return jsonify(time_exists.to_dict_with_boats()), 200
        # DELETE for TIME by ID
        elif request.method == 'DELETE':
            db.session.delete(time_exists)
            db.session.commit()
            return jsonify({"status": "DELETE successful"}), 200
        #  PATCH for TIME by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(time_exists, key, value)
            db.session.add(time_exists)
            db.session.commit()   
            return jsonify(time_exists.to_dict_with_boats()), 200


# route for all BoatTimes
@app.route("/boatTimes", methods = ['GET', 'POST'])
def boatTimes():
    if request.method == 'GET':
        boat_times = BoatTimes.query.all()
        boat_times_dict = [bt.to_dict() for bt in boat_times]
        return make_response(jsonify(boat_times_dict), 200) 
    elif request.method == 'POST':
        body = request.get_json()
        new_boat_time = BoatTimes()
        for key, value in body.items():
            setattr(new_boat_time, key, value)
        db.session.add(new_boat_time)
        db.session.commit()
        return make_response(jsonify(new_boat_time.to_dict()), 201) 
    
# route for BoatTimes by ID
@app.route('/boatTimes/<id>', methods = ['GET', 'DELETE', 'PATCH'])  
def boat_time_by_id(id):
    boat_time_exists = BoatTimes.query.get(id)
    # validates if boat`Time exists  
    if not boat_time_exists:
        return jsonify({"error": "boat-time not found"}), 404
    if boat_time_exists:
        # GET for BoatTime by ID
        if request.method == 'GET':
            return jsonify(boat_time_exists.to_dict()), 200
        # DELETE for BoatTime by ID
        elif request.method == 'DELETE':
            db.session.delete(boat_time_exists)
            db.session.commit()
            return jsonify({"status": "DELETE successful"}), 200
        # PATCH for BoatTime by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(boat_time_exists, key, value)
            db.session.add(boat_time_exists)
            db.session.commit()   
            return jsonify(boat_time_exists.to_dict()), 200     


# route for USER
@app.route("/users", methods = ['GET', 'POST'])
def user():
    if request.method == 'GET':
        users = User.query.all()
        user_dict = [user.to_dict() for user in users]
        return make_response(jsonify(user_dict), 200) 
    elif request.method == 'POST':
        body = request.get_json()
        new_user = User()
        for key, value in body.items():
            setattr(new_user, key, value)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)
    
# route for USER by ID
@app.route('/users/<id>', methods = ['GET', 'DELETE', 'PATCH'])
def get_user_by_id(id):
    user_exists = User.query.get(id)
    # validates if USER exists  
    if not user_exists:
        return jsonify({"error": "user not found"}), 404
    if user_exists:
        # GET for USER by ID
        if request.method == 'GET':
            return jsonify(user_exists.to_dict()), 200
        # DELETE for USER by ID
        elif request.method == 'DELETE':
            db.session.delete(user_exists)
            db.session.commit()
            return jsonify({"status": "DELETE successful"}), 200
        # PATCH for USER by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(user_exists, key, value)
            db.session.add(user_exists)
            db.session.commit()   
            return jsonify(user_exists.to_dict()), 200    