from .. import db

class Call(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    call_uuid = db.Column(db.String(128), unique=True)
    filename = db.Column(db.String(128))
    num_channels = db.Column(db.Integer)

    def __repr__(self):
        return '<Call \'%s\'>' % self.call_uuid