import pandas as pd
from fractions import Fraction
import streamlit as st
import base64
import io

def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="output.xlsx" class="download_link">Download Excel file</a>'

def main():
    st.title("👋 Decimal to Fraction Converter")

    # User selects the rounding denominator
    rounding_denominator = st.selectbox('Select rounding denominator', [8, 16, 32], index=1)

    # Upload the dataset
    file = st.file_uploader("Upload an excel file", type=['xlsx'])

    if file is not None:
        # Read the file
        df = pd.read_excel(file)

        # Assuming the column with the decimals is named 'Decimals'
        fractions = []
        for decimal in df['Decimals']:
            # Round to the nearest 1/rounding_denominator
            rounded_decimal = round(decimal * rounding_denominator) / rounding_denominator

            # Convert decimal to fraction
            fraction = Fraction(rounded_decimal).limit_denominator()

            # Convert the fraction to a string
            fraction_str = f"{fraction.numerator}/{fraction.denominator}"

            fractions.append(fraction_str)

        # Add Fractions column to the existing dataframe
        df['Fractions'] = fractions

        # Display the dataframe
        st.dataframe(df)

        # Provide download link for the dataframe in Excel format
        if st.button('Download Excel file'):
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
