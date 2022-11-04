import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import numpy as np



@st.cache(allow_output_mutation=True)
def load_data():
    engine = create_engine(
        "postgresql+pg8000://username:password@localhost:5432/dbt_db"
    )
    query = f"select * from dbt_schema.tweets_hourly"
    df = pd.read_sql_query(query, engine)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return df






# Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


data_load_state = st.text('Loading data...')
data = load_data()
df = data
df['data'] = pd.to_datetime(data['trunc_10_minute'], format=('%Y-%m-%dT%H:%M:%S.%f'))
data_load_state.text("Done! (using st.cache)")


with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Data Infra", "House of Dragon Data Analysis")
    )

if add_radio == "Data Infra":
    st.title('Test')
    st.subheader(
        "Test"
    )
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    selection = aggrid_interactive_table(df=df)

    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
else:
    st.title('Test2')
    st.subheader(
        "Test2"
    )
    columns = ["trunc_10_minute", "csum_tweets"]
    mask = (df['data'] >= "10/17/2022") & (df['data'] <= "10/24/2022")
    filter_df = df.loc[mask]
    st.bar_chart(filter_df, x="data", y="csum_tweets", use_container_width = True)
# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data["trunc_10_minute"], bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

