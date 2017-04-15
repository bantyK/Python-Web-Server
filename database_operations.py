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


def get_all_students():
    return session.query(Student).all()


def get_students_with_name(student_name):
    return session.query(Student).filter_by(name=student_name).all()


def add_into_database(new_student):
    session.add(new_student)
    session.commit()
    print "added into database"


def updateStudentData(old_student_name, new_student):
    student = session.query(Student).filter_by(name=old_student_name).one()

    if new_student.name:
        student.name = new_student.name
    if new_student.address:
        student.address = new_student.address
    if new_student.city:
        student.city = new_student.city
    if new_student.stream:
        student.stream = new_student.stream
    if new_student.gender:
        student.gender = new_student.gender

    session.add(student)
    session.commit()


def deleteStudent(student_name):
    student = session.query(Student).filter_by(name=student_name).one()
    session.delete(student)
    session.commit()
