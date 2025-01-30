import streamlit as st


def load_css():
    st.markdown("""
    <style>
        /* Estilos da navbar */
        .nav-bar {
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 1rem;
        }
        
        /* Estilos dos botões */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 12px;
            transition: all 0.3s ease;
            text-align: left;
        }
        
        .stButton>button:hover {
            transform: translateX(5px);
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Estilo do título */
        .header {
            font-size: 2.5em !important;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)
