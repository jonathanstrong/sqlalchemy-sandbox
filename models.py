import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

engine = sql.create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True) 
    username = sql.Column(sql.String(10))
    password = sql.Column(sql.String)

    addresses = sql.orm.relationship('Address', order_by='Address.id', back_populates='user')

    def __repr__(self):
        return self.username

def Address(Base):
    __tablename__ = 'addresses'
    id = sql.Column(sql.Integer, primary_key=True)
    email = sql.Column(sql.String(50))
    user_id = sql.Column(sql.Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return u'<Address(email={})>'.format(self.email)

Base.metadata.create_all(engine)
Session = sql.orm.sessionmaker(bind=engine)
session = Session()



