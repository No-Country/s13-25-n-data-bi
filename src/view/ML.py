import streamlit as st
import os
import pandas as pd
from data.SqlCommand import sqlCommand
from data.SnowflakeConnection import connectionBD

import yfinance as yf
from datetime import datetime, timedelta
from view.Datos import yahooFinance

def ml():
    icon = "🧠"
    title = "Modelo de Machine Learning"
    
    st.markdown(f"# {title} {icon}")
    st.sidebar.markdown(f"# {title} {icon}")
