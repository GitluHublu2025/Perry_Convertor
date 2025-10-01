import streamlit as st
import pandas as pd

st.title("🔄 Sathish Unit Conversion Tool-Perry Handbook")

# Step 1: File uploader
uploaded_file = st.file_uploader("Upload your unit conversion CSV", type=["csv"])

if uploaded_file is not None:
    # Load CSV
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Build forward and reverse mapping dictionary
    conversion_dict = {}

    for _, row in df.iterrows():
        from_u = str(row["To convert from"]).strip()
        to_u = str(row["To"]).strip()
        factor = row["Multiply by"]

        # Forward conversion
        conversion_dict.setdefault(from_u, {})[to_u] = factor

        # Reverse conversion
        if factor != 0:  # avoid divide by zero
            conversion_dict.setdefault(to_u, {})[from_u] = 1 / factor

    # Step 2: Dropdown for 'From Unit'
    from_units = sorted(conversion_dict.keys())
    from_unit = st.selectbox("Unit conversion From:", from_units)

    # Step 3: Dropdown for 'To Unit' (filtered)
    to_units = sorted(conversion_dict[from_unit].keys())
    to_unit = st.selectbox("Unit conversion To:", to_units)

    # Step 4: Input value
    input_value = st.number_input(f"Enter value in {from_unit}:", min_value=0.0, format="%.6f")

    # Step 5: Perform conversion
    if st.button("Convert"):
        factor = conversion_dict[from_unit][to_unit]
        result = input_value * factor
        st.success(f"{input_value} {from_unit} = {result} {to_unit}")

    # Step 6: Show all possible conversions for selected "From Unit"
    st.subheader(f"📊 All possible conversions from {from_unit}:")
    all_conversions = pd.DataFrame(
        [
            {"To Unit": k, "Multiply by": v}
            for k, v in conversion_dict[from_unit].items()
        ]
    )
    st.dataframe(all_conversions, use_container_width=True)

else:
    st.info("👆 Please upload a CSV file to begin.")
