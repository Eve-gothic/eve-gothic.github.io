#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generuje skórki wyglądu strony: css/themes/<motyw>.css  (motywy wybierane w panelu „Eve Admin” → content/theme.json).

Skórka = SAM CSS na istniejącym HTML (blog, komiksy, gry, 9 języków i PWA działają bez zmian). Ładowana PO css/eve.css.
Każdy plik powstaje z dwóch części:
  1) „remap” — wygenerowany z css/eve.css: wszystkie deklaracje z na sztywno wpisanymi kolorami (złoto, burgund, kremowe teksty)
     i fontami przepisane na zmienne CSS (--gold, --ink, --paper, --soft, --f-head, --f-body, --f-ui …), dzięki czemu skórka
     zmienia wygląd całej strony samym ustawieniem zmiennych;
  2) część ręczna scripts/themes/<motyw>.css — zmienne motywu + dopracowanie (tła, zaokrąglenia, efekty).
Uruchom po zmianie css/eve.css albo scripts/themes/*.css:   python3 scripts/make_themes.py   (nie jest częścią build.py)."""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
THEMES = ['neon', 'luksus', 'minimal', 'creator']

def split_blocks(css):
    """-> lista (prelude, body) na poziomie najwyższym; komentarze usunięte."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, depth, start, pre = [], 0, 0, ''
    i = 0
    for i, ch in enumerate(css):
        if ch == '{':
            if depth == 0: pre = css[start:i].strip(); start = i + 1
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: out.append((pre, css[start:i])); start = i + 1
        elif ch == ';' and depth == 0:   # @import / @charset
            start = i + 1
    return out

def decls(body):
    out, cur, par = [], '', 0
    for ch in body:
        if ch == '(': par += 1
        elif ch == ')': par -= 1
        if ch == ';' and par == 0: out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return [d for d in out if d]

def mix(var, a):
    a = float(a)
    return f'var({var})' if a >= 1 else f'color-mix(in srgb,var({var}) {round(a * 100, 1):g}%,transparent)'

RGBA = {'201,163,91': '--gold', '185,168,154': '--mut', '243,236,224': '--paper', '58,11,22': '--bur', '92,18,36': '--bur2', '12,7,8': '--ink', '6,3,4': '--ink'}
HEX = {'#e9dccb': 'var(--soft)', '#e2d4c3': 'var(--soft)', '#efe3d2': 'var(--soft)', '#f6e7d0': 'var(--soft)', '#fff': 'var(--paper)',
       '#f3ece0': 'var(--paper)', '#3a0b16': 'var(--bur)', '#0c0708': 'var(--ink)'}
def remap(d):
    n = d
    n = re.sub(r'rgba\((\d+),(\d+),(\d+),([\d.]+)\)', lambda m: mix(RGBA[f'{m[1]},{m[2]},{m[3]}'], m[4]) if f'{m[1]},{m[2]},{m[3]}' in RGBA else m[0], n)
    n = re.sub(r'#[0-9a-fA-F]{3,6}\b', lambda m: HEX.get(m[0].lower(), m[0]), n)
    if n.startswith('font-family'):
        n = re.sub(r'"Playfair Display"', 'var(--f-head)', n)
        n = re.sub(r'"Cormorant Garamond"', 'var(--f-body)', n)
        n = re.sub(r'(?<![\w-])Inter(?![\w-])', 'var(--f-ui)', n)
    return n

def remap_rules(blocks):
    out = []
    for pre, body in blocks:
        if pre.startswith('@media'):
            inner = remap_rules(split_blocks(body))
            if inner: out.append(f'{pre}{{{"".join(inner)}}}')
        elif pre.startswith('@'):
            continue   # @keyframes, @font-face — bez zmian
        elif pre.strip() == ':root':
            continue
        else:
            ch = [remap(d) for d in decls(body) if remap(d) != d]
            if ch: out.append(f'{pre}{{{";".join(ch)}}}')
    return out

def main():
    css = open(os.path.join(ROOT, 'css', 'eve.css'), encoding='utf-8').read()
    remapped = '\n'.join(remap_rules(split_blocks(css))) + '\n'
    os.makedirs(os.path.join(ROOT, 'css', 'themes'), exist_ok=True)
    for t in THEMES:
        src = os.path.join(ROOT, 'scripts', 'themes', t + '.css')
        hand = open(src, encoding='utf-8').read() if os.path.exists(src) else ''
        head = (f'/* Skórka „{t}” — GENEROWANA przez scripts/make_themes.py (część ręczna: scripts/themes/{t}.css). Nie edytuj tego pliku ręcznie. */\n')
        # zmienne motywu (część ręczna zaczyna się blokiem :root) muszą być przed „remap”, reszta ręczna po nim
        m = re.match(r'(\s*/\*.*?\*/\s*)?(:root\{.*?\}\s*)', hand, re.S)
        root_part, rest = (m.group(2), hand[m.end():]) if m else ('', hand)
        out = head + root_part + '/* --- remap eve.css na zmienne --- */\n' + remapped + '/* --- dopracowanie motywu --- */\n' + rest
        open(os.path.join(ROOT, 'css', 'themes', t + '.css'), 'w', encoding='utf-8').write(out)
        print(f'css/themes/{t}.css: {len(out) // 1024} KB')

if __name__ == '__main__':
    main()
