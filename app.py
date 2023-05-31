import calendar #Core Python Module
from datetime import datetime #Core Python Module

import streamlit as st #pip install streamlit
import plotly.graph_objects as go #pipt install plotly
from streamlit_option_menu import option_menu #pip install streamlit-option-menu

# Tutorial
# Corey Yang-Smith
# May 31 2023
# https://www.youtube.com/watch?v=3egaMfE9388

# ---------- SETTINGS ---------- #
# TODO Selectable currency as well
incomes = ["Salary", "Other"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Savings"]
currency = "CAD"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:" #https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered" #alternative: wide
# -----------########----------- #

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"], # https://icons.getbootstrap.com
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
if selected == "Data Entry":
    st.header(f"Date Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")

        "---"

        # TODO Add a way to manually enter the income and expenses cateogory, and have it dynamically generate on the page
        # TODO Add definable Sub Categories as well
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here ...")

        "---"

        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses} 
            # TODO: Insert values into database
            st.write(f"incomes: {incomes}")
            st.write(f"expenses: {expenses}")       
            st.success("Data saved!")

# ---------- PLOT PERIODS ----------
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        # TODO: get periods from database
        period = st.selectbox("Select Period:",["2022_March"])
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            #TODO: Get data from database
            comment = "Some comment"
            incomes = {'Salary': 10, 'Other': 0}
            expenses = {'Rent': 0, 'Utilities': 20, 'Groceries': 0, 'Car': 0, 'Other Expenses': 0, 'Savings': 0}

            #Create Metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")

            # Create Sankey Chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)

