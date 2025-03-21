#!/bin/bash

# Ассоциативный массив для хранения легитимных пользователей и их хэшей паролей
declare -A users=(
  ["admin"]="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" # Пароль: admin
  ["inno"]="5db1fee4b5703808c48078a76768b155b421b210c0761cd6a5d223f4d99f1eaa"  # Пароль: 1337
)

# Запрашиваем имя пользователя
read -p "Введите имя пользователя: " username

# Проверяем, существует ли пользователь
if [[ -z "${users[$username]}" ]]; then
  echo "Пользователь $username не найден."
  exit 1
fi

# Запрашиваем пароль (без отображения на экране)
read -sp "Введите пароль: " password
echo

# Хэшируем введенный пароль с использованием SHA-256
hashed_password=$(echo -n "$password" | sha256sum | awk '{print $1}')

# Сравниваем хэши
if [[ "${users[$username]}" == "$hashed_password" ]]; then
  echo "Аутентификация успешна. Добро пожаловать, $username!"
else
  echo "Неверные данные."
fi
