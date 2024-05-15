import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper
import threading

# List of available models
models = ["tiny", "base", "large", "extra_large"]

# Create an instance of the Whisper model
model = whisper.load_model(models[1])

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        threading.Thread(target=transcribe_file, args=(file_path,)).start()

def transcribe_file(file_path):
    display_transcription("Transcribing...", False)
    try:
        # Start the progress bar
        progress_bar.start()
        result = model.transcribe(file_path)
        display_transcription(result["text"])
        # Stop the progress bar
        progress_bar.stop()
    except Exception as e:
        display_transcription('Error occurred during transcription')
        progress_bar.stop()
        messagebox.showerror("Error", f"An error occurred during transcription: {str(e)}")

def display_transcription(text, dot = True):
    if dot:
        formatted_text = text.replace('.', '.\n')
    else:
        formatted_text = text
    transcription_text.config(state=tk.NORMAL)
    transcription_text.delete(1.0, tk.END)
    transcription_text.insert(tk.END, formatted_text)
    transcription_text.config(state=tk.DISABLED)

def copy_transcription():
    root.clipboard_clear()
    root.clipboard_append(transcription_text.get(1.0, tk.END))

def change_model(event):
    global model
    model = whisper.load_model(model_choice.get())

# Create the Tkinter interface
root = tk.Tk()
root.resizable(False, False)
root.title("MP3 File Analysis with Whisper")
root.configure(bg='light grey')

# Add a frame for the button and the combobox
frame1 = tk.Frame(root, bg='light grey')
frame1.pack(pady=20)

# Add a button to upload the file
upload_button = tk.Button(frame1, text="Upload MP3 File", command=upload_file, font=('Arial', 12), width=25)
upload_button.pack(side=tk.LEFT, padx=10)

# Add a dropdown menu to choose the model
model_choice = ttk.Combobox(frame1, values=models, state="readonly", font=('Arial', 14), width=20)
model_choice.current(1)  # set initial model
model_choice.bind("<<ComboboxSelected>>", change_model)
model_choice.pack(side=tk.LEFT, padx=10)

style = ttk.Style()
style.configure("TProgressbar", thickness=25, relief='flat', background='#0f0')

# Add a progress bar
progress_bar = ttk.Progressbar(root, length=200, mode='indeterminate')
progress_bar.pack(pady=20)
# Add a text area to display the transcription

label = tk.Label(root, text="Transcription", font=('Arial', 16), bg='light grey')
label.pack()

# Ajoutez un cadre pour la zone de texte et la barre de défilement
frame2 = tk.Frame(root, bg='light grey')
frame2.pack(fill=tk.BOTH, expand=True)

# Ajoutez une zone de texte pour afficher la transcription
transcription_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, width=80, height=20, font=('Arial', 14))
transcription_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Ajoutez un bouton pour copier la transcription
copy_button = tk.Button(root, text="Copy Transcription", command=copy_transcription, font=('Arial', 14), bg='green', fg='white')
copy_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')



# Start the Tkinter main loop
root.mainloop()