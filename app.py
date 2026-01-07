import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Store Analytics Dashboard", layout="wide", page_icon="🏪")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('store_report_country_cleaned.xlsx')
    # Clean data - remove rows where Country is NaN
    df = df[df['Country'].notna()].copy()
    # Remove 'Total' age group for detailed analysis
    df_detailed = df[df['Age Group'] != 'Total'].copy()
    return df, df_detailed

df_all, df = load_data()

# Title
st.title("Inovocb Interactive Store Analytics Dashboard")
st.markdown("### Explore store performance across countries and age groups")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Store filter - FIXED VERSION
stores = sorted(df['Store Name'].dropna().unique())
selected_stores = st.sidebar.multiselect(
    "Select Stores",
    options=stores,
    default=stores[:5] if len(stores) > 5 else stores
)

# Age group filter
age_groups = sorted([ag for ag in df['Age Group'].unique() if pd.notna(ag)])
selected_ages = st.sidebar.multiselect(
    "Select Age Groups",
    options=age_groups,
    default=age_groups
)

# Filter data based on selections
filtered_df = df[
    (df['Store Name'].isin(selected_stores)) &
    (df['Age Group'].isin(selected_ages))
].copy()

# Aggregate by country
country_data = filtered_df.groupby('Country').agg({
    'Visits': 'sum',
    'Total Spent': 'sum'
}).reset_index()

# Country coordinates (major countries)
country_coords = {
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Belgium': {'lat': 50.5039, 'lon': 4.4699},
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'Poland': {'lat': 51.9194, 'lon': 19.1451},
    'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
    'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
    'Austria': {'lat': 47.5162, 'lon': 14.5501},
    'Portugal': {'lat': 39.3999, 'lon': -8.2245},
    'Algeria': {'lat': 28.0339, 'lon': 1.6596},
    'Morocco': {'lat': 31.7917, 'lon': -7.0926},
    'Tunisia': {'lat': 33.8869, 'lon': 9.5375},
    'Canada': {'lat': 56.1304, 'lon': -106.3468},
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Australia': {'lat': -25.2744, 'lon': 133.7751},
    'Luxembourg': {'lat': 49.8153, 'lon': 6.1296},
    'Greece': {'lat': 39.0742, 'lon': 21.8243},
    'Bulgaria': {'lat': 42.7339, 'lon': 25.4858},
    'Romania': {'lat': 45.9432, 'lon': 24.9668},
    'Croatia': {'lat': 45.1, 'lon': 15.2},
    'Cameroon': {'lat': 7.3697, 'lon': 12.3547},
    'Guinea': {'lat': 9.9456, 'lon': -9.6966},
    'Benin': {'lat': 9.3077, 'lon': 2.3158},
    'Mali': {'lat': 17.5707, 'lon': -3.9962},
    'Senegal': {'lat': 14.4974, 'lon': -14.4524},
    'Gabon': {'lat': -0.8037, 'lon': 11.6094},
    'Haiti': {'lat': 18.9712, 'lon': -72.2852},
    'Ireland': {'lat': 53.4129, 'lon': -8.2439},
    'Norway': {'lat': 60.4720, 'lon': 8.4689},
    'Sweden': {'lat': 60.1282, 'lon': 18.6435},
    'Finland': {'lat': 61.9241, 'lon': 25.7482},
    'Denmark': {'lat': 56.2639, 'lon': 9.5018},
    'Iceland': {'lat': 64.9631, 'lon': -19.0208},
    'Czech Republic': {'lat': 49.8175, 'lon': 15.4730},
    'Slovakia': {'lat': 48.6690, 'lon': 19.6990},
    'Slovenia': {'lat': 46.1512, 'lon': 14.9955},
    'Hungary': {'lat': 47.1625, 'lon': 19.5033},
    'Ukraine': {'lat': 48.3794, 'lon': 31.1656},
    'Cyprus': {'lat': 35.1264, 'lon': 33.4299},
    'Andorra': {'lat': 42.5063, 'lon': 1.5218},
    'Monaco': {'lat': 43.7384, 'lon': 7.4246},
    'Chile': {'lat': -35.6751, 'lon': -71.5430},
    'Peru': {'lat': -9.1900, 'lon': -75.0152},
    'Honduras': {'lat': 15.2000, 'lon': -86.2419},
    'Estonia': {'lat': 58.5953, 'lon': 25.0136},
    'Madagascar': {'lat': -18.7669, 'lon': 46.8691},
    'Mauritius': {'lat': -20.3484, 'lon': 57.5522},
    'Reunion': {'lat': -21.1151, 'lon': 55.5364},
    'Guadeloupe': {'lat': 16.2650, 'lon': -61.5510},
    'Martinique': {'lat': 14.6415, 'lon': -61.0242},
    'French Guiana': {'lat': 3.9339, 'lon': -53.1258},
    'French Polynesia': {'lat': -17.6797, 'lon': -149.4068},
    'Mayotte': {'lat': -12.8275, 'lon': 45.1662},
    'Burkina Faso': {'lat': 12.2383, 'lon': -1.5616},
    'Qatar': {'lat': 25.3548, 'lon': 51.1839},
    'United Arab Emirates': {'lat': 23.4241, 'lon': 53.8478},
    'Israel': {'lat': 31.0461, 'lon': 34.8516},
    'South Africa': {'lat': -30.5595, 'lon': 22.9375},
    'Swaziland': {'lat': -26.5225, 'lon': 31.4659},
    "Cote D'Ivoire (Ivory Coast)": {'lat': 7.5400, 'lon': -5.5471},
    'Democratic Republic of the Congo': {'lat': -4.0383, 'lon': 21.7587},
    'Faroe Islands': {'lat': 61.8926, 'lon': -6.9118},
    'French Southern Territories': {'lat': -49.2804, 'lon': 69.3486},
    'Saint-Martin (French part)': {'lat': 18.0708, 'lon': -63.0501},
    'Dominica': {'lat': 15.4150, 'lon': -61.3710},
    'Suriname': {'lat': 3.9193, 'lon': -56.0278},
    'American Samoa': {'lat': -14.2710, 'lon': -170.1322},
    'Panama': {'lat': 8.5380, 'lon': -80.7821},
    'New Caledonia': {'lat': -20.9043, 'lon': 165.6180},
    'Cape Verde': {'lat': 16.5388, 'lon': -23.0418},
    'El Salvador': {'lat': 13.7942, 'lon': -88.8965},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'Rwanda': {'lat': -1.9403, 'lon': 29.8739},
    'Togo': {'lat': 8.6195, 'lon': 0.8248}
}

# Add coordinates to country data
country_data['lat'] = country_data['Country'].map(lambda x: country_coords.get(x, {}).get('lat'))
country_data['lon'] = country_data['Country'].map(lambda x: country_coords.get(x, {}).get('lon'))
country_data = country_data.dropna(subset=['lat', 'lon'])

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Interactive World Map")

    if len(country_data) > 0:
        # Country selection for detailed view
        selected_countries = st.multiselect(
            "Select countries to highlight and view details:",
            options=sorted(country_data['Country'].unique()),
            default=[]
        )

        # Create map
        fig = px.scatter_geo(
            country_data,
            lat='lat',
            lon='lon',
            hover_name='Country',
            hover_data={
                'Visits': ':,',
                'Total Spent': ':,.2f',
                'lat': False,
                'lon': False
            },
            size='Total Spent',
            size_max=50,
            color='Visits',
            color_continuous_scale='Viridis',
            title='Store Performance by Country',
            projection='natural earth'
        )

        # Highlight selected countries
        if selected_countries:
            selected_data = country_data[country_data['Country'].isin(selected_countries)]
            fig.add_trace(go.Scattergeo(
                lat=selected_data['lat'],
                lon=selected_data['lon'],
                mode='markers',
                marker=dict(size=20, color='red', symbol='star'),
                name='Selected',
                hovertext=selected_data['Country'],
                hoverinfo='text'
            ))

        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with col2:
    st.subheader("📊 Summary Statistics")

    if len(filtered_df) > 0:
        # Key metrics
        total_visits = filtered_df['Visits'].sum()
        total_spent = filtered_df['Total Spent'].sum()
        avg_per_visit = total_spent / total_visits if total_visits > 0 else 0

        st.metric("Total Visits", f"{total_visits:,}")
        st.metric("Total Spent", f"€{total_spent:,.2f}")
        st.metric("Avg Spent per Visit", f"€{avg_per_visit:.2f}")

        # Top countries
        st.subheader("🏆 Top 10 Countries")
        top_countries = country_data.nlargest(10, 'Total Spent')
        for idx, row in top_countries.iterrows():
            st.write(f"**{row['Country']}**")
            st.write(f"├─ Visits: {int(row['Visits']):,}")
            st.write(f"└─ Spent: €{row['Total Spent']:,.2f}")
            st.write("")

# Selected countries detail
if selected_countries:
    st.subheader(f"📍 Detailed View: {', '.join(selected_countries)}")

    for country in selected_countries:
        st.markdown(f"### {country}")

        country_filtered = filtered_df[filtered_df['Country'] == country]

        if len(country_filtered) > 0:
            col_a, col_b = st.columns(2)

            with col_a:
                # By store
                store_summary = country_filtered.groupby('Store Name').agg({
                    'Visits': 'sum',
                    'Total Spent': 'sum'
                }).reset_index()

                fig_store = px.bar(
                    store_summary,
                    x='Store Name',
                    y='Total Spent',
                    title=f'Spending by Store in {country}',
                    labels={'Total Spent': 'Total Spent (€)'}
                )
                fig_store.update_xaxes(tickangle=-45)
                st.plotly_chart(fig_store, use_container_width=True)

            with col_b:
                # By age group
                age_summary = country_filtered.groupby('Age Group').agg({
                    'Visits': 'sum',
                    'Total Spent': 'sum'
                }).reset_index()

                fig_age = px.pie(
                    age_summary,
                    values='Total Spent',
                    names='Age Group',
                    title=f'Spending by Age Group in {country}'
                )
                st.plotly_chart(fig_age, use_container_width=True)

            # Data table
            st.dataframe(
                country_filtered.sort_values('Total Spent', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(f"No data available for {country} with current filters.")

        st.markdown("---")

# Data table section
st.subheader("📋 Filtered Data Table")
if len(filtered_df) > 0:
    st.dataframe(
        filtered_df.sort_values('Total Spent', ascending=False),
        use_container_width=True,
        hide_index=True
    )

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_store_data.csv',
        mime='text/csv',
    )
else:
    st.info("No data matches the selected filters.")