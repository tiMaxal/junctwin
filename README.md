# junctwin

## windows right-click junctions instead of shortcuts

A Python application that adds a convenient "Send To" menu entry for creating junction points in Windows 11.

Junctions are created with the **[junct]** suffix for easy identification vs shortcuts.

## Features

- **Right-click context menu integration** via Windows "Send To" menu
- **Two-way junction creation**:
  - Create a junction in the current folder pointing to a target folder
  - Create a junction in the target folder pointing to the current folder
- **User-friendly GUI** with clear options
- **Validation** to prevent errors (same folder, existing junctions, etc.)
- **Easy installation** with automated setup script

## What is a Junction Point?

A junction point is a symbolic link that allows you to create a reference to a directory at another location. Unlike shortcuts, junction points are transparent to applications - they appear as actual directories.

## Installation

1. **Install Python** (if not already installed) - Download from [python.org](https://www.python.org/)

2. **Run the installer:**
   ```powershell
   python install_sendto.py
   ```

3. **Done!** The **junctwin** option is now available in your Send To menu.

## Usage

### Creating a Junction Point

1. **Right-click** any folder in Windows Explorer
2. Select **Send To → junctwin**
3. Choose the junction direction:
   - **IN current folder → TO target**: Creates a junction in your selected folder pointing to the target
   - **IN target → TO current**: Creates a junction in the target folder pointing to your selected folder
4. Click **Select Target Folder** and choose the destination
5. Confirm the creation

Junctions are automatically named with the **[junct]** suffix (e.g., `FolderName[junct]`) for easy identification.

### Example Scenarios

**Scenario 1: Link a project folder to a backup location**
- Right-click your project folder → Send To → junctwin
- Select "Create junction IN target folder → TO current folder"
- Choose your backup directory
- Result: A junction named `YourProject[junct]` appears in the backup folder

**Scenario 2: Access a deep folder structure easily**
- Right-click a deeply nested folder → Send To → junctwin
- Select "Create junction IN current folder → TO target"
- Choose a convenient location (e.g., Desktop)
- Result: Quick access junction named `DeepFolder[junct]` created at the convenient location

## Uninstallation

To remove from the Send To menu:
```powershell
python install_sendto.py uninstall
```

## Requirements

- Windows 10/11
- Python 3.6 or higher
- Administrator privileges (for creating junction points)

## Technical Details

- Uses Windows `mklink /J` command to create junction points
- Built with Python's `tkinter` for the GUI
- No external dependencies required (uses standard library only)

## File Structure

```
ai_winjunct/
├── create_junction.py      # Main application script
├── install_sendto.py        # Installation/uninstallation utility
└── README.md               # This file
```

## Troubleshooting

**"Access Denied" error when creating junction:**
- Junction points require administrator privileges in some directories
- Try running Windows Explorer as administrator, or use different target folders

**Script doesn't appear in Send To menu:**
- Verify installation completed successfully
- Check the SendTo folder manually: `%APPDATA%\Microsoft\Windows\SendTo`
- Restart Windows Explorer (Task Manager → Windows Explorer → Restart)

**GUI doesn't appear:**
- Make sure Python is installed and tkinter is available
- Try running `python create_junction.py "C:\Some\Folder"` directly to test

## License

This project is free to use and modify.

## Contributing

Feel free to submit issues, improvements, or suggestions!
