# from cryptography.fernet import Fernet
import base64, hashlib
import os, sys

class EncryptionParams:
    def __init__(self):
        self.encrypted_folder = 'encrypted'
        self.decrypted_folder = 'decrypted'
        self.unencrypted_extensions = ['.txt', '.md']
        self.encrypted_extensions = ['.txte', '.mde']

def load_passcode() -> str:
    with open('password.password', 'r') as password_file:
        return password_file.read()
    return ''

def gen_fernet_key(passcode:str) -> bytes:
    ## This is a better method, but it requires saving the fernet Key
    # key = Fernet.generate_key() #this is your "password"
    # return key

    assert isinstance(passcode, str)
    hlib = hashlib.md5()
    hlib.update(passcode.encode('utf-8'))
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


def process_bytes(unprocessed:bytes, key:bytes, isEncrypt:bool) -> bytes:
    # fernet = Fernet(key)
    # if isEncrypt:
        # return fernet.encrypt(unprocessed)
    # else:
        # return fernet.decrypt(unprocessed)


    unprocessed = bytearray(unprocessed)

    key_len = len(key)

    if isEncrypt:
        for  i in range(len(unprocessed)):
            unprocessed[i] = (unprocessed[i] + key[i%key_len]) % 256
    else:
        for  i in range(len(unprocessed)):
            unprocessed[i] = (unprocessed[i] - key[i%key_len]) % 256
    return bytes(unprocessed)


def process_string(unprocessed:str, key:bytes, isEncrypt:bool) -> str:
    return process_bytes(unprocessed.encode('latin-1'), key, isEncrypt).decode('latin-1')


def process_file(filepath:str, passcode:str, isEncrypt:bool) -> str:
    key = gen_fernet_key(passcode)

    # Get output file extension
    params = EncryptionParams()
    outputExtension = os.path.splitext(filepath)[1]

    if isEncrypt:
        input_dir = params.decrypted_folder
        output_dir = params.encrypted_folder
        outputExtension += 'e'
    else:
        input_dir = params.encrypted_folder
        output_dir = params.decrypted_folder
        outputExtension = outputExtension[:-1] 

    # Open file and process 
    with open(f"{input_dir}/{filepath}", 'rb') as unprocessed:
        _file = unprocessed.read()
        processed = process_bytes(_file, key, isEncrypt)

    # Get output file name
    processedFileName = process_string(os.path.splitext(filepath)[0], key, isEncrypt)

    # Write output file
    with open(f'{output_dir}/{processedFileName}{outputExtension}', 'wb') as encrypted_file:
        encrypted_file.write(processed)
    
    return f'{processedFileName}{outputExtension}'


def process_folder(isEncrypt:bool, passcode:str=None) -> None:
    if passcode is None:
        passcode = load_passcode()

    params = EncryptionParams()

    if isEncrypt:
        desired_extensions = params.unencrypted_extensions
        input_dir = params.decrypted_folder
    else:
        desired_extensions = params.encrypted_extensions
        input_dir = params.encrypted_folder


    for f in os.listdir(f'{input_dir}'):
        if os.path.splitext(f)[1] in desired_extensions:
            process_file(f, passcode, isEncrypt)      


if __name__=="__main__":
    if len(sys.argv) > 1:
        needEncrypt = sys.argv[1] == 1
        process_folder(needEncrypt)
    else:
        process_folder(False)
