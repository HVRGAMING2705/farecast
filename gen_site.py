import json
m = json.load(open("model.json"))
features, mean, std = m["features"], m["mean"], m["std"]
coef, icpt = m["coef"], m["intercept"]
mt = m["metrics"]
r2, mae, rmse, base_mae, mean_cost = mt["cv_r2"], mt["cv_mae"], mt["cv_rmse"], mt["baseline_mae"], mt["mean_cost"]
DOMAIN = "farecast.vercel.app"
JS_MODEL = f"""const MEAN = {json.dumps(mean)};
const STD = {json.dumps(std)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function farePred(vals){{
  let z = INTERCEPT;
  for (let i = 0; i < 6; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return Math.max(z, 1500);
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FareCast — Flight Fare Predictor | AI/ML Project</title>
<meta name="description" content="FareCast predicts flight ticket fares from airline tier, stops, duration, days before departure, route type and travel class, using a ridge regression model trained on 600 synthetic flight bookings. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="FareCast — Flight Fare Predictor">
<meta property="og:description" content="Enter your flight details and instantly see the predicted ticket fare, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="FareCast — Flight Fare Predictor">
<meta name="twitter:description" content="Ridge regression flight fare predictor. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"FareCast","applicationCategory":"EducationalApplication","description":"Flight fare predictor using ridge regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input,select{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:1.6em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}}
</style>
</head>
<body>
<h1>&#9992;&#65039; FareCast — Flight Fare Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A ridge regression model trained on 600 synthetic flight bookings predicts a ticket fare from airline tier, stops, duration, days booked before departure, route type and travel class. 5-fold CV: <b>R&sup2; = {r2:.3f}</b>, <b>MAE = &#8377;{mae:,.0f}</b> vs a mean-guess baseline MAE of &#8377;{base_mae:,.0f} (mean fare &#8377;{mean_cost:,.0f}).</p>
<div class="grid">
<label>Airline tier<select id="f0"><option value="1" selected>Budget</option><option value="2">Mid-range</option><option value="3">Premium</option></select></label>
<label>Stops<select id="f1"><option value="0" selected>Non-stop</option><option value="1">1 stop</option><option value="2">2 stops</option></select></label>
<label>Duration (hours)<input type="number" step="0.5" min="1" max="14" id="f2" value="2.0"></label>
<label>Days booked before departure<input type="number" step="1" min="1" max="90" id="f3" value="30"></label>
<label>Route<select id="f4"><option value="1" selected>Short domestic</option><option value="2">Long domestic</option><option value="3">International</option></select></label>
<label>Class<select id="f5"><option value="0" selected>Economy</option><option value="1">Business</option></select></label>
</div>
<button onclick="predict()">Predict Fare</button>
<button onclick="tryBusiness()">Try a business-class trip</button>
<button onclick="tryBudget()">Try a budget trip</button>
<div id="result"></div>
<p class="note">How it works: your six numbers are standardised (subtract the training mean, divide by the standard deviation), multiplied by the model&apos;s learned weights, and summed with a bias to give the fare in rupees; predictions are floored at &#8377;1,500. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: a budget non-stop 2-hour short domestic economy flight, booked 30 days early &rarr; about &#8377;6,734. A premium non-stop 9-hour international business flight, booked 3 days early &rarr; about &#8377;44,607. A mid-range 1-stop 5.5-hour long domestic economy flight, booked 45 days early &rarr; about &#8377;18,078.</p>
<p class="note">Honest note: this model was trained on synthetic bookings generated from simple fare logic, so it is a classroom demo — real fares also depend on the exact route, season, demand and the airline&apos;s dynamic pricing, which six numbers can&apos;t capture.</p>
<p><a href="https://github.com/HVRGAMING2705/farecast">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const vals = [];
  for (let i = 0; i < 6; i++) vals.push(parseFloat(document.getElementById("f" + i).value) || 0);
  const fare = farePred(vals);
  const el = document.getElementById("result");
  el.style.display = "block";
  const verdict = vals[5] === 1 ? "&#128747;&#65039; BUSINESS CLASS — the class upgrade is the biggest single fare driver" : vals[3] <= 7 ? "&#128308; BOOKED LATE — booking within a week of departure pushes the fare up" : fare >= 30000 ? "&#128993; PRICEY ROUTE — long or international flights cost much more" : "&#128994; BUDGET-FRIENDLY — book early, fly economy, fly direct";
  el.innerHTML = "<b>&#8377;" + fare.toLocaleString("en-IN", {{maximumFractionDigits: 0}}) + "</b><br>" + verdict;
}}
function predict(){{ show(); }}
function tryBusiness(){{ const v = [3, 0, 9.0, 3, 3, 1]; for (let i = 0; i < 6; i++) document.getElementById("f" + i).value = v[i]; show(); }}
function tryBudget(){{ const v = [1, 0, 2.0, 30, 1, 0]; for (let i = 0; i < 6; i++) document.getElementById("f" + i).value = v[i]; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — FareCast</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on FareCast.</p><p><a href="https://{DOMAIN}/">Back to FareCast</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# FareCast — Flight Fare Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — airline tier, stops, duration, days before departure, route type, class — trained on 600 synthetic flight bookings (seed 42).

- 5-fold CV R&sup2;: {r2:.3f}, MAE: &#8377;{mae:,.0f} (mean-guess baseline MAE: &#8377;{base_mae:,.0f}); mean fare &#8377;{mean_cost:,.0f}
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic bookings — real fares also depend on the exact route, season, demand and dynamic pricing.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{row: {json.dumps(s['row'])}, js: farePred({json.dumps(s['row'])}), py: {s['pred']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, R2", r2)
