# Test users with varied schedules for different testing scenarios

def create_test_data():
    import os

    test_users = [
        # Standard office worker
        {
            "username": "office_worker",
            "email": "office@example.com",
            "password": os.environ.get("TEST_PASSWORD_1"),
            "timezone": "America/New_York",
            "apply_to_weekends": False,
            "phases": [
                {"name": "Morning Routine", "start_time": "06:00", "end_time": "07:30", "color": "#f39c12"},
                {"name": "Commute", "start_time": "07:30", "end_time": "08:30", "color": "#95a5a6"},
                {"name": "Focus Work", "start_time": "08:30", "end_time": "12:00", "color": "#2ecc71"},
                {"name": "Lunch", "start_time": "12:00", "end_time": "13:00", "color": "#e74c3c"},
                {"name": "Meetings", "start_time": "13:00", "end_time": "16:00", "color": "#9b59b6"},
                {"name": "Admin Tasks", "start_time": "16:00", "end_time": "17:30", "color": "#3498db"},
                {"name": "Commute Home", "start_time": "17:30", "end_time": "18:30", "color": "#95a5a6"},
                {"name": "Family Time", "start_time": "18:30", "end_time": "21:00", "color": "#1abc9c"},
                {"name": "Relax", "start_time": "21:00", "end_time": "23:00", "color": "#34495e"}
            ]
        },
        # Night owl programmer
        {
            "username": "night_coder",
            "email": "night@example.com",
            "password": os.environ.get("TEST_PASSWORD_2"),
            "timezone": "America/Los_Angeles",
            "apply_to_weekends": True,
            "phases": [
                {"name": "Sleep In", "start_time": "00:00", "end_time": "10:00", "color": "#34495e"},
                {"name": "Morning Coffee", "start_time": "10:00", "end_time": "11:00", "color": "#f39c12"},
                {"name": "Light Work", "start_time": "11:00", "end_time": "14:00", "color": "#3498db"},
                {"name": "Lunch/Break", "start_time": "14:00", "end_time": "15:30", "color": "#e74c3c"},
                {"name": "Exercise", "start_time": "15:30", "end_time": "17:00", "color": "#2ecc71"},
                {"name": "Dinner", "start_time": "17:00", "end_time": "18:30", "color": "#e67e22"},
                {"name": "Coding Prime Time", "start_time": "18:30", "end_time": "00:00", "color": "#9b59b6"}
            ]
        },
        # Early riser fitness enthusiast
        {
            "username": "early_bird",
            "email": "early@example.com",
            "password": os.environ.get("TEST_PASSWORD_3"),
            "timezone": "Europe/London",
            "apply_to_weekends": False,
            "phases": [
                {"name": "Early Morning", "start_time": "04:30", "end_time": "05:30", "color": "#34495e"},
                {"name": "Workout", "start_time": "05:30", "end_time": "07:00", "color": "#e74c3c"},
                {"name": "Breakfast/Prep", "start_time": "07:00", "end_time": "08:00", "color": "#f39c12"},
                {"name": "Deep Work", "start_time": "08:00", "end_time": "12:00", "color": "#2ecc71"},
                {"name": "Lunch", "start_time": "12:00", "end_time": "13:00", "color": "#e67e22"},
                {"name": "Meetings", "start_time": "13:00", "end_time": "16:00", "color": "#9b59b6"},
                {"name": "Wind Down Work", "start_time": "16:00", "end_time": "17:30", "color": "#3498db"},
                {"name": "Evening Activities", "start_time": "17:30", "end_time": "20:00", "color": "#1abc9c"},
                {"name": "Early Sleep", "start_time": "20:00", "end_time": "04:30", "color": "#34495e"}
            ]
        },
        # Freelancer with flexible schedule
        {
            "username": "freelancer",
            "email": "freelance@example.com",
            "password": os.environ.get("TEST_PASSWORD_4"),
            "timezone": "Asia/Tokyo",
            "apply_to_weekends": True,
            "phases": [
                {"name": "Morning Pages", "start_time": "08:00", "end_time": "09:30", "color": "#f39c12"},
                {"name": "Client Work", "start_time": "09:30", "end_time": "12:30", "color": "#2ecc71"},
                {"name": "Lunch Break", "start_time": "12:30", "end_time": "14:00", "color": "#e74c3c"},
                {"name": "Personal Project", "start_time": "14:00", "end_time": "16:00", "color": "#9b59b6"},
                {"name": "Exercise", "start_time": "16:00", "end_time": "17:30", "color": "#3498db"},
                {"name": "Dinner", "start_time": "17:30", "end_time": "19:00", "color": "#e67e22"},
                {"name": "Evening Work", "start_time": "19:00", "end_time": "22:00", "color": "#16a085"},
                {"name": "Relaxation", "start_time": "22:00", "end_time": "00:00", "color": "#34495e"}
            ]
        },
        # Polyphasic sleeper
        {
            "username": "polyphasic",
            "email": "polyphasic@example.com",
            "password": os.environ.get("TEST_PASSWORD_5"),
            "timezone": "Europe/Berlin",
            "apply_to_weekends": True,
            "phases": [
                {"name": "Core Sleep", "start_time": "00:00", "end_time": "03:30", "color": "#34495e"},
                {"name": "Early Work", "start_time": "03:30", "end_time": "07:30", "color": "#2ecc71"},
                {"name": "Nap 1", "start_time": "07:30", "end_time": "08:00", "color": "#34495e"},
                {"name": "Breakfast", "start_time": "08:00", "end_time": "09:00", "color": "#f39c12"},
                {"name": "Mid-Morning Work", "start_time": "09:00", "end_time": "12:30", "color": "#3498db"},
                {"name": "Lunch", "start_time": "12:30", "end_time": "13:30", "color": "#e74c3c"},
                {"name": "Nap 2", "start_time": "13:30", "end_time": "14:00", "color": "#34495e"},
                {"name": "Afternoon Work", "start_time": "14:00", "end_time": "17:30", "color": "#9b59b6"},
                {"name": "Exercise", "start_time": "17:30", "end_time": "19:00", "color": "#2ecc71"},
                {"name": "Dinner", "start_time": "19:00", "end_time": "20:00", "color": "#e67e22"},
                {"name": "Evening Activities", "start_time": "20:00", "end_time": "22:00", "color": "#16a085"},
                {"name": "Nap 3", "start_time": "22:00", "end_time": "22:30", "color": "#34495e"},
                {"name": "Late Work", "start_time": "22:30", "end_time": "00:00", "color": "#2c3e50"}
            ]
        }
    ]
    
    return test_users