import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="CRM Client Data Entry",
    page_icon="Chart",
    layout="wide"
)

# DATA FILE — saved in the same folder as this script (works on Streamlit Cloud!)
DATA_FILE = "clients.csv"

# Initialize the CSV file with headers if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Timestamp", "Name", "Email", "Phone", "Company Name",
            "Industry Category", "Company Size", "Revenue",
            "Lead Source", "Sales Rep", "Lead Status", "Notes"
        ])
        df.to_csv(DATA_FILE, index=False)

# Load data from CSV
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception as e:
            st.error(f"Error reading data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Save new client entry
def save_client(data):
    df = load_data()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Main App
def main():
    st.title("CRM Client Data Entry System")
    st.markdown("---")

    # Always initialize (safe to call multiple times)
    initialize_data_file()

    tab1, tab2 = st.tabs(["Add New Client", "View & Download Clients"])

    # === TAB 1: Add New Client ===
    with tab1:
        st.header("Add New Client")

        with st.form("client_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Contact Info")
                name = st.text_input("Client Name *", placeholder="John Doe")
                email = st.text_input("Email *", placeholder="john@example.com")
                phone = st.text_input("Phone *", placeholder="+1 (555) 123-4567")
                company_name = st.text_input("Company Name *", placeholder="Acme Corp")

            with col2:
                st.subheader("Business Details")
                industry_category = st.selectbox(
                    "Industry Category *",
                    ["", "Technology", "Finance", "Healthcare", "Manufacturing",
                     "Retail", "Education", "Real Estate", "Consulting", "Other"]
                )
                company_size = st.selectbox(
                    "Company Size *",
                    ["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
                )
                revenue = st.selectbox(
                    "Annual Revenue *",
                    ["", "< $100K", "$100K-$500K", "$500K-$1M", "$1M-$5M",
                     "$5M-$10M", "$10M-$50M", "$50M+"]
                )
                lead_source = st.selectbox(
                    "Lead Source *",
                    ["", "Website", "Referral", "Cold Call", "Email Campaign",
                     "Social Media", "Trade Show", "Partner", "Other"]
                )

            col3, col4 = st.columns(2)
            with col3:
                sales_rep = st.text_input("Sales Rep *", placeholder="Jane Smith")
            with col4:
                lead_status = st.selectbox(
                    "Lead Status *",
                    ["", "New Lead", "Contacted", "Qualified", "Proposal Sent",
                     "Negotiation", "Closed Won", "Closed Lost"]
                )

            notes = st.text_area("Notes", placeholder="Additional info...", height=100)

            submitted = st.form_submit_button("Save Client", use_container_width=True)

            if submitted:
                required = [name, email, phone, company_name, industry_category,
                            company_size, revenue, lead_source, sales_rep, lead_status]
                if not all(required):
                    st.error("Please fill all required fields (*)")
                else:
                    client_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name, "Email": email, "Phone": phone,
                        "Company Name": company_name, "Industry Category": industry_category,
                        "Company Size": company_size, "Revenue": revenue,
                        "Lead Source": lead_source, "Sales Rep": sales_rep,
                        "Lead Status": lead_status, "Notes": notes or ""
                    }
                    save_client(client_data)
                    st.success(f"Client '{name}' added successfully!")
                    st.balloons()

    # === TAB 2: View & Download ===
    with tab2:
        st.header("All Clients")

        df = load_data()

        if df.empty:
            st.info("No clients yet. Add one in the first tab!")
        else:
            # Summary Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clients", len(df))
            with col2:
                qualified = len(df[df["Lead Status"].isin(["Qualified", "Proposal Sent", "Negotiation", "Closed Won"])])
                st.metric("Qualified Leads", qualified)
            with col3:
                won = len(df[df["Lead Status"] == "Closed Won"])
                st.metric("Closed Won", won)

            st.markdown("---")

            # Filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect("Lead Status", options=df["Lead Status"].unique())
            with col2:
                rep_filter = st.multiselect("Sales Rep", options=df["Sales Rep"].unique())

            filtered_df = df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df["Lead Status"].isin(status_filter)]
            if rep_filter:
                filtered_df = filtered_df[filtered_df["Sales Rep"].isin(rep_filter)]

            # Show table
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)

            # DOWNLOAD BUTTON
            csv = filtered_df.to_csv(index=False).encode()
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name=f"crm_clients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Also offer full data download
            full_csv = df.to_csv(index=False).encode()
            st.download_button(
                label="Download ALL Clients (Unfiltered)",
                data=full_csv,
                file_name=f"crm_all_clients_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
