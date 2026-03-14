# 🌍 PyClimaExplorer

PyClimaExplorer is an interactive climate data visualization platform built with **Streamlit**.
It transforms complex **NetCDF climate datasets** into interactive maps, time-series trends, and comparison insights.

The platform enables researchers, students, and the public to explore climate patterns easily through an intuitive dashboard.

---

# 🚀 Project Setup

Follow these steps to run the project locally.

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/HarryOhm33/Hack_It_Out.git
cd Hack_It_Out
```

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Mac / Linux:

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

Install the required Python libraries.

```bash
pip install -r requirements.txt
```

Main libraries used:

- Streamlit
- Xarray
- Pandas
- NumPy
- Plotly
- PyDeck

---

## 4️⃣ Run the Application

Start the Streamlit server.

```bash
streamlit run app.py
```

The app will open in your browser automatically:

```
http://localhost:8501
```

---

# 🌐 Live Application

The deployed version of PyClimaExplorer is available here:

```
https://pyclima-remarkable.streamlit.app
```

This version allows users to upload climate datasets and explore them interactively without installing anything.

---

# 📂 Required Dataset Format

PyClimaExplorer works with **NetCDF (.nc) climate datasets** that contain **spatiotemporal climate data**.

The platform is designed to analyze **hourly climate datasets covering multiple months or years**, with several environmental variables such as temperature, humidity, and precipitation.

---

# ⏱ Temporal Resolution

The dataset should ideally contain **hourly observations**.

Example:

```
time: hourly data
example: 2020-01-01 00:00
         2020-01-01 01:00
         2020-01-01 02:00
         ...
```

Datasets spanning **multiple months or years** provide better visualization and comparison.

Example:

```
time dimension length: 8760
(1 year of hourly data)
```

---

# 🌎 Required Spatial Dimensions

The dataset must contain **geographical coordinates**.

```
latitude
longitude
```

Typical structure:

```
variable[time][latitude][longitude]
```

Example:

```
temperature[time][lat][lon]
humidity[time][lat][lon]
precipitation[time][lat][lon]
```

---

# 🌡 Supported Climate Variables

The dataset should include **multiple climate variables** for meaningful analysis.

Examples:

• Surface Temperature
• Humidity
• Precipitation / Rainfall
• Wind Speed
• Atmospheric Pressure
• Cloud Cover
• Sea Surface Temperature

The dashboard automatically detects variables and allows users to select them for visualization.

---

# 📊 Example Dataset Structure

Example NetCDF dataset:

```
Dimensions:
time: 8760
lat: 181
lon: 360

Variables:
temperature(time, lat, lon)
humidity(time, lat, lon)
precipitation(time, lat, lon)
```

---

# 🌐 Recommended Data Sources

You can download compatible hourly climate datasets from:

**ERA5 Reanalysis Dataset**
https://cds.climate.copernicus.eu/

**NOAA Climate Data**
https://www.noaa.gov/

**NASA EarthData**
https://earthdata.nasa.gov/

ERA5 datasets are recommended because they provide **hourly global climate data with many variables**.

---

# 📊 Key Features

- 🌍 Global spatial heatmap visualization
- 📈 Time-series climate trend analysis
- 🆚 Comparison mode for different time periods
- 📚 Dataset explorer for inspecting variables
- 🎬 Story mode for guided climate analysis
- 🌐 3D globe visualization

---

# 🛠 Technology Stack

Frontend / Interface
Streamlit

Data Processing
Python, Xarray, Pandas, NumPy

Visualization
Plotly, Plotly Geo

Dataset Format
NetCDF (.nc)

---

# 📜 License

This project is open-source and available under the MIT License.

---

# 👨‍💻 Authors

Developed as part of a climate data visualization project.

Team: PyClimaExplorer
