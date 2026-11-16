import json
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

rng = np.random.default_rng(42)
N = 600  # synthetic flight bookings

airline = rng.integers(1, 4, N).astype(float)   # 1 budget, 2 mid, 3 premium
stops = rng.integers(0, 3, N).astype(float)      # 0, 1, 2 stops
duration = rng.uniform(1.0, 14.0, N)            # flight duration in hours
days = rng.integers(1, 91, N).astype(float)      # days booked before departure
route = rng.integers(1, 4, N).astype(float)      # 1 short domestic, 2 long domestic, 3 international
cls = rng.integers(0, 2, N).astype(float)        # 0 economy, 1 business

X_raw = np.column_stack([airline, stops, duration, days, route, cls])
FEATURES = ["airline", "stops", "duration", "days", "route", "cls"]

# Generative fare (Rs): duration is the main driver; premium airline, business
# class and international routes add large amounts; late booking costs more;
# extra stops make the ticket cheaper.
airline_effect = np.where(airline == 1, 0.0, np.where(airline == 2, 1500.0, 4000.0))
route_effect = np.where(route == 1, 0.0, np.where(route == 2, 2500.0, 9000.0))
late_effect = np.maximum(0, 30 - days) * 120.0   # last-minute surge
fare = (2500
        + 1800 * duration
        + airline_effect
        + route_effect
        + 12000 * cls
        - 700 * stops
        + late_effect
        + rng.normal(0, 800, N))
fare = np.clip(fare, 1500, None)
y = fare

mean = X_raw.mean(axis=0)
std = X_raw.std(axis=0)
X = (X_raw - mean) / std

model = Ridge(alpha=1.0).fit(X, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), X, y, cv=kf)
r2 = float(r2_score(y, pred_cv))
mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
base_mae = float(mean_absolute_error(y, np.full(N, y.mean())))
print(f"n={N} mean_fare={y.mean():.0f} median_fare={np.median(y):.0f}")
print(f"CV R2={r2:.3f} MAE={mae:.0f} RMSE={rmse:.0f} baseline_MAE={base_mae:.0f}")

mj = {"features": FEATURES, "mean": mean.tolist(), "std": std.tolist(),
      "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
      "metrics": {"cv_r2": r2, "cv_mae": mae, "cv_rmse": rmse,
                  "baseline_mae": base_mae, "mean_cost": float(y.mean()), "n": N}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def py_pred(row):
    xs = (np.array(row) - mean) / std
    return float(max(model.predict([xs])[0], 1500))

samples = [
    [1, 0, 2.0, 30, 1, 0],    # budget, nonstop, 2h, booked 30d early, short domestic, economy
    [3, 0, 9.0, 3, 3, 1],     # premium, nonstop, 9h, booked 3d early, international, business
    [2, 1, 5.5, 45, 2, 0],    # mid, 1 stop, 5.5h, booked 45d early, long domestic, economy
    [1, 2, 3.0, 60, 1, 0],    # budget, 2 stops, 3h, booked 60d early, short domestic, economy
    [3, 1, 12.0, 7, 3, 1],    # premium, 1 stop, 12h, booked 7d early, international, business
]
for s in samples:
    print(s, "->", round(py_pred(s), 2), "Rs")
with open("parity_samples.json", "w") as f:
    json.dump([{"row": s, "pred": py_pred(s)} for s in samples], f, indent=1)
