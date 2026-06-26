import hmac
import html
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
DEFAULT_ADMIN_PASSWORD = "admin"


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

if "elemento_video_z" not in st.session_state:
    st.session_state.elemento_video_z = 1

query_elemento_video = st.query_params.get("elemento_video")
if query_elemento_video:
    try:
        elemento_video_z = int(query_elemento_video)
    except ValueError:
        elemento_video_z = st.session_state.elemento_video_z

    if elemento_video_z in {elem["z"] for elem in ELEMENTOS}:
        st.session_state.elemento_video_z = elemento_video_z


def clean_secret(value):
    if value is None:
        return ""
    return str(value).strip()


def get_admin_password():
    candidates = [os.getenv("ADMIN_PASSWORD"), os.getenv("admin_password")]

    try:
        candidates.append(st.secrets.get("ADMIN_PASSWORD", ""))
        candidates.append(st.secrets.get("admin_password", ""))

        admin_section = st.secrets.get("admin", {})
        if hasattr(admin_section, "get"):
            candidates.append(admin_section.get("password", ""))
            candidates.append(admin_section.get("ADMIN_PASSWORD", ""))
    except Exception:
        pass

    for candidate in candidates:
        password = clean_secret(candidate)
        if password:
            return password

    return DEFAULT_ADMIN_PASSWORD


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


def selecionar_elemento_video(z):
    st.session_state.elemento_video_z = z
    st.query_params["elemento_video"] = str(z)


def elemento_tem_videos(z):
    return bool(st.session_state.videos.get(z))


def elementos_contabilizados():
    elementos_com_videos = {
        int(z)
        for z, videos in st.session_state.videos.items()
        if videos
    }
    return set(st.session_state.elementos_falados) | elementos_com_videos


def sincronizar_elementos_com_videos():
    st.session_state.elementos_falados = elementos_contabilizados()


sincronizar_elementos_com_videos()


def render_element_card(elem):
    marcado = elem["z"] in elementos_contabilizados()
    cor = CORES_CATEGORIA.get(elem["categoria"], "#f2f2f2")
    rgb = hex_to_rgb(cor)
    brilho_forte = f"rgba({rgb}, 0.72)"
    brilho_medio = f"rgba({rgb}, 0.48)"
    brilho_suave = f"rgba({rgb}, 0.26)"
    marcado_class = " is-marked" if marcado else ""
    title = html.escape(
        f"{elem['z']} - {elem['nome']} ({elem['símbolo']}) | {elem['categoria']} | Massa {MASSAS_ATOMICAS.get(elem['z'], '')}"
    )
    card_style = (
        f"--cat-color:{cor}; --cat-rgb:{rgb}; "
        f"border-color:{brilho_forte}; "
        f"background:radial-gradient(circle at 50% 18%, {brilho_medio} 0%, {brilho_suave} 38%, rgba(255,255,255,0) 74%), "
        "linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.24) 46%, rgba(255,255,255,0.05) 100%), "
        f"{cor}; "
        f"box-shadow:0 0 0 2px {brilho_forte}, 0 0 26px {brilho_medio}, 0 10px 24px rgba(15, 23, 42, 0.10), inset 0 0 22px {brilho_suave}, inset 0 1px 0 rgba(255,255,255,0.72);"
    )

    return (
        f"<a class='periodic-card{marcado_class}' href='?elemento_video={elem['z']}' style='{card_style}' title='{title}'>"
        f"<span class='periodic-glow-strip' style='background:{brilho_forte}; box-shadow:0 0 18px {brilho_forte};'></span>"
        f"<div class='periodic-atomic'>{elem['z']}</div>"
        f"<div class='periodic-symbol'>{html.escape(elem['símbolo'])}</div>"
        f"<div class='periodic-name'>{html.escape(elem['nome'])}</div>"
        "</a>"
    )


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "242, 242, 242"

    try:
        return ", ".join(str(int(hex_color[index:index + 2], 16)) for index in (0, 2, 4))
    except ValueError:
        return "242, 242, 242"


def render_periodic_grid(rows, columns, lookup):
    cells = []
    for header in range(1, columns + 1):
        cells.append(f"<div class='table-header'>{header}</div>")

    for row in rows:
        for column in range(1, columns + 1):
            elem = lookup.get((row, column))
            if elem is None:
                cells.append("<div class='periodic-empty'></div>")
            else:
                cells.append(render_element_card(elem))

    return (
        "<div class='periodic-table-shell'>"
        f"<div class='periodic-grid' style='--columns:{columns};'>"
        f"{''.join(cells)}"
        "</div>"
        "</div>"
    )


def render_series_grid(elementos):
    cells = [render_element_card(elem) for elem in elementos]
    return (
        "<div class='periodic-table-shell'>"
        f"<div class='periodic-grid series-grid' style='--columns:{len(elementos)};'>"
        f"{''.join(cells)}"
        "</div>"
        "</div>"
    )


def render_video_shortcut_buttons(rows, columns, lookup, key_prefix):
    for row in rows:
        cols = st.columns(columns, gap="small")
        for column in range(1, columns + 1):
            elem = lookup.get((row, column))
            with cols[column - 1]:
                if elem is None:
                    st.markdown("<div style='height:38px;'></div>", unsafe_allow_html=True)
                    continue

                marcado = elem["z"] in st.session_state.elementos_falados
                tem_videos = elemento_tem_videos(elem["z"])
                is_selected = elem["z"] == st.session_state.elemento_video_z
                if st.button(
                    elem["símbolo"],
                    key=f"{key_prefix}_{elem['z']}",
                    help=(
                        f"Mostrar vídeos de {elem['nome']}"
                        if marcado
                        else f"Marque {elem['nome']} para liberar o vídeo"
                    ),
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                    disabled=not (marcado or tem_videos),
                ):
                    selecionar_elemento_video(elem["z"])
                    st.rerun()


def render_series_video_shortcuts(elementos, key_prefix):
    cols = st.columns(len(elementos), gap="small")
    for index, elem in enumerate(elementos):
        with cols[index]:
            marcado = elem["z"] in st.session_state.elementos_falados
            tem_videos = elemento_tem_videos(elem["z"])
            is_selected = elem["z"] == st.session_state.elemento_video_z
            if st.button(
                elem["símbolo"],
                key=f"{key_prefix}_{elem['z']}",
                help=(
                    f"Mostrar vídeos de {elem['nome']}"
                    if marcado
                    else f"Marque {elem['nome']} para liberar o vídeo"
                ),
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                disabled=not (marcado or tem_videos),
            ):
                selecionar_elemento_video(elem["z"])
                st.rerun()


def formatar_botao_elemento(elem):
    return f"{elem['z']}  \n{elem['símbolo']}  \n{elem['nome']}"


def render_element_button(elem, key_prefix):
    marcado = elem["z"] in elementos_contabilizados()
    is_selected = elem["z"] == st.session_state.elemento_video_z
    status = "Marcado" if marcado else "Nao marcado"
    help_text = f"{elem['nome']} - {status}."

    if st.button(
        formatar_botao_elemento(elem),
        key=f"{key_prefix}_{elem['z']}",
        help=help_text,
        use_container_width=True,
        type="primary" if is_selected else "secondary",
    ):
        selecionar_elemento_video(elem["z"])
        st.rerun()


def render_periodic_button_grid(rows, columns, lookup, key_prefix):
    header_cols = st.columns(columns, gap="small")
    for index, col in enumerate(header_cols, start=1):
        col.markdown(f"<div class='table-header'>{index}</div>", unsafe_allow_html=True)

    for row in rows:
        cols = st.columns(columns, gap="small")
        for column in range(1, columns + 1):
            elem = lookup.get((row, column))
            with cols[column - 1]:
                if elem is None:
                    st.markdown("<div class='periodic-empty-button'></div>", unsafe_allow_html=True)
                else:
                    render_element_button(elem, key_prefix)


def render_series_button_grid(elementos, key_prefix):
    cols = st.columns(len(elementos), gap="small")
    for index, elem in enumerate(elementos):
        with cols[index]:
            render_element_button(elem, key_prefix)


def render_video_button_css():
    rules = []
    key_prefixes = ("periodic_main", "periodic_lanth", "periodic_act")
    elements_with_videos = [z for z, videos in st.session_state.videos.items() if videos]

    for z in elements_with_videos:
        selectors = ",\n".join(
            selector
            for key_prefix in key_prefixes
            for selector in (
                f".st-key-{key_prefix}_{z} button",
                f".st-key-{key_prefix.replace('_', '-')}-{z} button",
            )
        )
        text_selectors = ",\n".join(f"{selector} p" for selector in selectors.split(",\n"))
        rules.append(
            f"""
            {selectors} {{
                background: linear-gradient(145deg, #dffcf4 0%, #9eead9 100%) !important;
                border-color: #14b8a6 !important;
                color: #064e3b !important;
                box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.22), 0 8px 18px rgba(15, 118, 110, 0.16) !important;
            }}
            {text_selectors} {{
                color: #064e3b !important;
                font-weight: 800;
            }}
            """
        )

    return "\n".join(rules)


def render_selected_button_css():
    if "elemento_video_z" not in st.session_state:
        return ""

    z = st.session_state.elemento_video_z
    key_prefixes = ("periodic_main", "periodic_lanth", "periodic_act")
    selectors = ",\n".join(
        selector
        for key_prefix in key_prefixes
        for selector in (
            f".st-key-{key_prefix}_{z} button",
            f".st-key-{key_prefix.replace('_', '-')}-{z} button",
        )
    )
    text_selectors = ",\n".join(f"{selector} p" for selector in selectors.split(",\n"))

    return f"""
    {selectors} {{
        background: #e53935 !important;
        border-color: #c62828 !important;
        color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(229, 57, 53, 0.24), 0 8px 18px rgba(198, 40, 40, 0.22) !important;
    }}
    {text_selectors} {{
        color: #ffffff !important;
    }}
    """


st.markdown(
    """
    <style>
    .block-container {
        max-width: 1800px;
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    #MainMenu,
    header,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    .periodic-table-shell {
        width: 100%;
        overflow-x: auto;
        padding: 4px 2px 14px;
    }
    .periodic-grid {
        --cell-min: 72px;
        display: grid;
        grid-template-columns: repeat(var(--columns), minmax(var(--cell-min), 1fr));
        gap: 6px;
        min-width: calc(var(--columns) * var(--cell-min) + (var(--columns) - 1) * 6px);
        align-items: stretch;
    }
    .series-grid {
        --cell-min: 76px;
    }
    .periodic-card {
        --cat-color: #f2f2f2;
        box-sizing: border-box;
        width: 100%;
        min-height: 92px;
        height: 100%;
        padding: 7px 6px;
        border: 1px solid rgba(17, 24, 39, 0.14);
        border-radius: 8px;
        background:
            radial-gradient(circle at 50% 18%, rgba(var(--cat-rgb), 0.52) 0%, rgba(var(--cat-rgb), 0.24) 36%, rgba(var(--cat-rgb), 0) 72%),
            linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.24) 46%, rgba(255,255,255,0.05) 100%),
            var(--cat-color);
        box-shadow:
            0 0 0 2px rgba(var(--cat-rgb), 0.52),
            0 0 20px rgba(var(--cat-rgb), 0.48),
            0 10px 24px rgba(15, 23, 42, 0.10),
            inset 0 0 18px rgba(var(--cat-rgb), 0.42),
            inset 0 1px 0 rgba(255,255,255,0.72);
        display: grid;
        grid-template-rows: 16px 36px 18px;
        align-items: center;
        gap: 3px;
        overflow: hidden;
        position: relative;
        color: inherit;
        text-decoration: none;
        cursor: pointer;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .periodic-card:visited,
    .periodic-card:hover,
    .periodic-card:active {
        color: inherit;
        text-decoration: none;
    }
    .periodic-card::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        border-radius: inherit;
        background:
            linear-gradient(120deg, rgba(255,255,255,0.42), rgba(255,255,255,0) 42%),
            linear-gradient(180deg, rgba(var(--cat-rgb), 0.28), rgba(var(--cat-rgb), 0) 58%);
    }
    .periodic-card::before {
        content: "";
        position: absolute;
        inset: 4px;
        pointer-events: none;
        border-radius: 6px;
        border: 1px solid rgba(var(--cat-rgb), 0.58);
        box-shadow: inset 0 0 14px rgba(var(--cat-rgb), 0.42);
    }
    .periodic-glow-strip {
        position: absolute;
        top: 5px;
        left: 7px;
        right: 7px;
        height: 4px;
        border-radius: 999px;
        opacity: 0.9;
        pointer-events: none;
        z-index: 1;
    }
    .periodic-symbol,
    .periodic-name,
    .periodic-atomic {
        position: relative;
        z-index: 2;
    }
    .periodic-card:hover {
        transform: translateY(-3px);
        border-color: rgba(17, 24, 39, 0.24);
        box-shadow:
            0 0 0 3px rgba(var(--cat-rgb), 0.72),
            0 0 32px rgba(var(--cat-rgb), 0.68),
            0 16px 34px rgba(15, 23, 42, 0.16),
            inset 0 0 22px rgba(var(--cat-rgb), 0.54),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    .periodic-card.is-marked {
        opacity: 0.58;
    }
    .periodic-card.is-marked .periodic-name {
        text-decoration: line-through;
    }
    .periodic-empty {
        min-height: 92px;
        border: 1px dashed rgba(15, 23, 42, 0.08);
        border-radius: 8px;
        background: rgba(255,255,255,0.24);
    }
    .periodic-empty-button {
        min-height: 92px;
    }
    .st-key-periodic_main_grid,
    .st-key-periodic-main-grid {
        zoom: 0.78;
        transform-origin: top left;
    }
    .st-key-periodic_lanth_grid,
    .st-key-periodic_act_grid,
    .st-key-periodic-lanth-grid,
    .st-key-periodic-act-grid {
        zoom: 0.86;
        transform-origin: top left;
    }
    .st-key-periodic_main_grid [data-testid="stButton"] > button,
    .st-key-periodic_lanth_grid [data-testid="stButton"] > button,
    .st-key-periodic_act_grid [data-testid="stButton"] > button,
    .st-key-periodic-main-grid [data-testid="stButton"] > button,
    .st-key-periodic-lanth-grid [data-testid="stButton"] > button,
    .st-key-periodic-act-grid [data-testid="stButton"] > button {
        min-height: 108px;
        height: 108px;
        padding: 7px 5px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        white-space: pre-line;
        line-height: 1.12;
        overflow: hidden;
    }
    .st-key-periodic_main_grid [data-testid="stButton"] > button *,
    .st-key-periodic_lanth_grid [data-testid="stButton"] > button *,
    .st-key-periodic_act_grid [data-testid="stButton"] > button *,
    .st-key-periodic-main-grid [data-testid="stButton"] > button *,
    .st-key-periodic-lanth-grid [data-testid="stButton"] > button *,
    .st-key-periodic-act-grid [data-testid="stButton"] > button * {
        white-space: pre-line;
    }
    .st-key-periodic_main_grid [data-testid="stButton"] > button p,
    .st-key-periodic_lanth_grid [data-testid="stButton"] > button p,
    .st-key-periodic_act_grid [data-testid="stButton"] > button p,
    .st-key-periodic-main-grid [data-testid="stButton"] > button p,
    .st-key-periodic-lanth-grid [data-testid="stButton"] > button p,
    .st-key-periodic-act-grid [data-testid="stButton"] > button p {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: pre-line;
        width: 100%;
        margin: 0;
        font-size: 0.72rem;
        line-height: 1.12;
        text-align: center;
    }
    .st-key-periodic_main_grid [data-testid="stButton"] > button p::first-line,
    .st-key-periodic_lanth_grid [data-testid="stButton"] > button p::first-line,
    .st-key-periodic_act_grid [data-testid="stButton"] > button p::first-line,
    .st-key-periodic-main-grid [data-testid="stButton"] > button p::first-line,
    .st-key-periodic-lanth-grid [data-testid="stButton"] > button p::first-line,
    .st-key-periodic-act-grid [data-testid="stButton"] > button p::first-line {
        font-size: 0.82rem;
        font-weight: 800;
    }
    .periodic-symbol {
        color: #111827;
        font-size: 25px;
        font-weight: 900;
        line-height: 1;
        text-align: center;
        letter-spacing: 0;
    }
    .periodic-atomic {
        color: #111827;
        font-size: 12px;
        font-weight: 800;
        line-height: 1;
        font-variant-numeric: tabular-nums;
        text-align: center;
    }
    .periodic-name {
        color: #111827;
        font-size: 10px;
        font-weight: 800;
        line-height: 1.1;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width: 100%;
    }
    .table-header { font-weight: 700; color: #222; text-align: center; min-height: 20px; }
    .small-note { font-size: 13px; color: #555; }
    .video-box { border: 1px solid #e3e3e3; border-radius: 14px; padding: 16px; background: #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.04); }
    .video-box h3 { margin-top: 0; }
    @media (max-width: 900px) {
        .block-container {
            padding-left: 0.45rem;
            padding-right: 0.45rem;
            padding-top: 1rem;
        }
        .block-container [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
        }
        .block-container [data-testid="column"],
        .block-container [data-testid="stColumn"] {
            flex: 1 1 100%;
            min-width: 100%;
            width: 100%;
        }
        .st-key-periodic_main_grid,
        .st-key-periodic-main-grid,
        .st-key-periodic_lanth_grid,
        .st-key-periodic_act_grid,
        .st-key-periodic-lanth-grid,
        .st-key-periodic-act-grid {
            zoom: 1;
            overflow-x: auto;
            overflow-y: hidden;
            padding: 2px 0 12px;
            -webkit-overflow-scrolling: touch;
        }
        .st-key-periodic_main_grid [data-testid="stHorizontalBlock"],
        .st-key-periodic-main-grid [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap;
            min-width: 1188px;
            gap: 4px;
        }
        .st-key-periodic_lanth_grid [data-testid="stHorizontalBlock"],
        .st-key-periodic_act_grid [data-testid="stHorizontalBlock"],
        .st-key-periodic-lanth-grid [data-testid="stHorizontalBlock"],
        .st-key-periodic-act-grid [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap;
            min-width: 1015px;
            gap: 4px;
        }
        .st-key-periodic_main_grid [data-testid="column"],
        .st-key-periodic-main-grid [data-testid="column"],
        .st-key-periodic_lanth_grid [data-testid="column"],
        .st-key-periodic_act_grid [data-testid="column"],
        .st-key-periodic-lanth-grid [data-testid="column"],
        .st-key-periodic-act-grid [data-testid="column"],
        .st-key-periodic_main_grid [data-testid="stColumn"],
        .st-key-periodic-main-grid [data-testid="stColumn"],
        .st-key-periodic_lanth_grid [data-testid="stColumn"],
        .st-key-periodic_act_grid [data-testid="stColumn"],
        .st-key-periodic-lanth-grid [data-testid="stColumn"],
        .st-key-periodic-act-grid [data-testid="stColumn"] {
            flex: 0 0 62px;
            min-width: 62px;
            width: 62px;
        }
        .st-key-periodic_main_grid [data-testid="stButton"] > button,
        .st-key-periodic_lanth_grid [data-testid="stButton"] > button,
        .st-key-periodic_act_grid [data-testid="stButton"] > button,
        .st-key-periodic-main-grid [data-testid="stButton"] > button,
        .st-key-periodic-lanth-grid [data-testid="stButton"] > button,
        .st-key-periodic-act-grid [data-testid="stButton"] > button {
            min-height: 92px;
            height: 92px;
            padding: 5px 3px;
            border-radius: 7px;
        }
        .st-key-periodic_main_grid [data-testid="stButton"] > button p,
        .st-key-periodic_lanth_grid [data-testid="stButton"] > button p,
        .st-key-periodic_act_grid [data-testid="stButton"] > button p,
        .st-key-periodic-main-grid [data-testid="stButton"] > button p,
        .st-key-periodic-lanth-grid [data-testid="stButton"] > button p,
        .st-key-periodic-act-grid [data-testid="stButton"] > button p {
            font-size: 0.62rem;
            line-height: 1.08;
            word-break: break-word;
            overflow-wrap: anywhere;
        }
        .st-key-periodic_main_grid [data-testid="stButton"] > button p::first-line,
        .st-key-periodic_lanth_grid [data-testid="stButton"] > button p::first-line,
        .st-key-periodic_act_grid [data-testid="stButton"] > button p::first-line,
        .st-key-periodic-main-grid [data-testid="stButton"] > button p::first-line,
        .st-key-periodic-lanth-grid [data-testid="stButton"] > button p::first-line,
        .st-key-periodic-act-grid [data-testid="stButton"] > button p::first-line {
            font-size: 0.72rem;
        }
        .periodic-empty-button {
            min-height: 92px;
        }
        .table-header {
            font-size: 11px;
            min-height: 16px;
        }
        .periodic-grid {
            --cell-min: 66px;
            gap: 5px;
        }
        .periodic-card,
        .periodic-empty {
            min-height: 86px;
        }
        .periodic-card {
            grid-template-rows: 14px 33px 17px;
            padding: 6px 5px;
        }
        .periodic-symbol {
            font-size: 23px;
        }
        .periodic-name {
            font-size: 9.5px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"<style>{render_video_button_css()}</style>", unsafe_allow_html=True)
st.markdown(f"<style>{render_selected_button_css()}</style>", unsafe_allow_html=True)

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
            if hmac.compare_digest(clean_secret(senha_digitada), ADMIN_PASSWORD):
                st.session_state.admin_autenticado = True
                st.success("Acesso de edição liberado.")
                st.rerun()
            else:
                st.error("Senha incorreta.")
        st.info("Digite a senha para liberar edição e cadastro de vídeos.")
    else:
        st.warning("Defina ADMIN_PASSWORD para liberar edição com senha.")

    if IS_ADMIN and st.button("🔄 Resetar Elementos Falados"):
        st.session_state.elementos_falados = set()
        save_app_data()
        st.success("Progressão de estudo resetada!")

    total_elementos = len(ELEMENTOS)
    estudados = len(elementos_contabilizados())
    st.metric("Elementos marcados", f"{estudados}/{total_elementos}")
    if total_elementos:
        st.progress(estudados / total_elementos)
        st.caption(f"Progresso: {estudados / total_elementos * 100:.0f}%")

    if IS_ADMIN:
        st.markdown("---")
        elemento_para_marcar = st.selectbox(
            "Marcar ou desmarcar elemento:",
            options=sorted(ELEMENTOS, key=lambda e: e["z"]),
            format_func=lambda e: f"{e['z']} - {e['símbolo']} | {e['nome']}",
            key="elemento_marcacao_input",
        )
        ja_marcado = elemento_para_marcar["z"] in st.session_state.elementos_falados
        acao_label = "Desmarcar elemento" if ja_marcado else "Marcar elemento"
        if st.button(acao_label, use_container_width=True):
            toggle_elemento(elemento_para_marcar["z"])
            st.rerun()

with videos_col:
    st.markdown("<div id='videos'></div>", unsafe_allow_html=True)
    st.subheader("📹 Agregador de Vídeos")
    elementos_ordenados = sorted(ELEMENTOS, key=lambda e: e["z"])
    selected_index = next(
        (
            index
            for index, elem in enumerate(elementos_ordenados)
            if elem["z"] == st.session_state.elemento_video_z
        ),
        0,
    )

    elemento_selecionado = st.selectbox(
        "Buscar elemento:",
        options=elementos_ordenados,
        index=selected_index,
        key=f"elemento_video_select_{st.session_state.elemento_video_z}",
        format_func=lambda e: f"{e['símbolo']} - {e['nome']}",
    )
    if st.session_state.elemento_video_z != elemento_selecionado["z"]:
        selecionar_elemento_video(elemento_selecionado["z"])
    st.caption(
        f"Vídeos exibidos para {elemento_selecionado['símbolo']} - {elemento_selecionado['nome']}."
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
                st.session_state.elementos_falados.add(z)
                save_app_data()
                st.success("Vídeo cadastrado com sucesso!")
            else:
                st.error("Preencha URL e descrição antes de adicionar.")
    else:
        st.caption("Modo visualização: os vídeos cadastrados ficam disponíveis para assistir aqui.")

    st.markdown("---")
    st.subheader("📚 Vídeos por elemento")
    z = elemento_selecionado["z"]
    if z in st.session_state.videos and st.session_state.videos[z]:
        for idx, video in enumerate(st.session_state.videos[z]):
            st.markdown(f"**{html.escape(video['descricao'])}**")
            st.video(video["url"])
            st.caption(f"Adicionado em {video['data']}")
            if IS_ADMIN and st.button("Remover vídeo", key=f"del_{z}_{idx}"):
                st.session_state.videos[z].pop(idx)
                save_app_data()
                st.rerun()
    else:
        st.info("Nenhum vídeo cadastrado para este elemento.")

st.markdown("---")
st.subheader("📊 Tabela Periódica Completa")

with st.container(key="periodic_main_grid"):
    render_periodic_button_grid(range(1, 8), 18, ELEMENTOS_POR_POSICAO, "periodic_main")
st.caption("Clique em um elemento da tabela para mudar a busca e mostrar os vídeos no agregador.")

st.markdown("---")
if LANTANIDEOS:
    st.subheader("🎓 Lantanídeos")
    with st.container(key="periodic_lanth_grid"):
        render_series_button_grid(LANTANIDEOS, "periodic_lanth")

if ACTINIDEOS:
    st.subheader("🎓 Actinídeos")
    with st.container(key="periodic_act_grid"):
        render_series_button_grid(ACTINIDEOS, "periodic_act")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#555; font-size:13px;'>Tabela periódica completa com marcação interativa e agregador de vídeos.</div>",
    unsafe_allow_html=True,
)
