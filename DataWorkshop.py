import streamlit as st
import pandas as pd
from faker import Faker
import random
import uuid

# 初始化Faker实例并设置中文
fake = Faker('zh_CN')  # 设置为中文

# 页面标题
st.title("动态数据生成器")

# 自定义CSS样式，使弹窗提示为绿色
st.markdown(
    """
    <style>
    .stToast {
        background-color: #d4edda; /* 绿色背景 */
        color: #155724;           /* 深绿色文字 */
        border: 1px solid #c3e6cb; /* 边框颜色 */
        border-radius: 0.25rem;   /* 圆角 */
        padding: 0.75rem;         /* 内边距 */
        margin-bottom: 1rem;      /* 外边距 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 创建标签页
tab_default, tab_auto, tab_bank, tab_retail, tab_pharma = st.tabs(
    ["默认", "汽车", "银行", "零售", "医药"]
)

# 定义每个标签的默认列配置
default_columns = {
    "默认": [
        {"name": "ID", "type": "UUID"},  # 修改为 UUID 类型
        {"name": "姓名", "type": "姓名", "unique_count": 5},
        {"name": "城市", "type": "城市", "unique_count": 5},
        {"name": "注册日期", "type": "日期"},
        {"name": "金额", "type": "小数", "min": 100.0, "max": 10000.0},
    ],
    "汽车": [
        {"name": "车辆ID", "type": "UUID"},  # 添加 UUID 类型
        {"name": "品牌", "type": "自定义", "custom_values": "宝马, 奔驰, 特斯拉"},
        {"name": "车型", "type": "自定义", "custom_values": "轿车, SUV, 跑车"},
        {"name": "生产日期", "type": "日期"},
        {"name": "价格", "type": "小数", "min": 10000.0, "max": 100000.0},
    ],
    "银行": [
        {"name": "账户ID", "type": "UUID"},  # 添加 UUID 类型
        {"name": "客户姓名", "type": "姓名", "unique_count": 5},
        {"name": "账户类型", "type": "自定义", "custom_values": "储蓄账户, 信用卡账户"},
        {"name": "余额", "type": "小数", "min": 0.0, "max": 100000.0},
        {"name": "开户日期", "type": "日期"},
    ],
    "零售": [
        {"name": "订单ID", "type": "UUID"},  # 添加 UUID 类型
        {"name": "客户姓名", "type": "姓名", "unique_count": 5},
        {"name": "商品名称", "type": "自定义", "custom_values": "苹果, 香蕉, 橙子"},
        {"name": "购买数量", "type": "整数", "min": 1, "max": 10},
        {"name": "购买日期", "type": "日期"},
    ],
    "医药": [
        {"name": "药品ID", "type": "UUID"},  # 添加 UUID 类型
        {"name": "药品名称", "type": "自定义", "custom_values": "阿司匹林, 维生素C, 抗生素"},
        {"name": "生产厂家", "type": "公司", "unique_count": 5},
        {"name": "生产日期", "type": "日期"},
        {"name": "有效期", "type": "整数", "min": 1, "max": 36},
    ],
}

# 动态生成列配置函数
def generate_column_config(tab_name):
    columns = []
    column_types = []
    min_vals = []  # 存储最小值
    max_vals = []  # 存储最大值
    custom_values = []  # 存储用户输入的自定义值
    unique_counts = []  # 存储每个列的独特数据数量

    # 获取当前标签的默认列配置
    default_config = default_columns.get(tab_name, [])

    # 每行显示最多5个列配置
    cols_per_row = 5
    for i in range(0, len(default_config), cols_per_row):
        col_config = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(default_config):
                break  # 如果超出列数限制，停止循环
            
            config = default_config[idx]
            col_name = config["name"]
            column_type = config["type"]

            with col_config[j]:  # 在当前列中添加控件
                st.markdown(f"**第 {idx+1} 列配置**")
                col_name = st.text_input(f"列名", col_name, key=f"{tab_name}_col_name_{idx}")
                column_type = st.selectbox(
                    f"数据类型",
                    ["列名", "自定义", "日期", "姓名", "公司", "城市", "国家", "整数", "小数", "UUID"],  # 添加 UUID 类型
                    index=["列名", "自定义", "日期", "姓名", "公司", "城市", "国家", "整数", "小数", "UUID"].index(column_type),
                    key=f"{tab_name}_type_{idx}",
                )

                if column_type == "整数":
                    min_val = st.number_input(f"最小值", value=config.get("min", 0), key=f"{tab_name}_min_{idx}")
                    max_val = st.number_input(f"最大值", value=config.get("max", 100), key=f"{tab_name}_max_{idx}")
                    if min_val >= max_val:
                        st.error("最大值必须大于最小值！")
                    min_vals.append(min_val)
                    max_vals.append(max_val)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                elif column_type == "小数":
                    min_val = st.number_input(f"最小值", value=config.get("min", 0.0), step=0.01, format="%.2f", key=f"{tab_name}_min_{idx}")
                    max_val = st.number_input(f"最大值", value=config.get("max", 100.0), step=0.01, format="%.2f", key=f"{tab_name}_max_{idx}")
                    if min_val >= max_val:
                        st.error("最大值必须大于最小值！")
                    min_vals.append(min_val)
                    max_vals.append(max_val)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                elif column_type == "自定义":
                    custom_input = st.text_input(
                        f"请输入逗号或顿号分隔的值",
                        config.get("custom_values", ""),
                        key=f"{tab_name}_custom_{idx}",
                    )
                    # 支持中文逗号和顿号分隔符
                    custom_list = [val.strip() for val in custom_input.replace("，", ",").replace("、", ",").split(",") if val.strip()]
                    if not custom_list:
                        st.error("自定义值不能为空！")
                    custom_values.append(custom_list)  # 存储用户输入的自定义值
                    min_vals.append(None)
                    max_vals.append(None)
                    unique_counts.append(None)  # 独特数据数量为空
                elif column_type in ["姓名", "公司", "城市", "国家"]:
                    # 弹出滑动条，允许用户选择独特数据的数量
                    unique_count = st.slider(
                        f"{column_type} 的独特数据数量",
                        min_value=1,
                        max_value=20,
                        value=config.get("unique_count", 5),
                        key=f"{tab_name}_unique_{idx}"
                    )
                    unique_counts.append(unique_count)  # 存储独特数据数量
                    min_vals.append(None)
                    max_vals.append(None)
                    custom_values.append(None)  # 自定义值为空
                elif column_type == "UUID":
                    min_vals.append(None)
                    max_vals.append(None)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                else:
                    min_vals.append(None)
                    max_vals.append(None)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                
                columns.append(col_name)
                column_types.append(column_type)

    return columns, column_types, min_vals, max_vals, custom_values, unique_counts


# 数据生成函数
def generate_data(columns, column_types, min_vals, max_vals, custom_values, unique_counts, num_rows):
    unique_data_cache = {}
    for col_name, col_type, unique_count in zip(columns, column_types, unique_counts):
        if col_type in ["姓名", "公司", "城市", "国家"] and unique_count is not None:
            if col_type == "姓名":
                unique_data_cache[col_name] = [fake.name() for _ in range(unique_count)]
            elif col_type == "公司":
                unique_data_cache[col_name] = [fake.company() for _ in range(unique_count)]
            elif col_type == "城市":
                unique_data_cache[col_name] = [fake.city() for _ in range(unique_count)]
            elif col_type == "国家":
                unique_data_cache[col_name] = [fake.country() for _ in range(unique_count)]

    data = []
    for _ in range(num_rows):
        row = {}
        for col_name, col_type, min_val, max_val, custom_val in zip(columns, column_types, min_vals, max_vals, custom_values):
            if col_type == "列名":
                row[col_name] = f"{col_name}{random.randint(1, 10)}"
            elif col_type == "自定义":
                if custom_val:  # 如果用户输入了自定义值
                    row[col_name] = random.choice(custom_val)
                else:
                    row[col_name] = None  # 如果没有输入值，默认为 None
            elif col_type == "日期":
                row[col_name] = fake.date_this_year().strftime("%Y-%m-%d")  # 生成今年的随机日期
            elif col_type in ["姓名", "公司", "城市", "国家"]:
                row[col_name] = random.choice(unique_data_cache[col_name])  # 从预生成的独特数据中随机抽取
            elif col_type == "整数":
                row[col_name] = fake.random_int(min=min_val, max=max_val)
            elif col_type == "小数":
                row[col_name] = round(random.uniform(min_val, max_val), 2)  # 保留两位小数
            elif col_type == "UUID":
                row[col_name] = str(uuid.uuid4())  # 生成唯一的 UUID
        data.append(row)
    return pd.DataFrame(data)


# 显示数据和下载按钮
def display_and_download(df, tab_name):
    # 创建两列布局：左侧放按钮，右侧放下载按钮
    button_col1, button_col2 = st.columns([1, 1])  # 两个元素平分宽度

    with button_col1:
        st.write("")  # 占位符，保持对齐
    with button_col2:
        # 提供下载链接：导出为Excel
        from io import BytesIO
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Generated Data')
        excel_file.seek(0)
        st.download_button(
            label="下载为Excel",
            data=excel_file,
            file_name=f"{tab_name}_generated_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # 显示生成的数据表格（单独一行）
    st.markdown("---")  # 插入分割线
    st.write("生成的数据：")
    st.dataframe(df, use_container_width=True)  # 数据表格自适应屏幕宽度


# 主逻辑
for tab, tab_name in zip([tab_default, tab_auto, tab_bank, tab_retail, tab_pharma], 
                         ["默认", "汽车", "银行", "零售", "医药"]):
    with tab:
        st.markdown(f"## {tab_name} 数据生成器")

        # 将“生成数据条数”和“生成列数”放在同一行
        col1, col2 = st.columns(2)
        with col1:
            num_rows = st.number_input("选择生成的数据条数", min_value=100, max_value=5000, value=200, step=100, key=f"{tab_name}_num_rows")
        with col2:
            num_columns = st.number_input("选择生成的列数", min_value=1, max_value=20, value=5, step=1, key=f"{tab_name}_num_columns")

        # 在“生成数据条数”和“列配置”之间插入分割线
        st.markdown("---")  # 插入分割线

        # 动态生成列配置
        (
            columns,
            column_types,
            min_vals,
            max_vals,
            custom_values,
            unique_counts,
        ) = generate_column_config(tab_name)

        # 在列配置和数据生成按钮之间插入分割线
        st.markdown("---")  # 插入分割线

        # 按钮点击后生成数据
        if f"{tab_name}_df" not in st.session_state:
            st.session_state[f"{tab_name}_df"] = None  # 初始化 DataFrame 状态

        # 创建两列布局：左侧放按钮，右侧放下载按钮
        button_col1, button_col2 = st.columns([1, 1])  # 两个元素平分宽度

        with button_col1:
            if st.button("生成数据", key=f"{tab_name}_generate"):
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
                    # 生成数据
                    st.session_state[f"{tab_name}_df"] = generate_data(
                        columns, column_types, min_vals, max_vals, custom_values, unique_counts, num_rows
                    )
                    st.toast("数据已生成", icon="🎉")  # 使用 st.toast 显示弹窗提示

        with button_col2:
            if st.session_state[f"{tab_name}_df"] is not None:
                # 提供下载链接：导出为Excel
                from io import BytesIO
                excel_file = BytesIO()
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    st.session_state[f"{tab_name}_df"].to_excel(writer, index=False, sheet_name='Generated Data')
                excel_file.seek(0)
                st.download_button(
                    label="下载为Excel",
                    data=excel_file,
                    file_name=f"{tab_name}_generated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        # 显示生成的数据表格（单独一行）
        if st.session_state[f"{tab_name}_df"] is not None:
            st.markdown("---")  # 插入分割线
            st.write("生成的数据：")
            st.dataframe(st.session_state[f"{tab_name}_df"], use_container_width=True)  # 数据表格自适应屏幕宽度