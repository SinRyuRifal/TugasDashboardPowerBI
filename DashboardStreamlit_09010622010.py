from fileinput import filename
from logging import Filterer
from turtle import home
from altair import TitleAnchor
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Coffee Sales", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Dashboard Coffee Sales")
st.subheader(":student: Muhammad Rifqi Naufal Irsyad - 09010622010")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)
# Upload file
fl = st.file_uploader(":file_folder: Upload a File", type=["xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(fl)
else:
    st.warning("Upload file bernama 'Coffee Sales.xlsx'")
    st.stop()

# Buat sorting tanggal
df["Order Date"] = pd.to_datetime(df["Order Date"])


# Buat tanggal awal dan akhir
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

# Filter Order Date
st.sidebar.header("Order Date:")
date1 = pd.to_datetime(st.sidebar.date_input(":date: Start Date", startDate))

date2 = pd.to_datetime(st.sidebar.date_input(":date: End Date", endDate))

# Agar data update setiap kita pilih tanggal
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


# Filter negara
st.sidebar.header("Filter:")
country = st.sidebar.multiselect(":world_map: Negara", df["Customer Country"].unique())
if not country:
    df_filtered = df.copy()
else:
    df_filtered = df[df["Customer Country"].isin(country)]

# Filter kota
city = st.sidebar.multiselect(":cityscape: Kota", df_filtered["Customer City"].unique())
if not city:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Customer City"].isin(city)]

# Filter Loyalty Card
card = st.sidebar.multiselect(
    ":credit_card: Kepemilikan Loyalti Card",
    df_filtered["Customer Loyalty Card"].unique(),
)
if not card:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Customer Loyalty Card"].isin(card)]

# Filter jenis kopi
coffee_type = st.sidebar.multiselect(
    ":coffee: Jenis Kopi", df_filtered["Product Coffee Type"].unique()
)
if not coffee_type:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Coffee Type"].isin(coffee_type)]

# Filter jenis sangrai
roast_type = st.sidebar.multiselect(
    ":fire: Jenis Sangrai", df_filtered["Product Roast Type"].unique()
)
if not roast_type:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Roast Type"].isin(roast_type)]

# Filter ukuran
size = st.sidebar.multiselect(
    ":cup_with_straw: Ukuran Kemasan", df_filtered["Product Size (kg)"].unique()
)
if not size:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Size (kg)"].isin(size)]


# Method dan perulangan untuk filter dengan semua kondisi dari 0-6
def filter_dataframe(df, **filter):
    filtered_df = df.copy()
    for key1, value1 in filter.items():
        if value1:
            for key2, value2 in filter.items():
                if value2 and key1 != key2:
                    for key3, value3 in filter.items():
                        if value3 and key2 != key3 and key1 != key3:
                            for key4, value4 in filter.items():
                                if (
                                    value4
                                    and key3 != key4
                                    and key2 != key4
                                    and key1 != key4
                                ):
                                    for key5, value5 in filter.items():
                                        if (
                                            value5
                                            and key4 != key5
                                            and key3 != key5
                                            and key2 != key5
                                            and key1 != key5
                                        ):
                                            for key6, value6 in filter.items():
                                                if (
                                                    value6
                                                    and key5 != key6
                                                    and key4 != key6
                                                    and key3 != key6
                                                    and key2 != key6
                                                    and key1 != key6
                                                ):
                                                    for key7, value7 in filter.items():
                                                        if (
                                                            value7
                                                            and key6 != key7
                                                            and key5 != key7
                                                            and key4 != key7
                                                            and key3 != key7
                                                            and key2 != key7
                                                            and key1 != key7
                                                        ):
                                                            filtered_df = filtered_df[
                                                                filtered_df[key1].isin(
                                                                    value1
                                                                )
                                                                & filtered_df[
                                                                    key2
                                                                ].isin(value2)
                                                                & filtered_df[
                                                                    key3
                                                                ].isin(value3)
                                                                & filtered_df[
                                                                    key4
                                                                ].isin(value4)
                                                                & filtered_df[
                                                                    key5
                                                                ].isin(value5)
                                                                & filtered_df[
                                                                    key6
                                                                ].isin(value6)
                                                                & filtered_df[
                                                                    key7
                                                                ].isin(value7)
                                                            ]
    return filtered_df


filtered_df = filter_dataframe(
    df_filtered,
    country=country,
    city=city,
    card=card,
    coffee_type=coffee_type,
    roast_type=roast_type,
    size=size,
)


def Home(filtered_df):
    sum_order_quantity = filtered_df["Order Quantity"].sum()
    count_order = filtered_df["Order ID"].count()
    max_total_profit = filtered_df["Total Profit"].max()
    avg_total_profit = filtered_df["Total Profit"].mean()
    sum_total_profit = filtered_df["Total Profit"].sum()

    # Menampilkan summary
    total1, total2, total3, total4, total5 = st.columns(5, gap="large")
    with total1:
        st.info(":pencil: Jumlah Kopi Terjual")
        st.metric(label="Sum of Order Quantity", value=f"{sum_order_quantity:.2f}")
    with total2:
        st.info(":pencil: Pesanan Terselesaikan")
        st.metric(label="Count of Order", value=f"{count_order:.2f}")
    with total3:
        st.info(":pencil: Pendapatan Tertinggi")
        st.metric(label="Max of Total Profit", value=f"${max_total_profit:.2f}")
    with total4:
        st.info(":pencil: Rata-Rata Pendapatan")
        st.metric(label="Avg of Total Profit", value=f"${avg_total_profit:.2f}")
    with total5:
        st.info(":pencil: Total Pendapatan")
        st.metric(label="Sum of Total Profit", value=f"${sum_total_profit:.2f}")


# Panggil method yang sudah dibuat dengan DataFrame yang sudah difilter
Home(filtered_df)


# Menentukan besar kolom kontainer
col1, col2 = st.columns((2))
# bar chart jenis sangrai
penjualanJenisSangrai_df = filtered_df.groupby(
    by=["Order Date", "Product Roast Type"], as_index=False
)["Order Quantity"].sum()

# ambil tahun dari order data
penjualanJenisSangrai_df["Year"] = pd.to_datetime(
    penjualanJenisSangrai_df["Order Date"]
).dt.year


# konversi agar sumbu x bisa dipakai menggunakan tahun saja
penjualanJenisSangrai_df["Tahun"] = penjualanJenisSangrai_df["Year"].astype(str)

# dikelompokkan dari tahun dan tipe roasting
penjualanJenisSangrai_df = penjualanJenisSangrai_df.groupby(
    by=["Tahun", "Product Roast Type"], as_index=False
)["Order Quantity"].sum()

# Sorting by tahun saja
penjualanJenisSangrai_df["Tahun"] = pd.to_datetime(penjualanJenisSangrai_df["Tahun"])
penjualanJenisSangrai_df = penjualanJenisSangrai_df.sort_values(by="Tahun")

with col1:
    # setting bar chart
    fig = px.bar(
        penjualanJenisSangrai_df,
        x="Tahun",
        y="Order Quantity",
        color="Product Roast Type",
        template="seaborn",
        title="Tren Penjualan Berdasarkan Jenis Sangrai Kopi setiap tahunnya",
        barmode="group",
        text="Order Quantity",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True, height=400)

with col2:
    # count distinct customer name buat menentukan banyaknya yang punya loyalti card
    loyalty_card_counts = (
        filtered_df.groupby("Customer Loyalty Card")["Customer Name"]
        .nunique()
        .reset_index()
    )

    fig = px.pie(
        loyalty_card_counts,
        values="Customer Name",
        names="Customer Loyalty Card",
        title="Persentase Kepemilikan Loyalti Card",
        hole=0.5,
    )
    fig.update_traces(textinfo="label+percent", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with col1:
    fig = px.pie(
        filtered_df,
        values="Order Quantity",
        names="Product Coffee Type",
        hole=0.5,
        title="Persentase Jumlah Pesanan Berdasarkan Jenis Kopi",
    )
    fig.update_traces(textinfo="label+percent", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

# Bar Chart
# Kelompokkan data berdasarkan "Product Size (kg)" dan "Product Coffee Type"
productSize_df = filtered_df.groupby(
    by=["Product Size (kg)", "Product Coffee Type"], as_index=False
)["Order Quantity"].sum()

# Jumlah Pesanan Berdasarkan Ukuran Produk (Kg) dan jenis kopi
with col2:
    fig = px.bar(
        productSize_df,
        x="Product Size (kg)",
        y="Order Quantity",
        color="Product Coffee Type",
        template="seaborn",
        title="Jumlah Pesanan Berdasarkan Ukuran Produk (Kg) dan jenis kopi",
        barmode="group",  # agar jadi clustered, bukan stacked
        text="Order Quantity",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    # fig.update_layout(
    #     xaxis_title="Ukuran Produk (kg)",
    #     yaxis_title="Jumlah Pesanan",
    #     title_xanchor="center",
    #     title_yanchor="top",
    #     title_x=0.5,
    #     title_y=0.9,
    # )
    st.plotly_chart(fig, use_container_width=True, height=400)


# Map
with col1:
    fig = px.scatter_geo(
        filtered_df,
        title="Distribusi Penjualan Kopi di Kota-kota Negara Tertentu",
        lat="Latitude",
        lon="Longitude",
        color="Customer Country",
        size="Order Quantity",
        hover_name="Customer City",
        projection="natural earth",
    )
    st.plotly_chart(fig, use_container_width=True, width=800, height=600)

# Chart top 5
# Kelompokkan data berdasarkan nama pelanggan dan jumlahkan jumlah pesanan
with col2:
    customer_orders = (
        filtered_df.groupby("Customer Name")["Order Quantity"].sum().reset_index()
    )

    # Urutkan pelanggan berdasarkan jumlah pesanan secara menurun
    customer_orders = customer_orders.sort_values(by="Order Quantity", ascending=False)

    # Pilih top 5 pelanggan dengan jumlah pesanan tertinggi
    top_5_customers = customer_orders.head(5)

    # Buat grouped bar chart untuk top 5 pelanggan
    fig = px.bar(
        top_5_customers,
        x="Order Quantity",
        y="Customer Name",
        title="Top 5 Pelanggan dengan Jumlah Pesanan Tertinggi",
        template="seaborn",
        barmode="group",
        text="Order Quantity",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# bar chart Tren Total Pendapatan di Setiap Negara
pendapatanTotal_df = filtered_df.groupby(
    by=["Order Date", "Customer Country"], as_index=False
)["Total Profit"].sum()

# ambil tahun dan bulan dari order data
pendapatanTotal_df["Year"] = pd.to_datetime(pendapatanTotal_df["Order Date"]).dt.year
pendapatanTotal_df["Month"] = pd.to_datetime(pendapatanTotal_df["Order Date"]).dt.month

# gabung tahun dan bulan jadi 1
pendapatanTotal_df["Year_Month"] = (
    pendapatanTotal_df["Year"].astype(str)
    + "-"
    + pendapatanTotal_df["Month"].astype(str)
)

# dikelompokkan dari Year_Month dan Customer Country
pendapatanTotal_df = pendapatanTotal_df.groupby(
    by=["Year_Month", "Customer Country"], as_index=False
)["Total Profit"].sum()

# Sorting by Year dan Month
pendapatanTotal_df["Year_Month"] = pd.to_datetime(pendapatanTotal_df["Year_Month"])
pendapatanTotal_df = pendapatanTotal_df.sort_values(by="Year_Month")

# setting line chart
st.subheader("Tren Total Pendapatan di Setiap Negara")
fig = px.line(
    pendapatanTotal_df,
    x="Year_Month",
    y="Total Profit",
    color="Customer Country",
    template="seaborn",
)
fig.update_traces(mode="lines")
st.plotly_chart(fig, use_container_width=True, height=400)
