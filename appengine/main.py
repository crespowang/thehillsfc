import logging
from flask import Flask
from flask import redirect, request
from resources.match import MatchesResource, MatchResource, MatchPlayers, MatchHelper, \
    MatchPlayerIn, MatchSignUp, MatchLeave, MatchStatus,MatchManualSignin, MatchManualFine, \
    MatchComment, MatchesStat, MatchesResourceCron
from resources.people import PeopleResource, PeoplesResource, PeopleLoginResource, PeopleLogoutResource, PeopleSignUpResource,PeoplePasswordResource, MeResource,MeStat
from resources.play import PlayResource, PlayMatchResource, PlayTeamResource
from flask_restful import Api
from flask.ext.login import login_required, logout_user
from appengine_config import host_url
from resources.login import login_manager
import webapp2
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "asdbiu324yuihuebwfksdf9bkj234!@#$@"

login_manager.init_app(app)

custom_errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'InvalidLoginError': {
        'message': "The login details are not right",
        'status': 401
    },
    'MatchNotExistsError': {
        'message': "The match ID does not exist",
        'status': 404,
    },
    'PlayNotExistsError': {
        'message': "The play ID does not exist",
        'status': 404,
    },
    'PeopleNotExistsError': {
        'message': "The username/email does not exist",
        'status': 404,
    }
}

api = Api(app, errors=custom_errors)

api.add_resource(MatchesResource, '/api/matches')
api.add_resource(MatchSignUp, '/api/matches/<match_id>/signmeup')
api.add_resource(MatchStatus, '/api/matches/<match_id>/status/<status>')
api.add_resource(MatchLeave, '/api/matches/<match_id>/leave')
api.add_resource(MatchComment, '/api/matches/<match_id>/comment')
api.add_resource(MatchManualSignin, '/api/matches/<match_id>/manualsignin/<people_id>')
api.add_resource(MatchManualFine, '/api/matches/<match_id>/manualfine/<people_id>')
api.add_resource(MatchesStat, '/api/matches/stat')
api.add_resource(MatchesResourceCron, '/api/matches/autocreate')

api.add_resource(MatchResource, '/api/matches/<match_id>')
api.add_resource(PeoplesResource, '/api/people')
api.add_resource(MeResource, '/api/people/me')
api.add_resource(MeStat, '/api/people/me/stat')
api.add_resource(PeopleResource, '/api/people/<people_id>')
api.add_resource(PlayResource, '/api/play')
api.add_resource(PlayTeamResource, '/api/play/<play_id>/teamup')

api.add_resource(MatchPlayers, '/api/matches/<match_id>/registered-people')
api.add_resource(PlayMatchResource, '/api/matches/<match_id>/plays')
api.add_resource(MatchPlayerIn, '/api/matches/<match_id>/<people_id>')

api.add_resource(PeopleLoginResource, '/api/people/login')
api.add_resource(PeopleLogoutResource, '/api/people/logout')
api.add_resource(PeopleSignUpResource, '/api/people/signup')
api.add_resource(PeoplePasswordResource, '/api/people/password-reset')

@app.route('/.well-known/acme-challenge/<code>')
def xxxx(code):
    return '{}.thcMl-VXF71YS4cMbXPT8G5FdzQdxUOiUumUcivfFbU'.format(code)


@login_manager.unauthorized_handler
def unauthorized():
    logging.debug("unauthorized and next={}".format(request.path))

    return redirect('/#/login?next={}{}'.format(host_url,request.path))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



@app.route('/match-signin/<matchid>/<code>')
@login_required
def match_signin(matchid, code):
    logging.debug("Sign-in match {} code {}".format(matchid, code))

    checkin_status = MatchHelper.signin(matchid, code)
    if checkin_status and checkin_status.get('status'):
        logging.debug("Good Sign in")
        return redirect('/#/match-signin/{}/success'.format(matchid))
    else:
        logging.debug("Bad Sign in")
        if checkin_status.get("code") == -1:
            url = "/#/match-signin/{}/early".format(matchid)
        elif checkin_status.get("code") == 1:
            url = "/#/match-signin/{}/late".format(matchid)
        elif checkin_status.get("code") == 0:
            url = "/#/match-signin/{}/dup".format(matchid)

        return redirect(url)

    return redirect('/')



@app.route('/match-signup/<matchid>/<code>')
@login_required
def match_signup(matchid, code):
    logging.debug("Sign-up match {} code {}".format(matchid, code))
    checkin_status = MatchHelper.signup(matchid, code)
    if checkin_status:
        logging.debug("YEEAP")
        return redirect('/#/match-signup/{}/{}'.format(matchid, code))
    else:
        logging.debug("NOPPP")
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
