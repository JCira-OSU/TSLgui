# TSLgui: A fun side-project by John Cira
# Created for use in CS 362 - Software Engineering II

import tkinter as tk
import subprocess
import os


class GUI:
    """Main GUI window for TSLgui"""

    def __init__(self):

        # Initialize I/O paths
        self._bin = ""
        self._binOK = False
        self._binpath = "./data/binpath.txt"
        self._input = "./data/specs.txt"
        self._output = "./data/specs.tsl.txt"

        # create root window
        self.root = tk.Tk()
        self.root.geometry("700x800")
        self.root.title("TSLgui")

        # ------------- Initialize gui widgets -------------------------------
        self.binEntryContainer = tk.Frame(self.root, relief="solid")
        self.binEntryContainer.grid(row=0, column=0)
        self.binConfirmation = tk.Label(
            self.binEntryContainer, text="Binary OK", fg="green"
        )
        self.binRejection = tk.Label(
            self.binEntryContainer, text="Binary error", fg="red"
        )
        self.generateButton = tk.Button(
            self.binEntryContainer, text="Generate!", command=self.generate
        )

        self.showManButton = tk.Button(
            self.root, text="Show Manpage", command=self.show_manpage
        )
        self.showManButton.grid(row=0, column=1)

        self.binEntryLabel = tk.Label(
            self.binEntryContainer, text="Enter path to binary"
        )
        self.binEntryLabel.pack(side="left")
        self.binEntry = tk.Entry(self.binEntryContainer)
        self.binEntry.bind("<Return>", self.set_bin)
        self.binEntry.pack(side="left")

        self.inputText = tk.Text(self.root, height="300")
        self.inputText.grid(row=1, column=0)
        self.outputText = tk.Text(self.root, height="300")
        self.outputText.grid(row=1, column=1)
        self.consoleText = tk.Text(self.root, height="60", width=600)
        self.consoleText.grid(row=2, column=0, columnspan=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(1, weight=5)
        self.root.grid_rowconfigure(2, weight=1)
        # --------------------------------------------------------------------

        # Attempt to restore last session
        try:
            with open(self._binpath, "r") as file:
                self.outputToConsole("\nBinary path found, restoring...")
                self.binEntry.insert(0, file.read().replace("\n", ""))
                self.set_bin(self)
            self.outputToConsole("\nFinished restoring.")
        except FileNotFoundError:
            self.outputToConsole("\nBinary path not found.")

        try:
            with open(self._input, "r") as file:
                self.outputToConsole("\nInput file found, restoring...")
                for line in file.readlines():
                    self.inputText.insert(tk.END, line)
            self.outputToConsole("\nFinished restoring.")
        except FileNotFoundError:
            message = f"Welcome to TSLgui!  How to use:\n\n \
0. !!! Make SURE ./data/ directory exists !!! \n\n \
1. Paste the path to the TSLgenerator binary for\n \
   your OS in the box above.\n\n \
2. Press <Return/Enter>\n\n \
3. If the file path is good (check spelling and\n \
   executable status), then both 'Binary OK' and\n \
   a 'Generate!' button will appear.\n\n \
4. Write your TSLgenerator specs in this left box.\n\n \
5. Click 'Generate!'\n\n \
6. Your specs will be written to {self._input}\n \
   before being passed to \n \
   {self._bin if self._bin != "" else "TSLgenerator."}\n \
   The output of TSLgenerator will then be written\n \
   to {self._output} and appear in\n \
   the right box.\n\n \
7. After you input your binary path, you\n \
   may also click 'Show Manpage' to see\n \
   TSLgenerator's manpage."

            self.inputText.insert(tk.END, message)
            self.outputToConsole("\nInput file not found.")

        try:
            with open(self._output, "r") as file:
                self.outputToConsole(
                    f"\nTSL output found at {self._output}, restoring..."
                )
                self.outputText.delete(1.0, tk.END)
                for line in file.readlines():
                    self.outputText.insert(tk.END, line)
            self.outputToConsole("\nFinished reading.")
        except FileNotFoundError:
            self.outputToConsole("\nNo TSL output to restore.")

        # Start main gui
        self.root.mainloop()

    def outputToConsole(self, text: str):
        """Helper method to send text to bottom of console and scroll to see it"""
        self.consoleText.insert(tk.END, text)
        self.consoleText.see(tk.END)

    def show_manpage(self):
        """'Show Manpage' button logic"""
        # If valid binary is not set, print error and return.
        if not self._binOK:
            self.outputToConsole("\nFix binary path first!")
            return

        # Log operations to console
        self.outputToConsole("\nOpening manpage...")

        # Initialize window
        self.manpageWindow = tk.Toplevel(self.root)
        self.manpageWindow.title("TSLgenerator Manpage")
        self.manpageWindow.geometry("500x500")

        # get manpage info from TSLgenerator
        command = [self._bin, "--manpage"]
        result = subprocess.run(command, capture_output=True, text=True)

        # Display window with manpage info
        self.manpageLabel = tk.Label(self.manpageWindow, text=result.stdout)
        self.manpageLabel.pack(padx=5, pady=5)

    def set_bin(self, event):
        """Binary path entry and validation logic"""
        # set variable so data is not somehow manipulated mid-logic
        tempPath = self.binEntry.get()

        # If the file exists and is executable
        if os.path.exists(tempPath) and os.access(tempPath, os.X_OK):

            # Set internal variables
            self._bin = tempPath
            self._binOK = True

            # Display confirmation text and show 'Generate!' button
            self.binRejection.pack_forget()
            self.binConfirmation.pack(side="left")
            self.generateButton.pack(side="right", padx=20)

            # save validated executable path for restoring next session
            with open(self._binpath, "w") as file:
                self.outputToConsole(f"\nSaving binary path to {self._binpath}")
                file.write(self._bin)
            self.outputToConsole("\nBinary path saved.")

        # If the file does not exist or is not executable
        else:
            # Clear internal variables
            self._bin = ""
            self._binOK = False

            # Display error text and hide 'Generate!' button
            self.binConfirmation.pack_forget()
            self.generateButton.pack_forget()
            self.binRejection.pack(side="left")

    def generate(self):
        """TSLgenerator I/O logic"""
        # If valid binary is not set, print error and return.
        if not self._binOK:
            self.outputToConsole("\nFix binary path first!")
            return

        with open(self._input, "w") as file:
            # Log operations to console
            self.outputToConsole(f"\nWriting input file to {self._output}")

            # Write input data to file
            file.write(self.inputText.get(1.0, tk.END))

        self.outputToConsole("\nFinished writing.")

        # Run TSLgenerator and log to console
        command = [self._bin, self._input, "-o", self._output]
        result = subprocess.run(command, capture_output=True, text=True)
        self.outputToConsole(result.stdout)

        # Open TSLgenerator output file
        try:
            with open(self._output, "r") as file:
                self.outputToConsole(
                    f"\nTSL output found at {self._output}, reading..."
                )

                # Remove old data from output textbox
                self.outputText.delete(1.0, tk.END)

                # Insert new data to output textbox
                for line in file.readlines():
                    self.outputText.insert(tk.END, line)

            # Log operations to console
            self.outputToConsole("\nFinished reading.")
        except FileNotFoundError:
            self.outputToConsole("\nTSL output not found.")
            self.outputText.insert(tk.END, "TSL output not found.\n")
            self.outputText.insert(tk.END, f"Check {self._output}\n")


if __name__ == "__main__":
    GUI()
