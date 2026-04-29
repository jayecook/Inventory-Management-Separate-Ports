from database import Base, engine, SessionLocal
from models import User, Product
from auth import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin_username = "admin"
admin_password = "admin123"

existing_admin = db.query(User).filter(User.username == admin_username).first()
if not existing_admin:
    db.add(User(username=admin_username, password_hash=hash_password(admin_password), role="admin"))
    print("Admin user created.")
else:
    print("Admin user already exists.")

if db.query(Product).count() == 0:
    db.add_all([
        Product(name="Standard Steel Hammer", stock=25, amount=50),
        Product(name="Nails", stock=16, amount=100),
        Product(name="Screw Drivers", stock=55, amount=150),
        Product(name="Screws", stock=87, amount=200),
        Product(name="Weighted Handle Hammer", stock=22, amount=150),
        Product(name="Paint Roller", stock=12, amount=80),
        Product(name="Tape Measure", stock=40, amount=100),
        Product(name="Work Gloves", stock=18, amount=75),
        Product(name="Utility Knife", stock=20, amount=60),
        Product(name="Drill Bits", stock=9, amount=50),
    ])
    print("Starter products added.")
else:
    print("Products already exist. Not reseeding.")

db.commit()
db.close()
print("Database setup complete.")
