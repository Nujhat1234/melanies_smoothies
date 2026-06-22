# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbKcvidA1YRv5OqD5LWELk1rEQMjqYnQWfJGJ_ewtk1u2cnPdHPlF2rd2b&s=10')

# Write directly to the app
st.title(":green[Customise Your Smoothie] :cup_with_straw: ")
st.write(
  "Blend your way to better health!!!! Choose the fruits you want in your custom smoothie!!"
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

# For local development, create a connection
connection_parameters = {
    "account": "FPTWKTW-OYB54213",
    "user": "oyb54213",
    "password": "SaifeeHiba@pj12",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}
session = Session.builder.configs(connection_parameters).create()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
     my_dataframe
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" +name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:       
          session.sql(my_insert_stmt).collect()
          st.success('Your Smoothie is ordered!', icon="✅")
