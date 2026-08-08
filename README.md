# 🏨 Investigate Hotel Business Using Data Visualization

Understanding Booking & Cancellation Behaviour — a data analytics project on a real-world hotel bookings dataset (2017–2019), built with Python and deployed as an interactive Streamlit dashboard.

---

## 📌 Project Overview

Business performance analysis is key to understanding customer behaviour: what drives guests to book, and what drives them to cancel. This project cleans and analyses ~119K hotel bookings to answer three core business questions, then turns the findings into actionable recommendations for hotel management.

### Business Questions

1. **Hotel type popularity** — Which hotel type (City Hotel or Resort Hotel) do customers book most often?
2. **Stay duration vs. cancellation** — Does the length of a guest's stay affect the cancellation rate?
3. **Lead time vs. cancellation** — Does the gap between booking and arrival date affect the cancellation rate?

---

## 📊 Dataset

| Detail | Value |
|---|---|
| Source | Hotel bookings dataset, 2017–2019 |
| Rows | 119,390 (raw) → 117,398 (after cleaning) |
| Columns | 29 |
| Key fields | `hotel`, `is_canceled`, `lead_time`, `stays_in_weekend_nights`, `stays_in_weekdays_nights`, `arrival_date_month`, `adr` |

---

## 🧹 Data Cleaning Summary

| Issue | Action Taken | Reason |
|---|---|---|
| `company` / `agent` missing | Filled with `0` | Missing means "no company/agent on file," not an error |
| `city` missing | Filled with `"Unknown"` | Preserves the row without fabricating a location |
| `children` missing | Filled with `0` | Safest, most common default |
| `meal` = `"Undefined"` | Recoded to `"No Meal"` | Same real-world meaning |
| Duplicate rows (~28%) | **Kept** | No unique booking ID exists to prove they are errors |
| `adr` ≤ 0 or > 1000 | Removed | Invalid or clearly erroneous room rates |
| Zero-guest bookings | Removed | Cannot represent a real stay |

Full reasoning for every decision is documented in the analysis notebook.

---

## 📁 Project Structure

```
hotel-business-dashboard/
├── app.py                          # Streamlit dashboard
├── hotel_bookings_clean.csv        # Cleaned dataset used by the dashboard
├── hotel_business_analysis.ipynb   # Full analysis notebook (cleaning + charts + findings)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🛠️ Tools & Libraries

- **Python** — Pandas, NumPy
- **Visualization** — Matplotlib, Seaborn (notebook), Plotly (dashboard)
- **Dashboard** — Streamlit
- **Notebook** — Jupyter

---

## ▶️ Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/hotel-business-dashboard.git
   cd hotel-business-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

4. Open the notebook (optional, for full analysis and findings):
   ```bash
   jupyter notebook hotel_business_analysis.ipynb
   ```

---

## 🌐 Live Dashboard

🔗 **(https://hotel-analysis-wg7upyxavb5evfjwlegr7n.streamlit.app/)**

---

## 📈 Key Findings

- **City Hotel** receives more bookings than **Resort Hotel**, and both peak during the summer months.
- **Cancellation rate rises with length of stay** — longer bookings are cancelled more often, and City Hotel is consistently higher than Resort Hotel.
- **Cancellation rate rises sharply with lead time** — bookings made far in advance (365+ days) cancel most often, especially for City Hotel.

## 💡 Recommendations

1. **Grow the Resort Hotel segment** with targeted seasonal promotions, especially outside peak summer months.
2. **Introduce stricter deposit or cancellation policies for longer stays**, where cancellation risk is highest.
3. **Send confirmation reminders and offer flexible rescheduling for far-ahead bookings** to reduce late cancellations on high-lead-time reservations — this is the single highest-impact lever, since lead time shows the sharpest rise in cancellation risk across the dataset.

---


