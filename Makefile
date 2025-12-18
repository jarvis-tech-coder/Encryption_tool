CC = gcc
CFLAGS = -Iinclude -Wall
# Windows specific flags for GUI
GUI_FLAGS = -mwindows -lcomdlg32

# Files
CLI_SRC = src/main.c src/cipher.c
GUI_SRC = src/gui.c

# Targets (Output names)
CLI_TARGET = bin/encryptor.exe
GUI_TARGET = bin/gui_tool.exe

# "make" likhne par ye dono banayega
all: $(CLI_TARGET) $(GUI_TARGET)

# CLI Tool Banana
$(CLI_TARGET): $(CLI_SRC)
	if not exist bin mkdir bin
	$(CC) $(CFLAGS) -o $(CLI_TARGET) $(CLI_SRC)

# GUI Tool Banana
$(GUI_TARGET): $(GUI_SRC)
	if not exist bin mkdir bin
	$(CC) -o $(GUI_TARGET) $(GUI_SRC) $(GUI_FLAGS)

# Clean (Sab delete karne ke liye)
clean:
	if exist bin\encryptor.exe del bin\encryptor.exe
	if exist bin\gui_tool.exe del bin\gui_tool.exe