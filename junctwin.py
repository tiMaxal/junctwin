"""
Windows Junction/Hard Link Creator for 'Send To' Menu
Creates junction points for directories and hard links for files.
"""

import sys
import os
import subprocess
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(source_path):
    """Restart the script with administrator privileges"""
    try:
        script = sys.argv[0]
        params = f'"{source_path}"'
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to elevate privileges:\n{str(e)}")
        return False


class JunctionCreatorGUI:
    def __init__(self, source_path):
        self.source_path = Path(source_path).resolve()
        self.is_file = self.source_path.is_file()
        self.target_path = None
        
        # Create main window first
        self.root = tk.Tk()
        self.root.title("junctwin")
        self.root.geometry("550x300")
        self.root.resizable(False, False)
        
        # Initialize direction variable after root is created
        self.direction = tk.StringVar(value="to_source")
        
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
        
        # Source display
        source_type = "File" if self.is_file else "Folder"
        source_label = tk.Label(content_frame, text=f"Current {source_type}:", 
                               font=("Segoe UI", 9, "bold"))
        source_label.pack(anchor=tk.W)
        
        source_text = tk.Text(content_frame, height=2, wrap=tk.WORD, 
                             font=("Segoe UI", 9), bg="#F0F0F0", 
                             relief=tk.FLAT, padx=5, pady=5)
        source_text.pack(fill=tk.X, pady=(2, 15))
        source_text.insert(1.0, str(self.source_path))
        source_text.config(state=tk.DISABLED)
        
        # Direction options
        link_type = "hard link" if self.is_file else "junction"
        direction_frame = tk.LabelFrame(content_frame, text=f"{link_type.title()} Direction", 
                                       font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        direction_frame.pack(fill=tk.X, pady=(0, 15))
        
        if self.is_file:
            rb1_text = "Create link IN current file's folder → pointing TO target file"
            rb2_text = "Create link IN target file's folder → pointing TO current file"
        else:
            rb1_text = "Create junction IN current folder → pointing TO target folder"
            rb2_text = "Create junction IN target folder → pointing TO current folder"
        
        rb1 = tk.Radiobutton(direction_frame, 
                            text=rb1_text,
                            variable=self.direction, value="to_target",
                            font=("Segoe UI", 9))
        rb1.pack(anchor=tk.W, pady=2)
        
        rb2 = tk.Radiobutton(direction_frame,
                            text=rb2_text,
                            variable=self.direction, value="to_source",
                            font=("Segoe UI", 9))
        rb2.pack(anchor=tk.W, pady=2)
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        target_type = "File" if self.is_file else "Folder"
        select_btn = tk.Button(button_frame, text=f"Select Target {target_type}", 
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
        """Open file/folder picker and create link"""
        if self.is_file:
            if self.direction.get() == "to_target":
                # Creating link in current folder pointing to target file
                target = filedialog.askopenfilename(
                    title="Select Target File",
                    initialdir=self.source_path.parent
                )
            else:
                # Creating link in target folder pointing to current file
                target = filedialog.askdirectory(
                    title="Select Target Folder for Link",
                    initialdir=self.source_path.parent
                )
        else:
            target = filedialog.askdirectory(
                title="Select Target Folder",
                initialdir=self.source_path.parent
            )
        
        if not target:
            return
            
        self.target_path = Path(target).resolve()
        
        # Validate paths are different
        if self.target_path == self.source_path:
            messagebox.showerror("Error", 
                               "Source and target must be different!")
            return
        
        # For file + to_source: validate target is a folder
        if self.is_file and self.direction.get() == "to_source":
            if not self.target_path.is_dir():
                messagebox.showerror("Error", 
                                   "Please select a folder for the link location!")
                return
        
        # Create the link based on selected direction
        self.create_link()
        
    def create_link(self):
        """Create the junction point or hard link"""
        try:
            if self.is_file:
                # Determine link paths and target for files
                if self.direction.get() == "to_target":
                    # Create link IN source location pointing TO target file
                    # Check if cross-drive
                    source_drive = self.target_path.drive
                    link_drive = self.source_path.drive
                    is_cross_drive = source_drive.upper() != link_drive.upper()
                    link_suffix = "[symlink]" if is_cross_drive else "[link]"
                    
                    link_name = f"{self.target_path.stem}{link_suffix}{self.target_path.suffix}"
                    link_path = self.source_path.parent / link_name
                    target = self.target_path
                    location_desc = f"in {self.source_path.parent.name}"
                else:  # to_source
                    # Create link IN target folder pointing TO source file
                    # Check if cross-drive
                    source_drive = self.source_path.drive
                    link_drive = self.target_path.drive
                    is_cross_drive = source_drive.upper() != link_drive.upper()
                    link_suffix = "[symlink]" if is_cross_drive else "[link]"
                    
                    link_name = f"{self.source_path.stem}{link_suffix}{self.source_path.suffix}"
                    link_path = self.target_path / link_name
                    target = self.source_path
                    location_desc = f"in {self.target_path.name}"
            else:
                # Directory junctions
                link_suffix = "[junct]"
                if self.direction.get() == "to_target":
                    # Create junction IN source pointing TO target
                    link_name = f"{self.target_path.name}{link_suffix}"
                    link_path = self.source_path / link_name
                    target = self.target_path
                    location_desc = f"in {self.source_path.name}"
                else:  # to_source
                    # Create junction IN target pointing TO source
                    link_name = f"{self.source_path.name}{link_suffix}"
                    link_path = self.target_path / link_name
                    target = self.source_path
                    location_desc = f"in {self.target_path.name}"
            
            # Check if link already exists
            if link_path.exists():
                link_type = "Symbolic link" if (self.is_file and "symlink" in link_name) else ("Hard link" if self.is_file else "Junction")
                response = messagebox.askyesno(
                    f"{link_type} Exists",
                    f"'{link_name}' already exists {location_desc}.\n\n"
                    f"Do you want to delete it and create a new {link_type.lower()}?"
                )
                if not response:
                    return
                
                # Remove existing link
                if link_path.is_dir():
                    os.rmdir(link_path)
                else:
                    link_path.unlink()
            
            # Create hard link for files or junction for directories
            if self.is_file:
                # Check if files are on the same drive
                source_drive = target.drive
                link_drive = link_path.drive
                
                if source_drive.upper() != link_drive.upper():
                    # Use symbolic link for cross-drive file links
                    # Check for admin privileges
                    if not is_admin():
                        response = messagebox.askyesno(
                            "Elevation Required",
                            f"Files are on different drives ({source_drive} and {link_drive}).\n\n"
                            f"Symbolic links across drives require administrator privileges.\n\n"
                            "Would you like to restart junctwin with elevated privileges?"
                        )
                        if response:
                            if run_as_admin(self.source_path):
                                self.root.quit()
                        return
                    
                    cmd = f'mklink "{link_path}" "{target}"'
                    link_type = "Symbolic link"
                else:
                    cmd = f'mklink /H "{link_path}" "{target}"'
                    link_type = "Hard link"
            else:
                cmd = f'mklink /J "{link_path}" "{target}"'
                link_type = "Junction"
                
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo(
                    "Success", 
                    f"{link_type} created successfully!\n\n"
                    f"Link: {link_path}\n"
                    f"Points to: {target}"
                )
                self.root.quit()
            else:
                error_msg = result.stderr or result.stdout
                
                # Check if it's an access denied error and offer elevation
                if "Access is denied" in error_msg or "access denied" in error_msg.lower():
                    if not is_admin():
                        response = messagebox.askyesno(
                            "Elevation Required",
                            f"Failed to create {link_type.lower()} due to insufficient privileges.\n\n"
                            f"Error: {error_msg}\n\n"
                            "Would you like to restart junctwin with elevated privileges?"
                        )
                        if response:
                            if run_as_admin(self.source_path):
                                self.root.quit()
                        return
                
                messagebox.showerror("Error", 
                                   f"Failed to create {link_type.lower()}:\n{error_msg}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create link:\n{str(e)}")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()
        self.root.destroy()


def main():
    try:
        # Check if folder argument provided
        if len(sys.argv) < 2:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", 
                               "No file or folder specified!\n\n"
                               "This script should be called from the 'Send To' menu.")
            return
        
        source_path = sys.argv[1]
        
        # Check if path exists
        if not os.path.exists(source_path):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", 
                               f"Path not found: {source_path}")
            return
        
        # Create and run GUI (accepts both files and directories)
        app = JunctionCreatorGUI(source_path)
        app.run()
        
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", 
                           f"An error occurred:\n\n{str(e)}")


if __name__ == "__main__":
    main()
