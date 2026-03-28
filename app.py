import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

def format_state_name(state):
    return " ".join(
        word.capitalize() if word != "&" else "&"
        for word in state.replace("-", " ").split()
    )

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PhonePe Pulse Dashboard", layout="wide")


# ---------------- DATABASE CONNECTION ----------------
engine = create_engine("postgresql+psycopg2://postgres:Karan7826@localhost:5432/project")


# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Analysis"])

if page == "Home":
    st.title("PHONEPE")
    st.markdown("<h2 style='color: gold; text-decoration: underline;'> Welcome to the PhonePe Pulse business case study dashboard.</h2>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.write("### Aggregated Transaction total count")

    query = '''
    SELECT "State" AS state,
    SUM("Transaction_amount") AS total_amount
    FROM public."Agg_transaction"
    WHERE "Year" = 2023
    GROUP BY "State"
    '''
    df = pd.read_sql(query, engine)
    df["state"] = df["state"].apply(format_state_name)
    df['state'] = df['state'].replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')

    fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color='total_amount',
    color_continuous_scale='Reds')

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)    #Streamlit display

elif page == "Analysis":
    st.title("Business Case Study")
    selected_year = st.selectbox("📅 Select Year", [2018, 2019, 2020, 2021, 2022, 2023])

    case_study = st.selectbox(
        "📝 Choose Case Study",
        [
            "Transaction Dynamics",
            "Device Dominance and User Engagement",
            "User Registration Analysis",
            "Insurance Analysis",
            "Transaction Analysis Across States and Districts"
        ]
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- CASE STUDY: 01 ----------------

    # ------------- 1st. Query------------------
    if case_study == "Transaction Dynamics":
        st.subheader("🗺️ State-wise Transaction Analysis")

        state_query = '''
        SELECT DISTINCT "State"
        FROM public."Agg_transaction"
        ORDER BY "State"
        '''
        state_df = pd.read_sql(state_query, engine)
        state_df["Display_State"] = state_df["State"].apply(format_state_name)
        selected_display_state = st.selectbox("Choose a State", state_df["Display_State"])
        selected_state = state_df.loc[ state_df["Display_State"] == selected_display_state, "State" ].iloc[0]
        

        trend_query = f'''
        SELECT "Year",
        SUM("Transaction_count") AS total_transaction_count,
        SUM("Transaction_amount") AS total_amount
        FROM public."Agg_transaction"
        WHERE "State" = '{selected_state}'
        GROUP BY "Year"
        ORDER BY "Year"
        '''

        trend_df = pd.read_sql(trend_query, engine)

        if not trend_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.line(
                    trend_df,
                    x="Year",
                    y="total_transaction_count",
                    markers=True,
                    title="Total Transactions Count Over Years"
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = px.line(
                    trend_df,
                    x="Year",
                    y="total_amount",
                    markers=True,
                    title="Total Transaction Amount Over Years"
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No transaction trend data available for the selected state.")

    # ------------- 2nd. Query------------------
        st.subheader("💹 Payment Category Performance")

        category_query = f'''
        SELECT "Transaction_type",
        SUM("Transaction_count") AS total_count,
        SUM("Transaction_amount") AS total_amount
        FROM public."Agg_transaction"
        WHERE "State" = '{selected_state}'
        AND "Year" = {selected_year}
        GROUP BY "Transaction_type"
        ORDER BY total_amount DESC
        '''

        category_df = pd.read_sql(category_query, engine)

        if not category_df.empty:
            col3, col4 = st.columns(2)

            with col3:
                fig3 = px.pie(
                    category_df,
                    names="Transaction_type",
                    values="total_count",
                    title="Transaction Count Distribution")
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                fig4 = px.pie(
                    category_df,
                    names="Transaction_type",
                    values="total_amount",
                    title="Transaction Amount Distribution (₹)")
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("No category-wise data available for the selected state.")

    # ------------- 3rd. Query------------------   
        st.subheader("📈 Highest Transaction amount in States")

        highest_value_query = f'''
        SELECT "State", 
        SUM("Transaction_amount") AS total_amount
        FROM public."Agg_transaction"
        WHERE "Year" = {selected_year}
        GROUP BY "State"
        ORDER BY total_amount DESC
        LIMIT 10
        '''
        highest_value_df = pd.read_sql(highest_value_query, engine)
        if not highest_value_df.empty:
            fig5 = px.bar(
                highest_value_df, 
                x="State", 
                y="total_amount", 
                color = "State",
                title=f"Top 10 States in {selected_year}")
            st.plotly_chart(fig5, use_container_width=True)
            
    # ------------- 4th. Query------------------

        st.subheader("📍 States Quarterly Performance Trends: ")

        quarter_query = f'''
        SELECT "Quater", 
        SUM("Transaction_amount") AS quaterly_amount
        FROM public."Agg_transaction"
        WHERE "State" = '{selected_state}' AND "Year" = {selected_year}
        GROUP BY "Quater"
        ORDER BY "Quater"
        '''
        quarter_df = pd.read_sql(quarter_query, engine)

        if not quarter_df.empty:
            fig6 = px.area(
                quarter_df,
                x="Quater",
                y="quaterly_amount",
                title=f"Quarterly Growth Trend for {selected_display_state} in {selected_year}",
                markers=True
            )
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.warning("No quarterly data found for this selection.")

    # ------------- 5th. Query------------------

        st.subheader("📊 Average Transaction Value Analysis")

        avg_value_query = f'''
        SELECT "Year", 
        AVG("Transaction_amount") AS avg_values
        FROM public."Agg_transaction"
        WHERE "State" = '{selected_state}'
        GROUP BY "Year"
        ORDER BY "Year"
        '''

        avg_value_df = pd.read_sql(avg_value_query, engine)

        if not avg_value_df.empty:
            fig7 = px.area(
                avg_value_df,
                x="Year",
                y="avg_values",
                title=f"Average Transaction Value Trend: '{selected_display_state}' ",
                markers=True
            )
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.warning("No average value data found for this selection.")


    # ---------------- CASE STUDY: 02 ----------------

    elif case_study == "Device Dominance and User Engagement":
        st.subheader("📱 Brand-wise User Analysis")

        brand_query = '''
            SELECT DISTINCT "Brand"
            FROM public."Agg_user"
            ORDER BY "Brand"
            '''
        brand_df = pd.read_sql(brand_query, engine)

        selected_brand = st.selectbox("Choose a Brand", brand_df["Brand"])

        trend_query = f'''
        SELECT "Year",
        SUM("Count") AS total_users,
        AVG("Percentage") AS avg_percentage
        FROM public."Agg_user"
        WHERE "Brand" = '{selected_brand}'
        GROUP BY "Year"
        ORDER BY "Year"
        '''
        trend_df = pd.read_sql(trend_query, engine)

        if not trend_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.line(
                    trend_df,
                    x="Year",
                    y="total_users",
                    markers=True,
                    title="Total Users Over Years")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = px.line(
                    trend_df,
                    x="Year",
                    y="avg_percentage",
                    markers=True,
                    title="Average Percentage Over Years")
                st.plotly_chart(fig2, use_container_width=True)

    # ------------- 2nd. Query ------------------
        st.subheader("📅 Year-wise Brand Share")

        brand_share_query = f'''
        SELECT "Brand",
        SUM("Count") AS total_users
        FROM public."Agg_user"
        WHERE "Year" = {selected_year}
        GROUP BY "Brand"
        ORDER BY total_users DESC
        '''

        brand_share_df = pd.read_sql(brand_share_query, engine)

        if not brand_share_df.empty:
            col3, col4 = st.columns(2)
                    
            with col3:
                fig3 = px.pie(
                    brand_share_df,
                    names="Brand",
                    values="total_users",
                    title="Brand Share Distribution")
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                fig4 = px.pie(
                    brand_share_df.head(10),
                    names="Brand",
                    values="total_users",
                    title="Top Brands by Users")
                st.plotly_chart(fig4, use_container_width=True)

        # ------------- 3rd. Query ------------------
            
        st.subheader("📉 Underutilization Gap (Engagement Ratio)")

        engagement_query = f'''
        SELECT "state",
        SUM("registeredUsers") AS total_registered_users,
        SUM("appOpens") AS total_app_opens,
        ROUND(SUM("appOpens")::numeric / NULLIF(SUM("registeredUsers"), 0), 2) AS engagement_ratio
        FROM public."map_user"
        WHERE "year" = {selected_year}
        GROUP BY "state"
        ORDER BY engagement_ratio 
        LIMIT 10
        '''
        engagement_df = pd.read_sql(engagement_query, engine)

        if not engagement_df.empty:
            fig5 = px.bar(
                engagement_df,
                x="state",
                y="engagement_ratio",
                color="state",
                title="Lowest Engagement Ratio States"
            )
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.warning("No engagement ratio data available.")

        # ------------- 4th. Query ------------------

        st.subheader("📍 Low Engagement Districts")

        low_engage_dist_query = f''' 
        SELECT district,
        state,
        SUM("registeredUsers") AS users,
        SUM("appOpens") AS opens,
        ROUND(SUM("appOpens")::numeric / NULLIF(SUM("registeredUsers"),0), 2) AS engagement_ratio
        FROM public."map_user"
        WHERE year = {selected_year}
        GROUP BY district, state
        HAVING SUM("registeredUsers") > 5000
        ORDER BY engagement_ratio ASC
        '''
        low_engage_dist_df = pd.read_sql(low_engage_dist_query, engine).tail(10)

        fig6 = px.bar(
            low_engage_dist_df,
            x="district",
            y="engagement_ratio",
            color="state",
            title="Lowest Engagement Districts")
        st.plotly_chart(fig6, use_container_width=True)


    # ------------- 5th. Query ------------------
        
        st.subheader("🏆 Top Performing Brands")

        top_perform_brands_query = f''' 
        SELECT "Brand",
        SUM("Count") AS total_users,
        ROUND((AVG("Percentage") * 100)::numeric, 2) AS avg_share
        FROM public."Agg_user"
        WHERE "Year" = {selected_year}
        GROUP BY "Brand"
        ORDER BY avg_share DESC
        LIMIT 10        
        '''
        top_perform_brands_df = pd.read_sql(top_perform_brands_query, engine)

        fig7 = px.funnel(
            top_perform_brands_df,
            x="Brand",
            y="avg_share",
            color="Brand",
            title="Top Brand Performance (%)"
        )
        st.plotly_chart(fig7, use_container_width=True)


    # ---------------- CASE STUDY: 03 ----------------

    elif case_study == "User Registration Analysis":
        st.subheader("User Registration Analysis")

        st.subheader("📈  State-wise User Registration Analysis")

        state_query = '''
        SELECT DISTINCT state
        FROM public.map_user
        ORDER BY state
        '''
        state_df = pd.read_sql(state_query, engine)
        state_df["Display_State"] = state_df["state"].apply(format_state_name)
        selected_display_state = st.selectbox("Choose a State", state_df["Display_State"])
        selected_state = state_df.loc[state_df["Display_State"] == selected_display_state, "state"].iloc[0]

        trend_query = f'''
        SELECT year,
        SUM("registeredUsers") AS total_users,
        SUM("appOpens") AS total_app_opens
        FROM public.map_user
        WHERE state = '{selected_state}'
        GROUP BY year
        ORDER BY year
        '''
        trend_df = pd.read_sql(trend_query, engine)

        if not trend_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.line(
                    trend_df,
                    x="year",
                    y="total_users",
                    markers=True,
                    title="Registered Users Over Years")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = px.line(
                    trend_df,
                    x="year",
                    y="total_app_opens",
                    markers=True,
                    title="App Opens Over Years")
                st.plotly_chart(fig2, use_container_width=True)

    # ------------------ Section 2: District-wise share ------------------

        st.subheader("📍 District-wise User Distribution")

        district_query = f"""
        SELECT district,
        SUM("registeredUsers") AS total_users
        FROM public."map_user"
        WHERE state = '{selected_state}'
        AND year = {selected_year}
        GROUP BY district
        ORDER BY total_users ASC
        LIMIT 10;
        """
        district_df = pd.read_sql(district_query, engine)

        if not district_df.empty:
            fig3 = px.bar(
                district_df,
                x="total_users",
                y="district",
                color="district",
                orientation='h',
                title="Top Districts by Users"
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ------------------ 3rd. Query ------------------

        st.subheader("🏆 Top States by User Registration")

        top_state_query = f"""
        SELECT state,
        SUM("registeredUsers") AS total_users
        FROM public."map_user"
        WHERE year = {selected_year}
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10;
        """
        top_state_df = pd.read_sql(top_state_query, engine)

        if not top_state_df.empty:
            fig4 = px.bar(
                top_state_df,
                x="state",
                y="total_users",
                color= "total_users",
                orientation='v',
                title=f"Top 10 States ({selected_year})"
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ------------------ 4.th Query ------------------

        st.subheader("🔍 Users vs App Opens (Engagement Insight)")

        engagement_query = f"""
        SELECT state,
        SUM("registeredUsers") AS users,
        SUM("appOpens") AS opens
        FROM public."map_user"
        WHERE year = {selected_year}
        GROUP BY state;
        """
        engagement_df = pd.read_sql(engagement_query, engine)

        if not engagement_df.empty:
            fig5 = px.scatter(
                engagement_df,
                x="users",
                y="opens",
                size="opens",
                color="state",
                title="Users vs App Opens"
            )
            st.plotly_chart(fig5, use_container_width=True)

    # ------------------ 5.th Query ------------------ 

        st.subheader("🚀 Fastest Growing Districts")

        growth_query = """
        SELECT district,
        year,
        SUM("registeredUsers") AS users
        FROM public."map_user"
        GROUP BY district, year;
        """
        growth_df = pd.read_sql(growth_query, engine)

        if not growth_df.empty:
            growth_df["growth"] = growth_df.groupby("district")["users"].pct_change() * 100

            latest_growth = growth_df[growth_df["year"] == selected_year] \
            .sort_values(by="growth", ascending=False) \
            .head(10)

            fig6 = px.bar(
                latest_growth,
                x="district",
                y="growth",
                color="growth",
                title="Top Growing Districts (%)"
            )
            st.plotly_chart(fig6, use_container_width=True)
    

    # ---------------- CASE STUDY: 04 ----------------
    elif case_study == "Insurance Analysis":
        st.subheader("📈 Insurance Penetration and Growth Potential Analysis")

        state_query = '''
        SELECT DISTINCT state
        FROM public.top_insurance
        ORDER BY state
        '''

        state_df = pd.read_sql(state_query, engine)
        state_df["Display_State"] = state_df["state"].apply(format_state_name)
        selected_display_state = st.selectbox("Choose a State", state_df["Display_State"])
        selected_state = state_df.loc[state_df["Display_State"] == selected_display_state, "state"].iloc[0]
        
        
        trend_query = f'''
        SELECT year,
        SUM(count) AS total_count,
        SUM(amount) AS total_amount
        FROM public.top_insurance
        WHERE state = '{selected_state}'
        GROUP BY year
        ORDER BY year
        '''
        trend_df = pd.read_sql(trend_query, engine)

        if not trend_df.empty:

            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.line(
                    trend_df,
                    x="year",
                    y="total_count",
                    markers=True,
                    title="Insurance Count Over Years")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = px.line(
                    trend_df,
                    x="year",
                    y="total_amount",
                    markers=True,
                    title="Insurance Amount Over Years")
                st.plotly_chart(fig2, use_container_width=True)

        else:
            st.warning("No insurance trend data available for the selected state.")

        # ------------------ 2nd. Query ------------------
        st.subheader("📍 District-wise Insurance Distribution")

        share_query = f'''
        SELECT districts,
        SUM(count) AS total_count,
        SUM(amount) AS total_amount
        FROM public.top_insurance
        WHERE state = '{selected_state}'
        AND year = {selected_year}
        GROUP BY districts
        ORDER BY total_amount DESC
        '''
        share_df = pd.read_sql(share_query, engine)

        if not share_df.empty:
            top_share = share_df.head(10)
            col3, col4 = st.columns(2)

            with col3:
                fig3 = px.pie(
                    top_share,
                    names="districts",
                    values="total_count",
                    title="Insurance Count Share by District")
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                fig4 = px.pie(
                    top_share,
                    names="districts",
                    values="total_amount",
                    title="Insurance Amount Share by District")
                st.plotly_chart(fig4, use_container_width=True)

        else:
            st.warning("No district insurance data available for the selected year and state.")

    # ------------------ 3rd. Query ------------------

        st.subheader("📊 Top States by Insurance Amount")

        top_states_query = f'''
        SELECT state,
        SUM(amount) AS total_amount
        FROM public.top_insurance
        WHERE year = {selected_year}
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
        '''

        top_states_df = pd.read_sql(top_states_query, engine)

        if not top_states_df.empty:
            top_states_df["Display_State"] = top_states_df["state"].apply(format_state_name)

            fig5 = px.bar(
                top_states_df,
                x="total_amount",
                y="Display_State",
                color="total_amount",
                orientation='h',
                title=f"Top States by Insurance Amount ({selected_year})")
            st.plotly_chart(fig5, use_container_width=True)

        else:
             st.warning("No top state insurance data available.")


        # ------------------ 4th. Query ------------------

        st.subheader("📈 Insurance Growth Across India")

        india_growth_query = '''
        SELECT "year",
        SUM(count) AS total_count,
        SUM(amount) AS total_amount
        FROM public.top_insurance
        GROUP BY "year"
        ORDER BY "year"
        '''

        india_growth_df = pd.read_sql(india_growth_query, engine)

        if not india_growth_df.empty:
            col5, col6 = st.columns(2)

            with col5:
                fig6 = px.line(
                    india_growth_df,
                    x="year",
                    y="total_count",
                    markers=True,
                    title="India Insurance Count Trend"
                )
                st.plotly_chart(fig6, use_container_width=True)

            with col6:
                fig7 = px.line(
                    india_growth_df,
                    x="year",
                    y="total_amount",
                    markers=True,
                    title="India Insurance Amount Trend"
                )
                st.plotly_chart(fig7, use_container_width=True)
        else:
            st.warning("No India-level insurance trend data available.")

    # ------------------ 5th. Query ------------------

        st.subheader("📊 Insurance Penetration Ratio")

        ins_query = f'''
        SELECT state,
            SUM(count) AS insurance_users
        FROM public.top_insurance
        WHERE year = {selected_year}
        GROUP BY state
        '''

        user_query = f'''
        SELECT state,
            SUM("registeredUsers") AS total_users
        FROM public.map_user
        WHERE year = {selected_year}
        GROUP BY state
        '''

        ins_df = pd.read_sql(ins_query, engine)
        user_df = pd.read_sql(user_query, engine)

        if not ins_df.empty and not user_df.empty:
            merged_df = pd.merge(ins_df, user_df, on="state", how="inner")
            merged_df["penetration_ratio"] = (merged_df["insurance_users"] / merged_df["total_users"]) * 100
            merged_df = merged_df.sort_values(by="penetration_ratio", ascending=False).head(10)
            merged_df["Display_State"] = merged_df["state"].apply(format_state_name)

            fig8 = px.bar(
                merged_df,
                x="penetration_ratio",
                y="Display_State",
                color="penetration_ratio",
                orientation='h',
                title=f"Top States by Insurance Penetration Ratio ({selected_year})"
            )
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.warning("No penetration ratio data available.")
                
    # ---------------- CASE STUDY: 05 ----------------

    # ------------------ 1st. Query ------------------

    elif case_study == "Transaction Analysis Across States and Districts":
        
        st.subheader("📊 Transaction Analysis Across States and Districts")
        st.markdown("<br> <br>", unsafe_allow_html=True)

        st.subheader("🗺️ State-wise Transaction Trend")

        state_query = '''
        SELECT DISTINCT state
        FROM public.top_transaction
        ORDER BY state
        '''
        state_df = pd.read_sql(state_query, engine)

        state_df = pd.read_sql(state_query, engine)
        state_df["Display_State"] = state_df["state"].apply(format_state_name)
        selected_display_state = st.selectbox("Choose a State", state_df["Display_State"])
        selected_state = state_df.loc[state_df["Display_State"] == selected_display_state, "state"].iloc[0]

        trend_query = f'''
        SELECT year,
        SUM(count) AS total_count,
        SUM(amount) AS total_amount
        FROM public.top_transaction
        WHERE state = '{selected_state}'
        GROUP BY year
        ORDER BY year
        '''
        trend_df = pd.read_sql(trend_query, engine)

        if not trend_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.line(
                    trend_df,
                    x="year",
                    y="total_count",
                    markers=True,
                    title="Transaction Count Over Years"
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                fig2 = px.line(
                    trend_df,
                    x="year",
                    y="total_amount",
                    markers=True,
                    title="Transaction Amount Over Years"
                )
                st.plotly_chart(fig2, use_container_width=True)


        # ------------------ 2nd. Query ------------------

        st.subheader("📍 District-wise Transaction Share")

        district_query = f'''
        SELECT districts,
        SUM(count) AS total_count,
        SUM(amount) AS total_amount
        FROM public.top_transaction
        WHERE state = '{selected_state}'
        AND year = {selected_year}
        GROUP BY districts
        ORDER BY total_amount DESC
        '''
        district_df = pd.read_sql(district_query, engine)

        if not district_df.empty:
            top_districts = district_df.head(10)
            col3, col4 = st.columns(2)

            with col3:
                fig3 = px.pie(
                    top_districts,
                    names="districts",
                    values="total_count",
                    title="Transaction Count Share by District"
                )
                st.plotly_chart(fig3, use_container_width=True)

            with col4:
                fig4 = px.pie(
                    top_districts,
                    names="districts",
                    values="total_amount",
                    title="Transaction Amount Share by District"
                )
                st.plotly_chart(fig4, use_container_width=True)


        # ------------------ 3rd. Query ------------------

        st.subheader("📍 Top States by Transaction Amount")

        top_states_query = f'''
        SELECT "State",
            SUM("Transaction_amount") AS total_amount
        FROM public."Agg_transaction"
        WHERE "Year" = {selected_year}
        GROUP BY "State"
        ORDER BY total_amount DESC
        LIMIT 10
        '''
        top_states_df = pd.read_sql(top_states_query, engine)

        if not top_states_df.empty:
            top_states_df["Display_State"] = top_states_df["State"].apply(format_state_name)

            fig5 = px.bar(
                top_states_df,
                x="Display_State",
                y="total_amount",
                color= "total_amount",
                orientation='v',
                title=f"Top 🔟 States by Transaction Amount ({selected_year})"
            )
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.warning("No top state transaction data available.")

            
        # ------------------ 4th. Query ------------------

        st.subheader("📈 Fastest Growing Districts")

        growth_query = f'''
        SELECT "districts",
        "year",
        SUM(amount) AS total_amount
        FROM public.top_transaction
        WHERE "state"= '{selected_state}'
        GROUP BY "districts", "year"
        ORDER BY "districts", "year";
        '''
        growth_df = pd.read_sql(growth_query, engine)

        if not growth_df.empty:
            growth_df = growth_df.sort_values(["districts", "year"])
            growth_df["growth"] = growth_df.groupby("districts")["total_amount"].pct_change() * 100

            latest_growth = growth_df[growth_df["year"] == selected_year].sort_values(by="growth", ascending=False).head(10)

            if not latest_growth.empty:
                fig6 = px.bar(
                    latest_growth,
                    x="districts",
                    y="growth",
                    color="districts",
                    title=f"Top Growing Districts by Transaction Amount (%) - {selected_year}"
                )
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.warning("No district growth values available for the selected year.")
        else:
            st.warning("No district growth data available.")


        # ------------------ 5th. Query ------------------

        st.subheader("📊 District Contribution Percentage")

        share_query = f'''
        SELECT "districts",
        SUM(amount) AS total_amount
        FROM public.top_transaction
        WHERE "state" = '{selected_state}'
        AND "year" = {selected_year}
        GROUP BY "districts"
        ORDER BY total_amount DESC
        '''
        share_df = pd.read_sql(share_query, engine)

        if not share_df.empty:
            share_df["percentage"] = (share_df["total_amount"] / share_df["total_amount"].sum()) * 100
            top_share = share_df.sort_values(by="percentage", ascending=False).head(10)

            fig7 = px.bar(
                top_share,
                x="percentage",
                y="districts",
                color="percentage",
                orientation='h',
                title=f"Top Districts by Transaction Contribution (%) - {selected_year}"
            )
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.warning("No contribution percentage data available.")