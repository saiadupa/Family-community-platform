from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sur_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(150))
    date_of_birth = db.Column(db.String(20))
    place_of_birth = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    relations = db.Column(db.String(100))
    relation_name = db.Column(db.String(50))
    family_users = db.Column(db.String)
    registered = db.Column(db.Boolean)
    parent_user = db.Column(db.Integer)
    added_by = db.Column(db.Integer)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gotra = db.Column(db.String(20))
    religion = db.Column(db.String(20))
    caste = db.Column(db.String(20))
    sub_caste = db.Column(db.String(20))
    mother_tongue = db.Column(db.String(20))
    native_region = db.Column(db.String(30))
    date_of_birth = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    place_of_birth = db.Column(db.String(30))
    biography = db.Column(db.Text())

class FamilyDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    father_name = db.Column(db.String(30))
    mother_name = db.Column(db.String(30))
    grand_father = db.Column(db.String(30))
    grand_mother = db.Column(db.String(30))
    great_grand_father = db.Column(db.String(30))
    great_grand_mother = db.Column(db.String(30))
    spouse_name = db.Column(db.String(30))
    kids = db.Column(db.String(100))

class DnaTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    contact_number = db.Column(db.String(15))
    residence = db.Column(db.String(50))
    reason = db.Column(db.Text)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    message = db.Column(db.String(500))




