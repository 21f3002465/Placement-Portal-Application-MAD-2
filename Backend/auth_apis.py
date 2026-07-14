from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security.decorators import auth_token_required
from models import Company
from user_datastore import user_datastore
from flask_security import utils
from database import db

class RegisterStudent(Resource):
    def post(self):
        new_user = request.get_json()
        # role = new_user.get('role')

        if not new_user:
            return make_response(jsonify({'message': 'Details are required'}), 400)
        
        if not new_user.get('username'):
            return make_response(jsonify({'message': 'Please enter a valid username'}), 400)
        
        if not new_user.get('email'):
            return make_response(jsonify({'message': 'Please enter a valid email id'}), 400)
        
        if not new_user.get('password'):
            return make_response(jsonify({'message': 'Please enter a valid password'}), 400)

        # Check if User already exists
        user = user_datastore.find_user(username = new_user["username"])
        if user:
            return make_response(jsonify({'message': 'Username exists'}), 400)

        user = user_datastore.find_user(email = new_user["email"])
        if user:
            return make_response(jsonify({'message': 'email id  exists'}), 400)
        
        username = new_user["username"]
        email = new_user["email"]
        password = new_user["password"]

        if len(password)<8:
            return make_response(jsonify({'message': 'password must be 8 charachters long'}), 400)
        
        user_role = user_datastore.find_role('student')
        
        user_datastore.create_user(
            username = username,
            email = email,
            password = password,
            roles = [user_role]
        )

        db.session.commit()
        
        return make_response(jsonify({'message': 'Registration successful',
                                      'user':{
                                          "username":username,
                                          "email":email
                                      }}), 201)

class RegisterCompany(Resource):
    def post(self):
        new_user = request.get_json()
        if not new_user:
            return make_response(jsonify({'message': 'Details are required'}), 400)
        
        if not new_user.get('username'):
            return make_response(jsonify({'message': 'Please enter a valid username'}), 400)
        
        if not new_user.get('email'):
            return make_response(jsonify({'message': 'Please enter a valid email id'}), 400)
        
        if not new_user.get('password'):
            return make_response(jsonify({'message': 'Please enter a valid password'}), 400)

        # Validate Company-specific fields
        if not new_user.get('name'):
            return make_response(jsonify({'message': 'Please enter a valid company name'}), 400)
        
        if not new_user.get('contact_number'):
            return make_response(jsonify({'message': 'Please enter a valid contact number'}), 400)
        
        if not new_user.get('address'):
            return make_response(jsonify({'message': 'Please enter a valid address'}), 400)
        
        if not new_user.get('website'):
            return make_response(jsonify({'message': 'Please enter a valid website URL'}), 400)

        # Check if User already exists
        user = user_datastore.find_user(username = new_user["username"])
        if user:
            return make_response(jsonify({'message': 'Username exists'}), 400)

        user = user_datastore.find_user(email = new_user["email"])
        if user:
            return make_response(jsonify({'message': 'email id  exists'}), 400)
        
        username = new_user["username"]
        email = new_user["email"]
        password = new_user["password"]

        if len(password)<8:
            return make_response(jsonify({'message': 'password must be 8 charachters long'}), 400)
        
        user_role = user_datastore.find_role('company')
        
        company_user = user_datastore.create_user(
            username = username,
            email = email,
            password = password,
            roles = [user_role],
            active = False
        )

        new_company = Company(
            name = new_user["name"],
            contact_number = new_user["contact_number"],
            address = new_user["address"],
            website = new_user["website"],
            user = company_user,
            is_approved = False
        )
        db.session.add(new_company)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Registration successful. Pending admin approval',
                                      'user':{
                                          "username":username,
                                          "email":email
                                      }}), 201)
          
        
class LoginUser(Resource):
    def post(self):
        login_cred = request.get_json()

        if not login_cred:
            response = {'message': 'Username and password are mandatory'}
            return make_response(jsonify(response), 400)
        
        if not login_cred.get('username'):
            return make_response(jsonify({'message': 'username is required'}), 400)
        
        if not login_cred.get('password'):
            return make_response(jsonify({'message': 'password is required'}), 400)

        # Data Validation
        username = login_cred.get('username')
        password = login_cred.get('password')

        # Check if user exists or not

        user = user_datastore.find_user(username=username)
        if not user:
            return make_response(jsonify({'message': 'Username not found'}), 404)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Invalid password'}), 401)
        
        if not user.active:
            return make_response(jsonify({'message': 'Your account is pending admin approval.'}), 403)
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            'message': 'Login successful',
            'auth_token': auth_token,
            'user':{
                'username': user.username,
                'email': user.email,
                'role':[role.name for role in user.roles]
            }
        }
        return make_response(jsonify(response), 200)
    
class LogoutUser(Resource):
    @auth_token_required 
    def post(self):
        utils.logout_user()
        return make_response(jsonify({"message":"Loggged Out"}), 200)