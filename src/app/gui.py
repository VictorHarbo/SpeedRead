"""
SpeedRead - GUI module
Contains the main application window and GUI components.
"""

import customtkinter as ctk
from tkinter import PhotoImage
import os
from .text_extractor import extract_text


class SpeedReadApp(ctk.CTk):
    """Main application window for SpeedRead."""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("SpeedRead")
        
        # Set application icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "speedreadLogo_white_large.png")
            icon = PhotoImage(file=icon_path)
            self.iconphoto(True, icon)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Center window on screen
        window_width = 600
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set theme to light with white background
        ctk.set_appearance_mode("light")
        
        # Configure window background to white
        self.configure(fg_color="white")
        
        # Configure grid layout - single column
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="SpeedRead",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="black",
            fg_color="white"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        # Choose file button
        self.choose_file_button = ctk.CTkButton(
            self,
            text="Choose File",
            command=self.choose_file,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="black",
            hover_color="gray30"
        )
        self.choose_file_button.grid(row=1, column=0, padx=20, pady=10)
        
        # Selected file label
        self.selected_file_label = ctk.CTkLabel(
            self,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color="gray50",
            fg_color="white"
        )
        self.selected_file_label.grid(row=2, column=0, padx=20, pady=(0, 10))
        
        # Text display area
        self.text_display = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(size=32),
            fg_color="white",
            border_width=0,
            height=100
        )
        self.text_display.grid(row=3, column=0, padx=40, pady=20, sticky="ew")
        self.text_display.tag_config("center", justify="center")
        self.text_display.tag_config("red", foreground="red")
        self.text_display.insert("1.0", "Select a file to begin", "center")
        
        # Controls
        controls_frame = ctk.CTkFrame(self, fg_color="white")
        controls_frame.grid(row=4, column=0, padx=20, pady=(0, 10))
        
        self.speed_label = ctk.CTkLabel(
            controls_frame,
            text="WPM:",
            font=ctk.CTkFont(size=12),
            text_color="black",
            fg_color="white"
        )
        self.speed_label.grid(row=0, column=0, padx=(0, 5))
        
        self.speed_entry = ctk.CTkEntry(
            controls_frame,
            width=60,
            font=ctk.CTkFont(size=12),
            justify="center",
            fg_color="white",
            border_color="gray70"
        )
        self.speed_entry.insert(0, "300")
        self.speed_entry.grid(row=0, column=1, padx=5)
        
        self.start_button = ctk.CTkButton(
            controls_frame,
            text="Start",
            command=self.start_reading,
            width=80,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="black",
            hover_color="gray30"
        )
        self.start_button.grid(row=0, column=2, padx=5)
        
        self.stop_button = ctk.CTkButton(
            controls_frame,
            text="Stop",
            command=self.stop_reading,
            width=80,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="gray70",
            hover_color="gray50",
            state="disabled"
        )
        self.stop_button.grid(row=0, column=3, padx=5)
        
        self.is_reading = False
        self.selected_file_path = None
        self.word_list = []
        self.current_word_index = 0
        self.reading_speed_wpm = 120  # Words per minute
    
    def load_file(self, file_path):
        """Load a file and update the UI."""
        self.selected_file_path = file_path
        filename = file_path.split("/")[-1]
        file_extension = filename.split(".")[-1].lower()
        
        # Determine file type and log to console
        if file_extension == "txt":
            file_type = "text"
            print(f"Text file chosen: {filename}")
        elif file_extension in ["doc", "docx"]:
            file_type = "Word"
            print(f"Word file chosen: {filename}")
        elif file_extension == "pdf":
            file_type = "PDF"
            print(f"PDF file chosen: {filename}")
        else:
            file_type = "unknown"
            print(f"Unknown file type chosen: {filename}")
        
        self.selected_file_label.configure(text=f"Selected: {filename}", text_color="green")
        
        # Extract and display text based on file type
        try:
            if file_extension in ["txt", "pdf"]:
                # Use the text extractor for both text and PDF files
                words = extract_text(file_path)
                if words:
                    self.word_list = words
                    self.current_word_index = 0
                    self.text_display.delete("1.0", "end")
                    self.text_display.insert("1.0", f"{len(words)} words loaded", "center")
                else:
                    self.text_display.delete("1.0", "end")
                    self.text_display.insert("1.0", "Error loading file", "center")
            else:
                # For Word files and others, show a message
                self.text_display.delete("1.0", "end")
                self.text_display.insert("1.0", "Format not supported yet", "center")
        except Exception as e:
            self.selected_file_label.configure(text=f"Error: {str(e)}", text_color="red")
            print(f"Error loading file: {str(e)}")
    
    def choose_file(self):
        """Open file dialog to choose a text, Word, or PDF file."""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("Text files", "*.txt"),
                ("Word files", "*.doc *.docx"),
                ("PDF files", "*.pdf"),
                ("All supported files", "*.txt *.doc *.docx *.pdf"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path)
    
    def start_reading(self):
        """Start the speed reading session."""
        if not self.word_list:
            print("No text loaded. Please select a file first.")
            return
        
        # Get speed from entry box
        try:
            speed = int(self.speed_entry.get())
            if speed < 1:
                print("Speed must be at least 1 WPM")
                return
            self.reading_speed_wpm = speed
        except ValueError:
            print("Invalid speed value. Please enter a number.")
            return
        
        self.is_reading = True
        self.current_word_index = 0
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        print(f"Reading started at {self.reading_speed_wpm} WPM")
        
        # Clear display and show first word
        self.text_display.delete("1.0", "end")
        self.show_next_word()
    
    def show_next_word(self):
        """Display the next word in the sequence."""
        if not self.is_reading or self.current_word_index >= len(self.word_list):
            # Reading finished or stopped
            if self.current_word_index >= len(self.word_list):
                self.text_display.delete("1.0", "end")
                self.text_display.insert("1.0", "Reading complete!", "center")
                print("Reading complete!")
            self.stop_reading()
            return
        
        # Display current word with center letter highlighted
        current_word = self.word_list[self.current_word_index]
        self.text_display.delete("1.0", "end")
        
        # Calculate center position
        word_length = len(current_word)
        center_index = word_length // 2
        
        # Split word into three parts: before center, center letter, after center
        before = current_word[:center_index]
        center_letter = current_word[center_index]
        after = current_word[center_index + 1:]
        
        # Insert with center alignment
        self.text_display.insert("1.0", before + center_letter + after, "center")
        
        # Apply red color to the center letter
        # Calculate position in the text widget (1.0 is line 1, char 0)
        start_pos = f"1.{center_index}"
        end_pos = f"1.{center_index + 1}"
        self.text_display.tag_add("red", start_pos, end_pos)
        
        # Move to next word
        self.current_word_index += 1
        
        # Calculate delay in milliseconds (60000 ms per minute / WPM)
        delay_ms = int(60000 / self.reading_speed_wpm)
        
        # Schedule next word
        self.after(delay_ms, self.show_next_word)
    
    def stop_reading(self):
        """Stop the speed reading session."""
        self.is_reading = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        print("Reading stopped")
    
    def run(self):
        """Start the application main loop."""
        self.mainloop()
