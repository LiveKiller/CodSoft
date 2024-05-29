import customtkinter as ctk
import random


app = ctk.CTk()
app.title("Rock-Paper-Scissors")
app.geometry("600x300")
user_score = 0
computer_score = 0


def play_game(user_choice):
    global user_score, computer_score
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result_label.configure(text="It's a tie!")
    elif (
            (user_choice == "rock" and computer_choice == "scissors")
            or (user_choice == "paper" and computer_choice == "rock")
            or (user_choice == "scissors" and computer_choice == "paper")
    ):
        result_label.configure(text="You win!")
        user_score += 1
    else:
        result_label.configure(text="Computer wins!")
        computer_score += 1

    choice_label.configure(text=f"Computer chose: {computer_choice}")
    score_label.configure(text=f"Score: You {user_score} - {computer_score} Computer")

    play_again = ctk.CTkToplevel(app)
    play_again.title("Play Again?")
    play_again.geometry("400x100")
    play_again.maxsize(400, 100)
    play_again.grab_set()  # for windows only as the toplevel window loses focus, if you're on macOS or linux u can remove this line of code

    play_again_label = ctk.CTkLabel(play_again, text="Do you want to play again?")
    play_again_label.pack(pady=10)

    yes_button = ctk.CTkButton(play_again, text="Yes", command=play_again.destroy)
    yes_button.pack(side="left", padx=10)

    no_button = ctk.CTkButton(play_again, text="No", command=app.destroy)
    no_button.pack(side="right", padx=10)
    play_again.after(1000)
    app.wait_window(play_again)


choice_frame = ctk.CTkFrame(app)
choice_frame.pack(pady=20)

rock_button = ctk.CTkButton(choice_frame, text="Rock", corner_radius=10, fg_color="gray",
                            command=lambda: play_game("rock"))
rock_button.grid(row=0, column=0, padx=10)

paper_button = ctk.CTkButton(choice_frame, text="Paper", corner_radius=10, fg_color="white", text_color="black",
                             command=lambda: play_game("paper"))
paper_button.grid(row=0, column=1, padx=10)

scissors_button = ctk.CTkButton(choice_frame, text="Scissors", corner_radius=10, fg_color="red", text_color="white",
                                command=lambda: play_game("scissors"))
scissors_button.grid(row=0, column=2, padx=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

choice_label = ctk.CTkLabel(app, text="")
choice_label.pack()

score_label = ctk.CTkLabel(app, text=f"Score: You {user_score} - {computer_score} Computer")
score_label.pack(pady=10)

app.mainloop()
