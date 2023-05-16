import tkinter as tk
import random
import json
from datetime import datetime

# Game configuration
CLUES = [
    "The first clue is hidden under the old oak tree.",
    "Follow the winding path to find the next clue.",
    "Look for a clue near the tall stone statue.",
    "The clue is hidden inside the red mailbox.",
    "Check under the park bench for the next clue."
]
DEAD_ENDS = ["Oops! This is a dead end.", "You've reached a dead end. Try again."]
SOLUTION = "Congratulations! You found the hidden treasure."

# Function to generate a unique user ID
def generate_user_id():
    return str(random.randint(1000, 9999))

# Function to create a new user profile
def create_user(email, password):
    user_id = generate_user_id()
    user_data = {
        "email": email,
        "password": password,
        "progress": 0,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": []
    }
    save_user_data(user_id, user_data)
    return user_id

# Function to load user data
def load_user_data(user_id):
    try:
        with open(f"user_{user_id}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# Function to save user data
def save_user_data(user_id, user_data):
    with open(f"user_{user_id}.json", "w") as file:
        json.dump(user_data, file)

# Function to update user progress and log steps
def update_user_progress(user_id, progress, step):
    user_data = load_user_data(user_id)
    user_data["progress"] = progress
    user_data["steps"].append({
        "step": progress,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy": step
    })
    save_user_data(user_id, user_data)

# Function to resume or restart the game for a user
def resume_or_restart_game(user_id):
    user_data = load_user_data(user_id)
    if user_data:
        return user_data["progress"]
    else:
        return 0

# Function to track and analyze user data from the admin dashboard
def track_and_analyze_user_data():
    user_files = [file for file in os.listdir() if file.startswith("user_") and file.endswith(".json")]
    for user_file in user_files:
        with open(user_file, "r") as file:
            user_data = json.load(file)
            # Perform analysis or tracking based on user data

# Create the main window
window = tk.Tk()
window.title("Treasure Hunt Game")

# Game variables
user_id = ""
progress = 0

# Function to handle button click
def start_game():
    global user_id, progress
    email = email_entry.get()
    password = password_entry.get()
    user_id = create_user(email, password)
    progress = resume_or_restart_game(user_id)
    if progress == 0:
        clue_text = "Let's start the game!\n"
    else:
        clue_text = f"Resuming the game from step {progress}.\n"
    game_text.configure(state="normal")
    game_text.insert(tk.END, clue_text)
    game_text.configure(state="disabled")
    start_button.configure(state="disabled")
    next_clue_button.configure(state="normal")

def next_clue():
    global progress
    if progress < len(CLUES):
        clue_text = f"Clue {progress+1}: {CLUES[progress]}\n"
        # Simulating a random step accuracy (0 for wrong, 1 for correct)
        step_accuracy = random.choice([0, 1])
        update_user_progress(user_id, progress, step_accuracy)

        if step_accuracy == 0:
            clue_text += random.choice(DEAD_ENDS)
        else:
            progress += 1
            if progress == len(CLUES):
                clue_text += SOLUTION
        game_text.configure(state="normal")
        game_text.insert(tk.END, clue_text + "\n")
        game_text.configure(state="disabled")

# Create and configure GUI elements
email_label = tk.Label(window, text="Email:")
email_label.pack()

email_entry = tk.Entry(window)
email_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

start_button = tk.Button(window, text="Start Game", command=start_game)
start_button.pack()

game_text = tk.Text(window, height=10, width=50)
game_text.pack()

next_clue_button = tk.Button(window, text="Next Clue", command=next_clue)
next_clue_button.pack()
next_clue_button.configure(state="disabled")

# Function to handle game over
def game_over():
    save_user_data(user_id, None)
    start_button.configure(state="normal")
    next_clue_button.configure(state="disabled")

# Function to handle window close event
def on_close():
    game_over()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)

# Run the GUI event loop
window.mainloop()

