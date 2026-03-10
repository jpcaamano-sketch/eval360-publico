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
    /* Radio buttons horizontales: wrap en mobile */
    [data-testid="stRadio"] > div {
        flex-wrap: wrap !important;
        gap: 0.4rem 1.2rem !important;
    }
    [data-testid="stRadio"] label {
        font-size: 0.9rem !important;
        white-space: nowrap !important;
    }
    /* Reducir padding en mobile */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 2rem !important;
        }
        [data-testid="stRadio"] label {
            font-size: 0.82rem !important;
        }
    }
"""

AUTO_CSS = """
<style>
    .stApp {
        background-color: #e8f4f8;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {
        background-color: #e8f4f8 !important;
        border-bottom: none !important;
        box-shadow: none !important;
    }
    [data-testid="stToolbar"]        { visibility: hidden !important; }
    [data-testid="stToolbarActions"] { visibility: hidden !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    [data-testid="stStatusWidget"]   { display: none !important; }
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
    }
""" + EVAL_TABLE_CSS + """
</style>
"""

FEEDBACK_CSS = """
<style>
    .stApp {
        background-color: #e8f4f8;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {
        background-color: #e8f4f8 !important;
        border-bottom: none !important;
        box-shadow: none !important;
    }
    [data-testid="stToolbar"]        { visibility: hidden !important; }
    [data-testid="stToolbarActions"] { visibility: hidden !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    [data-testid="stStatusWidget"]   { display: none !important; }
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
    }
""" + EVAL_TABLE_CSS + """
</style>
"""
