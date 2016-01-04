import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

engine = sql.create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class Address(Base):
    __tablename__ = 'addresses'
    id = sql.Column(sql.Integer, primary_key=True)
    email = sql.Column(sql.String(50))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    user = sql.orm.relationship('User', back_populates='addresses')

    def __repr__(self):
        return u'<Address(email={})>'.format(self.email)

    @hybrid_property
    def is_gmail(self):
        return self.email.contains('gmail')

    @hybrid_property
    def startswith_admin(self):
        return self.email.startswith('admin')


class User(Base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True) 
    username = sql.Column(sql.String(10))
    password = sql.Column(sql.String)
    profile_id = sql.Column(sql.Integer, sql.ForeignKey('profiles.id'))
    profile = sql.orm.relationship('UserProfile', back_populates='user')

    addresses = sql.orm.relationship('Address', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return u'<User(username={})>'.format(self.username)

    @hybrid_property
    def gmail_addy(self):
        return self.addresses.filter(Address.is_gmail)

    @hybrid_property
    def is_active(self):
        if self.profile:
            return self.profile.active
        return False

class UserProfile(Base):
    __tablename__ = 'profiles'

    id = sql.Column(sql.Integer, primary_key=True)
    user = sql.orm.relationship('User', back_populates='profile')
    active = sql.Column(sql.Boolean, default=False)

    def __repr__(self):
        return u'<UserProfile(active={})>'.format(self.active)

class UserManager(object):
    def __init__(self, session):
        self._query = session.query(User)

    def gmail_addy(self):
        self._query = self._query.options(sql.orm.joinedload('addresses')).filter(Address.is_gmail)




Base.metadata.create_all(engine)
Session = sql.orm.sessionmaker(bind=engine)
session = Session()



jstrong = User(username='jstrong', password='pass')
admin = User(username='admin', password='admin')
address1 = Address(email='a@s.com')
address2 = Address(email='t@t.com')
address3 = Address(email='admin@hotmail.com')
address4 = Address(email='admin@gmail.com')
address5 = Address(email='not_admn@gmail.com')
jstrong.addresses.append(address1)
jstrong.addresses.append(address2)
admin.addresses.append(address3)
admin.addresses.append(address4)
admin.addresses.append(address5)

jstrong.profile = UserProfile(active=True)

session.add(jstrong)
session.add(admin)


