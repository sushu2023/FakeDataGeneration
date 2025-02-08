import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("宽屏模式示例")

# 添加一些内容
st.markdown("这是一个以宽屏模式运行的 Streamlit 应用。")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.header("左侧内容")
    st.write("这里是左侧的内容区域。")

with col2:
    st.header("右侧内容")
    st.write("这里是右侧的内容区域。")