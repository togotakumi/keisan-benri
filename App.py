import streamlit as st
import math
import numpy as np

st.set_page_config(page_title="多機能計算アプリ", page_icon="🧮")
st.title("多機能計算アプリ")

menu = st.sidebar.selectbox(
    "機能を選択",
    ("電卓", "連立方程式(2元)", "三角関数表")
)

# ------------------------------------------------
# 電卓
# ------------------------------------------------
if menu == "電卓":
  st.header("電卓")

# ディスプレイ（式表示）
if "calc_expr" not in st.session_state:
    st.session_state.calc_expr = ""

def set_expr(v):
    st.session_state.calc_expr = v

def add_char(c):
    st.session_state.calc_expr += c

def clear_disp():
    st.session_state.calc_expr = ""

def backspace():
    st.session_state.calc_expr = st.session_state.calc_expr[:-1]

# 上部ディスプレイ
display = st.text_input("式", st.session_state.calc_expr, key="display", label_visibility="collapsed")

# 上段：メモリ系を想定した行（ここでは C, ⌫, (, )）
row_top = st.columns(4)
with row_top[0]:
    if st.button("C"):
        clear_disp()
with row_top[1]:
    if st.button("⌫"):
        backspace()
with row_top[2]:
    if st.button("("):
        add_char("(")
with row_top[3]:
    if st.button(")"):
        add_char(")")

# 2段目：関数系（べき乗・階乗・順列・組合せ）
row_fn = st.columns(4)
with row_fn[0]:
    # x^y → 「**」 に変換して式に入れる
    if st.button("xʸ"):
        add_char("**")
with row_fn[1]:
    # 階乗 n! （math.factorial を使う）
    # 例: 5! としたい時は 5 の後に ! ボタン
    if st.button("n!"):
        add_char("math.factorial(")
with row_fn[2]:
    # 順列 P(n,r)
    if st.button("P"):
        add_char("math.perm(")
with row_fn[3]:
    # 組合せ C(n,r)
    if st.button("C"):
        add_char("math.comb(")

st.caption(
    "例: 5! → 5 n! と押してから ')' を押す／P(5,2) → P → 5,2) のように入力。"
)

# 数字・演算子ボタン（一般的な電卓に近い並び：上から 7 8 9 /, 4 5 6 ×, 1 2 3 -, 0 . = +）
rows = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

for row in rows:
    cols = st.columns(4)
    for i, label in enumerate(row):
        with cols[i]:
            if label == "=":
                if st.button("="):
                    try:
                        expr = st.session_state.calc_expr
                        # eval 用の安全な環境
                        allowed = {
                            "math": math,
                        }
                        result = eval(expr, {"__builtins__": None}, allowed)
                        set_expr(str(result))
                    except Exception as e:
                        st.error(f"エラー: {e}")
            else:
                if st.button(label):
                    add_char(label)

# 下段：三角関数や定数
row_bottom = st.columns(4)
with row_bottom[0]:
    if st.button("sin"):
        add_char("math.sin(")
with row_bottom[1]:
    if st.button("cos"):
        add_char("math.cos(")
with row_bottom[2]:
    if st.button("tan"):
        add_char("math.tan(")
with row_bottom[3]:
    if st.button("π"):
        add_char("math.pi")

st.caption(
    "三角関数はラジアン。角度で計算する場合は (角度*math.pi/180) のように入力してください。"
)

# ------------------------------------------------
# 連立方程式 (2元一次)
# ------------------------------------------------
elif menu == "連立方程式(2元)":
    st.header("連立方程式 (2元一次)")

    st.latex(r"""
\begin{cases}
a_1 x + b_1 y = c_1 \\
a_2 x + b_2 y = c_2
\end{cases}
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        a1 = st.number_input("a1", value=1.0)
        a2 = st.number_input("a2", value=1.0)
    with col2:
        b1 = st.number_input("b1", value=1.0)
        b2 = st.number_input("b2", value=1.0)
    with col3:
        c1 = st.number_input("c1", value=0.0)
        c2 = st.number_input("c2", value=0.0)

    if st.button("解を求める"):
        det = a1 * b2 - a2 * b1
        if det == 0:
            st.error("行列式が 0 のため、解が存在しないか無数にあります。")
        else:
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            st.success(f"x = {x},  y = {y}")


# ------------------------------------------------
# 三角関数表（度数法／弧度法 選択）
# ------------------------------------------------
elif menu == "三角関数表":
    st.header("三角関数表")

    mode = st.radio("角度の指定方法", ("度数法 (deg)", "弧度法 (rad)"))
    input_mode = st.radio("範囲 or 1点", ("範囲指定", "Θを1つ指定"))

    if mode == "度数法 (deg)":
        unit_label = "度"
        default_start = 0.0
        default_end = 90.0
        default_step = 15.0
    else:
        unit_label = "ラジアン"
        default_start = 0.0
        default_end = math.pi / 2
        default_step = math.pi / 12  # 約15°
    
    if input_mode == "範囲指定":
        start = st.number_input(f"開始 ({unit_label})", value=float(default_start))
        end = st.number_input(f"終了 ({unit_label})", value=float(default_end))
        step = st.number_input(f"刻み ({unit_label})", min_value=1e-6, value=float(default_step))
    else:
        theta = st.number_input(f"Θ ({unit_label})", value=float(default_start))
        start = end = theta
        step = 1.0  # ダミー

    if st.button("表を作成"):
        if end < start:
            st.error("終了は開始以上にしてください。")
        else:
            values = []
            current = start
            while current <= end + 1e-12:
                if mode == "度数法 (deg)":
                    theta_deg = current
                    theta_rad = math.radians(theta_deg)
                else:
                    theta_rad = current
                    theta_deg = math.degrees(theta_rad)

                sin_v = math.sin(theta_rad)
                cos_v = math.cos(theta_rad)
                if abs(cos_v) < 1e-10:
                    tan_v = None
                else:
                    tan_v = math.tan(theta_rad)

                values.append(
                    {
                        "θ (deg)": theta_deg,
                        "θ (rad)": theta_rad,
                        "sin θ": sin_v,
                        "cos θ": cos_v,
                        "tan θ": tan_v,
                    }
                )
                if input_mode == "範囲指定":
                    current += step
                else:
                    break

            st.table(values)
            st.caption("tan θ が空欄のところは、値が非常に大きく（発散）していると考えてください。")
