# a w r o

import time
import hashlib
from getpass import getpass

HELP_SESSION = "\n\
[read/r] FILE_NAME - to read file FILE_NAME\n\
[write/w] FILE_NAME - to write in file FILE_NAME\n\
[append/a] FILE_NAME - to append file FILE_NAME\n\
[create/c] FILE_NAME - to create file FILE_NAME\n\
[delete/d] FILE_NAME - to delete file FILE_NAME\n\
[show rights] FILE_NAME - to users' rights for your file FILE_NAME\n\
[change user/cu] - go back to auth\n\
[exit/e] - to quit from file manager\n\
[reset password/rp] - reset your password (for sure)\n\
[take/t] RIGHT FILE_NAME (USER_NAME or all) - \n\
to take RIGHT for FILE_NAME from USER_NAME (or all users)\n\
[give/g] RIGHT FILE_NAME (USER_NAME or all) - \n\
to give RIGHT for FILE_NAME to USER_NAME (or all users)\n\
[show my files/smf] - show all the files you own (ONLY FO USERS!)\n\
[show rtable/srt] - show rights table (ONLY FOR ADMINISTRATOR!)\n\
[show utable/sut] - show users table (ONLY FOR ADMINISTRATOR!)\n\
[show ftable/sft] - show filenames table (ONLY FOR ADMINISTRATOR!)"

HELP_LOGIN = "\n\
[sign/s] - to sign up\n\
[login/l] - to log in\n\
[exit/e] - to quit from file manager"

SRC_PATH = './src/'
FILES_PATH = './files/'

USERS_FILENAME = SRC_PATH + 'Users.txt'
FILES_FILENAME = SRC_PATH + 'Filenames.txt'
RIGHTS_FILENAME = SRC_PATH + 'Rights.txt'

def num2rights(number):
    string = ''
    if(number & 1):
        string += 'own,'
    if(number & 2):
        string += 'read,'
    if(number & 4):
        string += 'write,'
    if(number & 8):
        string += 'append,'
    if(string[-1] == ','):
        return string[:-1]
    return 'no rights'

def users_file_empty():
    file = open(USERS_FILENAME, 'r')
    if(file.read() != ''):
        file.close()
        return 0
    file.close()
    return 1

def filenames_file_empty():
    file = open(FILES_FILENAME, 'r')
    if(file.read() != ''):
        file.close()
        return 0
    file.close()
    return 1

def rights_file_empty():
    file = open(RIGHTS_FILENAME, 'r')
    if(file.read() != ''):
        file.close()
        return 0
    file.close()
    return 1

def get_users():
    if(users_file_empty()):
        return {'logins'    : ['admin'],
                 'pswds'     : ['21232f297a57a5a743894a0e4a801fc3']}
    file = open(USERS_FILENAME, 'r')
    users_tmp1 = file.read().split('\n')
    users_tmp2 = []
    for strings in users_tmp1:
        users_tmp2.append(strings.split(' ')[:-1])
    users = {'logins'   : users_tmp2[0],
             'pswds'    : users_tmp2[1]}
    file.close()
    return users

def get_filenames():
    if(filenames_file_empty()):
        return []
    file = open(FILES_FILENAME, 'r')
    filenames = file.read().split(' ')[:-1]
    file.close()
    return filenames

def get_rights():
    if(rights_file_empty()):
        return [[]]
    file = open(RIGHTS_FILENAME, 'r')
    rights_tmp = file.read().split('\n')
    rights = []
    for strings in rights_tmp:
        rights.append(strings.split(' ')[:-1])
    file.close()
    return rights

def update_users(users):
    file = open(USERS_FILENAME, 'w')
    string = ''
    for username in users['logins']:
        string += username + ' '
    string += '\n'
    for pswd in users['pswds']:
        string += pswd + ' '
    file.write(string)
    file.close()

def update_filenames(files):
    file = open(FILES_FILENAME, 'w')
    string = ''
    for filename in files:
        string += filename + ' '
    file.write(string)
    file.close()

def update_rights(rights):
    file = open(RIGHTS_FILENAME, 'w')
    string = ''
    for i in range(len(rights)):
        for j in range(len(rights[i])):
            string += str(rights[i][j]) + ' '
        string += '\n'
    if(string[-1] == '\n'):
        string = string[:-1]
    file.write(string)
    file.close()

def create_user(users, login, pswd):
    is_empty_cell = bool(users['logins'].count(''))
    if(is_empty_cell):
        new_ix = users['logins'].index('')
        users['logins'][new_ix] = login
        users['pswds'][new_ix] = pswd
    else:
        users['logins'].append(login)
        users['pswds'].append(pswd)
        rights.append(['0'] * len(filenames))
    update_rights(rights)
    update_users(users)
    return users

def change_pass(users, login, new_pswd):
    ix = users['logins'].index(login)
    users['pswds'][ix] = new_pswd
    return users

def files_session(request, user_ix, users, filenames, rights):
    if(len(request.split(' ')) != 2):
        print('Sorry, wrong request (wrong number of operands).\n')
        return users, filenames, rights

    type_of_rqst, file_name = request.split(' ')
    
    if(type_of_rqst == 'create' or type_of_rqst == 'c'):
        print('Enter a text for the file:\n> ', end = '')
        text = input()
        if len(text):
            file = open(FILES_PATH + file_name, 'w+')
            file.write(text)
        else:
            file = open(FILES_PATH + file_name, 'r')
        file.close()

        is_empty_cell = bool(filenames.count(''))
        if(is_empty_cell):
            new_ix = filenames.index('')
            filenames[new_ix] = file_name
            for i in range(len(rights)):
                if(i != user_ix and i != 0):
                    rights[i][new_ix] = '0'
                else:
                    rights[i][new_ix] = '15'
        else:
            filenames.append(file_name)
            for i in range(len(rights)):
                if(i != user_ix and i != 0):
                    rights[i].append('0')
                else:
                    rights[i].append('15')
        
        update_filenames(filenames)
        update_rights(rights)
        print('\nDONE!')
        return users, filenames, rights
                    
    if(filenames.count(file_name)):
        file_ix = filenames.index(file_name)
    else:
        print('Sorry, there is no files with this name.')
        return users, filenames, rights
    
    if(type_of_rqst == 'read' or type_of_rqst == 'r'):
        if not(int(rights[user_ix][file_ix]) & 2):
            print('Sorry, you don\'t have enough rights.')
        else:
            file = open(FILES_PATH + file_name, 'r')
            print('\n{}:\n{}\n{}\n{}'.format(file_name, '_' * 20, file.read(), '_' * 20))
            file.close()
        return users, filenames, rights
    
    elif(type_of_rqst == 'write' or type_of_rqst == 'w'):
        if not(int(rights[user_ix][file_ix]) & 4):
            print('Sorry, you don\'t have enough rights.')
        else:
            file = open(FILES_PATH + file_name, 'w')
            print('Enter new text for the file.\n\n' + file_name + ':\n> ', end = '')
            text = input()
            file.write(text)
            file.close()
    
    elif(type_of_rqst == 'append' or type_of_rqst == 'a'):
        if not(int(rights[user_ix][file_ix]) & 8):
            print('Sorry, you don\'t have enough rights.')
        else:
            file = open(FILES_PATH + file_name, 'a')
            print('\nEnter additional text for the file.\n\n' + file_name + ':\n> ', end = '')
            text = input()
            file.write(text)
            file.close()

    elif(type_of_rqst == 'delete' or type_of_rqst == 'd'):
        filenames[file_ix] = ''
        for i in range(len(rights)):
            rights[i][file_ix] = '0'
        update_filenames(filenames)
        update_rights(rights)

    else:
        print('Sorry, wrong type of request.')
        return users, filenames, rights

    print('\nDONE!')
    return users, filenames, rights

def rights_session(request, user_ix, users, filenames, rights):
    if (len(request.split(' ')) != 4):
        print('Sorry, wrong request (wrong nuber of operands).')
        return users, filenames, rights

    type_of_rqst, right, file_name, subject = request.split(' ')
    
    if(type_of_rqst == 'take' or type_of_rqst == 't'):
        take_flag = 1
    elif(type_of_rqst == 'give' or type_of_rqst == 'g'):
        take_flag = 0
    else:
        print('Sorry, wrong 1st operand!')
        return users, filenames, rights

    if(filenames.count(file_name)):
        file_ix = filenames.index(file_name)
    else:
        print('Sorry, there is no files with this name.')
        return users, filenames, rights

    if not(int(rights[user_ix][file_ix]) & 1):
        print('Sorry, you don\'t own this file.')
        return users, filenames, rights

    if(right == 'read' or right == 'r'):
        if(subject == 'all'):
            if(take_flag):
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (2 ^ 15)
            else:
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 2
        else:
            if(users['logins'].count(subject)):
                subject_ix = users['logins'].index(subject)
            else:
                print('Sorry, there is no users with this name.')
                return users, filenames, rights
            if(subject_ix == 0):
                print('Sorry, you can\'t change administrator\'s rights.')
                return users, filenames, rights
            if(take_flag):
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (2 ^ 15)
            else:
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 2

    elif(right == 'write' or right == 'w'):
        if(subject == 'all'):
            if(take_flag):
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (4 ^ 15)
            else:
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 4
        else:
            if(users['logins'].count(subject)):
                subject_ix = users['logins'].index(subject)
            else:
                print('Sorry, there is no users with this name.')
                return users, filenames, rights
            if(subject_ix == 0):
                print('Sorry, you can\'t change administrator\'s rights.')
                return users, filenames, rights
            if(take_flag):
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (4 ^ 15)
            else:
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 4
        
    elif(right == 'append' or right == 'a'):
        if(subject == 'all'):
            if(take_flag):
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (8 ^ 15)
            else:
                for subject_ix in range(1, len(rights)):
                    rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 8
        else:
            if(users['logins'].count(subject)):
                subject_ix = users['logins'].index(subject)
            else:
                print('Sorry, there is no users with this name.')
                return users, filenames, rights
            if(subject_ix == 0):
                print('Sorry, you can\'t change administrator\'s rights.')
                return users, filenames, rights
            if(take_flag):
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) & (8 ^ 15)
            else:
                rights[subject_ix][file_ix] = int(rights[subject_ix][file_ix]) | 8
    
    elif(right == 'own' or right == 'o'):
        print('You can\'t give or take own right.')
        return users, filenames, rights

    else:
        print('Sorry, there is no such rights.')
        return users, filenames, rights
    
    update_rights(rights)
    print('\nDONE!')
    
    return users, filenames, rights

def session(user_ix, users, filenames, rights):
    print('\nYou\'ve successfully loged in!')

    while(True):
            
        print('\nEnter your request ([commands/c] - to show available commands):\n> ', end='')
        request = input()

        if(request == 'reset password' or request == 'rp'):
            new_pswd = getpass('password: ')
            new_pswd_hash = hashlib.md5()
            new_pswd_hash.update(bytes(pswd, 'utf-8'))
            users = change_pass(users, users['logins'][user_ix], new_pswd_hash.hexdigest())
            continue

        if(request == 'exit' or request == 'e'):
            print('')
            exit(0)

        if(request == 'commands' or request == 'c'):
            print(HELP_SESSION)
            continue

        if(request == 'change user' or request == 'cu'):
            break
        
        if(request == 'delete user' or request == 'du'):
            if(user_ix == 0):
                print('Sorry, administrator can\'t delete himself.\n')
                continue
            pswd = getpass('password: ')
            pswd_hash = hashlib.md5()
            pswd_hash.update(bytes(pswd, 'utf-8'))
            if(pswd_hash.hexdigest() != users['pswds'][user_ix]):
                print('Wrong password!')
                continue
            users['logins'][user_ix] = ''
            users['pswds'][user_ix] = ''
            for j in range(len(filenames)):
                rights[user_ix][j] = '0'
            update_users(users)
            update_rights(rights)
            break
        
        if(request == 'show rtable' or request == 'srt'):
            if(user_ix == 0):
                print(rights)
            else:
                print('This request is available only for administrator!\n')
            continue
        
        if(request == 'show utable' or request == 'sut'):
            print(users['logins'])
            continue
        
        if(request == 'show ftable' or request == 'sft'):
            if(user_ix == 0):
                print(filenames)
            else:
                print('This request is available only for administrator!\n')
            continue

        if(request == 'show my files' or request == 'smf'):
            print('')
            if(user_ix == 0):
                print('This users\' request.\n')
            else:
                counter = 0
                for file_ix in range(len(rights[user_ix])):
                    if(int(rights[user_ix][file_ix]) & 1):
                        counter += 1
                        print(filenames[file_ix])
                if(counter):
                    print('\nTOTAL: {} files.'.format(counter))
                else:
                    print('You don\'t own any files yet.')
            continue

        is_full_sr = (len(request.split(' ')) == 3) and (request.split(' ')[0] + ' ' + request.split(' ')[1] == 'show rights')
        is_short_sr = len(request.split(' ')) == 2 and request.split(' ')[0] == 'sr'

        if(is_full_sr or is_short_sr):  
            print('')
            if(user_ix == 0):
                print('This users\' request.')
            if(len(request.split(' ')) != 3 and len(request.split(' ')) != 2):
                print('Sorry, wrong request (wrong nuber of operands).')
                continue
            if(is_full_sr):
                file_name = request.split(' ')[2]
            else:
                file_name = request.split(' ')[1]
            if(filenames.count(file_name)):
                file_ix = filenames.index(file_name)
            else:
                print('Sorry, there is no file with this name.')
                continue
            if not(int(rights[user_ix][file_ix]) & 1):
                print('Sorry, you don\'t own this file.')
                continue
            for subject_ix in range(len(rights)):
                if(rights[subject_ix][file_ix] != '0'):
                    print(users['logins'][subject_ix] + ': ' + num2rights(int(rights[subject_ix][file_ix])))
            continue

        is_create = request.split(' ')[0] == 'create' or request.split(' ')[0] == 'c'
        is_read = request.split(' ')[0] == 'read' or request.split(' ')[0] == 'r'
        is_write =request.split(' ')[0] == 'write' or request.split(' ')[0] == 'w'
        is_append = request.split(' ')[0] == 'append' or request.split(' ')[0] == 'a'
        is_delete = request.split(' ')[0] == 'delete' or request.split(' ')[0] == 'd'
        
        if(is_create or is_read or is_write or is_append or is_delete):
            users, filenames, rights = files_session(request, user_ix, users, filenames, rights)
            continue
        
        is_take = request.split(' ')[0] == 'take' or request.split(' ')[0] == 't'
        is_give = request.split(' ')[0] == 'give' or request.split(' ')[0] == 'g'
        
        if(is_take or is_give):
            users, filenames, rights = rights_session(request, user_ix, users, filenames, rights)
        else:
            print('Sorry, wrong type of request.')
        continue
        
    return users, filenames, rights

def auth(users, filenames, rights):
    
    while(True):
    
        print('\nLog in or sign up? ([commands/c] - to show available commands)\n> ', end='')
        answer = input()

        if(answer == 'exit' or answer == 'e'):
            print('')
            exit(0)

        elif(answer == 'commands' or answer == 'c'):
            print(HELP_LOGIN)
            continue
        
        elif(answer == 'sign' or answer == 's'):
            while(True):
                print('\nEnter your login (or empty string to cancel singing up) and password:\nlogin: ', end = '')
                login = input()
                if(login == ''):
                    break
                pswd = getpass('password: ')
                if(len(pswd) <= 1):
                    print('Password length must be 2 or more. Try Again.')
                    continue
                pswd_hash = hashlib.md5()
                pswd_hash.update(bytes(pswd, 'utf-8'))
                pswd_conf = getpass('confirm password: ')
                pswd_conf_hash = hashlib.md5()
                pswd_conf_hash.update(bytes(pswd_conf, 'utf-8'))
                if(pswd_hash.hexdigest() != pswd_conf_hash.hexdigest()):
                    print('Password confirmation failed. Try again.')
                    continue
                if(login.count(' ')):
                    print('Spaces are forbidden for usernames. Try again')
                    continue
                """if(users['logins'].count(login)):
                    print('Account with this name allready exists. Try again.')
                    continue"""
                break
            users = create_user(users, login, pswd_hash.hexdigest())
            print('You\'ve singed up successfully! You can log in now.')
            continue

        
        elif(answer == 'login' or answer == 'l'):
            success = 0
            while(True):
                print('\nEnter your login (or empty string to cancel loging in) and password:\nlogin: ', end = '')
                login = input()
                if(login == ''):
                    success
                    break
                pswd = getpass('password: ')
                if not(users['logins'].count(login)) or (len(pswd) < 2):
                    print('Wrong username or password! Try again.')
                    time.sleep(2)
                    continue
                ix = users['logins'].index(login)
                pswd_hash = hashlib.md5()
                pswd_hash.update(bytes(pswd, 'utf-8'))
                if(users['pswds'][ix] == pswd_hash.hexdigest()):
                    user_ix = ix
                    success = 1
                    break
                else:
                    print('Wrong username or password! Try again.')
                    time.sleep(2)
                    continue
            if(success):
                session(user_ix, users, filenames, rights)

        else:
            print('Wrong command!\n')          

user_ix = -1

users = get_users()
filenames = get_filenames()
rights = get_rights()

auth(users, filenames, rights)