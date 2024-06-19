#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import Volunteer, Organization, Opportunity


@app.before_request
def check_log_statues():
    open_access_list = [
        'signup',
        'login',
        'check_session'
    ]
    if request.endpoint not in open_access_list and (not session.get('volunteer_id')):
        return make_response({"error": "401 Unauthorized"}, 401)

class Home(Resource):
    def get(self):
        all_opps = []
        for opp in Opportunity.query.all():
            all_opps.append(opp.to_dict())
            return make_response(all_opps)

class Login(Resource):
    def post(self):
        params= request.json
        volunteer = Volunteer.query.filter(username=params.get('username')).first()
        if not volunteer:
            return make_response({"error": "Volunteer not found"}, 404)
        if volunteer.authenticate(params.get('password')):
            session['volunteer_id'] = volunteer.id
            return make_response(volunteer.to_dict())
        else:
            return make_response({"error": "Invalid password"}, 401)
    
class Logout(Resource):
    def delete(self):
        session['volunteer_id'] = None
        return make_response({}, 204)

class CheckSession(Resource):
    def get(self):
        volunteer_id = session['volunteer_id']
        if volunteer_id:
            volunteer = db.session.get(Volunteer, volunteer_id)
            if volunteer:
                return make_response(volunteer.to_dict(), 200)
        return make_response({"error": "Unauthorized: Must login"}, 401)
    
class Signup(Resource):
    def post(self):
        params = request.get_json()
        
        username = params.get('username')
        password = params.get('password')
        first_name = params.get('first_name')
        last_name= params.get('last_name')
        email = params.get('email')
        phone_number = params.get('phone_number')
        interests = params.get('interests')
        skills = params.get('skills')
        hours_wanted = params.get('hours_wanted')
        zipcode = params.get('zipcode')
        
        volunteer = Volunteer(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            interests = interests,
            skills = skills,
            hours_wanted = hours_wanted,
            zipcode = zipcode
        )
        volunteer.password_hash = password
        
        try:
            db.session.add(volunteer)
            db.session.commit()
            
            session['volunteer_id'] = volunteer.id
            return make_response(volunteer.to_dict(), 201)
        except IntegrityError:
            return make_response({"error": "422 Unprocessable Entity"}, 422)

class Opportunities(Resource):
    def get(self):
        opportunities = Opportunity.query.all()
        opportunity_list = [oppurtunity.to_dict() for oppurtunity in opportunities]
        return make_response(opportunity_list, 200)

    def post(self):
        data = request.json
        try: 
            opp = Opportunity(
                title = data['title'],
                description = data['description'],
                remote_or_online = data['remote_or_online'],
                category = data['category'],
                dates = data['dates'],
                duration = data['duration'],
                organization_id = data['organization_id']
            )
            db.session.add(opp)
            db.session.commit()
            return make_response(opp.to_dict(), 201)
        except:
            return make_response({"error": "Could not create Opportunity"}, 400)

class OpportunitiesById(Resource):
    def get(self, id):
        opp = Opportunity.query.get(Opportunity, id).first()
        if opp:
            return make_response(opp.to_dict(), 200)
        else:
            return make_response({'error': 'Opportunity not found'}, 404)
        
    def patch(self, id):
          opp = Opportunity.query.get(Opportunity, id).first()
          if opp:
              params = request.json
              for attr in params:
                  setattr(opp , attr, params[attr])
                  db.session.commit()
                  return make_response(opp.to_dict())
              
    def delete(self, id):
        opp = db.session.get(Opportunity, id)
        if opp:
            db.session.delete(opp)
            db.session.commit()
            return make_response({"message": "Successfully deleted Oppurtunity"})

class Organizations(Resource):
    def get(self):
        organizations = Organization.query.all()
        organization_list = [organization.to_dict() for organization in organizations]
        return make_response(organization_list, 200)
    
    def post(self):
        data = request.json
        try: 
            org = Organization(
                name = data['name'],
                website = data['website'],
                category = data['category'],
            )
            db.session.add(org)
            db.session.commit()
            return make_response(org.to_dict(), 201)
        except:
            return make_response({"error": "Could not create Organization"}, 400)

    
class OrganizationById(Resource):
    def get(self, id):
        org = Organization.query.get(Organization, id).first()
        if org:
            return make_response(org.to_dict(), 200)
        else:
            return make_response({'error': 'Organization not found'}, 404)
        
    def patch(self, id):
        org = Organization.query.get(Organization, id).first()
        if org:
            params = request.json
            for attr in params:
                setattr(org , attr, params[attr])
                db.session.commit()
                return make_response(org.to_dict())
    
    def delete(self, id):
        organization = db.session.get(Organization, id)
        if organization:
            db.session.delete(organization)
            db.session.commit()
            return make_response({"message": "Organization deleted successfully."}, 204)
        else:
            return make_response({"error": "Organization not found"}, 404)
        
   
class Profile(Resource):
    def get(self, id):
        volunteer = Volunteer.query.get(Volunteer, id).first()
        if volunteer:
            return make_response(volunteer.to_dict(), 200)
        else:
            return make_response({'error': 'Volunteer not found'}, 404)
        
    def patch(self, id):
        volunteer = Volunteer.query.get(Volunteer, id).first()
        if volunteer:
            params = request.json
            for attr in params:
                setattr(volunteer , attr, params[attr])
                db.session.commit()
                return make_response(volunteer.to_dict())
    
    def delete(self, id):
        volunteer = db.session.get(Volunteer, id)
        if volunteer:
            db.session.delete(volunteer)
            db.session.commit()
            return make_response({"message": "Volunteer deleted successfully."}, 204)
        else:
            return make_response({"error": "Volunteer not found"}, 404)

api.add_resource(Home, '/home')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Opportunities, '/opportunities')
api.add_resource(OpportunitiesById, '/opportunities/<int:id>')
api.add_resource(Profile, '/profile')
api.add_resource(Organizations, '/organization')
api.add_resource(OrganizationById, '/organization/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

