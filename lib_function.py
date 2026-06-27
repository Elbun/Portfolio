import streamlit as st
import altair as alt

def insert_icon(path, file):
    return st.image(path+file, width="content")

def tech_skill(skill, pic_path, pic):
    cola, colb = st.columns([1,5])
    with cola:
        insert_icon(pic_path, pic)
    with colb:
        st.html(f'<p style="font-size:20px;">{skill}</p>')

def education(school, pic_path, pic, period_from, period_to, desc):
    cola, colb = st.columns([1,10])
    with cola:
        insert_icon(pic_path, pic)
    with colb:
        colb1, colb2 = st.columns([3,1])
        with colb1:
            st.html(f'''
                <p style="font-size:20px;text-align:justify;margin-bottom:0"><b>{school}</b></p>
                ''')
        with colb2:
            st.html(f'''
                <p style="font-size:17px;text-align:right;margin-bottom:0"><i>{period_from} - {period_to}</i></p>
                ''')
        if(desc!=None):
            st.html(f'''
                <p style="font-size:15px;text-align:justify;margin-bottom:0">{desc}</p>
                ''')
    st.space(size=1)

def experience(company, pic_path, pic, period_from, period_to, role, desc=None):
    cola, colb = st.columns([1,10])
    with cola:
        insert_icon(pic_path, pic)
    with colb:
        colb1, colb2 = st.columns([3,1])
        with colb1:
            st.html(f'''
                <p style="font-size:20px;text-align:justify;margin-bottom:0"><b>{role}, {company}</b></p>
                ''')
        with colb2:
            st.html(f'''
                <p style="font-size:17px;text-align:right;margin-bottom:0"><i>{period_from} - {period_to}</i></p>
                ''')
        if(desc!=None):
            st.html(f'''
                <p style="font-size:15px;text-align:justify;margin-bottom:0">{desc}</p>
                ''')
    st.space(size=1)

def lets_connect(pic_path, pic, text, link):
    cola, colb = st.columns([1,9])
    with cola:
        st.image(pic_path+pic, width="content")
    with colb:
        if(link!=None):
            text_link = f'''<a href={link} target="_blank">{text}</a>'''
        else:
            text_link = f'''{text}'''
        st.html(f'''{text_link}''')

def sales_horizontal_bar_chart(df, chart_title, x, y, variable, color, subtitle_class, subtitle_support_text1, subtitle_support_text2):
    if(subtitle_class=="branch"):
        if(subtitle_support_text1==None):
            subtitle_support_text1 = f"all segmentation"
        subtitle_text = f"For sales in segmentation : {subtitle_support_text1}"
    if(subtitle_class=="segmentation"):
        if(subtitle_support_text1==None):
            subtitle_support_text1 = f"all branch"
        subtitle_text = f"For sales in branch : {subtitle_support_text1}"
    if(subtitle_class=="customer"):
        if(subtitle_support_text1==None):
            subtitle_support_text1 = f"all branch"
        else:
            subtitle_support_text1 = f"branch {subtitle_support_text1}"
        if(subtitle_support_text2==None):
            subtitle_support_text2 = f"all segmentation"
        else:
            subtitle_support_text2 = f"segmentation {subtitle_support_text2}"
        subtitle_text = f"Customer list in {subtitle_support_text2} in {subtitle_support_text1}"
    bar_chart1 = alt.Chart(
        df,
        title=alt.Title(f"{chart_title}",
            subtitle=f"{subtitle_text}",
            fontSize=20,
            anchor="start",
            offset=20)
        ).mark_bar().encode(
            x=alt.X(f"{x}:Q", 
                ).axis(
                    title=None,
                    labelAngle=0,
                    labelFontWeight="bold"  
                ),
            y=alt.Y(f"{y}:N",
                    sort=alt.EncodingSortField(field=f"{x}", order="descending")
                ).axis(
                    title=None,
                    labelFontWeight="bold"
                ),
            color=alt.Color(
                f"{color}:N",
                scale=None,
                legend=alt.Legend(
                    orient="top",
                    title=None)
                ),
            yOffset=f"{variable}",
            tooltip=["Sales Category",
                    alt.Tooltip("value:Q", title="Amount", format=",.0f")]
        ).configure_legend(
            strokeColor="gray"
        ).configure_axis(
            domainColor="black",
            domainWidth=10,
            gridColor="black",
            gridWidth=2,
            gridOpacity=0.03
        ).properties(
            height=500
        )
    st.altair_chart(bar_chart1, width=450)


def line_chart_inventory(df,x,y,title,subtitle_text,x_sort,y_tooltip):
    if y_tooltip=="DOI":
        num_format = ",.2f"
    else:
        num_format = ",.0f"
    # Show data in line chart
    line_chart = alt.Chart(
            df,
            title=alt.Title(f"{title}",
                subtitle=f"{subtitle_text}",    
                fontSize=20,
                anchor="start",
                offset=20)
    ).mark_line(point=True, size=3).encode(
        x=alt.X(f"{x}:N", 
                sort=alt.EncodingSortField(field=f"{x_sort}", order="ascending")
            ).axis(
                title=None,
                labelAngle=0,
                labelFontWeight="bold"  
            ),
        y=alt.Y(f"{y}:Q").axis(
            title=None,
            labelFontWeight="bold"
        ),
        # color=alt.Color("Sales Category:N",
        #     legend=alt.Legend(
        #         orient="top",
        #         title=None)
        #     ),
        # color=alt.Color(
        #     f"Hex_Code:N",
        #     scale=None,
        #     legend=alt.Legend(
        #         orient="top",
        #         title=None)
        #     ),
        tooltip=[x,
            alt.Tooltip(f"{y}:Q", title=f"{y_tooltip}", format=f"{num_format}")]
    ).configure_axis(
        domainColor="black",
        domainWidth=10,
        gridColor="black",
        gridWidth=2,
        gridOpacity=0.03
    ).configure_point(
        size=100
    ).properties(
        height=350
    )

    final_chart = line_chart

    # # Text Layer for Values
    # if point_value=="Y":
    #     text_labels = line_chart.mark_text(
    #         align="center",
    #         baseline="bottom",
    #         dy=-10,  # Shifts the text slightly above the point
    #     ).encode(
    #         text=f"{y}:Q"  # The value to display
    #     )
    #     final_chart = line_chart+text_labels
    st.altair_chart(final_chart, width=700)

def bar_chart_inventory(df,chart_title,subtitle_text,x,y):
    if chart_title=="Day of Inventory":
        num_format = ",.2f"
    else:
        num_format = ",.0f"
    bar_chart1 = alt.Chart(
        df,
        title=alt.Title(f"{chart_title}",
            subtitle=f"{subtitle_text}",
            fontSize=20,
            anchor="start",
            offset=20)
        ).mark_bar().encode(
            x=alt.X(f"{x}:N", 
                    sort=alt.EncodingSortField(field=f"{y}", order="descending")
                ).axis(
                    title=None,
                    labelAngle=0,
                    labelFontWeight="bold"  
                ),
            y=alt.Y(f"{y}:Q"
                ).axis(
                    title=None,
                    labelFontWeight="bold"
                ),
            # color=alt.Color(
            #     f"{color}:N",
            #     scale=None,
            #     legend=alt.Legend(
            #         orient="top",
            #         title=None)
            #     ),
            # yOffset=f"{variable}",
            tooltip=[f"{x}_Name",
                    alt.Tooltip(f"{y}:Q", title="Amount", format=f"{num_format}")]
        ).configure_legend(
            strokeColor="gray"
        ).configure_axis(
            domainColor="black",
            domainWidth=10,
            gridColor="black",
            gridWidth=2,
            gridOpacity=0.03
        ).properties(
            height=350
        )
    st.altair_chart(bar_chart1, width=700)

def line_chart_inventory_with_capacity(df,x,y,title,subtitle_text,x_sort,y_tooltip,df_capacity,capacity_col):
    if y_tooltip=="DOI":
        num_format = ",.2f"
    else:
        num_format = ",.2%"
    # --- LAYER 1: Inventory Line Chart (using df) ---
    line_layer = (
        alt.Chart(df)
        .mark_line(point=True, size=3)
        .encode(
            x=alt.X(
                f"{x}:N",
                sort=alt.EncodingSortField(
                    field=f"{x_sort}", order="ascending"
                ),
            ).axis(title=None, labelAngle=0, labelFontWeight="bold"),
            y=alt.Y(f"{y}:Q").axis(title=None, labelFontWeight="bold"),
            tooltip=[
                x,
                alt.Tooltip(
                    f"{y}:Q", title=f"{y_tooltip}", format=f"{num_format}"
                ),
            ],
        )
    )
    # --- LAYER 2: Capacity Chart (using df_capacity) ---
    # Example: A dashed red line showing capacity/threshold
    capacity_layer = (
        alt.Chart(df_capacity)
        .mark_line(
            strokeDash=[4, 4], size=2, color="red"
        )  # Or .mark_line(), .mark_bar(), etc.
        .encode(
            x=alt.X(
                f"{x}:N",
                sort=alt.EncodingSortField(
                    field=f"{x_sort}", order="ascending"
                ),
            ).axis(title=None, labelAngle=0, labelFontWeight="bold"),
            y=alt.Y(f"{capacity_col}:Q",
                axis=alt.Axis(format='%')),  # Y maps to the capacity data
            tooltip=[
                x,
                alt.Tooltip(
                    f"{capacity_col}:Q",
                    title="Capacity",
                    format=f"{num_format}",
                ),
            ],
        )
    )
    # --- COMBINE LAYERS & APPLY GLOBAL CONFIGS ---
    # High-level configurations (titles, axis configs) go here
    final_chart = (
        alt.layer(
            line_layer,
            capacity_layer,
            title=alt.Title(
                f"{title}",
                subtitle=f"{subtitle_text}",
                fontSize=20,
                anchor="start",
                offset=20,
            ),
        )
        .properties(height=350)
        .configure_axis(
            domainColor="black",
            domainWidth=10,
            gridColor="black",
            gridWidth=2,
            gridOpacity=0.03,
        ).configure_point(
        size=100
        )
    )
    st.altair_chart(final_chart, width=700)