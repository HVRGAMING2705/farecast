# FareCast — Flight Fare Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — airline tier, stops, duration, days before departure, route type, class — trained on 600 synthetic flight bookings (seed 42).

- 5-fold CV R&sup2;: 0.977, MAE: &#8377;1,284 (mean-guess baseline MAE: &#8377;8,349); mean fare &#8377;27,599
- Live demo: https://farecast.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic bookings — real fares also depend on the exact route, season, demand and dynamic pricing.
