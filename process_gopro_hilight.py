import os
from pymediainfo import MediaInfo
from struct import unpack

PURPLE = '\033[35m'

def extract_hilight_tags(mp4_file_path):
    hilight_tags = []
    try:
        with open(mp4_file_path, 'rb') as file:
            data = file.read()
            pos = data.find(b'HMMT')
            if pos != -1:
                count = unpack(">I", data[pos + 4:pos + 8])[0]
                for i in range(count):
                    tag_offset = pos + 8 + (i * 4)
                    tag = unpack(">I", data[tag_offset:tag_offset + 4])[0]
                    hilight_tags.append(tag)
    except Exception as e:
        print(f"Error reading HiLight tags from {mp4_file_path}: {e}")
    return hilight_tags

def get_video_duration(mp4_file_path):
    media_info = MediaInfo.parse(mp4_file_path)
    for track in media_info.tracks:
        if track.track_type == "Video":
            return int(track.duration)
    return 0

def process_gopro_folder(folder_path, fps):
    mp4_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
    mp4_files.sort(key=os.path.getctime)

    if not mp4_files:
        print("No MP4 files found in the specified folder.")
        return

    total_offset = 0
    hilight_data = []

    lua_code = f'''{PURPLE}-- GoPro HiLight Tags to DaVinci Resolve Lua script

local projectManager = resolve:GetProjectManager()
local project = projectManager:GetCurrentProject()
local timeline = project:GetCurrentTimeline()

local fps = {fps}
local markers = {{
'''

    for mp4_file in mp4_files:
        hilight_tags = extract_hilight_tags(mp4_file)
        for tag in hilight_tags:
            adjusted_time = total_offset + tag
            frame_id = (adjusted_time * fps) / 1000
            file_name = os.path.basename(mp4_file)
            hilight_data.append(f'    {{ {frame_id:.3f}, "Blue", "{file_name}", "", 1, "" }},')

        total_offset += get_video_duration(mp4_file)

    lua_code += "\n".join(hilight_data) + "\n"

    lua_code += '''}
for i, marker in ipairs(markers) do
    local frame_id = marker[1]
    local color = marker[2]
    local name = marker[3]
    local note = marker[4]
    local duration = marker[5]
    local customData = marker[6]
    timeline:AddMarker(frame_id, color, name, note, duration, customData)
end
print("Markers added successfuly!")
'''

    print(lua_code)

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder with GoPro videos: ").strip()
    fps = int(input("Enter the FPS of your videos: ").strip())
    process_gopro_folder(folder_path, fps)