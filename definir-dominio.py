# -*- coding: utf-8 -*-
"""Liga o site a um endereço definitivo.

Enquanto não há domínio, o site não declara endereço nenhum: sem canonical,
sem og:url e sem sitemap. Isso evita apontar o Google para um endereço que
ainda não existe.

Quando o domínio estiver registrado e apontado, rode uma vez:

    python3 definir-dominio.py https://clinicaosorio.com.br

Também serve para o endereço provisório do GitHub Pages, se você quiser que o
site seja indexado antes do domínio:

    python3 definir-dominio.py https://usuario.github.io/clinicaosorio

O script insere canonical e og:url em cada página, deixa a imagem de
compartilhamento com endereço absoluto (é o que faz a pré-visualização
aparecer no WhatsApp), preenche os dados estruturados e gera o sitemap.xml
e o robots.txt. Pode ser rodado de novo se o endereço mudar.
"""
import os, re, sys, datetime

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

BASE = sys.argv[1].rstrip("/")
RAIZ = os.path.dirname(os.path.abspath(__file__))

PRIO = {"/": "1.0", "/endoscopia/": "0.9", "/cirurgia-ambulatorial/": "0.9",
        "/endoscopia/preparo/": "0.8", "/contato/": "0.7",
        "/artigos/gastrite-enantematosa-leve-antro/": "0.8"}

urls = []

for pasta, _, arquivos in os.walk(RAIZ):
    for nome in sorted(arquivos):
        if not nome.endswith(".html"):
            continue
        caminho = os.path.join(pasta, nome)
        rel = os.path.relpath(caminho, RAIZ).replace(os.sep, "/")
        if rel == "404.html":
            url_pagina = BASE + "/404.html"
        elif rel == "index.html":
            url_pagina = BASE + "/"
        elif rel.endswith("/index.html"):
            url_pagina = BASE + "/" + rel[:-len("index.html")]
        else:
            url_pagina = BASE + "/" + rel

        t = open(caminho, encoding="utf-8").read()

        # limpa o que já existir, para poder rodar de novo
        t = re.sub(r'\n<link rel="canonical"[^>]*>', "", t)
        t = re.sub(r'\n<meta property="og:url"[^>]*>', "", t)
        t = re.sub(r'<meta property="og:image" content="[^"]*">',
                   '<meta property="og:image" content="%s/assets/og-centro-medico-osorio.jpg">' % BASE, t)

        t = t.replace('<meta name="robots"',
                      '<link rel="canonical" href="%s">\n<meta name="robots"' % url_pagina, 1)
        t = t.replace('<meta property="og:image"',
                      '<meta property="og:url" content="%s">\n<meta property="og:image"' % url_pagina, 1)

        # dados estruturados: troca os identificadores relativos por absolutos
        t = re.sub(r'("(?:@id|url|image|logo)":")(/[^"]*)"',
                   lambda m: m.group(1) + BASE + m.group(2) + '"', t)

        open(caminho, "w", encoding="utf-8").write(t)
        if rel != "404.html":
            urls.append(url_pagina)
        print("ajustado:", rel)

hoje = datetime.date.today().isoformat()
linhas = "".join(
    "  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n"
    % (u, hoje, PRIO.get(u[len(BASE):] or "/", "0.6")) for u in sorted(urls))
open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % linhas)
open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

print("\nEndereço definido:", BASE)
print("sitemap.xml e robots.txt gerados com %d páginas." % len(urls))
print("Agora envie o sitemap no Google Search Console.")
