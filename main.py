import secdel, getpass
from mabcapi import *
import texttable as tt

pwdPath = 'database/pwd.mbc'
loginsPath = 'database/logins.mbc'
passwordsPath = 'database/passwords.mbc'
sitesPath = 'database/sites.mbc'

###TMP
tmpLogins = 'database/tmpLogins'
tmpPwd = 'database/tmpPwd'
tmpSites = 'database/tmpSites'

class Database():

    def readLines(filename):
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines

    def displayTable(logins, passwords, sites):
        tab = tt.Texttable()
        tab.header(['id', 'username/email', 'password', 'website'])
        tab.set_cols_align(['c', 'l', 'l', 'l'])
    
        for i, (login, password, site) in enumerate(zip(logins, passwords, sites), start=1):
            tab.add_row([i, login, password, site])
        print(tab.draw())

class PasswordManager():

    def fileCheck():
        try:
            if os.path.exists(pwdPath):
                pass
            else:
                PasswordManager.setup()
                PasswordManager.login()
            if os.path.exists(loginsPath):
                pass
            else:
                with open(loginsPath, 'w') as file:
                    file.close()
            if os.path.exists(passwordsPath):
                pass
            else:
                with open(passwordsPath, 'w') as file:
                    file.close()
            if os.path.exists(sitesPath):
                pass
            else:
                with open(sitesPath, 'w') as file:
                    file.close()
            if os.path.exists(tmpLogins):
                pass
            else:
                with open(tmpLogins, 'w') as file:
                    file.close()
            if os.path.exists(tmpPwd):
                pass
            else:
                with open(tmpPwd, 'w') as file:
                    file.close()
            if os.path.exists(tmpSites):
                pass
            else:
                with open(tmpSites, 'w') as file:
                    file.close()

        except Exception as e:
            print(f"Error: {e}")

    def setup():
        print("Setup login credentials")
        login = input("login: ")
        password = input("password: ")

        loginSalt = Salt.generateSalt()
        passwordSalt = Salt.generateSalt()

        to_encode, s1, s2 = Salt.encryptCustomSalt(loginSalt, login)
        loginHash = Salt.createCiphertext(to_encode, s1, s2)
        to_encode, s1, s2 = Salt.encryptCustomSalt(passwordSalt, password)
        passwordHash = Salt.createCiphertext(to_encode, s1, s2)

        def generate():
            with open('database/pwd.mbc', 'w') as file:
                file.write(loginSalt + '\n')
                file.write(passwordSalt + '\n')
                file.write(loginHash + '\n')
                file.write(passwordHash + '\n')
                os.chmod('database/pwd.mbc', 0o444)
                print("Setup successfull")

        if os.path.exists('database'):
            generate()
        else:
            os.makedirs('database')
            generate()

    def checkCreds(login, password):
        with open(pwdPath, 'r') as file:
            loginSalt = file.readline()
            pwdSalt = file.readline()
            saltedLogin = file.readline()
            saltedPwd = file.readline()

        to_encode, s1, s2 = Salt.encryptCustomSalt(loginSalt.strip(), login)
        hashLogin = Salt.createCiphertext(to_encode, s1, s2)

        to_encode1, s11, s22 = Salt.encryptCustomSalt(pwdSalt.strip(), password)
        hashPwd = Salt.createCiphertext(to_encode1, s11, s22)

        if hashLogin == saltedLogin.strip() and hashPwd == saltedPwd.strip():
            return True
        else:
            return False
        
    def exitDatabase():
        os.system('cls')
        print("")
        pwd1 = input("pwd1: ")
        os.system('cls')
        pwd2 = input("pwd2: ")
        os.system('cls')
        BL = int(input("BL: "))
        os.system('cls')
        BD = int(input("BD: "))
        os.system('cls')

        secdel.main(loginsPath)
        secdel.main(passwordsPath)
        secdel.main(sitesPath)

        Encrypt.encrypt(pwd1, pwd2, BL, BD, tmpLogins, loginsPath)
        Encrypt.encrypt(pwd1, pwd2, BL, BD, tmpPwd, passwordsPath)
        Encrypt.encrypt(pwd1, pwd2, BL, BD, tmpSites, sitesPath)

        secdel.main(tmpLogins)
        secdel.main(tmpPwd)
        secdel.main(tmpSites)

    def addCreds():
        os.system('cls')
        login = getpass.getpass(prompt="login: ")
        os.system('cls')
        password = getpass.getpass(prompt="password: ")
        os.system('cls')
        site = getpass.getpass(prompt="site: ")
        os.system('cls')
        try:
            with open(tmpLogins, 'a') as file:
                file.write(login + '\n')
                file.close()
            with open(tmpPwd, 'a') as file:
                file.write(password + '\n')
                file.close()
            with open(tmpSites, 'a') as file:
                file.write(site + '\n')
                file.close()
            os.system('cls')
            print("Credentials added successfully")
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()
        except Exception as e:
            print(f"Error: {e}")
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()

    def editCreds():
        id = input("ID: ")
        if id.isalpha() == True:
            print("Wrong ID")
            os.system('cls')
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()
        else:
            with open(tmpLogins, 'r') as file:
                login = file.readlines()
                file.close()
            with open(tmpPwd, 'r') as file:
                password = file.readlines()
                file.close()
            with open(tmpSites, 'r') as file:
                site = file.readlines()
                file.close()

            if int(id) < 1 or int(id) > len(login):
                print("Invalid line number")
                PasswordManager.showDatabase()
                PasswordManager.databaseOperationHandler()

            newLogin = input("New login: ")
            os.system('cls')
            newPassword = input("New password: ")
            os.system('cls')
            newSite = input("New site: ")

            login[int(id) -1] = newLogin + '\n'
            password[int(id) - 1] = newPassword + '\n'
            site[int(id) - 1] = newSite + '\n'

            with open(tmpLogins, 'w') as file:
                file.writelines(login)
                file.close()
            with open(tmpPwd, 'w') as file:
                file.writelines(password)
                file.close()
            with open(tmpSites, 'w') as file:
                file.writelines(site)
                file.close()
            
            os.system('cls')
            print("Credentials saved successfully")
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()
        
    def deleteCreds():
        id = input("ID: ")
        if id.isalpha() == True:
            print("Wrong ID")
            os.system('cls')
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()
        else:
            with open(tmpLogins, 'r') as file:
                login = file.readlines()
                file.close()
            with open(tmpPwd, 'r') as file:
                password = file.readlines()
                file.close()
            with open(tmpSites, 'r') as file:
                site = file.readlines()
                file.close()

            if int(id) < 1 or int(id) > len(login):
                print("Invalid line number")
                PasswordManager.showDatabase()

            newLogin = ''
            newPassword = ''
            newSite = ''

            login[int(id) -1] = newLogin
            password[int(id) - 1] = newPassword
            site[int(id) - 1] = newSite

            with open(tmpLogins, 'w') as file:
                file.writelines(login)
                file.close()
            with open(tmpPwd, 'w') as file:
                file.writelines(password)
                file.close()
            with open(tmpSites, 'w') as file:
                file.writelines(site)
                file.close()

            os.system('cls')
            print("Credentials deleted successfully")
            PasswordManager.showDatabase()
            PasswordManager.databaseOperationHandler()
    
    def databaseOperationHandler():
        print("")
        print("[1] Add credentials")
        print("[2] Edit credentials")
        print("[3] Delete credentials")
        print("[4] Erase database")
        print("[5] Refresh")
        print("[6] Exit")
        print("")
        choice = input(">: ")
        match choice:
            case '1':
                PasswordManager.addCreds()
            case '2':
                PasswordManager.editCreds()
            case '3':
                PasswordManager.deleteCreds()
            case '4':
                PasswordManager.eraseDatabase()
            case '5':
                os.system('cls')
                PasswordManager.showDatabase()
                PasswordManager.databaseOperationHandler()
            case '6':
                PasswordManager.exitDatabase()
            case _:
                os.system('cls')
                PasswordManager.menu()

    def eraseDatabase():
        os.system('cls')
        print("WARNING: THIS ACTION CAN NOT BE REVERSED!")
        print("DO YOU WISH TO CONTINUE?")
        print("")
        print("yes/no")
        choice = input(">: ")

        match choice:
            case 'yes':
                secdel.delete_file(loginsPath)
                secdel.delete_file(passwordsPath)
                secdel.delete_file(sitesPath)
                secdel.delete_file(tmpLogins)
                secdel.delete_file(tmpPwd)
                secdel.delete_file(tmpSites)
                print("Database Successfully erased")
                sys.exit()
            case 'no':
                PasswordManager.showDatabase()
                PasswordManager.databaseOperationHandler()
            case _:
                print("Wrong action")
                PasswordManager.showDatabase()
                PasswordManager.databaseOperationHandler()
        
    def decryptDatabase():
        os.system('cls')
        print("Enter your database credentials")
        print("")
        pwd1 = input("pwd1: ")
        os.system('cls')
        pwd2 = input("pwd2: ")
        os.system('cls')
        BL = int(input("BL: "))
        os.system('cls')
        BD = int(input("BD: "))
        os.system('cls')

        Decrypt.decrypt(pwd1, pwd2, BL, BD, loginsPath, tmpLogins)
        Decrypt.decrypt(pwd1, pwd2, BL, BD, passwordsPath, tmpPwd)
        Decrypt.decrypt(pwd1, pwd2, BL, BD, sitesPath, tmpSites)
        print("Database decrypted successfully")

    def showDatabase():
        logins = Database.readLines(tmpLogins)
        passwords = Database.readLines(tmpPwd)
        sites = Database.readLines(tmpSites)

        Database.displayTable(logins, passwords, sites)

    def menu():
        print("Password Manager by MabSec")
        print("")
        print("[1] Database")
        print("[2] Info")
        choice = input(">: ")
        match choice:
            case '1':
                PasswordManager.decryptDatabase()
                PasswordManager.showDatabase()
                PasswordManager.databaseOperationHandler()
            case '2':
                os.system('cls')
                print("Version: 1.0")
                PasswordManager.menu()
            case _:
                os.system('cls')
                PasswordManager.menu()

    def login():
        print("Login")
        login = getpass.getpass(prompt=">: ")
        os.system('cls')
        pwd = getpass.getpass(prompt=">: ")
        os.system('cls')
        auth = PasswordManager.checkCreds(login, pwd)
        match auth:
            case False:
                print("Wrong Credentials!")
                sys.exit()
            case True:
                PasswordManager.menu()

PasswordManager.fileCheck()
PasswordManager.login()