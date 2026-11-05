#!/usr/bin/env python3
"""Run: python CEK_UNDUHAN.py http://server-anda/folder/"""
import hashlib,json,sys,urllib.request,urllib.parse
from pathlib import Path
if len(sys.argv)!=2:
    raise SystemExit('Cara pakai: python CEK_UNDUHAN.py http://server-anda/folder/')
base=sys.argv[1].rstrip('/')+'/'
if urllib.parse.urlsplit(base).scheme not in ('http','https'):
    raise SystemExit('Gunakan alamat HTTP atau HTTPS.')
items=json.loads(Path(__file__).with_name('file-manifest.json').read_text())
failed=False
for item in items:
    url=urllib.parse.urljoin(base,item['file'])
    try:
        h=hashlib.sha256();size=0
        with urllib.request.urlopen(url,timeout=60) as response:
            content_type=response.headers.get('Content-Type','')
            while True:
                chunk=response.read(1024*1024)
                if not chunk:break
                h.update(chunk);size+=len(chunk)
        ok=size==item['bytes'] and h.hexdigest()==item['sha256']
        print(('PASS' if ok else 'GAGAL'),item['file'],size,'byte',content_type)
        if 'text/html' in content_type.lower():
            print('PERINGATAN: server mengirim tipe HTML, periksa proteksi hosting/konfigurasi MIME.');ok=False
        if not ok:failed=True
    except Exception as exc:
        failed=True;print('GAGAL',item['file'],str(exc))
print('Unduhan cocok dengan sumber. Uji PS3 masih diperlukan.' if not failed else 'Jangan gunakan file gagal; perbaiki hosting/alamat lalu periksa lagi.')
sys.exit(1 if failed else 0)
