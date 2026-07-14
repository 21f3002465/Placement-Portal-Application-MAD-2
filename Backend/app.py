from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from flask_security import Security
from database import db
from user_datastore import user_datastore
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    # CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    Security(app, user_datastore)
    api = Api(app)

    return app, api

def init_db(app):
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        company_role = user_datastore.find_or_create_role(name='company', description='Company')
        student_role = user_datastore.find_or_create_role(name='student', description='Student')

        admin_user = user_datastore.find_user(username='admin')
        if not admin_user:
            user_datastore.create_user(
                username='admin',
                email='admin@gmail.com',
                password='admin1234',
                roles=[admin_role]
            )
            db.session.commit()


app, api = create_app()
CORS(app)

from auth_apis import LoginUser, LogoutUser, RegisterStudent, RegisterCompany
from func_apis import PendingCompany, ApproveCompany, PendingDrives, ApproveDrives, CreateDrives, CompanyUser, Students, ViewApplications, OngoingDrives, Applications, ApproveApplication, ViewDrives, OngoingDrivesCompany, DeleteDrive, ViewProfile, ApplyDrives, Resume, Search, DeleteUser

api.add_resource(LoginUser, '/api/Login')
api.add_resource(LogoutUser, '/api/Logout')

api.add_resource(RegisterStudent, '/api/Register/Student')
api.add_resource(RegisterCompany, '/api/Register/Company')

api.add_resource(CompanyUser, '/api/company')

api.add_resource(Students, '/api/students')

api.add_resource(PendingCompany, '/api/admin/pendingcompany')
api.add_resource(ApproveCompany, '/api/admin/approvecompany')
api.add_resource(PendingDrives, '/api/admin/pendingdrive')
api.add_resource(OngoingDrives, '/api/admin/ongoingdrives')
api.add_resource(ApproveDrives, '/api/admin/approvedrive')
api.add_resource(DeleteUser, '/api/admin/deleteuser')

api.add_resource(Applications, '/api/company/applications')
api.add_resource(ApproveApplication, '/api/company/approveapplication')

api.add_resource(OngoingDrivesCompany, '/api/company/ongoingdrives')
api.add_resource(DeleteDrive, '/api/company/delete_drive')
api.add_resource(ViewProfile, '/api/company/profile')


api.add_resource(ViewDrives, '/api/students/viewdrives')
api.add_resource(ApplyDrives, '/api/students/apply/<int:drive_id>')
api.add_resource(ViewApplications, '/api/student/applications')
api.add_resource(Resume, '/api/student/resume')
api.add_resource(Search, '/api/student/search')





api.add_resource(CreateDrives, '/api/company/createdrive')

if __name__=='__main__':
    init_db(app)
    app.run(debug=True)