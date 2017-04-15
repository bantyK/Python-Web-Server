from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Student, Base

engine = create_engine('sqlite:///student.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


def add_into_db(student):
    session.add(student)
    session.commit()


student = Student(name="Banty", address="401 Manas Dreams", city="Ranchi", stream="Computer", gender="Male")
add_into_db(student)

student = Student(name="Alex", address="Kothrud", city="Nashik", stream="Computer", gender="Male")
add_into_db(student)

student = Student(name="Sam", address="Karve Road", city="Aurangabad", stream="Computer", gender="Male")
add_into_db(student)

student = Student(name="Andrew", address="Kothrud", city="Nagpur", stream="Computer", gender="Male")
add_into_db(student)

student = Student(name="Zoe", address="Bawdhan", city="Patna", stream="Computer", gender="Female")
add_into_db(student)

student = Student(name="Angela", address="SB Road", city="Pune", stream="Computer", gender="Female")
add_into_db(student)

student = Student(name="Michael", address="MIT Boys Hostel", city="Jaipur", stream="Mechanical", gender="Male")
add_into_db(student)

student = Student(name="John", address="MIT Boys Hostel", city="Latur", stream="Mechanical", gender="Male")
add_into_db(student)

student = Student(name="Lucy", address="4th Eve Avenue", city="Mumbai", stream="Mechanical", gender="Female")
add_into_db(student)

student = Student(name="Gus", address="2192 Baker Street", city="London", stream="Electrical", gender="Male")
add_into_db(student)

student = Student(name="Daisy", address="3430 16th Street", city="Delhi", stream="Civil", gender="Female")
add_into_db(student)

student = Student(name="Samatha", address="3430 16th Street", city="Delhi", stream="Civil", gender="Female")
add_into_db(student)

student = Student(name="Abby", address="1149 Chestnut St.", city="Kolkatta", stream="Infomation Technology", gender="Female")
add_into_db(student)

print "Students added"