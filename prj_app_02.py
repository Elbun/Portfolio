import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt

print("-----------------------------------------------------------------------------------------------------------------------------------------")
print("Start printing")

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set folder path
path = "B. Project/geotag_data/"

#----------------------------- Read data file

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
        st.html('''<p style="text-align:justify;">There are xx data used in this showcase. </p>
            ''')
    with col2:
        # insert_icon(path, "geo_tag_relation_model.png")
        st.write("[ERD]")
    
    st.subheader("Special KPI")
    st.html('''<p style="text-align:justify;">There is a "special KPI" used in the dashboard. This KPI is common in the term of Supply Chain Management (SCM), it is <i>Day of Inventory</i> 
        (DOI). DOI is a metric to calculate how long the inventory are stored in a warehouse, so this KPI is served in time unit.
        It can be calculated with formula below.</p>''')
            
    st.latex(r'''
        DOI = \frac{Ending period stock}{Average Sales}
        ''')
        
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
        DOI (days)= \frac{Ending of month stock value (IDR)}{Monthly average Sales (IDR/month)} * 30 days/month
        ''')
    
    
print("End printing")