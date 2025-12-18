# CLI File Encryption Tool

A lightweight, command-line utility written in C for encrypting and decrypting files using XOR logic. This tool demonstrates low-level file I/O operations and modular C programming.

## Features
- **Simple Security:** Uses XOR encryption logic.
- **Universal:** Works on text files, images, PDFs, and binaries.
- **Memory Efficient:** Processes files byte-by-byte (suitable for large files).

## How to Build
1. Clone the repository.
2. Run `make` in the terminal.
   ```bash
   make

## Graphical User Interface (GUI)
This project includes a native Windows GUI built using the **Win32 API**.
- **User-Friendly:** Visual file picker dialog.
- **Lightweight:** No external libraries required (pure C).

**To Run the GUI:**
Double-click `bin/gui_tool.exe` or run via terminal:
```bash
./bin/gui_tool.exe