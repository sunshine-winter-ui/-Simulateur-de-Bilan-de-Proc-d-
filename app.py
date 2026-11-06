import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Bilan Procédé", layout="wide")
st.title("🧪 Simulateur de Bilan de Procédé")
st.markdown("Ajustez les paramètres ci-dessous pour recalculer l'ensemble du bilan matière et énergétique.")

# --- BARRE LATÉRALE : SAISIE DES PARAMÈTRES ---
st.sidebar.header("⚙️ Paramètres d'entrée")

m0 = st.sidebar.number_input("Débit massique initial (kg/h)", value=1000.0, min_value=1.0, step=50.0)
x0_ins = st.sidebar.number_input("Fraction massique insolubles (0-1)", value=0.02, min_value=0.0, max_value=1.0, step=0.01)
x0_sol = st.sidebar.number_input("Fraction massique solubles (0-1)", value=0.10, min_value=0.0, max_value=1.0, step=0.01)

st.sidebar.subheader("Filtration")
residus = st.sidebar.number_input("Résidus filtrés (kg/h)", value=20.0, min_value=0.0, step=5.0)

st.sidebar.subheader("Mélange")
mR = st.sidebar.number_input("Apport de jus concentré (kg/h)", value=100.0, min_value=0.0, step=10.0)
xR = st.sidebar.number_input("Concentration de l'apport (0-1)", value=0.40, min_value=0.0, max_value=1.0, step=0.05)

st.sidebar.subheader("Chauffage & Refroidissement")
T2 = st.sidebar.number_input("Température d'entrée (°C)", value=20.0)
T3 = st.sidebar.number_input("Température après chauffage (°C)", value=80.0)
cp = st.sidebar.number_input("Capacité calorifique Cp [kJ/(kg·K)]", value=3.8)

st.sidebar.subheader("Évaporation")
x4 = st.sidebar.number_input("Concentration finale visée (0-1)", value=0.40, min_value=0.01, max_value=1.0, step=0.05)
lambda_v = st.sidebar.number_input("Chaleur latente [kJ/kg]", value=2300.0)
T4 = st.sidebar.number_input("Température avant refroidissement (°C)", value=80.0)
T5 = st.sidebar.number_input("Température après refroidissement (°C)", value=25.0)


# --- CALCULS (reprennent la logique de votre script) ---
# 1. Filtration
m1 = m0 - residus
x1 = (m0 * x0_sol) / m1 if m1 > 0 else 0

# 2. Mélange
m2 = m1 + mR
x2 = (m1 * x1 + mR * xR) / m2 if m2 > 0 else 0

# 3. Chauffage
Q3 = m2 * cp * (T3 - T2) / 3600

# 4. Évaporation
m4 = m2 * x2 / x4 if x4 > 0 else 0
mv = m2 - m4
Q4 = mv * lambda_v / 3600

# 5. Refroidissement
Q5 = m4 * cp * (T4 - T5) / 3600

# Bilan global
entrees = m0 + mR
sorties = residus + mv + m4


# --- AFFICHAGE DES RÉSULTATS ---
st.header("📊 Résultats du Bilan")

# Indicateurs principaux
col1, col2, col3 = st.columns(3)
col1.metric("Débit après filtration", f"{m1:,.2f} kg/h")
col2.metric("Concentration mélange", f"{x2 * 100:.2f} %")
col3.metric("Débit concentré final", f"{m4:,.2f} kg/h")

col4, col5, col6 = st.columns(3)
col4.metric("Eau évaporée", f"{mv:,.2f} kg/h")
col5.metric("Puissance de chauffage", f"{Q3:,.2f} kW")
col6.metric("Puissance d'évaporation", f"{Q4:,.2f} kW")

col7, col8 = st.columns(2)
col7.metric("Puissance de refroidissement", f"{Q5:,.2f} kW")
# Vérification du bilan (la différence doit être proche de 0)
erreur = entrees - sorties
col8.metric("Erreur bilan global", f"{erreur:,.2f} kg/h", delta=f"{erreur:,.2f}", delta_color="inverse")

with st.expander("Voir le détail des calculs"):
    st.write(f"**Fraction de soluble après filtration (x1) :** {x1:.4f}")
    st.write(f"**Bilan total après mélange :** {m2:,.2f} kg/h")
    st.write(f"**Entrées totales :** {entrees:,.2f} kg/h")
    st.write(f"**Sorties totales (résidus + vapeur + concentré) :** {sorties:,.2f} kg/h")
