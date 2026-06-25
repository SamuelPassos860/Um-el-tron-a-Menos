import hmac
import json
import os
import streamlit as st
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="Tabela Periódica Interativa",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ELEMENTOS = [
    {"z": 1, "símbolo": "H", "nome": "Hidrogênio", "categoria": "Não-metal", "period": 1, "group": 1},
    {"z": 2, "símbolo": "He", "nome": "Hélio", "categoria": "Gás nobre", "period": 1, "group": 18},
    {"z": 3, "símbolo": "Li", "nome": "Lítio", "categoria": "Metal alcalino", "period": 2, "group": 1},
    {"z": 4, "símbolo": "Be", "nome": "Berílio", "categoria": "Metal alcalinoterroso", "period": 2, "group": 2},
    {"z": 5, "símbolo": "B", "nome": "Boro", "categoria": "Semimetal", "period": 2, "group": 13},
    {"z": 6, "símbolo": "C", "nome": "Carbono", "categoria": "Não-metal", "period": 2, "group": 14},
    {"z": 7, "símbolo": "N", "nome": "Nitrogênio", "categoria": "Não-metal", "period": 2, "group": 15},
    {"z": 8, "símbolo": "O", "nome": "Oxigênio", "categoria": "Não-metal", "period": 2, "group": 16},
    {"z": 9, "símbolo": "F", "nome": "Flúor", "categoria": "Halogênio", "period": 2, "group": 17},
    {"z": 10, "símbolo": "Ne", "nome": "Neônio", "categoria": "Gás nobre", "period": 2, "group": 18},
    {"z": 11, "símbolo": "Na", "nome": "Sódio", "categoria": "Metal alcalino", "period": 3, "group": 1},
    {"z": 12, "símbolo": "Mg", "nome": "Magnésio", "categoria": "Metal alcalinoterroso", "period": 3, "group": 2},
    {"z": 13, "símbolo": "Al", "nome": "Alumínio", "categoria": "Metal de pós-transição", "period": 3, "group": 13},
    {"z": 14, "símbolo": "Si", "nome": "Silício", "categoria": "Semimetal", "period": 3, "group": 14},
    {"z": 15, "símbolo": "P", "nome": "Fósforo", "categoria": "Não-metal", "period": 3, "group": 15},
    {"z": 16, "símbolo": "S", "nome": "Enxofre", "categoria": "Não-metal", "period": 3, "group": 16},
    {"z": 17, "símbolo": "Cl", "nome": "Cloro", "categoria": "Halogênio", "period": 3, "group": 17},
    {"z": 18, "símbolo": "Ar", "nome": "Argônio", "categoria": "Gás nobre", "period": 3, "group": 18},
    {"z": 19, "símbolo": "K", "nome": "Potássio", "categoria": "Metal alcalino", "period": 4, "group": 1},
    {"z": 20, "símbolo": "Ca", "nome": "Cálcio", "categoria": "Metal alcalinoterroso", "period": 4, "group": 2},
    {"z": 21, "símbolo": "Sc", "nome": "Escândio", "categoria": "Metal de transição", "period": 4, "group": 3},
    {"z": 22, "símbolo": "Ti", "nome": "Titânio", "categoria": "Metal de transição", "period": 4, "group": 4},
    {"z": 23, "símbolo": "V", "nome": "Vanádio", "categoria": "Metal de transição", "period": 4, "group": 5},
    {"z": 24, "símbolo": "Cr", "nome": "Cromo", "categoria": "Metal de transição", "period": 4, "group": 6},
    {"z": 25, "símbolo": "Mn", "nome": "Manganês", "categoria": "Metal de transição", "period": 4, "group": 7},
    {"z": 26, "símbolo": "Fe", "nome": "Ferro", "categoria": "Metal de transição", "period": 4, "group": 8},
    {"z": 27, "símbolo": "Co", "nome": "Cobalto", "categoria": "Metal de transição", "period": 4, "group": 9},
    {"z": 28, "símbolo": "Ni", "nome": "Níquel", "categoria": "Metal de transição", "period": 4, "group": 10},
    {"z": 29, "símbolo": "Cu", "nome": "Cobre", "categoria": "Metal de transição", "period": 4, "group": 11},
    {"z": 30, "símbolo": "Zn", "nome": "Zinco", "categoria": "Metal de transição", "period": 4, "group": 12},
    {"z": 31, "símbolo": "Ga", "nome": "Gálio", "categoria": "Metal de pós-transição", "period": 4, "group": 13},
    {"z": 32, "símbolo": "Ge", "nome": "Germânio", "categoria": "Semimetal", "period": 4, "group": 14},
    {"z": 33, "símbolo": "As", "nome": "Arsênio", "categoria": "Semimetal", "period": 4, "group": 15},
    {"z": 34, "símbolo": "Se", "nome": "Selênio", "categoria": "Não-metal", "period": 4, "group": 16},
    {"z": 35, "símbolo": "Br", "nome": "Bromo", "categoria": "Halogênio", "period": 4, "group": 17},
    {"z": 36, "símbolo": "Kr", "nome": "Criptônio", "categoria": "Gás nobre", "period": 4, "group": 18},
    {"z": 37, "símbolo": "Rb", "nome": "Rubídio", "categoria": "Metal alcalino", "period": 5, "group": 1},
    {"z": 38, "símbolo": "Sr", "nome": "Estrôncio", "categoria": "Metal alcalinoterroso", "period": 5, "group": 2},
    {"z": 39, "símbolo": "Y", "nome": "Ítrio", "categoria": "Metal de transição", "period": 5, "group": 3},
    {"z": 40, "símbolo": "Zr", "nome": "Zircônio", "categoria": "Metal de transição", "period": 5, "group": 4},
    {"z": 41, "símbolo": "Nb", "nome": "Nióbio", "categoria": "Metal de transição", "period": 5, "group": 5},
    {"z": 42, "símbolo": "Mo", "nome": "Molibdênio", "categoria": "Metal de transição", "period": 5, "group": 6},
    {"z": 43, "símbolo": "Tc", "nome": "Tecnécio", "categoria": "Metal de transição", "period": 5, "group": 7},
    {"z": 44, "símbolo": "Ru", "nome": "Rutênio", "categoria": "Metal de transição", "period": 5, "group": 8},
    {"z": 45, "símbolo": "Rh", "nome": "Ródio", "categoria": "Metal de transição", "period": 5, "group": 9},
    {"z": 46, "símbolo": "Pd", "nome": "Paládio", "categoria": "Metal de transição", "period": 5, "group": 10},
    {"z": 47, "símbolo": "Ag", "nome": "Prata", "categoria": "Metal de transição", "period": 5, "group": 11},
    {"z": 48, "símbolo": "Cd", "nome": "Cádmio", "categoria": "Metal de transição", "period": 5, "group": 12},
    {"z": 49, "símbolo": "In", "nome": "Índio", "categoria": "Metal de pós-transição", "period": 5, "group": 13},
    {"z": 50, "símbolo": "Sn", "nome": "Estanho", "categoria": "Metal de pós-transição", "period": 5, "group": 14},
    {"z": 51, "símbolo": "Sb", "nome": "Antimônio", "categoria": "Semimetal", "period": 5, "group": 15},
    {"z": 52, "símbolo": "Te", "nome": "Telúrio", "categoria": "Semimetal", "period": 5, "group": 16},
    {"z": 53, "símbolo": "I", "nome": "Iodo", "categoria": "Halogênio", "period": 5, "group": 17},
    {"z": 54, "símbolo": "Xe", "nome": "Xenônio", "categoria": "Gás nobre", "period": 5, "group": 18},
    {"z": 55, "símbolo": "Cs", "nome": "Césio", "categoria": "Metal alcalino", "period": 6, "group": 1},
    {"z": 56, "símbolo": "Ba", "nome": "Bário", "categoria": "Metal alcalinoterroso", "period": 6, "group": 2},
    {"z": 57, "símbolo": "La", "nome": "Lantânio", "categoria": "Lantanídeo", "period": 6, "group": 3},
    {"z": 58, "símbolo": "Ce", "nome": "Cério", "categoria": "Lantanídeo", "period": 8, "group": 4},
    {"z": 59, "símbolo": "Pr", "nome": "Praseodímio", "categoria": "Lantanídeo", "period": 8, "group": 5},
    {"z": 60, "símbolo": "Nd", "nome": "Neodímio", "categoria": "Lantanídeo", "period": 8, "group": 6},
    {"z": 61, "símbolo": "Pm", "nome": "Promécio", "categoria": "Lantanídeo", "period": 8, "group": 7},
    {"z": 62, "símbolo": "Sm", "nome": "Samário", "categoria": "Lantanídeo", "period": 8, "group": 8},
    {"z": 63, "símbolo": "Eu", "nome": "Európio", "categoria": "Lantanídeo", "period": 8, "group": 9},
    {"z": 64, "símbolo": "Gd", "nome": "Gadolínio", "categoria": "Lantanídeo", "period": 8, "group": 10},
    {"z": 65, "símbolo": "Tb", "nome": "Térbio", "categoria": "Lantanídeo", "period": 8, "group": 11},
    {"z": 66, "símbolo": "Dy", "nome": "Disprósio", "categoria": "Lantanídeo", "period": 8, "group": 12},
    {"z": 67, "símbolo": "Ho", "nome": "Hólmio", "categoria": "Lantanídeo", "period": 8, "group": 13},
    {"z": 68, "símbolo": "Er", "nome": "Érbio", "categoria": "Lantanídeo", "period": 8, "group": 14},
    {"z": 69, "símbolo": "Tm", "nome": "Túlio", "categoria": "Lantanídeo", "period": 8, "group": 15},
    {"z": 70, "símbolo": "Yb", "nome": "Itérbio", "categoria": "Lantanídeo", "period": 8, "group": 16},
    {"z": 71, "símbolo": "Lu", "nome": "Lutécio", "categoria": "Lantanídeo", "period": 8, "group": 17},
    {"z": 72, "símbolo": "Hf", "nome": "Háfnio", "categoria": "Metal de transição", "period": 6, "group": 4},
    {"z": 73, "símbolo": "Ta", "nome": "Tântalo", "categoria": "Metal de transição", "period": 6, "group": 5},
    {"z": 74, "símbolo": "W", "nome": "Tungstênio", "categoria": "Metal de transição", "period": 6, "group": 6},
    {"z": 75, "símbolo": "Re", "nome": "Rênio", "categoria": "Metal de transição", "period": 6, "group": 7},
    {"z": 76, "símbolo": "Os", "nome": "Ósmio", "categoria": "Metal de transição", "period": 6, "group": 8},
    {"z": 77, "símbolo": "Ir", "nome": "Irídio", "categoria": "Metal de transição", "period": 6, "group": 9},
    {"z": 78, "símbolo": "Pt", "nome": "Platina", "categoria": "Metal de transição", "period": 6, "group": 10},
    {"z": 79, "símbolo": "Au", "nome": "Ouro", "categoria": "Metal de transição", "period": 6, "group": 11},
    {"z": 80, "símbolo": "Hg", "nome": "Mercúrio", "categoria": "Metal de transição", "period": 6, "group": 12},
    {"z": 81, "símbolo": "Tl", "nome": "Tálio", "categoria": "Metal de pós-transição", "period": 6, "group": 13},
    {"z": 82, "símbolo": "Pb", "nome": "Chumbo", "categoria": "Metal de pós-transição", "period": 6, "group": 14},
    {"z": 83, "símbolo": "Bi", "nome": "Bismuto", "categoria": "Metal de pós-transição", "period": 6, "group": 15},
    {"z": 84, "símbolo": "Po", "nome": "Polônio", "categoria": "Semimetal", "period": 6, "group": 16},
    {"z": 85, "símbolo": "At", "nome": "Astato", "categoria": "Halogênio", "period": 6, "group": 17},
    {"z": 86, "símbolo": "Rn", "nome": "Radônio", "categoria": "Gás nobre", "period": 6, "group": 18},
    {"z": 87, "símbolo": "Fr", "nome": "Frâncio", "categoria": "Metal alcalino", "period": 7, "group": 1},
    {"z": 88, "símbolo": "Ra", "nome": "Rádio", "categoria": "Metal alcalinoterroso", "period": 7, "group": 2},
    {"z": 89, "símbolo": "Ac", "nome": "Actínio", "categoria": "Actinídeo", "period": 7, "group": 3},
    {"z": 90, "símbolo": "Th", "nome": "Tório", "categoria": "Actinídeo", "period": 9, "group": 4},
    {"z": 91, "símbolo": "Pa", "nome": "Protactínio", "categoria": "Actinídeo", "period": 9, "group": 5},
    {"z": 92, "símbolo": "U", "nome": "Urânio", "categoria": "Actinídeo", "period": 9, "group": 6},
    {"z": 93, "símbolo": "Np", "nome": "Netúnio", "categoria": "Actinídeo", "period": 9, "group": 7},
    {"z": 94, "símbolo": "Pu", "nome": "Plutônio", "categoria": "Actinídeo", "period": 9, "group": 8},
    {"z": 95, "símbolo": "Am", "nome": "Amerício", "categoria": "Actinídeo", "period": 9, "group": 9},
    {"z": 96, "símbolo": "Cm", "nome": "Cúrio", "categoria": "Actinídeo", "period": 9, "group": 10},
    {"z": 97, "símbolo": "Bk", "nome": "Berquélio", "categoria": "Actinídeo", "period": 9, "group": 11},
    {"z": 98, "símbolo": "Cf", "nome": "Califórnio", "categoria": "Actinídeo", "period": 9, "group": 12},
    {"z": 99, "símbolo": "Es", "nome": "Einstênio", "categoria": "Actinídeo", "period": 9, "group": 13},
    {"z": 100, "símbolo": "Fm", "nome": "Férmio", "categoria": "Actinídeo", "period": 9, "group": 14},
    {"z": 101, "símbolo": "Md", "nome": "Mendelévio", "categoria": "Actinídeo", "period": 9, "group": 15},
    {"z": 102, "símbolo": "No", "nome": "Nobelio", "categoria": "Actinídeo", "period": 9, "group": 16},
    {"z": 103, "símbolo": "Lr", "nome": "Laurêncio", "categoria": "Actinídeo", "period": 9, "group": 17},
    {"z": 104, "símbolo": "Rf", "nome": "Rutherfordio", "categoria": "Metal de transição", "period": 7, "group": 4},
    {"z": 105, "símbolo": "Db", "nome": "Dubnio", "categoria": "Metal de transição", "period": 7, "group": 5},
    {"z": 106, "símbolo": "Sg", "nome": "Seabórgio", "categoria": "Metal de transição", "period": 7, "group": 6},
    {"z": 107, "símbolo": "Bh", "nome": "Bóhrio", "categoria": "Metal de transição", "period": 7, "group": 7},
    {"z": 108, "símbolo": "Hs", "nome": "Hássio", "categoria": "Metal de transição", "period": 7, "group": 8},
    {"z": 109, "símbolo": "Mt", "nome": "Meitnério", "categoria": "Metal de transição", "period": 7, "group": 9},
    {"z": 110, "símbolo": "Ds", "nome": "Darmstádio", "categoria": "Metal de transição", "period": 7, "group": 10},
    {"z": 111, "símbolo": "Rg", "nome": "Roentgênio", "categoria": "Metal de transição", "period": 7, "group": 11},
    {"z": 112, "símbolo": "Cn", "nome": "Copernício", "categoria": "Metal de transição", "period": 7, "group": 12},
    {"z": 113, "símbolo": "Nh", "nome": "Nihônio", "categoria": "Metal de pós-transição", "period": 7, "group": 13},
    {"z": 114, "símbolo": "Fl", "nome": "Fleróvio", "categoria": "Metal de pós-transição", "period": 7, "group": 14},
    {"z": 115, "símbolo": "Mc", "nome": "Moscóvio", "categoria": "Metal de pós-transição", "period": 7, "group": 15},
    {"z": 116, "símbolo": "Lv", "nome": "Livermório", "categoria": "Metal de pós-transição", "period": 7, "group": 16},
    {"z": 117, "símbolo": "Ts", "nome": "Tenessino", "categoria": "Halogênio", "period": 7, "group": 17},
    {"z": 118, "símbolo": "Og", "nome": "Oganessônio", "categoria": "Gás nobre", "period": 7, "group": 18},
]

CORES_CATEGORIA = {
    "Não-metal": "#c8e6c9",
    "Gás nobre": "#b3e5fc",
    "Metal alcalino": "#fff9c4",
    "Metal alcalinoterroso": "#ffe0b2",
    "Semimetal": "#d1c4e9",
    "Halogênio": "#f8bbd0",
    "Metal de transição": "#b0bec5",
    "Metal de pós-transição": "#d7ccc8",
    "Lantanídeo": "#ffd54f",
    "Actinídeo": "#ff8a65",
}

MASSAS_ATOMICAS = {
    1: 1.008,
    2: 4.0026,
    3: 6.94,
    4: 9.0122,
    5: 10.81,
    6: 12.011,
    7: 14.007,
    8: 15.999,
    9: 18.998,
    10: 20.180,
    11: 22.990,
    12: 24.305,
    13: 26.982,
    14: 28.085,
    15: 30.974,
    16: 32.06,
    17: 35.45,
    18: 39.948,
    19: 39.098,
    20: 40.078,
    21: 44.956,
    22: 47.867,
    23: 50.942,
    24: 51.996,
    25: 54.938,
    26: 55.845,
    27: 58.933,
    28: 58.693,
    29: 63.546,
    30: 65.38,
    31: 69.723,
    32: 72.63,
    33: 74.922,
    34: 78.971,
    35: 79.904,
    36: 83.798,
    37: 85.468,
    38: 87.62,
    39: 88.906,
    40: 91.224,
    41: 92.906,
    42: 95.95,
    43: 98,
    44: 101.07,
    45: 102.91,
    46: 106.42,
    47: 107.87,
    48: 112.41,
    49: 114.82,
    50: 118.71,
    51: 121.76,
    52: 127.60,
    53: 126.90,
    54: 131.29,
    55: 132.91,
    56: 137.33,
    57: 138.91,
    58: 140.12,
    59: 140.91,
    60: 144.24,
    61: 145,
    62: 150.36,
    63: 151.96,
    64: 157.25,
    65: 158.93,
    66: 162.50,
    67: 164.93,
    68: 167.26,
    69: 168.93,
    70: 173.05,
    71: 174.97,
    72: 178.49,
    73: 180.95,
    74: 183.84,
    75: 186.21,
    76: 190.23,
    77: 192.22,
    78: 195.08,
    79: 196.97,
    80: 200.59,
    81: 204.38,
    82: 207.2,
    83: 208.98,
    84: 209,
    85: 210,
    86: 222,
    87: 223,
    88: 226,
    89: 227,
    90: 232.04,
    91: 231.04,
    92: 238.03,
    93: 237,
    94: 244,
    95: 243,
    96: 247,
    97: 247,
    98: 251,
    99: 252,
    100: 257,
    101: 258,
    102: 259,
    103: 266,
    104: 267,
    105: 270,
    106: 271,
    107: 270,
    108: 277,
    109: 278,
    110: 281,
    111: 282,
    112: 285,
    113: 286,
    114: 289,
    115: 289,
    116: 293,
    117: 294,
    118: 294,
}

ELEMENTOS_POR_POSICAO = {
    (elem["period"], elem["group"]): elem
    for elem in ELEMENTOS
    if elem["group"] is not None
}

LANTANIDEOS = [elem for elem in ELEMENTOS if elem["categoria"] == "Lantanídeo"]
ACTINIDEOS = [elem for elem in ELEMENTOS if elem["categoria"] == "Actinídeo"]
DATA_FILE = Path("dados_tabela.json")


def load_app_data():
    if not DATA_FILE.exists():
        return {"elementos_falados": set(), "videos": {}}

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        videos = {int(z): itens for z, itens in data.get("videos", {}).items()}
        elementos_falados = set(data.get("elementos_falados", []))
        return {"elementos_falados": elementos_falados, "videos": videos}
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return {"elementos_falados": set(), "videos": {}}


def save_app_data():
    data = {
        "elementos_falados": sorted(st.session_state.elementos_falados),
        "videos": {str(z): itens for z, itens in st.session_state.videos.items()},
    }
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


dados_iniciais = load_app_data()

if "elementos_falados" not in st.session_state:
    st.session_state.elementos_falados = dados_iniciais["elementos_falados"]

if "videos" not in st.session_state:
    st.session_state.videos = dados_iniciais["videos"]

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False


def get_admin_password():
    try:
        senha_secrets = st.secrets.get("ADMIN_PASSWORD", "")
    except Exception:
        senha_secrets = ""

    return os.getenv("ADMIN_PASSWORD") or senha_secrets


ADMIN_PASSWORD = get_admin_password()
IS_ADMIN = bool(ADMIN_PASSWORD) and st.session_state.admin_autenticado

if not IS_ADMIN:
    dados_atualizados = load_app_data()
    st.session_state.elementos_falados = dados_atualizados["elementos_falados"]
    st.session_state.videos = dados_atualizados["videos"]


def toggle_elemento(z):
    if z in st.session_state.elementos_falados:
        st.session_state.elementos_falados.remove(z)
    else:
        st.session_state.elementos_falados.add(z)
    save_app_data()

st.markdown(
    """
    <style>
    .periodic-card {
        --cat-color: #f2f2f2;
        box-sizing: border-box;
        width: 100%;
        aspect-ratio: 1 / 1;
        min-height: 0;
        padding: 8px;
        border: 1px solid rgba(17, 24, 39, 0.14);
        border-radius: 8px;
        background:
            linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.24) 46%, rgba(255,255,255,0.05) 100%),
            var(--cat-color);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.10), inset 0 1px 0 rgba(255,255,255,0.72);
        display: grid;
        grid-template-rows: auto 1fr auto auto;
        align-items: center;
        gap: 2px;
        overflow: hidden;
        position: relative;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .periodic-card::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(120deg, rgba(255,255,255,0.42), rgba(255,255,255,0) 42%);
    }
    .periodic-card:hover {
        transform: translateY(-3px);
        border-color: rgba(17, 24, 39, 0.24);
        box-shadow: 0 16px 34px rgba(15, 23, 42, 0.16), inset 0 1px 0 rgba(255,255,255,0.8);
    }
    .periodic-cell { min-height: 0; }
    .periodic-symbol {
        color: #111827;
        font-size: 26px;
        font-weight: 900;
        line-height: 1;
        text-align: center;
        letter-spacing: 0;
    }
    .periodic-atomic {
        color: #111827;
        font-size: 11px;
        font-weight: 800;
        line-height: 1;
    }
    .periodic-mass {
        color: rgba(17, 24, 39, 0.68);
        font-size: 10px;
        font-variant-numeric: tabular-nums;
        line-height: 1;
    }
    .periodic-name {
        color: #111827;
        font-size: 11px;
        font-weight: 800;
        line-height: 1.1;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width: 100%;
    }
    .periodic-category {
        color: rgba(17, 24, 39, 0.72);
        font-size: 9px;
        font-weight: 700;
        line-height: 1.1;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width: 100%;
    }
    .periodic-info { display: flex; justify-content: space-between; align-items: center; width: 100%; }
    .categoria-badge { display: inline-block; padding: 5px 12px; border-radius: 999px; font-size: 11px; margin: 3px 3px 3px 0; }
    .table-header { font-weight: 700; color: #222; text-align: center; }
    .small-note { font-size: 13px; color: #555; }
    .video-box { border: 1px solid #e3e3e3; border-radius: 14px; padding: 16px; background: #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.04); }
    .video-box h3 { margin-top: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚛️ Tabela Periódica Interativa")
st.markdown("Uma tabela periódica completa com marcação por elemento e agregador de vídeos sem barra lateral.")
st.markdown("---")

controls_col, videos_col = st.columns([1.1, 0.95], gap="large")

with controls_col:
    st.subheader("🎮 Controles")
    if IS_ADMIN:
        st.success("Modo administrador ativo.")
        if st.button("Sair do modo administrador"):
            st.session_state.admin_autenticado = False
            st.rerun()
    elif ADMIN_PASSWORD:
        senha_digitada = st.text_input("Senha de administrador", type="password")
        if st.button("Entrar como administrador"):
            if hmac.compare_digest(senha_digitada, ADMIN_PASSWORD):
                st.session_state.admin_autenticado = True
                st.success("Acesso de edição liberado.")
                st.rerun()
            else:
                st.error("Senha incorreta.")
        st.info("Visitantes podem visualizar a tabela e os links, mas não podem editar.")
    else:
        st.warning("Defina ADMIN_PASSWORD para liberar edição com senha.")

    if IS_ADMIN and st.button("🔄 Resetar Elementos Falados"):
        st.session_state.elementos_falados = set()
        save_app_data()
        st.success("Progressão de estudo resetada!")

    total_elementos = len(ELEMENTOS)
    estudados = len(st.session_state.elementos_falados)
    st.metric("Elementos marcados", f"{estudados}/{total_elementos}")
    if total_elementos:
        st.progress(estudados / total_elementos)
        st.caption(f"Progresso: {estudados / total_elementos * 100:.0f}%")

    st.markdown("---")
    st.subheader("🎨 Legenda de Categorias")
    categoria_cols = st.columns([1, 1, 1])
    idx = 0
    for categoria, cor in CORES_CATEGORIA.items():
        with categoria_cols[idx % len(categoria_cols)]:
            st.markdown(
                f"<span class='categoria-badge' style='background:{cor}; color:#212121;'>{categoria}</span>",
                unsafe_allow_html=True,
            )
        idx += 1

with videos_col:
    st.subheader("📹 Agregador de Vídeos")
    elemento_selecionado = st.selectbox(
        "Selecione o elemento:",
        options=sorted(ELEMENTOS, key=lambda e: e["z"]),
        format_func=lambda e: f"{e['símbolo']} - {e['nome']}",
    )
    if IS_ADMIN:
        url_video = st.text_input("URL do vídeo", placeholder="https://www.youtube.com/watch?v=...", key="video_url_input")
        descricao_video = st.text_input("Descrição do vídeo", placeholder="Ex: Aula sobre o elemento", key="descricao_input")

        if st.button("➕ Adicionar vídeo", use_container_width=True):
            if url_video.strip() and descricao_video.strip():
                z = elemento_selecionado["z"]
                st.session_state.videos.setdefault(z, []).append(
                    {
                        "url": url_video.strip(),
                        "descricao": descricao_video.strip(),
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    }
                )
                save_app_data()
                st.success("Vídeo cadastrado com sucesso!")
            else:
                st.error("Preencha URL e descrição antes de adicionar.")
    else:
        st.caption("Modo visualização: os links cadastrados ficam disponíveis para consulta.")

    st.markdown("---")
    st.subheader("📚 Vídeos por elemento")
    z = elemento_selecionado["z"]
    if z in st.session_state.videos and st.session_state.videos[z]:
        for idx, video in enumerate(st.session_state.videos[z]):
            with st.expander(f"{video['descricao']}"):
                st.markdown(f"🔗 [Abrir vídeo]({video['url']})")
                st.caption(f"Adicionado em {video['data']}")
                if IS_ADMIN and st.button("Remover vídeo", key=f"del_{z}_{idx}"):
                    st.session_state.videos[z].pop(idx)
                    save_app_data()
                    st.rerun()
    else:
        st.info("Nenhum vídeo cadastrado para este elemento.")

st.markdown("---")
st.subheader("📊 Tabela Periódica Completa")

group_headers = [f"{i}" for i in range(1, 19)]
cols = st.columns(18, gap="small")
for index, header in enumerate(group_headers):
    with cols[index]:
        st.markdown(f"<div class='table-header'>{header}</div>", unsafe_allow_html=True)

for period in range(1, 8):
    cols = st.columns(18, gap="small")
    for group in range(1, 19):
        elem = ELEMENTOS_POR_POSICAO.get((period, group))
        with cols[group - 1]:
            if elem is None:
                st.markdown("<div style='aspect-ratio:1 / 1; width:100%;'></div>", unsafe_allow_html=True)
                continue

            marcado = elem["z"] in st.session_state.elementos_falados
            cor = CORES_CATEGORIA.get(elem["categoria"], "#f2f2f2")
            opacidade = "0.55" if marcado else "1"
            decoracao = "line-through" if marcado else "none"
            texto = f"<div class='periodic-card periodic-cell' style='--cat-color:{cor}; opacity:{opacidade};'>"
            texto += f"<div class='periodic-info'><span class='periodic-atomic'>{elem['z']}</span><span class='periodic-mass'>{MASSAS_ATOMICAS.get(elem['z'], '')}</span></div>"
            texto += f"<div><span class='periodic-symbol'>{elem['símbolo']}</span></div>"
            texto += f"<div class='periodic-name'>{elem['nome']}</div>"
            texto += f"<div class='periodic-category' style='text-decoration:{decoracao};'>{elem['categoria']}</div>"
            texto += "</div>"
            st.markdown(texto, unsafe_allow_html=True)
            if IS_ADMIN:
                label = "Desmarcar" if marcado else "Marcar"
                if st.button(label, key=f"mark_{elem['z']}", on_click=toggle_elemento, args=(elem['z'],), use_container_width=True):
                    pass

st.markdown("---")
if LANTANIDEOS:
    st.subheader("🎓 Lantanídeos")
    cols = st.columns(15, gap="small")
    for index, elem in enumerate(LANTANIDEOS):
        with cols[index]:
            marcado = elem["z"] in st.session_state.elementos_falados
            cor = CORES_CATEGORIA.get(elem["categoria"], "#f2f2f2")
            opacidade = "0.55" if marcado else "1"
            decoracao = "line-through" if marcado else "none"
            texto = f"<div class='periodic-card periodic-cell' style='--cat-color:{cor}; opacity:{opacidade};'>"
            texto += f"<div class='periodic-info'><span class='periodic-atomic'>{elem['z']}</span><span class='periodic-mass'>{MASSAS_ATOMICAS.get(elem['z'], '')}</span></div>"
            texto += f"<div><span class='periodic-symbol'>{elem['símbolo']}</span></div>"
            texto += f"<div class='periodic-name'>{elem['nome']}</div>"
            texto += f"<div class='periodic-category' style='text-decoration:{decoracao};'>{elem['categoria']}</div>"
            texto += "</div>"
            st.markdown(texto, unsafe_allow_html=True)
            if IS_ADMIN:
                label = "Desmarcar" if marcado else "Marcar"
                if st.button(label, key=f"lanth_{elem['z']}", on_click=toggle_elemento, args=(elem['z'],), use_container_width=True):
                    pass

if ACTINIDEOS:
    st.subheader("🎓 Actinídeos")
    cols = st.columns(15, gap="small")
    for index, elem in enumerate(ACTINIDEOS):
        with cols[index]:
            marcado = elem["z"] in st.session_state.elementos_falados
            cor = CORES_CATEGORIA.get(elem["categoria"], "#f2f2f2")
            opacidade = "0.55" if marcado else "1"
            decoracao = "line-through" if marcado else "none"
            texto = f"<div class='periodic-card periodic-cell' style='--cat-color:{cor}; opacity:{opacidade};'>"
            texto += f"<div class='periodic-info'><span class='periodic-atomic'>{elem['z']}</span><span class='periodic-mass'>{MASSAS_ATOMICAS.get(elem['z'], '')}</span></div>"
            texto += f"<div><span class='periodic-symbol'>{elem['símbolo']}</span></div>"
            texto += f"<div class='periodic-name'>{elem['nome']}</div>"
            texto += f"<div class='periodic-category' style='text-decoration:{decoracao};'>{elem['categoria']}</div>"
            texto += "</div>"
            st.markdown(texto, unsafe_allow_html=True)
            if IS_ADMIN:
                label = "Desmarcar" if marcado else "Marcar"
                if st.button(label, key=f"act_{elem['z']}", on_click=toggle_elemento, args=(elem['z'],), use_container_width=True):
                    pass

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#555; font-size:13px;'>Tabela periódica completa com marcação interativa e agregador de vídeos.</div>",
    unsafe_allow_html=True,
)
