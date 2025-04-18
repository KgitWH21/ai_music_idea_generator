import tkinter as tk
import json
import random
import os
import pyperclip
from tkinter import messagebox

class MusicIdeaGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Idea Generator")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c2c2c")
        
        # Set app title
        title_label = tk.Label(
            root, 
            text="AI Music Idea Generator", 
            font=("Helvetica", 24, "bold"),
            fg="#ffffff",
            bg="#2c2c2c"
        )
        title_label.pack(pady=20)
        
        # Create frame for buttons
        button_frame = tk.Frame(root, bg="#2c2c2c")
        button_frame.pack(pady=10)
        
        # Generate button
        self.generate_button = tk.Button(
            button_frame,
            text="Generate Music Idea",
            command=self.generate_idea,
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2
        )
        self.generate_button.pack(side=tk.LEFT, padx=10)
        
        # Copy button
        self.copy_button = tk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=("Helvetica", 12),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2
        )
        self.copy_button.pack(side=tk.LEFT, padx=10)
        
        # Text area for displaying ideas
        self.text_frame = tk.Frame(root, bg="#2c2c2c")
        self.text_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)
        
        self.idea_text = tk.Text(
            self.text_frame,
            font=("Arial", 14),  # Changed from Courier 12 to Arial 14
            bg="#2a2a2a",        # Darker background for more contrast
            fg="#e0e0e0",        # Slightly softer white for less eye strain
            wrap=tk.WORD,
            height=20,
            width=60
        )
        self.idea_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.idea_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.idea_text.yview)
        self.idea_text.config(yscrollcommand=scrollbar.set)
        
        # Current idea storage
        self.current_idea = ""
        
        # Initialize music data
        self.load_music_data()
        
        # Configure text tags for formatting
        self.setup_text_tags()
        
        # Generate initial idea
        self.generate_idea()
    
    def load_music_data(self):
        """Load the music elements from JSON file"""
        # Check if the file exists, if not, create it
        if not os.path.exists("music_elements.json"):
            self.create_default_json()
            
        try:
            with open("music_elements.json", "r") as file:
                self.music_data = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load music data: {str(e)}")
            self.create_default_json()
            with open("music_elements.json", "r") as file:
                self.music_data = json.load(file)
    
    def create_default_json(self):
        """Create a default JSON file with music elements"""
        default_data = {
            "styles": [
                "Lo-Fi", "EDM", "Synthwave", "Hip Hop", "Trap", "Jazz", "Classical", 
                "Rock", "Indie", "Folk", "Country", "R&B", "Soul", "Funk", "Disco", 
                "House", "Techno", "Dubstep", "Drum & Bass", "Ambient", "Chillout", 
                "Orchestral", "Cinematic", "Experimental", "Metal", "Punk", "Reggae", 
                "Latin", "Afrobeat", "World Music", "Blues", "Gospel", "Acoustic"
            ],
            "genres": [
                "Progressive", "Future", "Deep", "Tropical", "Melodic", "Hard", 
                "Glitch", "Dark", "Ethereal", "Psychedelic", "Minimal", "Maximalist", 
                "Neoclassical", "Alternative", "Contemporary", "Traditional", "Fusion", 
                "Abstract", "Atmospheric", "Nostalgic", "Dystopian", "Utopian", 
                "Cyberpunk", "Vaporwave", "Hyperpop", "Industrial", "Organic"
            ],
            "emotions": [
                "Joyful", "Sad", "Hopeful", "Melancholic", "Anxious", "Calm", 
                "Energetic", "Contemplative", "Aggressive", "Peaceful", "Nostalgic", 
                "Triumphant", "Solemn", "Playful", "Mysterious", "Romantic", "Tense", 
                "Euphoric", "Bittersweet", "Dreamy", "Chaotic", "Serene", "Ominous", 
                "Whimsical", "Epic", "Introspective", "Passionate", "Vulnerable"
            ],
            "instrumentation_highs": [
                "Bell synths", "High piano notes", "Flutes", "Violin", "High-pitched pads", 
                "Chimes", "Glockenspiel", "Piccolo", "High guitar notes", "Whistles", 
                "Reverse cymbals", "High-passed noise", "Triangle", "High-pitched vocals", 
                "Bells", "Harpsichord", "Music box", "Kalimba", "High synth arps"
            ],
            "instrumentation_mids": [
                "Piano", "Guitar", "Saxophone", "Trumpet", "Synth leads", "Vocal chops", 
                "Electric piano", "Viola", "Clarinet", "Organ", "Pad synths", "Cello", 
                "Synth pads", "Trombone", "Synthesizers", "Electric guitar", "Oboe"
            ],
            "instrumentation_lows": [
                "Bass guitar", "808 bass", "Synthesized sub bass", "Cello", "Double bass", 
                "Tuba", "Baritone sax", "Low piano notes", "Timpani", "Taiko drums", 
                "Analog bass synth", "Booming kicks", "Sub drops", "Contrabassoon"
            ],
            "ear_candy": [
                "Reversed audio snippets", "Granular texture bursts", "Vinyl crackle", 
                "Tape hiss", "Field recordings", "Foley sounds", "Water droplets", 
                "Glitch effects", "Bitcrushed transitions", "Risers and falls", 
                "Record scratches", "Voice samples", "Nature sounds", "Industrial noise", 
                "Radio static", "Vocoders", "Ring modulation", "Atmospheric samples", 
                "Comb filtered noise", "Frequency modulated drones"
            ],
            "vocal_effects": [
                "Vocoder", "Auto-Tune", "Reverb", "Delay", "Chorus", "Formant shifting", 
                "Pitch shifting", "Granular processing", "Distortion", "Harmonizer", 
                "Spectral processing", "Sidechain compression", "Stutter edits", 
                "Tape emulation", "Robotic processing", "Whisper layers", "Time stretching", 
                "None (clean vocals)", "Filtered vocals", "Reverse vocals"
            ],
            "chord_progressions": [
                "I-V-vi-IV (Pop progression)", 
                "ii-V-I (Jazz progression)", 
                "I-IV-V (Blues progression)",
                "vi-IV-I-V (Andalusian cadence)",
                "i-bVI-bIII-bVII (Minor progression)",
                "I-vi-IV-V (50s progression)",
                "I-bVII-IV (Mixolydian vamp)",
                "i-iv-V (Minor blues)",
                "I-iii-IV-vi (Dream pop progression)",
                "i-VII-VI-VII (Dorian progression)",
                "I-V-bVII-IV (Rock progression)",
                "i-bIII-IV-bVI (Epic minor)",
                "i-bVI-bVII (Aeolian progression)",
                "I-ii-iii-IV (Ascending progression)",
                "IV-V-bVII-I (Lydian cadence)",
                "vi-bVII-bIII-bVI (Modal interchange)"
            ],
            "melody_ideas": [
                "Pentatonic scale runs", 
                "Chromatic passing tones",
                "Modal melody using Dorian scale",
                "Lydian mode for bright melodies",
                "Phrygian mode for exotic feel",
                "Call and response phrases",
                "Recurring motif with variations",
                "Wide interval jumps",
                "Stepwise motion",
                "Arpeggio-based melody",
                "Blues scale licks",
                "Rhythmic repetition of single note",
                "Descending melodic sequence",
                "Harmonized parallel thirds",
                "Fragmented, glitchy phrases",
                "Countermelody against main theme",
                "Tension-building dissonance resolving to consonance",
                "Melody derived from speech patterns"
            ],
            "ambience_ideas": [
                "Distant thunder with reverb",
                "Urban soundscapes with filtering",
                "Natural water sounds processed through granular synthesis",
                "Reversed cymbal swells",
                "Stretched and pitched down instrumental sounds",
                "Ambient crowd noise with delay",
                "Filtered traffic sounds",
                "Wind through trees with spectral processing",
                "Resonant drone layers",
                "Room tone from interesting acoustic spaces",
                "Processed mechanical sounds",
                "Layered atmospheric pads",
                "Convolution reverb with unusual impulse responses",
                "Timestretched textural elements",
                "Subtle field recordings",
                "Tape loops with varying degradation",
                "Processed radio transmissions",
                "Orchestral samples with extreme time-stretching"
            ]
        }
        
        with open("music_elements.json", "w") as file:
            json.dump(default_data, file, indent=4)
    
    def setup_text_tags(self):
        """Configure text tags for formatting the output"""
        self.idea_text.tag_configure("title", font=("Arial", 16, "bold"), foreground="#4CAF50", justify="center")
        self.idea_text.tag_configure("header", font=("Arial", 14, "bold"), foreground="#2196F3")
        self.idea_text.tag_configure("subheader", font=("Arial", 13, "bold"), foreground="#03A9F4")
        self.idea_text.tag_configure("content", font=("Arial", 14), foreground="#e0e0e0")
        self.idea_text.tag_configure("highlight", font=("Arial", 14, "bold"), foreground="#FFC107")
        self.idea_text.tag_configure("divider", font=("Arial", 14), foreground="#757575")
    
    def generate_idea(self):
        """Generate a random music idea"""
        try:
            # Select random elements
            styles = random.sample(self.music_data["styles"], 2)
            genres = random.sample(self.music_data["genres"], 2)
            emotion = random.choice(self.music_data["emotions"])
            
            # Instrumentation
            high_instr = random.sample(self.music_data["instrumentation_highs"], min(3, len(self.music_data["instrumentation_highs"])))
            mid_instr = random.sample(self.music_data["instrumentation_mids"], min(3, len(self.music_data["instrumentation_mids"])))
            low_instr = random.sample(self.music_data["instrumentation_lows"], min(2, len(self.music_data["instrumentation_lows"])))
            
            # Effects and techniques
            ear_candy = random.sample(self.music_data["ear_candy"], min(3, len(self.music_data["ear_candy"])))
            vocal_effect = random.choice(self.music_data["vocal_effects"])
            
            # Musical structure elements
            chord_progression = random.choice(self.music_data["chord_progressions"])
            melody_idea = random.choice(self.music_data["melody_ideas"])
            ambience_idea = random.choice(self.music_data["ambience_ideas"])
            
            # Clear the text area
            self.idea_text.delete(1.0, tk.END)
            
            # Insert formatted text with tags
            divider = "=" * 42 + "\n"
            
            # Title section
            self.idea_text.insert(tk.END, divider, "divider")
            self.idea_text.insert(tk.END, "AI MUSIC IDEA\n", "title")
            self.idea_text.insert(tk.END, divider, "divider")
            
            # Core elements
            self.idea_text.insert(tk.END, "\n>> STYLE FUSION: ", "header")
            self.idea_text.insert(tk.END, f"{styles[0]} + {styles[1]}\n", "highlight")
            
            self.idea_text.insert(tk.END, ">> GENRE EXPLORATION: ", "header")
            self.idea_text.insert(tk.END, f"{genres[0]} + {genres[1]}\n", "highlight")
            
            self.idea_text.insert(tk.END, ">> EMOTIONAL QUALITY: ", "header")
            self.idea_text.insert(tk.END, f"{emotion}\n\n", "highlight")
            
            # Instrumentation section
            self.idea_text.insert(tk.END, "INSTRUMENTATION:\n", "subheader")
            self.idea_text.insert(tk.END, "• Highs: ", "header")
            self.idea_text.insert(tk.END, f"{', '.join(high_instr)}\n", "content")
            self.idea_text.insert(tk.END, "• Mids: ", "header")
            self.idea_text.insert(tk.END, f"{', '.join(mid_instr)}\n", "content")
            self.idea_text.insert(tk.END, "• Lows: ", "header")
            self.idea_text.insert(tk.END, f"{', '.join(low_instr)}\n\n", "content")
            
            # Special elements section
            self.idea_text.insert(tk.END, "SPECIAL ELEMENTS:\n", "subheader")
            self.idea_text.insert(tk.END, "• Ear Candy/SFX: ", "header")
            self.idea_text.insert(tk.END, f"{', '.join(ear_candy)}\n", "content")
            self.idea_text.insert(tk.END, "• Vocal Processing: ", "header")
            self.idea_text.insert(tk.END, f"{vocal_effect}\n\n", "content")
            
            # Musical structure section
            self.idea_text.insert(tk.END, "MUSICAL STRUCTURE:\n", "subheader")
            self.idea_text.insert(tk.END, "• Chord Progression: ", "header")
            self.idea_text.insert(tk.END, f"{chord_progression}\n", "content")
            self.idea_text.insert(tk.END, "• Melody Approach: ", "header")
            self.idea_text.insert(tk.END, f"{melody_idea}\n", "content")
            self.idea_text.insert(tk.END, "• Ambience/Atmosphere: ", "header")
            self.idea_text.insert(tk.END, f"{ambience_idea}\n", "content")
            
            self.idea_text.insert(tk.END, divider, "divider")
            
            # Create the plain text version for clipboard
            idea = f"""==========================================
AI MUSIC IDEA
==========================================

>> STYLE FUSION: {styles[0]} + {styles[1]}
>> GENRE EXPLORATION: {genres[0]} + {genres[1]}
>> EMOTIONAL QUALITY: {emotion}

INSTRUMENTATION:
• Highs: {', '.join(high_instr)}
• Mids: {', '.join(mid_instr)}
• Lows: {', '.join(low_instr)}

SPECIAL ELEMENTS:
• Ear Candy/SFX: {', '.join(ear_candy)}
• Vocal Processing: {vocal_effect}

MUSICAL STRUCTURE:
• Chord Progression: {chord_progression}
• Melody Approach: {melody_idea}
• Ambience/Atmosphere: {ambience_idea}
=========================================="""
            
            # Store current idea for clipboard
            self.current_idea = idea
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate idea: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy the current idea to clipboard"""
        if self.current_idea:
            pyperclip.copy(self.current_idea)
            messagebox.showinfo("Success", "Music idea copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate an idea first!")

def main():
    root = tk.Tk()
    app = MusicIdeaGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()