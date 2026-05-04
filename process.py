  import os
import subprocess
import gdown
import requests
import urllib.parse

# دریافت لینک از متغیرهای محیطی گیت‌هاب اکشنز
url = os.environ.get("FILE_URL")

def download_file(url):
    # تشخیص لینک گوگل درایو
    if "drive.google.com" in url or "docs.google.com" in url:
        print("لینک گوگل درایو شناسایی شد. در حال دانلود...")
        # fuzzy=True برای پشتیبانی از فرمت‌های مختلف لینک درایو
        output = gdown.download(url, quiet=False, fuzzy=True)
        return output
    else:
        print("لینک مستقیم شناسایی شد. در حال دانلود...")
        parsed = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = "downloaded_file.dat"
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return filename

if __name__ == "__main__":
    if not url:
        print("هیچ لینکی وارد نشده است.")
        exit(1)
    
    filename = download_file(url)
    
    if filename and os.path.exists(filename):
        print(f"فایل {filename} دانلود شد. در حال پارت‌بندی (هر پارت 45 مگابایت)...")
        
        # پارت‌بندی با دستور split لینوکس
        prefix = f"{filename}_part_"
        subprocess.run(["split", "-b", "45M", filename, prefix])
        
        # حذف فایل اصلی برای جلوگیری از ارور محدودیت 100 مگابایتی گیت‌هاب
        os.remove(filename)
        print("پارت‌بندی تمام شد و فایل اصلی حذف گردید.")
    else:
        print("خطا در دانلود فایل.")
        exit(1)
