# ☀️ Solar ROI Analyzer (Myanmar-Focused)

A web-based Solar Return on Investment (ROI) Analyzer designed to help users in Myanmar assess the financial benefits of switching to solar energy. The system calculates potential savings, payback periods, break-even points, and supports data specific to local regions and appliance profiles.

---

## 🌟 Key Features

- 🔄 Multi-step ROI calculation with interactive UI
- 📍 Region-specific data (solar sunlight & electricity rates)
- 🧰 Appliance profiles (e.g. Tea Shop, Hospital Ward, Home)
- 🏷️ Package selection and incentive program options
- 📊 Live visual analysis of ROI and break-even results
- 🗺️ Integrated map with solar data per region
- 🧑‍💼 Admin dashboard for adding/editing profiles, incentives, and regions
- 📱 Fully responsive layout for desktop and mobile
- 🧠 Client-side validation and enhanced UX with JavaScript

---

## 🛠 Tech Stack

| Layer          | Technology               |
|----------------|--------------------------|
| Backend        | Django 4.x               |
| Frontend       | HTML5, CSS3, Bootstrap 5 |
| JS Enhancements| Vanilla JS + Chart.js    |
| Database       | SQLite3 (or PostgreSQL)  |
| Icons          | Bootstrap Icons          |
| Maps           | Leaflet.js               |
| Charts         | Chart.js                 |

---

## 📸 Screenshots

*(Add screenshots of key pages here if available)*

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure you have:

- Python 3.10+
- pip
- virtualenv (optional but recommended)
- Git (if cloning repo)

### 📦 Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/MinHein10/Solar-ROI-Analyzer-with-Django.git
   cd solar-roi-analyzer

2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install required packages
pip install -r requirements.txt

4. Apply database migrations
python manage.py migrate

5. Create a superuser (for admin login)
python manage.py createsuperuser

6. Run the server
python manage.py runserver


Then visit: http://127.0.0.1:8000/

How to Use
1. Homepage
    Browse the project landing page and explore the options.
2. ROI Analyzer
    Navigate to the ROI Analyzer and go through:
    - Step 1: Choose your region and appliance profile.
    - Step 2: Select your installation package and any incentives.
    - Step 3: View visual ROI results and financial summaries.
3. All Region Data Map
    See all regions in Myanmar and click on them to view solar sunlight data and electricity rates.
4. Admin Dashboard
    Log in as admin to add or manage:
    - Regions
    - Appliance profiles
    - Incentive programs
    - Installation packages


solar_roi_analyzer/
│
├── form/                    # Core app for forms and calculations
│   ├── models.py            # Models: Region, Appliance, Package, Incentive
│   ├── views.py             # Form views and logic
│   ├── forms.py             # Django forms
│   ├── templates/form/      # HTML templates
│   └── static/              # CSS and JS assets
│
├── solar_roi_analyzer/      # Project config
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL routing
│
├── manage.py
├── db.sqlite3               # Local database (can replace with PostgreSQL)
├── requirements.txt
└── README.md


Example User Roles
- End Users: Calculate their solar return based on their region and appliances.
- Admins: Manage the region, appliance, incentive, and package data in the admin panel.


Future Improvements
- Myanmar Unicode/Zawgyi language switch
- Downloadable PDF reports of ROI results
- User account system to save and compare multiple reports
- Real-time sunlight data integration using APIs


Future Improvements
Myanmar Unicode/Zawgyi language switch
Downloadable PDF reports of ROI results
User account system to save and compare multiple reports
Real-time sunlight data integration using APIs

Author
Min Thant
Project developed as part of an academic computing project tailored for Myanmar.
