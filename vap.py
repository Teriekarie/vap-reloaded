import streamlit as st
import pandas as pd
import plotly.express as px
# import seaborn as sns


# Define the data loading function
def load_data():
    data_path = "VAP_cleaned_data1.csv"
    df = pd.read_csv(data_path)
   
    return df

df = load_data()


# Use st.cache_data to cache the loaded data
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# Dashboard title
st.title("VAP Market Research Analysis")

# Overview and summary statistics
st.header("Overview")
total_shops = df.shape[0]  # Use shape[0] to get the number of rows in the DataFrame
st.write(f"Total Shops: {total_shops}")

# Interactive filters in the sidebar
st.sidebar.header("Search Market")
market_names = df["X3..Market.Name"].unique()
selected_market = st.sidebar.selectbox("Select a Market", options=market_names)

# Dashboard Filters in Sidebar
st.sidebar.header("Filter Options")
# filters based on new columns
group_filter = st.sidebar.multiselect("Group", options=df["X4...Group."].unique())
shop_occupancy_status_filter = st.sidebar.multiselect("Shop Occupancy Status", options=df["X11..Shop.Occupancy.Status"].unique())

# Applying multiple filters to the dataframe
filtered_data = df[df["X4...Group."].isin(group_filter) & df["X11..Shop.Occupancy.Status"].isin(shop_occupancy_status_filter)]


# Sidebar Filters
st.sidebar.header("Paticipation Status")
# Example of a select box for filtering by agreement to participate in the study
agreement_filter = st.sidebar.selectbox("Do you agree to participate in this study?", options=df["Do.you.agree.to.participate.in.this.study."].unique())

# Apply filters to the dataframe based on selection
filtered_data = df[df["Do.you.agree.to.participate.in.this.study."] == agreement_filter]

# Overview and summary statistics
st.header("Data Overview")
st.write(filtered_data.head())  # Show filtered data


# Filtering data based on selection
filtered_data = df[df["X3..Market.Name"] == selected_market]

# Display filtered data
#st.header("Filtered Data")
#st.write(filtered_data.head())  # Display only the top rows

# Visualizations
## Visualization 1: Distribution of Shop Occupancy Status
st.header("Shop Occupancy Status Distribution")
occupancy_status_counts = filtered_data["X11..Shop.Occupancy.Status"].value_counts()
fig_occupancy = px.pie(names=occupancy_status_counts.index, values=occupancy_status_counts.values, title="Shop Occupancy Status")
st.plotly_chart(fig_occupancy)

## Visualization 2: Number of People Working in the Shop
st.header("Number of People Working in Shops")
fig_people = px.histogram(filtered_data, x="X17..How.many.people.work.in.your.shop.each.day.", title="People Working in Shops")
st.plotly_chart(fig_people)

## Visualization 3: Shop Type Distribution
st.header("Shop Type Distribution")
shop_type_counts = filtered_data["X13..Shop.Type"].value_counts()
fig_shop_type = px.bar(x=shop_type_counts.index, y=shop_type_counts.values, title="Shop Types")
st.plotly_chart(fig_shop_type)

## Shop Closing Time Analysis
st.header("Shop Closing Time Analysis")
fig_closing_time = px.histogram(filtered_data, x="X19..Shop.Closing.Time", title="Distribution of Shop Closing Times")
st.plotly_chart(fig_closing_time)

## Number of Employees in Shops
st.header("Number of Employees in Shops")
fig_employees = px.histogram(filtered_data, x="X17..How.many.people.work.in.your.shop.each.day.", title="Number of Employees")
st.plotly_chart(fig_employees)

## Bank Account Ownership among Shop Owners
st.header("Bank Account Ownership")
bank_account_ownership = filtered_data["X20..Does.the.shop.owner.have.a.bank.account."].value_counts(normalize=True) * 100
fig_bank_account = px.pie(names=bank_account_ownership.index, values=bank_account_ownership.values, title="Bank Account Ownership among Shop Owners")
st.plotly_chart(fig_bank_account)

## Use of Smartphones
st.header("Smartphone Ownership")
smartphone_ownership = filtered_data["X23..Does.the.shop.owner.Have..a.smart.phone."].value_counts(normalize=True) * 100
fig_smartphone = px.pie(names=smartphone_ownership.index, values=smartphone_ownership.values, title="Smartphone Ownership")
st.plotly_chart(fig_smartphone)

## Payment Platform Usage
st.header("Payment Platform Usage")
payment_platform_usage = filtered_data["X24..Which.payment.platform.have.you.used."].value_counts()
fig_payment_platform = px.bar(x=payment_platform_usage.index, y=payment_platform_usage.values, title="Payment Platform Usage")
st.plotly_chart(fig_payment_platform)

# Geo-spatial representation on a map
st.header("Shop Locations on Map")
fig = px.scatter_mapbox(filtered_data,
                        lat="Latitude",
                        lon="Longitude",
                        hover_name="Address_ID",
                        color_discrete_sequence=["fuchsia"],
                        zoom=3,
                        height=500)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)

# Select numerical columns for correlation analysis
#numerical_data = df.select_dtypes(include=['float64', 'int64'])

# Calculate correlation matrix
#corr = numerical_data.corr()

# Plot heatmap
#st.header("Correlation Heatmap")
#fig, ax = px.subplots()
#sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
#st.pyplot(fig)