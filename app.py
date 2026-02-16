
# =========================================================
# ابزار ریاضی هوشمند – نسخه حرفه‌ای کامل
# Developed by Roham Rahimi
# =========================================================

import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import re
import os
from datetime import datetime

# تابع sym (برای ساده‌سازی عبارت‌ها)
def sym(expr):
    try:
        return sp.sympify(expr)
    except:
        raise ValueError("فرمت عبارت نادرست است")

# تابع preprocess (برای تشخیص ضرب ضمنی و اصلاح ورودی)
def preprocess(expr):
    expr = expr.replace(" ", "").replace("^", "**")
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z\d\)])([\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d])', r'\1*\2', expr)
    return expr

# ================= تنظیمات صفحه =================
st.set_page_config(
    page_title="ابزار ریاضی هوشمند",
    page_icon="🧮",
    layout="wide"
)

# بقیه کدت بدون تغییر...

st.markdown("""
<style>
    /* فونت فارسی قوی */
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;900&display=swap');

    /* RTL اجباری برای کل صفحه و همه المان‌ها */
    html, body, .stApp, .stMarkdown, .stText, .stTextInput, .stTextArea, .stButton, .stSelectbox, .stRadio, .stCheckbox, div, p, h1, h2, h3, label, input, textarea {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* اینپوت‌ها و text_area همچنان LTR برای نوشتن انگلیسی/عددی */
    input, textarea {
        direction: ltr !important;
        text-align: left !important;
    }

    /* بک‌گراند تیره (بدون نیاز به عکس خارجی) */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }

    /* عنوان بزرگ و درخشان */
    h1 {
        color: #00f0ff !important;
        text-shadow: 0 0 30px #00f0ff !important;
        font-size: 4.8rem !important;
        text-align: center !important;
        margin: 2rem 0 1rem !important;
    }

    /* زیرعنوان */
    p.subtitle {
        color: #b3e5fc !important;
        text-align: center !important;
        font-size: 1.8rem !important;
        margin-bottom: 3rem !important;
    }

    /* دکمه‌ها */
    button[kind="primary"], .stButton > button {
        background: linear-gradient(135deg, #0288d1, #42a5f5) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 16px 28px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5) !important;
        transition: all 0.4s ease !important;
        width: 100% !important;
        height: 85px !important;
        margin: 10px 0 !important;
    }

    button[kind="primary"]:hover, .stButton > button:hover {
        background: linear-gradient(135deg, #039be5, #0288d1) !important;
        transform: translateY(-6px) !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.6) !important;
    }

    /* فوتر */
    .footer {
        background: rgba(0,0,0,0.8) !important;
        color: #b3e5fc !important;
        padding: 25px !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin: 5rem 1rem 2rem !important;
        font-size: 1.2rem !important;
        border-top: 4px solid #00bfff !important;
    }
</style>
""", unsafe_allow_html=True)
# ================= مدیریت صفحه =================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(p):
    st.session_state.page = p
    st.rerun()

if st.session_state.page == "home":
    st.markdown("<h1>🧮 ابزار ریاضی هوشمند</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>حل مسائل، یادگیری و لذت ریاضی در یکجا</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.button("🔢 حل معادله", use_container_width=True, on_click=go, args=("equation",))
    c2.button("🧮 عملیات عددی", use_container_width=True, on_click=go, args=("integer",))
    c3.button("📘 عبارت‌های جبری", use_container_width=True, on_click=go, args=("algebra",))

    c4, c5, c6 = st.columns(3)
    c4.button("📐 هندسه", use_container_width=True, on_click=go, args=("geometry",))
    c5.button("📊 نمودار آماری", use_container_width=True, on_click=go, args=("stats",))
    c6.button("🔢 اعداد اول", use_container_width=True, on_click=go, args=("prime",))

    c7, c8, c9, c10 = st.columns(4)
    c7.button("📍 مختصات", use_container_width=True, on_click=go, args=("coordinates",))
    c8.button("📚 بانک سوالات", use_container_width=True, on_click=go, args=("bank",))
    c9.button("📖 آموزش علامت‌ها", use_container_width=True, on_click=go, args=("symbols_tutorial",))
    c10.button("💬 نظرات", use_container_width=True, on_click=go, args=("comments",))

    st.button("📝 درسنامه / آموزش", use_container_width=True, on_click=go, args=("tutorial",))


# ================= حل معادله =================
elif st.session_state.page == "equation":
    st.title("🔢 حل معادله")
    eq = st.text_input("معادله:", "x^2-5x+6=0")
    if eq:
        try:
            x = sp.symbols("x")
            if "=" in eq:
                l, r = eq.split("=")
            else:
                l, r = eq, "0"
            expr = sym(preprocess(l)) - sym(preprocess(r))
            sols = sp.solve(expr, x)
            if sols:
                for s in sols:
                    st.latex(sp.latex(s))
            else:
                st.warning("ریشه‌ای ندارد")
        except Exception as e:
            st.error(e)
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================= عملیات عددی =================
elif st.session_state.page == "integer":
    st.title("🧮 عملیات عددی")
    expr = st.text_input("عبارت:")
    if expr:
        try:
            res = sym(preprocess(expr))
            st.latex(sp.latex(res))
        except Exception as e:
            st.error(e)
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================== عبارت‌های جبری ==================
elif st.session_state.page == "algebra":     
    st.title("📘 عبارت‌های جبری")     
    x = sp.symbols('x')     
    expr_input = st.text_input(         
        "عبارت را وارد کنید",         
        placeholder="مثال: 2(x+3)-x   یا   x^2+5x-6   یا   3x(x-2)   یا   (x+1)(x-4)"     
    )     
    substitute = st.text_input(         
        "جایگذاری x (اختیاری)",         
        placeholder="مثال: 5   یا   -2   یا   1/2"     
    )     
    if expr_input and expr_input.strip():         
        try:             
            # پیش‌پردازش ورودی             
            expr = expr_input.replace(" ", "").replace("^", "**")             
            import re             
            expr = re.sub(r'(\d)([a-zA-Z ])', r'\1*\2', expr)             
            # 2x → 2*x    3( → 3*(             
            expr = re.sub(r'([a-zA-Z\d ])([ ])', r'\1*\2', expr)      
            # x( → x*(    5(             
            expr = re.sub(r'( )([a-zA-Z\d])', r'\1*\2', expr)             
            # )x → )*x    )2 → )*2             
            expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)            
            # x2 → x*2             
            # تبدیل به sympy             
            sym_expr = sp.sympify(expr)             
            # ================= اصلاح ترتیب ترم‌ها =================             
            # گسترش کامل             
            expanded = sp.expand(sym_expr)             
            # استخراج ترم‌ها به‌صورت لیست             
            terms = expanded.as_ordered_terms()             
            # مرتب‌سازی دستی: درجه نزولی x             
            def term_degree(t):                 
                if x in t.free_symbols:                     
                    return sp.degree(t, x)                 
                return 0             
            terms_sorted = sorted(terms, key=term_degree, reverse=True)             
            # جمع دوباره ترم‌ها             
            simplified = sum(terms_sorted)             
            # =====================================================             
            # نمایش نتیجه             
            st.markdown("**عبارت ساده‌شده (نمایش ریاضی):**")             
            st.latex(sp.latex(simplified))             
            st.markdown("**عبارت ساده‌شده (متن ساده - قابل کپی):**")             
            text_version = str(simplified).replace("**", "^").replace("*", "")             
            st.code(text_version, language=None)             
            # فاکتورگیری             
            try:                 
                factored = sp.factor(sym_expr)                 
                if str(factored) != str(simplified):                     
                    st.markdown("**فاکتور شده (ریاضی):**")                     
                    st.latex(sp.latex(factored))                     
                    st.markdown("**فاکتور شده (متن):**")                     
                    st.code(str(factored).replace("**", "^").replace("*", ""), language=None)             
            except:                 
                pass             
            # جایگذاری             
            if substitute and substitute.strip():                 
                try:                     
                    val = sp.sympify(substitute)                     
                    result = simplified.subs(x, val)                     
                    result = sp.simplify(result)                     
                    st.markdown("**نتیجه جایگذاری (ریاضی):**")                     
                    st.latex(sp.latex(result))                     
                    st.markdown("**نتیجه جایگذاری (متن):**")                     
                    st.code(str(result), language=None)                 
                except Exception as ve:                     
                    st.warning(f"مشکل جایگذاری: {str(ve)}")         
        except Exception as e:             
            st.error(                 
                f"خطا در پردازش عبارت:\n\n{str(e)}\n\n"                 
                "**مثال‌های درست:**\n"                 
                "• 2(x+3)-x\n"                 
                "• x^2 + 5x - 6\n"                 
                "• 3x(x-2)\n"                 
                "• (x+1)(x-4)\n"                 
                "• 2x(x+3)-x^2\n"                 
                "• x(x+1)(x-1)\n\n"                 
                "نکته: توان را با ^ یا ** بنویسید"             
            )     
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================= هندسه =================
elif st.session_state.page == "geometry":
    st.title("📐 هندسه")
    st.button("🔺 مثلث", on_click=go, args=("triangle",))
    st.button("📦 حجم و مساحت منشورها", on_click=go, args=("volume",))
    st.button("🔄 تبدیل هندسی", on_click=go, args=("transform",))
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

elif st.session_state.page == "triangle":
    st.title("🔺 زاویه مجهول مثلث")
    a = st.text_input("A")
    b = st.text_input("B")
    c = st.text_input("C")
    arr = [a, b, c]
    if all(arr):
        try:
            known = [float(x) for x in arr if x.lower() != "x"]
            if arr.count("x") != 1:
                st.error("دقیقاً یکی باید x باشد")
            else:
                res = 180 - sum(known)
                st.success(f"زاویه = {res}")
        except:
            st.error("ورودی نامعتبر")
    st.button("⬅️ بازگشت", on_click=go, args=("geometry",))

elif st.session_state.page == "volume":
    st.title("📦 حجم و مساحت منشور")
    l = st.number_input("طول")
    w = st.number_input("عرض")
    h = st.number_input("ارتفاع")
    st.success(f"حجم = {l*w*h}")
    st.success(f"مساحت = {2*(l*w+l*h+w*h)}")
    st.button("⬅️ بازگشت", on_click=go, args=("geometry",))

elif st.session_state.page == "transform":
    st.title("🔄 تبدیل هندسی")
    x = st.number_input("x")
    y = st.number_input("y")
    dx = st.number_input("dx")
    dy = st.number_input("dy")
    st.success(f"مختصات جدید: ({x+dx},{y+dy})")
    st.button("⬅️ بازگشت", on_click=go, args=("geometry",))

# ================= نمودار آماری =================
elif st.session_state.page == "stats":
    st.title("📊 نمودار آماری")
    raw = st.text_input("اعداد:", "2,4,6,3")
    if raw:
        try:
            data = [float(i) for i in raw.split(",")]
            fig, ax = plt.subplots()
            ax.bar(range(len(data)), data)
            ax.set_title("chart")
            st.pyplot(fig)
        except:
            st.error("فرمت نادرست")
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================= اعداد اول =================
elif st.session_state.page == "prime":
    st.title("🔢 عدد اول")
    n = st.number_input("عدد:", step=1, min_value=0)
    if n >= 2:
        f = sp.factorint(int(n))
        if len(f) == 1 and list(f.values())[0] == 1:
            st.success("عدد اول است")
        else:
            st.warning("اول نیست")
            st.write(f)
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================= مختصات =================
elif st.session_state.page == "coordinates":
    st.title("📍 مختصات")
    x = st.number_input("x")
    y = st.number_input("y")
    if x > 0 and y > 0:
        st.success("ربع اول")
    elif x < 0 and y > 0:
        st.success("ربع دوم")
    elif x < 0 and y < 0:
        st.success("ربع سوم")
    elif x > 0 and y < 0:
        st.success("ربع چهارم")
    else:
        st.info("روی محور")
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================= بانک سوالات =================
elif st.session_state.page == "bank":
    st.title("📚 بانک سوالات")
    st.markdown("[TIMSS پایه چهارم](https://tizline.ir/portal/wp-content/uploads/2021/02/Tizline-daftarche-timss-4.pdf)")
    st.markdown("[TIMSS پایه هشتم](https://tizline.ir/portal/wp-content/uploads/2021/02/Tizline-daftarche-timss-8.pdf)")
    st.markdown("[پایش ریاضی هفتم مرحل اول 1403-1404](https://tizline.ir/portal/wp-content/uploads/2021/12/%D9%BE%D8%A7%DB%8C%D8%B4-%D8%B3%D8%A7%D9%84-%D9%87%D9%81%D8%AA%D9%85-%D9%BE%D8%A7%D8%B3%D8%AE-%DA%A9%D9%84%DB%8C%D8%AF%DB%8C-1403-.pdf)")
    st.markdown("[پایش ریاضی هفتم مرحل اول 1402-1403](https://tizline.ir/portal/wp-content/uploads/2021/12/%D9%BE%D8%A7%DB%8C%D8%B4-%D8%B3%D8%A7%D9%84-%D9%87%D9%81%D8%AA%D9%85-%D9%BE%D8%A7%D8%B3%D8%AE-%D8%AA%D8%B4%D8%B1%DB%8C%D8%AD%DB%8C.pdf)")
    st.markdown("[پایش ریاضی هفتم مرحل اول 1401-1402](https://tizline.ir/portal/wp-content/uploads/2021/12/%D8%B3%D9%88%D8%A7%D9%84%D8%A7%D8%AA-%D9%88-%D9%BE%D8%A7%D8%B3%D8%AE%D9%86%D8%A7%D9%85%D9%87-%D9%BE%D8%A7%DB%8C%D8%B4-%D8%B3%D9%85%D9%BE%D8%A7%D8%AF-%D9%87%D9%81%D8%AA%D9%85-%D9%85%D8%B1%D8%AD%D9%84%D9%87-%D8%A7%D9%88%D9%84-%DB%B1%DB%B4%DB%B0%DB%B1-.pdf)")
    st.markdown("[پایش ریاضی هفتم مرحل اول 1400-1401](https://tizline.ir/portal/wp-content/uploads/2021/12/%D9%85%D8%B1%D8%AD%D9%84%D9%87-%D8%A7%D9%88%D9%84-%D8%A2%D8%B2%D9%85%D9%88%D9%86-%D9%BE%D8%A7%DB%8C%D8%B4-%D9%BE%D8%A7%DB%8C%D9%87-%D9%87%D9%81%D8%AA%D9%85-%DB%B1%DB%B4%DB%B0%DB%B0-%D8%A8%D8%A7-%D9%BE%D8%A7%D8%B3%D8%AE%D9%86%D8%A7%D9%85%D9%87.pdf)")

    st.markdown("تمام آزمون ها و نمونه سوالات از سایت تیزلاین فقط برای هدف آموزشی برداشته شده است و فاقد هرگونه کپی رایت می باشد.")
    st.markdown("[سایت آموزشی تیزلاین](https://tizline.ir)")
    st.button("⬅️ بازگشت", on_click=go, args=("home",))
# ================= درسنامه =================
elif st.session_state.page == "tutorial":
    st.title("📝 درسنامه")
    st.markdown("""
ریاضی هفتم  :point_down::point_down:

🔴فصل اول-درس راهبرد الگویابی
https://kandoo.medu.ir/v/NUmjcsgd2f4tb

درس الگو سازی.حذف حالتهای نامطلوب
 https://kandoo.medu.ir/v/NUmjcsr6mw1xt

درس راهبردهای زیر مسئله
https://kandoo.medu.ir/v/NUmjct30ba3z

درس راهبردهای حل مسئله
https://kandoo.medu.ir/v/NUmjctcdc41kv

درس راهبردهای حل مسئله روشهای نمادین
 https://kandoo.medu.ir/v/NUmjctkdyw1y2
                
---
                
:red_circle:  ریاضی هفتم فصل دوم -نمونه 1
                
عددهای صحیح

درس اول (معرفی عددهای علامت دار)
https://kandoo.medu.ir/v/NUmjhla9i35gl

درس دوم(جمع و تفریق  عددهای صحیح)
https://kandoo.medu.ir/v/NUmjhlmsj4yv

درس سوم(تفریق عددهای صحیح)
https://kandoo.medu.ir/v/NUmjhm4dnv68w

درس چهارم(ضرب و تقسیم  اعداد صحیح)
https://kandoo.medu.ir/v/NUmjhn5ulf3a
                
---
                
:red_circle: ریاضی هفتم فصل دوم-نمونه 2
عددهای صحیح
                

درس اول (معرفی عددهای علامت دار)
 https://kandoo.medu.ir/v/NUmk4ce3g04l4  

درس دوم(جمع عددهای صحیح)
https://kandoo.medu.ir/v/NUmk4cl9572lp

درس سوم (تفریق عددهای صحیح)
https://kandoo.medu.ir/v/NUmk4ct25547h

درس چهارم-بخش اول(ضرب اعداد صحیح)
https://kandoo.medu.ir/v/NUmk4d1gs22pd
                
---
                
:red_circle: ریاضی هفتم فصل سوم (جبر و معادله)
                

درس اول(الگوهای عددی)

https://kandoo.medu.ir/v/NUmji5kqh231k

درس دوم(عبارت های جبری)

https://kandoo.medu.ir/v/NUmji66jbd1hu
                
درس سوم(مقدار عددی یک عبارت جبری)

https://kandoo.medu.ir/v/NUmji6nvn6462

درس چهارم(معادله)

https://kandoo.medu.ir/v/NUmji74eok6d2
                
---
                
:red_circle:  ریاضی هفتم فصل چهارم (هندسه و استدلال)
                
درس اول(روابط بین پاره خط ها)

https://kandoo.medu.ir/v/NUmj9wwtf61f7

درس دوم(روابط بین زاویه ها)

https://kandoo.medu.ir/v/NUmj9y7vsq4v6

درس سوم(تبدیلات هندسی)

https://kandoo.medu.ir/v/NUmja20s7j131

درس چهارم(شکل های همنهشت)

https://kandoo.medu.ir/v/NUmja2gox15t0
                
---
                
:red_circle: ریاضی هفتم  فصل پنجم(شمارنده ها و اعداد اول)
درس اول (عدد اول)

https://kandoo.medu.ir/v/NUmj9tirgs2n2

درس دوم(شمارنده اول)

https://kandoo.medu.ir/v/NUmj9v8pn35he

درس سوم(بزرگ تمرین شمارنده مشترک)

https://kandoo.medu.ir/v/NUmj9vuhra5i2

درس چهارم(کوچکترین مضرب مشترک)

https://kandoo.medu.ir/v/NUmj9w5guk5e

---
                
🔴ریاضی هفتم فصل ششم(سطح و حجم)

-درس اول(حجم های هندسی)
https://kandoo.medu.ir/v/NUmkk4fhr25dd

-درس دوم(محاسبه حجم های منشوری)
https://kandoo.medu.ir/v/NUmkk4t4et5dd

-درس سوم(مساحت جانبی و کل)
https://kandoo.medu.ir/v/NUmkk59pgq18l

-درس چهارم(حجم و سطح)
https://kandoo.medu.ir/v/NUmkk5mea32nx
                
---
                
:red_circle: ریاضی هفتم فصل هفتم(توان و جذر)
                
درس اول و دوم(تعریف توان و محاسبه تعداد توان دار)
 https://kandoo.medu.ir/v/NUmk5qwnlw5a3


درس سوم(ساده کردن عبارت های توان دار)
https://kandoo.medu.ir/v/NUmk5r5ca421x

درس چهارم(جذر و ریشه)
https://kandoo.medu.ir/v/NUmk5ri1t2uc
                
---
                
:red_circle: ریاضی هفتم فصل هشتم(بردار و مختصات)

-درس اول(پاره خط جهت دار)
https://kandoo.medu.ir/v/NUmkk5uth8jf

-درس دوم(برادرهای مساوی و قرینه)
https://kandoo.medu.ir/v/NUmkk5z6nzef

-درس سوم(مختصات)
https://kandoo.medu.ir/v/NUmkk6kujm2ie

-درس چهارم(بردار انتقال)
https://kandoo.medu.ir/v/NUmkk6402g4zc

-درس پنجم(بردار انتقال)
https://kandoo.medu.ir/v/NUmkk6cvuc1ok
                
---
                
:red_circle: ریاضی هفتم فصل نهم(آمار و احتمال)

درس اول (جمع آوری و نمایش داده ها)
 https://kandoo.medu.ir/v/NUmk32ojba2fn

درس دوم(نمودارها و تفسیر نتیجه ها)
https://kandoo.medu.ir/v/NUmk334tqp4ap
                
درس سوم(احتمال یا اندازه گیری شانس)
https://kandoo.medu.ir/v/NUmkmf37up4cc

درس چهارم(احتمال و تجربه)
https://kandoo.medu.ir/v/NUmkmg0z1d4lw


  
    """)
    st.button("⬅️ بازگشت", on_click=go, args=("home",))
# ================== آموزش علامت‌ها ==================
elif st.session_state.page == "symbols_tutorial":
    st.title("📖 آموزش علامت‌ها")
    st.markdown("""
    (+) : جمع
    ---
    (-) : تفریق
    ---
    (*) : ضرب
    ---
    (/) : تقسیم
    ---
    (**) : توان
    ---
    """)
    st.button("⬅️ بازگشت", on_click=go, args=("home",))

# ================== نظرات ==================
elif st.session_state.page == "comments":
    st.title("💬 نظرات و پیشنهادات")

    # فایل ذخیره نظرات
    COMMENTS_FILE = "comments.txt"

    # لیست کلمات ممنوعه (فحش‌های رایج فارسی + تغییرات املایی)
    forbidden_words = [
        "کیر", "کص", "کوس", "کس", "جنده", "کون", "گاییدن", "گوه", "کونی", "مادرجنده", "کصکش",
        "کیرم", "کیرتو", "کسشر", "کصننه", "کیرم تو", "گاییدم", "کون گشاد", "کیرکلفت", "کس ننه",
        "کون ننه", "کیر گنده", "کص گشاد", "جق", "جق زدن", "ارگاسم", "پورن", "سکس", "سکسی",
        "کیرخر", "کصخر", "کیرم تو کون", "کسم تو دهنت", "کونت گشاد", "مادرتو گاییدم",
        "کیر تو کون", "کس تو دهن", "جنده مادر", "کونی مادر", "کسکش مادر",
        # تغییرات املایی رایج
        "kyr", "kos", "kon", "jende", "koni", "madarjende", "kaskesh", "kir", "kossher",
        "ک.س", "ک.یر", "ج.نده", "ک.ون", "گ.وه", "م.ادرجنده"
    ]

    # نمایش نظرات قبلی (برای همه کاربران)
    st.markdown("**نظرات کاربران:**")
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                st.text(content)
            else:
                st.info("هنوز هیچ نظری ثبت نشده است.")
    else:
        st.info("هنوز هیچ نظری ثبت نشده است.")

    # فرم نوشتن نظر جدید
    name = st.text_input("نام (اختیاری):", value="ناشناس")
    new_comment = st.text_area("نظر خود را بنویسید:", height=120)

    if st.button("ارسال نظر"):
        if new_comment.strip():
            # چک کردن کلمات ممنوعه
            lower_comment = new_comment.lower()
            bad_word_found = any(word in lower_comment for word in forbidden_words)

            if bad_word_found:
                st.error("⚠️ فحاشی، کلمات رکیک و توهین‌آمیز ممنوع است!\nلطفاً نظر مودبانه و سازنده بنویسید.")
            else:
                # زمان فعلی
                now = datetime.now().strftime("%Y-%m-%d   %H:%M:%S")

                # ذخیره نظر در فایل
                with open(COMMENTS_FILE, "a", encoding="utf-8") as f:
                    f.write(f"[{now}]   {name.strip() or 'ناشناس'} :\n{new_comment.strip()}\n{'─'*70}\n\n")

                st.success("نظر شما با موفقیت ثبت شد! ممنون از فیدبکت 🌟")
                st.rerun()  # صفحه رو رفرش کن تا نظر جدید نمایش داده بشه
        else:
            st.warning("لطفاً نظر خود را بنویسید!")

    st.button("⬅️ بازگشت", on_click=go, args=("home",))
st.markdown("""
<div class='footer'>
    © Roham Rahimi | نسخه ۱.۱ | به‌روزرسانی هفتگی | پلن رایگان
</div>
""", unsafe_allow_html=True)