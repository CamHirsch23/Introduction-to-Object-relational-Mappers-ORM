import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:your_password@localhost/fitness_center_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Member(db.Model):
    """Model for the members table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, age):
        self.name = name
        self.age = age


class WorkoutSession(db.Model):
    """Model for the workout sessions table"""
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)

    def __init__(self, member_id, date, duration_minutes, calories_burned):
        self.member_id = member_id
        self.date = date
        self.duration_minutes = duration_minutes
        self.calories_burned = calories_burned


class MemberSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the Member model"""
    class Meta:
        model = Member


class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    """Schema for the WorkoutSession model"""
    class Meta:
        model = WorkoutSession


# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/members', methods=['POST'])
def add_member():
    """Add a new member"""
    name = request.json['name']
    age = request.json['age']
    new_member = Member(name, age)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member)


@app.route('/members', methods=['GET'])
def get_members():
    """Retrieve all members"""
    all_members = Member.query.all()
    result = members_schema.dump(all_members)
    return jsonify(result)


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Retrieve a member by ID"""
    member = Member.query.get(member_id)
    return member_schema.jsonify(member)


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update a member by ID"""
    member = Member.query.get(member_id)
    name = request.json['name']
    age = request.json['age']
    member.name = name
    member.age = age
    db.session.commit()
    return member_schema.jsonify(member)


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member by ID"""
    member = Member.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    return member_schema.jsonify(member)


@app.route('/workouts', methods=['POST'])
def add_workout_session():
    """Add a new workout session"""
    member_id = request.json['member_id']
    date = request.json['date']
    duration_minutes = request.json['duration_minutes']
    calories_burned = request.json['calories_burned']
    new_session = WorkoutSession(member_id, date, duration_minutes, calories_burned)
    db.session.add(new_session)
    db.session.commit()
    return workout_session_schema.jsonify(new_session)


@app.route('/workouts', methods=['GET'])
def get_workout_sessions():
    """Retrieve all workout sessions"""
    all_sessions = WorkoutSession.query.all()
    result = workout_sessions_schema.dump(all_sessions)
    return jsonify(result)


@app.route('/workouts/<int:session_id>', methods=['GET'])
def get_workout_session(session_id):
    """Retrieve a workout session by ID"""
    session = WorkoutSession.query.get(session_id)
    return workout_session_schema.jsonify(session)


@app.route('/workouts/<int:session_id>', methods=['PUT'])
def update_workout_session(session_id):
    """Update a workout session by ID"""
    session = WorkoutSession.query.get(session_id)
    member_id = request.json['member_id']
    date = request.json['date']
    duration_minutes = request.json['duration_minutes']
    calories_burned = request.json['calories_burned']
    session.member_id = member_id
    session.date = date
    session.duration_minutes = duration_minutes
    session.calories_burned = calories_burned
    db.session.commit()
    return workout_session_schema.jsonify(session)


@app.route('/workouts/<int:session_id>', methods=['DELETE'])
def delete_workout_session(session_id):
    """Delete a workout session by ID"""
    session = WorkoutSession.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return workout_session_schema.jsonify(session)


@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workout_sessions(member_id):
    """Retrieve all workout sessions for a specific member"""
    sessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    result = workout_sessions_schema.dump(sessions)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
