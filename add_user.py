from data.db_session import global_init, create_session
from data.users import User

global_init('db/users.sqlite')

session = create_session()

user = User(
    surname="Scott",
    name="Ridley",
    age=21,
    position="captain",
    speciality="research engineer",
    address="module_1",
    email="scott_chief@mars.org",
    hashed_password="cap",
)
user.set_password(user.hashed_password)
session.add(user)
session.commit()
