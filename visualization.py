"""
==========================================================
visualization.py

Visualisasi Market Basket Analysis
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
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

import config as cfg


# ==========================================================
# DATASET STATISTICS
# ==========================================================

def show_dataset_statistics(df):
    """
    Menampilkan ringkasan statistik dataset.
    """

    if df is None or df.empty:

        st.warning("Dataset belum tersedia.")

        return

    total_rows = len(df)

    total_members = df[cfg.MEMBER_COL].nunique()

    total_products = df[cfg.ITEM_COL].nunique()

    total_transactions = df.groupby(
        [
            cfg.MEMBER_COL,
            cfg.DATE_COL
        ]
    ).ngroups

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Data",
        f"{total_rows:,}"
    )

    col2.metric(
        "Jumlah Member",
        f"{total_members:,}"
    )

    col3.metric(
        "Jumlah Produk",
        f"{total_products:,}"
    )

    col4.metric(
        "Jumlah Transaksi",
        f"{total_transactions:,}"
    )


# ==========================================================
# RULE STATISTICS
# ==========================================================

def show_rule_statistics(rules):
    """
    Menampilkan ringkasan Association Rules.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Rules",
        len(rules)
    )

    col2.metric(
        "Support Maksimum",
        f"{rules['support'].max():.4f}"
    )

    col3.metric(
        "Confidence Maksimum",
        f"{rules['confidence'].max():.4f}"
    )

    col4.metric(
        "Lift Maksimum",
        f"{rules['lift'].max():.4f}"
    )
# ==========================================================
# TOP SELLING PRODUCTS
# ==========================================================

def plot_top_items(df):
    """
    Menampilkan grafik Top Produk Terlaris.
    """

    if df is None or df.empty:

        st.warning("Dataset belum tersedia.")

        return

    top_items = (

        df[cfg.ITEM_COL]

        .value_counts()

        .head(cfg.TOP_N_PRODUCTS)

        .sort_values()

    )

    fig, ax = plt.subplots(

        figsize=(

            cfg.FIGURE_WIDTH,

            cfg.FIGURE_HEIGHT

        )

    )

    ax.barh(

        top_items.index,

        top_items.values

    )

    ax.set_title(

        f"Top {cfg.TOP_N_PRODUCTS} Produk Terlaris"

    )

    ax.set_xlabel("Jumlah Pembelian")

    ax.set_ylabel("Produk")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# SUPPORT DISTRIBUTION
# ==========================================================

def plot_support_distribution(rules):
    """
    Histogram nilai Support.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    fig, ax = plt.subplots(

        figsize=(

            cfg.FIGURE_WIDTH,

            cfg.FIGURE_HEIGHT

        )

    )

    ax.hist(

        rules["support"],

        bins=cfg.HISTOGRAM_BINS

    )

    ax.set_title(

        "Distribusi Support"

    )

    ax.set_xlabel(

        "Support"

    )

    ax.set_ylabel(

        "Jumlah Rules"

    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CONFIDENCE DISTRIBUTION
# ==========================================================

def plot_confidence_distribution(rules):
    """
    Histogram nilai Confidence.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    fig, ax = plt.subplots(

        figsize=(

            cfg.FIGURE_WIDTH,

            cfg.FIGURE_HEIGHT

        )

    )

    ax.hist(

        rules["confidence"],

        bins=cfg.HISTOGRAM_BINS

    )

    ax.set_title(

        "Distribusi Confidence"

    )

    ax.set_xlabel(

        "Confidence"

    )

    ax.set_ylabel(

        "Jumlah Rules"

    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# LIFT DISTRIBUTION
# ==========================================================

def plot_lift_distribution(rules):
    """
    Histogram nilai Lift.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    fig, ax = plt.subplots(

        figsize=(

            cfg.FIGURE_WIDTH,

            cfg.FIGURE_HEIGHT

        )

    )

    ax.hist(

        rules["lift"],

        bins=cfg.HISTOGRAM_BINS

    )

    ax.set_title(

        "Distribusi Lift"

    )

    ax.set_xlabel(

        "Lift"

    )

    ax.set_ylabel(

        "Jumlah Rules"

    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)
# ==========================================================
# SUPPORT VS CONFIDENCE
# ==========================================================

def plot_support_confidence(rules):
    """
    Scatter Plot Support vs Confidence.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    fig, ax = plt.subplots(

        figsize=(

            cfg.FIGURE_WIDTH,

            cfg.FIGURE_HEIGHT

        )

    )

    ax.scatter(

        rules["support"],

        rules["confidence"],

        alpha=0.7

    )

    ax.set_title(
        "Support vs Confidence"
    )

    ax.set_xlabel(
        "Support"
    )

    ax.set_ylabel(
        "Confidence"
    )

    ax.grid(True)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# ASSOCIATION RULE NETWORK
# ==========================================================

def plot_network(rules):
    """
    Menampilkan Network Graph Association Rules.
    """

    if rules is None or rules.empty:

        st.warning(cfg.MSG_NO_RULE)

        return

    graph = nx.DiGraph()

    top_rules = rules.head(
        cfg.NETWORK_MAX_RULES
    )

    for _, row in top_rules.iterrows():

        antecedents = row["antecedents"]

        consequents = row["consequents"]

        if isinstance(antecedents, str):

            antecedents = [

                item.strip()

                for item in antecedents.split(",")

            ]

        else:

            antecedents = list(
                antecedents
            )

        if isinstance(consequents, str):

            consequents = [

                item.strip()

                for item in consequents.split(",")

            ]

        else:

            consequents = list(
                consequents
            )

        for source in antecedents:

            for target in consequents:

                graph.add_edge(

                    source,

                    target,

                    weight=row["lift"]

                )

    if graph.number_of_nodes() == 0:

        st.warning(
            "Graph tidak dapat dibuat."
        )

        return

    fig, ax = plt.subplots(

        figsize=(10, 8)

    )

    pos = nx.spring_layout(

        graph,

        seed=42

    )

    nx.draw_networkx_nodes(

        graph,

        pos,

        node_size=1000,

        ax=ax

    )

    nx.draw_networkx_labels(

        graph,

        pos,

        font_size=9,

        ax=ax

    )

    nx.draw_networkx_edges(

        graph,

        pos,

        arrows=True,

        ax=ax

    )

    ax.set_title(
        "Association Rules Network"
    )

    ax.axis("off")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)
# ==========================================================
# ABOUT PAGE
# ==========================================================

def show_about():
    """
    Menampilkan informasi website.
    """

    st.title("Tentang Website")

    st.markdown(
        f"""
### {cfg.PROJECT_NAME}

Website ini dibuat untuk melakukan **Market Basket Analysis**
menggunakan **Algoritma Apriori** pada **Groceries Dataset**.

Melalui Website ini pengguna dapat:

- Melakukan analisis Frequent Itemset
- Membentuk Association Rules
- Melihat visualisasi hasil analisis
- Mendapatkan rekomendasi produk
- Mengunduh hasil analisis

---
"""
    )

#     col1, col2 = st.columns(2)

#     with col1:

#         st.info(
#             f"""
# **Versi**

# {cfg.APP_VERSION}

# **Tahun**

# {cfg.YEAR}
# """
#         )

#     with col2:

#         st.info(
#             f"""
# **Penyusun**

# {cfg.AUTHOR}

# **Universitas**

# {cfg.UNIVERSITY}
# """
#         )


# ==========================================================
# FOOTER
# ==========================================================

# def show_footer():
#     """
#     Footer aplikasi.
#     """

#     st.markdown("---")

#     st.caption(

#         f"""
# {cfg.PROJECT_NAME}

# Versi {cfg.APP_VERSION}

# {cfg.UNIVERSITY}

# © {cfg.YEAR} {cfg.AUTHOR}
# """

#     )