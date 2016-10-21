from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

# Imports column names from the main.py
from main import Base, Shelter, Puppy

import datetime

# Creates the engine
engine = create_engine('sqlite:///main.db')

# Binds engine to the Base metadata
Base.metadata.bind = engine

# Creates the Database session, in order to perform operations
DBSession = sessionmaker(bind=engine)
session = DBSession()


def query_one():
    """Query all of the puppies and return the results in ascending alphabetical order"""
    result = session.query(Puppy.name).order_by(Puppy.name.asc()).all()

    # print the result with puppy name only
    # print len(result)
    for item in result:
        print item[0]


def query_two():
    """Query all of the puppies that are less than 6 months old organized by the youngest first"""
    today = datetime.date.today()
    if passesLeapDay(today):
        sixMonthsAgo = today - datetime.timedelta(days=183)
    else:
        sixMonthsAgo = today - datetime.timedelta(days=182)
    result = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

    # print the result with puppy name and dob
    for item in result:
        print "{name}: {dob}".format(name=item[0], dob=item[1])


def query_three():
    """Query all puppies by ascending weight"""
    result = session.query(Puppy.name, Puppy.weight).order_by(
        Puppy.weight.asc()).all()

    for item in result:
        print item[0], item[1]


def query_four():
    """Query all puppies grouped by the shelter in which they are staying"""
    result = session.query(Shelter, func.count(Puppy.id)).join(
        Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]

# Helper Methods


def passesLeapDay(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    thisYear = today.timetuple()[0]
    if isLeapYear(thisYear):
        sixMonthsAgo = today - datetime.timedelta(days=183)
        leapDay = datetime.date(thisYear, 2, 29)
        return leapDay >= sixMonthsAgo
    else:
        return False


def isLeapYear(thisYear):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if thisYear % 4 != 0:
        return False
    elif thisYear % 100 != 0:
        return True
    elif thisYear % 400 != 0:
        return False
    else:
        return True

query_one()
query_two()
query_three()
query_four()

##############################################################################
# Examples
#
# CREATE
#
# We created a new Restaurant and called it Pizza Palace:
# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# session.add(myFirstRestaurant)
# sesssion.commit()
#
# We created a cheese pizza menu item and added it to the Pizza Palace Menu:
# cheesepizza = menuItem(name="Cheese Pizza",
#						 description="Made with all natural ingredients \
#						 and fresh mozzarella",
#						 course="Entree",
#						 price="$8.99",
#						 restaurant=myFirstRestaurant)
# session.add(cheesepizza)
# session.commit()
#
#
# READ
#
# We read out information in our database using the query method in SQLAlchemy:
# firstResult = session.query(Restaurant).first()
# firstResult.name
#
# items = session.query(MenuItem).all()
# for item in items:
#     print item.name
#
#
# UPDATE
#
# In order to update and existing entry in our database, we must execute
# the following commands:
#
# Find Entry
# Reset value(s)
# Add to session
# Execute session.commit()
# We found the veggie burger that belonged to the Urban Burger restaurant by
# executing the following query:
# veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#     print veggieBurger.id
#     print veggieBurger.price
#     print veggieBurger.restaurant.name
#     print "\n"
# Then we updated the price of the veggie burger to $2.99:
#
# UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()
#
#
# DELETE
#
# To delete an item from our database we must follow the following steps:
#
# Find the entry
# Session.delete(Entry)
# Session.commit()
# We deleted spinach Ice Cream from our Menu Items database with the
# following operations:
#
# spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
# session.delete(spinach)
# session.commit()
