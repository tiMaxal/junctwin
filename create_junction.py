"""
Windows Junction Creator for 'Send To' Menu
Creates junction points between the current folder and a chosen target folder.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


class JunctionCreatorGUI:
    def __init__(self, source_folder):
        self.source_folder = Path(source_folder).resolve()
        self.target_folder = None
        self.direction = tk.StringVar(value="to_source")
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("junctwin")
        self.root.geometry("550x300"
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#0078D4", height=50)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        title_label = tk.Label(title_frame, text="junctwin", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="#0078D4", fg="white")
        title_label.pack(pady=10)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source folder display
        source_label = tk.Label(content_frame, text="Current Folder:", 
                               font=("Segoe UI", 9, "bold"))
        source_label.pack(anchor=tk.W)
        
        source_text = tk.Text(content_frame, height=2, wrap=tk.WORD, 
                             font=("Segoe UI", 9), bg="#F0F0F0", 
                             relief=tk.FLAT, padx=5, pady=5)
        source_text.pack(fill=tk.X, pady=(2, 15))
        source_text.insert(1.0, str(self.source_folder))
        source_text.config(state=tk.DISABLED)
        
        # Direction options
        direction_frame = tk.LabelFrame(content_frame, text="Junction Direction", 
                                       font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        direction_frame.pack(fill=tk.X, pady=(0, 15))
        
        rb1 = tk.Radiobutton(direction_frame, 
                            text="Create junction IN current folder → pointing TO target folder",
                            variable=self.direction, value="to_target",
                            font=("Segoe UI", 9))
        rb1.pack(anchor=tk.W, pady=2)
        
        rb2 = tk.Radiobutton(direction_frame,
                            text="Create junction IN target folder → pointing TO current folder",
                            variable=self.direction, value="to_source",
                            font=("Segoe UI", 9))
        rb2.pack(anchor=tk.W, pady=2)
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        select_btn = tk.Button(button_frame, text="Select Target Folder", 
                              command=self.select_target,
                              font=("Segoe UI", 9, "bold"),
                              bg="#0078D4", fg="white",
                              padx=20, pady=8,
                              cursor="hand2")
        select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=self.root.quit,
                              font=("Segoe UI", 9),
                              padx=20, pady=8,
                              cursor="hand2")
        cancel_btn.pack(side=tk.RIGHT)
        
    def select_target(self):
        """Open folder picker and create junction"""
        target = filedialog.askdirectory(
            title="Select Target Folder",
            initialdir=self.source_folder.parent
        )
        
        if not target:
            return
            
        self.target_folder = Path(target).resolve()
        
        # Validate folders are different
        if self.target_folder == self.source_folder:
            messagebox.showerror("Error", 
                               "Source and target folders must be different!")
            return
        
        # Create the junction based on selected direction
        self.create_junction()
        
    def create_junction(self):
        """Create the junction point"""
        try:
            if self.direction.get() == "to_target":
                # Create junction IN source pointing TO target
                junction_name = f"{self.target_folder.name}[junct]"
                junction_path = self.source_folder / junction_name
                target_path = self.target_folder
                location_desc = f"in {self.source_folder.name}"
            else:  # to_source
                # Create junction IN target pointing TO source
                junction_name = f"{self.source_folder.name}[junct]"
                junction_path = self.target_folder / junction_name
                target_path = self.source_folder
                location_desc = f"in {self.target_folder.name}"
            
            # Check if junction already exists
            if junction_path.exists():
                response = messagebox.askyesno(
                    "Junction Exists",
                    f"'{junction_name}' already exists {location_desc}.\n\n"
                    f"Do you want to delete it and create a new junction?"
                )
                if not response:
                    return
                
                # Remove existing junction
                if junction_path.is_dir():
                    os.rmdir(junction_path)
                else:
                    junction_path.unlink()
            
            # Create junction using mklink
            cmd = f'mklink /J "{junction_path}" "{target_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo(
                    "Success", 
                    f"Junction created successfully!\n\n"
                    f"Junction: {junction_path}\n"
                    f"Points to: {target_path}"
                )
                self.root.quit()
            else:
                error_msg = result.stderr or result.stdout
                messagebox.showerror("Error", 
                                   f"Failed to create junction:\n{error_msg}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create junction:\n{str(e)}")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()
        self.root.destroy()


def main():
    # Check if running with administrator privileges
    try:
        if not os.path.exists(sys.argv[1]):
            messagebox.showerror("Error", 
                               f"Folder not found: {sys.argv[1]}")
            sys.exit(1)
    except IndexError:
        messagebox.showerror("Error", 
                           "No folder specified!\n\n"
                           "This script should be called from the 'Send To' menu.")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    
    # Verify it's a directory
    if not os.path.isdir(source_folder):
        messagebox.showerror("Error", 
                           "Please select a folder, not a file!")
        sys.exit(1)
    
    # Create and run GUI
    app = JunctionCreatorGUI(source_folder)
    app.run()


if __name__ == "__main__":
    main()
