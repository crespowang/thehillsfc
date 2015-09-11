__author__ = 'crespowang'
from google.appengine.ext import ndb
from datastore.people import People
from datastore.match import Match


class Play(ndb.Model):
    people = ndb.KeyProperty(kind=People)
    match = ndb.KeyProperty(kind=Match)
    registeredTime = ndb.DateTimeProperty(auto_now_add=True)
    checkinTime = ndb.DateTimeProperty()


    @classmethod
    def create(cls, peopleId, matchId):
        play = Play()
        play.populate(people=ndb.Key('People', long(peopleId)), match=ndb.Key('Match', long(matchId)))
        return play.put()

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()

    @classmethod
    def getbyMatch(cls, matchId):
        return cls.query(cls.match == ndb.Key('Match', long(matchId))).fetch()
