from .. import db

class Call(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    initial_phone_number = db.Column(db.String)  
    call_name = db.Column(db.String)
    call_uuid = db.Column(db.String(128), unique=True)
    filename = db.Column(db.String(128))
    num_channels = db.Column(db.Integer)
    _phone_numbers = db.Column(db.String)
    pdf_link = db.Column(db.String)

    @property
    def phone_numbers(self):
        return [(x) for x in self._phone_numbers.split(';')]
    @phone_numbers.setter
    def ratings(self, pn):
        self._phone_numbers += ';%s' % pn

    def __repr__(self):
        return '<Call \'%s\'>' % self.call_uuid