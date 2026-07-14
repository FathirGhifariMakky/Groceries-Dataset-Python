"""
==========================================================
app.py

Market Basket Analysis
Menggunakan Algoritma Apriori

Penulisan Ilmiah
Universitas Gunadarma
==========================================================
"""

# ==========================================================
# IMPORT LIBRARY
# ==========================================================
import matplotlib
matplotlib.use("Agg")

import streamlit as st

import config as cfg

from utils import (

    load_data,

    analyze_dataset,

    dataframe_to_csv,

    initialize_session_state,

    get_recommendation,

    search_dataframe

)

from visualization import (

    show_dataset_statistics,

    show_rule_statistics,

    plot_top_items,

    plot_support_distribution,

    plot_confidence_distribution,

    plot_lift_distribution,

    plot_support_confidence,

    # plot_network,

    show_about

    # show_footer

)

import pandas as pd

df = pd.read_csv("nama_file_dataset_anda.csv")

# GANTI dengan nama kolom asli di dataset Anda
# Cek dulu nama kolomnya dengan print(df.columns.tolist())
MEMBER_COL = "Member_number"   # sesuaikan
DATE_COL = "Date"              # sesuaikan
ITEM_COL = "itemDescription"   # sesuaikan

print("Jumlah baris:", len(df))
print("Jumlah item unik:", df[ITEM_COL].nunique())
print("Jumlah transaksi unik:", df.groupby([MEMBER_COL, DATE_COL]).ngroups)

# ==========================================================
# KONFIGURASI STREAMLIT
# ==========================================================

st.set_page_config(

    page_title=cfg.PAGE_TITLE,

    page_icon=cfg.PAGE_ICON,

    layout=cfg.PAGE_LAYOUT,

    initial_sidebar_state=cfg.SIDEBAR_STATE

)

# ==========================================================
# INITIALIZE SESSION STATE
# ==========================================================

initialize_session_state()

# ==========================================================
# HEADER
# ==========================================================

st.title(cfg.APP_TITLE)

st.markdown(cfg.APP_SUBTITLE)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("⚙ Pengaturan")

    uploaded_file = st.file_uploader(

        "Upload Dataset CSV",

        type=cfg.SUPPORTED_FILE_TYPES

    )

    st.markdown("---")

    st.subheader("Parameter Apriori")

    min_support = st.slider(

        "Minimum Support",

        min_value=cfg.MIN_SUPPORT_LIMIT,

        max_value=cfg.MAX_SUPPORT_LIMIT,

        value=cfg.DEFAULT_MIN_SUPPORT,

        step=0.001,

        format="%.3f"

    )

    min_confidence = st.slider(

        "Minimum Confidence",

        min_value=cfg.MIN_CONFIDENCE_LIMIT,

        max_value=cfg.MAX_CONFIDENCE_LIMIT,

        value=cfg.DEFAULT_MIN_CONFIDENCE,

        step=0.01,

        format="%.2f"

    )

    max_len = st.slider(

        "Maximum Itemset",

        min_value=cfg.MIN_ITEMSET,

        max_value=cfg.MAX_ITEMSET,

        value=cfg.DEFAULT_MAX_LEN

    )

        # tambahkan warning di sini
    if min_support < 0.02 and max_len >= 4:

        st.warning(
            "Kombinasi Minimum Support kecil dan Maximum Itemset besar "
            "dapat menyebabkan proses menjadi sangat berat. "
            "Disarankan menaikkan Minimum Support atau menurunkan Maximum Itemset."
        )

    st.markdown("---")

    analyze_button = st.button(

        "Jalankan Analisis",

        use_container_width=True

    )

    st.markdown("---")

    menu = st.radio(

        "Navigasi",

        cfg.MENU_LIST

    )
# ==========================================================
# MENJALANKAN ANALISIS
# ==========================================================

def run_analysis():
    """
    Menjalankan seluruh proses Market Basket Analysis.
    """

    if uploaded_file is None:

        st.warning(
            "Silakan upload dataset terlebih dahulu."
        )

        return

    try:

        with st.spinner(
            "Sedang menjalankan Apriori..."
        ):

            dataset = load_data(
                uploaded_file
            )

            result = analyze_dataset(

                dataset,

                min_support,

                min_confidence,

                max_len

            )

        st.session_state.dataset = result["dataset"]

        st.session_state.dataset_info = result["dataset_info"]

        st.session_state.basket = result["basket"]

        st.session_state.frequent_itemsets = result["frequent_itemsets"]

        st.session_state.rules = result["rules"]

        st.session_state.execution_time = result["execution_time"]

        st.session_state.analysis_done = True

        st.success(
            cfg.MSG_ANALYSIS_SUCCESS
        )

    except Exception as e:

        st.error(e)


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard_page():
    """
    Halaman Dashboard.
    """

    st.header("Dashboard")

    if not st.session_state.analysis_done:

        st.info(
            cfg.MSG_ANALYSIS_EMPTY
        )

        return

    show_dataset_statistics(
        st.session_state.dataset
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Frequent Itemset",

        len(
            st.session_state.frequent_itemsets
        )

    )

    col2.metric(

        "Association Rules",

        len(
            st.session_state.rules
        )

    )

    col3.metric(

        "Execution Time",

        f"{st.session_state.execution_time:.4f} s"

    )

    st.markdown("---")

    st.subheader(
        "Preview Dataset"
    )

    st.dataframe(

        st.session_state.dataset.head(10),

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    st.subheader(
        "Preview Association Rules"
    )

    if st.session_state.rules.empty:

        st.warning(
            cfg.MSG_NO_RULE
        )

    else:

        st.dataframe(

            st.session_state.rules.head(10),

            use_container_width=True,

            hide_index=True

        )
# ==========================================================
# DATASET PAGE
# ==========================================================

def dataset_page():
    """
    Halaman Dataset.
    """

    st.header("Dataset")

    if not st.session_state.analysis_done:

        st.info(
            cfg.MSG_ANALYSIS_EMPTY
        )

        return

    show_dataset_statistics(
        st.session_state.dataset
    )

    st.markdown("---")

    st.subheader("Preview Dataset")

    search = st.text_input(
        "Cari Data",
        placeholder="Masukkan kata kunci..."
    )

    dataset = search_dataframe(
        st.session_state.dataset,
        search
    )

    st.dataframe(

        dataset,

        use_container_width=True,

        hide_index=True

    )

    st.download_button(

        label="⬇ Download Dataset",

        data=dataframe_to_csv(dataset),

        file_name=cfg.DATASET_DOWNLOAD_NAME,

        mime="text/csv",

        use_container_width=True

    )


# ==========================================================
# FREQUENT ITEMSET PAGE
# ==========================================================

def itemset_page():
    """
    Halaman Frequent Itemset.
    """

    st.header("Frequent Itemset")

    if not st.session_state.analysis_done:

        st.info(
            cfg.MSG_ANALYSIS_EMPTY
        )

        return

    itemsets = st.session_state.frequent_itemsets

    st.metric(

        "Jumlah Frequent Itemset",

        len(itemsets)

    )

    st.markdown("---")

    search = st.text_input(

        "🔍 Cari Itemset",

        placeholder="Misal: whole milk"

    )

    itemsets = search_dataframe(

        itemsets,

        search

    )

    st.dataframe(

        itemsets,

        use_container_width=True,

        hide_index=True

    )

    st.download_button(

        label="⬇ Download Frequent Itemset",

        data=dataframe_to_csv(itemsets),

        file_name=cfg.ITEMSET_DOWNLOAD_NAME,

        mime="text/csv",

        use_container_width=True

    )
# ==========================================================
# ASSOCIATION RULES PAGE
# ==========================================================

def rules_page():
    """
    Halaman Association Rules.
    """

    st.header("Association Rules")

    if not st.session_state.analysis_done:

        st.info(cfg.MSG_ANALYSIS_EMPTY)

        return

    rules = st.session_state.rules

    show_rule_statistics(rules)

    st.markdown("---")

    search = st.text_input(

        "🔍 Cari Rules",

        placeholder="Misal: whole milk"

    )

    filtered_rules = search_dataframe(

        rules,

        search

    )

    st.dataframe(

        filtered_rules,

        use_container_width=True,

        hide_index=True

    )

    st.download_button(

        label="⬇ Download Association Rules",

        data=dataframe_to_csv(filtered_rules),

        file_name=cfg.RULES_DOWNLOAD_NAME,

        mime="text/csv",

        use_container_width=True

    )


# ==========================================================
# VISUALIZATION PAGE
# ==========================================================

def visualization_page():
    """
    Halaman Visualisasi.
    """

    st.header("Visualisasi")

    if not st.session_state.analysis_done:

        st.info(cfg.MSG_ANALYSIS_EMPTY)

        return

    show_rule_statistics(
        st.session_state.rules
    )

    st.markdown("---")

    chart = st.selectbox(

        "Pilih Visualisasi",

        [

            "Top Selling Products",

            "Support Distribution",

            "Confidence Distribution",

            "Lift Distribution",

            "Support vs Confidence",

            "Network Graph"

        ]

    )

    if chart == "Top Selling Products":

        plot_top_items(

            st.session_state.dataset

        )

    elif chart == "Support Distribution":

        plot_support_distribution(

            st.session_state.rules

        )

    elif chart == "Confidence Distribution":

        plot_confidence_distribution(

            st.session_state.rules

        )

    elif chart == "Lift Distribution":

        plot_lift_distribution(

            st.session_state.rules

        )

    elif chart == "Support vs Confidence":

        plot_support_confidence(

            st.session_state.rules

        )

    # elif chart == "Network Graph":

    #     plot_network(

    #         st.session_state.rules

    #     )
# ==========================================================
# RECOMMENDATION PAGE
# ==========================================================

def recommendation_page():
    """
    Halaman rekomendasi produk.
    """

    st.header("Rekomendasi Produk")

    if not st.session_state.analysis_done:

        st.info(cfg.MSG_ANALYSIS_EMPTY)

        return

    items = sorted(

        st.session_state.dataset[
            cfg.ITEM_COL
        ].unique()

    )

    selected_item = st.selectbox(

        "Pilih Produk",

        items

    )

    recommendation = get_recommendation(

        st.session_state.rules,

        selected_item

    )

    if recommendation.empty:

        st.warning(

            cfg.MSG_NO_RECOMMENDATION

        )

        return

    st.success(

        f"Ditemukan {len(recommendation)} rekomendasi."

    )

    st.dataframe(

        recommendation,

        use_container_width=True,

        hide_index=True

    )

    st.download_button(

        "⬇ Download Rekomendasi",

        data=dataframe_to_csv(
            recommendation
        ),

        file_name=cfg.RECOMMENDATION_DOWNLOAD_NAME,

        mime="text/csv",

        use_container_width=True

    )


# ==========================================================
# ABOUT PAGE
# ==========================================================

def about_page():
    """
    Halaman Tentang.
    """

    show_about()


# ==========================================================
# MAIN
# ==========================================================

def main():
    """
    Fungsi utama aplikasi.
    """

    # Tombol Jalankan Analisis

    if analyze_button:

        run_analysis()

    # Routing Menu

    if menu == cfg.MENU_DASHBOARD:

        dashboard_page()

    elif menu == cfg.MENU_DATASET:

        dataset_page()

    elif menu == cfg.MENU_ITEMSET:

        itemset_page()

    elif menu == cfg.MENU_RULES:

        rules_page()

    elif menu == cfg.MENU_VISUALIZATION:

        visualization_page()

    elif menu == cfg.MENU_RECOMMENDATION:

        recommendation_page()

    elif menu == cfg.MENU_ABOUT:

        about_page()

    # Footer

    # show_footer()


# ==========================================================
# PROGRAM UTAMA
# ==========================================================

if __name__ == "__main__":

    main()