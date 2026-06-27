import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import calendar
import datetime
from lib_function import insert_icon, line_chart_inventory, bar_chart_inventory, line_chart_inventory_with_capacity

print("-----------------------------------------------------------------------------------------------------------------------------------------")
print("Start printing")

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set folder path
path = "B. Project/whs_monitor_data/"
# path = "whs_monitor_data/"

#----------------------------- Read data file
df_master_branch = pd.read_csv(path+"master_warehouse_branches.csv", sep=",")
df_master_lotno = pd.read_csv(path+"master_product_batches.csv", sep=",")
df_master_product = pd.read_csv(path+"master_products.csv", sep=",")
df_master_product = df_master_product.merge(df_master_lotno, on="Product_ID", how="inner")
df_master_product["Principal_ID_Name"] = df_master_product["Principal_ID"] + " / " + df_master_product["Principal_Name"]

df_inventory = pd.read_csv(path+"warehouse_stock_inventory_2025.csv", sep=",")
df_inventory["Month_Name"] = pd.to_datetime(df_inventory["Stock_Date"],format="%m/%d/%Y").dt.strftime("%b")
df_inventory["Month_Num"] = pd.to_datetime(df_inventory["Stock_Date"],format="%m/%d/%Y").dt.strftime("%m").astype(int)
df_sales = pd.read_csv(path+"warehouse_sales_2025.csv", sep=",")
df_sales["Month_Num"] = pd.to_datetime(df_sales["Sales_Date"],format="%Y-%m").dt.strftime("%m").astype(int)

branch_list = df_master_branch["Branch_ID"].unique()
principal_list = df_master_product["Principal_ID_Name"].unique()
product_list = df_master_product["Product_ID"].unique()
year_list = 2025
month_list = ["All Month"]
for x in range (0,6):
    month_list.append(calendar.month_abbr[x+7])

tab1, tab2, tab3 = st.tabs(["Project Description","Warehouse Monitoring Dashboard","Warehouse & Inventory Analysis"])
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
            
            <p style="text-align:justify;">Finally we have <b>Master_Product</b> data, this is the tabel to store detail information about product. It contains
            <b>Product_ID</b> and <b>Product_Name</b> as the identity of product, <b>Principal_ID</b> and <b>Principal_Name</b> as the identity of the manufacturer, also <b>Product_Value</b>
            and <b>Product_Volume_cm3</b> as the measurement for each product.</p>''')
    with col2:
        insert_icon(path, "whs_relation_model.png")
    
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
    st.html('''<p style="text-align:justify;">As the result, there will be a monitoring dashboard to monitor all warehouse performance. The KPIs show inventory metrics 
        in quantity, value, and volume. The warehouse capacity usage shows the ratio between inventory volume compared to warehouse capacity in percentage. Also the
        special KPI (Day of Inventory) shows how long the inventory stays in the warehouse. The line charts show the movement of metrics across the year and the bar charts
        show the comparation of metrics between principals.</p>
        
        <p style="text-align:justify;">There is also an additional section for warehouse analysis. In the warehouse, there are many stocks that are already expired (recorded
        in every period). The analysis shows about what if all the expired stocks are eliminated (returned or destroyed) from the warehouse. ALl the expired inventory value from each principal is 
        shown in a bar chart. If they can be returned, it means the company can save not only space in warehouse but also some cash. What will happen to the metrics because 
        of the inventory reduction are illustrated by the line charts.</p>''')
    
    st.subheader("Future Improvements")
    st.html('''<p style="text-align:justify;">To achieve a better warehouse performance, each warehouse must operate based on standard or agreement. For example, there is an 
        agreement about the best DOI for each principal how to calculate it (based on some period of average sales). So the warehouse can maintain the principal's products to move faster. If the warehouse DOI is greater than the agreement,
        we can do further analysis to find what product that make up the number and what the reason (maybe the expired inventory in warehouse, too many product return from customer,
        or issue in sales performance).</p>''')
    

#----------------------------- Tab 2 : Warehouse Monitoring Dashboard
with tab2:
    # KPI card
    col1, col2, col3, col4 = st.columns(4)
    df_inventory_kpi = df_inventory.copy()
    df_sales_kpi = df_sales.copy()
    with col1:
        selected_year = st.selectbox(label="Year", placeholder="Select a year...", options=year_list, index=0)
        selected_month = st.selectbox(label="Month", placeholder="Select a month...", options=month_list, index=0)
        if(selected_month!="All Month"):
            month = selected_month
        elif(selected_month=="All Month"):
            month = "Dec"
        df_inventory_kpi = df_inventory_kpi[df_inventory_kpi["Month_Name"]==month]
        df_sales_kpi = df_sales_kpi[df_sales_kpi["Month_Num"]>=datetime.datetime.strptime(month, "%b").month-2]
        df_sales_kpi = df_sales_kpi[df_sales_kpi["Month_Num"]<=datetime.datetime.strptime(month, "%b").month]

        selected_branch = st.selectbox(label="Branch", placeholder="Select a branch...", options=branch_list, index=None)
        if(selected_branch!=None):
            df_master_branch = df_master_branch[df_master_branch["Branch_ID"]==selected_branch]
            df_inventory_kpi = df_inventory_kpi[df_inventory_kpi["Branch_ID"]==selected_branch]
            df_sales_kpi = df_sales_kpi[df_sales_kpi["Branch_ID"]==selected_branch]

        selected_principal = st.selectbox(label="Principal", placeholder="Select a principal...", options=principal_list, index=None)
        if(selected_principal!=None):
            df_master_product = df_master_product[df_master_product["Principal_ID_Name"]==selected_principal]
            batch_list = df_master_product["Lot_ID"].unique()
            df_inventory_kpi = df_inventory_kpi[df_inventory_kpi["Lot_ID"].isin(batch_list)]
            df_sales_kpi = df_sales_kpi[df_sales_kpi["Lot_ID"].isin(batch_list)]

    with col2:
        st.metric("Company Branch", df_master_branch["Branch_ID"].nunique(), border=True)
        st.metric("Principal", df_master_product["Principal_ID"].nunique(), border=True)
        st.metric("Product", df_master_product["Product_ID"].nunique(), border=True)

    with col3:
        df_inventory_product_kpi = df_inventory_kpi.merge(df_master_product, on="Lot_ID", how="inner")
        eom_product_qty = df_inventory_product_kpi["Product_Qty"].sum()
        st.metric("Inventory Quantity", f"{eom_product_qty:,}", border=True)

        df_inventory_product_kpi["Inventory_Value"] = df_inventory_product_kpi["Product_Qty"] * df_inventory_product_kpi["Product_Value"]
        eom_product_value = df_inventory_product_kpi["Inventory_Value"].sum()
        st.metric("Inventory Value", f"{eom_product_value:,}", border=True)

        df_inventory_product_kpi["Inventory_Volume"] = df_inventory_product_kpi["Product_Qty"] * df_inventory_product_kpi["Product_Volume_cm3"] / 1000000
        eom_product_volume = df_inventory_product_kpi["Inventory_Volume"].sum()
        st.metric("Inventory Volume (m3)", f"{round(eom_product_volume,2):2,}", border=True)

    with col4:
        whs_capacity = df_master_branch["Branch_Capacity_m3"].sum()
        st.metric("Warehouse Capacity (m3)", f"{round(whs_capacity,0):2,}", border=True)

        whs_capacity_usage = eom_product_volume/whs_capacity*100
        st.metric("Warehouse Capacity Usage", f"{round(whs_capacity_usage,2):2,} %", border=True)
        
        avg_whs_sales = df_sales_kpi["Sales_Value"].sum()/3
        whs_doi = eom_product_value / avg_whs_sales * 30
        st.metric("DOI (days)", f"{round(whs_doi,2):2,}", border=True)

    # Transaction data join master data
    df_inventory = df_inventory.merge(df_master_product, on="Lot_ID", how="inner")
    df_inventory = df_inventory.merge(df_master_branch, on="Branch_ID", how="inner")
    df_inventory["Inventory_Value"] = df_inventory["Product_Qty"] * df_inventory["Product_Value"]
    df_inventory["Inventory_Volume_m3"] = df_inventory["Product_Qty"] * df_inventory["Product_Volume_cm3"] / 1000000
    df_inventory["Stock_Date"] = pd.to_datetime(df_inventory['Stock_Date'], errors='coerce')
    df_inventory["Period"] = df_inventory["Stock_Date"].dt.strftime("%b %Y").astype(str)
    df_inventory["Date_YYYYmm"] = df_inventory["Stock_Date"].dt.strftime("%Y%m").astype(int)

    df_sales = df_sales.merge(df_master_product, on="Lot_ID", how="inner")
    df_sales = df_sales.merge(df_master_branch, on="Branch_ID", how="inner")

    # As of month dataframe for sales and inventory
    base_data = np.arange(1, 13)
    df_as_of_month = None
    df_as_of_month_sales = None
    df_as_of_month_inventory = None
    for i in range (0,3):
        df_as_of_month_data = pd.DataFrame({
            'Month_Num': base_data,
            'As_of_Month_Num': base_data + i
        })
        df_as_of_month_sales = pd.concat([df_as_of_month_sales, df_as_of_month_data], ignore_index=True).sort_values(by=["As_of_Month_Num","Month_Num"], ascending=[False,False])
        df_as_of_month_sales = df_as_of_month_sales[df_as_of_month_sales["As_of_Month_Num"]<=12]
        df_as_of_month_sales["Type"] = "Sales"
    for i in range (0,1):
        df_as_of_month_data = pd.DataFrame({
            'Month_Num': base_data,
            'As_of_Month_Num': base_data + i
        })
        df_as_of_month_inventory = pd.concat([df_as_of_month_inventory, df_as_of_month_data], ignore_index=True).sort_values(by=["As_of_Month_Num","Month_Num"], ascending=[False,False])
        df_as_of_month_inventory = df_as_of_month_inventory[df_as_of_month_inventory["As_of_Month_Num"]<=12]
        df_as_of_month_inventory["Type"] = "Inventory"
        
    df_as_of_month = pd.concat([df_as_of_month_sales, df_as_of_month_inventory], ignore_index=True).sort_values(by=["Type","As_of_Month_Num","Month_Num"], ascending=[True,False,False])
    df_as_of_month["As_of_EOM"] = pd.to_datetime(dict(year=selected_year, month=df_as_of_month['As_of_Month_Num'], day=1)) + pd.offsets.MonthEnd(0)
    df_as_of_month["As_of_Month_Name"] = df_as_of_month["As_of_EOM"].dt.strftime("%b").astype(str)
    df_as_of_month["As_of_Period"] = df_as_of_month["As_of_EOM"].dt.strftime("%b %Y").astype(str)
    df_as_of_month["As_of_Date_YYYYmm"] = df_as_of_month["As_of_EOM"].dt.strftime("%Y%m").astype(int)

    col1, col2 = st.columns(2)
    with col1:
        # Inventory value per month
        df_chart1 = df_inventory.copy()
        df_chart1 = df_chart1.groupby(["Month_Name","Period","Date_YYYYmm"])["Inventory_Value"].sum().reset_index()
        line_chart_inventory(df_chart1, "Month_Name", "Inventory_Value", "Inventory Value", "", "Date_YYYYmm", "Inventory Value")

        # Inventory volume per month
        df_chart3 = df_inventory.copy()
        df_chart3 = df_chart3.groupby(["Month_Name","Period","Date_YYYYmm"])["Inventory_Volume_m3"].sum().reset_index()
        line_chart_inventory(df_chart3, "Month_Name", "Inventory_Volume_m3", "Inventory Volume (m3)", "", "Date_YYYYmm", "Inventory Volume (m3)")

        # DOI per month
        df_chart2_inventory = df_inventory.copy()
        df_chart2_inventory = df_chart2_inventory.merge(df_as_of_month[df_as_of_month["Type"]=="Inventory"], on="Month_Num", how="inner")
        df_chart2_inventory = df_chart2_inventory.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Inventory_Value"].sum().reset_index()
        df_chart2_sales = df_sales.copy()
        df_chart2_sales = df_chart2_sales.merge(df_as_of_month[df_as_of_month["Type"]=="Sales"], on="Month_Num", how="inner")
        df_chart2_sales = df_chart2_sales.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Sales_Value"].sum().reset_index()
        df_chart2 = df_chart2_inventory.merge(df_chart2_sales, on=["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm"], how="inner")
        df_chart2["DOI"] = df_chart2["Inventory_Value"] / (df_chart2["Sales_Value"]/3) * 30
        line_chart_inventory(df_chart2, "As_of_Month_Name", "DOI", "Day of Inventory", "", "As_of_Date_YYYYmm", "DOI")
    
    with col2:
        period = "per " + str(month) + " " + str(selected_year)
        # Inventory value per principal
        df_chart2 = df_inventory_product_kpi.copy()
        df_chart2 = df_chart2.groupby(["Principal_ID","Principal_ID_Name"])["Inventory_Value"].sum().reset_index()
        bar_chart_inventory(df_chart2, "Inventory Value by Principal", period, "Principal_ID", "Inventory_Value")
        
        # Inventory volume per principal
        df_chart3 = df_inventory_product_kpi.copy()
        df_chart3["Inventory_Volume_m3"] = df_chart3["Product_Qty"] * df_chart3["Product_Volume_cm3"] / 1000000
        df_chart3 = df_chart3.groupby(["Principal_ID","Principal_ID_Name"])["Inventory_Volume_m3"].sum().reset_index()
        bar_chart_inventory(df_chart3, "Inventory Volume (m3) by Principal", period, "Principal_ID", "Inventory_Volume_m3")
        
        # DOI per principal
        df_inventory_product_kpi = df_inventory_product_kpi.merge(df_as_of_month[df_as_of_month["Type"]=="Inventory"], on="Month_Num", how="inner")
        df_inventory_product_kpi = df_inventory_product_kpi.groupby(["Principal_ID","Principal_ID_Name","As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Inventory_Value"].sum().reset_index()
        df_sales_kpi = df_sales_kpi.merge(df_master_product, on="Lot_ID", how="inner")
        df_sales_kpi = df_sales_kpi.merge(df_as_of_month[df_as_of_month["Type"]=="Sales"], on="Month_Num", how="inner")
        df_sales_kpi = df_sales_kpi.groupby(["Principal_ID","Principal_ID_Name","As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Sales_Value"].sum().reset_index()
        df_chart4 = df_inventory_product_kpi.merge(df_sales_kpi, on=["Principal_ID","Principal_ID_Name","As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm"], how="inner")
        df_chart4["DOI"] = df_chart4["Inventory_Value"] / (df_chart4["Sales_Value"]/3) * 30
        bar_chart_inventory(df_chart4, "Day of Inventory", period, "Principal_ID", "DOI")

#----------------------------- Tab 3 : Warehouse & Inventory Analysis
with tab3:
    if selected_branch==None:
        st.write("Please select a branch in the previous page.")
    else:
        # st.write("Selected branch :", selected_branch)
        # st.write("On period :", period)
        df_inventory2 = df_inventory.copy()
        df_inventory2["Inventory_Volume"] = df_inventory2["Product_Qty"] * df_inventory2["Product_Volume_cm3"] / 1000000
        df_inventory2['Expiry_Date'] = pd.to_datetime(df_inventory2['Expiry_Date'], format="%m/%d/%Y")
        df_inventory2["Expired_Aging"] = (df_inventory2["Expiry_Date"] - df_inventory2['Stock_Date']).dt.days
        df_inventory2["Expired_Flag"] = df_inventory2.apply(lambda x: "Y" if x["Expired_Aging"] < 0 else "N", axis=1)

        df_whs_info = df_inventory2[df_inventory2["Month_Name"]=="Dec"].copy()
        df_whs_inv_value = df_whs_info["Inventory_Value"].sum()
        df_whs_inv_exp_value = df_whs_info[df_whs_info["Expired_Flag"]=="Y"]["Inventory_Value"].sum()
        df_whs_inv_volume = df_whs_info["Inventory_Volume"].sum()
        df_whs_inv_exp_volume = df_whs_info[df_whs_info["Expired_Flag"]=="Y"]["Inventory_Volume"].sum()
        df_chart5 = df_whs_info[df_whs_info["Expired_Flag"]=="Y"].groupby(["Principal_ID","Principal_ID_Name"])["Inventory_Value"].sum().reset_index()

        df_whs_info = df_master_branch.copy()
        df_whs_capacity = df_whs_info["Branch_Capacity_m3"].iloc[0]
        df_whs_info["Branch_Capacity_m3"] = f"{df_whs_capacity:,}"
        df_whs_info[f"Inventory Value ({period})"] = f"{df_whs_inv_value:,}"
        df_whs_info[f"Expired Inventory Value ({period})"] = f"{df_whs_inv_exp_value:,}"
        df_whs_info[f"Expired Inventory Value Percentage ({period})"] = f"{df_whs_inv_exp_value/df_whs_inv_value:.2%}"
        # df_whs_info[f"Inventory Volume ({period})"] = f"{df_whs_inv_volume:,.2f} m3"
        df_whs_info[f"Expired Inventory Volume ({period})"] = f"{df_whs_inv_exp_volume:,.2f} m3"
        df_whs_info[f"Expired Inventory Volume to Capacity ({period})"] = f"{df_whs_inv_exp_volume/df_whs_capacity:.2%}"
        df_whs_info_T = df_whs_info.T
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(df_whs_info_T)
        with col2:
            # Expired Inventory value per principal
            bar_chart_inventory(df_chart5, "Expired Inventory Value by Principal", period, "Principal_ID", "Inventory_Value")
        
        st.write(f'''As {period} in {selected_branch}, the expired inventory value is {df_whs_inv_exp_value/df_whs_inv_value:.2%} from all inventory value in the warehouse.
            They also consume {df_whs_inv_exp_volume:,.2f} m3 or {df_whs_inv_exp_volume/df_whs_capacity:.2%} of the warehouse capacity. The graph in top right shows which
            principal gives the most expired product in the warehouse. What will happend if all the expired inventory are eliminated from the warehouse (returned or destroyed)?
        ''')
        st.space()
        
        col1, col2 = st.columns(2)
        with col1:
            # Inventory volume per month
            df_chart6 = df_inventory2.copy()
            df_chart6 = df_chart6.groupby(["Month_Name","Period","Date_YYYYmm"])["Inventory_Volume_m3"].sum().reset_index()
            df_chart6["Capacity Usage"] = df_chart6["Inventory_Volume_m3"]/df_whs_capacity
            df_chart6["Full Capacity"] = 1
            value_from = df_chart6[df_chart6["Month_Name"]==month]["Capacity Usage"].iloc[0]
            line_chart_inventory_with_capacity(df_chart6, "Month_Name", "Capacity Usage", "Warehouse Capacity Usage", "", "Date_YYYYmm", "Capacity Usage", df_chart6, "Full Capacity")
        with col2:
            # Inventory volume per month
            df_chart7 = df_inventory2.copy()
            df_chart7 = df_chart7[df_chart7["Expired_Flag"]=="N"].groupby(["Month_Name","Period","Date_YYYYmm"])["Inventory_Volume_m3"].sum().reset_index()
            df_chart7["Capacity Usage"] = df_chart7["Inventory_Volume_m3"]/df_whs_capacity
            df_chart7["Full Capacity"] = 1
            value_to = df_chart7[df_chart7["Month_Name"]==month]["Capacity Usage"].iloc[0]
            line_chart_inventory_with_capacity(df_chart7, "Month_Name", "Capacity Usage", "Warehouse Capacity Usage (Exclude Expired Inventory)", "", "Date_YYYYmm", "Capacity Usage (Exclude Expired Inventory)", df_chart7, "Full Capacity")
            st.write(f'''
                Warehouse capacity usage will reduce from {value_from:.2%} to {value_to:.2%} as {period}.
            ''')
        
        st.space()
        col1, col2 = st.columns(2)
        with col1:
            # DOI per month
            df_chart8a = df_inventory2.copy()
            df_chart8a = df_chart8a.merge(df_as_of_month[df_as_of_month["Type"]=="Inventory"], on="Month_Num", how="inner")
            df_chart8a = df_chart8a.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Inventory_Value"].sum().reset_index()
            df_chart8b = df_sales.copy()
            df_chart8b = df_chart8b.merge(df_as_of_month[df_as_of_month["Type"]=="Sales"], on="Month_Num", how="inner")
            df_chart8b = df_chart8b.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Sales_Value"].sum().reset_index()
            df_chart8 = df_chart8a.merge(df_chart8b, on=["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm"], how="inner")
            df_chart8["DOI"] = df_chart8["Inventory_Value"] / (df_chart8["Sales_Value"]/3) * 30
            value_from = df_chart8[df_chart8["As_of_Month_Name"]==month]["DOI"].iloc[0]
            line_chart_inventory(df_chart8, "As_of_Month_Name", "DOI", "Day of Inventory", "", "As_of_Date_YYYYmm", "DOI")
        with col2:
            # DOI per month
            df_chart9a = df_inventory2[df_inventory2["Expired_Flag"]=="N"].copy()
            df_chart9a = df_chart9a.merge(df_as_of_month[df_as_of_month["Type"]=="Inventory"], on="Month_Num", how="inner")
            df_chart9a = df_chart9a.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Inventory_Value"].sum().reset_index()
            df_chart9b = df_sales.copy()
            df_chart9b = df_chart9b.merge(df_as_of_month[df_as_of_month["Type"]=="Sales"], on="Month_Num", how="inner")
            df_chart9b = df_chart9b.groupby(["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm","Type"])["Sales_Value"].sum().reset_index()
            df_chart9 = df_chart9a.merge(df_chart9b, on=["As_of_Month_Name","As_of_Period","As_of_Date_YYYYmm"], how="inner")
            df_chart9["DOI"] = df_chart9["Inventory_Value"] / (df_chart9["Sales_Value"]/3) * 30
            value_to = df_chart9[df_chart9["As_of_Month_Name"]==month]["DOI"].iloc[0]
            line_chart_inventory(df_chart9, "As_of_Month_Name", "DOI", "Day of Inventory (Exclude Expired Inventory)", "", "As_of_Date_YYYYmm", "DOI")
            st.write(f'''
                DOI will reduce from {value_from:.2f} to {value_to:.2f} as {period}.
            ''')

print("End printing")