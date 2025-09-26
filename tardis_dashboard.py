import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#load dataset
df = pd.read_csv("cleaned_dataset.csv")


delay_columns = [
    'Average delay of late trains at departure',
    'Average delay of all trains at departure',
    'Average delay of all trains at arrival',
    'Average delay of late trains at arrival',
    'Average delay of trains > 15min (if competing with flights)'
]

st.title("🚂Tardis Dashboard🚂")
st.title("Welcome👋😃")
selected_column = st.selectbox("What delay statistic did you want to view?📊 :", delay_columns)

# Histograms
st.subheader("📊 Histograms")
fig1, ax1 = plt.subplots()
sns.histplot(df[selected_column], bins=30, kde=True, ax=ax1, color="skyblue")
ax1.set_xlabel("Minutes de retard")
ax1.set_ylabel("Nombre de trains")
st.pyplot(fig1)

# Boxplot
st.subheader("📦 Boxplot of arrival delay⏰ by arrival station🚉")
fig_arrival, ax_arrival = plt.subplots()
sns.boxplot(
    data=df,
    x=df['Arrival station'], 
    y=df['Average delay of all trains at arrival'], 
    ax=ax_arrival,
    hue='Arrival station',
    palette="Reds"
)
ax_arrival.set_title("Delay in arrival by station")
ax_arrival.set_xlabel("Arrival station")
ax_arrival.set_ylabel("Average delay in arrival (min)")
plt.xticks(rotation=45)
st.pyplot(fig_arrival)

st.subheader("📦 Boxplot of departure delay⏰ by departure station🚉")

fig_departure, ax_departure = plt.subplots()
sns.boxplot(
    data=df,
    x=df['Departure station'], 
    y=df['Average delay of all trains at departure'],
    hue='Departure station',
    ax=ax_departure, 
    palette="Greens"
)
ax_departure.set_title("Delay in departure by station")
ax_departure.set_xlabel("Departure station")
ax_departure.set_ylabel("Average delay on departure (min)")
plt.xticks(rotation=45)
st.pyplot(fig_departure)

st.header("❌ Cancellation Rates")

# Slider to choose how many stations to display
top_n = st.slider("Choose the number of stations to display", min_value=5, max_value=35, value=15)

# Aggregate the number of cancelled trains per departure station
cancelled_total = df.groupby('Departure station')['Number of cancelled trains'].sum().sort_values(ascending=False)

# Select the top N stations with the most cancellations
top_cancelled = cancelled_total.head(top_n).reset_index()
top_cancelled.columns = ['Departure station', 'Cancelled trains']

# Display the data table
st.subheader("📋 Top stations with the most cancellations")
st.dataframe(top_cancelled)

# Display the bar chart
st.subheader("📊 Cancellation chart by station")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=top_cancelled,
    x='Departure station',
    y='Cancelled trains',
    hue='Departure station',
    palette='Purples',
    ax=ax
)
ax.set_ylabel("Number of cancelled trains")
ax.set_xlabel("Departure station")
ax.set_title("Top stations by number of cancelled trains")
plt.xticks(rotation=45)
st.pyplot(fig)

st.header("🔥 Heatmaps to show correlations between delay factors")

# All available correlation columns
all_correlation_columns = [
    'Pct delay due to external causes',
    'Pct delay due to infrastructure',
    'Pct delay due to traffic management'
]

# Multiselect for user to choose which columns to include
selected_corr_columns = st.multiselect(
    "📌 Select 2️⃣ delay factors to include in the correlation heatmap:",
    options=all_correlation_columns,
)

# Filter and compute correlation only if at least two columns are selected
if len(selected_corr_columns) >= 2:
    df_corr = df[selected_corr_columns].dropna()
    corr_matrix = df_corr.corr()

    # Display the heatmap
    st.subheader("📊 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Correlation between selected delay factors")
    st.pyplot(fig)
else:
    st.warning("Please select at least 2️⃣ factors to generate the heatmap.")

df['Date'] = pd.to_datetime(df['Date'])

st.header("🧭 Interactive Route & Month Range Analysis")

# Select departure station
departure_station = st.selectbox(
    "🚉 Select a departure station:",
    options=df['Departure station'].unique()
)

# Select arrival station
arrival_station = st.selectbox(
    "🏁 Select an arrival station:",
    options=df['Arrival station'].unique()
)

# Create a column with just month and year as Period
df['MonthPeriod'] = df['Date'].dt.to_period('M')

# Get all available months
available_months = sorted(df['MonthPeriod'].unique())

# Select a range of months
selected_range = st.select_slider(
    "🗓️ Select a range of months:",
    options=available_months,
    value=(available_months[0], available_months[-1])
)

# Filter data based on route and selected month range
filtered_df = df[
    (df['Departure station'] == departure_station) &
    (df['Arrival station'] == arrival_station) &
    (df['MonthPeriod'] >= selected_range[0]) &
    (df['MonthPeriod'] <= selected_range[1])
]

# Display route statistics
st.subheader("📊 Route Statistics")
st.metric("Average delay at departure", f"{filtered_df['Average delay of all trains at departure'].mean():.2f} min")
st.metric("Average delay at arrival", f"{filtered_df['Average delay of all trains at arrival'].mean():.2f} min")
st.metric("Number of cancelled trains", f"{filtered_df['Number of cancelled trains'].sum()}")

# Show filtered train records
st.subheader(f"📋 Train records from {selected_range[0]} to {selected_range[1]}")
st.dataframe(filtered_df)

st.header("📊 Global Train Traffic Statistics")

# Calculate average delays
avg_departure_delay = df['Average delay of all trains at departure'].mean()
avg_arrival_delay = df['Average delay of all trains at arrival'].mean()

# Total number of cancelled trains
total_cancelled = df['Number of cancelled trains'].sum()

# Total number of trains
total_trains = len(df)

# Convert relevant columns to numeric format
cols = [
    "Number of scheduled trains",
    "Number of trains delayed at arrival",
    "Number of cancelled trains"
]

for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Remove rows where scheduled train count is missing or zero
df = df[df["Number of scheduled trains"] > 0].copy()

# Calculate percentages for each row
df["pct_delayed"] = df["Number of trains delayed at arrival"] / df["Number of scheduled trains"] * 100
df["pct_cancelled"] = df["Number of cancelled trains"] / df["Number of scheduled trains"] * 100
df["pct_on_time"] = 100 - (df["pct_delayed"] + df["pct_cancelled"])

# Compute average punctuality percentage
avg_pct_on_time = df["pct_on_time"].mean()

# Estimate punctuality rate based on total trains
punctuality_rate = (avg_pct_on_time * total_trains) / 100

# Display key metrics
st.metric("Average delay at departure", f"{avg_departure_delay:.2f} min")
st.metric("Average delay at arrival", f"{avg_arrival_delay:.2f} min")
st.metric("Total number of cancelled trains", int(total_cancelled))
st.metric("Estimated punctuality rate", f"{punctuality_rate:.2f} trains out of {total_trains}")
