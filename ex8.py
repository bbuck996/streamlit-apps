import streamlit as st

st.header('Layout Example')

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader('Column 1')
    st.write('This is the left column')
    st.button('Left Button')

with col2:
    st.subheader('Column 2')
    st.write('This is the right column')
    st.button('Right Button')
    