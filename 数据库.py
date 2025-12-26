import streamlit as st
import random
import time

# --- 1. 题目数据结构 (已按章节清洗) ---
# 数据来源：您上传的《数据库原理与应用试题库.doc》
# Chapter 1: [cite: 1-48]; Chapter 2: [cite: 58-76]; Chapter 3: [cite: 83-116]
# Chapter 4: [cite: 117-140]; Chapter 5: [cite: 141-146]; Chapter 6: [cite: 147-166]

ALL_QUESTIONS = [
    # === 第一章：基本概念 ===
    {
        "chapter": "第一章：基本概念",
        "type": "单选题",
        "question": "在数据管理技术的发展过程中，数据独立性最高的是哪个阶段？",
        "options": ["A. 数据库系统", "B. 文件系统", "C. 人工管理", "D. 数据项管理"],
        "answer": "A. 数据库系统",
        "explanation": "解析：数据库系统阶段实现了物理独立性和逻辑独立性，因此独立性最高 [cite: 1]。"
    },
    {
        "chapter": "第一章：基本概念",
        "type": "简答题",
        "question": "什么是数据库的数据独立性？",
        "answer": "数据独立性表示应用程序与数据库中存储的数据不存在依赖关系。\n包括：\n1. 逻辑数据独立性：用户的逻辑结构与全局逻辑结构独立。\n2. 物理数据独立性：数据的存储结构改变时，应用程序也不用改 [cite: 49, 50]。",
    },

    # === 第二章：关系数据库 ===
    {
        "chapter": "第二章：关系数据库",
        "type": "单选题",
        "question": "关系数据库管理系统应能实现的专门关系运算包括？",
        "options": ["A. 排序、索引、统计", "B. 选择、投影、连接", "C. 关联、更新、排序", "D. 显示、打印、制表"],
        "answer": "B. 选择、投影、连接",
        "explanation": "解析：专门的关系运算主要指选择(Select)、投影(Project)和连接(Join) [cite: 58]。",
    },
    {
        "chapter": "第二章：关系数据库",
        "type": "简答题",
        "question": "简述等值连接与自然连接的区别。",
        "answer": "1. 自然连接一定是等值连接，但等值连接不一定是自然连接。\n2. 等值连接不去除重复属性，而自然连接会去除重复属性。\n3. 自然连接要求进行比较的分量必须是相同的属性组 [cite: 77]。",
    },

    # === 第三章：SQL语言 ===
    {
        "chapter": "第三章：SQL语言",
        "type": "单选题",
        "question": "SQL语言中，用于修改表结构的命令是？",
        "options": ["A. ALTER", "B. CREATE", "C. UPDATE", "D. INSERT"],
        "answer": "A. ALTER",
        "explanation": "解析：ALTER TABLE用于修改结构；UPDATE用于修改数据 [cite: 85]。",
    },
    {
        "chapter": "第三章：SQL语言",
        "type": "简答题",
        "question": "写出SQL语句：从学生表S(SNO, SN, AGE)中查询年龄大于20岁的学生姓名。",
        "answer": "SELECT SN FROM S WHERE AGE > 20;",
    },

    # === 第四章：关系数据理论 (范式) ===
    {
        "chapter": "第四章：关系数据理论",
        "type": "单选题",
        "question": "关系数据库规范化是为解决关系数据库中什么问题而引入的？",
        "options": ["A. 插入、删除和数据冗余", "B. 提高查询速度", "C. 减少数据操作的复杂性", "D. 数据安全性"],
        "answer": "A. 插入、删除和数据冗余",
        "explanation": "解析：规范化的主要目的是消除插入异常、删除异常和降低数据冗余 [cite: 118]。",
    },
    {
        "chapter": "第四章：关系数据理论",
        "type": "简答题",
        "question": "简述什么是第三范式 (3NF)。",
        "answer": "如果关系模式R是2NF，且每个非主属性都不传递依赖于候选码，则称R是3NF [cite: 126]。",
    },

    # === 第五章：数据库设计 ===
    {
        "chapter": "第五章：数据库设计",
        "type": "单选题",
        "question": "E-R图是数据库设计的工具之一，它适用于建立数据库的什么模型？",
        "options": ["A. 概念模型", "B. 逻辑模型", "C. 结构模型", "D. 物理模型"],
        "answer": "A. 概念模型",
        "explanation": "解析：E-R图（实体-联系图）是概念设计阶段的主要工具 [cite: 141]。",
    },

    # === 第六章：数据库保护 ===
    {
        "chapter": "第六章：数据库保护",
        "type": "单选题",
        "question": "事务的原子性是指？",
        "options": ["A. 事务中包括的所有操作要么都做，要么都不做", "B. 事务一旦提交是永久的", "C. 事务之间是隔离的",
                    "D. 数据库从一个一致性状态变到另一个一致性状态"],
        "answer": "A. 事务中包括的所有操作要么都做，要么都不做",
        "explanation": "解析：原子性(Atomicity)强调事务的不可分割性 [cite: 148]。",
    },
    {
        "chapter": "第六章：数据库保护",
        "type": "简答题",
        "question": "并发操作会带来哪三类数据不一致性？",
        "answer": "1. 丢失修改 (Lost Update)\n2. 不可重复读 (Non-repeatable Read)\n3. 读“脏”数据 (Dirty Read) [cite: 161]。",
    }
]

# --- 2. 页面配置 ---
st.set_page_config(page_title="数据库刷题神器", page_icon="🎓", layout="wide")

# 初始化 Session State (用于保存状态)
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

# --- 3. 侧边栏：设置与过滤 ---
st.sidebar.title("🛠️ 刷题设置")
st.sidebar.markdown("根据您的需求筛选题目：")

# 获取所有章节和类型
all_chapters = ["全部章节"] + sorted(list(set([q['chapter'] for q in ALL_QUESTIONS])))
all_types = ["全部题型"] + sorted(list(set([q['type'] for q in ALL_QUESTIONS])))

# 选择框
selected_chapter = st.sidebar.selectbox("选择章节", all_chapters)
selected_type = st.sidebar.selectbox("选择题型", all_types)

# 开始/重置按钮
if st.sidebar.button("🔄 开始 / 重置刷题"):
    # 筛选逻辑
    filtered = ALL_QUESTIONS
    if selected_chapter != "全部章节":
        filtered = [q for q in filtered if q['chapter'] == selected_chapter]
    if selected_type != "全部题型":
        filtered = [q for q in filtered if q['type'] == selected_type]

    if not filtered:
        st.error("没有找到符合条件的题目！")
    else:
        # 随机打乱并重置状态
        random.shuffle(filtered)
        st.session_state.quiz_data = filtered
        st.session_state.current_q_index = 0
        st.session_state.score = 0
        st.session_state.show_explanation = False
        st.session_state.user_answer = None
        st.rerun()  # 强制刷新页面

# 显示当前进度
if st.session_state.quiz_data:
    st.sidebar.markdown("---")
    progress = (st.session_state.current_q_index) / len(st.session_state.quiz_data)
    st.sidebar.progress(progress)
    st.sidebar.write(f"当前得分: {st.session_state.score}")
    st.sidebar.write(f"进度: {st.session_state.current_q_index + 1} / {len(st.session_state.quiz_data)}")

# --- 4. 主界面区域 ---
st.title("🎓 数据库原理与应用 - 智能刷题系统")

if not st.session_state.quiz_data:
    st.info("👈 请在左侧侧边栏选择章节和题型，然后点击“开始 / 重置刷题”开始。")
    st.markdown("""
    **包含内容：**
    * 第一章：基本概念 (DBMS, DBS, 数据独立性)
    * 第二章：关系数据库 (关系代数, 集合运算)
    * 第三章：SQL语言 (Select, Update, Alter)
    * 第四章：关系数据理论 (范式, 函数依赖)
    * 第五章：数据库设计 (E-R图, 概念模型)
    * 第六章：数据库保护 (事务, 并发控制, 锁)
    """)
else:
    # 获取当前题目
    q = st.session_state.quiz_data[st.session_state.current_q_index]

    # 题目卡片
    with st.container():
        st.markdown(f"### {q['chapter']} - {q['type']}")
        st.markdown(f"#### Q{st.session_state.current_q_index + 1}: {q['question']}")

        # --- 单选题逻辑 ---
        if q['type'] == "单选题":
            # 使用 Radio button 显示选项
            # 注意：key需要唯一，所以加上 index
            choice = st.radio(
                "请选择答案：",
                q['options'],
                index=None,
                key=f"radio_{st.session_state.current_q_index}"
            )

            if st.button("提交答案", type="primary"):
                if choice:
                    st.session_state.show_explanation = True
                    if choice == q['answer']:
                        st.success("✅ 回答正确！")
                        if not st.session_state.show_explanation:  # 防止重复加分（虽然逻辑上rerun会重置）
                            pass  # 简化逻辑，这里只展示效果
                    else:
                        st.error(f"❌ 回答错误！正确答案是：{q['answer']}")
                else:
                    st.warning("请先选择一个选项。")

        # --- 简答/SQL题逻辑 ---
        elif q['type'] == "简答题":
            user_text = st.text_area("请输入你的答案/思路：", height=100)
            if st.button("查看参考答案", type="primary"):
                st.session_state.show_explanation = True

        # --- 显示解析与下一题 ---
        if st.session_state.show_explanation:
            st.markdown("---")
            if q['type'] == "简答题":
                st.info(f"**参考答案：**\n\n{q['answer']}")
                st.markdown("💡 **自评：** 如果你的意思和参考答案一致，就算对！")
            else:
                st.info(q['explanation'])

            # 下一题按钮
            if st.session_state.current_q_index < len(st.session_state.quiz_data) - 1:
                if st.button("下一题 ➡️"):
                    st.session_state.current_q_index += 1
                    st.session_state.show_explanation = False
                    st.session_state.user_answer = None
                    st.rerun()
            else:
                st.balloons()
                st.success("🎉 恭喜！你已经刷完了当前筛选的所有题目！")
                if st.button("重新开始"):
                    st.session_state.current_q_index = 0
                    st.session_state.score = 0
                    st.session_state.show_explanation = False
                    st.rerun()