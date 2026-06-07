import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import ast
import altair as alt
import math
from lib_function import insert_icon, sales_horizontal_bar_chart

print("-----------------------------------------------------------------------------------------------------------------------------------------")
print("Start printing")

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set folder path
# path = "B. Project/geotag_data/"
path = "geotag_data/"

#----------------------------- Read data file
df_master_branch = pd.read_excel(path+"master_branch.xlsx")
df_master_customer = pd.read_excel(path+"master_customer.xlsx")
df_sales_data = pd.read_excel(path+"sales_data.xlsx")
df_ar_data = pd.read_excel(path+"ar_data.xlsx")
df_ar_data["EOM_Period"] = pd.to_datetime("2025-12-31")
df_ar_color = pd.read_excel(path+"ar_color.xlsx")
customer_list = df_master_customer["Customer_Name"].unique()
branch_list = df_master_branch["Branch_ID"].unique()
segment_list = df_master_customer["Segmentation"].unique()

tab1, tab2, tab3 = st.tabs(["Project Description","Sales Overview","Customer Info"])
#----------------------------- Tab 1 : Project Description
with tab1:
    st.header("Introduction")
    st.html('''<p style="text-align:justify;">AAM is a pharmaceuticals and medical devices distributor company that distributes its product across Indonesia. 
        This company has 38 branches and over 100,000 customer spread over Indonesia from Aceh to Jayapura. A lot of activities done by its branches make the 
        headquarter must have a reliable data to monitor its operation, including sales and collection.</p>
            
        <p style="text-align:justify;">In order to monitor its sales and collection performance, the company need to have a big overview about how much the sales 
        transaction and AR remaining also where they happen relative to the company branch. Maintaining a lot of customer requires a lot of effort for the company. 
        So this system is developed to help the company "finding a spot" in a quick way. This project showcase demonstrates a project that I have done in the company. 
        The data and model used in this showcase are simplified just to show how the data processing works.</p>''')
    
    st.subheader("Data Model")
    col1, col2 = st.columns(2)
    with col1:
        st.html('''<p style="text-align:justify;">There are 4 data used in this showcase. The data structure are simplified until there are only information we need 
            to build this project. The picture beside shows the data structure and their relation.</p>
                
            <p style="text-align:justify;">First we have <b>Sales</b> data, that is the table to record transactions that have been made by customers. In this table, we will find 
            5 attributes or columns that will give information about each transaction happen. The <b>Date</b> tells us when the transaction happen. It presents value with date format. 
            The <b>Invoice_No</b> is the identity of each data, in this case Invoice_No can be considerred as the primary key. The <b>Customer_ID</b> is the ones who make 
            the transaction. The information detail about customer can be found in Master_Customer. The <b>Gross_Value</b> and <b>Net_Value</b> are the transaction 
            value presented in gross and net.</p>
                
            <p style="text-align:justify;">And then we have <b>AR</b> data, that is the table to record the remaining amount that the customers still have to pay from their transactions. In this data, 
            there are 5 attributes or columns that will give detail information. <b>EOM_Period</b> tells us about when the snapshot happen to support calculation about how long
            that the pending of sinvoice payment. The <b>Invoice_No</b> is the identity of transaction from customer. The <b>Invoice_Date</b> is the invoice date issued. 
            The <b>Customer_ID</b> is the ones who make the transaction. The information detail about customer can be found in Master_Customer. And then the <b>Remaining_Amount</b>
            is the remaining value of invoice that still have to be paid by customers.</p>
            
            <p style="text-align:justify;">After that, we also have <b>Master_Customer</b>, that is a table to tell us detail information about customer. There are 7 attributes or columns in this data.
            The <b>Customer_ID</b> is the identity of each data, in this case Customer_ID can be considerred as the primary key. The <b>Customer_Name</b> is the name of each customer.
            Two customers can have a same name but the IDs are still different. The <b>Longitude</b> and <b>Latitude</b> are the geographic location of each customer. The <b>Segmentation</b>
            is the classification of customer. The <b>Branch_ID</b> is the company branch that serve the customer. The <b>TOP_Days</b> is the aggreement with customer about how long they
            can pend their payment. This TOP will be used to calculate the aging of pending payment.</p>
            ''')
        
    st.html('''
        <p style="text-align:justify;">Finally, we have <b>Master_Branch</b>, that is a table to tell us detail information about company branch. There are 6 attributes or columns in this data.
        The <b>Branch_ID</b> is the identity of each data, in this case Branch_ID can be considerred as the primary key. The <b>Branch_Name</b> is the name of each branch.
        Two branches can have a same name but the IDs are still different. The <b>Longitude</b> and <b>Latitude</b> are the geographic location of each branch. The <b>City</b>
        and <b>Province</b> are the branch location name.</p>
        ''')
    with col2:
        insert_icon(path, "geo_tag_relation_model.png")
        
    st.subheader("Future Improvements")
    st.html('''<p style="text-align:justify;">For future improvements, this analysis can be added by <b>sales target</b> and <b>AR collection target</b> data. This data can be combined with
        sales data or AR data to monitor the company achievement to the target, either it achieves the target or not. The target data is broken down by branch target so each 
        branch achievement also can be analyzed. The cause of success of target achievement is analyzed with several factors, such as place, time, or customer segmentation.</p>
            
        <p style="text-align:justify;">For more rigid anlysis, we can add a master data about <b>product</b>. This data can include attribute such as the product ID, product name, manufacturer, 
        product price, and so on. In this showcase, we only see invoice number and its value in sales data. But in reality, a customer can purchase more than one product in one 
        transaction. This data, combined with other existing data, also can help us to do more complex analysis about product sold. So the company can efficiently make effort to 
        distribute product to a place with more potential revenue.</p>
        ''')
    
#----------------------------- Tab 2 : Sales Overview
with tab2:
    st.header("Sales Performance 2025")
    st.space()

    # All data joined
    df_master_branch_customer = pd.merge(df_master_customer, df_master_branch, on="Branch_ID", how='left')

    df_sales_dashboard = pd.merge(df_sales_data, df_master_customer, on="Customer_ID", how='left')
    df_sales_dashboard = pd.merge(df_sales_dashboard, df_master_branch, on="Branch_ID", how="left")
    df_sales_filter_branch = df_sales_dashboard.copy()
    df_sales_filter_segment = df_sales_dashboard.copy()
    
    df_ar_dashboard = pd.merge(df_ar_data, df_master_customer, on="Customer_ID", how='left')
    df_ar_dashboard = pd.merge(df_ar_dashboard, df_master_branch, on="Branch_ID", how="left")
    df_ar_dashboard["AR_Aging"] = (df_ar_dashboard["EOM_Period"] - df_ar_dashboard["Invoice_Date"]).dt.days
    df_ar_dashboard["Overdue"] = np.where(df_ar_dashboard["AR_Aging"] > df_ar_dashboard["TOP_Days"], "Y", "N")

    # Select branch and segment (col1), show KPI (col2, col3, col4)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.html('''<p style="text-align:justify;"><b>Filter selection</b></p>''')
        selected_branch = st.selectbox(label="Branch", placeholder="Select a branch...", options=branch_list, index=None)
        if(selected_branch!=None):
            df_master_branch_customer = df_master_branch_customer[df_master_branch_customer["Branch_ID"]==selected_branch]
            df_sales_dashboard = df_sales_dashboard[df_sales_dashboard["Branch_ID"]==selected_branch]
            df_sales_filter_branch = df_sales_filter_branch[df_sales_filter_branch["Branch_ID"]==selected_branch]
            df_ar_dashboard = df_ar_dashboard[df_ar_dashboard["Branch_ID"]==selected_branch]

        selected_segment = st.selectbox(label="Segment", placeholder="Select a segment...", options=segment_list, index=None)
        if(selected_segment!=None):
            df_master_branch_customer = df_master_branch_customer[df_master_branch_customer["Segmentation"]==selected_segment]
            df_sales_dashboard = df_sales_dashboard[df_sales_dashboard["Segmentation"]==selected_segment]
            df_sales_filter_segment = df_sales_filter_segment[df_sales_filter_segment["Segmentation"]==selected_segment]
            df_ar_dashboard = df_ar_dashboard[df_ar_dashboard["Segmentation"]==selected_segment]
    with col2:
        st.metric("Company Branch", df_master_branch_customer["Branch_ID"].nunique(), border=True)
        st.metric("Active Customer", df_master_branch_customer["Customer_ID"].nunique(), border=True)
    with col3:
        st.metric("Invoice Created", f"{df_sales_dashboard['Invoice_Number'].nunique():,}", border=True)
        st.metric("Overdue Invoice", f"{df_ar_dashboard[df_ar_dashboard['Overdue']=='Y']['Invoice_Number'].nunique():,}", border=True)
    with col4:
        st.metric("Gross Sales Value", f"IDR {df_sales_dashboard['Gross_Value'].sum():,}", border=True)
        st.metric("Net Sales Value", f"IDR {df_sales_dashboard['Net_Value'].sum():,}", border=True)

    # Horizontal Bar Chart
    st.space()
    col1, col2, col3 = st.columns(3)
    # Sales by branch chart
    with col1:
        df_chart1 = df_sales_filter_segment.groupby(["Branch_ID","Branch_Name"])[["Gross_Value","Net_Value"]].sum().sort_values("Gross_Value", ascending=False).reset_index()
        # df_chart1 = df_chart1.head(10)
        df_chart1 = df_chart1.melt(
                        id_vars=["Branch_ID","Branch_Name"],
                        value_vars=["Gross_Value","Net_Value"],
                    )
        df_chart1["Highlight"] = np.where(df_chart1["Branch_ID"]==selected_branch, "Y", "N")
        df_chart1["Hex_Code"] = np.where(selected_branch==None, 
                                    np.where(df_chart1["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b"),
                                    np.where(df_chart1["Highlight"]=="Y", 
                                        np.where(df_chart1["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b"),
                                        np.where(df_chart1["variable"]=="Gross_Value", "#c5ddd4ff", "#d8c3af")
                                    )
                                )
        df_chart1["Sales Category"] = df_chart1["variable"].str.replace("_", " ", regex=False)
        # Show data in bar chart
        sales_horizontal_bar_chart(df_chart1, chart_title="Branch Sales Performance", x="value", y="Branch_ID", variable="Sales Category", color="Hex_Code",
                                   subtitle_class="branch", subtitle_support_text1=selected_segment, subtitle_support_text2=None)
    
    # Sales by segmentation chart
    with col2:
        df_chart2 = df_sales_filter_branch.groupby("Segmentation")[["Gross_Value","Net_Value"]].sum().sort_values("Gross_Value", ascending=False).reset_index()
        # df_chart1 = df_chart1.head(10)
        df_chart2 = df_chart2.melt(
                        id_vars=["Segmentation"],
                        value_vars=["Gross_Value","Net_Value"],
                    )
        df_chart2["Highlight"] = np.where(df_chart2["Segmentation"]==selected_segment, "Y", "N")
        df_chart2["Hex_Code"] = np.where(selected_segment==None, 
                                    np.where(df_chart2["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b"),
                                    np.where(df_chart2["Highlight"]=="Y", 
                                        np.where(df_chart2["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b"),
                                        np.where(df_chart2["variable"]=="Gross_Value", "#c5ddd4ff", "#d8c3af")
                                    )
                                )
        df_chart2["Sales Category"] = df_chart2["variable"].str.replace("_", " ", regex=False)
        # Show data in bar chart
        sales_horizontal_bar_chart(df_chart2, chart_title="Segmentation Sales Performance", x="value", y="Segmentation", variable="Sales Category", color="Hex_Code",
                                   subtitle_class="segmentation", subtitle_support_text1=selected_branch, subtitle_support_text2=None)
    
    # Sales by customer chart
    with col3:
        df_chart3 = df_sales_dashboard.groupby("Customer_Name")[["Gross_Value","Net_Value"]].sum().sort_values("Gross_Value", ascending=False).reset_index()
        df_chart3 = df_chart3.head(10)
        df_chart3 = df_chart3.melt(
                        id_vars=["Customer_Name"],
                        value_vars=["Gross_Value","Net_Value"],
                    )
        df_chart3["Hex_Code"] = np.where(df_chart3["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b")
        df_chart3["Sales Category"] = df_chart3["variable"].str.replace("_", " ", regex=False)
        # Show data in bar chart
        sales_horizontal_bar_chart(df_chart3, chart_title="Top 10 Customer by Sales", x="value", y="Customer_Name", variable="Sales Category", color="Hex_Code",
                                   subtitle_class="customer", subtitle_support_text1=selected_branch, subtitle_support_text2=selected_segment)


    # Pie chart and Line chart
    st.space()
    col1, col2 = st.columns([1,2])
    with col1:
        df_chart4 = df_ar_dashboard.groupby("Overdue")["Remaining_Amount"].sum().reset_index()
        df_chart4["AR Group"] = np.where(df_chart4["Overdue"]=="N", "Not Overdue", "Overdue")
        df_chart4["Hex_Code"] = np.where(df_chart4["Overdue"]=="N", "#7c9e92ff", "#c9996b")
        pie_chart1 = alt.Chart(
            df_chart4,
            title=alt.Title("Outstanding Account Receivable",
                subtitle=f"With overdue partition",
                fontSize=20,
                anchor="start",
                offset=20)
            ).mark_arc().encode(
                theta="Remaining_Amount",
                color=alt.Color("Hex_Code:N",
                    scale=None,
                    legend=alt.Legend(
                        orient="top",
                        title=None)
                    ),
                tooltip=["AR Group",
                        alt.Tooltip("Remaining_Amount:Q", title="Amount", format=",.0f")]
            ).configure_axis(
                domainColor="black",
                domainWidth=10,
                gridColor="black",
                gridWidth=2,
                gridOpacity=0.03
            ).properties(
                height=500
            )
        st.altair_chart(pie_chart1, width=450)

    with col2:
        df_chart5 = df_sales_dashboard.copy()
        df_chart5["Date_mmmYYYY"] = df_chart5["Date"].dt.strftime("%b %Y").astype(str)
        df_chart5["Date_mm"] = df_chart5["Date"].dt.strftime("%m").astype(int)
        df_chart5["Date_YYYY"] = df_chart5["Date"].dt.strftime("%Y").astype(int)
        df_chart5["Date_YYYYmm"] = df_chart5["Date"].dt.strftime("%Y%m").astype(int)
        df_chart5 = df_chart5.groupby(["Date_mmmYYYY","Date_mm","Date_YYYY","Date_YYYYmm"])[["Gross_Value","Net_Value"]].sum().reset_index()
        df_chart5 = df_chart5.sort_values(by=["Date_mm","Date_YYYY"], ascending=[True,True])
        df_chart5 = df_chart5.melt(
                    id_vars=["Date_mmmYYYY","Date_mm","Date_YYYY","Date_YYYYmm"],
                    value_vars=["Gross_Value","Net_Value"],
                )
        df_chart5["Hex_Code"] = np.where(df_chart5["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b")
        df_chart5["Sales Category"] = df_chart5["variable"].str.replace("_", " ", regex=False)
        df_chart5.rename(columns={"variable":"Sales",
                "value":"Sales Value",
                "Date_mmmYYYY":"Period"}, inplace=True)
        # Show data in line chart
        line_chart = alt.Chart(
                df_chart5,
                title=alt.Title("Annual Sales Trend",
                    fontSize=20,
                    anchor="start",
                    offset=0)
        ).mark_line(point=True, size=3).encode(
            x=alt.X("Period:N", 
                    sort=alt.EncodingSortField(field="Date_YYYYmm", order="ascending")
                ).axis(
                    title=None,
                    labelAngle=0,
                    labelFontWeight="bold"  
                ),
            y=alt.Y("Sales Value:Q").axis(
                title=None,
                labelFontWeight="bold"
            ),
            # color=alt.Color("Sales Category:N",
            #     legend=alt.Legend(
            #         orient="top",
            #         title=None)
            #     ),
            color=alt.Color(
                f"Hex_Code:N",
                scale=None,
                legend=alt.Legend(
                    orient="top",
                    title=None)
                ),
            tooltip=["Sales Category",
                    alt.Tooltip("Sales Value:Q", title="Amount", format=",.0f")]
        ).configure_axis(
            domainColor="black",
            domainWidth=10,
            gridColor="black",
            gridWidth=2,
            gridOpacity=0.03
        ).configure_point(
            size=100
        ).properties(
            height=500,
            width=850
        )
        st.altair_chart(line_chart)


    # Map chart
    df_chart6 = df_master_branch_customer.copy()
    df_chart6_cust = df_chart6[["Customer_ID","Customer_Name","Latitude_x","Longitude_x","Segmentation","City","Province"]].drop_duplicates()
    df_chart6_cust["Type"] = "Customer"
    df_chart6_brch = df_chart6[["Branch_ID","Branch_Name","Latitude_y","Longitude_y","City","Province"]].drop_duplicates()
    df_chart6_brch["Type"] = "Branch"
    df_chart6 = pd.concat([df_chart6_cust, df_chart6_brch])
    df_chart6["ID"] = df_chart6["Customer_ID"].fillna(df_chart6["Branch_ID"])
    df_chart6["Name"] = df_chart6["Customer_Name"].fillna(df_chart6["Branch_Name"])
    df_chart6["Longitude"] = df_chart6["Longitude_x"].fillna(df_chart6["Longitude_y"])
    df_chart6["Latitude"] = df_chart6["Latitude_x"].fillna(df_chart6["Latitude_y"])

    # Icon in map
    # df_chart6["Local_image"] = np.where(df_chart6["Type"]=="Branch", path+"pic18_scm.png", None)
    # df_chart6["Local_image"] = np.where(df_chart6["Type"]=="Branch", path+"pic.jpeg", None)
    # icon_data = {
    #         "width":512,
    #         "height":512,
    #         "anchorY":512,
    #         "mask":False
    #     }
    # df_chart6["icon_data"] = None
    # for i in df_chart6.index:
    #     df_chart6["icon_data"][i] = icon_data

    # Define the Initial View (Where the camera starts)
    center_lat = (df_chart6["Latitude"].max() + df_chart6["Latitude"].min())/2
    center_lon = (df_chart6["Longitude"].max() + df_chart6["Longitude"].min())/2
    lat_range = df_chart6["Latitude"].max() - df_chart6["Latitude"].min()
    lon_range = df_chart6["Longitude"].max() - df_chart6["Longitude"].min()
    lat_km = abs(lat_range) * 111.1
    lon_km = abs(lon_range) * 111.32 * math.cos(math.radians(center_lat))
    max_km = max(lat_km, lon_km)
    EARTH_EQUATOR_KM = 40075
    if selected_branch != None:
        dynamic_zoom = np.log2(EARTH_EQUATOR_KM / (max_km * 1.5))
    else:
        dynamic_zoom = 6.5
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=dynamic_zoom,
        pitch=0,  # Tilts the map for a 3D effect
        bearing=0
    )

    # Define the Layer
    layer1 = pdk.Layer(
        "ScatterplotLayer",
        df_chart6[df_chart6["Type"]=="Branch"],
        get_position="[Longitude, Latitude]",
        get_color='[0, 0, 0, 160]',    # RGBA color
        get_radius=200,                # Radius in meters
        pickable=True,                   # Allows for tooltips
        radius_min_pixels = 3,
        radius_max_pixels = 30 
    )
    layer1b = pdk.Layer(
        "IconLayer",
        df_chart6[df_chart6["Type"]=="Branch"],
        get_position="[Longitude, Latitude]",
        get_icon="icon_data",
        get_image_url="Local_image",
        get_size=4,
        size_scale=15,
        pickable=True                   # Allows for tooltips
    )
    layer2 = pdk.Layer(
        "ScatterplotLayer",
        df_chart6[df_chart6["Type"]=="Customer"],
        get_position="[Longitude, Latitude]",
        get_color='[0, 180, 255, 160]',    # RGBA color
        get_radius=200,                # Radius in meters
        pickable=True,                   # Allows for tooltips
        radius_min_pixels = 3,
        radius_max_pixels = 30 
    )

    # Render the Map
    st.pydeck_chart(
        pdk.Deck(
            map_style='light',
            initial_view_state=view_state,
            layers=[layer1, layer2, layer1b],        # layer drawn from bottom up
            tooltip={
                "html": '''
                    <b>ID:</b> {ID}
                    <br><b>Name:</b> {Name}
                    <br><b>Type:</b> {Type}
                    <br><b>City:</b> {City}
                    <br><b>Province:</b> {Province}
                    ''',
                "style": {"color": "white"}
            }
        )
    )

#----------------------------- Tab 3 : Customer Info
with tab3:
    # Select customer
    col1, col2 = st.columns(2)
    with col1:
        selected_customer = st.selectbox(label="Customer", placeholder="Select a customer...", options=customer_list, index=None)
    
    if (selected_customer!=None):
        # Filter data
        df_customer_selected = df_master_customer[df_master_customer["Customer_Name"]==selected_customer]
        df_customer_selected["TOP_Days"] = df_customer_selected["TOP_Days"].astype(str) + " days"
        customer_top = df_customer_selected["TOP_Days"].iloc[0]

        df_branch_selected = df_master_branch[df_master_branch["Branch_ID"]==df_customer_selected["Branch_ID"].iloc[0]]
        customer_branch_name = df_branch_selected["Branch_Name"].iloc[0]
        customer_branch_city = df_branch_selected["City"].iloc[0]
        customer_branch_prov = df_branch_selected["Province"].iloc[0]

        df_customer_transaction = df_sales_data[df_sales_data["Customer_ID"]==df_customer_selected["Customer_ID"].iloc[0]]
        df_customer_transaction["Date_ddmmmYYYY"] = df_customer_transaction["Date"].dt.strftime("%d %b %Y")
        customer_last_purchase_date = df_customer_transaction["Date_ddmmmYYYY"].max()
        customer_last_purchase_gross_value = df_customer_transaction[df_customer_transaction["Date"]==customer_last_purchase_date]["Gross_Value"].iloc[0]
        customer_last_purchase_net_value = df_customer_transaction[df_customer_transaction["Date"]==customer_last_purchase_date]["Net_Value"].iloc[0]

        df_customer_ar = df_ar_data[df_ar_data["Customer_ID"]==df_customer_selected["Customer_ID"].iloc[0]]
        df_customer_ar_period = df_customer_ar.groupby("EOM_Period")["Remaining_Amount"].sum()
        customer_ar = df_customer_ar["Remaining_Amount"].sum()

        df_show_table = df_customer_selected.copy()
        df_show_table["Branch_Name"] = customer_branch_name
        df_show_table["City"] = customer_branch_city
        df_show_table["Province"] = customer_branch_prov
        df_show_table["Last Purchase Date"] = customer_last_purchase_date
        df_show_table["Last Purchase Gross Value"] = f"IDR {customer_last_purchase_gross_value:,}"
        df_show_table["Last Purchase Net Value"] = f"IDR {customer_last_purchase_net_value:,}"
        df_show_table["Outstanding AR"] = f"IDR {customer_ar:,}"

        df_show_table = df_show_table[["Customer_ID", 
                                "Customer_Name", 
                                "Segmentation", 
                                "Longitude",
                                "Latitude",
                                "Last Purchase Date", 
                                "Last Purchase Gross Value",
                                "Last Purchase Net Value",  
                                "Outstanding AR",
                                "TOP_Days",
                                "Branch_ID", 
                                "Branch_Name", 
                                "City", 
                                "Province"]]
        df_show_table.rename(columns={"Customer_ID":"Customer ID",
                                "Customer_Name":"Customer Name",
                                "Branch_ID":"Branch ID",
                                "Branch_Name":"Branch Name",
                                "TOP_Days":"TOP"}, inplace=True)
        df_show_table_T = df_show_table.T

        df_show_map = pd.concat([df_customer_selected, df_branch_selected])
        df_show_map["ID"] = df_show_map["Customer_ID"].fillna(df_show_map["Branch_ID"])
        df_show_map["Name"] = df_show_map["Customer_Name"].fillna(df_show_map["Branch_Name"])
        df_show_map["Segmentation"] = df_show_map["Segmentation"].fillna("Company Branch")
        df_show_map["City"] = df_show_map["City"].fillna(df_show_map[df_show_map["Segmentation"]=="Company Branch"]["City"].iloc[0])
        df_show_map["Province"] = df_show_map["Province"].fillna(df_show_map[df_show_map["Segmentation"]=="Company Branch"]["Province"].iloc[0])
        df_show_map = df_show_map[["ID", 
                                "Name", 
                                "Segmentation", 
                                "Longitude",
                                "Latitude",
                                "City", 
                                "Province"]]

        # col1, col2 = st.columns(2)
        with col1:
            # Show customer info
            # st.dataframe(
            #     df_show_table_T,
            #     column_config={
            #         "Col1": st.column_config.Column(width=300),
            #         "Col2": st.column_config.Column(width=300)
            #     }
            # )
            st.table(df_show_table_T.style.hide(axis="columns"))
        with col2:
            # Define the Initial View (Where the camera starts)
            lat_cust = df_show_map[df_show_map["Segmentation"]!="Company Branch"]["Latitude"].iloc[0]
            lon_cust = df_show_map[df_show_map["Segmentation"]!="Company Branch"]["Longitude"].iloc[0]
            lat_brch = df_show_map[df_show_map["Segmentation"]=="Company Branch"]["Latitude"].iloc[0]
            lon_brch = df_show_map[df_show_map["Segmentation"]=="Company Branch"]["Longitude"].iloc[0]
            init_lat = (lat_cust + lat_brch)/2
            init_long = (lon_cust + lon_brch)/2
            lat_diff = lat_cust - lat_brch
            long_diff = lon_cust - lon_brch
            lat_km = abs(lat_diff) * 111.1
            lon_km = abs(long_diff) * 111.32 * math.cos(math.radians(center_lat))
            max_km = max(lat_km, lon_km)
            dynamic_zoom = np.log2(EARTH_EQUATOR_KM / (max_km*3))
            view_state = pdk.ViewState(
                latitude=init_lat,
                longitude=init_long,
                zoom=dynamic_zoom,
                pitch=0,  # Tilts the map for a 3D effect
                bearing=0
            )
            # Layer customer & branch
            df_show_map.loc[df_show_map["Segmentation"]=="Company Branch", "Color"] = "[255, 0, 0]"
            df_show_map.loc[df_show_map["Segmentation"]!="Company Branch", "Color"] = "[0, 0, 255]"
            df_show_map["Color"] = df_show_map["Color"].apply(ast.literal_eval)
            df_show_map[["R","G","B"]] = pd.DataFrame(df_show_map["Color"].tolist(), index=df_show_map.index)
            layer1 = pdk.Layer(
                "ScatterplotLayer",
                df_show_map,
                get_position='[Longitude, Latitude]',
                get_fill_color='[R, G, B]',        # RGB color
                filled=True,
                get_radius=100,                # Radius in meters
                pickable=True,                   # Allows for tooltips
                radius_min_pixels = 3,
                radius_max_pixels = 30 
            )
            # layer2 = pdk.Layer(
            #     "IconLayer",
            #     df_show_map,
            #     get_position='[Longitude, Latitude]',
            #     get_icon="",
            #     get_size=,
            #     size_scale=,                  # Allows for tooltips
            # )

            # Render the Map
            st.pydeck_chart(pdk.Deck(
                map_style='light',
                initial_view_state=view_state,
                layers=[layer1],        # layer drawn from bottom up
                tooltip={
                    "html": '''
                        <b>ID:</b> {ID}
                        <br><b>Name:</b> {Name}
                        <br><b>Segmentation:</b> {Segmentation}
                        <br><b>City:</b> {City}
                        <br><b>Province:</b> {Province}
                        ''',
                    "style": {"color": "white"}
                }
            ))

        st.space()
        st.space()
        col1, col2 = st.columns([3,2])
        with col1:
            # Prepare data
            df_customer_transaction2 = df_customer_transaction.copy()
            df_customer_transaction2["Date_mmmYYYY"] = df_customer_transaction["Date"].dt.strftime("%b %Y").astype(str)
            df_customer_transaction2["Date_mm"] = df_customer_transaction["Date"].dt.strftime("%m").astype(int)
            df_customer_transaction2["Date_YYYY"] = df_customer_transaction["Date"].dt.strftime("%Y").astype(int)
            df_customer_transaction2["Date_YYYYmm"] = df_customer_transaction["Date"].dt.strftime("%Y%m").astype(int)
            df_customer_transaction2 = df_customer_transaction2.groupby(["Date_mmmYYYY","Date_mm","Date_YYYY","Date_YYYYmm"])[["Gross_Value","Net_Value"]].sum().reset_index()
            df_customer_transaction2 = df_customer_transaction2.sort_values(by=["Date_mm","Date_YYYY"], ascending=[True,True])
            df_customer_transaction2 = df_customer_transaction2.melt(
                                            id_vars=["Date_mmmYYYY","Date_mm","Date_YYYY","Date_YYYYmm"],
                                            value_vars=["Gross_Value","Net_Value"],
                                        )
            df_customer_transaction2["Hex_Code"] = np.where(df_customer_transaction2["variable"]=="Gross_Value", "#7c9e92ff", "#c9996b")
            df_customer_transaction2["Sales Category"] = df_customer_transaction2["variable"].str.replace("_", " ", regex=False)
            df_customer_transaction2.rename(columns={"variable":"Sales",
                                    "value":"Sales Value",
                                    "Date_mmmYYYY":"Period"}, inplace=True)
            
            # Show data in line chart
            line_chart = alt.Chart(
                    df_customer_transaction2,
                    title=alt.Title("Sales Trend from Customer",
                        fontSize=40,
                        anchor="start",
                        offset=0)
            ).mark_line(point=True, size=3).encode(
                x=alt.X("Period:N", 
                        sort=alt.EncodingSortField(field="Date_YYYYmm", order="ascending")
                    ).axis(
                        title=None,
                        labelAngle=0,
                        labelFontWeight="bold"  
                    ),
                y=alt.Y("Sales Value:Q").axis(
                    title=None,
                    labelFontWeight="bold"
                ),
                # color=alt.Color("Sales Category:N",
                #     legend=alt.Legend(
                #         orient="top",
                #         title=None)
                #     ),
                color=alt.Color(
                    f"Hex_Code:N",
                    scale=None,
                    legend=alt.Legend(
                        orient="top",
                        title=None)
                    ),
                tooltip=["Sales Category",
                        alt.Tooltip("Sales Value:Q", title="Amount", format=",.0f")]
            ).configure_axis(
                domainColor="black",
                domainWidth=10,
                gridColor="black",
                gridWidth=2,
                gridOpacity=0.03
            ).configure_point(
                size=100
            ).properties(
                height=500,
                width=850
            )
            st.altair_chart(line_chart)
        
        with col2:
            df_customer_ar2 = df_customer_ar.copy()
            df_customer_ar2["AR_Aging"] = (df_customer_ar2["EOM_Period"] - df_customer_ar2["Invoice_Date"]).dt.days
            conditions = [
                (df_customer_ar2["AR_Aging"] <= 30),
                (df_customer_ar2["AR_Aging"] <= 60),
                (df_customer_ar2["AR_Aging"] <= 90),
                (df_customer_ar2["AR_Aging"] <= 180),
                (df_customer_ar2["AR_Aging"] <= 360)
            ]
            values = [
                "0 - 30 days",
                "31 - 60 days",
                "61 - 90 days",
                "91 - 180 days",
                "181 - 360 days"
            ]
            values2 = [
                1,
                2,
                3,
                4,
                5
            ]
            values3 = [
                30,
                60,
                90,
                180,
                360
            ]
            values4 = [
                "red",
                "red",
                "red",
                "red",
                "red"
            ]
            df_customer_ar2["AR_Aging_Group"] = np.select(conditions, values, default="> 360 days")
            df_customer_ar2["AR_Aging_Group_Order"] = np.select(conditions, values2, default=99)
            df_customer_ar2["Color"] = np.select(conditions, values4, default="gray")
            df_customer_ar2["Max_Aging_in_Group"] = np.select(conditions, values3, default=999)
            df_customer_ar2 = df_customer_ar2.groupby(["Customer_ID","AR_Aging_Group","AR_Aging_Group_Order","Color","Max_Aging_in_Group"])["Remaining_Amount"].sum().reset_index().sort_values("AR_Aging_Group_Order", ascending=True)
            df_customer_ar2 = pd.merge(df_customer_ar2, df_master_customer, on="Customer_ID", how="left")
            df_customer_ar2["Color_Index"] = np.where(
                                                df_customer_ar2["Max_Aging_in_Group"] == df_customer_ar2["TOP_Days"], 
                                                5,
                                                np.where( 
                                                    df_customer_ar2["Max_Aging_in_Group"] != 999,
                                                    df_customer_ar2["AR_Aging_Group_Order"],
                                                    df_customer_ar2[df_customer_ar2["AR_Aging_Group_Order"]!=99]["AR_Aging_Group_Order"].max() + 1
                                                )  - df_customer_ar2[df_customer_ar2["Max_Aging_in_Group"] == df_customer_ar2["TOP_Days"]]["AR_Aging_Group_Order"].iloc[0] + 5
                                            ) 
            df_customer_ar2 = pd.merge(df_customer_ar2, df_ar_color, on="Color_Index", how="left")

            # Show data in bar chart
            bar_chart = alt.Chart(
                df_customer_ar2,
                title=alt.Title("AR Value from Customer",
                    subtitle=f"with TOP {customer_top}",
                    fontSize=40,
                    anchor="start",
                    offset=20)
            ).mark_bar().encode(
                x=alt.X("Remaining_Amount:Q", 
                        sort=alt.EncodingSortField(field="Date_YYYYmm", order="ascending")
                    ).axis(
                        title=None,
                        labelAngle=0,
                        labelFontWeight="bold"  
                    ),
                y=alt.Y("AR_Aging_Group:N",
                        sort=alt.EncodingSortField(field="AR_Aging_Group_Order", order="ascending")
                    ).axis(
                        title=None,
                        labelAngle=0,
                        labelFontWeight="bold"  
                    ),
                color=alt.Color("Hex_Code:N",
                    scale=None
                    ),
                tooltip=[alt.Tooltip("AR_Aging_Group:N", title="AR Aging Group"),
                        alt.Tooltip("Remaining_Amount:Q", title="Amount", format=",.0f"),
                        alt.Tooltip("Visual Intensity:N", title="TOP Status")]
            ).configure_axis(
                domainColor="black",
                domainWidth=10,
                gridColor="black",
                gridWidth=2,
                gridOpacity=0.03
            ).properties(
                height=500
            )
            st.altair_chart(bar_chart)

    else:
        st.write("Please select a customer to see details.")

print("End printing")
