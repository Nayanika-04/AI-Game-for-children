import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pygame
import numpy as np
from collections import defaultdict

# Initialize pygame mixer for background music
pygame.mixer.init()
pygame.mixer.music.load("suspense-music.mp3")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

class CrimeCase:
    def __init__(self):
        self.victim = random.choice(["John Doe", "Alice Smith", "David Johnson", "Emma Brown", "Victoria Sanders", "Isabella Clarke", "Alexander Pierce", "Charlotte Hayes", "Madeline Brooks", "Lucas Foster"])
        self.location = random.choice(["Mansion", "Alleyway", "Hotel Room", "Office", "Warehouse", "Parking Garage", "Crowded Nightclub"])
        self.cause_of_death = random.choice(["Stabbing", "Gunshot", "Poisoning", "Strangulation", "Blunt Force Trauma", "Drowning", "Electrocution", "Suffocation", "Accident", "Medical Tampering"])
        self.suspects = self.generate_suspects()
        self.evidence = self.generate_evidence()
        self.guilty_suspect, self.motive = self.assign_guilty_suspect()
        self.suspect_statements = self.generate_suspect_statements()
        self.hints = self.generate_logic_based_hints()
        self.probabilities = self.calculate_bayesian_probabilities()
        self.chances = 2  # Number of attempts allowed for the player

    def generate_suspects(self):
        names = ["Michael", "Sophia", "Daniel", "Olivia", "James", "Emma", "William", "Ava", "Ethan", "Lily"]
        return random.sample(names, 5)

    def generate_evidence(self):
        possible_evidence = ["Bloody Knife", "Fingerprint on Glass", "CCTV Footage", "Suspicious Note", "Torn Fabric"]
        return random.sample(possible_evidence, 3)

    def assign_guilty_suspect(self):
        guilty = random.choice(self.suspects)
        motive = random.choice(["Revenge", "Jealousy", "Financial Gain", "Accidental", "Psychological Instability"])
        return guilty, motive

    def generate_suspect_statements(self):
        statements = {}
        for suspect in self.suspects:
            if suspect == self.guilty_suspect:
                statements[suspect] = "I don’t know what you’re talking about. I wasn’t even there."
            else:
                statements[suspect] = "I saw someone near the crime scene."
        return statements

    def generate_logic_based_hints(self):
        hints = []
        suspect_involved = random.choice(self.suspects)

        # Contradictory Alibi Statements
        hints.append(f"{random.choice(self.suspects)} claims to have seen {suspect_involved} elsewhere, but CCTV suggests otherwise.")
        hints.append(f"One suspect's alibi relies on another suspect’s testimony, making it unreliable.")

        # Evidence Contradictions
        hints.append(f"The {random.choice(self.evidence)} was found near the crime scene, but it could have been planted.")
        hints.append(f"A witness saw someone suspicious near the crime scene but couldn't identify them.")

        # Psychological Hints
        hints.append(f"{random.choice(self.suspects)} became defensive when questioned about {self.victim}.")
        hints.append(f"{self.guilty_suspect} reacted oddly when the murder weapon was mentioned.")

        # Financial or Motive-Based Hints
        hints.append(f"Financial records show {random.choice(self.suspects)} had money problems, but the victim wasn’t rich.")
        hints.append(f"Personal messages hint at an unknown conflict between the victim and at least one suspect.")

        # Time-Based Confusion
        hints.append(f"A loud argument was heard an hour before the estimated time of death.")
        hints.append(f"The murder occurred between 9-11 PM, but all suspects report conflicting timelines.")

        return random.sample(hints, min(4, len(hints)))

    def calculate_bayesian_probabilities(self):
        probabilities = defaultdict(float)
        for suspect in self.suspects:
            likelihood = random.uniform(0.2, 0.8)
            evidence_factor = 1.5 if suspect == self.guilty_suspect else 1.0
            probabilities[suspect] = likelihood * evidence_factor
        total_prob = sum(probabilities.values())
        for suspect in probabilities:
            probabilities[suspect] /= total_prob
        return probabilities

class CrimeGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Investigation Game")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.menu_bg_image = Image.open("crime_scene_menu.jpeg").resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.menu_bg_photo = ImageTk.PhotoImage(self.menu_bg_image)
        self.menu_bg_label = tk.Label(self.root, image=self.menu_bg_photo)
        self.menu_bg_label.place(relwidth=1, relheight=1)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 14), bg="red", fg="white")
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.quit_game, font=("Arial", 14), bg="gray", fg="white")
        self.exit_button.pack(pady=10)

    def start_game(self):
        self.case = CrimeCase()
        self.attempts = 0  # Track number of attempts
        self.create_ui()

    def create_ui(self):
        self.clear_window()
        self.bg_image = Image.open("murder_scene.jpeg").resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        frame = tk.Frame(self.root, bg="black", bd=5)
        frame.pack(pady=10)

        tk.Label(frame, text=f"Victim: {self.case.victim}", fg="white", bg="black", font=("Arial", 12, "bold")).pack()
        tk.Label(frame, text=f"Location: {self.case.location}", fg="white", bg="black", font=("Arial", 12, "bold")).pack()
        tk.Label(frame, text=f"Cause of Death: {self.case.cause_of_death}", fg="white", bg="black", font=("Arial", 12, "bold")).pack()
        tk.Label(frame, text="Hints:", fg="lightblue", bg="black", font=("Arial", 12, "bold")).pack()

        for hint in self.case.hints:
            tk.Label(frame, text=f"• {hint}", fg="lightblue", bg="black", font=("Arial", 12)).pack()

        tk.Label(frame, text="Suspects:", fg="red", bg="black", font=("Arial", 12, "bold")).pack()
    
        for suspect in self.case.suspects:
            btn = tk.Button(
                frame,
                text=suspect,
                command=lambda s=suspect: self.show_statement(s),
                font=("Arial", 12),
                bg="gray",
                fg="white"
            )
            btn.pack(pady=2)

    # Label to display suspect statements
        self.statement_label = tk.Label(frame, text="", fg="lightblue", bg="black", font=("Arial", 12, "bold"))
        self.statement_label.pack(pady=5)
        
        
        self.criminal_var = tk.StringVar()
        self.criminal_dropdown = ttk.Combobox(self.root, textvariable=self.criminal_var, values=self.case.suspects, font=("Arial", 12))
        self.criminal_dropdown.pack(pady=5)

        tk.Button(self.root, text="Select Culprit", command=self.check_criminal, bg="yellow", fg="black", font=("Arial", 12, "bold")).pack(pady=5)

    def show_statement(self, suspect):
        self.statement_label.config(text=self.case.suspect_statements[suspect])

    
    def check_criminal(self):
        selected_criminal = self.criminal_var.get()
        if selected_criminal == self.case.guilty_suspect:
            messagebox.showinfo("Correct!", "You found the murderer! Starting a new case...")
            self.start_game()
        else:
            self.attempts += 1
            if self.attempts < 2:
                messagebox.showwarning("Incorrect", "Wrong choice! Try again.")
            else:
                messagebox.showinfo("Game Over", f"The real murderer was {self.case.guilty_suspect}. Starting a new case...")
                self.start_game()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def quit_game(self):
        pygame.mixer.music.stop()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    app = CrimeGameUI(root)
    root.mainloop()
