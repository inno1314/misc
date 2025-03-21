#!/bin/bash

# Проверяем, переданы ли два аргумента (директории)
if [ $# -ne 2 ]; then
  echo "Использование: $0 <директория1> <директория2>"
  exit 1
fi

dir1=$1
dir2=$2

# Проверяем, существуют ли директории
if [ ! -d "$dir1" ]; then
  echo "Директория $dir1 не существует."
  exit 1
fi

if [ ! -d "$dir2" ]; then
  echo "Директория $dir2 не существует."
  exit 1
fi

# Получаем список файлов в каждой директории
files_dir1=$(ls -1 "$dir1")
files_dir2=$(ls -1 "$dir2")

# Используем `comm` для поиска общих файлов
common_files=$(comm -12 <(echo "$files_dir1" | sort) <(echo "$files_dir2" | sort))

# Выводим результат
if [ -z "$common_files" ]; then
  echo "Одноименных файлов не найдено."
else
  echo "Одноименные файлы:"
  echo "$common_files"
fi
