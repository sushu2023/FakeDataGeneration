from datetime import date
import pandas as pd
import streamlit as st

# 创建示例数据
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Birthdate": [date(1990, 1, 1), date(1985, 6, 15), date(1980, 11, 30)],
    "Score": [85.5, 92.3, 78.0]
})

# 自定义列配置
edited_df = st.data_editor(
    df,
    column_config={
        "Name": "Full Name",  # 修改列名
        "Birthdate": st.column_config.DateColumn("Birthdate", format="YYYY-MM-DD"),  # 设置日期格式
        "Score": st.column_config.NumberColumn("Score", min_value=0, max_value=100, step=0.1)  # 设置数值范围
    }
)
st.write("编辑后的数据：", edited_df)

