"""
Installer script to add Junction Creator to Windows 'Send To' menu
"""

import os
import sys
import subprocess
from pathlib import Path


def create_sendto_entry():
    """Create a shortcut in the SendTo folder"""
    
    # Get the SendTo folder path
    sendto_folder = Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SendTo"))
    
    if not sendto_folder.exists():
        print(f"Error: SendTo folder not found at {sendto_folder}")
        return False
    
    # Get the current script directory
    script_dir = Path(__file__).parent.resolve()
    python_script = script_dir / "junctwin.py"
    
    if not python_script.exists():
        print(f"Error: junctwin.py not found at {python_script}")
        return False
    
    # Find Python executable
    python_exe = sys.executable
    
    # Create the shortcut name
    shortcut_name = "junctwin.lnk"
    shortcut_path = sendto_folder / shortcut_name
    
    # Create VBS script to create shortcut (PowerShell alternative)
    vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{python_exe}"
oLink.Arguments = """{python_script}"""
oLink.WorkingDirectory = "{script_dir}"
oLink.Description = "junctwin - Create Junction Point"
oLink.Save
'''
    
    # Write VBS script to temp file
    temp_vbs = script_dir / "create_shortcut.vbs"
    try:
        with open(temp_vbs, 'w') as f:
            f.write(vbs_script)
        
        # Execute VBS script
        result = subprocess.run(
            ['cscript.exe', '//Nologo', str(temp_vbs)],
            capture_output=True,
            text=True
        )
        
        # Clean up temp VBS file
        temp_vbs.unlink()
        
        if result.returncode == 0 and shortcut_path.exists():
            print(f"✓ Successfully installed to Send To menu!")
            print(f"  Shortcut: {shortcut_path}")
            print(f"\nYou can now right-click any folder → Send To → junctwin")
            return True
        else:
            print(f"Error creating shortcut: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        if temp_vbs.exists():
            temp_vbs.unlink()
        return False


def remove_sendto_entry():
    """Remove the shortcut from SendTo folder"""
    sendto_folder = Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SendTo"))
    shortcut_path = sendto_folder / "junctwin.lnk"
    
    if shortcut_path.exists():
        try:
            shortcut_path.unlink()
            print(f"✓ Successfully removed from Send To menu!")
            return True
        except Exception as e:
            print(f"Error removing shortcut: {e}")
            return False
    else:
        print("Shortcut not found in Send To menu.")
        return False


def main():
    print("=" * 60)
    print("junctwin - Send To Menu Installer")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1].lower() == "uninstall":
        print("Uninstalling...")
        remove_sendto_entry()
    else:
        print("Installing...")
        create_sendto_entry()
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
