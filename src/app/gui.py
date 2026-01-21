"""
SpeedRead - GUI module
Contains the main application window and GUI components.
"""

import customtkinter as ctk
from typing import Optional
from .text_extractor import extract_text
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("Warning: tkinterdnd2 not installed. Drag and drop will not work.")
    print("Install with: pip install tkinterdnd2")


class SpeedReadApp(ctk.CTk):
    """Main application window for SpeedRead."""
    
    def __init__(self):
        super().__init__()
        
        # Try to enable drag and drop support
        if DRAG_DROP_AVAILABLE:
            try:
                self.drop_target_register(DND_FILES)
            except:
                pass
        
        # Configure window
        self.title("SpeedRead")
        self.geometry("800x600")
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create title label (spans both columns)
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="SpeedRead",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        # Create left frame for file selection
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.grid(row=1, column=0, padx=(20, 10), pady=20, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)
        
        # File selection title
        self.file_label = ctk.CTkLabel(
            self.left_frame,
            text="Select File",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.file_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Drop zone
        self.drop_zone = ctk.CTkTextbox(
            self.left_frame,
            width=250,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        self.drop_zone.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.drop_zone.insert("1.0", "Drop a file here\n\n(Text, Word, or PDF)\n\nor\n\nClick 'Choose File' below")
        self.drop_zone.configure(state="disabled")
        
        # Enable drag and drop on the drop zone
        if DRAG_DROP_AVAILABLE:
            try:
                self.drop_zone.drop_target_register(DND_FILES)
                self.drop_zone.dnd_bind('<<Drop>>', self.on_drop)
            except Exception as e:
                print(f"Could not enable drag and drop: {e}")
        
        # Choose file button
        self.choose_file_button = ctk.CTkButton(
            self.left_frame,
            text="Choose File",
            command=self.choose_file,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.choose_file_button.grid(row=2, column=0, padx=20, pady=(10, 20))
        
        # Selected file label
        self.selected_file_label = ctk.CTkLabel(
            self.left_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.selected_file_label.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        # Create right frame for text display
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)
        
        # Text display title
        self.display_label = ctk.CTkLabel(
            self.right_frame,
            text="Text Display",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.display_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Text display area
        self.text_display = ctk.CTkTextbox(
            self.right_frame,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        self.text_display.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.text_display.tag_config("center", justify="center")
        self.text_display.tag_config("red", foreground="red")
        self.text_display.insert("1.0", "Welcome to SpeedRead!\n\nSelect a file to begin.", "center")
        
        # Create control frame (spans both columns, at bottom)
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        # Create speed slider
        self.speed_label = ctk.CTkLabel(
            self.control_frame,
            text="Reading Speed (WPM):",
            font=ctk.CTkFont(size=14)
        )
        self.speed_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.speed_entry = ctk.CTkEntry(
            self.control_frame,
            width=100,
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.speed_entry.insert(0, "120")
        self.speed_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Create buttons
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20))
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Reading",
            command=self.start_reading,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="Stop",
            command=self.stop_reading,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.is_reading = False
        self.selected_file_path = None
        self.word_list = []
        self.current_word_index = 0
        self.reading_speed_wpm = 120  # Words per minute
    
    def on_drop(self, event):
        """Handle file drop event."""
        # Get the dropped file path
        file_path = event.data
        # Remove curly braces if present (Windows format)
        file_path = file_path.strip('{}').strip()
        
        if file_path:
            self.load_file(file_path)
    
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
                    self.text_display.insert("1.0", f"File loaded: {len(words)} words\nPress 'Start Reading' to begin", "center")
                else:
                    self.text_display.delete("1.0", "end")
                    self.text_display.insert("1.0", f"Error: Could not extract text from {file_type} file.", "center")
            else:
                # For Word files and others, show a message
                self.text_display.delete("1.0", "end")
                self.text_display.insert("1.0", f"{file_type} file selected: {filename}\n\n"
                                        f"Processing for {file_type} files will be implemented soon.", "center")
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
