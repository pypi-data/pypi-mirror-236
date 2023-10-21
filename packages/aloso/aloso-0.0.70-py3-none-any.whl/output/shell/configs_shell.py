import codecs
import hashlib
import logging
import os
import re
import subprocess

from Crypto.Cipher import AES

import config
from domain.configs_management import ConfigsManagement


class ConfigsShell(ConfigsManagement):
    data_base: str = "ftp_password = \n" \
                     "grafana_password = \n" \
                     "syslog_password = \n" \
                     "ansible_password = \n" \
                     "equipments_password = \n" \
                     "ssh_password = "

    ###  CONFIGURATION FILE  ###

    def edit_variable(self):
        try:
            with open(self.config_file_path, 'r+') as file:
                lines = file.readlines()
                variables_names = [line.split('=')[0].strip() for line in lines]

                if self.variable_name not in variables_names:
                    logging.error(
                        f'La variable {self.variable_name} n\'existe pas dans le fichier {self.config_file_path}')
                    return False

                for index, line in enumerate(lines):
                    if self.variable_name in line.strip():
                        if isinstance(self.variable_value, int):
                            lines[index] = f'{self.variable_name} = {self.variable_value}\n'
                        else:
                            lines[index] = f'{self.variable_name} = "{self.variable_value}"\n'
                        break

                file.seek(0)
                file.writelines(lines)
                file.truncate()
            logging.info(f'La variable {self.variable_name} a été modifiée avec succès')
            return True
        except Exception as e:
            logging.error(f'Une erreur est survenue lors de la modification de la variable {self.variable_name} : {e}')
            return False

    @staticmethod
    def find_sample_file(env_folder_path):
        for root, dirs, files in os.walk(env_folder_path):
            for file in files:
                if file == 'config_sample.py':
                    return os.path.join(root, file)
        return None

    @staticmethod
    def update_production_config_file(sample_file_path: str,
                                      config_file_path_to_update: str):

        with open(sample_file_path, "r") as file_1, open(config_file_path_to_update, "r") as file_2:
            file_1_content = file_1.read()
            file_2_content = file_2.read()

        print("\033[1m\033[32mRécupération des variables du fichier de configuration...\033[0m")
        file_1_vars = dict(re.findall(r'(\w+)\s*=\s*(.*)', file_1_content))
        file_2_vars = dict(re.findall(r'(\w+)\s*=\s*(.*)', file_2_content))

        print("\033[1m\033[32mCopie des nouvelles variables...\033[0m")
        for var_name, var_value in file_1_vars.items():
            if var_name not in file_2_vars.keys():
                file_2_content += f"\n{var_name} = {var_value}"

        print("\033[1m\033[32mSuppression des variables non utilisées...\033[0m")
        for var_name, var_value in file_2_vars.items():
            if var_name not in file_1_vars.keys():
                file_2_content = re.sub(pattern=rf"{var_name}\s*=\s*(.*)", repl="", string=file_2_content)

        with open(config_file_path_to_update, 'w') as file:
            file.write(file_2_content)

    def modify_from_dict(self, param_dict: dict, my_config_file=None):
        if not my_config_file:
            self.config_file_path = f"{config.root_dir}/config.py"
        else:
            self.config_file_path = my_config_file
        try:
            for key, value in param_dict.items():
                self.variable_name = key
                self.variable_value = value
                # print(f"{key} = {value}")
                self.edit_variable()
            return True
        except Exception as err:
            return err.__str__()

    ###  PACKAGE VERSION  ###

    @staticmethod
    def get_version_package(path: str = config.package_dir, env_path: str = config.env_path):
        try:
            command = f"cd {path} && source {env_path}/activate &&  pip show aloso | grep Version"
            result = subprocess.run(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
            return result.stdout.decode('utf-8').split(': ')[1]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de la version : {e}")
            return ''

    ###  SALT  ###

    @staticmethod
    def salt(salt_p):
        salt_phrase = f"$2a$12$/qzser"
        hashed_salt = hashlib.pbkdf2_hmac(hash_name='sha512', password=salt_p.encode('utf-8'),
                                          salt=salt_phrase.encode('utf-8'), iterations=100000)
        salt_hash = codecs.encode(hashed_salt, "base64")
        return salt_hash

    @staticmethod
    def generate_salt_file(list_data: list[str] = None, salt_file: str = config.salt_file,
                           clear_file: str = config.clear_salt):
        key = ConfigsShell.salt(config.cchottsa_herbenv)[0:32]
        initial_vector = b'o\xa59\x8f\xeaf\xdc\xa477\xa1\xcfg\x87Ip'
        cipher = AES.new(key, AES.MODE_OFB, initial_vector)
        if list_data:
            ciphertext = cipher.encrypt(str.encode("\n".join(list_data)))
        else:
            with open(f"{clear_file}", "rb") as file:
                plaintext = file.read()
                ciphertext = cipher.encrypt(plaintext)
            os.system(f"rm {clear_file}")
        with open(f"{salt_file}", "wb") as file:
            file.write(ciphertext)

    @staticmethod
    def get_salt_content(salt_file: str = config.salt_file):
        key = ConfigsShell.salt(config.cchottsa_herbenv)[0:32]
        initial_vector = b'o\xa59\x8f\xeaf\xdc\xa477\xa1\xcfg\x87Ip'
        cipher = AES.new(key, AES.MODE_OFB, initial_vector)
        with open(f"{salt_file}", "rb") as file:
            ciphertext = file.read()
            plaintext = cipher.decrypt(ciphertext)
            our_salt = bytes.decode(plaintext)
        return our_salt

    @staticmethod
    def generate_clear_salt(salt_file: str = config.salt_file, clear_salt: str = config.clear_salt):
        if os.path.isfile(f"{salt_file}"):
            our_salt = ConfigsShell.get_salt_content(salt_file)
        else:
            our_salt = ConfigsShell.data_base
        with open(f"{clear_salt}", "w") as file:
            file.write(our_salt)

    @staticmethod
    def get_value_config(my_config_value: str = config.salted_name, salt_file: str = config.salt_file):
        our_salt = ConfigsShell.get_salt_content(salt_file=salt_file)
        for salts in our_salt.split('\n'):
            if salts.startswith(my_config_value):
                return salts.split(' = ')[1]
        return "This variable does not exist"

    @staticmethod
    def get_value(variable: str, salt_file: str = config.salt_file):
        our_salt = ConfigsShell.get_salt_content(salt_file)
        for salts in our_salt.split('\n'):
            if salts.split(' = ')[0] == variable:
                return salts.split(' = ')[1]
        return None

    @staticmethod
    def delete_salt(salted_name: str, salt_file: str = config.salt_file):
        print(f'delete {salted_name}')
        our_salt = ConfigsShell.get_salt_content(salt_file=salt_file)
        list_salt = our_salt.split('\n')
        new_list = []
        for salts in list_salt:
            if not salts.split(' = ')[0] == salted_name:
                new_list.append(salts)
        ConfigsShell.generate_salt_file(new_list, salt_file=salt_file)

    @staticmethod
    def update_salt(name: str, value: str, salt_file: str = config.salt_file):
        # print(f'update {name}, value = {value}')
        our_salt = ConfigsShell.get_salt_content(salt_file=salt_file)
        list_salt = our_salt.split('\n')
        bool_check_name_in_salt = False
        line_same_name = ""
        new_salts = f"{name} = {value}"

        for salts in list_salt:
            if salts.split(' = ')[0] == name:
                bool_check_name_in_salt = True
                line_same_name = salts

        if bool_check_name_in_salt:
            list_salt.remove(line_same_name)
            list_salt.append(new_salts)
            ConfigsShell.generate_salt_file(list_salt, salt_file=salt_file)
        else:
            ConfigsShell.create_salt(name=name, value=value, salt_file=salt_file)

    @staticmethod
    def create_salt(name: str, value: str, salt_file: str = config.salt_file):
        # print(f'update {name}, value = {value}')
        our_salt = ConfigsShell.get_salt_content(salt_file=salt_file)
        list_salt = our_salt.split('\n')
        new_salts = f"{name} = {value}"
        bool_new_value = False

        for line in list_salt:
            bool_new_value = False
            if line.split(' = ')[0] != name:
                bool_new_value = True

        if bool_new_value:
            list_salt.append(new_salts)
            ConfigsShell.generate_salt_file(list_salt, salt_file=salt_file)


if __name__ == '__main__':
    # ConfigsShell.generate_clear_salt()
    # ConfigsShell.generate_salt_file()
    # print(ConfigsShell.get_salt_content())
    ...
