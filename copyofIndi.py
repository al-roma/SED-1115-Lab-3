import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

data = pd.read_csv(
    "daily_climate55.csv",
    keep_default_na=False
)
#keep_default_na=False tells the program not to automatically treat standard missing
# values since we want to control what qualifies as missing

for column in data.columns:
    for index in data.index:
        value = data.at[index, column] #This tells the program to pick a value at a specific row
        #and column and stores it as "value"

        if pd.isna(value) or str(value).strip() in ("M", ""):
            data.at[index, column] = pd.NA
            #pd.isna(value) returns True if the value is already missing, and str(value).strip()
            #turns the value into text.

data["Date/Time"] = pd.to_datetime(data["Date/Time"])
data["Max Temp (°C)"] = pd.to_numeric(data["Max Temp (°C)"])
data["Total Snow (cm)"] = pd.to_numeric(data["Total Snow (cm)"])
data = data.dropna(subset=["Date/Time", "Max Temp (°C)", "Total Snow (cm)"])

plt.figure(figsize=(12,6))

x = data["Date/Time"]

plt.plot(x, data["Max Temp (°C)"], label="Maximum Temperature", color="red")
plt.plot(x, data["Total Snow (cm)"], label="Total Snow (cm)", color="blue")

plt.title("Maximum Temp and Total Snow (cm) comparison")
plt.xlabel("Date")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)


plt.tight_layout()
plt.savefig("climate_graph.png")
plt.show()

date_input = input("What date would you like to see? (1955-01-01 - 1955-12-31): ").strip()
selected_date = pd.to_datetime(date_input, format="%Y-%m-%d", errors="coerce")

if pd.isna(selected_date):
    print("Please enter the date in YYYY-MM-DD format, for example 1955-01-03.")
else:
    matching_rows = data[data["Date/Time"] == selected_date]

    if matching_rows.empty:
        print(f"No climate data was found for {date_input}.")
    else:
        snow_amount = matching_rows.iloc[0]["Total Snow (cm)"]
        print(f"Total snow on {date_input}: {snow_amount:g} cm")

        if snow_amount > 8:
            snow_image = Image.open("0_SWNS_SCOTTISH_SNOW_01JPG.avif")
            snow_image.show()
        if 8 > snow_amount > 3:
            snow_image = Image.open("6cmsnow.webp")
            snow_image.show
        if 3 > snow_amount > 0:
            snow_image = Image.open("lightsnow.jpg")
            snow_image.show()
        else:
            print("There was no snowfall on this date, so no snow image was opened.")