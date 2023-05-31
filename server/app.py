from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    response = make_response(
        {"message": "Hello Scientists!"}
    )

class ScientistPath(Resource):
    def get(self):
        scientists=Scientist.query.all()
        allscientists = []
        print(scientists[0].planets)
        for scientist in scientists:
            dict_scientist = scientist.to_dict()
            # dict_planets = []
            # for planet in scientist.planets:
            #     dict_planets.append(planet.to_dict())
            # dict_scientist["planets"] = dict_planets
            allscientists.append(dict_scientist)
        return make_response(allscientists,200)

    def post(self):
        try:
            data = request.get_json()
            newscientist = Scientist(name = data["name"], field_of_study=data['field_of_study'],avatar = data['avatar'])
            db.session.add(newscientist)
            db.session.commit()
            return make_response(newscientist.to_dict(),201)
        except:
            return make_response({"errors": ["validation errors"]}, 400)
api.add_resource(ScientistPath,'/scientists')

class ScientistId(Resource):
    def get(self,id):
        try:
            scientist = Scientist.query.filter(Scientist.id == id).first()
            return make_response(scientist.to_dict(),200)
        except:
            return make_response({"error": "Scientist not found"},404)
    def patch(self,id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if not scientist:
            return make_response({"error": "Scientist not found"},404)
        try:
            data = request.get_json()
            for key in data:
                setattr(scientist,key,data[key])
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(),202)
        except:
            return make_response({"errors": ["validation errors"]},404)
    def delete(self,id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        missions = scientist.missions
        db.session.delete(scientist)
        for mission in missions:
            db.session.delete(mission)
        db.session.commit()
        return make_response({"Deleted": "Success"},204)
api.add_resource(ScientistId,'/scientists/<id>')


class PlanetPath(Resource):
    def get(self):
        planets=Planet.query.all()
        allplanets = []
        # print(planets[0])
        for planet in planets:
            allplanets.append(planet.to_dict())
        return make_response(allplanets,200)
api.add_resource(PlanetPath,'/planets')

class MissionPath(Resource):
    def post(self):
        try:
            data = request.get_json()
            newMission = Mission(name = data["name"],planet_id = data['planet_id'], scientist_id=data['scientist_id'])
            db.session.add(newMission)
            db.session.commit()
            return make_response(newMission.to_dict(),201)
        except:
            return make_response({"errors": ["validation errors"]}, 400)
api.add_resource(MissionPath,'/mission')

if __name__ == '__main__':
    app.run(port=5555)
