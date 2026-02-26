"""Estilos CSS para las aplicaciones."""

ADMIN_CSS = """
<style>
    /* Sidebar azul oscuro */
    [data-testid="stSidebar"] { background-color: #1a4a7a; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio label { color: white !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.3); }

    /* Círculo amarillo en opción seleccionada */
    [data-testid="stSidebar"] input[type="radio"]:checked {
        box-shadow: 0 0 0 3px #FFD700 !important;
        outline: none !important;
    }

    /* Botones del contenido principal más pequeños */
    [data-testid="stMainBlockContainer"] .stButton > button {
        font-size: 0.8rem !important;
        padding: 4px 10px !important;
        min-height: 0 !important;
        white-space: nowrap !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs [data-baseweb="tab"] { font-size: 1rem; }
</style>
"""

EVAL_TABLE_CSS = """
    /* Centrar contenido en columnas de escala (3ra en adelante) */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(n+3) [data-testid="stElementContainer"] {
        text-align: center !important;
    }
    [data-testid="stCheckbox"] {
        display: inline-flex !important;
    }
"""

AUTO_CSS = """
<style>
    .stApp {
        background-color: #e8f4f8;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }
""" + EVAL_TABLE_CSS + """
</style>
"""

FEEDBACK_CSS = """
<style>
    .stApp {
        background-color: #f0f8e8;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }
""" + EVAL_TABLE_CSS + """
</style>
"""
