
# streamlit_cara_transport.py

import streamlit as st
import pulp

st.title("Cara Orange Growers: Retail Transportation Planning")

st.write("""
Optimize transportation costs from Cara Orange Growers' production sites
to regional distribution centers (RDCs).
""")

# Define supply (tons) for each growing region
supply = {
    'Indian River, FL': 150,
    'Rio Grande Valley, TX': 170,
    'Central Valley, CA': 200
}

# Define demand (tons) for each RDC
demand = {
    'Atlanta, GA': 140,
    'Chicago, IL': 130,
    'Dallas, TX': 120,
    'Los Angeles, CA': 130
}

# Define transportation costs per ton
costs = {
    ('Indian River, FL', 'Atlanta, GA'): 500,
    ('Indian River, FL', 'Chicago, IL'): 700,
    ('Indian River, FL', 'Dallas, TX'): 800,
    ('Indian River, FL', 'Los Angeles, CA'): 1200,
    ('Rio Grande Valley, TX', 'Atlanta, GA'): 400,
    ('Rio Grande Valley, TX', 'Chicago, IL'): 600,
    ('Rio Grande Valley, TX', 'Dallas, TX'): 300,
    ('Rio Grande Valley, TX', 'Los Angeles, CA'): 1000,
    ('Central Valley, CA', 'Atlanta, GA'): 900,
    ('Central Valley, CA', 'Chicago, IL'): 850,
    ('Central Valley, CA', 'Dallas, TX'): 650,
    ('Central Valley, CA', 'Los Angeles, CA'): 400
}

# Build LP model
model = pulp.LpProblem("Cara_Orange_Transportation", pulp.LpMinimize)
routes = pulp.LpVariable.dicts("Route", (supply.keys(), demand.keys()), lowBound=0, cat='Continuous')

# Objective function
model += pulp.lpSum([routes[i][j] * costs[i, j] for i in supply for j in demand])

# Supply constraints
for i in supply:
    model += pulp.lpSum([routes[i][j] for j in demand]) <= supply[i], f"Supply_{i}"

# Demand constraints
for j in demand:
    model += pulp.lpSum([routes[i][j] for i in supply]) == demand[j], f"Demand_{j}"

# Solve the LP problem
model.solve()

# Show results
st.header("Optimization Result")

if model.status == 1:
    st.success(f"Total Minimum Transportation Cost: ${pulp.value(model.objective):,.2f}")
    
    st.subheader("Optimal Shipping Plan")
    for i in supply:
        for j in demand:
            if routes[i][j].varValue > 0:
                st.write(f"Ship {routes[i][j].varValue:.0f} tons from {i} to {j}")

    st.subheader("Sensitivity Analysis")
    st.write("Shadow Prices for Constraints:")
    for name, constraint in model.constraints.items():
        st.write(f"{name}: Shadow Price = {constraint.pi}, Slack = {constraint.slack}")
else:
    st.error("No optimal solution found.")
