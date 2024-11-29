# GoPro HiLight Marker Script for DaVinci Resolve

This Python script extracts HiLight markers from GoPro MP4 files and generates a Lua script that can be used to add these markers to a DaVinci Resolve timeline.

## Prerequisites

Before running this script, ensure you have the following:

- **Python 3**: The script is written in Python 3. You can download Python 3 from the official website: [python.org](https://www.python.org/).
- **DaVinci Resolve**: This script works with DaVinci Resolve 18 or later, which supports Lua scripting and the Resolve API.
- **pymediainfo**: A Python library used to extract metadata from video files (like duration).

You can install the necessary Python dependencies by running the following command:

### Install pymediainfo
`pip install pymediainfo`

## Setup

### Step 1: Download the Script

- Download the Python script `process_gopro_hilight.py` from the repository, or copy the content into a `.py` file.

### Step 2: Prepare the Videos

- Place your GoPro MP4 videos in a folder. The script will scan all `.mp4` files in the specified folder and extract HiLight tags from them.

### Step 3: Ensure DaVinci Resolve is Running

- Open DaVinci Resolve and make sure you have a project open.

### Step 4: Run the Script

1. Open the terminal or command prompt.
2. Navigate to the directory where you saved the Python script.
3. Run the script using Python:

`python process_gopro_hilight.py`

### Step 5: Provide Folder Path and FPS

- When prompted, input the full path to the folder containing your GoPro MP4 videos.
- Enter the FPS (Frames Per Second) of your videos (typically 25 or 30 FPS, depending on your GoPro model).

### Step 6: Generate the Lua Code

- The script will process the videos and extract HiLight tags.
- It will generate a Lua script with markers that can be used in DaVinci Resolve.
- The generated Lua code will be printed in the terminal.

### Step 7: Add Markers to DaVinci Resolve

- Copy the generated Lua code.
- Open DaVinci Resolve and go to **Workspace** > **Console**.
- Paste the Lua code into the console and press **Enter**.
- The HiLight markers will be added to your DaVinci Resolve timeline.

## Example Output (Lua Script)

The Lua script generated by the Python script will look something like this:

```
– Lua script for DaVinci Resolve to add HiLight markers from GoPro

local projectManager = resolve:GetProjectManager()
local project = projectManager:GetCurrentProject()
local timeline = project:GetCurrentTimeline()

local fps = 30
local markers = {
{ 1000.0, “Blue”, “FileName1”, “”, 1, “” },
{ 2000.0, “Green”, “FileName2”, “”, 1, “” },
{ 3000.0, “Red”, “FileName3”, “”, 1, “” },
}

for i, marker in ipairs(markers) do
local frame_id = marker[1]
local color = marker[2]
local name = marker[3]
local note = marker[4]
local duration = marker[5]
local customData = marker[6]
timeline:AddMarker(frame_id, color, name, note, duration, customData)
end
print(“Markers successfully added!”)
```

## Troubleshooting

### Issue: DaVinci Resolve does not recognize the Lua script

Make sure the following are true:
- You are using DaVinci Resolve 18 or later.
- You have copied and pasted the Lua script correctly into the Console window in DaVinci Resolve.
- The project is open and a timeline is available.

### Issue: No markers appear on the timeline

Check the FPS and ensure the GoPro video files are correctly processed. Verify that the generated Lua script contains correct time values for the markers.

## License

This project is licensed under the MIT License.
