#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dlyoutube.py
============
โปรแกรมสำหรับดาวน์โหลดวิดีโอจาก YouTube

วิธีใช้งาน:
    1. ติดตั้งไลบรารีที่จำเป็นก่อน:
         pip install yt-dlp
    2. รันโปรแกรม:
         python dlyoutube.py
    3. ใส่ลิงก์ YouTube ที่ต้องการดาวน์โหลดตามที่โปรแกรมถาม

ไลบรารีที่ใช้:
    - yt_dlp : ไลบรารีสำหรับดาวน์โหลดวิดีโอจาก YouTube และเว็บไซต์อื่น ๆ
      (เป็นเวอร์ชันที่พัฒนาต่อจาก pytube/youtube-dl และดูแลรักษาอย่างต่อเนื่อง
       รองรับการเปลี่ยนแปลงโครงสร้างเว็บ YouTube ได้ดีกว่า)
"""

import os
import sys

try:
    import yt_dlp
except ImportError:
    # กรณียังไม่ได้ติดตั้งไลบรารี ให้แจ้งผู้ใช้แล้วจบโปรแกรม
    print("ไม่พบไลบรารี yt-dlp กรุณาติดตั้งก่อนด้วยคำสั่ง: pip install yt-dlp")
    sys.exit(1)


def download_video(url: str, output_path: str = "downloads", audio_only: bool = False) -> None:
    """
    ฟังก์ชันหลักสำหรับดาวน์โหลดวิดีโอ (หรือเสียง) จาก YouTube

    พารามิเตอร์:
        url (str)         : ลิงก์วิดีโอ YouTube ที่ต้องการดาวน์โหลด
        output_path (str) : โฟลเดอร์ปลายทางที่จะเก็บไฟล์ที่ดาวน์โหลด (ค่าเริ่มต้น "downloads")
        audio_only (bool) : ถ้าเป็น True จะดาวน์โหลดเฉพาะเสียง (แปลงเป็น mp3)
                             ถ้าเป็น False จะดาวน์โหลดวิดีโอแบบเต็ม (ค่าเริ่มต้น)
    """

    # สร้างโฟลเดอร์ปลายทางถ้ายังไม่มี
    os.makedirs(output_path, exist_ok=True)

    # ตั้งค่า (options) ให้ yt-dlp ใช้ในการดาวน์โหลด
    # extractor_args: ระบุให้ yt-dlp ดึงข้อมูลผ่าน "android client"
    # ช่วยแก้ปัญหา HTTP Error 403: Forbidden ที่เกิดจาก YouTube
    # เปลี่ยนวิธีตรวจสอบสิทธิ์การเข้าถึงไฟล์วิดีโอบ่อย ๆ
    extractor_args = {"youtube": {"player_client": ["android"]}}

    if audio_only:
        # กรณีต้องการเฉพาะไฟล์เสียง (mp3)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "extractor_args": extractor_args,
        }
    else:
        # กรณีต้องการวิดีโอแบบเต็ม (คุณภาพดีที่สุดที่มี)
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "extractor_args": extractor_args,
        }

    # เริ่มกระบวนการดาวน์โหลดโดยใช้ context manager ของ yt_dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"กำลังดึงข้อมูลวิดีโอจาก: {url}")
            info = ydl.extract_info(url, download=True)  # download=True คือให้ดาวน์โหลดจริง
            title = info.get("title", "ไม่ทราบชื่อวิดีโอ")
            print(f"ดาวน์โหลดสำเร็จ: {title}")
            print(f"ไฟล์ถูกบันทึกไว้ที่โฟลเดอร์: {os.path.abspath(output_path)}")
        except yt_dlp.utils.DownloadError as e:
            # ดักจับข้อผิดพลาดที่เกิดจากการดาวน์โหลด เช่น ลิงก์ผิด หรือวิดีโอถูกลบ/ตั้งค่าเป็นส่วนตัว
            print(f"เกิดข้อผิดพลาดในการดาวน์โหลด: {e}")


def main():
    """
    ฟังก์ชันหลักของโปรแกรม
    ทำหน้าที่รับค่าจากผู้ใช้ผ่านทาง command line (input)
    แล้วเรียกใช้ฟังก์ชัน download_video()
    """
    print("=== โปรแกรมดาวน์โหลดวิดีโอ YouTube ===")

    # รับลิงก์วิดีโอจากผู้ใช้
    url = input("กรุณาใส่ลิงก์วิดีโอ YouTube: ").strip()

    if not url:
        print("ไม่ได้ใส่ลิงก์ กรุณาลองใหม่อีกครั้ง")
        return

    # ถามผู้ใช้ว่าต้องการดาวน์โหลดแบบวิดีโอ หรือเฉพาะเสียง
    choice = input("ต้องการดาวน์โหลดแบบใด? (1=วิดีโอ, 2=เฉพาะเสียง mp3) [ค่าเริ่มต้น 1]: ").strip()
    audio_only = (choice == "2")

    # เรียกใช้ฟังก์ชันดาวน์โหลด
    download_video(url, output_path="downloads", audio_only=audio_only)


# จุดเริ่มต้นของโปรแกรม
# บรรทัดนี้จะทำงานก็ต่อเมื่อไฟล์นี้ถูกรันโดยตรง (ไม่ใช่ถูก import ไปใช้ในไฟล์อื่น)
if __name__ == "__main__":
    main()