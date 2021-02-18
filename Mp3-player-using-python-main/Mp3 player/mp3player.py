from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Into Nirvana')
root.geometry("1280x720")

#Initialize Pygame mixer
pygame.mixer.init()

# Grab Song Length Time Info
def play_time():
	#check for double timing
	if stopped:
		return
	# Grab Current Song Elapsed Time
	current_time = pygame.mixer.music.get_pos() / 1000

	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	#get currently playin 
	#current_song = song_box.curselection()
	#grab song by name from playlist
	song = song_box.get(ACTIVE)

	song = f'E:/Project/audio/{song}.mp3'

	#get song lenght using mutagen
	song_mut = MP3(song)
	global song_length
	song_length=song_mut.info.length
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	#increase current time by 1
	current_time +=1 

	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f'Time Elapsed: {converted_song_length}')
	elif paused:
		pass


	elif int(my_slider.get()) == int(current_time):
		#update silder position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))
	else:
		#update silder position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(my_slider.get()))
		#output time to status bar
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')

		#move this thing along by one second
		next_time = int(my_slider.get()+1)
		my_slider.config(value=int(next_time))	

	#output time to status bar 
	#status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')

	#update slider position value to current song position
	#my_slider.config(value=int(current_time))

	
	

	# update time
	status_bar.after(1000, play_time)

#Add Song Function
def add_song():
	song = filedialog.askopenfilename(initialdir='E:Project/audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	#strip out the directory info and .mp3 extension from the song name
	song = song.replace("E:/Project/audio/", "")
	song = song.replace(".mp3", "")

	# Add song to listbox
	song_box.insert(END, song)

#Add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='E:Project/audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

	#loop thru list
	for song in songs:
		song = song.replace("E:/Project/audio/", "")
		song = song.replace(".mp3", "")
		#insert in playlist
		song_box.insert(END, song)

#play selected song
def play():
	#set stopped variable to false
	global stopped
	stopped = False
	song = song_box.get(ACTIVE)
	song = f'E:/Project/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#call the play time function to get song lenght
	play_time()

	#update silder position
	slider_position = int(song_length)
	my_slider.config(to=slider_position, value=0)

#Stop playing current song
global stopped
stopped = False
def stop():
	#reset slider and status bar
	my_slider.config(value=0)
	status_bar.config(text='')
	#stop song from playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

	#clear status bar
	status_bar.config(text='')

	#set stop variable to true
	global stopped
	stopped = True

#play the next song in playlist
def next_song():
	#reset slider and status bar
	my_slider.config(value=0)
	status_bar.config(text='')

	#get current song tupple no
	next_one = song_box.curselection()
	#add one to current song number
	next_one = next_one[0]+1
	#grab song by name from playlist
	song = song_box.get(next_one)

	song = f'E:/Project/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#move active bar in playlist
	song_box.selection_clear(0, END)
	song_box.activate(next_one)
	song_box.selection_set(next_one, last=None)

#play previous song in playlist
def previous_song():
	#reset slider and status bar
	my_slider.config(value=0)
	status_bar.config(text='')

	#get current song tupple no
	next_one = song_box.curselection()
	#add one to current song number
	next_one = next_one[0]-1
	#grab song by name from playlist
	song = song_box.get(next_one)

	song = f'E:/Project/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#move active bar in playlist
	song_box.selection_clear(0, END)
	song_box.activate(next_one)
	song_box.selection_set(next_one, last=None)

#Delete A song
def delete_song():
	stop()
	song_box.delete(ANCHOR)
	pygame.mixer.music.stop()

#Delete All songs from playlist
def delete_all_songs():
	stop()
	#will delete all songs of playlist
	song_box.delete(0, END)
	pygame.mixer.music.stop()

#create global pause
global paused
paused = False

#pause and unpause current song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True

#create slider
def slide(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'E:/Project/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())
	#current_volume = pygame.mixer.music.get_volume()

#create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

#playlist box
song_box =Listbox(master_frame, bg="black", fg="blue", width=100,height=25,selectbackground="blue", selectforeground="black")
song_box.grid(row=0,column=0)

#Define control buttons
back_btn_img=PhotoImage(file='E:Project/Backward.png')
forward_btn_img=PhotoImage(file='E:Project/Forward.png')
play_btn_img=PhotoImage(file='E:Project/Play.png')
pause_btn_img=PhotoImage(file='E:Project/Pause.png')
stop_btn_img=PhotoImage(file='E:Project/Stop.png')

#control frame
controls_frame= Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20) 

#create Control buttons
back_button=Button(controls_frame, image=back_btn_img, borderwidth=0,command=previous_song)
forward_button=Button(controls_frame, image=forward_btn_img, borderwidth=0,command=next_song)
play_button=Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button=Button(controls_frame, image=pause_btn_img, borderwidth=0, command= lambda:pause(paused))
stop_button=Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

#add many song to playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

#Create Delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From playlist", command=delete_all_songs)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM,ipady=2)

my_slider = ttk.Scale(master_frame, from_=0, to=100 , orient=HORIZONTAL, value=0, length=600, command=slide)
my_slider.grid(row=2,column=0,pady=10)

#create volume frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0,column=1,padx=40)
#create volume silder
volume_slider = ttk.Scale(volume_frame, from_=1, to=0 , orient=VERTICAL, value=1, length=300, command=volume)
volume_slider.pack(pady=10)


root.mainloop()