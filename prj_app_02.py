import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import calendar
import datetime
from lib_function import insert_icon, sales_horizontal_bar_chart

print("-----------------------------------------------------------------------------------------------------------------------------------------")
print("Start printing")

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set folder path
# path = "B. Project/whs_monitor_data/"
path = ""

#----------------------------- Read data file
df_master_branch = pd.read_csv(path+"master_warehouse_branches.csv", sep=",")
df_master_lotno = pd.read_csv(path+"master_product_batches.csv", sep=",")
df_master_product = pd.read_csv(path+"master_products.csv", sep=",")
df_master_product = df_master_product.merge(df_master_lotno, on="Product_ID", how="inner")

df_inventory = pd.read_csv(path+"warehouse_stock_inventory_2025.csv", sep=",")
df_inventory["Month_Name"] = pd.to_datetime(df_inventory["Stock_Date"],format="%m/%d/%Y").dt.strftime("%b")
df_sales = pd.read_csv(path+"warehouse_sales_2025.csv", sep=",")
df_sales["Month_Num"] = pd.to_datetime(df_sales["Sales_Date"],format="%Y-%m").dt.strftime("%m").astype(int)

branch_list = df_master_branch["Branch_ID"].unique()
product_list = df_master_product["Product_ID"].unique()
year_list = 2025
month_list = ["All Month"]
for x in range (0,6):
    month_list.append(calendar.month_abbr[x+7])

tab1, tab2 = st.tabs(["Project Description","Warehouse Monitoring Dashboard"])
#----------------------------- Tab 1 : Project Description
with tab1:
    st.header("Introduction")
    st.html('''<p style="text-align:justify;">AAM is a pharmaceuticals and medical devices distributor company that distributes its product across Indonesia. 
        This company has 38 branches and over 100,000 customer spread over Indonesia from Aceh to Jayapura. A lot of activities done by its branches make the 
        headquarter must have a reliable data to monitor its operation, including stock and warehouse performance.</p>
            
        <p style="text-align:justify;">In order to monitor its warehouse management, the compoany need to have a big overview about how its inventory are stored. Several KPI
        are used to monitor the warehouse performance. Its desire are want to have a short period of inventory stored and use a lot of space for valuable inventory (can be sold).
        Maintaining a lot of inventory data and do calculation from it requires a great effort for the company. So this dashboard is developed to help the company monitor its 
        warehouse management system and "finding a spot" in a quick way. This project showcase demonstrate a project that I have done in the company. The data used in this showcase
        are simplified just to show how the data processing works.</p>''')
    
    st.subheader("Data Model")
    col1, col2 = st.columns(2)
    with col1:
        st.html('''<p style="text-align:justify;">There are 5 data used in this showcase, two transaction data and three master data. The data structure are simplified until there are only information we need 
            to build this project. The picture beside shows the data structure and their relation.</p>
                
            <p style="text-align:justify;">First we have <b>Sales</b> transaction data, this is the table to record transactions that have been made in each warehouse. In this table, we will find 
            5 attributes or columns that will give information about each transaction happen. The <b>Sales_Date</b> tells us when the transaction happen. It presents value with date format. 
            The <b>Branch_ID</b> tells us where the transaction happen. The <b>Lot_ID</b> is the product lot number that involved in the transaction. The detail information about product can be found in Master_Product_Lot and
            Master_Product. The <b>Sales_Quantity</b> and <b>Sales_Vaue</b> are the transaction measure.</p>
                
            <p style="text-align:justify;">And then we have <b>Stock</b> data, this is the table to record the snapshot of stocks in each warehouse every end of month. In this data, 
            there are 4 attributes or columns that will give detail information. <b>Stock_Date</b> tells us about when the snapshot happen to support calculation about how long
            that a product has been expired. The <b>Branch_ID</b> is the warehouse identity and the <b>Lot_ID</b> is the product identity. They have a similar function with ones
            in the Sales data. The <b>Product_Quantity</b> is quantity of product stored in the warehouse at the certain period.
            
            <p style="text-align:justify;">Next we have <b>Master_Branch</b> data, this is the table to describe our warehouse. It contains <b>Branch_ID</b> as the warehouse 
            identifier, <b>Branch_Name</b> as the name of warehouse, and <b>Branch_Capacity_m3</b> as the warehouse capacity presented in meter cubic.</p>
            
            <p style="text-align:justify;">We also have <b>Master_Product_Lot</b> data, this is the table to inform the batch number of products. It contains <b>Lot_ID</b> as the batch 
            identifier, <b>Product_ID</b> as the product identifier, and <b>Expired_Date</b>. In this case, there is only one expired date for one lot ID.</p>
            ''')
    with col2:
        insert_icon(path, "whs_relation_model.png")
    st.html('''<p style="text-align:justify;">Finally we have <b>Master_Product</b> data, this is the tabel to store detail information about product. It contains
        <b>Product_ID</b> and <b>Product_Name</b> as the identity of product, <b>Principal_ID</b> and <b>Principal_Name</b> as the identity of the manufacturer, also <b>Product_Value</b>
        and <b>Product_Volume_cm3</b> as the measurement for each product.</p>''')
    
    st.subheader("Special KPI")
    st.html('''<p style="text-align:justify;">There is a "special KPI" used in the dashboard. This KPI is common in the term of Supply Chain Management (SCM), it is <i>Day of Inventory</i> 
        (DOI). DOI is a metric to calculate how long the inventory are stored in a warehouse, so this KPI is served in time unit.
        It can be calculated with formula below.</p>''')
            
    st.latex(r'''
        \text{DOI} = \frac{\text{Ending period stock value}}{\text{Average Sales Value}}''')
        
    st.html('''<p style="text-align:justify;">The SCM team said that the smaller DOI give the greater warehouse performance. Why? Because from the formula, it indicates the inventory did not 
        take a long time to be stored before it went out from the warehouse. The inventory are "sold quickly". So the SCM team always use this metric to measure every warehouse
        performance in every month. With this historical measure, the team also can spot what the cause of number and make improvements from it.</p>

        <p style="text-align:justify;">In Kaizen, we know that to implement continuous improvements, we need to reduce or even eliminate the wastes. One of them is <i>inventory</i>, it means how much and how long
        we stored our inventory in a warehouse. We need to reducce inventory in a term of not to store too many inventory for too long. Just store our inventory does not give an
        additional value to the goods. Reduce the number of inventory gives us more space that can be utilized.</p>

        <p style="text-align:justify;">From the formula, we see that there is no strict rules about the scope of average sales. We can calculte the average sales from the last 
        week or from last three months or even from the last year sales. This condition is determined by the company policy or by the agreement with the product owner. For more
        complex analysis, forecesting data also can be included to the formula. In this show case, we will calculate DOI by dividing the value of our stock at the end of month 
        with the last three months average sales (in days). So we will approach this formula below.</p>
        ''')
            
    st.latex(r'''
        \text{DOI (days)} = \frac{\text{Ending of month stock value (IDR)}}{\text{Monthly average Sales (IDR/month)}} \times 30 \text{ days/month}
        ''')
    
    st.subheader("Product Result")
    st.html('''<p style="text-align:justify;">Text</p>''')
    
    st.subheader("Future Improvements")
    st.html('''<p style="text-align:justify;">Text</p>''')
    

#----------------------------- Tab 2 : Warehouse Monitoring Dashboard
with tab2:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        selected_year = st.selectbox(label="Year", placeholder="Select a year...", options=year_list, index=0)
        selected_month = st.selectbox(label="Month", placeholder="Select a month...", options=month_list, index=0)
        if(selected_month!="All Month"):
            df_inventory = df_inventory[df_inventory["Month_Name"]==selected_month]
            df_sales = df_sales[df_sales["Month_Num"]>=datetime.datetime.strptime(selected_month, "%b").month-2]
            df_sales = df_sales[df_sales["Month_Num"]<=datetime.datetime.strptime(selected_month, "%b").month]
        elif(selected_month=="All Month"):
            df_inventory = df_inventory[df_inventory["Month_Name"].isin(["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])]
            df_sales = df_sales[df_sales["Month_Num"]>=datetime.datetime.strptime("Jul", "%b").month-2]
    with col2:
        selected_branch = st.selectbox(label="Branch", placeholder="Select a branch...", options=branch_list, index=None)
        if(selected_branch!=None):
            df_master_branch = df_master_branch[df_master_branch["Branch_ID"]==selected_branch]
            df_inventory = df_inventory[df_inventory["Branch_ID"]==selected_branch]
            df_sales = df_sales[df_sales["Branch_ID"]==selected_branch]
        selected_product = st.selectbox(label="Product", placeholder="Select a product...", options=product_list, index=None)
        if(selected_product!=None):
            df_master_product = df_master_product[df_master_product["Product_ID"]==selected_product]
            df_master_lotno = df_master_lotno[df_master_lotno["Product_ID"]==selected_product]
            batch_list = df_master_lotno["Lot_ID"].unique()
            df_inventory = df_inventory[df_inventory["Lot_ID"].isin(batch_list)]
            df_sales = df_sales[df_sales["Lot_ID"].isin(batch_list)]

print("End printing")
