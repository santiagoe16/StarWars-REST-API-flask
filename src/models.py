from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))

    
    def __repr__(self):
        return '<Characters %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "gender": self.gender,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
        
            # do not serialize the password, its a security breach
        }
    
class FavoritesCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    user = db.relationship('User')
    character = db.relationship('Characters')

    def __repr__(self):
        return '<FavoritesCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "character_id": self.character_id,
            "character_name": self.character.name if self.character else None
        }
    
class FavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    user = db.relationship('User')
    planet = db.relationship('Planets')


    def __repr__(self):
        return '<FavoritesPlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "planet_id": self.planet_id,
            "planet_name": self.planet.name if self.planet else None
        }
    
