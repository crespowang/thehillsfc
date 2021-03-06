__author__ = 'crespowang'
from flask_restful import fields
from ext.util import UTCTime

# People Resource
people_field = {
    "id": fields.String,
    "name": fields.String,
    "position": fields.String,
    "weiboId": fields.String,
    "qqId": fields.String,
    "wechatId": fields.String,
    "facebookId": fields.String,
    "createdTime": UTCTime,
    "username": fields.String,
    "password": fields.String
}

people_resource_field = {
    "people": fields.Nested(people_field)
}

match_people_field = {
    "id": fields.String,
    "playId": fields.String,
    "name": fields.String,
    "signupTime": UTCTime,
    "signinTime": UTCTime,
    "signinLate": fields.Boolean,
    "signinOntime": fields.Boolean,
    "admin": fields.Boolean,
    "team": fields.String,
    "leave": fields.Boolean,
    "signupMissing": fields.Boolean,
    "finePaid": fields.Integer
}

match_people_resource = {
    "people": fields.Nested(match_people_field)
}



login_resource_field = {
    "username": fields.String,
    "password": fields.String
}


# Match Resource
match_field = {
    "id": fields.String,
    "location": fields.String,
    "startTime": UTCTime,
    "finishTime": UTCTime,
    "signinEarliest": UTCTime,
    "signinLatest": UTCTime,
    "createdTime": UTCTime,
    "signinLink": fields.String,
    "signupLink": fields.String,
    "signupCode": fields.String,
    "nosignups": fields.Integer,
    "noleaves": fields.Integer,
    "status": fields.String,
    "comment": fields.String
}

match_resource_fields = {
    'match': fields.Nested(match_field)
}

matches_resource_fields = {
    'matches': fields.Nested(match_field)
}

match_stat_field = {
    "id": fields.String,
    "start": UTCTime,
    "leave": fields.Integer,
    "ontime": fields.Integer,
    "signup": fields.Integer
}
matches_stat_fields = {
    'matches': fields.Nested(match_stat_field)
}


play_field = {
    "id": fields.String,
    "matchDetail": fields.Nested(match_field),
    "peopleDetail": fields.Nested(people_resource_field),
    "signupTime": UTCTime,
    "signinTime": UTCTime
}

play_of_match_resource_field = play_field
play_of_match_resource_field.__delitem__('matchDetail')

plays_resource_field = {

    "plays": fields.Nested(play_field)
}


play_resource_field = {
    "play": fields.Nested(play_field)
}


plays_of_match_resource_field = {
    "plays": fields.Nested(play_of_match_resource_field)
}