import streamlit as st
import os

from encryption import *




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

    process_folder(0, password)
    
    # Have a better explorer here
    fils = [ process_string(fil.split('.')[0], key, False) + '.' + fil.split('.')[1] for fil in  os.listdir('encrypted')]
    fils.sort()
    fils.append('')

    selected_file = st.sidebar.selectbox("Journal Files", fils)


    file_contents = ''
    with open(f"decrypted/{selected_file}", "r") as f:    
        file_contents = f.read()

    journal_mode = st.sidebar.radio("Mode Selection", ("Edit", "Render"))
    
    if journal_mode == "Render":
        st.markdown(file_contents)
    else:
        new_file_contents = st.text_area("Edit File", file_contents, 600)

        if new_file_contents != file_contents:
            st.button("Save File", on_click=process_file(selected_file,password, True))


    