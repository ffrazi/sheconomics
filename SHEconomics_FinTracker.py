import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# ---- SESSION STATE INITIALIZATION ----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users" not in st.session_state:
    st.session_state.users = {"admin": "password"}  # Default user
if "salary" not in st.session_state:
    st.session_state.salary = 0
if "savings_target" not in st.session_state:
    st.session_state.savings_target = 0
if "total_expenses" not in st.session_state:
    st.session_state.total_expenses = 0.0
if "expenses_list" not in st.session_state:
    st.session_state.expenses_list = []
if "page" not in st.session_state:
    st.session_state.page = "home"  # Set default page

# ---- HOME PAGE FUNCTION ----
def home_page():
    st.title("💰 SHEconomics FinTracker ")
    st.markdown("""
    **Welcome to your personal finance manager!**  
    Track your income, expenses, investments, and more all in one place.  
    SHEconomics FinTracker is here to help you plan and grow your financial future.  
    """)

    if st.button("Login to Access Your Dashboard"):
        st.session_state.page = "login"
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.users = {"admin": "password"}  # Default user

# ---- LOGIN & SIGNUP FUNCTION ----
def login_page():
    st.title("🔐 Login Page")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = "dashboard"
        else:
            st.error("❌ Invalid credentials. Try again!")

    st.markdown("---")
    st.subheader("Don't have an account? Sign Up Below")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        if new_user and new_pass:
            if new_user in st.session_state.users:
                st.error("⚠️ Username already exists. Choose a different one.")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("🎉 Account created! You can now log in.")
        else:
            st.warning("⚠️ Please enter a valid username and password.")

# ---- MAIN DASHBOARD FUNCTION ----
def main_dashboard():
    st.sidebar.title(f"🔍 Welcome, {st.session_state.username}!")
    menu = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Expense Tracker", "Investment Tracker", "EMI Calculator", "SIP Calculator", "Learning corner", "Quizdom", "🚪 Logout"])

    if menu == "🏠 Home":
        st.title("💰 SHEconomics FinTracker ")
        st.markdown("""
        **Welcome to SHEconomics FinTracker! Your Personal Finance Powerhouse!** 💰✨  

Ladies, it's time to take control of your financial future with confidence! SheWealth is an exclusive financial empowerment platform designed **by women, for women** – because your financial journey deserves a path of its own. From **budgeting and expense tracking** to **smart investments and savings goals**, we provide the tools you need to build wealth, secure your future, and achieve financial independence.  

Whether you're planning your first investment, managing everyday expenses, or setting long-term financial goals, SHEconomics FinTracker is here to guide you with **personalized insights, easy-to-use tools, and expert financial tips** – all tailored for **your unique financial needs**. 💼🌸  

**Because when women take charge of their finances, they take charge of everything!** 🚀💖""")
    
    elif menu == "📊 Expense Tracker":
        expense_tracker()
    elif menu == "Investment Tracker":
        investment_tracker()
    elif menu == "EMI Calculator":
        emi_calculator()
    elif menu == "SIP Calculator":
        sip_calculator()
    elif menu == "Learning corner":
        learning_corner()
    elif menu == "Quizdom":
        quiz_corner()
    elif menu == "🚪 Logout":
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.page = "home"

# ---- EXPENSE TRACKER FUNCTION ----
def expense_tracker():
    st.title("📊 Expense Tracker & Budgeting")

    # Salary & Savings Target
    st.subheader("💼 Set Your Salary & Savings Goal")
    col1, col2 = st.columns(2)

    with col1:
        salary = st.number_input("Enter Your Salary (₹)", min_value=0, value=st.session_state.salary, step=1000)
    with col2:
        savings_target = st.number_input("Enter Your Savings Target (₹)", min_value=0, value=st.session_state.savings_target, step=500)

    if st.button("Save Details"):
        st.session_state.salary = salary
        st.session_state.savings_target = savings_target
        st.success(f"Salary: ₹{salary} and Savings Target: ₹{savings_target} saved!")

    st.divider()

    # Expense Entry
    st.subheader("📋 Add Your Expenses")
    expense = st.number_input("Enter Expense Amount (₹):", min_value=0.0, format="%.2f")
    category = st.selectbox("Select Expense Category", ["Food", "Shopping", "Bills", "Investment", "Others"])

    if st.button("Add Expense"):
        st.session_state.expenses_list.append({"Category": category, "Amount": expense})
        st.session_state.total_expenses += expense
        st.success(f"Added ₹{expense} under {category}")

    # Display Expense History
    if st.session_state.expenses_list:
        st.subheader("📜 Expense History")
        df = pd.DataFrame(st.session_state.expenses_list)
        st.table(df)

    st.markdown(f"### 🏷️ Total Expenses (from tracker): ₹{st.session_state.total_expenses:.2f}")

    st.divider()

    # Budget Planning
    st.subheader("📉 Budget Planning")
    income = st.number_input("Enter Your Monthly Income (₹)", min_value=0, value=st.session_state.salary, step=1000)

    st.markdown("### 📝 Add Your Budgeted Expenses")
    expense_categories = ["Rent", "Groceries", "Utilities", "Transportation", "Entertainment", "Others"]
    budgeted_expenses = {}

    for category in expense_categories:
        budgeted_expenses[category] = st.number_input(f"Enter {category} Expenses (₹)", min_value=0, value=0, step=100)

    # Calculate total expenses including tracker + budgeted ones
    total_expenses = st.session_state.total_expenses + sum(budgeted_expenses.values())
    balance = income - total_expenses

    st.divider()

    # Financial Summary
    st.subheader("📊 Financial Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Income", f"₹{income}")
    col2.metric("📉 Total Expenses", f"₹{total_expenses:.2f}")
    col3.metric("💵 Balance", f"₹{balance:.2f}")

    if balance < 0:
        st.warning("⚠️ You are exceeding your budget! Consider reducing expenses.")
    elif balance < st.session_state.savings_target:
        st.info(f"You're within budget, but haven't reached your savings target of ₹{st.session_state.savings_target}. Try saving more!")
    else:
        st.success("🎉 You are within your budget and reaching your savings target! Great job!")

    st.divider()

    # Financial Tips
    st.subheader("💡 Financial Tips")
    st.markdown("""
### **1️⃣ Pay Yourself First 💰**  
Before spending, **save at least 20%** of your income. Treat savings as a non-negotiable expense.  

### **2️⃣ Build an Emergency Fund 🚨**  
Life is unpredictable! Aim for **3–6 months of living expenses** in a separate account to handle unexpected financial shocks.  

### **3️⃣ Take Charge of Investments 📈**  
Don’t just save—**invest!** Explore **mutual funds, stocks, bonds, and real estate** to make your money grow over time.  

### **4️⃣ Say No to Financial Dependence 🚫**  
Never rely **solely on a partner or family** for financial security. Always have a **personal income source and independent savings**.  

### **5️⃣ Budget Like a Boss 📝**  
Track expenses and stick to a **50/30/20 rule** (50% needs, 30% wants, 20% savings/investments) to balance spending and savings.  

### **6️⃣ Prioritize Retirement Savings 🏡**  
Start investing in retirement plans like **PPF, NPS, or SIPs** early to secure a stress-free future. The earlier you start, the more you gain!  

### **7️⃣ Protect Yourself with Insurance 🛡️**  
Health and financial security go hand in hand. Get **health insurance, life insurance, and critical illness coverage** to safeguard your future.  

### **8️⃣ Never Ignore Credit Scores 💳**  
A good **credit score** (750+) helps you get loans at **lower interest rates**. Pay credit card bills on time and avoid unnecessary debt.  

### **9️⃣ Negotiate Your Salary 💼**  
Women often **undervalue** their work. Research market standards and confidently negotiate for **equal pay** and better benefits.  

### **🔟 Build Multiple Income Streams 💡**  
Apart from a 9-to-5 job, consider **freelancing, consulting, side hustles, or passive income sources** to increase financial stability.  

💡 **Final Tip:** Knowledge is power! Keep learning about personal finance and **make your money work for you**. **SHEconomics FinTracker** is here to help! 🚀💖  
""")


# -------- Investment Tracker --------
def investment_tracker():
    st.title("Investment Tracker")
    
    # Initialize session state for storing investments
    if 'investments' not in st.session_state:
        st.session_state['investments'] = []
    
    # User input fields
    st.subheader("Add a New Investment")
    investment_name = st.text_input("Investment Name")
    amount = st.number_input("Amount Invested ($)", min_value=0.0, format="%.2f")
    date = st.date_input("Investment Date", datetime.today())
    category = st.selectbox("Investment Category", ["Stocks", "Bonds", "Crypto", "Real Estate", "Others"])
    
    if st.button("Add Investment"):
        if investment_name and amount > 0:
            st.session_state['investments'].append({
                "Name": investment_name,
                "Amount": amount,
                "Date": date.strftime('%Y-%m-%d'),
                "Category": category
            })
            st.success("Investment added successfully!")
        else:
            st.error("Please enter valid details.")
    
    # Display investments
    if st.session_state['investments']:
        st.subheader("Investment Portfolio")
        df = pd.DataFrame(st.session_state['investments'])
        st.dataframe(df)
        
        # Calculate total investment
        total_invested = df["Amount"].sum()
        st.write(f"**Total Invested: ${total_invested:.2f}**")
    else:
        st.info("No investments added yet.")

# -------- EMI Calculator --------
def emi_calculator():
    st.title("EMI Calculator")
    st.subheader("Calculate Your Monthly EMI")

    loan_amount = st.number_input("Enter Loan Amount (₹)", min_value=0.0, format="%.2f")
    interest_rate = st.number_input("Enter Annual Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    loan_term = st.number_input("Enter Loan Term (years)", min_value=1, max_value=30, step=1)

    if st.button("Calculate EMI"):
        rate_of_interest = interest_rate / (12 * 100)
        number_of_months = loan_term * 12
        emi = loan_amount * rate_of_interest * ((1 + rate_of_interest) ** number_of_months) / (((1 + rate_of_interest) ** number_of_months) - 1)

        st.write(f"Your monthly EMI is: ₹{emi:.2f}")

# -------- SIP Calculator --------
def sip_calculator():
    st.title("SIP Calculator")
    st.subheader("Calculate Your Monthly SIP Investment")

    monthly_investment = st.number_input("Enter Monthly SIP Amount (₹)", min_value=0.0, format="%.2f")
    rate_of_return = st.number_input("Expected Annual Return (%)", min_value=0.0, max_value=100.0, step=0.1)
    investment_period = st.number_input("Enter Investment Period (years)", min_value=1, max_value=30, step=1)

    if st.button("Calculate SIP Returns"):
        rate_of_return = rate_of_return / 100
        months = investment_period * 12
        future_value = monthly_investment * (((1 + rate_of_return / 12) ** months - 1) / (rate_of_return / 12)) * (1 + rate_of_return / 12)

        st.write(f"Your SIP value after {investment_period} years will be: ₹{future_value:.2f}")

#------learning corner-----

def learning_corner():
    st.header("Learning Corner: Financial Empowerment for Women")
    
    # Educational Resources
    st.subheader("Educational Resources")
    st.write(
        """
        - **[Women & Money – The Essential Guide to Financial Security](https://www.suzeorman.com/)**: A book by Suze Orman that empowers women with financial knowledge.
        - **[SheCapital](https://www.shecapital.in/)**: A platform offering financial literacy videos and articles tailored for women.
        - **[Women and Wealth by Ellevest](https://www.ellevest.com/)**: A platform providing tools and education for women to invest and plan for their financial futures.
        - **[The Financial Diet](https://thefinancialdiet.com/)**: A YouTube channel and blog offering financial advice on budgeting, investing, and more.
    """)

    # Financial Tools
    st.subheader("Financial Tools")
    
    st.write("**Budgeting & Expense Tracker Tools**")
    st.write("""
        - **[Mint](https://www.mint.com/)**: A tool to help you manage your budget and track expenses.
        - **[GoodBudget](https://www.goodbudget.com/)**: An envelope budgeting system for managing finances.
        - **[PocketGuard](https://www.pocketguard.com/)**: Helps track your spending and suggests ways to save.
    """)
    
    st.write("**SIP Calculator**")
    st.write("""
        - **[ET Money SIP Calculator](https://www.etmoney.com/)**: Calculate the potential returns on your SIP investments.
        - **[HDFC SIP Calculator](https://www.hdfcfund.com/)**: Another useful tool to evaluate the growth of SIP investments.
    """)

    st.write("**EMI Calculator**")
    st.write("""
        - **[HDFC EMI Calculator](https://www.hdfc.com/emi-calculator)**: Calculate your monthly EMI for loans.
        - **[BankBazaar EMI Calculator](https://www.bankbazaar.com/emi-calculator.html)**: A tool for calculating EMIs on personal loans and mortgages.
    """)

    st.write("**Investment Portfolio Tracker**")
    st.write("""
        - **[Personal Capital](https://www.personalcapital.com/)**: Track your investments and plan your financial future.
        - **[MoneyControl Portfolio Tracker](https://www.moneycontrol.com/)**: Keep track of all your investments in one place.
    """)

    # Financial Tools
    st.subheader("Financial Tools")
    
    st.write("**Budgeting & Expense Tracker Tools**")
    st.write("""
        - **[Mint](https://www.mint.com/)**: A tool to help you manage your budget and track expenses.
        - **[GoodBudget](https://www.goodbudget.com/)**: An envelope budgeting system for managing finances.
        - **[PocketGuard](https://www.pocketguard.com/)**: Helps track your spending and suggests ways to save.
    """)
    
    st.write("**SIP Calculator**")
    st.write("""
        - **[ET Money SIP Calculator](https://www.etmoney.com/)**: Calculate the potential returns on your SIP investments.
        - **[HDFC SIP Calculator](https://www.hdfcfund.com/)**: Another useful tool to evaluate the growth of SIP investments.
    """)

    st.write("**EMI Calculator**")
    st.write("""
        - **[HDFC EMI Calculator](https://www.hdfc.com/emi-calculator)**: Calculate your monthly EMI for loans.
        - **[BankBazaar EMI Calculator](https://www.bankbazaar.com/emi-calculator.html)**: A tool for calculating EMIs on personal loans and mortgages.
    """)

    st.write("**Investment Portfolio Tracker**")
    st.write("""
        - **[Personal Capital](https://www.personalcapital.com/)**: Track your investments and plan your financial future.
        - **[MoneyControl Portfolio Tracker](https://www.moneycontrol.com/)**: Keep track of all your investments in one place.
    """)


#--------quizdom------
def quiz_corner():
    st.header("Quiz Corner: Test Your Financial Knowledge")
    
    # Quiz Questions (Multiple-choice format)
    quiz_questions = [
        {
            "question": "What does SIP stand for in financial planning?",
            "options": ["Systematic Investment Plan", "Standard Investment Plan", "Systematic Income Plan"],
            "answer": "Systematic Investment Plan"
        },
        {
            "question": "Which tool helps you calculate your monthly EMI?",
            "options": ["Mint", "HDFC EMI Calculator", "GoodBudget"],
            "answer": "HDFC EMI Calculator"
        },
        {
            "question": "What is the main purpose of budgeting tools?",
            "options": ["Track monthly expenses", "Track investments", "Track personal goals"],
            "answer": "Track monthly expenses"
        }
    ]
    
    score = 0

    # Loop through the quiz questions
    for i, question in enumerate(quiz_questions, 1):
        user_answer = st.radio(f"Q{i}: {question['question']}", question["options"], key=i)
        
        if user_answer == question["answer"]:
            score += 1

    # Submit button to show score
    if st.button("Submit Quiz"):
        st.write(f"Your score is {score} out of {len(quiz_questions)}.")

    st.write("Good luck and keep learning!")


# ---- Main Execution ----
if __name__ == "__main__":
    if st.session_state.authenticated:
        if st.session_state.page == "dashboard":
            main_dashboard()
        else:
            home_page()
    else:
        if st.session_state.page == "login":
            login_page()
        else:
            home_page()
