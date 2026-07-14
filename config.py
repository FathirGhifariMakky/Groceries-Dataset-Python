"""
==========================================================
config.py

Konfigurasi Aplikasi
Market Basket Analysis Menggunakan Algoritma Apriori

Penulisan Ilmiah
Universitas Gunadarma
==========================================================
"""

# ==========================================================
# INFORMASI APLIKASI
# ==========================================================

APP_TITLE = "Market Basket Analysis"

APP_SUBTITLE = """
Implementasi Algoritma Apriori
untuk menemukan pola pembelian konsumen
menggunakan Groceries Dataset.
"""

PROJECT_NAME = "Market Basket Analysis Menggunakan Algoritma Apriori"

APP_VERSION = "2.0.0"

AUTHOR = "Fathir"

UNIVERSITY = "Universitas Gunadarma"

YEAR = "2026"

# ==========================================================
# STREAMLIT
# ==========================================================

PAGE_TITLE = APP_TITLE

PAGE_ICON = ""

PAGE_LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ==========================================================
# DATASET
# ==========================================================

DEFAULT_DATASET = "Groceries_dataset.csv"

SUPPORTED_FILE_TYPES = ["csv"]

# ==========================================================
# NAMA KOLOM DATASET
# ==========================================================

MEMBER_COL = "Member_number"

DATE_COL = "Date"

ITEM_COL = "itemDescription"

# ==========================================================
# PARAMETER APRIORI
# ==========================================================

DEFAULT_MIN_SUPPORT = 0.01

DEFAULT_MIN_CONFIDENCE = 0.10

DEFAULT_MAX_LEN = 2

# ==========================================================
# BATAS INPUT
# ==========================================================

MIN_SUPPORT_LIMIT = 0.001

MAX_SUPPORT_LIMIT = 1.000

MIN_CONFIDENCE_LIMIT = 0.01

MAX_CONFIDENCE_LIMIT = 1.00

MIN_ITEMSET = 2

MAX_ITEMSET = 5

# ==========================================================
# VISUALISASI
# ==========================================================

TOP_N_PRODUCTS = 10

NETWORK_MAX_RULES = 20

HISTOGRAM_BINS = 20

FIGURE_WIDTH = 10

FIGURE_HEIGHT = 6

# ==========================================================
# DOWNLOAD
# ==========================================================

DATASET_DOWNLOAD_NAME = "dataset.csv"

ITEMSET_DOWNLOAD_NAME = "frequent_itemsets.csv"

RULES_DOWNLOAD_NAME = "association_rules.csv"

RECOMMENDATION_DOWNLOAD_NAME = "recommendation.csv"

# ==========================================================
# MENU NAVIGASI
# ==========================================================

MENU_DASHBOARD = "Dashboard"

MENU_DATASET = "Dataset"

MENU_ITEMSET = "Frequent Itemset"

MENU_RULES = "Association Rules"

MENU_VISUALIZATION = "Visualisasi"

MENU_RECOMMENDATION = "Rekomendasi"

MENU_ABOUT = "Tentang"

MENU_LIST = [

    MENU_DASHBOARD,

    MENU_DATASET,

    MENU_ITEMSET,

    MENU_RULES,

    MENU_VISUALIZATION,

    MENU_RECOMMENDATION,

    MENU_ABOUT

]

# ==========================================================
# SESSION STATE
# ==========================================================

SESSION_KEYS = {

    "analysis_done": False,

    "dataset": None,

    "dataset_info": None,

    "basket": None,

    "frequent_itemsets": None,

    "rules": None,

    "execution_time": 0

}

# ==========================================================
# PESAN
# ==========================================================

MSG_ANALYSIS_SUCCESS = "Analisis berhasil diselesaikan."

MSG_ANALYSIS_EMPTY = "Silakan jalankan analisis terlebih dahulu."

MSG_NO_RULE = "Tidak ditemukan Association Rules."

MSG_NO_RECOMMENDATION = "Tidak ada rekomendasi untuk produk tersebut."

# ==========================================================
# WARNA (Opsional)
# ==========================================================

PRIMARY_COLOR = "#1E88E5"

SUCCESS_COLOR = "#43A047"

WARNING_COLOR = "#FB8C00"

ERROR_COLOR = "#E53935"