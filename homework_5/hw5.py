"""Homework 09 - Scenario analysis for a delta-hedged spread-squared option."""
import itertools
import numpy as np

# ---------------- Parameters ----------------
r = 0.0132
sigma1_0, sigma2_0, rho_0 = 0.2214, 0.3036, 0.237
T = 0.25
S1_0, S2_0 = 158.12, 170.33
Delta = 1 / 252
h = 5 * Delta                       # 5-day horizon


# ---------------- (a) Closed-form price ----------------
def V(t, s1, s2, sig1, sig2, rho):
    """Price of payoff (S_T^(1) - S_T^(2))^2 at time t."""
    tau = T - t
    return np.exp(r * tau) * (s1**2 * np.exp(sig1**2 * tau)
                              - 2 * s1 * s2 * np.exp(sig1 * sig2 * rho * tau)
                              + s2**2 * np.exp(sig2**2 * tau))


def deltas(t, s1, s2, sig1, sig2, rho):
    """Black-Scholes deltas h^(1) = dV/ds1, h^(2) = dV/ds2."""
    tau = T - t
    h1 = 2 * np.exp(r * tau) * (s1 * np.exp(sig1**2 * tau) - s2 * np.exp(sig1 * sig2 * rho * tau))
    h2 = 2 * np.exp(r * tau) * (s2 * np.exp(sig2**2 * tau) - s1 * np.exp(sig1 * sig2 * rho * tau))
    return h1, h2


# ---------------- Portfolio at t = 0 ----------------
h1, h2 = deltas(0, S1_0, S2_0, sigma1_0, sigma2_0, rho_0)
V_opt0 = V(0, S1_0, S2_0, sigma1_0, sigma2_0, rho_0)
V_0 = V_opt0 - h1 * S1_0 - h2 * S2_0

print(f"h1 = {h1:.4f}, h2 = {h2:.4f}")
print(f"Option value = {V_opt0:.4f}, Portfolio V_0 = {V_0:.4f}\n")

# ---------------- Scenario grid and weights ----------------
X_grid = [-0.20, -0.10, -0.05, 0.05, 0.10, 0.20]
K_grid = [0.5, 0.75, 1.25, 1.5, 1.75, 2.0]          # sigma_{t+5D}/sigma_t
R_grid = [-0.5, 0.0, 0.5]                           # rho_{t+5D} - rho_t

wX = {0.20: 0.5, 0.10: 0.75, 0.05: 1.0}
wK = {0.5: 0.5, 2.0: 0.5, 0.75: 1.25, 1.75: 1.25, 1.25: 0.75, 1.5: 0.75}
wR = {0.0: 0.5, 0.5: 1.25}

# ---------------- Loop over all N = 3888 scenarios ----------------
results = []
for x1, x2, k1, k2, dr in itertools.product(X_grid, X_grid, K_grid, K_grid, R_grid):
    S1 = S1_0 * np.exp(x1)
    S2 = S2_0 * np.exp(x2)
    sig1, sig2, rho = k1 * sigma1_0, k2 * sigma2_0, rho_0 + dr
    V_h = V(h, S1, S2, sig1, sig2, rho) - h1 * S1 - h2 * S2   # hedge held fixed
    loss = -(V_h - V_0)
    w = wX[abs(x1)] * wX[abs(x2)] * wK[k1] * wK[k2] * wR[abs(dr)]
    results.append(dict(X1=x1, X2=x2, k1=k1, k2=k2, drho=dr, loss=loss, w=w, wloss=w * loss))

print(f"N = {len(results)} scenarios\n")


def show(tag, s):
    print(f"{tag}: X1={s['X1']:+.2f}, X2={s['X2']:+.2f}, "
          f"sig1/sig1_0={s['k1']}, sig2/sig2_0={s['k2']}, drho={s['drho']:+.1f}")
    print(f"   loss = {s['loss']:.4f}, weight = {s['w']:.6f}, w*loss = {s['wloss']:.4f}\n")


# (b) Worst case
show("(b) max loss", max(results, key=lambda s: s["loss"]))
# (c) Weighted worst case
show("(c) max weighted loss", max(results, key=lambda s: s["wloss"]))
