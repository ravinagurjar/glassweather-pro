# 🌤️ GlassWeather Pro — Google-Inspired Weather Dashboard

A modern, responsive, and feature-rich Weather Application built with **Python (Flask)** and **JavaScript**. Inspired by Google's clean weather card design, this application fetches real-time weather metrics, multi-day forecasts, and hourly timelines using the free **Open-Meteo API**.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Iconify](https://img.shields.io/badge/Icons-Iconify--Meteocons-1769aa?style=for-the-badge)

---

## ✨ Features

- **Real-Time Data**: Instant updates for temperature, "feels like" status, humidity, wind speed, atmospheric pressure, and visibility.
- **3D Animated SVGs**: Interactive and smooth animated weather icons provided by Meteocons via Iconify.
- **6-Day Forecast**: Multi-day weather preview cards with daily high/low temperatures.
- **Hourly Weather Timeline**: Interactive horizontal scroll displaying hourly temperature fluctuations.
- **Dynamic Embedded Map**: Real-time location visualizer centered on the searched city.
- **No API Keys Required**: Uses open-access geocoding and forecasting endpoints.

---

## 🌐 Weather Data Provider

All meteorological data and geocoding services used in this application are provided by:

* **Open-Meteo**: [https://open-meteo.com](https://open-meteo.com)

---

## 📁 Recommended Directory Structure

To ensure Flask locates templates and virtual environments correctly, maintain the following file structure:

```text
weather-app/
│
├── venv/                 # Virtual environment folder (auto-generated)
├── templates/
│   └── index.html        # Main dashboard HTML template
├── app.py                # Core Flask backend script
├── requirements.txt      # Project dependencies list
└── README.md             # Project documentation
```

## Quick Setup & Execution (Combined Commands)

### Option A: One-Line Complete Setup & Run (Linux / macOS / Git Bash)
Copy and run this single command to clone, navigate, create a virtual environment, install dependencies, and start the app automatically:

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git) && cd your-repo-name && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install flask requests && python app.py
```
### Option B: Step-by-Step Combined Commands
#### 1. Clone & Enter Project
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git) && cd your-repo-name
```

#### 2. Create, Activate Virtual Environment & Install Dependencies
- Linux / macOS / Git Bash:
```bash
python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install flask requests
```

- Windows (Command Prompt):
```bash
python -m venv venv && venv\Scripts\activate && python -m pip install --upgrade pip && pip install flask requests
```

- Windows (PowerShell):
```bash
python -m venv venv; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install flask requests
```

#### 3. Run the Application
```bash
python app.py
```

> Once executed, open your browser and go to: http://127.0.0.1:5000

### Individual Bash Maintenance Commands

Action | Command
Activate venv | source venv/bin/activate (macOS/Linux) or venv\Scripts\activate (Windows)
Deactivate venv | deactivate
Export dependencies | pip freeze > requirements.txt
Install from file | pip install -r requirements.txt
Clean cache files | find . -type d -name "__pycache__" -exec rm -rf {} +
Delete virtual env | rm -rf venv

## HAPPY LEARNING