"""
==========================================================
utils.py

Fungsi-fungsi utama untuk proses
Market Basket Analysis menggunakan Algoritma Apriori

Penulisan Ilmiah
Universitas Gunadarma
==========================================================
"""

# ==========================================================
# IMPORT LIBRARY
# ==========================================================

import time

import pandas as pd

from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)

import config as cfg


# ==========================================================
# LOAD DATASET
# ==========================================================

def load_data(file):
    """
    Membaca dataset CSV kemudian melakukan validasi.

    Parameters
    ----------
    file : UploadedFile | str

    Returns
    -------
    pandas.DataFrame
    """

    try:

        df = pd.read_csv(file)

    except Exception as e:

        raise Exception(
            f"Gagal membaca dataset.\n\n{e}"
        )

    validate_dataset(df)

    df = df.dropna().copy()

    return df


# ==========================================================
# VALIDASI DATASET
# ==========================================================

def validate_dataset(df):
    """
    Memastikan dataset memiliki seluruh
    kolom yang dibutuhkan.
    """

    required_columns = [

        cfg.MEMBER_COL,

        cfg.DATE_COL,

        cfg.ITEM_COL

    ]

    missing_columns = [

        col

        for col in required_columns

        if col not in df.columns

    ]

    if missing_columns:

        raise ValueError(

            "Dataset tidak memiliki kolom:\n"

            + "\n".join(missing_columns)

        )


# ==========================================================
# INFORMASI DATASET
# ==========================================================

def dataset_information(df):
    """
    Menghasilkan ringkasan informasi dataset.

    Returns
    -------
    dict
    """

    total_rows = len(df)

    total_members = df[
        cfg.MEMBER_COL
    ].nunique()

    total_products = df[
        cfg.ITEM_COL
    ].nunique()

    total_transactions = df.groupby(

        [

            cfg.MEMBER_COL,

            cfg.DATE_COL

        ]

    ).ngroups

    avg_items = (

        df.groupby(

            [

                cfg.MEMBER_COL,

                cfg.DATE_COL

            ]

        )

        .size()

        .mean()

    )

    return {

        "total_rows": total_rows,

        "total_members": total_members,

        "total_products": total_products,

        "total_transactions": total_transactions,

        "average_items": round(
            avg_items,
            2
        )

    }
# ==========================================================
# PREPARE BASKET
# ==========================================================

def prepare_basket(df):
    """
    Mengubah dataset transaksi menjadi
    basket transaction untuk Apriori.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    basket = (

        df

        .groupby(

            [

                cfg.MEMBER_COL,

                cfg.DATE_COL

            ]

        )[cfg.ITEM_COL]

        .value_counts()

        .unstack(fill_value=0)

    )

    basket = basket.astype(bool)

    return basket


# ==========================================================
# MENJALANKAN APRIORI
# ==========================================================

def run_apriori(
    basket,
    min_support,
    min_confidence,
    max_len
):
    """
    Menjalankan algoritma Apriori
    dan menghasilkan Association Rules.

    Parameters
    ----------
    basket : DataFrame

    min_support : float

    min_confidence : float

    max_len : int

    Returns
    -------
    frequent_itemsets,
    rules,
    execution_time
    """

    if basket.empty:

        raise ValueError(
            "Basket transaction kosong."
        )

    start_time = time.perf_counter()

    frequent_itemsets = apriori(
    basket,
    min_support=min_support,
    use_colnames=True,
    max_len=max_len,
    low_memory=True
    )

    execution_time = (
        time.perf_counter()
        - start_time
    )

    if frequent_itemsets.empty:

        return (

            frequent_itemsets,

            pd.DataFrame(),

            execution_time

        )

    rules = association_rules(

        frequent_itemsets,

        metric="confidence",

        min_threshold=min_confidence

    )

    if rules.empty:

        return (

            frequent_itemsets,

            rules,

            execution_time

        )

    rules = rules.sort_values(

        by=[

            "confidence",

            "lift"

        ],

        ascending=False

    ).reset_index(

        drop=True

    )

    return (

        frequent_itemsets,

        rules,

        execution_time

    )
# ==========================================================
# FORMAT FREQUENT ITEMSETS
# ==========================================================

def format_itemsets(frequent_itemsets):
    """
    Mengubah tampilan frequent itemsets agar
    lebih mudah dibaca.
    """

    if frequent_itemsets.empty:

        return frequent_itemsets

    df = frequent_itemsets.copy()

    df["itemsets"] = df["itemsets"].apply(

        lambda x: ", ".join(
            sorted(list(x))
        )

    )

    df["support"] = df["support"].round(4)

    return df


# ==========================================================
# FORMAT ASSOCIATION RULES
# ==========================================================

def format_rules(rules):
    """
    Memformat Association Rules agar lebih
    mudah ditampilkan pada Streamlit.
    """

    if rules.empty:

        return rules

    df = rules.copy()

    df["antecedents"] = df["antecedents"].apply(

        lambda x: ", ".join(
            sorted(list(x))
        )

    )

    df["consequents"] = df["consequents"].apply(

        lambda x: ", ".join(
            sorted(list(x))
        )

    )

    numeric_columns = [

        "support",

        "confidence",

        "lift"

    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = df[col].round(4)

    return df


# ==========================================================
# FILTER RULES BERDASARKAN PRODUK
# ==========================================================

def get_recommendation(
    rules,
    selected_item
):
    """
    Mengambil rekomendasi produk berdasarkan
    item yang dipilih pengguna.
    """

    if rules.empty:

        return pd.DataFrame()

    recommendation = rules[

        rules["antecedents"].apply(

            lambda items:

            selected_item in items

            if isinstance(items, (set, frozenset))

            else selected_item in str(items)

        )

    ].copy()

    if recommendation.empty:

        return recommendation

    recommendation = format_rules(
        recommendation
    )

    columns = [

        "antecedents",

        "consequents",

        "support",

        "confidence",

        "lift"

    ]

    columns = [

        col

        for col in columns

        if col in recommendation.columns

    ]

    recommendation = recommendation[columns]

    recommendation = recommendation.sort_values(

        by=[

            "confidence",

            "lift"

        ],

        ascending=False

    ).reset_index(

        drop=True

    )

    return recommendation
# ==========================================================
# SEARCH DATAFRAME
# ==========================================================

def search_dataframe(df, keyword):
    """
    Mencari data pada seluruh kolom DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame

    keyword : str

    Returns
    -------
    pandas.DataFrame
    """

    if df.empty:
        return df

    if keyword is None:
        return df

    keyword = keyword.strip()

    if keyword == "":
        return df

    mask = df.astype(str).apply(

        lambda col: col.str.contains(
            keyword,
            case=False,
            na=False
        )

    )

    return df[mask.any(axis=1)]


# ==========================================================
# DATAFRAME TO CSV
# ==========================================================

def dataframe_to_csv(df):
    """
    Mengubah DataFrame menjadi bytes CSV
    untuk download Streamlit.
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ==========================================================
# INITIALIZE SESSION STATE
# ==========================================================

def initialize_session_state():
    """
    Inisialisasi seluruh Session State.
    """

    import streamlit as st

    for key, value in cfg.SESSION_KEYS.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==========================================================
# RESET SESSION
# ==========================================================

def reset_session():
    """
    Menghapus hasil analisis tanpa
    menghapus dataset.
    """

    import streamlit as st

    st.session_state.analysis_done = False

    st.session_state.dataset_info = None

    st.session_state.basket = None

    st.session_state.frequent_itemsets = None

    st.session_state.rules = None

    st.session_state.execution_time = 0


# ==========================================================
# VALIDASI PARAMETER APRIORI
# ==========================================================

def validate_parameters(
    min_support,
    min_confidence,
    max_len
):
    """
    Memastikan parameter Apriori valid.
    """

    if not (

        cfg.MIN_SUPPORT_LIMIT

        <= min_support

        <= cfg.MAX_SUPPORT_LIMIT

    ):

        raise ValueError(

            "Minimum Support tidak valid."

        )

    if not (

        cfg.MIN_CONFIDENCE_LIMIT

        <= min_confidence

        <= cfg.MAX_CONFIDENCE_LIMIT

    ):

        raise ValueError(

            "Minimum Confidence tidak valid."

        )

    if not (

        cfg.MIN_ITEMSET

        <= max_len

        <= cfg.MAX_ITEMSET

    ):

        raise ValueError(

            "Maximum Itemset tidak valid."

        )


# ==========================================================
# MENJALANKAN SELURUH ANALISIS
# ==========================================================

def analyze_dataset(
    df,
    min_support,
    min_confidence,
    max_len
):
    """
    Menjalankan seluruh proses
    Market Basket Analysis.

    Returns
    -------
    dict
    """

    validate_parameters(

        min_support,

        min_confidence,

        max_len

    )

    dataset_info = dataset_information(
        df
    )

    basket = prepare_basket(
        df
    )

    frequent_itemsets, rules, execution_time = run_apriori(

        basket,

        min_support,

        min_confidence,

        max_len

    )

    frequent_itemsets = format_itemsets(
        frequent_itemsets
    )

    # rules = format_rules(
    #     rules
    # )

    return {

        "dataset": df,

        "dataset_info": dataset_info,

        "basket": basket,

        "frequent_itemsets": frequent_itemsets,

        "rules": rules,

        "execution_time": execution_time

    }