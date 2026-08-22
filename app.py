"""
DTAA Advisor - Main Streamlit Application
AI-Powered Double Tax Treaty Advisory Suite for Chartered Accountants
Built under Income Tax Act, 2025 | Income Tax Rules, 2026
TAXAVK — Beespoke Tax Advisors | AICA Level 2 Capstone 2026
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="DTAA Advisor | TAXAVK",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — TAXAVK Executive Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --bg:        #0D1117;
        --panel:     #161B22;
        --panel-h:   #1C2330;
        --gold:      #C9A84C;
        --gold-lt:   #E8C97D;
        --gold-dim:  rgba(201,168,76,0.20);
        --gold-glow: rgba(201,168,76,0.10);
        --text:      #E6EDF3;
        --muted:     #8B949E;
        --grid:      rgba(201,168,76,0.04);
        --red:       #F85149;
        --green:     #3FB950;
        --yellow:    #E3B341;
    }

    /* App background — deep navy with faint gold grid */
    .stApp {
        background-color: var(--bg);
        background-image:
            linear-gradient(var(--grid) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    html, body, [class*="css"] { color: var(--text); font-family: 'Inter', sans-serif; }

    /* Main header — dark executive panel */
    .main-header {
        background: linear-gradient(135deg, #161B22 0%, #1C2330 50%, #161B22 100%);
        color: var(--text);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        border: 1px solid var(--gold-dim);
        box-shadow: 0 4px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(201,168,76,0.06);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: "";
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--gold) 30%, var(--gold-lt) 50%, var(--gold) 70%, transparent 100%);
        animation: hdr-shimmer 3s ease-in-out infinite;
    }
    .main-header::after {
        content: "";
        position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
    }
    @keyframes hdr-shimmer {
        0%, 100% { opacity: 0.5; }
        50%       { opacity: 1.0; }
    }
    .main-header h1 {
        color: var(--gold);
        margin: 0; font-size: 2.2rem;
        font-family: 'Orbitron', sans-serif; font-weight: 800;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(201,168,76,0.25);
    }
    .main-header p {
        color: var(--muted); margin: 0.5rem 0 0; font-size: 0.875rem;
        font-family: 'Inter', sans-serif; font-weight: 300; letter-spacing: 0.3px;
    }
    .main-header .brand-tag {
        display: inline-block; margin-top: 0.8rem;
        font-family: 'Orbitron', sans-serif; font-size: 0.7rem;
        letter-spacing: 3px; color: #0D1117;
        background: linear-gradient(135deg, var(--gold), var(--gold-lt));
        padding: 4px 14px; border-radius: 3px; font-weight: 700;
    }

    /* Risk badges */
    .risk-low  { background: rgba(63,185,80,0.10);  color: #3FB950; padding: 6px 14px;
                 border-radius: 4px; font-weight: 600; font-size: 0.85rem;
                 border: 1px solid rgba(63,185,80,0.30);  font-family: 'Inter', sans-serif; }
    .risk-med  { background: rgba(227,179,65,0.10);  color: #E3B341; padding: 6px 14px;
                 border-radius: 4px; font-weight: 600; font-size: 0.85rem;
                 border: 1px solid rgba(227,179,65,0.30); font-family: 'Inter', sans-serif; }
    .risk-high { background: rgba(248,81,73,0.10);   color: #F85149; padding: 6px 14px;
                 border-radius: 4px; font-weight: 600; font-size: 0.85rem;
                 border: 1px solid rgba(248,81,73,0.30);  font-family: 'Inter', sans-serif; }

    /* Info boxes */
    .ita-box {
        background: rgba(22,27,34,0.9); border-left: 3px solid var(--gold);
        border-top: 1px solid var(--gold-dim); border-right: 1px solid var(--gold-dim);
        border-bottom: 1px solid var(--gold-dim);
        padding: 0.9rem 1.2rem; border-radius: 0 8px 8px 0;
        margin: 0.8rem 0; font-size: 0.85rem; color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    .warning-box {
        background: rgba(248,81,73,0.06); border-left: 3px solid var(--red);
        border-top: 1px solid rgba(248,81,73,0.15); border-right: 1px solid rgba(248,81,73,0.15);
        border-bottom: 1px solid rgba(248,81,73,0.15);
        padding: 0.9rem 1.2rem; border-radius: 0 8px 8px 0;
        margin: 0.8rem 0; font-size: 0.85rem; color: var(--red);
        font-family: 'Inter', sans-serif;
    }
    .success-box {
        background: rgba(63,185,80,0.06); border-left: 3px solid var(--green);
        border-top: 1px solid rgba(63,185,80,0.15); border-right: 1px solid rgba(63,185,80,0.15);
        border-bottom: 1px solid rgba(63,185,80,0.15);
        padding: 0.9rem 1.2rem; border-radius: 0 8px 8px 0;
        margin: 0.8rem 0; font-size: 0.85rem; color: var(--green);
        font-family: 'Inter', sans-serif;
    }

    /* Metric cards */
    .metric-card {
        background: var(--panel); border: 1px solid var(--gold-dim);
        border-radius: 10px; padding: 1.2rem 1rem; text-align: center;
        box-shadow: 0 2px 16px rgba(0,0,0,0.3);
        transition: all 0.3s ease; position: relative; overflow: hidden;
    }
    .metric-card::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
    }
    .metric-card:hover {
        border-color: rgba(201,168,76,0.5);
        box-shadow: 0 4px 24px rgba(201,168,76,0.15); transform: translateY(-2px);
    }
    .metric-card h3 {
        color: var(--gold); font-size: 2rem; margin: 0;
        font-family: 'Orbitron', sans-serif; font-weight: 700;
        text-shadow: 0 0 20px rgba(201,168,76,0.25);
    }
    .metric-card p {
        color: var(--muted); font-size: 0.72rem; margin: 0.4rem 0 0;
        font-family: 'Inter', sans-serif; letter-spacing: 1.5px;
        text-transform: uppercase; font-weight: 500;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117, #0A0E13);
        border-right: 1px solid var(--gold-dim);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--gold), var(--gold-lt));
        color: #0D1117; font-family: 'Orbitron', sans-serif; font-weight: 700;
        border: none; border-radius: 6px; letter-spacing: 0.8px;
        box-shadow: 0 2px 16px rgba(201,168,76,0.25);
        transition: all 0.3s ease; font-size: 0.8rem;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 24px rgba(201,168,76,0.45);
        transform: translateY(-2px);
        background: linear-gradient(135deg, var(--gold-lt), var(--gold));
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--panel); border-radius: 8px 8px 0 0;
        border-bottom: 1px solid var(--gold-dim); gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif; color: var(--muted);
        font-size: 0.8rem; font-weight: 500;
        border-bottom: 2px solid transparent; transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom-color: var(--gold) !important;
        background: var(--gold-glow) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--gold-lt) !important; background: var(--gold-glow) !important;
    }

    /* Output area */
    .output-box {
        background: var(--panel); border: 1px solid var(--gold-dim);
        border-left: 3px solid var(--gold);
        border-radius: 8px; padding: 1.5rem;
        font-family: 'Inter', sans-serif; line-height: 1.8;
        color: var(--text); box-shadow: 0 2px 16px rgba(0,0,0,0.2);
    }

    /* Headings */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: var(--gold); }

    /* Inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: var(--panel) !important; border-color: var(--gold-dim) !important;
        color: var(--text) !important; border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* st.metric native */
    [data-testid="metric-container"] {
        background: var(--panel); border: 1px solid var(--gold-dim);
        border-radius: 10px; padding: 1rem;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] { color: var(--muted) !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--gold) !important; font-family: 'Orbitron', sans-serif;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--panel) !important; color: var(--text) !important;
        border: 1px solid var(--gold-dim) !important; border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Dividers */
    hr { border-color: var(--gold-dim) !important; }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }

    /* Captions */
    .stCaption { color: var(--muted) !important; font-family: 'Inter', sans-serif !important; }

    /* st.info / st.success / st.warning / st.error — native alert boxes
       (these default to light backgrounds and were left unstyled, which is
       why they showed up as solid white blocks against the dark theme) */
    [data-testid="stAlert"] {
        background: var(--panel) !important;
        border: 1px solid var(--gold-dim) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stAlert"] p { color: var(--text) !important; }
    [data-testid="stAlertContentInfo"]    { border-left: 3px solid var(--gold) !important; }
    [data-testid="stAlertContentSuccess"] { border-left: 3px solid var(--green) !important; }
    [data-testid="stAlertContentWarning"] { border-left: 3px solid var(--yellow) !important; }
    [data-testid="stAlertContentError"]   { border-left: 3px solid var(--red) !important; }

    /* Dropdown / select menus render in a portal outside .stApp, so they
       need to be targeted separately or they fall back to white */
    div[data-baseweb="popover"] ul[data-baseweb="menu"],
    div[data-baseweb="select"] div[role="listbox"] {
        background: var(--panel) !important;
        border: 1px solid var(--gold-dim) !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li {
        background: var(--panel) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="popover"] li:hover {
        background: var(--gold-glow) !important;
    }

    /* Radio / checkbox labels */
    .stRadio label, .stCheckbox label, .stMultiSelect label,
    .stSelectbox label, .stTextInput label, .stTextArea label,
    .stNumberInput label, .stDateInput label, .stFileUploader label {
        color: var(--text) !important; font-family: 'Inter', sans-serif !important;
    }
    .stRadio [role="radiogroup"] label span,
    .stCheckbox label span { color: var(--text) !important; }

    /* Multiselect selected-item tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: var(--gold-dim) !important; color: var(--text) !important;
    }

    /* File uploader dropzone */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--panel) !important; border: 1px dashed var(--gold-dim) !important;
    }
    [data-testid="stFileUploaderDropzone"] * { color: var(--muted) !important; }

    /* Date input */
    .stDateInput input {
        background: var(--panel) !important; color: var(--text) !important;
        border-color: var(--gold-dim) !important;
    }

    /* Expander body */
    .streamlit-expanderContent {
        background: rgba(22,27,34,0.6) !important; color: var(--text) !important;
        border: 1px solid var(--gold-dim) !important; border-top: none !important;
    }

    /* st.dataframe / st.table wrapper */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: var(--panel) !important; border-radius: 8px;
        border: 1px solid var(--gold-dim);
    }

    /* Sidebar text + widgets */
    section[data-testid="stSidebar"] * { color: var(--text); }
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: var(--panel-h) !important; border-color: var(--gold-dim) !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── OPENING SOUND (plays a short chime once when the app loads) ────────────
_CHIME_B64 = "UklGRtIzAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0Ya4zAAAAAAYAGQA1AFcAewCbALIAvAC1AJoAagApANn/ff8e/8L+cv42/hP+EP4w/nT+2v5d//f/ngBIAekBdQLhAiMDNAMPA7QCJQJqAYwAmv+g/rD92/ww/Lz7ifuf+/77pPyJ/aH+2/8kAWgCkAOJBEEFqQW4BWkFvgS/A3oCAgFu/9X9UvwA+/X5Rvn/+Cj5w/nI+ir81P2t/5gBdgMpBZMGmwctCD8IygfTBmgFnAOKAVT/G/0E+zL5xPfU9nT2rfZ/99/4uvr1/Gz/+QF0BLMGkQjtCa8KyAoyCvQIHwfOBCQCTf9y/MX5cPec9Wj06vMu9DL16fY7+QT8Gf9JAmEFLwiECjkMLg1SDaAMHgvjCBAG0AJY/9z7lvi89X3zAPJg8arx3fLo9K33Avuz/oYCPQacCWwMfA6qD94PFA9TDbYKYwePA3b/V/t39xX0aPGf79juI++A8NryEPbv+Tv+sAIIB/oKRw64ECISbBKNEZEPlQzGCF8Epv/l+mn2fPJe70PtUeya7BvuwfBk9Mv4sf3IAsEHSQwXEOsSlhT5FAwU2RGCDjkKQQXp/4X6bPXx8F7t7urM6Q3qsOud7qnylfcU/c4CaAiIDdoRFhUGF4cXjxYqFHwQvAs0Bj0ANvp/9HTvaeug6Ernfuc96W7s4PBP9mX8wQL+CLgOkBM3F3AZFRoXGYQWghJODToHpQD6+aPzBe5/6VnmyuTt5MTmNOoK7/n0pPuhAoIJ1w85FU8Z1huiHKMb5hiUFO8OUAggAdH52PKm7KDnGeRN4lviReTw5yXtkvPR+m8C9AnmENQWXRs2Hi4fMx5RG7MWoBB4CawBuvke8lXrzeXi4dPfx9/A4aPlM+sa8uz5KwJVCuURYhhiHZEguSHGIMMd3RhgErEKTAK1+XbxFOoH5LLfXt0y3TbfS+M06ZPw9fjTAaMK1BLiGVsf5SJCJFwjPCASGy4U/Av9AsP53/Di6E3ii93t2p7ap9zr4Cfn/O7s92oB3gqxE1QbSiEyJckm9CW8IlIdChZXDcED5Pla8MDnn+Bt24DYCdgT2oHeDuVV7dL27QAIC34UtxwuI3gnTimPKEMlnh/1F8MOlwQX+ufvrub/3lnZGNZ11XvXD9zp4p7rpvVeAB8LOhUMHgYltynPKysr0CfzIe4ZPxCABV36hu+s5YDdfdcD1EnTW9UY2jXhPuqj9L//3gpQFWweoSV8Kq4sFSy6KNMivhr9ECsG+PoV8DDm6d3E1yPUQNMq1cLZv+Cw6Qb0HP8/Cr8U8x1IJUcqoSwxLP0oOSNAG5MRzQab+67wt+ZU3g3YRdQ60/zUbtlK4CLpafN4/qAJLhR5HewkECqSLEssPimdI8EbKRJuBz78SPE+58HeWNhq1DbTz9Qc2djfl+jM8tX9AAmcE/0cjyTXKYEsYix9Kf8jQRy+Eg8I4fzj8cfnL9+l2JHUNNOl1MzYZ98M6DDyMv1gCAgTgBwvJJspbSx3LLkpXyS/HFITsAiE/X7yUeif3/TYutQ1033Uftj43oLnlfGP/L8HdBIBHM4jXSlXLIos9Cm+JDsd5RNQCSf+GvPc6BHgRdnl1DjTV9Qy2Ire+ub78Oz7HgfeEYEbayMeKT4smiwsKholth13FPAJyv6382nphOCY2RPVPdM01OjXHt5z5mHwSvt8BkgR/xoGI9woIyyoLGIqdSUwHggVjwpt/1X09un54O3ZQ9VE0xPUoNe03e7lye+n+toFsRB8Gp8imCgGLLQslirNJagelxUtCxAA8/SF6nDhRNp11U7T9NNb10zdauUx7wX6OAUZEPgZNyJSKOcrvSzHKiQmHh8mFssLswCR9RXr6OGd2qnVW9PX0xfX5tzn5JruY/mWBIAPchnMIQkoxSvELPcqeSaTH7MWaAxXATD2puti4vja39Vp073T1daB3GXkBO7C+PMD5g7rGGAhvyehK8ksJCvLJgYgQBcFDfoB0PY47N3iVdsY1nrTpdOW1h7c5eNu7SH4UANMDmIY8iBzJ3srzCxPKxwndyDLF6ENnQJw98vsWuO021PWjdOP01nWvttn49rsgPetArEN2ReDICQnUyvMLHcrayfnIFUYPA5AAxH4YO3Z4xXckNaj03zTHtZf2+riR+zg9goCFQ1OFxEg1CYoK8osniu3J1Uh3RjXDuMDsvj17Vnkd9zP1rrTa9Pl1QHbbuK160D2ZwF4DMEWnh+BJvsqxSzCKwIowSFkGXEPhgRT+Yvu2uTc3BDX1NNc067Vptr04STrofXEANsLNBYqHy0mzCq+LOQrSigsIuoZChAoBfX5Iu9c5ULdVNfx00/TetVN2nzhlOoC9SAAPQumFbQe1iWbKrUsAyyRKJUibxqiEMoFl/q57+Hlqt2Z1w/URdNH1fbZBeEF6mT0fv+eChYVPB5+JWcqqSwhLNUo/CLyGjkRbAY5+1LwZuYU3uHXMNQ+0xfVoNmQ4Hfpx/Pa/v8JhRTDHSMlMSqcLDwsFylhI3QbzxEOB9z77PDt5n/eK9hU1DjT6tRN2Rzg6ugq8zf+YAn0E0gdxyT5KYssVCxXKcQj9BtlEq8Hf/yG8XXn7d522HnUNdO+1PzYqt9f6I7ylP3ACGETyxxpJL8peSxrLJUpJiRzHPkSUAgi/SHy/udc38TYodQ005XUrdg639Xn8vHx/B8IzRJNHAkkgylkLH8s0SmFJPEcjRPwCMX9vfKJ6MzfFNnL1DbTbtRf2MzeTOdX8U78fwc4Es4bpyNEKU0skCwKKuMkbR0fFJAJaP5Z8xTpP+Bm2ffUOdNJ1BTYX97E5r3wq/vdBqIRTRtDIwQpNCygLEIqPyXnHbEULwoL//bzoemz4LrZJtVA0ybUy9f03T7mJPAJ+zwGDBHLGt0iwSgYLK0sdyqYJWAeQRXOCq//lPQv6inhENpW1UjTBtSE14vdueWM72b6mgV0EEcadSJ8KPoruCyqKvAl1x7RFWwLUQAy9b/qoOFo2onVU9Po0z/XI9015fTuxPn3BNwPwhkMIjUo2ivALNoqRiZNH18WCgz1ANH1T+sZ4sHavtVg08zT/Na93LPkXu4j+VUEQw88GaEh7Ce3K8csCSuaJsEf7BanDJgBcPbh65PiHdv21XDTs9O81lncMuTI7YH4sgOpDrQYNCGhJ5Iryiw1K+wmNCB3F0MNOwIQ93PsD+N72y/WgdOc033W99uz4zPt4fcPAw4OKxjGIFMnayvMLF8rPCekIAIY3w3eArD3B+2N49rba9aV04fTQdaX2zXjn+xA92wCcg2hF1YgBCdCK8sshyuKJxMhixh6DoEDUfib7QzkPNyp1qzTddMH1jnbuOIM7KD2yQHWDBYX5B+zJhYryCysK9UngSETGRQPJATy+DHujOSf3OnWxNNk08/V3do94nvrAfYmATkMiRZwH2Am6SrCLNArHyjsIZoZrg/HBJT5x+4O5QTdK9ff01fTmdWC2sTh6upi9YIAnAv7FfseCia5Krss8StnKFYiHxpHEGkFNvpe75Hla91v1/3TS9Nl1SraTOFa6sP04P/+CmwVhB6zJYYqsSwPLKwoviKkGt4QCwbY+vbvFubU3bbXHNRC0zTV09nW4MzpJfQ8/18K3BQMHlolUiqkLCws8CgkIyYbdRGtBnr7j/Cc5j/e/tc+1DvTBdV/2WLgP+mI85n+wAlLFJId/yQbKpUsRiwxKYkjpxsLEk4HHfwp8SPnq95J2GLUNtPY1CzZ79+y6Ovy9v0gCbkTFh2hJOIphCxdLHAp6yMnHKAS7wfA/MTxq+cZ35XYidQ0063U3Nh93yfoT/JT/YAIJhOZHEIkpylxLHMsrSlMJKYcNROQCGP9X/I16Inf5Nix1DTThdSN2A7fnue08bD83weSEhsc4iNqKVsshizoKaskIx3IEzAJBv778sDo+t812dzUN9Nf1EHYoN4V5xrxDfw+B/wRmxt/IyspQyyXLCEqCCWeHVoU0Amp/pjzTelt4IfZCdU80zvU99c03o7mgPBq+50GZhEZGxoj6SgpLKUsVypjJRge6xRvCk3/NfTa6eLg3Nk51UPTGdSu18ndCObn78j6+wXPEJYatCKlKAwssiyLKrwlkB57FQ0L8P/T9GnqWOEz2mrVTNP602jXYd2E5U/vJvpZBTcQEhpMImAo7Su8LL0qEyYHHwoWqwuTAHH1+OrQ4YvantVY093TJNf63AHluO6E+bYEnw+NGeIhGCjMK8Ms7SpoJnwflxZJDDYBEPaJ60ri5trU1WbTwtPi1pXcf+Qi7uL4FAQFDwYZdiHOJ6kryCwbK7sm7x8kF+YM2QGw9hvsxeJC2wzWdtOp06PWMtz/44ztQfhxA2sOfhgIIYIngyvLLEYrDCdhIK8Xgg18AlD3ruxB46HbR9aJ05PTZdbR24Dj+Oyg984C0A30F5kgNCdbK8wsbytbJ9EgORgdDh8D8fdC7b/jAdyD1p7Tf9Mp1nHbA+Nk7AD3KwI0DWkXKCDkJjEryiyWK6gnPyHCGLgOwgOS+NftP+Rj3MLWtdNu0/DVFNuH4tLrYPaIAZcM3ha2H5ImBCvGLLsr8yesIUkZUg9lBDP5be7A5MfcA9fP01/TudW42g3iQevB9eQA+gtQFkEfPibWKsAs3Ss8KBci0BnrDwgF1fkD70LlLd1G1+vTUtOE1V/alOGw6iL1QQBdC8IVyx7oJaUqtyz9K4MogCJUGoMQqgV3+pvvxuWV3YvXCdRH01HVB9od4SHqhPSe/74KMxVUHpAlciqsLBssyCjnItgaGxFMBhn7M/BL5v7d0tcq1D/TIdWx2afgk+nm8/v+HwqiFNsdNiU8Kp8sNiwKKU0jWhuxEe0Gu/vN8NLmat4c2EzUOdPz1F7ZM+AG6UnzWP6ACREUYB3aJAUqjyxPLEspsCPbG0cSjwde/GfxWefX3mfYcdQ108fUDNnB33vorfK1/eAIfhPkHHwkyyl9LGYsiSkSJFoc3BIvCAH9AvLi50XftNiZ1DTTndS82FHf8OcR8hH9QAjrEmccHCSPKWgseyzFKXIk2BxvE9AIpP2d8m3ott8E2cLUNdN11G/Y4t5n53bxbvyfB1YS6Bu6I1EpUiyNLP8p0CRUHQIUcAlH/jrz+Ogo4FXZ7tQ401DUI9h03t/m3PDM+/4GwBFnG1cjESk5LJ0sNyosJc8dlBQPCuv+1/OF6Zzgqdkc1T7TLdTa1wneWeZD8Cn7XAYqEeUa8SLOKB4sqyxsKoclSB4kFa4Kjv909BPqEeH+2UzVRtMM1JLXn93T5arvh/q6BZMQYhqKIooo+CucLHYqrCWKHoYVMAswADb18eoE4v3aTdY61OXUQdgW3gTmjO8T+u8EdQ/8GOsgxiYvKvQqCSmQJNEdPBVZC8kAN/ZI7J3jvtwZ2PbVddaM2QffjOaj77f5JwRMDoUXPh/9JGcoSSmWJ2wjDh3mFHYLVwEs95XtLuV63uTZtNcJ2N3aAeAf58bvaPlqAy4NFxaXHTgjoCacJx4mPyJBHIQUhgvXARX42e635jHgrdty2aHZNtwE4b7n9e8l+boCGwyzFPcbdiHZJOwloCQLIWkbFhSJC0wC8/gS8Djo4uFz3THbPduV3RHiZ+gw8O/4FgITC1cTXhq5HxQjOiQdI88fiBqeE4ELswLF+UHxsemO4zff8Nzc3PreJuMb6Xfwxfh+ARcKBhLNGAAeUCGHIpUhjB6dGRkTbAsPA4v6ZfIi6zPl9+Cw3n/eZeBE5Nnpy/Co+PIAJQm9EEIXTByNH9IgCSBBHagYihJKC14DRft/84rs0+a04m/gJODX4Wrlouoq8Zf4cwA/CH8PvxWdGswdHB95Hu8bqhfwER0LoAPz+4706e1s6G7kLeLM4U3jmOZ165Txk/gAAGQHSw5EFPMYDhxlHeQclhqjFkoR4wrWA5X8kvU/7/7pJObr43bjyuTO51LsCvKb+Jr/lQYgDdESThdSGq0bTBs3GZMVmhCeCgAEK/2M9ovwiuvW56jlI+VL5gzpOe2M8q/4P//SBQAMZhGvFZgY9BmwGdIXeRTeD0wKHQS1/Xr3z/EO7YPpZOfR5tHnUuoq7hnz0Pjx/hoF6goDEBYU4hY8GBEYZhZYExkP7wkuBDP+XfgJ84zuLOse6YHoXOmf6yTvsfP8+LD+bwTfCakOghIuFYMWbxb1FC4SSQ6GCTIEpP40+Tn0AvDR7NfqMurr6vPsKPBV9DX5e/7PA94IWA31EH4TyxTKFH0T+xBuDREJKgQK/wD6X/Vw8XDujezk637sTe418QP1evlS/jsD6AcQDG8P0hEUEyMTARLBD4oMkQgWBGP/wfp89tbyCvBB7pftFe6v70vyvPXL+TX+swL9BtAK7w0pEF0RehF/EH8OnAsFCPUDr/92+473NfSf8fPvS++v7xfxafOA9ij6Jf43Ah0Gmgl2DIUOqA/OD/gONQ2jCm4HyAPw/yD8lviL9S3zovH/8E3xhfKR9E/3kfoi/scBSQVtCAQL5Qz0DSEObQ3kC6IJywaPAyMAvfyU+dn2tvRO87Py7vL588H1KPgF+yr+YwF/BEoHmglKC0EMcwzdC4wKlwgeBkoDSgBP/Yf6Hvg59vb0Z/SS9HP1+fYL+YX7P/4MAcEDMQY3CLMJkQrDCkkKLQmCB2UF+QJmANX9b/ta+bb3m/Ya9jj28vY5+Pj5Efxh/sEADgMhBdwGIgjiCBIJsQjHB2UGogScAnQAT/5N/I36K/k8+Mz34fd2+IH57/qo/I7+ggBmAhwEiAWWBjcHYQcWB1sGPgXUAzMCdwC9/h/9t/ua+tn5fvmM+QD60frx+0r9yP5PAMsBIQM9BBAFjQWwBXcF6AQPBPsCvgFtAB//5/3Y/AL8cvsu+zj7jvso/Pv8+P0O/ykAOgEwAvsCkAPnA/4D1ANwA9cCGAI9AVcAdf+j/u/9Y/0G/dz85vwh/Yf9EP6x/mD/DwC2AEkBwAEVAkQCTAIvAvEBlwEqAbEANQC//1T//f68/pb+if6V/rj+7P4t/3X/vv8CAD4AbgCPAKEApQCbAIgAbQBPADIAGQAGAPz/+v8AAAkAIwBGAGcAewB4AFkAHADJ/2r/Ef/P/rP+yv4V/5H/LQDXAHQB6gEhAgwCpgH3ABQAHf8y/nn9Ev0S/X/9Uv5x/7YA9QH+AqcD0gNyA40CPwGy/x3+ufy++1T7kft0/OL9rf+WAVkDtARwBWwFoQQnAysB9P7P/Az77vmk+T/6sfvL/UUAyQL8BIkGNQfgBo8FagO7AN/9PPs1+Rb4Dvgn+T/7EP44AUkE0AZxCOkIIggwBlMD7v94/G75QfdE9qL2Vfgl+7T+gwIMBswIXAp+CiYJfQbdAsX+xfpv9z/1ifRt9dL3avu2/yAECAjhCj0M5gvgCW4GBgJE/dD4TfU98/DyefSo9w/8FAEHBjQKAQ0EDhMNRwr/BdAAcfui9hPzSfGK8dTz3PcX/cwCMAiADB0PpA/5DVIKLAU8/1T5SPTS8HLvYvCG83T4gf7VBJAK4Q4oEQ0RjQ77CfQDT/319s/xl+7I7YXvl/Nz+UkAKQccDUcREhM0EsYOPAlYAg77YfRD73LsV+z+7g/02fptAr8JxQ+kE8wUDBOcDhQIWgCC+KLxtexx6i3r1+7x9Kf85gSKDH0S6BVHFokTBg6ABgH+tPXH7jTqpOhY6hjvQfbY/qoHfg83FQMYdxehEwMNgwRQ+7Ly3uvO5xrn4enH7wD4ZwGwCo0S4RfmGU8YTRONCx8CU/iG7/foleXf5dPp6vAs+k8E7A2pFWsahBvEGIYSpQlb/xP1QOwh5pbjAeU26oLywfyFB1ERwRjHHM0cyhhIEU0HPPyd8fDobuPi4YzkEeuR9Lr/AAvPFMUb5B61HVsYkA+IBMz4/u2k5ezgh+CI5GnsFPcPA7EOVxilHrIgMB5vF10NWwEX9UbqbuKu3pHfAOU+7gj6uAaMEtkbTyEkIjMeAxaxCtD9KvGE5l/fwdwN3/nlk/Bm/agKgBZDH7QjLCO3HRIUkQfv+RLtyeKI3DXbBd9452XzJgHSDn0ahSLDJb0jtByeEQIExPXh6Cjf+tkX2oLff+mw9j8FJxNzHowlbSfNIycbqA4NAF3xpuSx28XXddmK4BDsbvqlCZcXTyJHKKUoVCMLGTULvfvJ7HPgd9j51VjZJOIn75b+Sg4SHP4lpipcKUkiYRZKBxz3Gehb3IvVo9TL2VDkwfIdAx0ThCBuKZgsiSmoICAT7QJT8qDj4tia04PUftuQ5wv3xQdrF8wjLyuLLLEnTR3SDkf++e0v4NXWOdPd1WHeluul+04MQBtlJi8szytTJaEZXAqm+dLpFt051VTTqteh4dXvSQC0EMoelSi2LJsqjSKuFckFFfXn5V3aE9Tq0+fZNeVA9O4E7BT/IVQqwizwKGkfgBEmAaPwReIM2GbT+dSN3BPpzPiFCesY1ySfK1Is1SbuGyENgPxc7PTeKdY104DWld8w7Wv9AQ6kHEgncixnK08kJhieCOT3Suj/27rUf9N52PbigfERAlcSDyBOKcksBSpkIRsUBARe83rkbdnC00PU39qo5vr1sgZ7FiEj4SqlLC8oHh7ZD1//+u724EbXRdOB1avdn+qP+kALYBrTJf4rBizqJYQaawu7+sbqx92P1ULTNNfW4NLuM/+vD/0dHCiiLO4qPSOhFt0GJfbM5vfaTdS801fZV+Qz89gD9BNHIfYpyixfKS4ggBI9AqvxGOON2ITTr9Tl2yXouPdzCAEYNSRcK3csXifGHCsOl/1Y7bTfkNY10xrW19407FT89wzLG78mSyypK/AkDxmwCff4Oemo3AbVYtP41yTievD5AFcRSh/eKMAsYyocIhMVGQVr9Fnl/tny0wrURdrD5ev0nQWIFXEijSq5LKgo6h7dEHUA/u/C4b3XV9Ms1frcq+l6+TEKfRk6JcYrNyx8JmMbeAzR+77rft7s1TjTw9YQ4NHtG/6pDisdnCeGLDor5iOQF/EHNve155fbjtSU083YfuMp8sEC+BKJIJEpzCzHKe4gfRNUA7Xy8OMV2ajTa9RC2zrnpvZgBxMXjiMTK5Ys4CeaHTMPrv5Y7njg/tY907rVHd476z776wvuGjAmHizkK4sl9RnACgz6K+pX3VjVTdN+11bhde/j/1QQfx5pKK8suirPIggWLwZ59Tvmldoo1NjTsdnj5N3zhwSRFLwhMirGLBopsh/eEYwBBPGS4jvYcNPd1E/cu+hm+CAJlRicJIcrYCwIJz4cgw3n/LjsOt9P1jTTWdZO39PsBP2fDVUcFydkLIAriyR8GAMJSfii6D3c1dRz00nYqOIg8aoB+RHHHyUpxywoKqkhdxRqBMHzy+Si2dPTLtSl2lPmlvVMBiIW4SLDKq0sXChqHjkQxv9a70DhcddL02HVad1F6in63AoNGpsl6isZLCEm1xrOCyH7IesK3rDVPtMK14zgc+7M/k8PsB3tJ5gsCyt8I/oWQweK9iLnMttk1KzTI9kH5NHycQOXEwIh0SnLLIYpdSDdEqQCDfJn47/YkNOV1KjbzudT9w4IqRf4I0IrgyyOJxUdjQ7+/bbt+9+41jfT9tWS3tjr7vuUDHobiyY7LMArKiVkGRQKXfmS6ejcI9VZ08rX1+Ea8JMA+BAAH7QouyyEKl4ibhWABc70rOU12gXU99MO2nDlh/Q3BS0VLyJsKr4s0ig0HzwR3ABe8A7i69dg0w7VutxS6RT5zAkoGQAlsCtHLLAmtBvbDDf8GuzD3g/WNtOc1sjfc+21/UcO3RxsJ3osVSskJOgXVgic9wzo1Nun1IfTm9gu48fxWgKaEkIgainLLOspMyHZE7oDF/NA5EjZt9NU1Ajb5eZC9voGuhZPI/YqnywOKOcdlA8V/7buweAo10HTmNXa3eDq2PqHC5wa+iUMLPgrwyVJGiQLcvqF6pjdeNVG01LXC+EW73z/9A8zHjwoqCzZKg8jYRaVBt71kObO2j3Ux9N82ZHkevMhBDUUeCEPKsksQin7Hz0S8wFl8eDia9h708LUEdxj6AH4uwg/GGAkbytuLDonjhzlDU79Fe2B33XWNNM01gjfduye/D0NBRzkJlYsmCvGJNIYaAmv+Proe9zx1GnTGdhb4r/wQwGbEX4f/CjDLEsq7CHSFNAEJPQe5djZ5dMZ1G3a/+Uy9eYFyBWgIqQqtCyIKLUemRAsALnvjOGd11LTQtUo3evpw/l4CrkZYyXVKyssViYpGzEMh/t8607e09U60+DWQ+AU7mX+7g5jHb4njiwnK7ojUheoB+72d+dt23zUntPx2Lbjb/IKAzoTvCCsKcwsrCm8IDoTCgNv8rbj8die03zUbdt35+72qAdSF7ojJyuOLL4nYx3uDmX+FO5D4ODWOtPT1U7efOuH+zEMKRtWJiss1StjJbkZeArD+evpKN1C1VLTndeM4bnvLACZELUeiCi0LKQqoCLIFeYFMvX/5W3aGdTl09jZHuUk9NAE0hTsIUsqwyz8KH4fmxFDAb/wW+IZ2GnT8dR73Pror/hoCdIYxiSYK1Ys5CYFHD0Nnvx27AjfNNY003XWgd8V7U795Q2OHDonbixvK2AkPxi7CAH4Y+gR3MLUe9Nr2ODiZfHzAT0S+x9CKcksDyp4ITUUIQR685HkfNnH0z3UztqQ5t71lQZhFg8j2SqoLDwoMx70D3z/Fu8L4VLXRtN41Zjdhepy+iQLSRrDJfgrDCz6JZwahwvY+uDq2t2Y1UHTKNfB4LbuFf+UD+cdDiifLPYqTyO6FvoGQvbl5gjbVNS300jZQOQX87oD2RMzIespyyxqKUIgmhJaAsfxLuOb2IfTp9TU2wzonPdWCOgXJCRVK3osbCfdHEcOtf1z7cjfnNY20w/Ww94a7Df82wy0G7AmRyywKwAlKBnMCRT5Uum63A7VYNPr1w7iXvDcADwRNB/SKL4sbCovIi0VNwWH9HDlDtr30wXUNdqs5c70gAVuFV4ihCq7LLQoAB/4EJMAGvDX4crXWdMj1ejckuld+RQKZBkqJcArOyyLJnoblAzu+9jrkt721TfTuNb737bt/v2NDhUdjieDLEIr+COpFw4IU/fO56jbldSQ07/YZ+MN8qQC3RJ1IIYpyyzRKQIhlxNxA9HyB+Qj2azTZNQy2yLnivZDB/oWfCMLK5gs7SewHU8PzP5z7ozgCtc+07DVCt4h6yH7zgvXGiEmGSzqK5slDRrcCin6Repp3WHVS9Nx10DhWu/G/zkQah5cKK0swyrhIiIWTAaW9VPmpdou1NPTotnL5MHzagR3FKkhKCrHLCUpxx/5EaoBIPGo4knYc9PV1D3couhJ+AMJfBiLJIArZCwXJ1Ucnw0E/dPsTt9Z1jTTT9Y637js5/yDDT4cCCdgLIcrnCSVGCAJZvi76E/c3dRw0zvYkuIE8YwB3hGyHxopxiwyKrwhkRSHBN3z4+Sx2djTKNSV2jvmefUvBggWzyK6Kq8saSh/HlQQ4/9171bhftdN01jVV90r6gz6wAr1GYsl5CseLDAm7hrrCz77O+sd3rrVPdP+1njgWO6u/jMPmh3gJ5YsEyuOIxMXYAem9jrnQttr1KjTFdnw47XyVAN9E+4gxynMLJEpiSD4EsECKfJ+483YlNOO1Jfbtec29/EHkBfmIzorhiycJysdqQ4b/tHtEODD1jjT7NV+3r7r0ft4DGMbfCY3LMYrOiV9GTEKevmr6frcLNVX073XwuH+73UA3RDqHqgouSyNKnEiiBWdBev0w+VF2grU8tP+2Vnla/QZBRMVHCJjKsAs3ihKH1cR+QB68CTi+Ndi0wbVqNw56ff4sAkPGfAkqStLLL8myxv3DFT8NOzX3hrWNdOQ1rTfWO2X/SsOxhxeJ3csXCs1JAEYcwi49yXo5duv1ITTjdgY46vxPQKAEi4gXynKLPYpRyH0E9gDM/NX5FfZvNNN1PfazOYl9t0GoRY9I+4qoiwcKP0drw8z/9Lu1uA010LTj9XH3cbqu/prC4Qa6iUGLP4r0yVgGkALj/qf6qvdgdVF00bX9uD67l//2Q8eHi8opSzhKiEjexayBvr1qObf2kPUwtNt2XrkXvMEBBsUZCEFKsksTikPIFcSEQKB8fbiedh/07rU/9tK6OT3nggmGE8kZytyLEgnpBwBDmv9MO2V34DWNdMp1vTeXOyA/CEN7hvVJlIsnyvXJOsYhQnM+BPpjdz51GbTDNhF4qPwJgGAEWkf8CjCLFQq/yHsFO4EQPQ15efZ6tMT1F3a5+UV9ckFrhWNIpsqtiyVKMoetBBJANXvoeGq11TTOdUW3dLppvlcCqEZUyXPKy8sZSZAG04MpfuW62He3dU509XWL+D57Uf+0g5NHbEniywvK8wjaxfFBwv3kOd+24PUmtPi2KDjU/LtAiATqCChKcwstynQIFUTKAOL8s3j/9ii03XUXNtf59L2iwc5F6kjHyuRLMwneR0KD4L+L+5Y4OzWO9PJ1TreYutq+xUMERtHJiYs2ytzJdEZlQrg+QXqO91K1VDTkdd24Z7vDgB9EJ8efCiyLK0qsyLiFQMGT/UX5n3aH9Tf08jZBuUH9LMEuBTZIUEqxCwIKZMfthFgAdvwceIn2GzT6dRp3OHokvhLCboYtSSSK1os8iYcHFkNu/yR7BzfP9Y002rWbd/77DD9yQ13HCwnaix2K3EkVxjYCB74fOgi3MrUeNNd2MriSvHWASIS5h83KcgsGSqMIVAUPgSW86jki9nM0zfUvtp35sH1dwZIFv0i0CqqLEkoSR4QEJr/Me8g4V/XSNNu1YXdbOpV+gcLMRqzJfMrESwJJrMapAv1+vrq7d2i1UDTHNes4Jvu+P54D9EdASicLP4qYSPUFhcHX/b95hnbWtSz0znZKeT78p0DvxMfIeEpyyx1KVcgtRJ4AuPxReOp2IvToNTC2/Pnf/c5CM8XEiRNK34seifzHGMO0v2O7dzfp9Y20wXWr97/6xr8vwydG6ImQiy2KxElQBnpCTH5bOnM3BbVXdPe1/jhQ/C/ACERHx/GKL0sdipCIkcVVAWj9IjlHtr80//TJdqU5bL0YgVUFUwieiq8LMAoFR8TEbAANfDt4dfXXNMb1dbceOlA+fcJTBkZJbkrQCyaJpIbsAwL/PLrpd4A1jbTrdbn35vt4f1xDv4cgCeALEorCiTCFysIcPfn57rbnNSN07DYUOPx8YYCwxJhIHspyyzcKRYhshOOA+3yHuQy2bHTXdQh2wnnbfYmB+AWaiMDK5ss+yfGHWoP6f6O7qHgFtc/06fV990H6wT7sgu/GhEmFCzwK6slJRr5Ckb6X+p83WrVSdNl1yvhPu+o/x0QVB5PKKsszCr0IjsWaQaz9Wvmtto01M7Tk9m05KTzTQRdFJUhHirHLDEp3B8UEscBPPG+4lbYd9PN1Cvciegs+OYIZBh6JHkraCwlJ2wcuw0i/e3sYt9k1jTTRNYm357syvxnDScc+iZcLI4rrSStGD0Jg/jU6GDc5dRt0y7YfOLo8G8BwxGdHw4pxSw8Ks8hqxSlBPnz+uTB2d3TItSF2iPmXfUSBu4VvCKxKrEsdiiVHnAQAACQ72vhitdP00/VRN0S6u75owrdGXsl3isjLD8mBhsHDFv7Vesx3sTVO9Py1mPgPe6R/hgPhB3SJ5MsGyugIywXfQfD9lPnU9ty1KTTBtnZ45nyNgNiE9ogvCnMLJwpniATE94CRfKU49vYmNOH1IbbnOca99QHdxfVIzMriSyqJ0IdxA45/uztJODP1jnT4tVr3qPrs/tcDEwbbSYyLMwrSiWVGU0Kl/nF6QzdNNVV07HXrOHj71gAwhDVHpsotyyWKoQioRW6BQf12+VV2hDU7NPv2UHlTvT8BPkUCSJZKsEs6ihfH3IRFwGW8DriBdhl0/3Ultwg6dr4kwn3GN8koytPLM4m4hsTDXL8Tuzq3iTWNdOF1p/fPe16/Q8OsBxQJ3MsZCtGJBkYkAjV9z7o9tu21IDTgNgC44/xHwJlEhkgUynKLAAqWyEOFPUDUPNu5GbZwNNH1OfatOYJ9sAGiBYqI+UqpCwpKBMeyw9Q/+3u6+BA10TThtW03azqnvpOC2wa2yUBLAQs4iV4Gl0LrPq56r7ditVD0zrX4eDf7kH/vQ8IHiIooyzqKjQjlBbPBhf2wObv2krUvtNe2WPkQfPmAwEUUSH7KcosWSkkIHISLgKd8Q3jhtiC07PU7tsx6Mf3gQgNGD4kYCt1LFcnuxwdDoj9S+2p34vWNdMf1uHeQexj/AUN1xvHJk0spivnJAMZoQnp+Czpn9wC1WTT/9cv4ojwCAFlEVQf5CjALF4qEyIGFQsFXPRN5ffZ79MN1E3az+X59KsFlBV7IpIquCyhKOAezxBmAPDvt+G311bTMNUD3bjpifk/CokZQiXJKzQsdSZYG2oMwvuw63Te59U408nWGuDe7Sr+tg42HaMniCw2K94jhBfiByj3qeeP24rUltPU2InjN/LQAgUTkyCWKcwswSnkIG8TRQOn8uTjDtmm027US9tG57X2bgcfF5cjFyuULNknjx0lD6D+Su5t4PjWPNO/1SfeSOtN+/kL+ho4JiEs4SuDJekZsQr9+R7qTd1T1U7ThNdh4YPv8v9iEIoebyiwLLYqxSL7FSAGa/Uv5o3aJdTa07nZ7+Tr85YEnhTGITcqxSwUKagf0RF+Afbwh+I02G/T4dRX3MfodfguCaEYpCSLK14sASczHHUN2Pyr7DDfSdY001/WWN/g7BP9rQ1gHB4nZix9K4IkcBj1CDv4leg03NHUddNP2LPiLvG5AQcS0R8rKccsIyqfIWoUWwSy88Dkm9nR0zHUrdpf5qT1WgYuFuoixyqsLFYoXx4rELf/TO824WvXStNl1XPdUuo3+usKGRqjJe0rFiwZJssawAsS+xTrAd6s1T7TENeX4IDu2v5dD7sd9CeaLAcrcyPtFjQHe/YV5ynbYdSu0yvZEuTf8oADpBMMIdcpyyyAKWsg0BKVAv/xXOO42I7TmdSx29rnYvccCLYXASRGK4EshycKHX8O7/2p7fHfstY30/vVnN7l6/z7ogyGG5MmPiy9KyElWBkGCk75henf3B/VW9PR1+LhJ/ChAAYRCh+6KLssfypVImEVcQXA9KDlLdoC1PrTFtp85ZX0RQU6FTkicSq+LMwoKh8uEc0AUfAD4uTXXtMS1cPcX+kj+dsJNBkJJbMrRCypJqkbzQwo/Azsud4K1jbTodbS34Dtw/1VDugccyd8LFErGyTbF0gIjff/58vbpNSJ06LYOuPV8WkCqBJMIHApyyzmKSkhzBOsAwnzNeRB2bXTV9QQ2/HmUPYJB8cWWCP6Kp4sCCjcHYYPB/+p7rbgItdA053V5N3t6uf6lQunGgImDiz2K7slPRoVC2P6eOqP3XPVR9NY1xbhI++L/wIQPh5DKKks1CoGI1UWhgbP9YPmxto61MnThNmd5IjzLwRCFIIhFCrILD0p8B8vEuUBV/HV4mTYetPG1BrccOgP+MoISxhpJHIrbCwzJ4Ic1w0//Qjtd99v1jTTOdYS34PsrPxLDRAc6yZYLJUrviTGGFoJoPjt6HLc7dRq0yDYZuLN8FIBqBGIHwIpwyxGKuMhxRTCBBX0EuXQ2eLTHNR12gvmQPX0BdUVqSKoKrMsgiiqHosQHQCs74Hhl9dR00bVMd346dH5hwrFGWsl2CsoLE8mHRsjDHn7b+tE3s7VOtPm1k7gIu50/vwObh3FJ5AsIyuxI0UXmgfg9mvnZNt51KDT+NjC433yGQNIE8YgsSnMLKcpsiAtE/wCYfKr4+nYnNOA1HXbhOf99rcHXhfDIysrjSy3J1gd4A5W/gfuOeDb1jnT4NVr3p3rnPsqDPsa/SWtK0Ir0SRFGTwK0/lS6uPdPtZw1LXYcOJC8DgAHBC0HR4nDSv7KDQh1BSXBaD1J+cv3D7WI9bc25rm2fSYBKgT7x+4J/MpVSZiHV8QHwHF8XLkANu+1j/YR9/Z6lP5rwjIFqoh0SdoKF4jahn1C+L8Su424lPatde32ufiHu+k/XEMdxnlIm4ndiYkIFwVpQfq+Djrd+Aj2hvZf92t5lrzvgHYD7AboiOXJikktBxHEXwDQvWS6DLfbNrm2orgi+qA95cF2hJyHeYjVCWOIR8ZOA2G//HxXuZo3ibbCt3K43HugfsjCXQVvB60I64jsB5xFT4Jz/sA753kE95J3HvfMOdS8lL/XAyhF5IfFSOyIZ8buRFmBV/4dOxO4zDezN0s4q/qIfbnAjkPYBn0Hw8iaR9nGAUOuwFA9VHqceK43qTfEeU47tD5Nwa1Ea8a6R+sIOIcFhVjCkn+efKY6APiot/G4RzowPFU/TsJzRORG3cf9x4oGrkR3QYY+w/wSuf/4efgJeRA6zf1ogDrC34VCBykHvkcSBdfDoADMfgF7mXmX+J94rbmcO6T+LIDQQ7IFhkceh3AGk8UEgtWAJv1Xuzo5RzjWORs6Z/xyPt7BjoQrBfJGwMcVhhLEeAHaf1a8xvrzuUt5G7mO+zB9M3+9gjVESwYHxtHGsgVRw7TBL/6c/E66hHmiuWy6BTvyfeXASALDxNOGCMaUxgjE1AL9AFg+OjvuOmr5ijnGevu8a/6IATyDOsTFRjfGDIWchBwCE7/UPa47pLpk+f86JftvPRn/WIGbQ5rFIkXXBfwE8INswXm/JP05O3D6cHo/Oog8HL36v9XCI8PkxSyFqUVmBEdCyEDw/or82jtROor6hztqPIH+i8C/AlaEGcUlxXFEzUPjwjEAOr4GfJC7Q7rx+tQ7yX1cvwyBFALzxDuE0MUxhHUDCIGov5e91vxa+0X7IvtjfGL96v+7QVRDPIQMBO/ErQPfwrdA8D8Ifbv8N7tWO1r78nz0fmpAF4HAA3JEDUSFhGaDUAIygEj+zT10fCT7sbuXfH49e/7agKDCGENWRAFEVMPggsgBvD/zvmV9P3wg+9W8FXzEfjd/ecDWwl2DakPqw9/DXgJKQRS/sP4QvRt8aTwAPJK9Qr6k/8eBecJRQ3DDjAOpguEB2EC9fwC+Df0GPLt8bfzMffc+w0BDgYqCtMMrQ2fDNMJsAXOAN37ivdw9PnyVPNy9QD5fv1JArYGKAooDHMMAgsOCAQEeP8K+1n35vQF9ND0Jvew+uz+QQMXB+UJTAsdC2MJYgaHAl/+ffpq95P1M/VV9sr4N/wfAPYDNQdoCUcKtQnNB9YEPgGH/TP6ufdu9nv22fdU+pD9FQFoBBIHtwghCUYISAZzAy4A8fws+kD4b/fS91T5vvu0/swBlwS0BtsH5gfZBt0EPgJc/5z8Yfr4+I74Lfm8+v78oP9CAocEIgbbBp4GdwWVAz4ByP6I/ND62PnA+YX6CPwP/k8AdwI8BGEFwQVTBSsEdwJ2AHL+sfxx+9n6/PrO+zD97P7AAG8CuwN6BJYEDwT8AokB6/9c/hT9Pfzy+zj8Af0t/o//9AArAgoDdgNkA9sC8wHPAJz/g/6q/S39GP1r/RX++v74/+kArwEwAlwCNALAARUBTwCL/+T+bv43/kP+jP4B/5H/IgCjAAIBNQE3AQ8BxgBqAAoAt/95/1j/VP9q/5H/wP/u/xAAJQAqACEAEQA="
st.markdown(f"""
<audio autoplay style="display:none;">
    <source src="data:audio/wav;base64,{_CHIME_B64}" type="audio/wav">
</audio>
""", unsafe_allow_html=True)


# ── MARKDOWN STRIPPER — for clean plain text downloads ───────────────────────
def strip_markdown(text):
    import re
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    text = re.sub(r'^---+$', '─' * 60, text, flags=re.MULTILINE)
    text = re.sub(r'^\|[-| :]+\|$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\|(.+)\|$', lambda m: '  '.join(
        c.strip() for c in m.group(1).split('|') if c.strip()
    ), text, flags=re.MULTILINE)
    text = re.sub(r'`{1,3}', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── IMPORTS (lazy to handle missing packages gracefully) ──────────────────
def import_modules():
    try:
        from treaty_reader import (get_available_treaties, get_all_treaty_names,
                                   detect_country_from_filename, TREATIES_FOLDER)
        from advisor import (generate_advisory, generate_notice_reply,
                             generate_rate_comparison, classify_form_145,
                             get_claude_client)
        return True, get_available_treaties, get_all_treaty_names, \
               detect_country_from_filename, TREATIES_FOLDER, \
               generate_advisory, generate_notice_reply, \
               generate_rate_comparison, classify_form_145, get_claude_client
    except ImportError as e:
        return False, str(e), None, None, None, None, None, None, None, None


result = import_modules()
MODULES_OK = result[0]


# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤖 DTAA ADVISOR</h1>
    <p>AI-Powered Double Tax Treaty Advisory Suite &nbsp;|&nbsp;
       Built under Income Tax Act, 2025 &nbsp;|&nbsp;
       Income Tax Rules, 2026</p>
    <span class="brand-tag">TAXAVK — BEESPOKE TAX ADVISORS</span>
</div>
""", unsafe_allow_html=True)

# ── WORLD CLOCK (self-contained component so the live-updating script runs) ─
_WORLD_CLOCK_HTML = """
<div style="font-family:'Inter', sans-serif;">
<div id="taxavk-world-clock" style="display:flex;flex-wrap:wrap;gap:0.6rem;">
    <div class="wc-card" data-tz="Asia/Kolkata" data-city="India (IST)"></div>
    <div class="wc-card" data-tz="America/New_York" data-city="USA (EST/EDT)"></div>
    <div class="wc-card" data-tz="Europe/London" data-city="UK (GMT/BST)"></div>
    <div class="wc-card" data-tz="Asia/Dubai" data-city="UAE (GST)"></div>
    <div class="wc-card" data-tz="Asia/Singapore" data-city="Singapore (SGT)"></div>
    <div class="wc-card" data-tz="Australia/Sydney" data-city="Australia (AEST/AEDT)"></div>
</div>
</div>
<style>
    body { margin: 0; background: transparent; }
    .wc-card { background: #161B22; border: 1px solid rgba(201,168,76,0.20); border-radius: 8px;
               padding: 0.55rem 0.9rem; min-width: 128px; text-align: center;
               box-shadow: 0 2px 12px rgba(0,0,0,0.4); }
    .wc-city { font-family: 'Inter', sans-serif; font-size: 0.68rem;
               letter-spacing: 0.8px; text-transform: uppercase; color: #8B949E; font-weight: 500; }
    .wc-time { font-family: 'Orbitron', sans-serif; font-size: 1.1rem;
               font-weight: 700; color: #C9A84C; margin-top: 2px;
               text-shadow: 0 0 12px rgba(201,168,76,0.25); }
    .wc-date { font-family: 'Inter', sans-serif; font-size: 0.62rem;
               color: #8B949E; margin-top: 1px; font-weight: 400; }
</style>
<script>
(function() {
    var cards = document.querySelectorAll("#taxavk-world-clock .wc-card");
    cards.forEach(function(card) {
        var city = card.getAttribute("data-city");
        card.innerHTML = '<div class="wc-city">' + city + '</div>' +
                          '<div class="wc-time">--:--:--</div>' +
                          '<div class="wc-date">--</div>';
    });
    function tick() {
        var now = new Date();
        cards.forEach(function(card) {
            var tz = card.getAttribute("data-tz");
            try {
                var timeStr = new Intl.DateTimeFormat("en-GB", {
                    timeZone: tz, hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false
                }).format(now);
                var dateStr = new Intl.DateTimeFormat("en-GB", {
                    timeZone: tz, day: "2-digit", month: "short", year: "numeric"
                }).format(now);
                card.querySelector(".wc-time").textContent = timeStr;
                card.querySelector(".wc-date").textContent = dateStr;
            } catch (e) { /* timezone lookup unsupported in this browser */ }
        });
    }
    tick();
    setInterval(tick, 1000);
})();
</script>
"""
components.html(_WORLD_CLOCK_HTML, height=110, scrolling=False)

# ── AMBIENT MUSIC PLAYER ──────────────────────────────────────────────────────
_MUSIC_PLAYER_HTML = """
<div id="taxavk-audio-bar" style="display:flex;align-items:center;gap:1rem;padding:0.5rem 1.2rem;background:#161B22;border:1px solid rgba(201,168,76,0.18);border-radius:8px;margin:4px 0 2px;font-family:'Orbitron',sans-serif;">
  <button id="taxavk-amb-btn" onclick="taxavkAmb()"
    style="background:linear-gradient(135deg,#C9A84C,#E8C97D);color:#0D1117;border:none;
           border-radius:5px;padding:4px 14px;font-family:'Orbitron',sans-serif;font-weight:800;
           font-size:0.62rem;letter-spacing:1.5px;cursor:pointer;transition:all 0.2s;white-space:nowrap;">
    ▶ AMBIENT
  </button>
  <span style="color:#8B949E;font-family:'Inter',sans-serif;font-size:0.72rem;letter-spacing:0.5px;">
    🎵 Executive Soundscape
  </span>
  <input type="range" id="taxavk-vol" min="0" max="100" value="25"
         oninput="taxavkVolume(this.value)"
         style="accent-color:#C9A84C;width:75px;cursor:pointer;">
  <span id="taxavk-vol-disp"
        style="color:#C9A84C;font-size:0.6rem;min-width:30px;font-family:'Orbitron',sans-serif;">25%</span>
  <span id="taxavk-amb-state"
        style="color:#8B949E;font-size:0.6rem;font-family:'Inter',sans-serif;letter-spacing:0.5px;">READY</span>
</div>
<script>
(function(){
  var actx=null, master=null, on=false, started=false;

  // C major chord — stacked sine oscillators for a warm executive drone
  var CHORD=[
    {hz:65.41,  amp:0.22},  // C2  bass
    {hz:98.00,  amp:0.10},  // G2
    {hz:130.81, amp:0.12},  // C3  pad
    {hz:164.81, amp:0.08},  // E3
    {hz:196.00, amp:0.07},  // G3
    {hz:246.94, amp:0.04},  // B3
    {hz:261.63, amp:0.05},  // C4
    {hz:329.63, amp:0.03},  // E4
    {hz:392.00, amp:0.025}, // G4
    {hz:523.25, amp:0.012}  // C5  shimmer
  ];

  function boot(){
    actx   = new (window.AudioContext || window.webkitAudioContext)();
    master = actx.createGain();
    master.gain.value = 0;

    // Delay-based reverb
    var dly=actx.createDelay(2.0); dly.delayTime.value=0.5;
    var fb=actx.createGain();  fb.gain.value=0.30;
    var wet=actx.createGain(); wet.gain.value=0.30;
    var dry=actx.createGain(); dry.gain.value=0.70;
    dly.connect(fb); fb.connect(dly); dly.connect(wet);
    wet.connect(master); dry.connect(master);
    master.connect(actx.destination);

    CHORD.forEach(function(n, i){
      var o=actx.createOscillator(), g=actx.createGain();
      var lfo=actx.createOscillator(), lg=actx.createGain();
      o.type='sine'; o.frequency.value=n.hz; g.gain.value=n.amp;
      // Gentle vibrato per voice
      lfo.type='sine'; lfo.frequency.value=0.07+i*0.009;
      lg.gain.value=n.hz*0.0015;
      lfo.connect(lg); lg.connect(o.frequency);
      o.connect(g); g.connect(dry); g.connect(dly);
      lfo.start(); o.start();
    });
    started=true;
  }

  window.taxavkAmb=function(){
    var btn=document.getElementById('taxavk-amb-btn');
    var st =document.getElementById('taxavk-amb-state');
    if(!on){
      if(!started) boot();
      else if(actx.state==='suspended') actx.resume();
      var v=document.getElementById('taxavk-vol').value/100*0.4;
      master.gain.cancelScheduledValues(actx.currentTime);
      master.gain.linearRampToValueAtTime(v, actx.currentTime+2.0);
      btn.textContent='⏸ PAUSE';
      btn.style.background='linear-gradient(135deg,#6E7681,#484f58)';
      btn.style.color='#E6EDF3';
      st.textContent='● PLAYING'; st.style.color='#C9A84C';
      on=true;
    } else {
      master.gain.cancelScheduledValues(actx.currentTime);
      master.gain.linearRampToValueAtTime(0, actx.currentTime+1.5);
      setTimeout(function(){ if(actx) actx.suspend(); }, 1600);
      btn.textContent='▶ AMBIENT';
      btn.style.background='linear-gradient(135deg,#C9A84C,#E8C97D)';
      btn.style.color='#0D1117';
      st.textContent='PAUSED'; st.style.color='#8B949E';
      on=false;
    }
  };

  window.taxavkVolume=function(v){
    document.getElementById('taxavk-vol-disp').textContent=v+'%';
    if(actx && on && master){
      master.gain.cancelScheduledValues(actx.currentTime);
      master.gain.linearRampToValueAtTime(v/100*0.4, actx.currentTime+0.15);
    }
  };
})();
</script>
"""
components.html(_MUSIC_PLAYER_HTML, height=62, scrolling=False)


# ITA 2025 banner
st.markdown("""
<div class="ita-box">
<b>ITA 2025 Active:</b> Form 145 (replaces 15CA) &nbsp;|&nbsp;
Form 146 (replaces 15CB) &nbsp;|&nbsp;
Form 41 mandatory (replaces Form 10F) &nbsp;|&nbsp;
Section 393 (replaces Section 195) &nbsp;|&nbsp;
Rule 220(3) exempt list — 33 categories
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 DTAA Advisor")
    st.markdown("**TAXAVK — Beespoke Tax Advisors**")
    st.markdown("---")

    # Load API key silently from Streamlit Secrets
    if "ANTHROPIC_API_KEY" in st.secrets:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
        st.success("✅ AI features enabled")
    else:
        os.environ.pop("ANTHROPIC_API_KEY", None)

    st.markdown("---")

    # Treaties status
    st.markdown("#### 📂 Treaty Library")
    treaties_path = Path(__file__).parent / "treaties"
    if treaties_path.exists():
        pdfs = list(treaties_path.glob("*.pdf"))
        st.success(f"✅ {len(pdfs)} treaty PDFs loaded")
        with st.expander("View loaded treaties"):
            for pdf in sorted(pdfs):
                if "afghanistan" not in pdf.name.lower():
                    st.caption(f"📄 {pdf.name[:50]}")
    else:
        st.error("❌ Treaties folder not found")
        st.caption("Expected: treaties/ folder in project root")
        st.info("Create treaties/ folder in your repo and add treaty PDFs")

    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.caption("AICA Level 2 Capstone Project")
    st.caption("May 2026")
    st.caption("25 Indian DTAAs covered")


# ── STATS ROW ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><h3>25</h3><p>Indian DTAAs</p></div>',
                unsafe_allow_html=True)
with col2:
    treaties_path = Path(__file__).parent / "treaties"
    count = len(list(treaties_path.glob("*.pdf"))) if treaties_path.exists() else 0
    st.markdown(f'<div class="metric-card"><h3>{count}</h3><p>PDFs Loaded</p></div>',
                unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h3>5</h3><p>Core Modules</p></div>',
                unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h3>&lt;10m</h3><p>Per Advisory</p></div>',
                unsafe_allow_html=True)

st.markdown("---")


# ── TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🔍 DTAA Rate Lookup",
    "📋 AI Advisory",
    "📄 Form 145 Classifier",
    "📨 Notice Reply Drafter",
    "📚 Treaty Search",
    "📝 Form 145 Draft",
    "🏛️ Form 146 Draft",
    "📋 Form 41 Template",
    "🌐 Residential Status"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — DTAA RATE LOOKUP
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🔍 DTAA Rate Comparator")
    st.caption("Compare DTAA rates vs domestic Section 393 rates. "
               "Green = DTAA beneficial. ⚠️ = Use domestic rate.")

    # Rate database
    rate_data = {
        "Country": ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
                    "Japan", "Canada", "Australia", "Netherlands", "France",
                    "Switzerland", "Hong Kong", "Malaysia", "China",
                    "New Zealand", "South Africa", "Sri Lanka", "Thailand", "Italy"],
        "Dividend DTAA%": [15, 15, 10, 15, "Nil", 10, 10, 15, 15, 10,
                            10, 10, 5, 10, 10, 15, 10, 15, 15, 15],
        "Interest DTAA%": [15, 15, 12.5, 15, "Nil", 10, 10, 15, 15, 10,
                            10, 10, 10, 10, 10, 10, 10, 10, 15, 15],
        "Royalty DTAA%": [15, 15, 10, 10, 15, 10, 10, 15, 10, 10,
                           10, 10, 10, 10, 10, 10, 10, 10, 15, 20],
        "FTS DTAA%": [15, 15, "N/A", 10, "N/A", 10, 10, 15, 10, 10,
                       10, 10, 10, 10, 10, "N/A", 10, 10, 15, 20],
        "Cap Gains DTAA%": ["Domestic", "Domestic", "Exempt", "Domestic",
                             "Domestic*", "Domestic", "Domestic", "Domestic",
                             "Domestic", "Domestic", "Domestic", "Domestic",
                             "Exempt", "Exempt", "Domestic", "Domestic",
                             "Domestic", "Domestic", "Domestic", "Domestic"],
        "MLI": ["No", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes",
                 "Yes", "Yes", "Yes", "No", "Yes", "Partial", "Yes",
                 "No", "No", "No", "Yes"],
        "GAAR Risk": ["LOW", "MEDIUM", "MEDIUM", "MEDIUM", "HIGH", "MEDIUM",
                       "LOW", "MEDIUM", "MEDIUM", "MEDIUM", "MEDIUM", "MEDIUM",
                       "LOW", "MEDIUM", "MEDIUM", "LOW", "LOW", "LOW",
                       "LOW", "MEDIUM"],
    }

    df = pd.DataFrame(rate_data)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        selected_country = st.selectbox(
            "Select Country",
            options=["All Countries"] + df["Country"].tolist()
        )
        income_filter = st.selectbox(
            "Income Type",
            ["All", "Dividend", "Interest", "Royalty", "FTS", "Capital Gains"]
        )

    with col_b:
        # Domestic rates reference
        st.markdown("""
        <div class="ita-box">
        <b>Domestic Rates (Section 393 ITA 2025):</b><br>
        Dividend: 20% + SC + Cess &nbsp;|&nbsp;
        Interest: 20% + SC + Cess &nbsp;|&nbsp;
        Royalty: 10% + SC + Cess &nbsp;|&nbsp;
        FTS: 10% + SC + Cess &nbsp;|&nbsp;
        Capital Gains: 12.5% (LTCG Sec 112A) / 20% (STCG)
        </div>
        """, unsafe_allow_html=True)

        if selected_country == "Italy":
            st.markdown("""
            <div class="warning-box">
            ⚠️ <b>Italy Royalty Trap:</b> DTAA rate is 20% vs domestic 10%.
            Always use domestic rate for India-Italy royalty payments.
            </div>
            """, unsafe_allow_html=True)

        if selected_country == "Mauritius" and income_filter in ["Capital Gains", "All"]:
            st.markdown("""
            <div class="warning-box">
            ⚠️ <b>Mauritius Capital Gains:</b> Post-2016 Protocol — shares acquired after 1 April 2017
            taxable at full domestic rate (12.5% LTCG). Grandfathering only for pre-April 2017 acquisitions.
            HIGH GAAR risk — substance in Mauritius must be demonstrated.
            </div>
            """, unsafe_allow_html=True)

    # Display table
    if selected_country != "All Countries":
        display_df = df[df["Country"] == selected_country]
    else:
        display_df = df

    # Filter columns based on income type
    if income_filter == "Dividend":
        display_df = display_df[["Country", "Dividend DTAA%", "MLI", "GAAR Risk"]]
    elif income_filter == "Interest":
        display_df = display_df[["Country", "Interest DTAA%", "MLI", "GAAR Risk"]]
    elif income_filter == "Royalty":
        display_df = display_df[["Country", "Royalty DTAA%", "MLI", "GAAR Risk"]]
    elif income_filter == "FTS":
        display_df = display_df[["Country", "FTS DTAA%", "MLI", "GAAR Risk"]]
    elif income_filter == "Capital Gains":
        display_df = display_df[["Country", "Cap Gains DTAA%", "MLI", "GAAR Risk"]]

    # Color code GAAR risk
    def color_gaar(val):
        colors = {"HIGH": "background-color: #FCE4D6; color: #9C0006",
                  "MEDIUM": "background-color: #FFF2CC; color: #7D6608",
                  "LOW": "background-color: #E2EFDA; color: #375623"}
        return colors.get(val, "")

    if "GAAR Risk" in display_df.columns:
        styled_df = display_df.style.map(color_gaar, subset=["GAAR Risk"])
    else:
        styled_df = display_df.style
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    if selected_country != "All Countries":
        row = df[df["Country"] == selected_country].iloc[0]
        st.markdown("#### Key Notes")
        c1, c2, c3 = st.columns(3)
        with c1:
            risk = row["GAAR Risk"]
            icon = "🔴" if risk == "HIGH" else "🟡" if risk == "MEDIUM" else "🟢"
            st.metric("GAAR Risk", f"{icon} {risk}")
        with c2:
            st.metric("MLI Applies", "✅ Yes" if row["MLI"] == "Yes" else "❌ No")
        with c3:
            st.metric("Form 41", "✅ Mandatory")

        # AI Rate Analysis button
        if st.button(f"🤖 Get AI Rate Analysis for {selected_country}", type="primary"):
            with st.spinner(f"Analysing India-{selected_country} DTAA rates..."):
                try:
                    from advisor import generate_rate_comparison
                    result = generate_rate_comparison(selected_country)
                    st.markdown("#### AI Rate Analysis")
                    st.markdown(
                        f'<div class="output-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI ADVISORY
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📋 AI-Powered DTAA Advisory")
    st.caption("Describe your cross-border transaction. "
               "The AI reads the actual treaty PDF and generates a structured advisory.")

    col1, col2 = st.columns(2)
    with col1:
        adv_country = st.selectbox(
            "Country of Payee/Recipient",
            ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
             "Japan", "Canada", "Australia", "Netherlands", "France",
             "Switzerland", "Hong Kong", "Malaysia", "China",
             "New Zealand", "South Africa", "Sri Lanka", "Thailand", "Italy"],
            key="adv_country"
        )
        adv_income = st.selectbox(
            "Nature of Income",
            ["Royalty / Software Licence", "Fees for Technical Services (FTS)",
             "Dividend", "Interest", "Capital Gains", "Salary / Employment Income",
             "Business Profits / PE income", "Other Income"],
            key="adv_income"
        )

    with col2:
        adv_amount = st.number_input(
            "Transaction Amount (Rs. Lakhs)",
            min_value=0.0, value=25.0, step=1.0
        )
        adv_trc = st.selectbox(
            "TRC Available?",
            ["Yes — TRC obtained", "No — TRC not yet obtained",
             "In process of obtaining"]
        )

    adv_details = st.text_area(
        "Transaction Details",
        placeholder="Describe the transaction: e.g. Indian company paying annual software licence "
                    "fee of Rs. 25 lakhs to a US-based company. Services involve use of proprietary "
                    "software under EULA. No copyright rights transferred.",
        height=100
    )

    use_treaty_pdf = st.checkbox(
        "📄 Use actual treaty PDF for analysis (recommended)",
        value=True
    )

    # Demo scenarios

    if st.button("🤖 Generate DTAA Advisory", type="primary", key="gen_advisory"):
        if not adv_details.strip():
            st.warning("Please describe the transaction details.")

        else:
            income_map = {
                "Royalty / Software Licence": "royalty",
                "Fees for Technical Services (FTS)": "fts",
                "Dividend": "dividend",
                "Interest": "interest",
                "Capital Gains": "capital gains",
                "Salary / Employment Income": "salary",
                "Business Profits / PE income": "business profits",
                "Other Income": "other"
            }
            income_type = income_map.get(adv_income, adv_income.lower())
            full_details = (f"{adv_details}\n\nAmount: Rs. {adv_amount} lakhs. "
                           f"TRC status: {adv_trc}.")

            with st.spinner("Reading treaty PDF and generating advisory... (20-30 seconds)"):
                try:
                    from advisor import generate_advisory
                    result = generate_advisory(
                        adv_country, income_type,
                        full_details, use_treaty_pdf
                    )
                    st.markdown("#### Advisory Output")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Advisory as Text",
                        data=strip_markdown(result),
                        file_name=f"DTAA_Advisory_{adv_country}_{income_type}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating advisory: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — FORM 145 CLASSIFIER
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 📄 Form 145 / Form 146 Classifier")
    st.markdown("""
    <div class="ita-box">
    <b>ITA 2025 Update (w.e.f. 1 April 2026):</b>
    Form 15CA → <b>Form 145</b> &nbsp;|&nbsp;
    Form 15CB → <b>Form 146</b> &nbsp;|&nbsp;
    Rule 37BB → <b>Rule 220(3)</b> (33 exempt categories) &nbsp;|&nbsp;
    Form 10F → <b>Form 41</b> (mandatory)
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        f_payment = st.selectbox(
            "Nature of Payment",
            ["Royalty / Software Licence", "Fees for Technical Services",
             "Dividend to NRI", "Interest to NR Lender",
             "Capital Gains (NR seller)", "Salary to NR Employee",
             "Import of Goods", "Professional Services",
             "Rent of Foreign Property", "Partnership Profit",
             "RBI Exempt List Payment"]
        )
    with col2:
        f_amount = st.number_input("Amount (Rs. Lakhs)", min_value=0.0, value=10.0)
    with col3:
        f_taxable = st.selectbox(
            "Taxable in India?",
            ["Yes — chargeable to tax", "No — not chargeable", "Exempt under Rule 220(3)"]
        )

    f_dtaa = st.selectbox(
        "DTAA Benefit Claimed?",
        ["Yes — DTAA rate applied", "No — domestic rate applied",
         "Nil TDS — Article 7 (Business Profits, no PE)"]
    )

    # Instant classification logic
    st.markdown("#### Instant Classification")

    if f_payment == "Import of Goods" or "Exempt" in f_taxable:
        part = "PART D"
        part_color = "#DDEBF7"
        part_text_color = "#185FA5"
        form146 = "❌ Not Required"
        form41 = "❌ Not Required"
        note = "RBI exempt list under Rule 220(3) — No Form 145 required at all."
    elif "not chargeable" in f_taxable and f_amount <= 5:
        part = "PART A"
        part_color = "#E2EFDA"
        part_text_color = "#375623"
        form146 = "❌ Not Required"
        form41 = "✅ Required if DTAA claimed"
        note = "Non-taxable, ≤ Rs. 5 lakh. Remitter files on portal. No CA required."
    elif "not chargeable" in f_taxable and f_amount > 5:
        part = "PART B"
        part_color = "#FFF2CC"
        part_text_color = "#7D6608"
        form146 = "✅ REQUIRED"
        form41 = "✅ Mandatory"
        note = "Non-taxable but > Rs. 5 lakh. AO certificate OR Form 146 needed."
    else:
        part = "PART C"
        part_color = "#FCE4D6"
        part_text_color = "#9C0006"
        form146 = "✅ REQUIRED — Upload BEFORE Form 145 Part C"
        form41 = "✅ MANDATORY under Rule 75 / Section 159(8) ITA 2025"
        note = "Chargeable remittance. Form 146 (CA Certificate) mandatory."

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.markdown(
            f'<div style="background:{part_color};color:{part_text_color};'
            f'padding:1rem;border-radius:8px;text-align:center;">'
            f'<b style="font-size:1.4rem">{part}</b><br>'
            f'<small>Form 145</small></div>',
            unsafe_allow_html=True
        )
    with col_r2:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>Form 146</b><br>{form146}</div>',
            unsafe_allow_html=True
        )
    with col_r3:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>Form 41 (ITA 2025)</b><br>{form41}</div>',
            unsafe_allow_html=True
        )
    with col_r4:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>TRC Required</b><br>{"✅ Yes" if "Not Required" not in form41 else "❌ No"}</div>',
            unsafe_allow_html=True
        )

    st.info(f"📌 {note}")

    if st.button("🤖 Get Detailed AI Classification", key="classify_btn"):
        with st.spinner("Generating detailed classification..."):
                try:
                    from advisor import classify_form_145
                    result = classify_form_145(f_payment, f_amount, f_taxable, f_dtaa)
                    st.markdown(
                        f'<div class="output-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — NOTICE REPLY DRAFTER
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📨 IT Department Notice Reply Drafter")
    st.caption("Generate submission-ready formal replies citing treaty articles, "
               "Supreme Court judgments, and CBDT circulars.")

    col1, col2 = st.columns(2)
    with col1:
        n_country = st.selectbox(
            "Country of Foreign Entity",
            ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
             "Japan", "Canada", "Australia", "Netherlands", "France",
             "Switzerland", "Hong Kong", "Malaysia", "China"],
            key="n_country"
        )
        n_type = st.selectbox(
            "Notice Type",
            ["FTS / Royalty characterisation dispute",
             "PE allegation — Business Profits",
             "GAAR / Treaty Shopping challenge",
             "Short deduction / Non-deduction of TDS",
             "MFN clause dispute",
             "Beneficial ownership challenge",
             "Transfer Pricing adjustment"]
        )
    with col2:
        n_article = st.text_input(
            "Treaty Article in dispute",
            placeholder="e.g. Article 12 (FTS) vs Article 7 (Business Profits)"
        )
        n_section = st.text_input(
            "ITA 2025 Section",
            placeholder="e.g. Section 393"
        )

    n_facts = st.text_area(
        "Facts of the Case",
        placeholder="Describe: what payment was made, to whom, what TDS was deducted, "
                    "what is the department's objection, what documents were obtained...",
        height=120
    )

    if st.button("📝 Draft Notice Reply", type="primary", key="draft_notice"):
        if not n_facts.strip():
            st.warning("Please describe the facts of the case.")

        else:
            with st.spinner("Drafting formal reply (30-40 seconds)..."):
                try:
                    from advisor import generate_notice_reply
                    result = generate_notice_reply(n_type, n_country, n_facts, n_article)
                    st.markdown("#### Draft Notice Reply")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Reply as Text",
                        data=strip_markdown(result),
                        file_name=f"Notice_Reply_{n_country}_{n_type[:20]}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — TREATY SEARCH
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📚 Treaty Text Search")
    st.caption("Search and view actual CBDT treaty text from the treaty library.")

    treaties_path = Path(__file__).parent / "treaties"

    if not treaties_path.exists():
        st.error("❌ Treaties folder not found")
        st.info("Add a 'treaties/' folder to your GitHub repository and commit your treaty PDFs into it.")
    else:
        pdfs = sorted([p for p in treaties_path.glob("*.pdf")
                       if "afghanistan" not in p.name.lower()])

        if not pdfs:
            st.warning("No PDF files found in the treaties/ folder in your repository.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                selected_pdf = st.selectbox(
                    "Select Treaty PDF",
                    options=[p.name for p in pdfs]
                )
            with col2:
                search_topic = st.text_input(
                    "Search Topic",
                    placeholder="e.g. royalties, dividends, permanent establishment, FTS"
                )

            if st.button("🔍 Search Treaty", key="search_treaty"):
                selected_path = treaties_path / selected_pdf
                with st.spinner("Reading PDF and finding relevant sections..."):
                        try:
                            from treaty_reader import (extract_text_from_pdf,
                                                        find_relevant_sections)
                            text = extract_text_from_pdf(selected_path, max_pages=80)

                            if search_topic:
                                relevant = find_relevant_sections(text, search_topic)
                                if relevant:
                                    st.success(f"✅ Found relevant sections for '{search_topic}'")
                                    st.markdown(f"#### Treaty Text — Results for '{search_topic}'")
                                    # Clean and display in scrollable text area
                                    clean_text = relevant.replace("---", "\n" + "─"*60 + "\n")
                                    st.text_area(
                                        label="Relevant Treaty Sections",
                                        value=clean_text,
                                        height=400,
                                        label_visibility="collapsed"
                                    )
                                    st.download_button(
                                        "📥 Download Treaty Extract",
                                        data=clean_text,
                                        file_name=f"Treaty_{selected_pdf[:20]}_{search_topic[:20]}.txt",
                                        mime="text/plain"
                                    )
                                else:
                                    st.info(f"No specific results for '{search_topic}'. Showing first 2000 characters.")
                                    st.text_area(
                                        label="Treaty Text",
                                        value=text[:2000],
                                        height=400,
                                        label_visibility="collapsed"
                                    )
                            else:
                                st.markdown("#### Treaty Text (first 3000 characters)")
                                st.text_area(
                                    label="Treaty Text",
                                    value=text[:3000],
                                    height=400,
                                    label_visibility="collapsed"
                                )

                        except Exception as e:
                            st.error(f"Error reading PDF: {str(e)}")

            # Show PDF info
            st.markdown("#### Available Treaties")
            pdf_info = []
            for p in pdfs:
                size_kb = p.stat().st_size // 1024
                pdf_info.append({
                    "File Name": p.name[:60],
                    "Size (KB)": size_kb,
                    "Type": "MLI Synthesised" if "synthes" in p.name.lower()
                            else "Comprehensive"
                })
            st.dataframe(pd.DataFrame(pdf_info), use_container_width=True, hide_index=True)




# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — FORM 145 DRAFT GENERATOR
# ════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("### 📝 Form 145 Draft Generator")
    st.markdown("""
    <div class="ita-box">
    <b>ITA 2025:</b> Form 145 replaces Form 15CA (w.e.f. 1 April 2026) — Section 397(3)(d) |
    Rule 220 IT Rules 2026 | File on TRACES portal before remittance
    </div>
    """, unsafe_allow_html=True)
    st.caption("Generate a pre-filled Form 145 draft. CA to review and upload on TRACES portal.")

    col1, col2 = st.columns(2)
    with col1:
        f145_remitter_name = st.text_input("Remitter Name (Indian Entity)", placeholder="e.g. TechSoft Pvt Ltd")
        f145_remitter_pan = st.text_input("Remitter PAN", placeholder="e.g. AAACT1234A")
        f145_remitter_address = st.text_area("Remitter Address", height=80, placeholder="Full address with PIN")
        f145_country = st.selectbox("Country of Remittance", [
            "USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
            "Japan", "Canada", "Australia", "Netherlands", "France",
            "Switzerland", "Hong Kong", "Malaysia", "China", "New Zealand",
            "South Africa", "Sri Lanka", "Thailand", "Italy"
        ])
        f145_currency = st.selectbox("Currency", ["USD", "GBP", "AED", "EUR", "SGD", "JPY", "CAD", "AUD"])

    with col2:
        f145_payee_name = st.text_input("Payee Name (Foreign Entity)", placeholder="e.g. DataCorp LLC")
        f145_payee_address = st.text_area("Payee Address (Foreign)", height=80, placeholder="Full foreign address")
        f145_nature = st.selectbox("Nature of Remittance", [
            "Royalty / Software Licence",
            "Fees for Technical Services (FTS)",
            "Dividend",
            "Interest",
            "Capital Gains",
            "Salary / Employment Income",
            "Business Profits",
            "Other"
        ])
        f145_amount_foreign = st.number_input("Amount (Foreign Currency)", min_value=0.0, step=1000.0)
        f145_amount_inr = st.number_input("Amount (Rs. Lakhs)", min_value=0.0, step=0.5)
        f145_tds_rate = st.number_input("TDS Rate (%)", min_value=0.0, max_value=40.0, step=0.5, value=10.0)
        f145_part = st.selectbox("Form 145 Part", ["Part A", "Part B", "Part C", "Part D"])

    f145_dtaa = st.checkbox("DTAA Benefit Claimed", value=True)
    f145_trc = st.checkbox("TRC Obtained from Payee", value=True)
    f145_form41 = st.checkbox("Form 41 Obtained from Payee", value=True)
    f145_form146 = st.checkbox("Form 146 (CA Certificate) Obtained", value=True)
    f145_purpose = st.text_input("Purpose Code (RBI)", placeholder="e.g. P0802 for software royalty")
    f145_remarks = st.text_area("Additional Remarks", height=60)

    if st.button("📝 Generate Form 145 Draft", type="primary", key="gen_f145"):
        if not f145_remitter_name or not f145_payee_name:
            st.warning("Please fill Remitter Name and Payee Name.")
        else:
            tds_amount = (f145_amount_inr * f145_tds_rate / 100)
            net_remittance = f145_amount_inr - tds_amount

            draft = f"""
FORM 145 — DRAFT
[Under Section 397(3)(d) of Income Tax Act, 2025 read with Rule 220 of Income Tax Rules, 2026]
[Replaces erstwhile Form 15CA]

{'='*70}
FORM 145 — {f145_part.upper()}
{'='*70}

PART I — REMITTER DETAILS
Name of Remitter        : {f145_remitter_name}
PAN of Remitter         : {f145_remitter_pan or '[TO BE FILLED]'}
Address                 : {f145_remitter_address or '[TO BE FILLED]'}
Status                  : Company / Firm / Individual [select]
Residential Status      : Resident

PART II — PAYEE DETAILS
Name of Payee           : {f145_payee_name}
Address (Foreign)       : {f145_payee_address or '[TO BE FILLED]'}
Country of Residence    : {f145_country}
PAN / Tax ID            : [TO BE FILLED — Payee TIN]
Email                   : [TO BE FILLED]

PART III — REMITTANCE DETAILS
Nature of Remittance    : {f145_nature}
Currency                : {f145_currency}
Amount (Foreign Curr.)  : {f145_currency} {f145_amount_foreign:,.2f}
Amount (Indian Rs.)     : Rs. {f145_amount_inr:.2f} Lakhs
Purpose Code (RBI)      : {f145_purpose or '[TO BE FILLED]'}
Country of Remittance   : {f145_country}
Bank through which      : [TO BE FILLED — AD Bank Name and Branch]
  remittance is made
Date of Remittance      : [TO BE FILLED]

PART IV — TAX DEDUCTION DETAILS
Applicable Rate         : {f145_tds_rate}%
TDS Amount Deducted     : Rs. {tds_amount:.2f} Lakhs
Net Remittance Amount   : Rs. {net_remittance:.2f} Lakhs
TDS Challan No.         : [TO BE FILLED after TDS deposit]
BSR Code of Bank        : [TO BE FILLED]
Date of TDS Deposit     : [TO BE FILLED]

PART V — DTAA AND COMPLIANCE DETAILS
DTAA Benefit Claimed    : {'Yes' if f145_dtaa else 'No'}
Applicable DTAA         : India-{f145_country} DTAA
Applicable Article      : [TO BE FILLED — Article No.]
TRC Obtained            : {'Yes' if f145_trc else 'No'}
Form 41 Obtained        : {'Yes' if f145_form41 else 'No'}
Form 146 Obtained       : {'Yes' if f145_form146 else 'No — Obtain before filing'}
Form 146 Cert No.       : [TO BE FILLED — from CA]
Form 146 Date           : [TO BE FILLED]

PART VI — DECLARATION
I/We hereby declare that the information given above is true and correct
to the best of my/our knowledge and belief.

Name of Authorised Person : [TO BE FILLED]
Designation               : [TO BE FILLED]
Date                      : [TO BE FILLED]
Place                     : [TO BE FILLED]

{'='*70}
ADDITIONAL REMARKS: {f145_remarks or 'Nil'}
{'='*70}

IMPORTANT NOTES:
1. This is a DRAFT only. Review carefully before filing on TRACES portal.
2. Form 145 {f145_part} to be filed at: https://www.tdscpc.gov.in
3. Form 146 (CA Certificate) must be uploaded BEFORE Form 145 Part C/D.
4. Form 41 must be obtained from payee BEFORE remittance.
5. TDS to be deposited via Challan 281 within 7 days of deduction.
6. File Form 27Q quarterly return for TDS on non-resident payments.

ITA 2025 References:
- Section 397(3)(d) — Form 145 filing requirement
- Rule 220 IT Rules 2026 — Form 145 Parts A/B/C/D
- Section 393 — TDS on payments to non-residents
- Section 159(8) / Rule 75 — Form 41 mandatory

DISCLAIMER: This draft is for reference only. Actual Form 145 must be
filed on the TRACES portal (www.tdscpc.gov.in) by the authorised person.
Portal submission cannot be automated and requires DSC/OTP authentication.
"""
            st.markdown("#### Form 145 Draft")
            st.text_area("Draft Output", value=draft, height=500, label_visibility="collapsed")
            st.download_button(
                "📥 Download Form 145 Draft",
                data=draft,
                file_name=f"Form145_Draft_{f145_remitter_name[:15]}_{f145_country}.txt",
                mime="text/plain"
            )
            st.info("📌 Upload this on TRACES portal after review. Form 146 must be uploaded first.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — FORM 146 DRAFT GENERATOR
# ════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown("### 🏛️ Form 146 Draft Generator")
    st.markdown("""
    <div class="ita-box">
    <b>ITA 2025:</b> Form 146 replaces Form 15CB (w.e.f. 1 April 2026) — Section 397(3)(d) |
    Must be certified by a Practising Chartered Accountant | Upload on TRACES before Form 145
    </div>
    """, unsafe_allow_html=True)
    st.caption("Generate Form 146 CA Certificate draft. CA to review, certify with DSC and upload on TRACES.")


    col1, col2 = st.columns(2)
    with col1:
        f146_remitter = st.text_input("Remitter Name", placeholder="e.g. TechSoft Pvt Ltd", key="f146_rem")
        f146_remitter_pan = st.text_input("Remitter PAN", placeholder="e.g. AAACT1234A", key="f146_rpan")
        f146_payee = st.text_input("Payee Name (NR)", placeholder="e.g. DataCorp LLC", key="f146_pay")
        f146_country = st.selectbox("Country", [
            "USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
            "Japan", "Canada", "Australia", "Netherlands", "France",
            "Switzerland", "Hong Kong", "Malaysia", "China", "New Zealand"
        ], key="f146_cty")
        f146_nature = st.selectbox("Nature of Payment", [
            "Royalty / Software Licence",
            "Fees for Technical Services (FTS)",
            "Dividend", "Interest", "Capital Gains", "Business Profits"
        ], key="f146_nat")

    with col2:
        f146_amount = st.number_input("Amount (Rs. Lakhs)", min_value=0.0, step=0.5, key="f146_amt")
        f146_dtaa_article = st.text_input("Applicable DTAA Article", placeholder="e.g. Article 12", key="f146_art")
        f146_dtaa_rate = st.number_input("DTAA Rate (%)", min_value=0.0, max_value=40.0, step=0.5, key="f146_rate")
        f146_domestic_rate = st.number_input("Domestic Rate (%)", min_value=0.0, max_value=40.0, step=0.5, value=10.0, key="f146_dom")
        f146_applicable_rate = st.number_input("Applicable Rate (Lower of above) (%)", min_value=0.0, max_value=40.0, step=0.5, key="f146_app")
        f146_trc = st.selectbox("TRC Status", ["Obtained and Verified", "Not Obtained"], key="f146_trc")
        f146_form41 = st.selectbox("Form 41 Status", ["Obtained and Verified", "Not Obtained"], key="f146_f41")

    f146_ca_name = st.text_input("CA Name", placeholder="e.g. TAXAVK — Beespoke Tax Advisors", key="f146_ca")
    f146_ca_memno = st.text_input("CA Membership Number", placeholder="e.g. 078991", key="f146_mem")
    f146_ca_firm = st.text_input("CA Firm Name", placeholder="e.g. TAXAVK — Beespoke Tax Advisors", key="f146_firm")
    f146_remarks = st.text_area("CA Remarks / Qualifications", height=80,
            placeholder="Any qualifications or conditions...", key="f146_rem2")

    if st.button("🏛️ Generate Form 146 Draft", type="primary", key="gen_f146"):
        if not f146_remitter or not f146_payee or not f146_ca_name:
            st.warning("Please fill Remitter, Payee, and CA Name.")
        else:
            tds_amount = f146_amount * f146_applicable_rate / 100

            draft146 = f"""
FORM 146 — DRAFT
[Under Section 397(3)(d) of Income Tax Act, 2025 read with Rule 220 of Income Tax Rules, 2026]
[Replaces erstwhile Form 15CB]
[To be certified by a Practising Chartered Accountant]

{'='*70}
CERTIFICATE UNDER SECTION 397(3)(d) OF INCOME TAX ACT, 2025
FORM 146 — CA CERTIFICATE
{'='*70}

I, {f146_ca_name}, Chartered Accountant, Membership No. {f146_ca_memno},
{f'Partner/Proprietor of {f146_ca_firm},' if f146_ca_firm else ''}
having been appointed to certify the particulars relating to remittance
by {f146_remitter} (PAN: {f146_remitter_pan or '[PAN]'}) hereby certify as follows:

PART I — DETAILS OF REMITTER
Name                    : {f146_remitter}
PAN                     : {f146_remitter_pan or '[TO BE FILLED]'}
Status                  : [Company / Firm / Individual]
Address                 : [TO BE FILLED]

PART II — DETAILS OF PAYEE / BENEFICIARY
Name                    : {f146_payee}
Country of Residence    : {f146_country}
Tax Identification No.  : [TO BE FILLED — Payee TIN in {f146_country}]
Address                 : [TO BE FILLED]

PART III — DETAILS OF REMITTANCE
Nature of Remittance    : {f146_nature}
Amount of Remittance    : Rs. {f146_amount:.2f} Lakhs
Currency                : [TO BE FILLED]
Purpose Code (RBI)      : [TO BE FILLED]
Proposed Date           : [TO BE FILLED]

PART IV — DTAA ANALYSIS AND RATE CERTIFICATION

Applicable DTAA         : India-{f146_country} Double Taxation Avoidance Agreement
Applicable Article      : {f146_dtaa_article or '[TO BE FILLED]'}
DTAA Rate               : {f146_dtaa_rate}% (as per {f146_dtaa_article or 'applicable article'})
Domestic Rate           : {f146_domestic_rate}% (Section 393 read with Section 115A ITA 2025)
More Beneficial Rate    : {f146_applicable_rate}% (being lower of DTAA and Domestic rate)
                          [Under Section 159(2) ITA 2025]

TDS Amount Certifiable  : Rs. {tds_amount:.2f} Lakhs

PART V — DOCUMENTATION VERIFICATION

Tax Residency Certificate (TRC): {f146_trc}
  - Issued by              : Tax Authority of {f146_country}
  - Period covered         : [TO BE FILLED]
  - Reference No.          : [TO BE FILLED]

Form 41 (erstwhile Form 10F): {f146_form41}
  - Submitted by           : {f146_payee}
  - Under Rule 75, Section 159(8) ITA 2025
  - Contains               : Status, Nationality, TIN, Period, Address ✓

PART VI — BENEFICIAL OWNERSHIP VERIFICATION
I hereby certify that based on my examination of available information
and documents, {f146_payee} is the beneficial owner of the above income
and is not a conduit entity.

PART VII — GAAR / PPT ASSESSMENT
Based on my examination, the transaction appears to be:
□ Commercially motivated and not primarily tax-driven
□ Beneficial ownership is clear and not challenged
□ No conduit arrangement is evident
□ MLI PPT / GAAR risk: [LOW / MEDIUM / HIGH — CA to assess]

PART VIII — CA CERTIFICATION

I hereby certify that:
(a) The information furnished above is based on the books of account,
    documents and other records produced before me;
(b) The proposed remittance is in accordance with the provisions of the
    Income Tax Act, 2025 and Income Tax Rules, 2026;
(c) The rate of TDS deducted/to be deducted is correct as per the
    applicable provisions;
(d) Form 41 and Tax Residency Certificate have been duly obtained and
    verified;
(e) To the best of my knowledge and belief, no information material to
    this certificate has been suppressed.

{'CA REMARKS / QUALIFICATIONS:' if f146_remarks else ''}
{f146_remarks if f146_remarks else ''}

Signature of Chartered Accountant: _______________
Name                              : {f146_ca_name}
Membership Number                 : {f146_ca_memno}
Firm Name                         : {f146_ca_firm or '[FIRM NAME]'}
FRN                               : [TO BE FILLED]
Date                              : [TO BE FILLED]
Place                             : [TO BE FILLED]
UDIN                              : [TO BE FILLED — Generate on ICAI portal]

{'='*70}
IMPORTANT NOTES FOR CA:
1. This draft requires your professional review before certification.
2. Generate UDIN on ICAI portal (www.udin.icai.org) before signing.
3. Upload on TRACES portal BEFORE Form 145 is filed.
4. This certificate is valid only with your DSC/OTP authentication.
5. Portal: https://www.tdscpc.gov.in

ITA 2025 References:
- Section 397(3)(d) — Form 146 certification requirement
- Rule 220 IT Rules 2026 — CA Certificate requirement
- Section 159(2) — Beneficial rate selection
- Section 159(8) / Rule 75 — Form 41 verification

DISCLAIMER: This is a DRAFT for reference. The certifying CA is solely
responsible for the accuracy of this certificate. Actual filing on
TRACES portal requires DSC authentication and cannot be automated.
{'='*70}
"""
            st.markdown("#### Form 146 Draft")
            st.text_area("Draft Output", value=draft146, height=500, label_visibility="collapsed")
            st.download_button(
                    "📥 Download Form 146 Draft",
                    data=draft146,
                    file_name=f"Form146_Draft_{f146_remitter[:15]}_{f146_country}.txt",
                    mime="text/plain"
                )
            st.warning("⚠️ CA must review, generate UDIN, sign with DSC and upload on TRACES portal.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — FORM 41 TEMPLATE GENERATOR
# ════════════════════════════════════════════════════════════════════════════
with tab8:
    st.markdown("### 📋 Form 41 Template Generator")
    st.markdown("""
    <div class="ita-box">
    <b>ITA 2025:</b> Form 41 replaces Form 10F (w.e.f. 1 April 2026) — Rule 75, Section 159(8) |
    MANDATORY for ALL DTAA benefit claims | To be furnished by Non-Resident payee
    </div>
    """, unsafe_allow_html=True)
    st.caption("Generate Form 41 data collection template to send to your non-resident payee.")

    col1, col2 = st.columns(2)
    with col1:
        f41_payee_name = st.text_input("Payee Name (NR Entity)", placeholder="e.g. DataCorp LLC", key="f41_name")
        f41_country = st.selectbox("Country of Residence", [
            "USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
            "Japan", "Canada", "Australia", "Netherlands", "France",
            "Switzerland", "Hong Kong", "Malaysia", "China", "New Zealand"
        ], key="f41_cty")
        f41_status = st.selectbox("Status of Payee", [
            "Company", "Firm", "Individual", "Trust", "LLP", "LLC", "Other"
        ], key="f41_status")
        f41_nature = st.selectbox("Nature of Income", [
            "Royalty / Software Licence",
            "Fees for Technical Services",
            "Dividend", "Interest", "Capital Gains", "Business Profits"
        ], key="f41_nat")

    with col2:
        f41_dtaa_article = st.text_input("DTAA Article being claimed",
            placeholder="e.g. Article 12 — Royalties", key="f41_art")
        f41_fy = st.text_input("Financial Year", value="2025-26", key="f41_fy")
        f41_remitter = st.text_input("Indian Remitter Name", placeholder="e.g. TechSoft Pvt Ltd", key="f41_rem")
        f41_ca_name = st.text_input("CA Name (for letter)", placeholder="e.g. TAXAVK — Beespoke Tax Advisors", key="f41_ca")

    if st.button("📋 Generate Form 41 Template", type="primary", key="gen_f41"):
        if not f41_payee_name or not f41_remitter:
            st.warning("Please fill Payee Name and Remitter Name.")
        else:
            template41 = f"""
FORM 41 — DATA COLLECTION TEMPLATE
[Under Rule 75 read with Section 159(8) of Income Tax Act, 2025]
[Replaces erstwhile Form 10F]
[To be completed by Non-Resident Payee and returned to Indian Remitter]

{'='*70}
REQUEST FOR FORM 41 PARTICULARS
{'='*70}

Date: [TO BE FILLED by {f41_payee_name}]

To,
The Authorised Signatory
{f41_payee_name}
{f41_country}

Sub: Request for Form 41 Particulars under Section 159(8) of ITA 2025

Dear Sir/Madam,

We, {f41_remitter}, are required to deduct TDS on the payment to be made
to you under Section 393 of the Income Tax Act, 2025.

To avail the benefit of India-{f41_country} DTAA under {f41_dtaa_article},
we are required to obtain the following particulars from you in Form 41
as mandated by Rule 75 of Income Tax Rules, 2026.

Please furnish the following information:

{'='*70}
FORM 41 — PARTICULARS TO BE FURNISHED BY {f41_payee_name.upper()}
{'='*70}

MANDATORY FIELDS (Rule 75, Section 159(8) ITA 2025):

1. STATUS OF THE PERSON
   Status (tick): □ Company  □ Firm  □ Individual  □ Trust  □ LLC  □ LLP  □ Other
   Suggested: {f41_status}
   Your Response: _______________________________________________

2. NATIONALITY / COUNTRY OF INCORPORATION
   Country: _______________________________________________
   (Suggested: {f41_country})

3. TAX IDENTIFICATION NUMBER IN COUNTRY OF RESIDENCE
   TIN / EIN / UTR / UEN (as applicable): _______________________________________________
   Name of Issuing Authority: _______________________________________________

4. PERIOD FOR WHICH RESIDENTIAL STATUS IS CLAIMED
   From Date: _______________ To Date: _______________
   Financial Year: {f41_fy}
   Confirm residence in {f41_country} for above period: □ Yes  □ No

5. ADDRESS IN COUNTRY OF RESIDENCE
   Registered/Official Address:
   _______________________________________________
   _______________________________________________
   _______________________________________________
   City/State/ZIP: _______________________________________________
   Country: {f41_country}

6. DTAA BENEFIT CLAIMED
   Treaty: India-{f41_country} DTAA
   Article being claimed: {f41_dtaa_article or '[TO BE FILLED]'}
   Nature of Income: {f41_nature}

7. BENEFICIAL OWNERSHIP DECLARATION
   I/We hereby declare that:
   (a) We are the beneficial owner of the income described above
   (b) We are NOT a conduit or pass-through entity
   (c) The income will not be passed on to a resident of a third country
       to obtain treaty benefits not otherwise available

   Confirmation: □ Yes, we confirm the above declarations

8. PERMANENT ESTABLISHMENT (PE) DECLARATION
   Do you have a PE in India? □ Yes  □ No
   If yes, income attributable to PE: _______________________________________________

9. TAX RESIDENCY CERTIFICATE (TRC)
   TRC Enclosed: □ Yes  □ No — Will provide by: _______________
   TRC issued by: _______________________________________________
   TRC Reference Number: _______________________________________________
   TRC Valid for period: _______________________________________________

{'='*70}
DECLARATION BY AUTHORISED SIGNATORY OF {f41_payee_name.upper()}
{'='*70}

I, _________________________, being duly authorised, hereby declare that:

(a) The information furnished above is true and correct;
(b) The entity is a tax resident of {f41_country} for the period stated;
(c) The Tax Identification Number stated above is correct;
(d) We are eligible to claim benefits under India-{f41_country} DTAA;
(e) We will immediately inform {f41_remitter} of any change in residential
    status or any other information affecting the above declaration.

Name of Authorised Person  : _______________________________________________
Designation                : _______________________________________________
Date                       : _______________________________________________
Place                      : _______________________________________________
Signature                  : _______________________________________________
Official Stamp             : [AFFIX COMPANY STAMP]

{'='*70}
IMPORTANT NOTES FOR {f41_payee_name.upper()}:
1. This form is MANDATORY under Section 159(8) of ITA 2025.
2. Without this form, {f41_remitter} CANNOT avail DTAA benefit and must
   deduct TDS at the higher domestic rate of 20-40%.
3. Enclose a copy of your Tax Residency Certificate (TRC) with this form.
4. Return the signed form along with TRC to {f41_remitter} / {f41_ca_name or 'the CA'}.
5. This information will be used for Form 146 CA Certificate preparation.

FOR QUERIES CONTACT:
{f41_ca_name or '[CA NAME]'}
Chartered Accountant
[Contact details]

{'='*70}
LEGAL REFERENCE:
Rule 75, Income Tax Rules, 2026 (Form 41 requirements)
Section 159(8), Income Tax Act, 2025 (mandatory for DTAA benefit)
Replaces erstwhile Form 10F under Rule 21AB of Income Tax Rules, 1962

DISCLAIMER: This template is for guidance only. The non-resident entity
is responsible for accuracy of declarations made in Form 41.
{'='*70}
"""
            st.markdown("#### Form 41 Template")
            st.text_area("Template Output", value=template41, height=500, label_visibility="collapsed")
            st.download_button(
                "📥 Download Form 41 Template",
                data=template41,
                file_name=f"Form41_Template_{f41_payee_name[:15]}_{f41_country}.txt",
                mime="text/plain"
            )
            st.success("✅ Send this to your non-resident payee for completion. Collect signed copy before remittance.")
            st.info("📌 Form 41 must be signed by authorised signatory of the foreign entity and returned along with TRC.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 9 — RESIDENTIAL STATUS CHECKER (Section 6, Income Tax Act, 2025)
# ════════════════════════════════════════════════════════════════════════════
with tab9:
    st.markdown("### 🌐 Residential Status Checker")
    st.caption("Determine residential status under **Section 6 of the Income Tax Act, 2025** "
               "(applicable to tax years beginning on or after 1 April 2026). "
               "Covers Resident & Ordinarily Resident (ROR), Resident but Not Ordinarily "
               "Resident (RNOR), Non-Resident (NR), and the deemed-resident rule for "
               "high-income citizens under Section 6(1A).")

    st.markdown("""
    <div class="ita-box">
    <b>Note:</b> The basic day-count tests under ITA 2025 are unchanged from Section 6(1) of the
    Income-tax Act, 1961. This calculator is a practitioner aid for a first-cut assessment only —
    always verify against the exact facts, travel records and the final Act/Rules text before
    advising a client or filing a return.
    </div>
    """, unsafe_allow_html=True)

    assessee_type = st.radio(
        "Type of Assessee",
        ["Individual", "Hindu Undivided Family (HUF)", "Firm / AOP / BOI", "Company"],
        horizontal=True,
        key="rs_assessee_type"
    )

    st.markdown("---")

    # ── INDIVIDUAL ──────────────────────────────────────────────────────
    if assessee_type == "Individual":
        col1, col2 = st.columns(2)
        with col1:
            rs_days_this_year = st.number_input(
                "Days stayed in India during the relevant tax year",
                min_value=0, max_value=366, value=0, key="rs_days_ty"
            )
            rs_days_prev4 = st.number_input(
                "Total days stayed in India during the 4 tax years immediately preceding",
                min_value=0, max_value=1464, value=0, key="rs_days_p4"
            )
            rs_category = st.selectbox(
                "Category of Individual",
                ["Ordinary case (not covered by the categories below)",
                 "Indian citizen leaving India for employment outside India, or as a crew "
                 "member of an Indian ship",
                 "Indian citizen / Person of Indian Origin (PIO) coming on a visit to India"],
                key="rs_category"
            )
        with col2:
            rs_indian_income = st.number_input(
                "Total income from Indian sources, excluding foreign income (₹ Lakhs) — "
                "for this tax year",
                min_value=0.0, value=0.0, step=1.0, key="rs_income",
                help="Relevant only for the 'visit to India' category and for the deemed-"
                     "resident test under Section 6(1A)."
            )
            rs_is_citizen = st.checkbox(
                "Individual is an Indian citizen",
                value=False, key="rs_is_citizen"
            )
            rs_liable_tax_elsewhere = st.radio(
                "Liable to tax in any other country/territory by reason of domicile, "
                "residence or a similar criterion?",
                ["Yes", "No"], horizontal=True, key="rs_liable_elsewhere",
                help="Used only for the Section 6(1A) deemed-resident test, which applies "
                     "when the normal day-count tests do NOT make the individual a resident."
            )

        st.markdown("##### For the Ordinarily Resident (ROR) test — only needed if Resident")
        col3, col4 = st.columns(2)
        with col3:
            rs_resident_years_10 = st.number_input(
                "Resident in India in how many of the preceding 10 tax years?",
                min_value=0, max_value=10, value=0, key="rs_res_10"
            )
        with col4:
            rs_days_prev7 = st.number_input(
                "Total days stayed in India during the preceding 7 tax years",
                min_value=0, max_value=2562, value=0, key="rs_days_p7"
            )

        if st.button("🧮 Determine Residential Status", type="primary", key="rs_calc_individual"):
            notes = []
            # Determine effective "60-day" threshold per category
            if rs_category.startswith("Indian citizen leaving India for employment"):
                threshold = 182
                notes.append("Category: citizen leaving for employment abroad / ship crew — "
                              "the 60-day limb is replaced with 182 days, so effectively only "
                              "the 182-day test applies.")
            elif rs_category.startswith("Indian citizen / Person of Indian Origin"):
                if rs_indian_income > 15:
                    threshold = 120
                    notes.append("Category: citizen/PIO on a visit to India with Indian-source "
                                  "income above ₹15 lakh — the 60-day limb is replaced with 120 days.")
                else:
                    threshold = 182
                    notes.append("Category: citizen/PIO on a visit to India with Indian-source "
                                  "income up to ₹15 lakh — the 60-day limb is replaced with 182 "
                                  "days, so effectively only the 182-day test applies.")
            else:
                threshold = 60

            cond_a = rs_days_this_year >= 182
            cond_b = (rs_days_this_year >= threshold) and (rs_days_prev4 >= 365)
            is_resident = cond_a or cond_b

            deemed_resident = False
            if not is_resident:
                if (rs_is_citizen and rs_indian_income > 15
                        and rs_liable_tax_elsewhere == "No"):
                    deemed_resident = True
                    is_resident = True
                    notes.append("Deemed Resident under Section 6(1A): Indian citizen, "
                                  "Indian-source income above ₹15 lakh, and not liable to tax "
                                  "in any other country by reason of domicile/residence.")

            if not is_resident:
                st.markdown("""
                <div class="warning-box">
                <b>Result: NON-RESIDENT (NR)</b><br>
                Neither the 182-day test nor the 60/120/182-day + 365-day test (nor the Section
                6(1A) deemed-resident rule) is satisfied. Only income received/accruing in
                India is taxable in India.
                </div>
                """, unsafe_allow_html=True)
            else:
                # RNOR direct-trigger: visiting citizen/PIO, income > 15L, resident only via
                # the 120-day route (i.e. stayed 120–181 days, not the full 182)
                direct_rnor = (
                    rs_category.startswith("Indian citizen / Person of Indian Origin")
                    and rs_indian_income > 15
                    and not cond_a and cond_b
                )
                ror_conditions_met = (rs_resident_years_10 >= 2) and (rs_days_prev7 >= 730)

                if deemed_resident:
                    final_status = "RNOR"
                    notes.append("A deemed resident under Section 6(1A) is always classified "
                                  "as Resident but Not Ordinarily Resident (RNOR).")
                elif direct_rnor:
                    final_status = "RNOR"
                    notes.append("Resident only via the 120-day route for a high-income "
                                  "citizen/PIO visiting India — classified directly as RNOR.")
                elif ror_conditions_met:
                    final_status = "ROR"
                else:
                    final_status = "RNOR"

                if final_status == "ROR":
                    st.markdown("""
                    <div class="success-box">
                    <b>Result: RESIDENT AND ORDINARILY RESIDENT (ROR)</b><br>
                    Global (worldwide) income is taxable in India.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="ita-box">
                    <b>Result: RESIDENT BUT NOT ORDINARILY RESIDENT (RNOR)</b><br>
                    Indian-source income is taxable. Foreign income is taxable only if it is
                    derived from a business controlled from, or a profession set up in, India.
                    </div>
                    """, unsafe_allow_html=True)

            with st.expander("Show reasoning / basis"):
                st.write(f"182-day test satisfied: **{cond_a}**")
                st.write(f"{threshold}-day + 365-day (preceding 4 years) test satisfied: **{cond_b}**")
                for n in notes:
                    st.caption(f"• {n}")
                st.caption("Legal basis: Section 6, Income Tax Act, 2025 (basic conditions, "
                           "citizen/PIO relaxations, Section 6(1A) deemed-resident rule, and "
                           "the ROR test of 2-out-of-10 preceding years + 730 days in the "
                           "preceding 7 years).")

    # ── HUF ──────────────────────────────────────────────────────────────
    elif assessee_type == "Hindu Undivided Family (HUF)":
        rs_huf_control = st.radio(
            "Is the control and management of the HUF's affairs situated "
            "**wholly outside India** during the relevant tax year?",
            ["Yes — wholly outside India", "No — wholly or partly in India"],
            key="rs_huf_control"
        )
        st.markdown("##### Karta's residential history (needed only if the HUF is Resident)")
        col1, col2 = st.columns(2)
        with col1:
            rs_karta_years_10 = st.number_input(
                "Karta resident in India in how many of the preceding 10 tax years?",
                min_value=0, max_value=10, value=0, key="rs_karta_10"
            )
        with col2:
            rs_karta_days_7 = st.number_input(
                "Karta's total days in India during the preceding 7 tax years",
                min_value=0, max_value=2562, value=0, key="rs_karta_7"
            )

        if st.button("🧮 Determine Residential Status", type="primary", key="rs_calc_huf"):
            if rs_huf_control.startswith("Yes"):
                st.markdown("""
                <div class="warning-box"><b>Result: NON-RESIDENT (NR)</b><br>
                Control and management is wholly outside India during the year.
                </div>""", unsafe_allow_html=True)
            else:
                ror = (rs_karta_years_10 >= 2) and (rs_karta_days_7 >= 730)
                if ror:
                    st.markdown("""
                    <div class="success-box"><b>Result: RESIDENT AND ORDINARILY RESIDENT (ROR)</b><br>
                    Global income is taxable in India.</div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="ita-box"><b>Result: RESIDENT BUT NOT ORDINARILY RESIDENT (RNOR)</b><br>
                    Based on the Karta not satisfying the ROR conditions (resident in at least
                    2 of the preceding 10 years, and 730+ days in India in the preceding 7 years).
                    </div>""", unsafe_allow_html=True)

    # ── FIRM / AOP / BOI ─────────────────────────────────────────────────
    elif assessee_type == "Firm / AOP / BOI":
        rs_firm_control = st.radio(
            "Is the control and management of the affairs of the firm / AOP / BOI "
            "situated **wholly outside India** during the relevant tax year?",
            ["Yes — wholly outside India", "No — wholly or partly in India"],
            key="rs_firm_control"
        )
        if st.button("🧮 Determine Residential Status", type="primary", key="rs_calc_firm"):
            if rs_firm_control.startswith("Yes"):
                st.markdown("""
                <div class="warning-box"><b>Result: NON-RESIDENT (NR)</b></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box"><b>Result: RESIDENT</b><br>
                Firms, AOPs and BOIs can only be Resident or Non-Resident — there is no
                RNOR category for these entities.</div>
                """, unsafe_allow_html=True)

    # ── COMPANY ──────────────────────────────────────────────────────────
    else:
        rs_incorporated_india = st.radio(
            "Is the company incorporated in India?",
            ["Yes", "No"], horizontal=True, key="rs_co_incorp"
        )
        rs_poem_india = st.radio(
            "Is the Place of Effective Management (POEM) of the company in India "
            "during the relevant tax year?",
            ["Yes", "No"], horizontal=True, key="rs_co_poem"
        )
        if st.button("🧮 Determine Residential Status", type="primary", key="rs_calc_company"):
            if rs_incorporated_india == "Yes" or rs_poem_india == "Yes":
                st.markdown("""
                <div class="success-box"><b>Result: RESIDENT</b><br>
                A company is resident in India if it is incorporated in India, or if its
                POEM is in India during the year.</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box"><b>Result: NON-RESIDENT (NR)</b></div>
                """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6B7570; font-size:0.8rem; font-family:'Share Tech Mono', monospace;">
🤖 DTAA ADVISOR — TAXAVK — BEESPOKE TAX ADVISORS &nbsp;|&nbsp;
AICA Level 2 Capstone 2026 &nbsp;|&nbsp;
Built under Income Tax Act, 2025 | Income Tax Rules, 2026 &nbsp;|&nbsp;
Form 145 | Form 146 | Form 41 | Section 393<br>
<i>This tool is for professional guidance only. Verify with actual treaty text before filing.</i>
</div>
""", unsafe_allow_html=True)
