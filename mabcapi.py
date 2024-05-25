import sys, string, os
from random import randint, choice

alphabet =  string.ascii_lowercase + \
           '1234567890`~!@#$%^&*()-_=+[{]};:.,?"/\'' + \
           string.ascii_uppercase
alphabet_only_letters =  string.ascii_lowercase + string.ascii_uppercase
digits = '0123456789'

class Salt(): #for -s/-ss

    def generateSalt(): #generate random salt
        salt = ''
        i = 0
        while i != 16:
            letter_or_digit = randint(0, 1)
            if letter_or_digit == 0:
                chosen_letter = choice(alphabet_only_letters)
                salt += chosen_letter
            else:
                chosen_digit = choice(digits)
                salt += chosen_digit
            i += 1
        return salt
    
    def encryptRandomSalt(input): #split salt into two parts and mix with input
        s1 = Salt.generateSalt()
        s2 = Salt.generateSalt()
        s = s1 + s2
        print(f"Salt: {s}")
        to_encode = s1 + input + s2
        return to_encode, s1, s2

    def encryptCustomSalt(salt, input): #split custom salt into two parts and mix with input
        index = len(salt) // 2
        s1 = salt[:index]
        s2 = salt[index:]
        s = s1 + s2
        to_encode = s1 + input + s2
        return to_encode, s1, s2

    def createCiphertext(input, s1, s2): #encrypt using salt
        cipher = ''
        num_to_delete = len(s2) - 27
        mod = Logic.alphabetModify(s1)
        all_lines = Logic.stringModify(s2, mod)
        extracted_characters = Logic.charExtract(mod, all_lines)
        modified_extracted_characters = Logic.charRightDel(extracted_characters, num_to_delete)
        final_result = Logic.charExtractedDel(modified_extracted_characters, 2)
        cipher = Logic.textEncrypt(mod, final_result.split(), input)
        return cipher

class Logic(): #main logic of the cipher

    #####FOR ENCRYPTION/DECRYPTION#####

    def alphabetModify(pwd1):
        alphabet_list = list(alphabet)
        for char in pwd1:
            if char in alphabet_list:
                alphabet_list.remove(char)
        modified_alphabet = ''.join(alphabet_list)
        result = pwd1 + modified_alphabet
        return result

    def stringModify(pwd2, mod):
        lines = []
        for char in pwd2:
            index = mod.find(char)
            if index != -1:
                before_char = mod[:index]
                after_char = mod[index:]
                mod = after_char + before_char
                lines.append(mod)
        return lines

    def charExtract(mod, all_lines):
        extracted = ''
        for i, char in enumerate(mod):
            for line in all_lines:
                if i < len(line):
                    extracted += line[i]
            extracted += ' '
        return extracted.strip()

    def charRightDel(extracted, num_of_chars_to_delete):
        chars_list = extracted.split()
        modified_chars_list = [char[:-num_of_chars_to_delete] if len(char) > num_of_chars_to_delete else '' for char in chars_list]
        modified_extracted = ' '.join(modified_chars_list)
        return modified_extracted

    def charExtractedDel(extracted, BD):
        chars_list = extracted.split()
        modified_chars_list = [char[:BD-1] + char[BD:] if len(char) > BD else char for char in chars_list]
        modified_extracted = ' '.join(modified_chars_list)
        return modified_extracted
    
    def textEncrypt(mod, final_result, encrypt_me):
        encrypted_text = ''
        for char in encrypt_me:
            if char in mod:
                index = mod.find(char)
                if index != -1 and index < len(final_result):
                    encrypted_text += final_result[index]
                else:
                    encrypted_text += char
            else:
                encrypted_text += char
        return encrypted_text
    
    ###################################
    
    #####ONLY FOR DECRYPTION#####
    
    def bitsIndex(divided_bits, final_result):
        indexed_bits = []
        for item in divided_bits:
            if item in final_result:
                index = final_result.index(item) + 1
                indexed_bits.append(index)
        return indexed_bits

    def bitsDivide(mod, phrase, total_char):
        divided_bits = []
        for i in range(0, len(phrase), total_char):
            divided_bits.append(phrase[i:i+total_char])
        return divided_bits

    def textDecrypt(mod, indexed_bits):
        result = ''
        for number in indexed_bits:
            if 0 < number <= len(mod):
                result += mod[number - 1]
            else:
                result += ' '
        plaintext = result.strip()
        return plaintext
    
    ########################

    #####INTERACTING WITH FILES#####

    def extractInput(phrase):
        try:
            with open(phrase, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print("Error: File Not Found")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def saveOutput(output_file, text):
        try:
            if not os.path.exists(output_file):
                with open(output_file, 'w') as file:
                    pass
            with open(output_file, 'a') as file:
                file.write(text + '\n')
        except Exception as e:
            print(f"Error: {e}")

    ################################

class Encrypt(): # for -e

    def encrypt(pwd1, pwd2, BL, BD, input_file, output_file):
        num_to_delete = len(pwd2) - BL
        mod = Logic.alphabetModify(pwd1)
        plaintext = Logic.extractInput(input_file)
        for line in plaintext: #encrypt for each line in input file
            extracted_characters = Logic.charExtract(mod, Logic.stringModify(pwd2, mod))
            modified_extracted_characters = Logic.charRightDel(extracted_characters, num_to_delete)
            final_result = Logic.charExtractedDel(modified_extracted_characters, BD)
            cipher = Logic.textEncrypt(mod, final_result.split(), line.strip())
            Logic.saveOutput(output_file, cipher.replace(" ", "")) #automatically save output to file

class Decrypt(): #for -d

    def decrypt(pwd1, pwd2, BL, BD, input_file, output_file):
        num_to_delete = len(pwd2) - BL
        total_char = len(pwd2) - num_to_delete - 1
        mod = Logic.alphabetModify(pwd1)
        ciphertext = Logic.extractInput(input_file)
        for line in ciphertext: #decrypt for each line in input file
            all_lines = Logic.stringModify(pwd2, mod)
            extracted_characters = Logic.charExtract(mod, all_lines)
            modified_extracted_characters = Logic.charRightDel(extracted_characters, num_to_delete)
            final_result = Logic.charExtractedDel(modified_extracted_characters, BD)
            bits = Logic.bitsDivide(mod, line.strip(), total_char)
            index_bits = Logic.bitsIndex(bits, final_result.split())
            plaintext = Logic.textDecrypt(mod, index_bits)
            Logic.saveOutput(output_file, plaintext.replace(" ", "")) #automatically save output to file

class Utils(): #utility

    def checkAction(action):
        actions = ['-e', '-d', '-s', '-cs', '-h', '-v'] #all available options
        if action not in actions:
            Utils.errorMessage("WrongAction")
        if action == '-v':
            Utils.versionInfo()
        if action == '-h':
            Utils.usageInfo()

    def checkArgs(action, pwd1, pwd2, BL, BD, input_file, output_file): # here we check if the variables are correct
        Utils.checkAction(action)
        if BL >= len(pwd2):
            Utils.errorMessage("TooHighBL")
            sys.exit()
        if BD > BL:
            Utils.errorMessage("TooHighBD")
            sys.exit()
        if not os.path.exists(input_file):
            Utils.errorMessage("FileDoesNotExist")
        match action: #two main functions
            case '-e':
                Encrypt.encrypt(pwd1, pwd2, BL, BD, input_file, output_file)
            case '-d':
                Decrypt.decrypt(pwd1, pwd2, BL, BD, input_file, output_file)

    def errorMessage(type): #some error messages
        match type:
            case "WrongAction":
                print("Error: Wrong action")
                print("Available options: -e/-d/-s/-cs")
                sys.exit()
            case "TooHighBL":
                print("Error: BL can't be higher than the length of pwd2")
                sys.exit()
            case "TooHighBD":
                print("Error: BD can't be higher than BL")
                #LSiq29rzx5goejqyv3fnejhpw4ktludl/Fw4ktfnqyv3fnejgoktrzx5w4w4rzsifn
                sys.exit()
            case "FileDoesNotExist":
                print("Error: Specified input file does not exist")
                sys.exit()
            case "WrongArgumentCount":
                print("Error: Wrong argument count")
                print("Use: mabc -h for help")
                sys.exit()

    def versionInfo(): #version info
        print("Mab-Cipher")
        print("v1.4 by MabSec")

    def usageInfo(): #usage info
        print("""
Mab-Cipher Usage:
              
-e  - Encrypt
-d  - Decrypt
-s  - Encrypt with random salt
-cs - Encrypt with custom salt
-v  - Version info
-h  - prints this menu

mabc {-e/-d} {pwd1} {pwd2} {BL} {BD} {input_file} {output_file}
mabc {-s} {plaintext}
mabc {-cs} {salt} {plaintext}
              """)
        sys.exit()