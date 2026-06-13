"""
NeoBank — Streamlit Banking Dashboard
Run with:  streamlit run app.py
"""

import streamlit as st
import bank

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="NeoBank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Root palette ── */
:root {
    --ink:        #0f1117;
    --surface:    #181c27;
    --card:       #1e2333;
    --border:     #2a2f45;
    --accent:     #4f8ef7;
    --accent-alt: #7c5cbf;
    --green:      #2ecc71;
    --red:        #e74c3c;
    --amber:      #f39c12;
    --text:       #e8eaf6;
    --muted:      #8892b0;
    --radius:     14px;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--ink);
    color: var(--text);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.92rem;
    color: var(--muted);
    padding: 6px 0;
    transition: color 0.15s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: var(--text); }

/* ── Main background ── */
.main .block-container { background: var(--ink); padding-top: 1.5rem; }

/* ── Page heading ── */
.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.15rem;
}
.page-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}

/* ── Cards ── */
.neo-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.neo-card h4 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
.neo-card .value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text);
}
.neo-card .label {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 0.15rem;
}

/* ── Account detail card ── */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}
.detail-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
}
.detail-item .d-label {
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
    margin-bottom: 0.25rem;
}
.detail-item .d-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}

/* ── Balance pill ── */
.balance-pill {
    display: inline-block;
    background: linear-gradient(135deg, #1a3a6e 0%, #2d1b69 100%);
    border: 1px solid var(--accent);
    border-radius: 50px;
    padding: 0.5rem 1.2rem;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
    margin: 0.5rem 0 1rem;
}

/* ── Accent divider ── */
.acc-line {
    height: 3px;
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent-alt) 100%);
    border-radius: 2px;
    margin-bottom: 1.4rem;
}

/* ── Form inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,142,247,0.18) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.87 !important; }

/* ── Alert overrides ── */
.stAlert { border-radius: 10px !important; }

/* ── Sidebar brand ── */
.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    padding: 0.5rem 0 1.2rem;
}
.brand span { color: var(--accent); }

/* ── Danger button ── */
.danger > button {
    background: var(--red) !important;
}

/* ── Transaction badge ── */
.txn-badge {
    display: inline-block;
    border-radius: 6px;
    padding: 0.18rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
}
.txn-deposit  { background: rgba(46,204,113,0.15); color: var(--green); }
.txn-withdraw { background: rgba(231,76,60,0.15);  color: var(--red); }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────

def _init_state():
    defaults = {
        "page": "Create Account",
        "last_account": None,   # stores account dict after successful create/login
        "flash": None,          # {"type": "success"|"error", "msg": str}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="brand">Neo<span>Bank</span></div>', unsafe_allow_html=True)
    st.markdown("---")

    nav_items = [
        "🏠  Dashboard",
        "➕  Create Account",
        "💰  Deposit",
        "💸  Withdraw",
        "🔍  Account Details",
        "✏️  Update Details",
        "🗑️  Delete Account",
    ]

    page_labels = {item.split("  ")[1]: item for item in nav_items}

    chosen = st.radio(
        "Navigation",
        options=[item.split("  ")[1] for item in nav_items],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<p style="font-size:0.75rem;color:#8892b0;">JSON-backed · Local storage</p>', unsafe_allow_html=True)


# ── Flash message helper ──────────────────────────────────────────────────────

def show_flash():
    if st.session_state.flash:
        f = st.session_state.flash
        if f["type"] == "success":
            st.success(f["msg"])
        else:
            st.error(f["msg"])
        st.session_state.flash = None


def set_flash(type_: str, msg: str):
    st.session_state.flash = {"type": type_, "msg": msg}


# ── Reusable auth form ────────────────────────────────────────────────────────

def auth_fields(key_prefix: str):
    c1, c2 = st.columns(2)
    acc = c1.text_input("Account Number", key=f"{key_prefix}_acc", placeholder="e.g. AB3C9Z7D")
    pin = c2.text_input("PIN", type="password", key=f"{key_prefix}_pin", max_chars=4, placeholder="4-digit PIN")
    return acc.strip(), pin.strip()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Overview of all accounts in the system</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    accounts = bank.get_all_accounts()
    total_accounts = len(accounts)
    total_balance = sum(a["balance"] for a in accounts)
    avg_balance = total_balance / total_accounts if total_accounts else 0

    # KPI cards
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="neo-card">
          <h4>Total Accounts</h4>
          <div class="value">{total_accounts}</div>
          <div class="label">active accounts</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="neo-card">
          <h4>Total Deposits Held</h4>
          <div class="value">₹{total_balance:,.0f}</div>
          <div class="label">across all accounts</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="neo-card">
          <h4>Average Balance</h4>
          <div class="value">₹{avg_balance:,.0f}</div>
          <div class="label">per account</div>
        </div>""", unsafe_allow_html=True)

    # Account table
    if accounts:
        st.markdown("#### All Accounts")
        display = [
    {
        "Name": a.get("name", ""),
        "Account No": a.get("account_no", ""),
        "Email": a.get("email", ""),
        "Age": a.get("age", ""),
        "Balance (₹)": f"₹{a.get('balance', 0):,.2f}",
    }
    for a in accounts
]
        st.dataframe(display, use_container_width=True, hide_index=True)
    else:
        st.info("No accounts found. Create one to get started!")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CREATE ACCOUNT
# ══════════════════════════════════════════════════════════════════════════════

def page_create():
    st.markdown('<p class="page-title">Open New Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Fill in the details below to create a new bank account</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    with st.form("create_form"):
        c1, c2 = st.columns(2)
        name  = c1.text_input("Full Name *", placeholder="e.g. Priya Sharma")
        email = c2.text_input("Email Address *", placeholder="priya@example.com")

        c3, c4, c5 = st.columns(3)
        age     = c3.number_input("Age *", min_value=1, max_value=120, value=25)
        pin     = c4.text_input("4-Digit PIN *", type="password", max_chars=4, placeholder="••••")
        deposit = c5.number_input("Initial Deposit (₹)", min_value=0.0, value=0.0, step=100.0)

        submitted = st.form_submit_button("Create Account →", use_container_width=True)

    if submitted:
        result = bank.create_account(name, int(age), email, pin, deposit)
        if result["success"]:
            acc = result["data"]
            st.session_state.last_account = acc
            set_flash("success", result["message"])
            # Show account card immediately
            st.markdown("#### Your New Account")
            st.markdown(f"""
            <div class="neo-card">
              <h4>Account Created</h4>
              <div class="detail-grid">
                <div class="detail-item"><div class="d-label">Name</div><div class="d-value">{acc['name']}</div></div>
                <div class="detail-item"><div class="d-label">Account Number</div><div class="d-value" style="color:#4f8ef7;font-family:monospace">{acc['account_no']}</div></div>
                <div class="detail-item"><div class="d-label">Email</div><div class="d-value">{acc['email']}</div></div>
                <div class="detail-item"><div class="d-label">Opening Balance</div><div class="d-value">₹{acc['balance']:,.2f}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.warning("🔐 Save your account number and PIN — they cannot be recovered.")
        else:
            set_flash("error", result["message"])
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DEPOSIT
# ══════════════════════════════════════════════════════════════════════════════

def page_deposit():
    st.markdown('<p class="page-title">Deposit Money</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Add funds to your account</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    with st.form("deposit_form"):
        acc_no, pin = auth_fields("dep")
        amount = st.number_input("Amount to Deposit (₹) *", min_value=1.0, value=1000.0, step=500.0)
        submitted = st.form_submit_button("Deposit →", use_container_width=True)

    if submitted:
        result = bank.deposit(acc_no, pin, amount)
        if result["success"]:
            bal = result["data"]["balance"]
            st.success(result["message"])
            st.markdown(f"""
            <div class="neo-card" style="max-width:340px;">
              <h4>Updated Balance</h4>
              <div class="balance-pill">₹{bal:,.2f}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.error(result["message"])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: WITHDRAW
# ══════════════════════════════════════════════════════════════════════════════

def page_withdraw():
    st.markdown('<p class="page-title">Withdraw Money</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Transfer funds out of your account</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    with st.form("withdraw_form"):
        acc_no, pin = auth_fields("wit")
        amount = st.number_input("Amount to Withdraw (₹) *", min_value=1.0, value=500.0, step=100.0)
        submitted = st.form_submit_button("Withdraw →", use_container_width=True)

    if submitted:
        result = bank.withdraw(acc_no, pin, amount)
        if result["success"]:
            bal = result["data"]["balance"]
            st.success(result["message"])
            st.markdown(f"""
            <div class="neo-card" style="max-width:340px;">
              <h4>Remaining Balance</h4>
              <div class="balance-pill">₹{bal:,.2f}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.error(result["message"])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ACCOUNT DETAILS
# ══════════════════════════════════════════════════════════════════════════════

def page_details():
    st.markdown('<p class="page-title">Account Details</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">View your full account information</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    with st.form("details_form"):
        acc_no, pin = auth_fields("det")
        submitted = st.form_submit_button("Fetch Details →", use_container_width=True)

    if submitted:
        result = bank.get_account(acc_no, pin)
        if result["success"]:
            a = result["data"]
            st.markdown(f"""
            <div class="neo-card">
              <h4>Account Holder</h4>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;margin-bottom:0.3rem">{a['name']}</div>
              <div class="balance-pill">₹{a['balance']:,.2f}</div>
              <div class="detail-grid">
                <div class="detail-item"><div class="d-label">Account Number</div><div class="d-value" style="font-family:monospace;color:#4f8ef7">{a['account_no']}</div></div>
                <div class="detail-item"><div class="d-label">Email</div><div class="d-value">{a['email']}</div></div>
                <div class="detail-item"><div class="d-label">Age</div><div class="d-value">{a['age']} years</div></div>
                <div class="detail-item"><div class="d-label">Account Status</div><div class="d-value" style="color:#2ecc71">● Active</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(result["message"])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPDATE DETAILS
# ══════════════════════════════════════════════════════════════════════════════

def page_update():
    st.markdown('<p class="page-title">Update Account Details</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Change your name, email, or PIN. Leave a field blank to keep it unchanged.</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    with st.form("update_form"):
        st.markdown("**Authenticate**")
        acc_no, pin = auth_fields("upd")
        st.markdown("---")
        st.markdown("**New Values** *(leave blank to keep current)*")
        c1, c2, c3 = st.columns(3)
        new_name  = c1.text_input("New Name",  placeholder="leave blank to skip")
        new_email = c2.text_input("New Email", placeholder="leave blank to skip")
        new_pin   = c3.text_input("New PIN",   type="password", max_chars=4, placeholder="leave blank to skip")
        submitted = st.form_submit_button("Save Changes →", use_container_width=True)

    if submitted:
        result = bank.update_account(acc_no, pin, new_name, new_email, new_pin)
        if result["success"]:
            a = result["data"]
            st.success(result["message"])
            st.markdown(f"""
            <div class="neo-card" style="max-width:480px;">
              <h4>Updated Profile</h4>
              <div class="detail-grid">
                <div class="detail-item"><div class="d-label">Name</div><div class="d-value">{a['name']}</div></div>
                <div class="detail-item"><div class="d-label">Email</div><div class="d-value">{a['email']}</div></div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.error(result["message"])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DELETE ACCOUNT
# ══════════════════════════════════════════════════════════════════════════════

def page_delete():
    st.markdown('<p class="page-title">Delete Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">This action is permanent and cannot be undone.</p>', unsafe_allow_html=True)
    st.markdown('<div class="acc-line"></div>', unsafe_allow_html=True)

    show_flash()

    st.warning("⚠️ Deleting your account will permanently erase all data and your remaining balance.")

    with st.form("delete_form"):
        acc_no, pin = auth_fields("del")
        confirmed = st.checkbox("I understand this action is irreversible")
        submitted = st.form_submit_button("Delete Account", use_container_width=True)

    if submitted:
        if not confirmed:
            st.error("Please check the confirmation box before deleting.")
        else:
            result = bank.delete_account(acc_no, pin)
            if result["success"]:
                st.success(result["message"])
                st.balloons()
            else:
                st.error(result["message"])


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════

PAGES = {
    "Dashboard":       page_dashboard,
    "Create Account":  page_create,
    "Deposit":         page_deposit,
    "Withdraw":        page_withdraw,
    "Account Details": page_details,
    "Update Details":  page_update,
    "Delete Account":  page_delete,
}

PAGES[chosen]()