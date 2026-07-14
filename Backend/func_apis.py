from werkzeug.utils import secure_filename
from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security.decorators import auth_token_required, roles_required, roles_accepted

from flask_security import current_user
from database import db
from models import Company, PlacementDrive, Application, User
from datetime import datetime
# from app import app
import os


"""APIs for Admin"""

# View Registered Companies
class CompanyUser(Resource):
    # @auth_token_required
    # @roles_accepted('admin')
    def get(self):
        # students_registered = Application.query.get(Application.student_id).all()
        company = User.query.filter(User.roles.any(name="company")).all()
        return make_response(jsonify([{
            "id":c.id,
            "username":c.username,
            "email":c.email
        }for c in company]), 200)
    
# View all Pending Company Registrations
class PendingCompany(Resource):
    # @auth_token_required
    # @roles_required('admin')
    def get(self):
        pending_companies = Company.query.filter_by(is_approved = False).all()
        return make_response(jsonify([{
            "id": c.id,
            "name": c.name,
            "contact_number":c.contact_number,
            "address":c.address,
            "website":c.website,
            "username":c.user.username,
            "email":c.user.email
        } for c in pending_companies]), 200)
    
# Approve companies
class ApproveCompany(Resource):
    @auth_token_required
    @roles_required('admin')

    def post(self):
        data = request.get_json()
        company_id = data.get('company_id')
        action = data.get('action')

        # The company id here is the id in the Company table, not user table
        company = Company.query.get(company_id)
        if action=="approve":
            company.is_approved=True
            company.user.active=True
        
            db.session.commit()
            return make_response(jsonify({"message": f'"{company.name}" Approved'}))
        
# View Pending drives
class PendingDrives(Resource):
    @auth_token_required
    @roles_required('admin')

    def get(self):
        drives = PlacementDrive.query.filter_by(is_active=False).all()
        return make_response(jsonify([{
            "id": d.id,
            "drive_name":d.drive_name,
            "company_id":d.company_id,
            "title":d.title,
            "type":d.type,
            "salary":d.salary,
            "location":d.location,
            "description":d.description,
            "eligibility":d.eligibility,
            "posted_date":d.posted_date,
            "deadline":d.deadline,
            "status":d.is_active,      
        } for d in drives]), 200)
    
# Approve pending placement drives
class ApproveDrives(Resource):
    @auth_token_required
    @roles_required('admin')

    def post(self):
        data = request.get_json()
        drive_id = data.get('drive_id')
        status = data.get('status')

        drive = PlacementDrive.query.get(drive_id)
        if status=="approve":
            drive.is_active=True

            db.session.commit()
            return make_response(jsonify({"message": f"{drive.drive_name} Approved"}), 200)
        
# View Registered Students
class Students(Resource):
    # @auth_token_required
    # @roles_required('admin')
    # Get all student users

    def get(self):
        students=  User.query.filter(User.roles.any(name="student")).all()
        # roles is a many-to-many relationship (a collection of objects), not a column. You cannot filter it directly with a string.
        return make_response(jsonify([{
            "id":s.id,
            "username":s.username,
            "email":s.email
        }for s in students]), 200)
    
# View All Applications
class ViewApplications(Resource):
    @auth_token_required
    @roles_required('admin')

    def get(self):
        applications = Application.query.all()
        return make_response(jsonify([{
            "id":a.id,
            "drive_id":a.drive_id,
            "student_id":a.student_id,
            "applied_on":a.applied_on,
            "status":a.status,
            "application_status":a.application_status
        } for a in applications]), 200)  
    

# View Placement Drives
class OngoingDrives(Resource):
    # @auth_token_required
    # @roles_required('admin')

    def get(self):
        ongoingdrives = PlacementDrive.query.all()
        return make_response(jsonify([{
            "id":o.id,
            "drive_name":o.drive_name,
            "title":o.title,
            "type":o.type,
            "salary":o.salary,
            "location":o.location,
            "description":o.description,
            "eligibility":o.eligibility,
            "posted_date":o.posted_date,
            "deadline":o.deadline,   
        } for o in ongoingdrives]), 200)
    
# delete user
class DeleteUser(Resource):
    @auth_token_required
    @roles_required('admin')
    def delete(self):
        data = request.get_json()
        user_id = data.get('id')
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message":f"{user.username} deleted"}), 200)
        
"""Company"""
# Can view own profile
class ViewProfile(Resource):
    @auth_token_required
    @roles_required('company')

    def get(self):
        company_profile = Company.query.filter_by(user_id = current_user.id).first()
        return make_response(jsonify([{
            "id":company_profile.id,
            "name":company_profile.name,
            "contact_number":company_profile.contact_number,
            "address":company_profile.address,
            "website":company_profile.website,
        }]), 200)
 

# Create Placement Drives
class CreateDrives(Resource):
    @auth_token_required
    @roles_required('company')

    def post(self):
        new_drive = request.get_json()

        if not new_drive:
            return make_response(jsonify({'message': 'Details are required'}), 400)
        
        if not new_drive.get('drive_name'):
            return make_response(jsonify({'message': 'Please enter a valid drive_name'}), 400)
        
        if not new_drive.get('title'):
            return make_response(jsonify({'message': 'Please enter a valid title'}), 400)
        
        if not new_drive.get('type'):
            return make_response(jsonify({'message': 'Please enter whether job or internship'}), 400)

        
        if not new_drive.get('location'):
            return make_response(jsonify({'message': 'Please enter location'}), 400)
        
        if not new_drive.get('description'):
            return make_response(jsonify({'message': 'Please enter description'}), 400)

        if not new_drive.get('eligibility'):
            return make_response(jsonify({'message': 'Please enter eligibility criteria'}), 400)
        
        if not new_drive.get('posted_date'):
            return make_response(jsonify({'message': 'Please enter post date'}), 400)
        
        if not new_drive.get('deadline'):
            return make_response(jsonify({'message': 'Please enter deadline'}), 400)
        
        # 3. SECURELY LOOKUP THE COMPANY PROFILE USING THE TOKEN OWNER'S ID
        # Flask-Security maps the token to current_user.id automatically
        company_user = Company.query.filter_by(user_id=current_user.id).first()

        # Check if Drive already exists
        drive = PlacementDrive.query.filter_by(drive_name = new_drive["drive_name"]).first()
        if drive:
            return make_response(jsonify({'message': 'Drive exists'}), 400)

        drive_name = new_drive["drive_name"]
        title = new_drive["title"]
        type = new_drive["type"]
        salary = new_drive["salary"]
        location = new_drive["location"]
        description = new_drive["description"]
        eligibility = new_drive["eligibility"]
        posted_date = new_drive["posted_date"]
        deadline = new_drive["deadline"]

        # In models.py, PlacementDrive.company_id is defined as nullable=False. However, when creating a new drive, company_id is never passed or resolved. Committing this will fail with an IntegrityError (NOT NULL constraint failed)
        
        Drive = PlacementDrive(
            drive_name = drive_name,
            title = title,
            type = type,
            salary = salary,
            location = location,
            description = description,
            eligibility = eligibility,
            posted_date = posted_date,
            deadline = deadline,
            company_id = company_user.id,
            is_active=False
        )

        db.session.add(Drive)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Drive creation successful'}), 201)
    
# View it's ongoing applications
class OngoingDrivesCompany(Resource):
    @auth_token_required
    @roles_required('company')

    def get(self):
        company_user = Company.query.filter_by(user_id=current_user.id).first()
        ongoingdrives = PlacementDrive.query.filter_by(company_id = company_user.id, is_active=True).all()
        return make_response(jsonify([{
            "id":o.id,
            "drive_name":o.drive_name,
            "title":o.title,
            "type":o.type,
            "salary":o.salary,
            "location":o.location,
            "description":o.description,
            "eligibility":o.eligibility,
            "posted_date":o.posted_date,
            "deadline":o.deadline,   
        } for o in ongoingdrives]), 200)
    
# View Applications recieved by the students
class Applications(Resource):
    @auth_token_required
    @roles_required('company')

    def get(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        if not company:
            return make_response(jsonify({'message': 'Company profile not found'}), 404)
        applications = Application.query.filter(Application.drive.has(company_id = company.id)).all()
        return make_response(jsonify([{
            "id":a.id,
            "drive_id":a.drive_id,
            "student_id":a.student_id,
            "applied_on":a.applied_on,
            "status":a.status,
            "application_status":a.application_status
        } for a in applications]), 200)  

# Approve Application
class ApproveApplication(Resource):
    @auth_token_required
    @roles_required('company')

    def post(self):
        data = request.get_json()
        application_id = data.get('application_id')
        application_status = data.get('application_status')

        application = Application.query.get(application_id)
        if application_status=="approve":
            application.application_status="approved"

            db.session.commit()
            return make_response(jsonify({"message": f"Application Approved"}), 200)

        if application_status=="reject":
            application.application_status="rejected"

            db.session.commit()
            return make_response(jsonify({"message": f"Application Rejected"}), 200)

        if application_status=="shortlisted":
            application.application_status="shortlisted"
            # application.remarks = data.get('remarks')

            db.session.commit()
            return make_response(jsonify({"message": f"Application shortlisted"}), 200)

        
# Delete Placement Drives
class DeleteDrive(Resource):
    @auth_token_required
    @roles_required('company')
    def delete(self):
        data = request.get_json()
        drive_id = data.get('drive_id')
        drive = PlacementDrive.query.get(drive_id)
        if drive:
            company_user = Company.query.filter_by(user_id=current_user.id).first()
            if not company_user or drive.company_id != company_user.id:
                return make_response(jsonify({"message":"Unauthorized to delete this drive"}), 403)
            db.session.delete(drive)
            db.session.commit()
            return make_response(jsonify({"message":f"{drive.drive_name} deleted"}), 200)
        return make_response(jsonify({"message":"Drive not found"}), 404)

"""Student"""

# View available placement drives
class ViewDrives(Resource):
    # @auth_token_required
    # @roles_required('student')

    def get(self):
        drives = PlacementDrive.query.filter_by(is_active=True).all()
        return make_response(jsonify([{
            "id": d.id,
            "drive_name":d.drive_name,
            "company_id":d.company_id,
            "title":d.title,
            "type":d.type,
            "salary":d.salary,
            "location":d.location,
            "description":d.description,
            "eligibility":d.eligibility,
            "posted_date":d.posted_date,
            "deadline":d.deadline,
            "status":d.is_active,      
        }]for d in drives), 200)

# Apply for placement drives
class ApplyDrives(Resource):
    @auth_token_required
    @roles_required('student')

    def post(self, drive_id=None):
        data = request.get_json(silent=True) or {}

        if drive_id is None:
            drive_id = data.get('drive_id')

        if not drive_id:
            return make_response(jsonify({"message":"fill all the mandatory details"}), 400)

        date = datetime.now().date()

        # application only to be done once
        if not Application.query.filter_by(student_id=current_user.id, drive_id=drive_id).first():
            db.session.add(Application(
                drive_id = drive_id,
                student_id = current_user.id,
                applied_on = date,
                status = 'applied',
                application_status = 'applied'
            ))
            db.session.commit()
            return make_response(jsonify({'message': 'Application submitted successfully'}), 201)
        else:
            return make_response(jsonify({'message': 'Already applied for this drive'}), 400)

# Submit Resumes
class Resume(Resource):
    @auth_token_required
    @roles_required('student')

    def post(self):
        from app import app

        resume = request.files.get('resume')

        if resume and resume.filename.lower().endswith('.pdf'):
            file_name = secure_filename(f"resume_{current_user.id}_{current_user.username}")
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

            current_user.resume_file = file_name
            db.session.commit()
            return make_response(jsonify({'message': 'Resume uploaded successfully'}), 201)
        else:
            return make_response(jsonify({'message': 'No resume file uploaded or wrong file format'}), 400)
        
    def delete(self):
        current_user.resume_file = None
        db.session.commit()
        return make_response(jsonify({'message': 'Resume deleted successfully'}), 200)


# View placement drive history
class Search(Resource):
    @auth_token_required
    @roles_required('student')

    def get(self):
        my_applications = Application.query.filter_by(student_id=current_user.id).all()
        return make_response(jsonify([{
            "id":a.id,
            "drive_id":a.drive_id,
            "student_id":a.student_id,
            "applied_on":a.applied_on,
            "status":a.status,
            "application_status":a.application_status
        }for a in my_applications]), 200)