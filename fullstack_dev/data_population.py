from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# restaurant_name = ['Urban Burger','Panda Garden','Thyme for That Vegetatian Cuisine',"Tony's Bistro","Andala's","Auntie Ann's Diner","Cocina Y amor"]
# for i in range(len(restaurant_name)):
#     name_add=Restaurant(name=restaurant_name[i])
#     session.add(name_add)
#     session.commit()

# items = session.query(Restaurant).all()
# for item in items:
#     print(item.name)
#     print(item.id)

# delete_first = session.query(Restaurant).all()
# for item in delete_first:
#     session.delete(item)
#     session.commit()
