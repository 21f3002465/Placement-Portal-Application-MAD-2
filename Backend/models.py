from sqlalchemy import Nullable
from sqlalchemy.orm import backref
from database import db 
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fs_token_uniquifier = db.Column(db.String(150), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    resume_file =db.Column(db.String(1000))

    roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(500), nullable=False)

    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship to user who owns this company profile
    user = db.relationship('User', backref='Company', lazy=True)

    # Relationship links drives created by this company to it 
    drive = db.relationship('PlacementDrive', backref='Company', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_name = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(250))
    location = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    eligibility = db.Column(db.String(1000), nullable=False)
    posted_date = db.Column(db.String(50), nullable = False)
    deadline = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship links applications for this drive to it. Placement drive can recieve many applications from students
    applications = db.relationship('Application', backref='drive', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
# Application contains status of a student for a placement drive
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_on = db.Column(db.Date)
    status = db.Column(db.String(200), default='Applied')
    application_status = db.Column(db.String(200), default='pending')
    remarks = db.Column(db.String(10000)) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
