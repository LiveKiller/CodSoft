from tkinter import Listbox, END, filedialog
import pygame.mixer as mixer
import os
import customtkinter as ctk
from pygame import USEREVENT


class MusicPlayer(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.loop_status = True
        self.geometry("700x300")
        self.title("CodSoft Music Player")
        self.current_song = ctk.StringVar(value='<No song selected>')
        self.song_status = ctk.StringVar(value='<Not Available>')
        self.setup_ui()
        mixer.init()

    def setup_ui(self):
        # ----------------------------------Current song--------------------------------------------------------------------
        self.song_frame = ctk.CTkLabel(self, text='Currently Playing:', font=('Arial', 12, 'bold'))
        self.song_frame.place(x=20, y=20)
        self.song_label = ctk.CTkLabel(self, textvariable=self.current_song, font=('Cosmos MT', 15))
        self.song_label.place(x=20, y=50)
        # ----------------------------------Control buttons------------------------------------------------------------------

        button_style = {
            'bg_color': 'green',
            'border_spacing': 1,
            'font': ('Cosmos MT', 20),
            'border_width': 2,
            'width': 60,
            'height': 40,
            'hover_color': "green"
        }

        self.button_frame = ctk.CTkFrame(self, width=600, height=50)
        self.button_frame.place(x=150, y=250)

        self.skip_back_button = ctk.CTkButton(self.button_frame, text='\u23EA', command=self.skip_back, **button_style)
        self.skip_back_button.grid(row=0, column=0, padx=5, pady=5)

        self.play_button = ctk.CTkButton(self.button_frame, text='\u25B6', command=self.play_music, **button_style)
        self.play_button.grid(row=0, column=2, padx=5, pady=5)

        self.pause_button = ctk.CTkButton(self.button_frame, text='\u23F8', command=self.pause_music, **button_style)
        self.pause_button.grid(row=0, column=3, padx=5, pady=5)

        self.stop_button = ctk.CTkButton(self.button_frame, text='\u23F9', command=self.stop_music, **button_style)
        self.stop_button.grid(row=0, column=4, padx=5, pady=5)

        self.skip_button = ctk.CTkButton(self.button_frame, text='\u23E9', command=self.skip_song, **button_style)
        self.skip_button.grid(row=0, column=6, padx=5, pady=5)

        # self.loop_button_text = ctk.StringVar(value='🔁')  # Default: No loop
        # self.loop_button = ctk.CTkButton(self.button_frame, textvariable=self.loop_button_text,
        #                                  command=self.toggle_loop, **button_style)
        # self.loop_button.grid(row=0, column=7, padx=5, pady=5)

        # -------------------------------------Playlist----------------------------------------------------------------------
        self.listbox_frame = ctk.CTkFrame(self, width=400, height=200)
        self.listbox_frame.place(x=250, y=20)
        self.playlist_label = ctk.CTkLabel(self.listbox_frame, text='Playlist', font=('Arial', 12, 'bold'))
        self.playlist_label.pack()
        self.playlist = Listbox(self.listbox_frame, width=40, height=10)
        self.playlist.pack()
        self.add_button = ctk.CTkButton(self.listbox_frame, text='Add Song', command=self.add_song)
        self.add_button.pack()

    def add_song(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Song',
                                               filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if file_path:
            self.playlist.insert(END, os.path.basename(file_path))

    def play_music(self):
        selected_song = self.playlist.curselection()
        if selected_song:
            song_index = selected_song[0]
            song_name = self.playlist.get(song_index)
            song_path = os.path.join(os.getcwd(), song_name)
            mixer.music.load(song_path)
            mixer.music.play()
            mixer.music.play(loops=1 if self.loop_status else 0)
            self.current_song.set(song_name)
            self.song_status.set('Playing')
            mixer.music.set_endevent(USEREVENT)
            self.bind(USEREVENT, self.play_music)


    def pause_music(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.song_status.set('Paused')

    def stop_music(self):
        mixer.music.stop()
        self.current_song.set('<No song selected>')
        self.song_status.set('<Not Available>')

    def skip_song(self):
        try:
            if self.playlist.curselection():
                mixer.music.stop()
                next_song_index = (self.playlist.curselection()[0] + 1) % self.playlist.size()

                self.playlist.selection_clear(0, END)
                self.playlist.activate(next_song_index)
                self.playlist.selection_set(next_song_index)
                self.play_music()
        except IndexError:
            if self.playlist.size() > 0:
                self.playlist.activate(0)
                self.playlist.selection_set(0)
                self.play_music()

    def skip_back(self):
        if self.playlist.curselection():
            mixer.music.stop()
            prev_song_index = (self.playlist.curselection()[0] - 1) % self.playlist.size()
            self.playlist.activate(prev_song_index)
            self.playlist.selection_clear(0, END)
            self.playlist.selection_set(prev_song_index)
            self.play_music()
    # def toggle_loop(self):
    #     self.loop_status = not self.loop_status
    #     if self.loop_status:
    #         self.loop_button_text.set('🔂')
    #     else:
    #         self.loop_button_text.set('🔁')


if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
