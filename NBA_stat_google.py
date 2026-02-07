import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()

    gauth.settings['client_config_backend'] = 'service'
    gauth.settings['service_config'] = {
        "client_json_file_path": "service_account.json"
    }

    gauth.ServiceAuth()
    return GoogleDrive(gauth)

st.title("Google Drive with Service Account")

drive = connect_to_drive()

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

st.subheader("Files accessible to the service account:")
for f in file_list:
    st.write(f["title"], f["id"])
