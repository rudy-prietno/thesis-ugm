import pandas as pd
import random

# Generate a dataset for 200 boxes of medication
ranges = 200
data = {
    "Barang": [f"Obat-{i+1}" for i in range(ranges)],
    "Panjang (cm)": [random.randint(40, 70) for _ in range(ranges)],
    "Lebar (cm)": [random.randint(30, 50) for _ in range(ranges)],
    "Tinggi (cm)": [random.randint(20, 40) for _ in range(ranges)],
    "Berat (kg)": [random.randint(5, 15) for _ in range(ranges)],
    "Jarak (km)": [random.randint(10, 100) for _ in range(ranges)],
}

# Create DataFrame
df_boxes = pd.DataFrame(data)

# Step 1: Calculate volume
df_boxes["Volume (cm³)"] = (
    df_boxes["Panjang (cm)"] * df_boxes["Lebar (cm)"] * df_boxes["Tinggi (cm)"]
)

# Step 2: Calculate ranks
df_boxes["Rank Berat"] = df_boxes["Berat (kg)"].rank(ascending=False)
df_boxes["Rank Jarak"] = df_boxes["Jarak (km)"].rank(ascending=False)
df_boxes["Rank Volume"] = df_boxes["Volume (cm³)"].rank(ascending=False)

# Step 3: Calculate LIFO Combination
df_boxes["LIFO Kombinasi"] = (
    df_boxes["Rank Berat"] * 0.3 +
    df_boxes["Rank Jarak"] * 0.4 +
    df_boxes["Rank Volume"] * 0.3
)

# Step 4: Sort by LIFO Combination
df_boxes = df_boxes.sort_values(by="LIFO Kombinasi", ascending=False)

# Step 5: Assign trucks based on cumulative volume
truck_volume_limit = 310 * 170 * 170
current_volume = 0
truck_id = 1
truck_assignments = []

for volume in df_boxes["Volume (cm³)"]:
    if current_volume + volume > truck_volume_limit:
        truck_id += 1
        current_volume = 0
    truck_assignments.append(truck_id)
    current_volume += volume

df_boxes["Truck ID"] = truck_assignments

# Step 6: Adjust cumulative volume for each truck
df_boxes["Adjusted Cumulative Volume"] = df_boxes.groupby("Truck ID")["Volume (cm³)"].cumsum()

# Step 7: Assign LIFO Order within each truck
df_boxes["LIFO Order"] = df_boxes.groupby("Truck ID").cumcount() + 1

# Output the final DataFrame
#filtered_truck_2 = df_boxes[df_boxes["Truck ID"] == 2]
#filtered_truck_2
df_boxes.head(15)
df_boxes.info()
