from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    serialize_rules = ('-scientist.missions','-planet.missions')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable = False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = False)

    #scientist created
    # scientist = db.relationship('Scientist', back_populate = "missions")

    @validates('name')
    def valName(self, key, value):
        if value != "":
            return value
        else:
            ValueError("Cannot be empty")
    
    @validates('scientist_id')
    def valScientist(self, key, value):
        scientist = Scientist.query.filter(Scientist.id == value).first()
        print(self.planet_id)
        for planet in scientist.planets:
            if planet.id == self.planet_id:
                return ValueError("Scientist going to this planet") 
        if scientist:
            return value
        else:
            ValueError("Scientist does not exist")
    
    @validates('planet_id')
    def valPlanet(self, key, value):
        planet = Planet.query.filter(Planet.id == value).first()
        if planet:
            return value
        else:
            ValueError("Planet does not exist")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-missions.scientist',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False, unique= True)
    field_of_study = db.Column(db.String, nullable = False)
    avatar = db.Column(db.String)

    missions = db.relationship('Mission', backref = "scientist")

    planets = association_proxy('missions','planet')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def valName(self, key, value):
        if value != "":
            return value
        else:
            ValueError("Cannot be empty")
    
    @validates('field_of_study')
    def valFOS(self, key, value):
        if value != "":
            return value
        else:
            ValueError("Cannot be empty")


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    serialize_rules = ('-missions.planet',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)

    missions = db.relationship('Mission', backref = "planet")
    scientist = association_proxy('missions','scientist')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
