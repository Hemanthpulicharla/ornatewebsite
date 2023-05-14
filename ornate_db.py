import datetime
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,TEXT,PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.mutable import MutableList
from passlib.apps import custom_app_context as pwd_context


Base=declarative_base()

class Admins(Base):
	 
	__tablename__='admins'

	admin_id=Column(String(100),primary_key=True,unique=True,nullable=False)
	name=Column(String(200),nullable=False)
	email=Column(String(200),nullable=False)
	picture=Column(String(200))
	department=Column(String(200))
	contact=Column(Integer)
	password_hash=Column(String(100))


	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password,self.password_hash)

class Students(Base):
	__tablename__='students'

	id=Column(Integer,index=True,autoincrement=True)
	id_num=Column(String(200),primary_key=True)
	name=Column(String(200),nullable=False)
	email=Column(String(200),nullable=False,unique=True)
	receipt=Column(String(200))
	branch=Column(String(200))
	contact=Column(Integer)
	events=Column(String(100))
	Timestamp=Column(DateTime, default=datetime.datetime.utcnow)


engine=create_engine('sqlite:///ornate_db.db')

Base.metadata.create_all(engine)
