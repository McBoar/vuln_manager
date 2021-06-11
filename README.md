# vuln_manager
Файловый менеджер, дискреционная модель разграничения доступа.

# Функционал
- [sign/s] - to sign up
- [login/l] - to log in
- [read/r] FILE_NAME - to read file FILE_NAME
- [write/w] FILE_NAME - to write in file FILE_NAME
- [append/a] FILE_NAME - to append file FILE_NAME
- [create/c] FILE_NAME - to create file FILE_NAME
- [show rights] FILE_NAME - to users' rights for your file FILE_NAME
- [change user/cu] - go back to auth
- [exit/e] - to quit from file manager
- [reset password/rp] - reset your password (for sure)
- [take/t] RIGHT FILE_NAME (USER_NAME or all) - to take RIGHT for FILE_NAME from USER_NAME (or all users)\n\
- [give/g] RIGHT FILE_NAME (USER_NAME or all) - to give RIGHT for FILE_NAME to USER_NAME (or all users)\n\
- [show my files/smf] - show all the files you own
- [show rtable/srt] - show rights table
- [show utable/sut] - show users table
- [show ftable/sft] - show filenames table

# Уязвимости
1) path traversal
2) распространение права own любым пользователем на любой файл
3) хешировать пароли md5

# Кейсы пользователя
видны из функционала

# Кейсы чекера
CHECK: 
1) регистрация нового пользователя
2) создание файла со строкой
3) проверка существования файла
4) проверка корректности содержимого файла

PUT:
1) регистрация нового пользователя
2) создание файла со флагом

GET:
1) логин под созданного в PUT пользователя
2) чтение файла
3) проверка корректности флага

# Эксплуатация уязвимостей
1) path traversal:
  - создаем файл с названием "../files/FLAG_FILE_SALT", текст для файла оставляем пустым, чтобы не перезатирать файл
  - имеем право own на файл "../files/FLAG_FILE_SALT", не имея прав на файл "FLAG_FILE_SALT" (один и тот же файл)
2) распространение права own:
  - с помощью команды sft получаем список названий файлов
  - распространяем на них право own для пользователя, под которым залогинены
  - распространяем на них право read для пользователя, под которым залогинены
  - командой read читаем флаг из файлов
4) хешировать пароли md5:
  - повторяем действия path traversal для файла "../src/Users.txt"
  - получаем доступ к логинам и соответстсвующим хэшам паролей

#Contributors
Архитектура сервиса, его реализация, технические решения, искусственно добавленные уязвимости, чекер и эксплойты написаны полностью совместно без разделения областей ответсвенности @Stomnok и @McBoar.
