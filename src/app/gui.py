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
        
        # Text display area - use a frame with label for non-scrollable display
        self.text_display_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        self.text_display_frame.grid(row=3, column=0, padx=40, pady=20, sticky="ew")
        self.text_display_frame.grid_propagate(False)
        
        self.text_display = ctk.CTkLabel(
            self.text_display_frame,
            text="Select a file to begin",
            font=ctk.CTkFont(family="Courier", size=32),
            fg_color="white",
            text_color="black"
        )
        self.text_display.place(relx=0.5, rely=0.5, anchor="center")
        
        # Citation style selector
        citation_frame = ctk.CTkFrame(self, fg_color="white")
        citation_frame.grid(row=4, column=0, padx=20, pady=(10, 10))
        
        self.citation_label = ctk.CTkLabel(
            citation_frame,
            text="Citation Style:",
            font=ctk.CTkFont(size=12),
            text_color="black",
            fg_color="white"
        )
        self.citation_label.grid(row=0, column=0, padx=(0, 10))
        
        # Citation style variable
        self.citation_style = ctk.StringVar(value="none")
        
        # Citation style radio buttons
        citation_options = [
            ("None", "none"),
            ("Notes", "notes"),
            ("Parenthesis", "parenthesis"),
            ("Numeric", "numeric")
        ]
        
        for idx, (text, value) in enumerate(citation_options):
            radio_btn = ctk.CTkRadioButton(
                citation_frame,
                text=text,
                variable=self.citation_style,
                value=value,
                font=ctk.CTkFont(size=12),
                text_color="black",
                fg_color="black",
                hover_color="gray30"
            )
            radio_btn.grid(row=0, column=idx+1, padx=5)
        
        # Controls
        controls_frame = ctk.CTkFrame(self, fg_color="white")
        controls_frame.grid(row=5, column=0, padx=20, pady=(0, 10))
        
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
                # Get the selected citation style
                citation_style = self.citation_style.get()
                words = extract_text(file_path, citation_style)
                if words:
                    self.word_list = words
                    self.current_word_index = 0
                    # Clear display frame
                    for widget in self.text_display_frame.winfo_children():
                        widget.destroy()
                    # Show status
                    status_label = ctk.CTkLabel(
                        self.text_display_frame,
                        text=f"{len(words)} words loaded",
                        font=ctk.CTkFont(family="Courier", size=32),
                        fg_color="white",
                        text_color="black"
                    )
                    status_label.place(relx=0.5, rely=0.5, anchor="center")
                else:
                    for widget in self.text_display_frame.winfo_children():
                        widget.destroy()
                    error_label = ctk.CTkLabel(
                        self.text_display_frame,
                        text="Error loading file",
                        font=ctk.CTkFont(family="Courier", size=32),
                        fg_color="white",
                        text_color="black"
                    )
                    error_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                # For Word files and others, show a message
                for widget in self.text_display_frame.winfo_children():
                    widget.destroy()
                msg_label = ctk.CTkLabel(
                    self.text_display_frame,
                    text="Format not supported yet",
                    font=ctk.CTkFont(family="Courier", size=32),
                    fg_color="white",
                    text_color="black"
                )
                msg_label.place(relx=0.5, rely=0.5, anchor="center")
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
        for widget in self.text_display_frame.winfo_children():
            widget.destroy()
        self.show_next_word()
    
    def show_next_word(self):
        """Display the next word in the sequence."""
        if not self.is_reading or self.current_word_index >= len(self.word_list):
            # Reading finished or stopped
            if self.current_word_index >= len(self.word_list):
                self.text_display.configure(text="Reading complete!")
                print("Reading complete!")
            self.stop_reading()
            return
        
        # Display current word with center letter highlighted
        current_word = self.word_list[self.current_word_index]
        
        # Calculate center position of the word
        word_length = len(current_word)
        center_index = word_length // 2
        
        # Split word into parts
        before = current_word[:center_index]
        center_letter = current_word[center_index]
        after = current_word[center_index + 1:]
        
        # Create the display text with red letter using unicode or simple concatenation
        # Since we can't color individual letters in a label, we'll use three separate labels
        # positioned horizontally
        self.update_word_display(before, center_letter, after)
        
        # Move to next word
        self.current_word_index += 1
        
        # Calculate delay in milliseconds (60000 ms per minute / WPM)
        delay_ms = int(60000 / self.reading_speed_wpm)
        
        # Schedule next word
        self.after(delay_ms, self.show_next_word)
    
    def update_word_display(self, before, center, after):
        """Update the word display with colored center letter."""
        # Clear any existing word widgets
        for widget in self.text_display_frame.winfo_children():
            widget.destroy()
        
        # Create labels for each part with monospace font
        font = ctk.CTkFont(family="Courier", size=32)
        
        # Get frame width to calculate center position
        self.text_display_frame.update_idletasks()
        frame_center_x = self.text_display_frame.winfo_width() / 2
        
        # With monospace font, estimate character width (roughly 0.6 * font size)
        char_width = 19  # Approximate for Courier size 32
        
        # Calculate pixel positions
        # Center letter should be at frame_center_x
        center_label = ctk.CTkLabel(
            self.text_display_frame, 
            text=center, 
            font=font, 
            fg_color="white", 
            text_color="red"
        )
        center_label.place(x=frame_center_x, y=50, anchor="center")
        
        # Before text ends just before center letter
        if before:
            before_width = len(before) * char_width
            before_label = ctk.CTkLabel(
                self.text_display_frame, 
                text=before, 
                font=font, 
                fg_color="white", 
                text_color="black"
            )
            before_label.place(x=frame_center_x - char_width/2, y=50, anchor="e")
        
        # After text starts just after center letter
        if after:
            after_label = ctk.CTkLabel(
                self.text_display_frame, 
                text=after, 
                font=font, 
                fg_color="white", 
                text_color="black"
            )
            after_label.place(x=frame_center_x + char_width/2, y=50, anchor="w")
    
    def stop_reading(self):
        """Stop the speed reading session."""
        self.is_reading = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        print("Reading stopped")
    
    def run(self):
        """Start the application main loop."""
        self.mainloop()
