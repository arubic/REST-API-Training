from db import db


class CandidateModel(db.Model):
    __tablename__ = 'candidate'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.Integer)
    resume_url = db.Column(db.String())
    site = db.Column(db.String())
    wtt = db.Column(db.Boolean)
    yeo = db.Column(db.Integer)
    recruited = db.Column(db.Boolean)

    def __init__(self, fname, lname, email, phone_number, resume_url, site, wtt, yeo, recruited):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone_number = phone_number
        self.resume_url = resume_url
        self.site   = site
        self.wtt = wtt
        self.yeo = yeo
        self.recruited = recruited

    def json(self):
        return{
            #'id': self.id,
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'phone_number': self.phone_number,
            'reumse_url': self.resume_url,
            'site': self.site,
            'wtt': self.wtt,
            'yeo': self.yeo,
            'recruited': self.recruited
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
        
    @classmethod
    def find_by_candidate_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_candidate_name(cls, fname, lname):
        return cls.query.filter_by(fname=fname, lname = lname).first()
    #@classmethod
    #def find_by_id(cls, _id):
        #return cls.query.filter_by(id=_id).first()
