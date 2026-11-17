#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert Eve vs The Suits page JPEGs to optimized WebP for the site.

Same approach as comics 1 and 2: RGB WebP, quality=82, method=6, native
1190×1785 (already the site size; comic 1 was 2× from smaller raws).
Ignores ref-gry-*.jpg and any non p-NN files.

Default source: /workspace/eve-komiks3/pages/<lang>/p-NN.jpg
Default dest:   <repo>/assets/komiks3/<lang>/p-NN.webp

To add pages 7–11 later:
  1. Drop p-07.jpg … p-11.jpg into /workspace/eve-komiks3/pages/<lang>/
  2. python3 scripts/convert_komiks3.py
  3. Rebuild (python3 scripts/build.py). The page list is scanned from
     assets/komiks3/<lang>/p-NN.webp, so no count change is needed.
"""
import glob, os, re, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DEFAULT = '/workspace/eve-komiks3/pages'
DEST_REL = 'assets/komiks3'
PAGE_RE = re.compile(r'^p-(\d+)\.(jpe?g|png|webp)$', re.I)
LANGS = ['pl', 'en', 'es', 'pt', 'it', 'ja', 'zh']
QUALITY = 82
METHOD = 6

def convert_one(src, dest):
    im = Image.open(src).convert('RGB')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, 'WEBP', quality=QUALITY, method=METHOD)
    return im.size, os.path.getsize(src), os.path.getsize(dest)

def main():
    src_root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else SRC_DEFAULT)
    dest_root = os.path.join(ROOT, DEST_REL)
    n = 0
    for lang in LANGS:
        d = os.path.join(src_root, lang)
        if not os.path.isdir(d):
            print(f'skip {lang}: no {d}')
            continue
        for path in sorted(glob.glob(os.path.join(d, '*'))):
            name = os.path.basename(path)
            if name.lower().startswith('ref-'):
                continue
            m = PAGE_RE.match(name)
            if not m:
                continue
            dest = os.path.join(dest_root, lang, f'p-{int(m.group(1)):02d}.webp')
            size, a, b = convert_one(path, dest)
            print(f'{lang}/{os.path.basename(dest)}  {size[0]}×{size[1]}  {a/1024:.0f}KB → {b/1024:.0f}KB')
            n += 1
    print(f'OK: {n} pages → {dest_root}')

if __name__ == '__main__':
    main()
