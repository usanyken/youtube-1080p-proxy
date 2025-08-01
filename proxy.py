#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

CHANNELS = {
    "中天新闻": "pXBrROy-rvE",
    "CCTV4中文国际（美洲）": "OvopT1IJycY",
    "東森新聞": "E0zhe2gkXBs",
    "台視新聞": "xL0ch83RAK8",
    "TVBS新聞": "2mCSYvcfhtc",
    "中視新聞": "TCnaIE_SAtM",
    "非凡財經": "eA6Aczd3FZM"
}

def get_hls_url(video_id):
    try:
        cmd = f'yt-dlp -f "bestvideo[height=1080]+bestaudio" --get-url "https://youtu.be/{video_id}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def generate_m3u8():
    m3u8 = ["#EXTM3U"]
    for name, vid in CHANNELS.items():
        url = get_hls_url(vid)
        m3u8.append(f'#EXTINF:-1 tvg-id="{name}",{name}')
        m3u8.append(url if url else "https://example.com/fallback.mp4")
    
    with open("youtube_1080p.m3u8", "w") as f:
        f.write("\n".join(m3u8))

if __name__ == "__main__":
    generate_m3u8()
    print(f"Updated at {datetime.now()}")