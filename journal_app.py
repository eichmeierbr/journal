import streamlit as st
import os

from encryption import *

def get_decrypted_folder(files, key):
    a = {fil:process_string(fil,key,False) for fil in files}
    return a

def save_file(file, text, key):
    enc_text = process_string(text, key, True).encode('latin-1')
    with open(f"encrypted/{selected_file}", "wb") as f:
        f.write(enc_text)


if __name__=="__main__":
    st.set_page_config(layout="wide")
    st.title("Braden's Journal")


    password = st.sidebar.text_input("Enter Password", type="password")
    save_passcode = load_passcode()

    if not password == save_passcode:
        if len(password) > 0:
            st.sidebar.text('Password incorrect')
        st.stop()
        
    key = gen_fernet_key(password)

    # TODO: Have a better explorer here
    # fils = [ process_string(fil.split('.')[0], key, False) + '.' + fil.split('.')[1] for fil in  os.listdir('encrypted')]
    # fils.sort()
    # fils.append('')

    fils = os.listdir('encrypted')
    files_decrypted = get_decrypted_folder(fils, key)
    selected_file = st.sidebar.selectbox("Journal Files", fils, format_func=lambda x: files_decrypted[x])

    file_contents = ''
    with open(f"encrypted/{selected_file}", "rb") as f:    
        fil_conts = f.read()  
        file_contents = process_bytes(fil_conts, key, False).decode('latin-1')

    journal_mode = st.sidebar.radio("Mode Selection", ("Edit", "Render"))
    
    if journal_mode == "Render":
        st.markdown(file_contents)
    else:
        new_file_contents = st.text_area("Edit File", file_contents, 600)

        if new_file_contents != file_contents:
            st.button("Save File", on_click=save_file, args=(f'encrypted/{selected_file}', new_file_contents, key))