# Практическое занятие №1. Введение, основы работы в командной строке

> Сделаны задачи 1, 2, 3, 8, 10

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

> Решение:
```console
[root@localhost etc]# grep -oE '^[^:]+' passwd | sort
adm
bin
chrony
daemon
dbus
dnsmasq
ftp
games
geoclue
halt
kojibuilder
lp
mail
nobody
operator
pesign
```

## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```

> Решение
```console
[root@localhost etc]# awk '{if ($1 != "#") print $2, $1}' protocols | sort -r -nk1 | head -5
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```

## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

Перед отправкой решения проверьте его в ShellCheck на предупреждения.

> Решение
```console
[root@localhost ~]# cat test
#!/bin/bash
len=${#1}+2
echo -n '+'
for ((i=0;i<len;i++)) do
echo -n '-'
done
echo '+'
echo -n '| '
echo -n "$1"
echo ' |'
echo -n '+'
for ((i=0;i<len;i++)) do
echo -n '-'
done
echo '+'
[root@localhost ~]# ./test "RTU MIREA"
+-----------+
| RTU MIREA |
+-----------+
```

## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```

В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.

## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

> Решение
```console
localhost:~# cat archive_files
#!/bin/bash
tar cvf output.tar *.$1
localhost:~# ls
archive_files  hello.c        readme.txt
bench.py       hello.js       test.c
localhost:~# bash archive_files c
hello.c
test.c
localhost:~# ls
archive_files  hello.c        output.tar     test.c
bench.py       hello.js       readme.txt
```

## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.

> Решение
```console
[root@localhost ~]# cat empty_files
#!/bin/bash
find $1 -type f -empty
[root@localhost ~]# ./empty_files /etc
/etc/machine-id
/etc/motd
/etc/fstab
/etc/selinux/targeted/contexts/files/file_contexts.subs
/etc/selinux/targeted/contexts/files/file_contexts.local
/etc/exports
/etc/security/opasswd
/etc/subgid
/etc/environment
/etc/subuid
/etc/.pwd.lock
/etc/pki/ca-trust/extracted/pem/objsign-ca-bundle.pem
```

## Полезные ссылки

Линукс в браузере: https://bellard.org/jslinux/

ShellCheck: https://www.shellcheck.net/

Разработка CLI-приложений

Общие сведения

https://ru.wikipedia.org/wiki/Интерфейс_командной_строки
https://nullprogram.com/blog/2020/08/01/
https://habr.com/ru/post/150950/

Стандарты

https://www.gnu.org/prep/standards/standards.html#Command_002dLine-Interfaces
https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html

Реализация разбора опций

Питон

https://docs.python.org/3/library/argparse.html#module-argparse
https://click.palletsprojects.com/en/7.x/
