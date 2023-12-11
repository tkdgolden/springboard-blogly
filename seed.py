from models import User, Post, db

db.drop_all()
db.create_all()

hawkeye = User(first_name="Alan", last_name="Alda", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Alan_Alda_circa_1960s.JPG/330px-Alan_Alda_circa_1960s.JPG")
radar = User(first_name="Gary", last_name="Burghoff", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/GaryBurghoff03.jpg/330px-GaryBurghoff03.jpg")
margaret = User(first_name="Loretta", last_name="Swit", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Loretta_Swit_MASH_1972.JPG/300px-Loretta_Swit_MASH_1972.JPG")

db.session.add(hawkeye)
db.session.add(radar)
db.session.add(margaret)

db.session.commit()

hell = Post(title="Hell", content="War isn't Hell. War is war, and Hell is Hell.  And of the two, war is a lot worse.", user_id=1)
gin = Post(title="gin", content="I thought this stuff was supposed to make you feel better.", user_id=2)
disgusting = Post(title="You're Disgusting", content="Yes, Frank, we've all discussed you, and we all find you disgusting!", user_id=1)
lips = Post(title="Get Out!", content="Listen to these lips, Frank. Get Out!", user_id=3)
wounds = Post(title="Wounds", content="Look Colonel, I'll heal their wounds, treat their wounds, bind their wounds, but I will not inflict their wounds.", user_id=1)

db.session.add(hell)
db.session.add(gin)
db.session.add(disgusting)
db.session.add(lips)
db.session.add(wounds)

db.session.commit()