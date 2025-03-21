#!/bin/bash

# Проверяем, передан ли файл в качестве аргумента
if [ $# -ne 1 ]; then
  echo "Использование: $0 <имя_файла>"
  exit 1
fi

filename=$1

# Проверяем, существует ли файл
if [ ! -f "$filename" ]; then
  echo "Файл $filename не найден."
  exit 1
fi

declare -A word_count

# Читаем файл построчно
while IFS= read line; do
  # Разбиваем строку на слова
  for word in $line; do
    # Убираем знаки препинания и приводим к нижнему регистру
    word=$(echo "$word" | tr -d '[:punct:]' | tr '[:upper:]' '[:lower:]')
    # Увеличиваем счетчик для данного слова
    ((word_count[$word]++))
  done
done <"$filename"

# Выводим результат
for word in "${!word_count[@]}"; do
  echo "$word: ${word_count[$word]}"
done
