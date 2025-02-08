import streamlit as st
import pandas as pd
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta

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
tabs = [
    "默认", "汽车", "银行", "医药", "电商", "教育", "医疗健康", "物流与运输", 
    "房地产", "旅游与酒店", "保险行业", "社交媒体", "游戏行业", "金融投资", 
    "农业", "娱乐与影视"
]
tab_objects = st.tabs(tabs)  # 创建标签页对象


# 定义每个标签的默认列配置
default_columns = {
    "默认": [
        {"name": "ID", "type": "UUID"},
        {"name": "姓名", "type": "姓名", "unique_count": 5},
        {"name": "城市", "type": "城市", "unique_count": 5},
        {"name": "注册日期", "type": "日期"},
        {"name": "金额", "type": "小数", "min": 100.0, "max": 10000.0},
    ],
    "汽车": [
        {"name": "车辆ID", "type": "UUID"},
        {"name": "品牌", "type": "枚举", "custom_values": "宝马, 奔驰, 特斯拉"},
        {"name": "车型", "type": "枚举", "custom_values": "轿车, SUV, 跑车"},
        {"name": "生产日期", "type": "日期"},
        {"name": "价格", "type": "小数", "min": 10000.0, "max": 100000.0},
    ],
    "银行": [
        {"name": "账户ID", "type": "UUID"},
        {"name": "客户姓名", "type": "姓名", "unique_count": 5},
        {"name": "账户类型", "type": "枚举", "custom_values": "储蓄账户, 信用卡账户"},
        {"name": "余额", "type": "小数", "min": 0.0, "max": 100000.0},
        {"name": "开户日期", "type": "日期"},
    ],
    "医药": [
        {"name": "药品ID", "type": "UUID"},
        {"name": "药品名称", "type": "枚举", "custom_values": "阿司匹林, 维生素C, 抗生素"},
        {"name": "生产厂家", "type": "公司", "unique_count": 5},
        {"name": "生产日期", "type": "日期"},
        {"name": "有效期", "type": "整数", "min": 1, "max": 36},
    ],
    "电商": [
        {"name": "订单ID", "type": "UUID"},
        {"name": "用户ID", "type": "UUID"},
        {"name": "商品名称", "type": "枚举", "custom_values": "手机, 电脑, 服装"},
        {"name": "商品类别", "type": "枚举", "custom_values": "电子产品, 家居用品, 食品"},
        {"name": "购买数量", "type": "整数", "min": 1, "max": 10},
        {"name": "单价", "type": "小数", "min": 50.0, "max": 1000.0},
        {"name": "总金额", "type": "小数", "min": 50.0, "max": 10000.0},
        {"name": "下单时间", "type": "日期"},
        {"name": "支付状态", "type": "枚举", "custom_values": "已支付, 未支付"},
        {"name": "物流状态", "type": "枚举", "custom_values": "已发货, 运输中, 已签收"},
    ],
    "教育": [
        {"name": "学生ID", "type": "UUID"},
        {"name": "姓名", "type": "姓名", "unique_count": 5},
        {"name": "年龄", "type": "整数", "min": 5, "max": 25},
        {"name": "性别", "type": "枚举", "custom_values": "男, 女"},
        {"name": "班级", "type": "枚举", "custom_values": "一年级, 二年级, 三年级"},
        {"name": "成绩", "type": "小数", "min": 0.0, "max": 100.0},
        {"name": "入学日期", "type": "日期"},
        {"name": "家庭住址", "type": "城市", "unique_count": 5},
        {"name": "联系电话", "type": "列名", "unique_count": 5},
    ],
    "医疗健康": [
        {"name": "患者ID", "type": "UUID"},
        {"name": "姓名", "type": "姓名", "unique_count": 5},
        {"name": "性别", "type": "枚举", "custom_values": "男, 女"},
        {"name": "年龄", "type": "整数", "min": 1, "max": 100},
        {"name": "病历号", "type": "UUID"},
        {"name": "就诊日期", "type": "日期"},
        {"name": "疾病类型", "type": "枚举", "custom_values": "感冒, 高血压, 糖尿病"},
        {"name": "医生姓名", "type": "姓名", "unique_count": 5},
        {"name": "诊断结果", "type": "枚举", "custom_values": "确诊, 疑似, 未确诊"},
        {"name": "药品名称", "type": "枚举", "custom_values": "阿司匹林, 维生素C"},
    ],
    "物流与运输": [
        {"name": "运单ID", "type": "UUID"},
        {"name": "发货人姓名", "type": "姓名", "unique_count": 5},
        {"name": "收货人姓名", "type": "姓名", "unique_count": 5},
        {"name": "发货地址", "type": "城市", "unique_count": 5},
        {"name": "收货地址", "type": "城市", "unique_count": 5},
        {"name": "物品名称", "type": "枚举", "custom_values": "电子产品, 食品, 家具"},
        {"name": "物品重量", "type": "小数", "min": 0.1, "max": 100.0},
        {"name": "运输方式", "type": "枚举", "custom_values": "空运, 陆运, 海运"},
        {"name": "发货日期", "type": "日期"},
        {"name": "预计到达日期", "type": "日期"},
        {"name": "物流状态", "type": "枚举", "custom_values": "已发货, 运输中, 已签收"},
    ],
    "房地产": [
        {"name": "房产ID", "type": "UUID"},
        {"name": "房产类型", "type": "枚举", "custom_values": "公寓, 别墅, 商铺"},
        {"name": "地址", "type": "城市", "unique_count": 5},
        {"name": "面积", "type": "小数", "min": 50.0, "max": 500.0},
        {"name": "房间数量", "type": "整数", "min": 1, "max": 10},
        {"name": "价格", "type": "小数", "min": 500000.0, "max": 10000000.0},
        {"name": "是否出售", "type": "枚举", "custom_values": "是, 否"},
        {"name": "上市日期", "type": "日期"},
        {"name": "房主姓名", "type": "姓名", "unique_count": 5},
        {"name": "联系电话", "type": "列名", "unique_count": 5},
    ],
    "旅游与酒店": [
        {"name": "订单ID", "type": "UUID"},
        {"name": "客户姓名", "type": "姓名", "unique_count": 5},
        {"name": "出行日期", "type": "日期"},
        {"name": "返回日期", "type": "日期"},
        {"name": "目的地", "type": "城市", "unique_count": 5},
        {"name": "酒店名称", "type": "枚举", "custom_values": "希尔顿, 万豪, 如家"},
        {"name": "房型", "type": "枚举", "custom_values": "标准间, 豪华间, 套房"},
        {"name": "价格", "type": "小数", "min": 500.0, "max": 5000.0},
        {"name": "预订状态", "type": "枚举", "custom_values": "已确认, 待确认, 已取消"},
    ],
    "保险行业": [
        {"name": "保单ID", "type": "UUID"},
        {"name": "客户姓名", "type": "姓名", "unique_count": 5},
        {"name": "年龄", "type": "整数", "min": 18, "max": 80},
        {"name": "性别", "type": "枚举", "custom_values": "男, 女"},
        {"name": "保险类型", "type": "枚举", "custom_values": "人寿保险, 车险, 健康险"},
        {"name": "保额", "type": "小数", "min": 100000.0, "max": 10000000.0},
        {"name": "保费", "type": "小数", "min": 1000.0, "max": 50000.0},
        {"name": "投保日期", "type": "日期"},
        {"name": "到期日期", "type": "日期"},
        {"name": "理赔状态", "type": "枚举", "custom_values": "已理赔, 未理赔"},
    ],
    "社交媒体": [
        {"name": "用户ID", "type": "UUID"},
        {"name": "用户名", "type": "姓名", "unique_count": 5},
        {"name": "注册日期", "type": "日期"},
        {"name": "性别", "type": "枚举", "custom_values": "男, 女"},
        {"name": "年龄", "type": "整数", "min": 13, "max": 80},
        {"name": "关注人数", "type": "整数", "min": 0, "max": 10000},
        {"name": "粉丝数量", "type": "整数", "min": 0, "max": 1000000},
        {"name": "发帖数量", "type": "整数", "min": 0, "max": 10000},
        {"name": "最近登录时间", "type": "日期"},
        {"name": "所在城市", "type": "城市", "unique_count": 5},
    ],
    "游戏行业": [
        {"name": "玩家ID", "type": "UUID"},
        {"name": "玩家昵称", "type": "姓名", "unique_count": 5},
        {"name": "注册日期", "type": "日期"},
        {"name": "游戏名称", "type": "枚举", "custom_values": "王者荣耀, 原神, 英雄联盟"},
        {"name": "角色等级", "type": "整数", "min": 1, "max": 100},
        {"name": "在线时长", "type": "小数", "min": 0.0, "max": 1000.0},
        {"name": "充值金额", "type": "小数", "min": 0.0, "max": 10000.0},
        {"name": "最近登录时间", "type": "日期"},
        {"name": "所在地区", "type": "城市", "unique_count": 5},
    ],
    "金融投资": [
        {"name": "投资者ID", "type": "UUID"},
        {"name": "姓名", "type": "姓名", "unique_count": 5},
        {"name": "投资产品", "type": "枚举", "custom_values": "股票, 基金, 债券"},
        {"name": "投资金额", "type": "小数", "min": 1000.0, "max": 1000000.0},
        {"name": "投资日期", "type": "日期"},
        {"name": "当前价值", "type": "小数", "min": 1000.0, "max": 10000000.0},
        {"name": "收益率", "type": "小数", "min": -1.0, "max": 1.0},
        {"name": "风险等级", "type": "枚举", "custom_values": "低风险, 中风险, 高风险"},
        {"name": "投资状态", "type": "枚举", "custom_values": "持有中, 已赎回"},
    ],
    "农业": [
        {"name": "农场ID", "type": "UUID"},
        {"name": "农场名称", "type": "公司", "unique_count": 5},
        {"name": "农产品类型", "type": "枚举", "custom_values": "小麦, 玉米, 水果"},
        {"name": "种植面积", "type": "小数", "min": 10.0, "max": 1000.0},
        {"name": "产量", "type": "小数", "min": 100.0, "max": 10000.0},
        {"name": "销售价格", "type": "小数", "min": 10.0, "max": 500.0},
        {"name": "收获日期", "type": "日期"},
        {"name": "农场地址", "type": "城市", "unique_count": 5},
    ],
    "娱乐与影视": [
        {"name": "电影ID", "type": "UUID"},
        {"name": "电影名称", "type": "枚举", "custom_values": "复仇者联盟, 泰坦尼克号"},
        {"name": "导演姓名", "type": "姓名", "unique_count": 5},
        {"name": "上映日期", "type": "日期"},
        {"name": "类型", "type": "枚举", "custom_values": "动作, 喜剧, 科幻"},
        {"name": "票房收入", "type": "小数", "min": 100000.0, "max": 100000000.0},
        {"name": "观影人数", "type": "整数", "min": 1000, "max": 1000000},
        {"name": "评分", "type": "小数", "min": 0.0, "max": 10.0},
    ],
}

# 动态生成列配置函数
def generate_column_config(tab_name, num_columns):
    columns = []
    column_types = []
    min_vals = []  # 存储最小值
    max_vals = []  # 存储最大值
    custom_values = []  # 存储用户输入的自定义值
    unique_counts = []  # 存储每个列的独特数据数量
    date_ranges = []  # 存储日期范围（开始日期和结束日期）

    # 获取当前标签的默认列配置
    default_config = default_columns.get(tab_name, [])

    # 如果用户选择的列数超过默认配置的数量，则补充默认列配置
    if num_columns > len(default_config):
        for i in range(len(default_config), num_columns):
            default_config.append({
                "name": f"新增列{i+1}",
                "type": "整数",
                "min": 0,
                "max": 100,
            })

    # 动态截取指定数量的列配置
    config_to_display = default_config[:num_columns]

    # 每行显示最多5个列配置
    cols_per_row = 5
    for i in range(0, len(config_to_display), cols_per_row):
        col_config = st.columns(cols_per_row)  # 创建一行最多5列的布局
        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(config_to_display):
                break  # 如果超出列数限制，停止循环
            config = config_to_display[idx]
            col_name = config["name"]
            column_type = config["type"]
            with col_config[j]:  # 在当前列中添加控件
                st.markdown(f"**第 {idx+1} 列配置**")
                col_name = st.text_input(f"列名", col_name, key=f"{tab_name}_col_name_{idx}")
                column_type = st.selectbox(
                    f"数据类型",
                    ["列名", "枚举", "日期", "姓名", "公司", "城市", "国家", "整数", "小数", "UUID"],
                    index=["列名", "枚举", "日期", "姓名", "公司", "城市", "国家", "整数", "小数", "UUID"].index(column_type),
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
                    date_ranges.append((None, None))  # 日期范围为空
                elif column_type == "小数":
                    min_val = st.number_input(f"最小值", value=config.get("min", 0.0), step=0.01, format="%.2f", key=f"{tab_name}_min_{idx}")
                    max_val = st.number_input(f"最大值", value=config.get("max", 100.0), step=0.01, format="%.2f", key=f"{tab_name}_max_{idx}")
                    if min_val >= max_val:
                        st.error("最大值必须大于最小值！")
                    min_vals.append(min_val)
                    max_vals.append(max_val)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                    date_ranges.append((None, None))  # 日期范围为空
                elif column_type == "枚举":
                    custom_input = st.text_input(
                        f"请输入逗号或顿号分隔的值",
                        config.get("custom_values", ""),
                        key=f"{tab_name}_custom_{idx}",
                    )
                    custom_list = [val.strip() for val in custom_input.replace("，", ",").replace("、", ",").split(",") if val.strip()]
                    if not custom_list:
                        st.error("枚举值不能为空！")
                    custom_values.append(custom_list)  # 存储用户输入的自定义值
                    min_vals.append(None)
                    max_vals.append(None)
                    unique_counts.append(None)  # 独特数据数量为空
                    date_ranges.append((None, None))  # 日期范围为空
                elif column_type in ["姓名", "公司", "城市", "国家"]:
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
                    date_ranges.append((None, None))  # 日期范围为空
                elif column_type == "日期":
                    start_date = st.date_input(
                        "开始日期",
                        value=datetime(datetime.now().year, 1, 1),  # 默认为当年1月1日
                        key=f"{tab_name}_start_date_{idx}",
                    )
                    end_date = st.date_input(
                        "结束日期",
                        value=datetime.today(),  # 默认为当天
                        key=f"{tab_name}_end_date_{idx}",
                    )
                    if start_date > end_date:
                        st.error("结束日期必须晚于或等于开始日期！")
                    date_ranges.append((start_date, end_date))  # 存储日期范围
                    min_vals.append(None)
                    max_vals.append(None)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                elif column_type == "列名":
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
                    date_ranges.append((None, None))  # 日期范围为空
                else:
                    min_vals.append(None)
                    max_vals.append(None)
                    custom_values.append(None)  # 自定义值为空
                    unique_counts.append(None)  # 独特数据数量为空
                    date_ranges.append((None, None))  # 日期范围为空
                columns.append(col_name)
                column_types.append(column_type)
        
        # 在每行配置结束后插入分割线
        if i + cols_per_row < len(config_to_display):  # 只有当还有下一行时才插入分割线
            st.markdown("---")  # 插入分割线

    return columns, column_types, min_vals, max_vals, custom_values, unique_counts, date_ranges

# 数据生成函数
def generate_data(columns, column_types, min_vals, max_vals, custom_values, unique_counts, date_ranges, num_rows):
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
        for col_name, col_type, min_val, max_val, custom_val, date_range in zip(
            columns, column_types, min_vals, max_vals, custom_values, date_ranges
        ):
            if col_type == "列名":
                unique_count = unique_counts[columns.index(col_name)]
                unique_data = [f"{col_name}{i}" for i in range(1, unique_count + 1)]
                row[col_name] = random.choice(unique_data)
            elif col_type == "枚举":
                if custom_val:  # 如果用户输入了自定义值
                    row[col_name] = random.choice(custom_val)
                else:
                    row[col_name] = None  # 如果没有输入值，默认为 None
            elif col_type == "日期":
                start_date, end_date = date_range
                if start_date and end_date:
                    random_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
                    row[col_name] = random_date.strftime("%Y-%m-%d")
                else:
                    row[col_name] = None
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
    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        st.write("")
    with button_col2:
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
    st.markdown("---")
    st.write("生成的数据：")
    st.dataframe(df, use_container_width=True)

# 主逻辑
for tab, tab_name in zip(tab_objects, tabs):
    with tab:
        st.markdown(f"## {tab_name} 数据生成器")
        col1, col2 = st.columns(2)
        with col1:
            num_rows = st.number_input("选择生成的数据条数 (500~5000)", min_value=500, max_value=5000, value=1000, step=100, key=f"{tab_name}_num_rows")
        with col2:
            # 动态设置默认列数
            default_num_columns = len(default_columns.get(tab_name, []))
            num_columns = st.number_input("选择生成的列数 (1~20)", min_value=1, max_value=20, value=default_num_columns, step=1, key=f"{tab_name}_num_columns")
        st.markdown("---")
        (
            columns,
            column_types,
            min_vals,
            max_vals,
            custom_values,
            unique_counts,
            date_ranges,
        ) = generate_column_config(tab_name, num_columns)  # 传递 num_columns 参数
        st.markdown("---")
        if f"{tab_name}_df" not in st.session_state:
            st.session_state[f"{tab_name}_df"] = None
        button_col1, button_col2 = st.columns([1, 1])
        with button_col1:
            if st.button("生成数据", key=f"{tab_name}_generate"):
                has_error = False
                for min_val, max_val in zip(min_vals, max_vals):
                    if min_val is not None and max_val is not None and min_val >= max_val:
                        has_error = True
                        break
                for custom_val in custom_values:
                    if custom_val is not None and len(custom_val) == 0:
                        has_error = True
                        break
                for start_date, end_date in date_ranges:
                    if start_date and end_date and start_date > end_date:
                        has_error = True
                        break
                if has_error:
                    st.error("数据验证失败，请检查最小值/最大值或自定义值是否正确！")
                else:
                    st.session_state[f"{tab_name}_df"] = generate_data(
                        columns, column_types, min_vals, max_vals, custom_values, unique_counts, date_ranges, num_rows
                    )
                    st.toast("数据已生成", icon="🎉")
        with button_col2:
            if st.session_state[f"{tab_name}_df"] is not None:
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
        if st.session_state[f"{tab_name}_df"] is not None:
            st.markdown("---")
            st.write("生成的数据：")
            st.dataframe(st.session_state[f"{tab_name}_df"], use_container_width=True)