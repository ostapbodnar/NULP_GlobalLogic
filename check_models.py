from models import Session, User, Advertisment, Place

session = Session()

place1 = Place(id=1, name="Lviv")
place2 = Place(id=2, name="Rozvadiv")

user1 = User(id=1, user_name="AlexGer", first_name="Alex", last_name="Gerbert", email="ddd@gmail.com", password="7896",
             phone="3809355566",
             place=place1)
user2 = User(id=2, user_name="BOnzai", first_name="Roman", last_name="Biliy", email="udesity@gmail.com",
             password="1234", phone="38093474747",
             place=place2)

adv1 = Advertisment(id=1, name="Buy a flat", description="I need a flat ....", quantity=1,
                    createdate="01.12.2020 12:31", status=1, tag=0,
                    owner=user1)
adv2 = Advertisment(id=2, name="Buy a cat", description="I need a cats ....", quantity=3,
                    createdate="31.11.2020 01:01", status=1, tag=1,
                    owner=user2)
adv3 = Advertisment(id=3, name="Buy a cat", description="I need a cats ....", quantity=3,
                    createdate="31.11.2020 01:01", status=1, tag=1,
                    owner=user2)
adv4 = Advertisment(id=4, name="Buy a cat", description="I need a cats ....", quantity=3,
                    createdate="31.11.2020 01:01", status=1, tag=1,
                    owner=user2)
session.add(place1)
session.add(place2)

session.add(user1)
session.add(user2)

session.add(adv1)
session.add(adv2)
session.add(adv3)
session.add(adv4)

session.commit()

# psql -h localhost -d test -U postgres -p 5432 -a -q -f create_tables.sql

