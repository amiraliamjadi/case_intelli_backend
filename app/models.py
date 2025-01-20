from .extensions import db
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash


class CategoryModel(db.Model):
    __tablename__ = "LGS.Category"

    CategoryID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=False)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    PricingMethod = db.Column(db.String(256), nullable=True)

    def json(self):
        return {
            "CategoryID": self.CategoryID,
            "Code": self.Code,
            "Name": self.Name,
            "PricingMethod": self.PricingMethod,
        }

    @classmethod
    def find_by_name(self, name):
        return self.query.filter_by(Name=name).first()

    @classmethod
    def find_all(self):
        return self.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(self, page=1, pageSize=10, orderBy="", **kwargs):
        return self.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)

class UnitModel(db.Model):

    __tablename__ = "GNR.Unit"

    UnitID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    AbbreviatedName = db.Column(db.String(256), nullable=True)

    def json(self):
        return {
            "UnitID": self.UnitID,
            "Name": self.Name,
            "AbbreviatedName": self.AbbreviatedName,
        }

    @classmethod
    def find_by_name(self, name):
        return self.query.filter_by(Name=name).first()

    @classmethod
    def find_all(self):
        return self.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(self, page=1, pageSize=10, orderBy="", **kwargs):
        return self.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)
    
class StoreModel(db.Model):
    __tablename__ = "LGS.Store"

    StoreID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128), nullable=False)
    Code = db.Column(db.String(64), nullable=False)

    # relationship with StorePositionModel
    positions = db.relationship(
        "StorePositionModel",
        back_populates="store",
        cascade="all, delete",
        lazy="dynamic"
    )

    def json(self):
        return {
            "StoreID": self.StoreID,
            "Name": self.Name,
            "Code": self.Code,
            "Positions": [position.json() for position in self.positions]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(Name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(cls, page=1, pageSize=10, orderBy="", **kwargs):
        return cls.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)

class StorePositionModel(db.Model):
    __tablename__ = "LGS.StorePosition"

    StorePositionID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=False)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    StoreID = db.Column(db.Integer, db.ForeignKey("LGS.Store.StoreID"), nullable=False)
    store = db.relationship("StoreModel", back_populates="positions")

    def json(self):
        return {
            "StorePositionID": self.StorePositionID,
            "Code": self.Code,
            "Name": self.Name,
            "StoreID": self.StoreID
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(Name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(cls, page=1, pageSize=10, orderBy="", **kwargs):
        return cls.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)
    
class PartyModel(db.Model):
    __tablename__ = "GNR.Party"

    PartyID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), nullable=True)
    FirstName = db.Column(db.String(50), nullable=True)
    LastName = db.Column(db.String(50), nullable=True)
    Gender = db.Column(db.String(20), nullable=True)
    Mobile = db.Column(db.String(20), nullable=True)
    EducationDegree = db.Column(db.String(50), nullable=True)

    # Relationship with UserModel
    users = db.relationship(
        "UserModel",
        back_populates="party",
        cascade="all, delete",
        lazy="dynamic"
    )

    def json(self):
        return {
            "PartyID": self.PartyID,
            "Title":   self.Title,
            "FirstName":   self.FirstName,
            "LastName":    self.LastName,
            "Gender":  self.Gender,
            "Mobile":  self.Mobile,
            "EducationDegree": self.EducationDegree,
            "Users": [user.json() for user in self.users]
        }

    @classmethod
    def find_by_id(self, PartyID):
        return self.query.filter_by(PartyID=PartyID).first()

    @classmethod
    def find_all(self):
        return self.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(self, page=1, pageSize=10, orderBy="", **kwargs):
        return self.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)

class UserModel(db.Model):
    __tablename__ = "SYS1.User"

    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(50), nullable=True)
    PartyRef = db.Column(db.Integer, db.ForeignKey("GNR.Party.PartyID"), nullable=False)
    IsAdministrator = db.Column(db.Boolean, default=False, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship with PartyModel
    party = db.relationship("PartyModel", back_populates="users")

    def __init__(self, email, partyref, password, isadministrator=False):
        self.Email = email
        self.PartyRef = partyref
        self.password_hash = self.generate_hash(password)
        self.IsAdministrator = isadministrator


    def json(self):
        return {
            "UserID": self.UserID,
            "PartyRef": self.PartyRef,
            "IsAdministrator": self.IsAdministrator,
            "Email":   self.Email
        }

    @staticmethod
    def generate_hash(password):
        """Hash a plaintext password using Werkzeug."""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        """Find a user by their email."""
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete the user from the database."""
        db.session.delete(self)
        db.session.commit()
