#!/bin/bash

if ! command -v streamlit &> /dev/null
then
  echo "Streamlit tidak ditemukan, menginstal Streamlit..."
  pip install streamlit
fi

streamlit run main.py
