GitHub 自动化解决方案，包含：

自动生成 1080P M3U8 的 Python 脚本

GitHub Actions 定时自动更新

托管到 GitHub Pages 实现永久访问链接

完整方案部署步骤
1. 创建 GitHub 仓库
bash
gh repo create youtube-1080p-proxy --public --clone
cd youtube-1080p-proxy
2. 添加核心文件
📂 文件结构
text
.
├── .github/workflows/update.yml    # 自动化脚本
├── proxy.py                       # 主程序
├── requirements.txt               # 依赖
└── README.md
📜 proxy.py
python
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
⚙️ .github/workflows/update.yml
yaml
name: Update M3U8

on:
  schedule:
    - cron: '0 */4 * * *'  # 每4小时运行一次
  workflow_dispatch:        # 支持手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install yt-dlp
          sudo apt-get install -y jq
      
      - name: Run proxy generator
        run: |
          python proxy.py
          cat youtube_1080p.m3u8
      
      - name: Commit changes
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add youtube_1080p.m3u8
          git commit -m "Auto-update M3U8 $(date +'%Y-%m-%d %H:%M')" || true
          git push
📝 requirements.txt
text
yt-dlp>=2023.11.16
3. 启用 GitHub Pages
仓库设置 → Pages → 选择 main 分支作为源

访问地址：https://[你的用户名].github.io/youtube-1080p-proxy/youtube_1080p.m3u8

🔍 工作原理
每4小时自动运行：GitHub Actions 定时执行脚本

动态获取最新 HLS：通过 yt-dlp 获取实时 1080P 流地址

自动提交更新：将新生成的 M3U8 文件提交回仓库

永久访问链接：通过 GitHub Pages 提供稳定访问

📌 高级配置（可选）
1. 添加监控通知
在 update.yml 中添加：

yaml
      - name: Notify on failure
        if: failure()
        uses: actions/telegram@v1
        with:
          token: ${{ secrets.TELEGRAM_TOKEN }}
          chat_id: ${{ secrets.TELEGRAM_CHAT_ID }}
          text: "YouTube 1080P 更新失败！"
2. 使用 Docker 增强稳定性
创建 Dockerfile：

dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y jq
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "proxy.py"]
3. 多 CDN 备用源
修改 get_hls_url() 函数：

python
def get_hls_url(video_id):
    cdn_servers = [
        "rr1---sn-4g5ednsl.googlevideo.com",
        "rr2---sn-4g5ednsl.googlevideo.com",
        "rr3---sn-4g5ednsl.googlevideo.com"
    ]
    for cdn in cdn_servers:
        try:
            cmd = f'yt-dlp -f "best[height=1080]" --get-url "https://youtu.be/{video_id}" --proxy "https://{cdn}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            continue
    return None
💡 使用建议
本地测试：先手动运行 python proxy.py 测试

查看日志：在仓库 Actions 标签页监控执行情况

自定义频道：修改 CHANNELS 字典即可增减频道

⚠️ 注意：YouTube 可能会限制频繁请求，建议不要设置短于2小时的更新间隔
