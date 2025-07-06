import plotly.graph_objects as go
import streamlit as st
from calculate_fi_progress import calculate_fire_number, estimate_years_to_fi

st.set_page_config(page_title="🔥 FIRE Progress Tracker", page_icon="🔥")

st.image("logo.png", width=120)
st.title("🔥 FIRE Progress Tracker")
st.caption("Built with purpose by Money Matters Studio — tools for financial clarity and freedom.")

with st.expander("💡 What is FIRE and How Does This Tool Help?", expanded=True):
    st.markdown("""
**FIRE** stands for **Financial Independence, Retire Early**, a movement focused on reclaiming time, freedom, and choice by building a nest egg large enough to support your lifestyle without needing to work for money.

This tracker helps you answer one big question:

> _“How close am I to financial independence, and how long will it take me to get there?”_

### What It Calculates:
- **FIRE Number**: The amount of $ you'd need saved to sustainably cover your future lifestyle
- **Years to FIRE**: How long it’ll take to reach your FIRE Number, given your current savings habits
- **Net Worth Trajectory**: A year-by-year look at your financial progress
- **Progress Bar + Feedback**: Visual tools and insights to keep you motivated

Customize your inputs below and explore how your financial future unfolds.
    """)


st.header("📥 Input Your Info")

# Input fields
liquid_assets = st.number_input(
    "💰 Liquid or Investable Assets ($)",
    value=100000,
    step=1000,
    help="Include brokerage accounts, retirement accounts (401k, IRA), HSA, and cash savings. These are assets contributing to your FIRE path."
)
illiquid_assets = st.number_input(
    "🏠 Illiquid Assets (e.g. home equity) ($)",
    value=0,
    step=1000,
    help="Include your primary residence's equity, private businesses, real estate not producing income, collectibles, and other non-liquid holdings."
)
include_illiquid = st.checkbox("Include illiquid assets (e.g. home equity) in FIRE calculation?")
if include_illiquid:
    st.info("🏠 *You're including illiquid assets in your FIRE projection.*\n\nThis assumes you could sell or unlock equity from property or other non-liquid holdings—like real estate, private businesses, or collectibles.")
else:
    st.info("💰 *You're excluding illiquid assets from your FIRE projection.*\n\nThis gives a conservative view based only on accessible, investable funds like brokerage accounts, retirement accounts, and cash.")
if include_illiquid:
    current_net_worth = liquid_assets + illiquid_assets
else:
    current_net_worth = liquid_assets
st.caption("🔁 Not sure whether to include home equity in your FIRE calculation? Try toggling it on and off to see how it affects your timeline and progress. It’s a great way to model real-world tradeoffs.")
total_net_worth = liquid_assets + illiquid_assets
# Annual Savings
annual_savings = st.number_input(
    "Annual Savings ($)",
    value=30000,
    step=100,
    help="Total amount you save each year towards FI, including retirement and brokerage contributions."
)   
# Target Annual Expenses at FI
target_expenses = st.number_input(
    "Target Annual Expenses at FI ($)",
    value=50000,
    step=100,
    help="How much you expect to spend each year once you’ve reached financial independence. Think: housing, food, travel, healthcare... your lifestyle costs when you’re no longer working for income."
)
# Safe Withdrawal Rate (as a slider)
swr_percent = st.slider(
    "Safe Withdrawal Rate (%)",
    min_value=2.0,
    max_value=6.0,
    value=4.0,
    step=0.1,
    help="The percentage of your portfolio you plan to withdraw each year in retirement without running out of money. A common rule of thumb is 4%, but many FIRE folks use 3–3.5% for extra safety."
)
withdrawal_rate = swr_percent / 100  # Convert to decimal for calculations

# Expected Annual Return (as a slider)
expected_return_percent = st.slider(
    "Expected Annual Return (%)",
    min_value=3.0,
    max_value=10.0,
    value=7.0,
    step=0.1,
    help="The average yearly growth rate you expect from your investments before retirement. This includes stock market returns, dividends, and interest—minus any fees or taxes."
)
annual_return = expected_return_percent / 100  # Convert to decimal

#REAL ESTATE INVESTOR SECTION

with st.expander("🏠 Real Estate Investor? Add rental income & expenses (optional)", expanded=False):
    rental_income = st.number_input(
        "Annual Rental Income ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Total rent you expect to receive from the property each year."
    )

    mortgage = st.number_input(
        "Annual Mortgage Payments ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Total yearly mortgage payments (principal + interest)."
    )

    maintenance = st.number_input(
        "Annual Maintenance & Repairs ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Estimated yearly cost of upkeep, repairs, and maintenance."
    )

    tax_insurance = st.number_input(
        "Annual Property Tax & Insurance ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Combined yearly cost of property taxes and insurance."
    )

    net_re_cashflow = rental_income - mortgage - maintenance - tax_insurance
    st.markdown(f"**Net Real Estate Cashflow:** ${net_re_cashflow:,.0f} / year")
    include_real_estate = st.checkbox("Include net real estate cashflow in FIRE calculation?")

# Adjust expenses based on inclusion toggle
if include_real_estate:
    adjusted_expenses = max(target_expenses - net_re_cashflow, 0)
    st.info(f"🏠 You're factoring in ${net_re_cashflow:,.0f} in net rental income to reduce your annual expenses.")
else:
    adjusted_expenses = target_expenses
    st.info("💼 You're calculating FIRE based only on your spending and savings. Real estate income excluded.")

with st.expander("📈 Real Estate Appreciation (Optional)", expanded=False):
    st.markdown("Estimate how much your property might grow in value by the time you reach FIRE.")

    property_value = st.number_input(
        "Current Property Value ($)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        help="Estimated current market value of your property (primary or rental)."
    )

    appreciation_rate = st.slider(
        "Expected Annual Appreciation Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.1,
        help="Estimated yearly increase in property value."
    )

    years_to_fi_estimate = st.number_input(
        "Years Until FI (for projection)",
        min_value=0,
        value=10,
        help="Rough estimate of how many years until you reach financial independence."
    )

    future_value = property_value * ((1 + appreciation_rate / 100) ** years_to_fi_estimate)
    appreciation_gain = future_value - property_value

    st.markdown(f"**Estimated Property Value at FI:** ${future_value:,.0f}")
    st.caption(f"📈 That’s a projected gain of ${appreciation_gain:,.0f} over {years_to_fi_estimate} years.")


# Calculation trigger
if st.button("Calculate My FIRE Path"):
    fire_goal = calculate_fire_number(adjusted_expenses, withdrawal_rate)
    years_to_fi, final_net_worth, net_worth_history = estimate_years_to_fi(
        current_net_worth, annual_savings, annual_return, fire_goal
        )

    st.subheader("🎯 Results Summary")

    st.markdown(f"💡 Your target expenses were adjusted by **${net_re_cashflow:,.0f}** in rental income.")
    st.markdown(f"**Adjusted Annual Expenses at FI:** ${adjusted_expenses:,.0f}")

    st.markdown(f"""
    - **FIRE Goal:** ${fire_goal:,.0f}  
    - **Liquid Investable Assets:** ${liquid_assets:,.0f}  
    - **Illiquid Assets (e.g. home equity):** ${illiquid_assets:,.0f}  
    - **Total Net Worth:** ${total_net_worth:,.0f}  
    - **Estimated Years to FI (based on liquid assets):** {years_to_fi}  
    - **Projected Net Worth at FI:** ${final_net_worth:,.0f}
    """)


    st.subheader("🧭 Progress Toward FIRE")

    progress_pct = min(current_net_worth / fire_goal, 1.0)
    st.markdown(f"""
    **Liquid FIRE Progress:** {progress_pct * 100:.1f}%  
    **Total Net Worth:** ${total_net_worth:,.0f}  
    """)
    st.progress(progress_pct, text=f"{progress_pct * 100:.1f}% of FIRE goal reached")

    st.subheader("📣 A Message for you")

    if progress_pct >= 1.0:
        st.success("🎉 Based on your liquid assets alone, you’ve reached your FIRE number! You’re financially independent—and your net worth is even higher when counting other assets.")
    elif progress_pct >= 0.75:
        st.info(f"You're {progress_pct * 100:.1f}% of the way to FIRE. So close you can smell the campfire on your freedom hikes. At this pace, you’ll get there in {years_to_fi} years.")
    elif progress_pct >= 0.5:
        st.info(f"Halfway there! You’ve built up {progress_pct * 100:.1f}% of your FIRE goal. Keep stacking—it’s all compounding from here. FIRE is {years_to_fi} years away.")
    elif progress_pct >= 0.25:
        st.info(f"You’re {progress_pct * 100:.1f}% of the way in. You’ve started something powerful—stay the course and your {years_to_fi}-year plan will pay off.")
    else:
        st.info(f"Every FIRE journey starts with that first spark. You’re {progress_pct * 100:.1f}% there. With your current pace, independence is on the horizon in about {years_to_fi} years.")



    st.subheader("📈 Net Worth Projection")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=list(range(len(net_worth_history))),
    y=net_worth_history,
    mode='lines+markers',
    fill='tozeroy',
    name='Net Worth'
))

    # Add FIRE goal line
    fig.add_shape(
    type="line",
    x0=0,
    x1=len(net_worth_history),
    y0=fire_goal,
    y1=fire_goal,
    line=dict(color="green", width=2, dash="dash"),
)

    # Add annotation
    fig.add_annotation(
    x=years_to_fi,
    y=fire_goal,
    text="🎯 FIRE Target",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

    fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Net Worth ($)",
    template="plotly_white",
    showlegend=False
)

    st.plotly_chart(fig, use_container_width=True)
