# vuln_manager
Файловый менеджер, дискреционная модель разграничения доступа.

# Функционал

- [sign/s] - to sign up
- [login/l] - to log in
- [read/r] FILE_NAME - to read file FILE_NAME
- [write/w] FILE_NAME - to write in file FILE_NAME
- [append/a] FILE_NAME - to append file FILE_NAME
- [create/c] FILE_NAME - to create file FILE_NAME
- [delete/d] FILE_NAME - to delete file FILE_NAME
- [show rights] FILE_NAME - to users' rights for your file FILE_NAME
- [change user/cu] - go back to auth
- [exit/e] - to quit from file manager
- [reset password/rp] - reset your password (for sure)
- [take/t] RIGHT FILE_NAME (USER_NAME or all) - to take RIGHT for FILE_NAME from USER_NAME (or all users)
- [give/g] RIGHT FILE_NAME (USER_NAME or all) - to give RIGHT for FILE_NAME to USER_NAME (or all users)
- [show my files/smf] - show all the files you own (ONLY FO USERS!)
- [show rtable/srt] - show rights table (ONLY FOR ADMINISTRATOR!)
- [show utable/sut] - show users table (ONLY FOR ADMINISTRATOR!)
- [show ftable/sft] - show filenames table (ONLY FOR ADMINISTRATOR!)
- [exit/e] - to quit from file manager

# Уязвимости
1) админские логин и пароль захардкожены
2) path traversal
3) хешировать пароли md5
4) нарушение логики работы команды show utable/sut
5) повторная регистрация пользователя
  - TODO

# Кейсы пользователя
видны из функционала

# Кейсы чекера
Чекер кладет флаг: 
1) sign; checker_login; checker_pass (+confirm)
2) login; checker_login; checker_pass
3) create FLAG_FILE_SALT; [A-Z0-9]{31}=
4) exit

Чекер проверяет флаг:
1) login; checker_login; checker_pass
2) read FLAG_FILE_SALT
3) exit

# Эксплуатация уязвимостей
1) админские логин и пароль захардкожены:
  - логинимся в систему с помощью admin admin
2) path traversal:
  - создаем файл с названием "../files/FLAG_FILE_SALT", текст для файла оставляем пустым, чтобы не перезатирать файл
  - имеем право own на файл "../files/FLAG_FILE_SALT", не имея прав на файл "FLAG_FILE_SALT" (один и тот же файл)
3) хешировать пароли md5:
  - повторяем действия path traversal для файла "../src/Users.txt"
  - получаем доступ к логинам и соответстсвующим хэшам паролей 
4) нарушение логики работы команды show utable/sut:
  - обращаемся к команде, не являясь админом (нет проверки на администратора)
  - получаем список всех пользователей
5) повторная регистрация пользователя:
  - TODO
