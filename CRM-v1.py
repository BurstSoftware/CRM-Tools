import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="CRM Client Data Entry",
    page_icon="📊",
    layout="wide"
)

# File path for storing client data
DATA_FILE = "/home/ubuntu/crm_app/clients.csv"

# Initialize the CSV file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Timestamp", "Name", "Email", "Phone", "Company Name", 
            "Industry Category", "Company Size", "Revenue", 
            "Lead Source", "Sales Rep", "Lead Status", "Notes"
        ])
        df.to_csv(DATA_FILE, index=False)

# Load existing client data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

# Save new client data
def save_client(data):
    df = load_data()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Main app
def main():
    st.title("📊 CRM Client Data Entry System")
    st.markdown("---")
    
    # Initialize data file
    initialize_data_file()
    
    # Create tabs
    tab1, tab2 = st.tabs(["➕ Add New Client", "📋 View Clients"])
    
    # Tab 1: Add New Client
    with tab1:
        st.header("Add New Client")
        
        with st.form("client_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Contact Information")
                name = st.text_input("Client Name *", placeholder="John Doe")
                email = st.text_input("Email *", placeholder="john.doe@example.com")
                phone = st.text_input("Phone Number *", placeholder="+1 (555) 123-4567")
                company_name = st.text_input("Company Name *", placeholder="Acme Corporation")
                
            with col2:
                st.subheader("Business Details")
                industry_category = st.selectbox(
                    "Industry Category *",
                    ["", "Technology", "Finance", "Healthcare", "Manufacturing", 
                     "Retail", "Education", "Real Estate", "Consulting", "Other"]
                )
                
                company_size = st.selectbox(
                    "Company Size *",
                    ["", "1-10 employees", "11-50 employees", "51-200 employees", 
                     "201-500 employees", "501-1000 employees", "1000+ employees"]
                )
                
                revenue = st.selectbox(
                    "Annual Revenue *",
                    ["", "< $100K", "$100K - $500K", "$500K - $1M", 
                     "$1M - $5M", "$5M - $10M", "$10M - $50M", "$50M+"]
                )
                
                lead_source = st.selectbox(
                    "Lead Source *",
                    ["", "Website", "Referral", "Cold Call", "Email Campaign", 
                     "Social Media", "Trade Show", "Partner", "Other"]
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("Sales Information")
                sales_rep = st.text_input("Assigned Sales Rep *", placeholder="Jane Smith")
                
            with col4:
                st.subheader("Lead Status")
                lead_status = st.selectbox(
                    "Lead Status *",
                    ["", "New Lead", "Contacted", "Qualified", "Proposal Sent", 
                     "Negotiation", "Closed Won", "Closed Lost"]
                )
            
            st.subheader("Additional Notes")
            notes = st.text_area("Notes", placeholder="Enter any additional information about the client...", height=100)
            
            # Submit button
            submitted = st.form_submit_button("💾 Save Client", use_container_width=True)
            
            if submitted:
                # Validate required fields
                if not all([name, email, phone, company_name, industry_category, 
                           company_size, revenue, lead_source, sales_rep, lead_status]):
                    st.error("⚠️ Please fill in all required fields marked with *")
                else:
                    # Create client data dictionary
                    client_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name,
                        "Email": email,
                        "Phone": phone,
                        "Company Name": company_name,
                        "Industry Category": industry_category,
                        "Company Size": company_size,
                        "Revenue": revenue,
                        "Lead Source": lead_source,
                        "Sales Rep": sales_rep,
                        "Lead Status": lead_status,
                        "Notes": notes
                    }
                    
                    # Save to CSV
                    save_client(client_data)
                    st.success(f"✅ Client '{name}' from '{company_name}' has been successfully added!")
                    st.balloons()
    
    # Tab 2: View Clients
    with tab2:
        st.header("Client Database")
        
        df = load_data()
        
        if df.empty:
            st.info("No clients in the database yet. Add your first client in the 'Add New Client' tab!")
        else:
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Clients", len(df))
            with col2:
                if "Lead Status" in df.columns:
                    qualified_count = len(df[df["Lead Status"].isin(["Qualified", "Proposal Sent", "Negotiation", "Closed Won"])])
                    st.metric("Qualified Leads", qualified_count)
            with col3:
                if "Lead Status" in df.columns:
                    won_count = len(df[df["Lead Status"] == "Closed Won"])
                    st.metric("Closed Won", won_count)
            with col4:
                if "Sales Rep" in df.columns:
                    unique_reps = df["Sales Rep"].nunique()
                    st.metric("Sales Reps", unique_reps)
            
            st.markdown("---")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if "Lead Status" in df.columns:
                    status_filter = st.multiselect(
                        "Filter by Lead Status",
                        options=df["Lead Status"].unique().tolist(),
                        default=None
                    )
                else:
                    status_filter = []
            
            with col2:
                if "Sales Rep" in df.columns:
                    rep_filter = st.multiselect(
                        "Filter by Sales Rep",
                        options=df["Sales Rep"].unique().tolist(),
                        default=None
                    )
                else:
                    rep_filter = []
            
            with col3:
                if "Industry Category" in df.columns:
                    industry_filter = st.multiselect(
                        "Filter by Industry",
                        options=df["Industry Category"].unique().tolist(),
                        default=None
                    )
                else:
                    industry_filter = []
            
            # Apply filters
            filtered_df = df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df["Lead Status"].isin(status_filter)]
            if rep_filter:
                filtered_df = filtered_df[filtered_df["Sales Rep"].isin(rep_filter)]
            if industry_filter:
                filtered_df = filtered_df[filtered_df["Industry Category"].isin(industry_filter)]
            
            # Display filtered data
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Client Data (CSV)",
                data=csv,
                file_name=f"crm_clients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
