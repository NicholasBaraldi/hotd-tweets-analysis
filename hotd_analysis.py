import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import numpy as np
from datetime import date
from PIL import Image



@st.cache(allow_output_mutation=True)
def load_data():
    engine = create_engine(
        "postgresql+pg8000://username:password@localhost:5432/dbt_db"
    )
    query = f"select * from dbt_schema.tweets_hourly"
    df = pd.read_sql_query(query, engine)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return df


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
df['date'] = pd.to_datetime(df['trunc_10_minute']).dt.date
data_load_state.text("Done! (using st.cache)")


with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Data Infra", "House of Dragon Data Analysis")
    )

if add_radio == "Data Infra":
    st.title('Data Infra')
    st.subheader(
        "Documentation"
    )
    image = Image.open('assests/house-of-the-dragon-capa.webp')
    st.image(image, caption='House of The Dragon')
    st.markdown("""
        Esse projeto foi um inferno, deu quase tudo errado, mas no final deu pra aprender.


        """)
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

else:
    st.title('House of Dragon Data Analysis')
    d = st.date_input("When's your birthday", date(2022, 10, 16))
    st.subheader(
        "Soma acumulada de tweets"
    )
    columns = ["trunc_10_minute", "csum_tweets"]
    mask = (df['date'] >= d) & (df['date'] <= d)
    filter_df = df.loc[mask]
    st.bar_chart(filter_df, x="data", y="csum_tweets", use_container_width = True)
    st.subheader(
        "Soma acumulada de usuários"
    )
    st.bar_chart(filter_df, x="data", y="csum_users", use_container_width = True)
    


