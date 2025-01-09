import os
import pandas as pd

# Define the root folder containing your measurement data
root_folder = r"C:\Users\Anwender\hochschule-stralsund.de\Jan-Christian Kuhr - 1 Dr. Diestel GmbH\2 Wissenschaftliche Literatur\Abschlussarbeiten\Talaviya (Masterarbeit)\Measurement"

# Define the measurement folders (adjust if more folders exist)
measurement_folders = ["31", "32", "34"]

def load_data(root_folder, measurement_folders):
    """Load raw measurement data from multiple folders into a pandas DataFrame."""
    data = []

    # Iterate through each measurement folder
    for folder in measurement_folders:
        folder_path = os.path.join(root_folder, folder)

        # Files for x, y, and z axes
        files = {
            "x": os.path.join(folder_path, "xAxisS1.txt"),
            "y": os.path.join(folder_path, "yAxisS1.txt"),
            "z": os.path.join(folder_path, "zAxisS1.txt")
        }

        # Process each file (x, y, z axes)
        folder_data = {}
        for axis, file_path in files.items():
            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            # Load the data from the file
            try:
                folder_data[axis] = pd.read_csv(file_path, header=None)[0]  # Extract the first column explicitly
            except Exception as e:
                print(f"Error loading file {file_path}: {e}")
                continue

        if folder_data:
            folder_df = pd.DataFrame(folder_data)
            folder_df['folder'] = folder  # Add a column for the folder name
            data.append(folder_df)

    # Combine all data into a single DataFrame
    if data:
        combined_data = pd.concat(data, ignore_index=True)
        return combined_data
    else:
        print("No data loaded.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = load_data(root_folder, measurement_folders)
