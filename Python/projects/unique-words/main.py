import re
import sys
from textual.app import App, ComposeResult
from textual.widgets import Header, Label
from textual.containers import ScrollableContainer

class UniqueWords(App):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Header() # widget from Textual
        with ScrollableContainer(id="results"):
            # open file and count words
            try:
                with open(self.filename, 'r') as file:
                    content = file.read().lower()
                    words = re.findall(r'\w+', content) # first arg is regex for words (raw)
                    
                    # Count frequencies
                    word_counts = {}
                    for word in words:
                        word_counts[word] = word_counts.get(word, 0) + 1
                    
                    # sort and output
                    yield Label(f"No. of unique words: {len(words)}")
                    
                    for word, count in sorted(word_counts.items(), key=lambda x: x[0]): # for every word, return a Label component
                        yield Label(f"{word} - {count}")
            
            except FileNotFoundError:
                yield Label(f"Error: File {self.filename} not found")
            except Exception as e:
                yield Label(f"Error: {str(e)}")
    
if len(sys.argv) != 2:
    print("Usage: python3 main.py <filename>")
    exit();
    
app = UniqueWords(sys.argv[1])
app.run()

