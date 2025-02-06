import streamlit as st
import pandas as pd
from faker import Faker
import random

# 初始化Faker实例并设置中文
fake = Faker('zh_CN')  # 设置为中文

# 页面标题
st.title("动态假数据生成器")


# 将“生成数据条数”和“生成列数”放在同一行
col1, col2 = st.columns(2)
with col1:
    num_rows = st.number_input("选择生成的数据条数", min_value=100, max_value=5000, value=200, step=100)
with col2:
    num_columns = st.number_input("选择生成的列数", min_value=1, max_value=20, value=5, step=1)

# 在“生成数据条数”和“列配置”之间插入分割线
st.markdown("---")  # 插入分割线

# 动态生成列名和数据类型选择
columns = []
column_types = []
min_vals = []  # 存储最小值
max_vals = []  # 存储最大值
custom_values = []  # 存储用户输入的自定义值

# 数据类型的选项（按新顺序）
data_type_options = ["列名", "自定义", "日期", "姓名", "公司", "城市", "国家", "整数", "小数"]

# 每行显示最多5个列配置
cols_per_row = 5
for i in range(0, num_columns, cols_per_row):
    # 创建一行中的多个列
    col_config = st.columns(cols_per_row)
    for j in range(cols_per_row):
        idx = i + j
        if idx >= num_columns:
            break  # 如果超出列数限制，停止循环
        
        with col_config[j]:  # 在当前列中添加控件
            st.markdown(f"**第 {idx+1} 列配置**")
            col_name = st.text_input(f"列名", f"Column {idx+1}", key=f"col_name_{idx}")
            column_type = st.selectbox(f"数据类型", data_type_options, index=0, key=f"type_{idx}")
            
            if column_type == "整数":
                min_val = st.number_input(f"最小值", value=0, key=f"min_{idx}")
                max_val = st.number_input(f"最大值", value=100, key=f"max_{idx}")
                if min_val >= max_val:
                    st.error("最大值必须大于最小值！")
                min_vals.append(min_val)
                max_vals.append(max_val)
                custom_values.append(None)  # 自定义值为空
            elif column_type == "小数":
                min_val = st.number_input(f"最小值", value=0.0, step=0.01, format="%.2f", key=f"min_{idx}")
                max_val = st.number_input(f"最大值", value=100.0, step=0.01, format="%.2f", key=f"max_{idx}")
                if min_val >= max_val:
                    st.error("最大值必须大于最小值！")
                min_vals.append(min_val)
                max_vals.append(max_val)
                custom_values.append(None)  # 自定义值为空
            elif column_type == "自定义":
                custom_input = st.text_input(
                    f"请输入逗号或顿号分隔的值",
                    "默认值1、默认值2、默认值3",
                    key=f"custom_{idx}"
                )
                # 支持中文逗号和顿号分隔符
                custom_list = [val.strip() for val in custom_input.replace("，", ",").replace("、", ",").split(",") if val.strip()]
                if not custom_list:
                    st.error("自定义值不能为空！")
                custom_values.append(custom_list)  # 存储用户输入的自定义值
                min_vals.append(None)
                max_vals.append(None)
            else:
                min_vals.append(None)
                max_vals.append(None)
                custom_values.append(None)  # 自定义值为空
            
            columns.append(col_name)
            column_types.append(column_type)
    
    # 在每行配置结束后插入分割线
    if i + cols_per_row < num_columns:  # 只有当还有下一行时才插入分割线
        st.markdown("---")  # 插入分割线

# 按钮点击后生成数据
if 'df' not in st.session_state:
    st.session_state.df = None  # 初始化 DataFrame 状态

# 创建两列布局：左侧放按钮，右侧放表格
button_col, table_col = st.columns([1, 3])  # 左侧按钮占1份宽度，右侧表格占3份宽度

with button_col:
    if st.button("生成假数据"):
        # 数据验证：检查是否有错误
        has_error = False
        for min_val, max_val in zip(min_vals, max_vals):
            if min_val is not None and max_val is not None and min_val >= max_val:
                has_error = True
                break
        for custom_val in custom_values:
            if custom_val is not None and len(custom_val) == 0:
                has_error = True
                break
        
        if has_error:
            st.error("数据验证失败，请检查最小值/最大值或自定义值是否正确！")
        else:
            data = []
            for _ in range(num_rows):
                row = {}
                for col_name, col_type, min_val, max_val, custom_val in zip(columns, column_types, min_vals, max_vals, custom_values):
                    if col_type == "列名":
                        products = [f"{col_name}{i+1}" for i in range(5)]
                        row[col_name] = random.choice(products)
                    elif col_type == "自定义":
                        if custom_val:  # 如果用户输入了自定义值
                            row[col_name] = random.choice(custom_val)
                        else:
                            row[col_name] = None  # 如果没有输入值，默认为 None
                    elif col_type == "日期":
                        row[col_name] = fake.date_this_year().strftime("%Y-%m-%d")  # 生成今年的随机日期
                    elif col_type == "姓名":
                        row[col_name] = fake.name()
                    elif col_type == "公司":
                        row[col_name] = fake.company()
                    elif col_type == "城市":
                        row[col_name] = fake.city()
                    elif col_type == "国家":
                        row[col_name] = fake.country()
                    elif col_type == "整数":
                        row[col_name] = fake.random_int(min=min_val, max=max_val)
                    elif col_type == "小数":
                        row[col_name] = round(random.uniform(min_val, max_val), 2)  # 保留两位小数
                data.append(row)
            
            # 转换为pandas DataFrame
            st.session_state.df = pd.DataFrame(data)
            
            # 显示提示信息
            st.success("假数据已生成！")

    if st.session_state.df is not None:  # 只有在生成假数据后才显示下载按钮
        # 提供下载链接：导出为Excel
        from io import BytesIO
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='Fake Data')
        
        # 将文件的指针移动到文件开头
        excel_file.seek(0)
        
        # 提供下载按钮
        st.download_button(
            label="下载为Excel",
            data=excel_file,
            file_name="fake_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with table_col:
    if st.session_state.df is not None:
        # 自定义CSS样式，使表格宽度占满屏幕
        st.markdown(
            """
            <style>
            .full-width-table {
                width: 100% !important;
                overflow-x: auto;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # 显示生成的假数据表格
        st.write("生成的假数据：")
        st.dataframe(st.session_state.df, use_container_width=True)