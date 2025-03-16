#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <locale.h>
#include <stdlib.h>

int password_check(const char* correct_password, const char* password) {
    return strcmp(correct_password, password) == 0;
}

int main() {
    setlocale(LC_ALL, "Russian");

    FILE* file = fopen("C:\\Users\\mefod\\Desktop\\OIB\\Lab 6\\password.txt", "r");

    char correct_password[100];
    fgets(correct_password, sizeof(correct_password), file);
    fclose(file);

    correct_password[strcspn(correct_password, "\n")] = 0; // Удаление \n
    char password[100];
    printf("Enter the password: ");
    fgets(password, sizeof(password), stdin);

    password[strcspn(password, "\n")] = 0; // Удаление \n
    if (!password_check(correct_password, password)) {
        printf("Incorrect password\n");
    }
    else {
        printf("Correct password\n");
    }

    system("pause");

    return 0;
}
