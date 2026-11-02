#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deploy strony Eve na Cloudflare (Worker ze statycznymi plikami „eve-gothic”, adres: patrz SITE w build.py).

Bez zależności (tylko Python 3). Dwa tryby:

A) Z tokenem API (np. GitHub Actions, sekret CLOUDFLARE_API_TOKEN z uprawnieniem „Workers Scripts: Edit”):
     CLOUDFLARE_API_TOKEN=… python3 scripts/deploy_cf.py deploy
B) Agent z MCP Cloudflare (bez tokena na dysku) — 3 kroki, opis w BLOG.md:
     python3 scripts/deploy_cf.py manifest            # -> /tmp/eve-cf/manifest.json (wklej do MCP: assets-upload-session)
     python3 scripts/deploy_cf.py upload <JWT> '<buckets-json>'   # wysyła brakujące pliki, wypisuje completion JWT
     (potem MCP: PUT skryptu z assets.jwt = completion JWT)
"""
import os, sys, json, hashlib, base64, mimetypes, urllib.request, uuid

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '208efe56d8d17e7137cd7bdfa74346cf')
WORKER = os.environ.get('EVE_WORKER', 'eve-gothic')
API = 'https://api.cloudflare.com/client/v4'
SKIP_DIRS = {'.git', '.github', 'scripts', '__pycache__', 'node_modules', 'posts'}   # blog/posts = źródła .md
SKIP_FILES = {'BLOG.md', 'README.md', '.gitignore', '.nojekyll', '.assetsignore', 'wrangler.jsonc'}
ASSETS_CONFIG = {'html_handling': 'auto-trailing-slash', 'not_found_handling': 'none'}
COMPAT_DATE = '2026-10-01'
mimetypes.add_type('image/webp', '.webp'); mimetypes.add_type('video/webm', '.webm'); mimetypes.add_type('application/rss+xml', '.xml')

def files():
    out = {}
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith('.'))
        for f in sorted(fs):
            if f in SKIP_FILES or f.startswith('.') or f.endswith('.pyc'): continue
            full = os.path.join(d, f); rel = '/' + os.path.relpath(full, ROOT).replace(os.sep, '/')
            out[rel] = full
    return out

def manifest():
    m, by_hash = {}, {}
    for rel, full in files().items():
        data = open(full, 'rb').read(); ext = os.path.splitext(rel)[1][1:]
        h = hashlib.sha256(base64.b64encode(data) + ext.encode()).hexdigest()[:32]
        m[rel] = {'hash': h, 'size': len(data)}; by_hash[h] = rel
    return m, by_hash

def ctype(rel):
    if rel.endswith('sitemap.xml'): return 'application/xml'
    return (mimetypes.guess_type(rel)[0] or 'application/octet-stream') + ('; charset=utf-8' if rel.endswith(('.html', '.css', '.js', '.xml', '.txt', '.svg')) else '')

def req(method, url, token, body=None, ctype_hdr=None):
    r = urllib.request.Request(url, data=body, method=method, headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'eve-deploy/1'})
    if ctype_hdr: r.add_header('Content-Type', ctype_hdr)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp: return json.loads(resp.read() or b'{}')
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code} {method} {url}: {e.read().decode(errors="replace")[:800]}')

def multipart(parts):
    b = uuid.uuid4().hex; out = b''
    for name, value, ct, fn in parts:
        out += f'--{b}\r\nContent-Disposition: form-data; name="{name}"'.encode() + (f'; filename="{fn}"'.encode() if fn else b'') + f'\r\nContent-Type: {ct}\r\n\r\n'.encode() + value + b'\r\n'
    return out + f'--{b}--\r\n'.encode(), f'multipart/form-data; boundary={b}'

def upload(jwt, buckets, by_hash):
    done = jwt
    for i, bucket in enumerate(buckets, 1):
        parts = [(h, base64.b64encode(open(os.path.join(ROOT, by_hash[h][1:]), 'rb').read()), ctype(by_hash[h]), None) for h in bucket]
        body, ct = multipart(parts)
        r = req('POST', f'{API}/accounts/{ACCOUNT_ID}/workers/assets/upload?base64=true', jwt, body, ct)
        print(f'  paczka {i}/{len(buckets)}: {len(bucket)} plików', file=sys.stderr)
        if (r.get('result') or {}).get('jwt'): done = r['result']['jwt']
    return done

def put_worker(token, completion_jwt):
    meta = {'compatibility_date': COMPAT_DATE, 'assets': {'jwt': completion_jwt, 'config': ASSETS_CONFIG}}
    body, ct = multipart([('metadata', json.dumps(meta).encode(), 'application/json', None)])
    req('PUT', f'{API}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER}', token, body, ct)
    req('POST', f'{API}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER}/subdomain', token,
        json.dumps({'enabled': True, 'previews_enabled': False}).encode(), 'application/json')

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'deploy'
    m, by_hash = manifest()
    if cmd == 'manifest':
        os.makedirs('/tmp/eve-cf', exist_ok=True)
        json.dump(m, open('/tmp/eve-cf/manifest.json', 'w'), separators=(',', ':'))
        print(f'/tmp/eve-cf/manifest.json ({len(m)} plików)')
    elif cmd == 'upload':
        print(upload(sys.argv[2], json.loads(sys.argv[3]), by_hash))
    elif cmd == 'deploy':
        token = os.environ.get('CLOUDFLARE_API_TOKEN') or sys.exit('Brak CLOUDFLARE_API_TOKEN (albo użyj trybu MCP z BLOG.md).')
        r = req('POST', f'{API}/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER}/assets-upload-session', token,
                json.dumps({'manifest': m}).encode(), 'application/json')['result']
        print(f'{len(m)} plików, do wysłania: {sum(len(b) for b in r.get("buckets") or [])}')
        put_worker(token, upload(r['jwt'], r.get('buckets') or [], by_hash))
        print('OK: wdrożono', WORKER)
    else: sys.exit(__doc__)

if __name__ == '__main__': main()
