# junctwin

created by ai 'voding' [vibe-coding] copilot20251229timaxal

## windows right-click junctions and hard links

A Python application that adds a convenient "Send To" menu entry for creating junction points (directories) and hard links (files) in Windows 11.

Junctions are created with the **[junct]** suffix for easy identification vs shortcuts.

## Features

- **Right-click context menu integration** via Windows "Send To" menu
- **Works with both files and directories**:
  - **Files**: Creates hard links (same drive) or symbolic links (cross-drive)
  - **Directories**: Creates junction points
- **Two-way link creation**:
  - Create a link in the current location pointing to a target
  - Create a link in the target location pointing to current
- **User-friendly GUI** with clear options
- **Automatic privilege elevation** when administrator rights are needed
- **Cross-drive support** with automatic symbolic link creation for files
- **Validation** to prevent errors (same location, existing links, etc.)
- **Easy installation** with automated setup script

## What are Junction Points and Hard Links?

**Junction points** are symbolic links for directories that allow you to create a reference to a folder at another location. Unlike shortcuts, junctions are transparent to applications - they appear as actual directories.

**Hard links** are multiple directory entries for the same file. Changes to the file through any hard link are reflected in all links because they all reference the same physical file data. Hard links only work within the same drive.

**Symbolic links** (symlinks) are similar to hard links but work across different drives and require administrator privileges.

## Installation

1. **Install Python** (if not already installed) - Download from [python.org](https://www.python.org/)

2. **Run the installer:**

   ```powershell
   python install_sendto.py
   ```

3. **Done!** The **junctwin** option is now available in your Send To menu.

## Usage

### Creating Links

1. **Right-click** any file or folder in Windows Explorer
2. Select **Send To → junctwin**
3. Choose the link direction:
   - **IN current location → TO target**: Creates a link next to your selected item pointing to the target
   - **IN target location → TO current**: Creates a link at the target location pointing to your selected item
4. Click **Select Target File** or **Select Target Folder** and choose the destination
5. Confirm the creation

Links are automatically named with suffixes for easy identification:
- **[junct]** for directory junctions (e.g., `FolderName[junct]`)
- **[link]** for same-drive file hard links (e.g., `filename[link].txt`)
- **[symlink]** for cross-drive file symbolic links (e.g., `filename[symlink].txt`)

### Example Scenarios

**Scenario 1: Cloud storage folder access without duplication**
- Right-click your cloud-synced folder (e.g., Dropbox, OneDrive)
- Select **Send To → junctwin**
- Choose "Create junction IN target folder → TO current folder"
- Select a convenient location (e.g., Desktop or project folder)
- Result: A junction named `CloudFolder[junct]` provides access without duplicating files

**Scenario 2: Link a configuration file across projects**
- Right-click a config file you want to share
- Select **Send To → junctwin**  
- Choose "Create hard link IN target file's folder → TO current file"
- Select the target project folder
- Result: Both projects use the same physical file - edits in one appear in both

**Scenario 3: Access deeply nested folders easily**
- Right-click a deeply nested folder → **Send To → junctwin**
- Choose "Create junction IN target folder → TO current folder"
- Select a convenient location (e.g., Desktop)
- Result: Quick access junction named `DeepFolder[junct]` at convenient location

## Uninstallation

To remove from the Send To menu:

```powershell
python install_sendto.py uninstall
```

## Requirements

- Windows 10/11
- Python 3.6 or higher
- Administrator privileges (automatic elevation when needed for symbolic links or protected directories)

## Technical Details

- Uses Windows `mklink` command:
  - `/J` for directory junctions
  - `/H` for file hard links (same drive)
  - Symbolic links for cross-drive file links
- Automatic privilege elevation when administrator rights required
- Built with Python's `tkinter` for the GUI
- No external dependencies required (uses standard library only)

## File Structure

```
ai_junctwin/
├── junctwin.py              # Main application script
├── install_sendto.py        # Installation/uninstallation utility
└── README.md                # This file
```

## Troubleshooting

**"Access Denied" error when creating junction or link:**
- The app will automatically offer to restart with administrator privileges
- Alternatively, try using different target locations that don't require admin rights
- Some system directories are protected and may still fail even with admin rights

**Cross-drive file links require admin privileges:**
- The app automatically detects cross-drive scenarios
- You'll be prompted to restart with elevated privileges
- Click "Yes" when the UAC prompt appears

**Script doesn't appear in Send To menu:**
- Verify installation completed successfully
- Check the SendTo folder manually: `%APPDATA%\Microsoft\Windows\SendTo`
- Restart Windows Explorer (Task Manager → Windows Explorer → Restart)

**GUI doesn't appear:**
- Make sure Python is installed and tkinter is available
- Try running `python junctwin.py "C:\Some\Folder"` directly to test

## Important: Cloud Storage Considerations

**⚠️ Understanding Junctions with Cloud Storage**

When using junctions with cloud-synced folders (Dropbox, OneDrive, Google Drive, etc.), it's critical to understand how file operations behave:

**How Junctions Work:**
- A junction is a pointer to another location - files physically exist in only ONE place
- If you create a junction pointing TO your cloud folder, the actual files are IN the cloud folder
- Accessing files through the junction is the same as accessing them directly

**Editing Files:**
- ✅ **Local edits** through the junction → Immediately synced to cloud (files are actually in the cloud folder)
- ✅ **Cloud edits** (from another device or web) → Reflected locally through the junction

**Deleting Files - CRITICAL:**
- ⚠️ **Deleting through the junction** = Deleting the actual files in the cloud folder
  - Files are removed from cloud sync
  - Files are **permanently deleted** (or moved to Recycle Bin if available)
  - All other devices synced to that cloud folder will lose those files
  
- ⚠️ **Deleting from cloud** (another device or web interface):
  - Files are removed from the cloud
  - The junction still exists but points to deleted/non-existent files
  - Local junction becomes "broken" - files appear to vanish

- ⚠️ **Deleting the junction itself** (right-click junction → Delete):
  - Removes ONLY the junction pointer
  - Original cloud files remain intact and safe
  - This is the safe way to remove the junction

**Best Practices:**
1. **Clearly label junctions** - The `[junct]` suffix helps identify them
2. **Think before deleting** - Remember you're working with the actual files, not copies
3. **Test first** - Try with non-critical files to understand the behavior
4. **Document your junctions** - Keep track of what points where
5. **Consider read-only** - If you just need access, consider making files read-only

**Remember:** Junctions are not backups or copies - they're alternate pathways to the same files. Any destructive operation affects the actual files regardless of which path you use.

## License

This project is free to use and modify.

## Contributing

Feel free to submit issues, improvements, or suggestions!
