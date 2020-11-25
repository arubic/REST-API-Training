from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )

from models.candidate import CandidateModel


_candidate_parser = reqparse.RequestParser()
_candidate_parser.add_argument(  'fname',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
_candidate_parser.add_argument(  'lname',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )                            

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(  'fname',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'lname',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'email',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'phone_number',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'resume_url',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'site',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'wtt',
                            type=bool,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'yeo',
                            type=int,
                            required=True,
                            help="This field cannot be blank."
                            )
post_put_parser.add_argument(  'recruited',
                            type=bool,
                            required=True,
                            help="This field cannot be blank."
                            )



class Candidate(Resource):
    def get(self):
        data = _candidate_parser.parse_args()
        candidate = CandidateModel.find_by_candidate_name(data['fname'],data['lname'])
        if candidate:
            return candidate.json()
        return {'message': 'Candidate not found'}, 404

    def post(self):
        data = post_put_parser.parse_args()
        if CandidateModel.find_by_candidate_name(data['fname'],data['lname']):
            return {'message': "A candidate with name '{}' alreayd exists".format(data['fname']+ ' ' + data['lname'])},400

        candidate = CandidateModel(**data)

        try:
            candidate.save_to_db()
        except:
            return {'message': 'An error occured inserting the candidate.'}, 50
        
        return candidate.json(), 201

    def put(self):
        data = post_put_parser.parse_args()

        candidate = CandidateModel.find_by_candidate_name(data['fname'],data['lname'])

        if candidate:
            candidate.fname = data['fname']
            candidate.lname = data['lname']
            candidate.email = data['email']
            candidate.phone_number = data['phone_number']
            candidate.resume_url = data['resume_url']
            candidate.site = data['site']
            candidate.wtt = data['wtt']
            candidate.yeo = data['yeo']
            candidate.recruited = data['recruited']
        else:
            candidate = CandidateModel(**data)

        candidate.save_to_db()

        return candidate.json()

    def delete(self):
        data = _candidate_parser.parse_args()
        candidate = CandidateModel.find_by_candidate_name(data['fname'],data['lname'])
        if candidate:
            candidate.delete_from_db()
            return {'message': 'Candidate deleted.'}
        return {'message': 'Candidate not found.'}, 404

class CandidateList(Resource):
    def get(self):
        return [candidate.json() for candidate in CandidateModel.find_all()]

    def delete(self):
        try:
            for candidate in CandidateModel.find_all():
                candidate.delete_from_db()
            return {'message': 'All candidates have been deleted.'}, 200
        except:
            return {'message': 'An error has occured while deleting candiates.'}, 500
