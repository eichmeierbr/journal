import streamlit as st
import os
import hashlib

from encryption import *

# TODO: Reset app after add/delete

def verify_password(password: str) -> None:
    h = hashlib.blake2b()
    h.update(password.encode())
    a = h.hexdigest()

    if not a == st.secrets['password_verify']:
        if len(password) > 0:
            st.sidebar.text('Password incorrect')
        st.stop()


def get_decrypted_folder(files: list[str], key: bytes) -> list[str]:
    a = {fil:process_string(fil,key,False) for fil in files}
    return a


def save_file(file: str, text: str, key: bytes) -> None:

    enc_text = process_string(text, key, True).encode('latin-1')
    with open(file, "wb") as f:
        f.write(enc_text)


def rename_file(file_name: str, new_file_name: str, key: bytes) -> None:
    if not os.path.exists(f"encrypted/{file_name}"):
        st.text("File does not exsist")
    elif os.path.exists(f"encrypted/{process_string(new_file_name,key, True)}"):
        st.text("Desired File Name Taken")
    else:
        os.rename(f"encrypted/{file_name}", f"encrypted/{process_string(new_file_name,key, True)}")


def create_file(key: bytes) -> None:
    new_file_name = st.text_input("Enter File Name")
    if st.button("Save File"):
        encrypted_name = process_string(new_file_name, key, True)
        if not encrypted_name in os.listdir('encrypted'):
            st.text(f'Created File: {new_file_name}')
            with open(f'encrypted/{encrypted_name}', 'w') as fp:
                pass
        else:
            st.text(f'File already exists: {encrypted_name}')
    st.stop()


def delete_file(selected_file: str, file_contents: str) -> None:
    if st.checkbox("Are you SURE?"):
        if st.checkbox("Are you REALLY Sure? This is permanent"):
            if st.button("Final Delete"):
                del st.session_state.mode_selector
                st.write(st.session_state)
                os.remove(f'encrypted/{selected_file}')
                st.experimental_rerun()

    st.markdown(file_contents)


def edit_file(selected_file: str, file_contents: str, key: bytes, split=False) -> None:
    col1, col2 = st.columns(2)
    new_file_name = col1.text_input("File Name", process_string(selected_file,key,False), label_visibility='collapsed')
    col2.button("Rename File", on_click=rename_file, args=(selected_file, new_file_name, key))

    if split:
        new_file_contents = col1.text_area("File Contents", file_contents, 600)
        col2.markdown(file_contents)
    else:
        new_file_contents = st.text_area("File Contents", file_contents, 600)

    st.button("Save File", on_click=save_file, args=(f'encrypted/{selected_file}', new_file_contents, key))


if __name__=="__main__":
    st.set_page_config(layout="wide")
    st.title("Braden's Journal")

    password = st.sidebar.text_input("Enter Password", type="password")

    verify_password(password)
        
    key = gen_fernet_key(password)

    journal_mode = st.sidebar.radio("Mode Selection", (
                                                        "Edit", 
                                                        "View", 
                                                        "Split",
                                                        "Delete File",
                                                        "Add File", 
                                                        ),
                                                key="mode_selector")

    if journal_mode == "Add File":
        create_file(key)

    # TODO: Have a better explorer here
    # fils = [ process_string(fil.split('.')[0], key, False) + '.' + fil.split('.')[1] for fil in  os.listdir('encrypted')]
    # fils.sort()
    # fils.append('')

    # File directory
    fils = os.listdir('encrypted')
    files_decrypted = get_decrypted_folder(fils, key)
    selected_file = st.sidebar.selectbox("Journal Files", fils, format_func=lambda x: files_decrypted[x])

    # Read File
    file_contents = ''
    with open(f"encrypted/{selected_file}", "rb") as f:    
        fil_conts = f.read()  
        file_contents = process_bytes(fil_conts, key, False).decode('latin-1')

    
    if journal_mode == "View":
        st.markdown(file_contents)
    elif journal_mode == "Edit":
        edit_file(selected_file, file_contents, key)
    elif journal_mode == "Delete File":
        delete_file(selected_file, file_contents)
    elif journal_mode == "Split":
        edit_file(selected_file, file_contents, key, True)

