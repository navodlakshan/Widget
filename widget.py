import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Label, Frame
import time

# Function to fetch and parse the live cricket score
def get_live_score():
    url = "https://www.espncricinfo.com/series/sri-lanka-in-england-2024-1385672/england-vs-sri-lanka-1st-test-1385694/live-cricket-score"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the score section (Note: This is based on the current structure of the page)
    score_section = soup.find('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3')

    if score_section:
        raw_score = score_section.text.strip()

        # Process the score to match the desired structure
        # Assuming the structure is "Sri Lanka 236 England (4 ov) 22/0 Day 1 - England trail by 214 runs."
        score_parts = raw_score.split("Day ")

        # First part contains the scores of the two teams
        score_summary = score_parts[0]
        # Second part contains the day and additional information
        day_info = "Day " + score_parts[1] if len(score_parts) > 1 else "Day information not found"

        # Separate the two teams' scores (assuming the format is consistent)
        team_scores = score_summary.split("England")
        sri_lanka_score = team_scores[0].strip() if len(team_scores) > 0 else " "
        england_score = "England  " + team_scores[1].strip() if len(team_scores) > 1 else ""

        return sri_lanka_score, england_score, day_info
    else:
        return "Score not found", "", ""


# Function to update the score on the widget
def update_score():
    sri_lanka_score, england_score, day_info = get_live_score()
    sri_lanka_label.config(text=sri_lanka_score)
    england_label.config(text=england_score)
    day_info_label.config(text=day_info)
    root.after(10000, update_score)  # Update every 10 seconds

# Set up the Tkinter window
root = tk.Tk()
root.title("Live Cricket Score Widget")
root.geometry("500x250")
root.configure(bg="#2c3e50")


# Create a frame to hold the score labels
frame = Frame(root, bg="#34495e", bd=5, relief="groove")
frame.pack(expand=True, fill='both', padx=15, pady=15)

# Define the labels for the score with enhanced styling
sri_lanka_label = Label(frame, font=("Helvetica", 20, "bold"), fg="#ecf0f1", bg="#34495e")
sri_lanka_label.pack(anchor="w", pady=(10, 5))

england_label = Label(frame, font=("Helvetica", 20, "bold"), fg="#ecf0f1", bg="#34495e")
england_label.pack(anchor="w", pady=(0, 5))

day_info_label = Label(frame, font=("Helvetica", 16, "italic"), fg="#95a5a6", bg="#34495e")
day_info_label.pack(anchor="w", pady=(10, 5))

# Add a bottom frame to display additional details or branding (optional)
bottom_frame = Frame(root, bg="#1abc9c", bd=2, relief="ridge")
bottom_frame.pack(fill='x', padx=15, pady=(0, 15))

branding_label = Label(bottom_frame, text="Powered by ESPN Cricinfo", font=("Helvetica", 12, "bold"), fg="#2c3e50", bg="#1abc9c")
branding_label.pack(pady=5)

# Initialize the score update
update_score()

# Run the Tkinter main loop
root.mainloop()
