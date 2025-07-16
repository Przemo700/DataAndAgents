import streamlit as st

def shared_page_header(title, subtitle, page_image):

    with st.container():

        col1, col2 = st.columns([5,1])

        with col1:
            st.title(title)
            st.markdown(f"""
                <h1 style='
                    font-size: 14px;
                    color: #ababab;
                    padding: 0;
                '>{subtitle}
                </h1>
            """, unsafe_allow_html=True
            )

        with col2:
            st.image(
                page_image, 
                width=75
            )

    # Add some space after header
    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)