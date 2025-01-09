from . import db

# association table for the many-to-many relationship
user_art_favourites = db.Table(
    'user_art_favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('art_id', db.Integer, db.ForeignKey('Art.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship to Art through the association table
    favourites = db.relationship('Art', secondary=user_art_favourites, back_populates='favourited_by')

    def __init__(self, username):
        self.username = username   

    def register_user_if_not_already(self):        
        db_user = User.query.filter(User.username == self.username).all()
        if not db_user:
            db.session.add(self)
            db.session.commit()
        return True  

    def get_by_username(username):        
        db_user = User.query.filter(User.username == username).first()
        return db_user   

    def __repr__(self):
        return f"<User {self.username}>"


class Art(db.Model):
    __tablename__ = "Art"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    objectID = db.Column(db.Integer, nullable=False)
    primaryImage = db.Column(db.String(), nullable=False)

    favourited_by = db.relationship('User', secondary=user_art_favourites, back_populates='favourites')

    def __init__(self, objectID, primaryImage):
        self.objectID = objectID
        self.primaryImage = primaryImage

    def get_by_objectID(objectID):        
        db_objectID = Art.query.filter(Art.objectID == objectID).first()
        return db_objectID  

    def __repr__(self):
        return f"<Art {self.objectAPI_ID}>"
    
    def to_dict(self):
        return {
            'objectID': self.objectID,
            'primaryImage': self.primaryImage           
        }
