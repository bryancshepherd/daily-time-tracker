from app import db
from app.models import User, Phase
from app import bcrypt

def seed_default_data(force=False):
    # Check if there are already users in the database
    # Skip if data exists and not forcing
    if not force and User.query.count() > 0:
        print("Database already contains users. Skipping seeding.")
        return
    
    # Import your test user data
    from app.test_data import create_test_data
    test_users = create_test_data()
    
    # Add users and their phases
    for user_data in test_users:
        phases = user_data.pop('phases')
        
        # Hash the password
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        
        # Create user
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        
        # Add phases for this user
        for phase_data in phases:
            phase_data['user_id'] = user.id
            phase = Phase(**phase_data)
            db.session.add(phase)
        
    db.session.commit()
    print(f"Added {len(test_users)} test users with their schedules.")

