import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from typing import Optional

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="DataNexus | Enterprise Analytics Hub",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS: Clean typography, rounded corners, shadow depth
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

# --- 3. HELPER FUNCTIONS (Typed & Documented) ---

@st.cache_data
def load_data(file) -> Optional[pd.DataFrame]:
    """
    Loads CSV or Excel data into a Pandas DataFrame using Lazy Loading.
    Args:
        file: The uploaded file object.
    Returns:
        pd.DataFrame or None if error occurs.
    """
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None

def convert_df(df: pd.DataFrame) -> bytes:
    """
    Converts DataFrame to CSV bytes for download.
    """
    return df.to_csv(index=False).encode('utf-8')

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103665.png", width=60)
    st.title("DataNexus")
    st.markdown("*Enterprise Analytics Hub*")
    st.divider()
    
    menu = st.radio(
        "Navigation Module:",
        ["📁 Ingestion", "🔍 Profiling", "🧹 Transformation", "📈 Visualization"],
        index=0
    )
    
    st.divider()
    st.info("System Status: Online \nVersion: 1.2.0 (Stable)")

# --- 5. MAIN MODULES ---

# === MODULE 1: INGESTION ===
if menu == "📁 Ingestion":
    st.header("📂 Data Ingestion Interface")
    st.markdown("Upload raw datasets (`.csv`, `.xlsx`) to initialize the ETL pipeline.")
    
    uploaded_file = st.file_uploader("Drag and drop source file", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.session_state['df'] = df
            st.session_state['file_name'] = uploaded_file.name
            st.toast("File successfully loaded!", icon="✅")
            
            # KPI Metrics Row
            st.subheader("Dataset Telemetry")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Rows", f"{df.shape[0]:,}")
            c2.metric("Total Columns", df.shape[1])
            c3.metric("Missing Values", df.isnull().sum().sum())
            c4.metric("Duplicates", df.duplicated().sum())
            
            st.divider()
            st.subheader("Raw Data Preview")
            # st.dataframe is standard, but st.data_editor is modern & interactive
            st.data_editor(df.head(50), use_container_width=True)

# === MODULE 2: PROFILING ===
elif menu == "🔍 Profiling":
    st.header("📊 Automated Data Profiling")
    
    if st.session_state['df'] is None:
        st.warning("⚠️ No data loaded. Please go to the Ingestion module.")
    else:
        df = st.session_state['df']
        
        # Tabbed interface for cleaner UX
        tab1, tab2, tab3 = st.tabs(["Overview", "Missing Data Analysis", "Correlation Matrix"])
        
        with tab1:
            st.subheader("Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
            
            st.subheader("Data Types")
            dtypes = df.dtypes.value_counts()
            fig_dtypes = px.pie(values=dtypes.values, names=dtypes.index.astype(str), 
                                title="Column Data Type Distribution", hole=0.4,
                                color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig_dtypes, use_container_width=True)

        with tab2:
            st.subheader("Null Value Heatmap")
            missing = df.isnull().sum()
            if missing.sum() > 0:
                st.bar_chart(missing[missing > 0])
            else:
                st.success("✅ Dataset is clean. No missing values detected.")

        with tab3:
            st.subheader("Correlation Analysis")
            # Filter only numeric columns for correlation
            numeric_df = df.select_dtypes(include=['float64', 'int64'])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("Not enough numeric columns to generate correlation matrix.")

# === MODULE 3: TRANSFORMATION ===
elif menu == "🧹 Transformation":
    st.header("🛠️ ETL Transformation Engine")
    
    if st.session_state['df'] is None:
        st.warning("⚠️ No data loaded. Please go to the Ingestion module.")
    else:
        df = st.session_state['df']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container(border=True):
                st.subheader("🗑️ Drop Features")
                cols_to_drop = st.multiselect("Select columns to remove", df.columns)
                if st.button("Execute Drop", type="primary"):
                    st.session_state['df'] = df.drop(columns=cols_to_drop)
                    st.success("Columns removed successfully.")
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader("🩹 Impute Missing Values")
                col_option = st.selectbox("Select Target Column", df.columns)
                method = st.radio("Imputation Method", ["Drop Rows", "Fill with 0", "Fill with Mean"])
                
                if st.button("Apply Transformation"):
                    if method == "Drop Rows":
                        st.session_state['df'] = df.dropna(subset=[col_option])
                    elif method == "Fill with 0":
                        st.session_state['df'][col_option] = df[col_option].fillna(0)
                    elif method == "Fill with Mean":
                        if pd.api.types.is_numeric_dtype(df[col_option]):
                            st.session_state['df'][col_option] = df[col_option].fillna(df[col_option].mean())
                        else:
                            st.error("Operation failed: Cannot calculate mean for non-numeric column.")
                            st.stop()
                    st.success("Transformation applied.")
                    st.rerun()

        st.divider()
        
        # NEW FEATURE: Filtering
        with st.expander("🔎 Advanced Filtering (New)"):
            filter_col = st.selectbox("Filter by Column", df.columns)
            if pd.api.types.is_numeric_dtype(df[filter_col]):
                min_val = float(df[filter_col].min())
                max_val = float(df[filter_col].max())
                val_range = st.slider(f"Select range for {filter_col}", min_val, max_val, (min_val, max_val))
                
                if st.button("Apply Filter"):
                    st.session_state['df'] = df[(df[filter_col] >= val_range[0]) & (df[filter_col] <= val_range[1])]
                    st.success("Filter applied!")
                    st.rerun()

        st.subheader("✅ Processed Data Snapshot")
        st.dataframe(st.session_state['df'].head(10), use_container_width=True)
        
        csv = convert_df(st.session_state['df'])
        st.download_button(
            label="⬇️ Download Processed Dataset",
            data=csv,
            file_name=f"processed_{st.session_state['file_name']}",
            mime='text/csv'
        )

# === MODULE 4: VISUALIZATION ===
elif menu == "📈 Visualization":
    st.header("📊 Interactive Analytics Dashboard")
    
    if st.session_state['df'] is None:
        st.warning("⚠️ No data loaded. Please go to the Ingestion module.")
    else:
        df = st.session_state['df']
        
        with st.container(border=True):
            st.subheader("Chart Configuration")
            c1, c2, c3, c4 = st.columns(4)
            
            chart_type = c1.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Histogram", "Box"])
            x_axis = c2.selectbox("X-Axis", df.columns)
            y_axis = c3.selectbox("Y-Axis", df.columns) 
            color_enc = c4.selectbox("Color Grouping (Optional)", [None] + list(df.columns))
            
        st.write("---")
        
        try:
            fig = None
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_enc, title=f"{y_axis} by {x_axis}", template="plotly_white")
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_enc, title=f"{y_axis} Trends", template="plotly_white")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_enc, title=f"Correlation: {y_axis} vs {x_axis}", template="plotly_white")
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, color=color_enc, title=f"Distribution of {x_axis}", template="plotly_white")
            elif chart_type == "Box":
                fig = px.box(df, x=x_axis, y=y_axis, color=color_enc, title=f"Distribution of {y_axis} by {x_axis}", template="plotly_white")
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("🔎 View Chart Data"):
                    st.dataframe(df[[x_axis, y_axis]].head(20))
                    
        except Exception as e:
            st.error(f"⚠️ Error creating chart: {e}. Ensure Y-Axis is numeric for this chart type.")