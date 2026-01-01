# ai-hist junctwin

## 20251229

### initial prompt

- provide win11 r-click 'send to' menu entry acting in current folder, to create a junction to the chosen target folder

- app [obv] name play on 'junction'+'windows'

### development and naming

- **initial implementation**: created `create_junction.py` with GUI for two-way junction creation
- **installer script**: created `install_sendto.py` to add shortcut to Windows Send To menu
- **README**: comprehensive documentation with usage examples and troubleshooting
- **naming evolution**: 
  - Initial: "Junction Point Creator" (too generic)
  - Second: "winjunct" (windows + junction)
  - Final: "junctwin" (junction + windows, better play on words)
- **[junct] suffix**: implemented to distinguish junctions from shortcuts
- **GUI polish**: added Windows 11 style with Segoe UI font and blue header

## 20260101

### bug fixes and feature expansion

- **window flash issue**: fixed missing parenthesis in `geometry()` call, then fixed tkinter StringVar initialization order
- **file support request**: added hard link support for files alongside junction support for directories
- **cross-drive limitation**: implemented automatic symbolic link creation for files on different drives with privilege elevation
- **target selection UX**: updated file link creation to select target folder instead of requiring existing target file
- **auto-elevation**: added privilege elevation detection and restart capability for all "Access Denied" errors
- **link suffix labeling**: implemented intelligent suffix system - `[junct]`, `[link]`, `[symlink]`
- **rename**: changed `create_junction.py` → `junctwin.py` for cleaner naming
- **README updates**: comprehensive documentation of file support, link types, cloud storage safety warnings, and privilege elevation
- **git commit**: prepared summary of all changes for repository update