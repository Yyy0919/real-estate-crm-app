import streamlit as st
import json
import os
from datetime import datetime

# 页面基础配置
st.set_page_config(page_title="房产客户购房需求总结与分析系统", layout="wide", page_icon="🏠")

# 引入自定义 CSS 样式（视觉细节优化：圆角、标签颜色、渐变背景）
st.markdown("""
<style>
    /* 核心卡片圆角与边框 */
    .stContainer {
        border-radius: 12px !important;
    }
    /* 自定义彩色标签样式 */
    .tag-strong {
        background-color: #d4edda; color: #155724; padding: 4px 10px; 
        border-radius: 12px; font-weight: bold; font-size: 14px;
    }
    .tag-medium {
        background-color: #ffe8cc; color: #d9480f; padding: 4px 10px; 
        border-radius: 12px; font-weight: bold; font-size: 14px;
    }
    .tag-weak {
        background-color: #e9ecef; color: #495057; padding: 4px 10px; 
        border-radius: 12px; font-weight: bold; font-size: 14px;
    }
    .tag-danger {
        background-color: #ffe3e3; color: #e03131; padding: 3px 8px; 
        border-radius: 6px; font-size: 13px; margin-right: 5px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 数据读取与保存辅助函数
FILE_PATH = "clients.json"

def load_clients():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_client(data):
    clients = load_clients()
    clients.insert(0, data)  # 新记录插入最前
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(clients, f, ensure_ascii=False, indent=4)

# ----------------- 顶层 Tab 架构 -----------------
st.title("🏠 房产客户购房需求总结与分析系统")
tab_main, tab_history = st.tabs(["📝 录入与报告", "📂 历史客户档案库"])

# ==================== Tab 1: 录入与报告 ====================
with tab_main:
    left_col, right_col = st.columns([1, 1.1], gap="medium")
    
    # ------------ 左侧录入区（5个 Tab 分组）------------
    with left_col:
        st.subheader("📋 客户需求表单")
        
        in_tab1, in_tab2, in_tab3, in_tab4, in_tab5 = st.tabs([
            "👤 基础", "🎯 意向", "🏠 房屋", "📍 区位", "⛔ 避雷"
        ])
        
        with in_tab1:
            st.caption("录入客户的基本身份与联系方式")
            name = st.text_input("客户姓名 *", value="张先生")
            phone = st.text_input("联系电话", value="13800138000")
            wechat = st.text_input("微信号", value="wx_demo123")
            age = st.number_input("年龄", min_value=18, max_value=100, value=35)
            job_type = st.radio("职业类型", ["上班族", "经营者/老板", "自由职业/其他"], horizontal=True)
            
        with in_tab2:
            st.caption("明确购房动机与决策紧迫度")
            intent = st.selectbox("购房意向强烈度", ["高（近期必买）", "中（观望对比）", "低（随便看看）"])
            c_a, c_b = st.columns(2)
            with c_a:
                is_first_buy = st.radio("是否刚需", ["是", "否"], horizontal=True)
                is_replacement = st.radio("是否置换（以旧换新）", ["是", "否"], horizontal=True)
            with c_b:
                is_upgrade = st.radio("是否改善", ["是", "否"], horizontal=True)
                
        with in_tab3:
            st.caption("设定房屋硬性指标与预算")
            budget = st.number_input("购房总预算 (万元) *", min_value=0, value=350, step=10)
            layout = st.text_input("户型要求", value="3室2厅2卫")
            area = st.text_input("面积要求", value="90-110㎡")
            floor = st.text_input("楼层要求", value="中高楼层，避开一楼和顶楼")
            accept_foreclosure = st.radio("是否接受法拍房", ["不接受", "接受", "价格合适可考虑"], horizontal=True)
            
        with in_tab4:
            st.caption("地段、学区与周边生活配套")
            location = st.text_input("地段/板块要求", value="核心城区或高新区主干道附近")
            school = st.text_input("学区要求", value="需带优质公办小学/初中学区")
            facilities = st.multiselect(
                "配套要求", 
                ["近地铁", "近大型商圈/超市", "近三甲医院", "近公园", "停车位充裕"],
                default=["近地铁", "近大型商圈/超市"]
            )
            
        with in_tab5:
            st.caption("带看与推荐房源时必须严格避开的因素")
            resisted_factors = st.multiselect(
                "抗拒的不利因素", 
                [
                    "高压线 / 变电站", "垃圾转运站 / 堆放点", "临主干道 / 噪音大", 
                    "靠近墓地 / 殡仪馆", "采光差 / 挡光", "顶层易漏水", 
                    "底楼潮湿", "房龄超过20年老旧小区"
                ],
                default=["高压线 / 变电站", "临主干道 / 噪音大"]
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 生成客户总结报告", type="primary", use_container_width=True)

    # ------------ 右侧报告区（Card + Expander + Tab）------------
    with right_col:
        st.subheader("📊 分析与总结报告")
        
        if generate_btn:
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # 存入 json 数据结构
            record = {
                "created_at": now_str, "name": name, "phone": phone, "wechat": wechat,
                "age": age, "job_type": job_type, "intent": intent, "is_first_buy": is_first_buy,
                "is_upgrade": is_upgrade, "is_replacement": is_replacement, "budget": budget,
                "layout": layout, "area": area, "floor": floor, "accept_foreclosure": accept_foreclosure,
                "location": location, "school": school, "facilities": facilities,
                "resisted_factors": resisted_factors
            }
            save_client(record)
            
            # 1. 摘要 Card（st.container(border=True)）
            with st.container(border=True):
                # 意向标签颜色映射
                if "高" in intent:
                    tag_html = f'<span class="tag-strong">意向：强 🔥</span>'
                elif "中" in intent:
                    tag_html = f'<span class="tag-medium">意向：中 ⚖️</span>'
                else:
                    tag_html = f'<span class="tag-weak">意向：弱 ❄️</span>'
                
                st.markdown(f"### 👤 {name} ({phone}) &nbsp;&nbsp; {tag_html}", unsafe_allow_html=True)
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("购房预算", f"{budget} 万")
                m2.metric("年龄", f"{age} 岁")
                m3.metric("职业类型", job_type)
                m4.metric("客户属性", "刚需" if is_first_buy=="是" else ("改善" if is_upgrade=="是" else "投资/其他"))

            # 生成完整的 Markdown 文本（用于导出）
            full_md = f"""# 📋 房产客户需求档案报告
**建档时间**：{now_str}  

### 一、 客户基础画像
* **姓名/称呼**：{name}（{age}岁） | **职业类型**：{job_type}
* **联系电话**：{phone} | **微信号**：{wechat}
* **购房性质**：{'【刚需】' if is_first_buy=='是' else ''} {'【改善】' if is_upgrade=='是' else ''} {'【以旧换新置换】' if is_replacement=='是' else ''}

### 二、 房屋核心指标
* **总预算**：`{budget} 万元` | **法拍房意向**：{accept_foreclosure}
* **户型/面积**：{layout} | {area} | **楼层偏好**：{floor}

### 三、 地段与配套诉求
* **地段偏好**：{location}
* **学区要求**：{school}
* **核心配套**：{', '.join(facilities) if facilities else '无'}

### 四、 避雷红线
⚠️ **坚决抗拒因素**：{', '.join(resisted_factors) if resisted_factors else '无'}

### 💡 顾问专属带看与匹配策略建议
1. **资金风控**：总预算 {budget} 万，{'需优先确认旧房变现周期；' if is_replacement=='是' else ''}精准匹配首付与按揭区间。
2. **带看红线**：严格过滤包含 `{', '.join(resisted_factors)}` 的不利房源。
3. **推介核心**：围绕 `{location}` 板块，主推绑定 `{school}` 且符合 `{layout}` 的核心房源。
"""

            st.download_button(
                label="📥 导出完整 Markdown 报告",
                data=full_md,
                file_name=f"购房总结_{name}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

            # 2. 右侧 Tab：分栏阅读 vs 完整 Markdown
            view_tab1, view_tab2 = st.tabs(["📖 分栏阅读模式", "📄 完整 Markdown 模式"])
            
            with view_tab1:
                with st.expander("1. 基础信息模块", expanded=True):
                    st.write(f"**微信号**：{wechat} | **电话**：{phone}")
                    st.write(f"**购房类型**：{'刚需 ' if is_first_buy=='是' else ''}{'改善 ' if is_upgrade=='是' else ''}{'置换 ' if is_replacement=='是' else ''}")
                
                with st.expander("2. 意向与动机", expanded=False):
                    st.write(f"**意向强度**：{intent}")
                    st.write(f"**职业**：{job_type}")

                with st.expander("3. 房屋指标模块", expanded=True):
                    st.write(f"**户型/面积**：{layout} | {area}")
                    st.write(f"**楼层**：{floor}")
                    st.write(f"**法拍房**：{accept_foreclosure}")

                with st.expander("4. 区位与配套", expanded=False):
                    st.write(f"**地段**：{location}")
                    st.write(f"**学区**：{school}")
                    st.write(f"**配套**：{', '.join(facilities)}")

                with st.expander("5. 避雷红线（重要）", expanded=True):
                    if resisted_factors:
                        for rf in resisted_factors:
                            st.markdown(f'<span class="tag-danger">⚠️ {rf}</span>', unsafe_allow_html=True)
                    else:
                        st.write("无特殊避雷因素")

                with st.expander("6. 顾问分析与建议", expanded=True):
                    st.info(f"优先推介 **{location}** 板块，预算锁死在 **{budget}万** 内。避开高压线/噪声等不良栋座。")

            with view_tab2:
                with st.container(border=True):
                    st.markdown(full_md)
        else:
            st.info("👈 请在左侧填写信息，点击【生成客户总结报告】查看结果。")

# ==================== Tab 2: 历史客户档案页 ====================
with tab_history:
    st.subheader("📂 历史客户档案库")
    
    clients_data = load_clients()
    
    # 顶部 3 个 Metric 指标
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("累计客户数", f"{len(clients_data)} 人")
    m_col2.metric("最近录入时间", clients_data[0]["created_at"] if clients_data else "暂无")
    m_col3.metric("数据存储文件", "clients.json")
    
    st.divider()
    
    if not clients_data:
        st.warning("目前还没有录入任何客户档案。")
    else:
        for idx, item in enumerate(clients_data):
            # 每条记录用 expander 折叠展示
            expander_title = f"👤 {item.get('name', '未命名')} | 预算: {item.get('budget', 0)}万 | 意向: {item.get('intent', '未知')} | 建档时间: {item.get('created_at', '')}"
            with st.expander(expander_title):
                hc1, hc2 = st.columns(2)
                with hc1:
                    st.write(f"**电话**：{item.get('phone')}")
                    st.write(f"**微信**：{item.get('wechat')}")
                    st.write(f"**需求**：{item.get('layout')} | {item.get('area')} | {item.get('floor')}")
                    st.write(f"**地段**：{item.get('location')}")
                with hc2:
                    st.write(f"**学区**：{item.get('school')}")
                    st.write(f"**避雷**：{', '.join(item.get('resisted_factors', []))}")
                    st.write(f"**配套**：{', '.join(item.get('facilities', []))}")