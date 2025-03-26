#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#define ConstXOR 50
#define MaxSize 100

// Функция для шифрования и дешифрования с использованием XOR
void XOR(char* Text) {
    for (int i = 0; i < MaxSize && Text[i] != '\0'; i++) {
        // printf("%c ", Text[i]);
        Text[i] ^= ConstXOR;
        // printf("%c \n", Text[i]);
    }
}

int main() {
    // Чтение зашифрованного пароля из файла
    FILE* file = fopen("passwordnew.txt", "r");
    if (file == NULL) {
        printf("Ошибка открытия файла!\n");
        return 1;
    }
    char correct_password[MaxSize];
    fgets(correct_password, MaxSize, file);
    // printf("%s", correct_password);
    fclose(file);

    // Удаление символа новой строки
    correct_password[strcspn(correct_password, "\n")] = 0;

    // Ввод пароля от пользователя
    char password[MaxSize];
    printf("Enter the password: ");
    fgets(password, sizeof(password), stdin);

    // Удаление символа новой строки
    password[strcspn(password, "\n")] = 0;

    // Шифруем введенный пароль
    XOR(correct_password);
    // XOR(password);

    // Сравниваем пароли
    if (strcmp(correct_password, password) == 0) {
        printf("Correct password\n");
    } else {
        printf("Incorrect password\n");
    }

    return 0;
}