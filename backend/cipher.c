#include "../include/cipher.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h> // Ye zaroori hai string length napne ke liye

void run_encryption(const char *filename, const char *key) {
    FILE *source, *dest;
    char temp_filename[] = "temp.bin";
    int ch;
    
    // Password ki lambai check karo
    size_t key_len = strlen(key);
    size_t key_index = 0; // Ye track karega ki password ka kaunsa letter use karna hai

    if (key_len == 0) {
        printf("Error: Password cannot be empty.\n");
        return;
    }

    // Source File kholo
    source = fopen(filename, "rb");
    if (!source) {
        perror("File open error");
        return;
    }

    // Temp File kholo
    dest = fopen(temp_filename, "wb");
    if (!dest) {
        fclose(source);
        perror("Temp file error");
        return;
    }

    // --- MAIN LOGIC (Updated) ---
    while ((ch = fgetc(source)) != EOF) {
        // Current character ko Key ke current letter se XOR karo
        fputc(ch ^ key[key_index], dest);
        
        // Key ke agle letter par jao (Circular logic)
        // Agar password "ABC" hai, toh 0->1->2->0->1->2 chalega
        key_index = (key_index + 1) % key_len;
    }

    // Cleanup
    fclose(source);
    fclose(dest);

    // Replace old file with encrypted file
    remove(filename);
    rename(temp_filename, filename);

    printf("Success: File processed with multi-char password.\n");
}