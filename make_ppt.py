from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "farecast-zeta.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "FareCast — Flight Fare Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that looks at your flight — airline, stops, duration, how early you book — and predicts the ticket fare"])
add(1, "The Problem", ["Flight fares feel random: the same route can cost Rs 6,000 one week and Rs 12,000 the next", "Airline, stops, duration, booking time and class all push the price — but by how much?", "Can a simple, explainable model turn flight details into a fair fare estimate?", "FareCast answers that question with ridge regression anyone can follow"])
add(2, "The Solution — FareCast", ["Enter 6 details: airline tier, stops, duration, days before departure, route type, class", "The model returns the predicted ticket fare instantly", "Try a business-class trip or a budget trip with one click", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset generation and model training", "Ridge regression (alpha = 1.0) on 6 standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 600 synthetic flight bookings built from simple fare logic", "Flight details -> standardisation -> ridge regression -> ticket fare (floored at Rs 1,500)", "model.json ships with the site; JavaScript applies the same formula", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter the flight details and press Predict Fare", "Budget non-stop 2-hour short domestic economy flight, booked 30 days early -> about Rs 6,734", "Premium non-stop 9-hour international business flight, booked 3 days early -> about Rs 44,607", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation R-squared: 0.977, MAE: Rs 1,284", "Baseline (always guessing the mean fare): MAE Rs 8,349 — about 6.5x worse", "Mean fare in the data: Rs 27,599", "Browser demo matches Python predictions exactly on all test samples"])
add(7, "Future Scope", ["Train on real flight-fare data from public datasets", "Add features: exact route, season, departure time and day of week", "Show a fare trend — how the price moves as the departure date nears", "Compare fares across airlines for the same route and date"])
add(8, "Thank You", ["FareCast — Flight Fare Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/farecast", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_FareCast_2026-11-16.pptx")
print("slides:", len(prs.slides._sldIdLst))
