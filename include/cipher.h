#ifndef CIPHER_H
#define CIPHER_H

// Change: 'char key' ab 'const char *key' ban gaya (Pointer to String)
void run_encryption(const char *filename, const char *key);

#endif