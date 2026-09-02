# -*- coding: utf-8 -*-
"""Liga o site a um endereço definitivo.

Enquanto não há domínio, o site não declara endereço nenhum: sem canonical,
sem og:url e sem sitemap. Isso evita apontar o Google para um endereço que
ainda não existe.

Quando o domínio estiver registrado e apontado, rode uma vez, dentro da pasta
do site:

    python3 definir-dominio.py https://clinicaosorio.com.br

Também serve para o endereço provisório do GitHub Pages:

    python3 definir-dominio.py https://usuario.github.io/clinicaosorio

O script insere canonical e og:url em cada página, deixa a imagem de
compartilhamento com endereço absoluto (é o que faz a pré-visualização
aparecer no WhatsApp), completa os dados estruturados e gera o sitemap.xml
e o robots.txt. Pode ser rodado de novo se o endereço mudar.
"""
import os, re, sys, datetime, glob

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)

BASE = sys.argv[1].rstrip("/")
RAIZ = os.path.dirname(os.path.abspath(__file__))
PRIO = {"index.html": "1.0", "endoscopia.html": "0.9", "cirurgia-ambulatorial.html": "0.9",
        "preparo-endoscopia.html": "0.8", "gastrite-no-laudo.html": "0.8",
        "azia-e-queimacao.html": "0.8", "unha-encravada.html": "0.8",
        "caroco-na-pele.html": "0.8", "contato.html": "0.7", "dr-omar.html": "0.7"}
urls = []

for caminho in sorted(glob.glob(os.path.join(RAIZ, "*.html"))):
    nome = os.path.basename(caminho)
    url = BASE + "/" if nome == "index.html" else BASE + "/" + nome
    t = open(caminho, encoding="utf-8").read()

    t = re.sub(r'\n<link rel="canonical"[^>]*>', "", t)
    t = re.sub(r'\n<meta property="og:url"[^>]*>', "", t)
    t = re.sub(r'<meta property="og:image" content="[^"]*">',
               '<meta property="og:image" content="%s/assets/og-centro-medico-osorio.jpg">' % BASE, t)
    t = t.replace('<meta name="robots"', '<link rel="canonical" href="%s">\n<meta name="robots"' % url, 1)
    t = t.replace('<meta property="og:image"', '<meta property="og:url" content="%s">\n<meta property="og:image"' % url, 1)
    t = re.sub(r'("(?:@id|url|image|logo)":")(/[^"]*)"', lambda m: m.group(1) + BASE + m.group(2) + '"', t)

    open(caminho, "w", encoding="utf-8").write(t)
    if nome != "404.html":
        urls.append((nome, url))
    print("ajustado:", nome)

hoje = datetime.date.today().isoformat()
linhas = "".join("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n"
                 % (u, hoje, PRIO.get(n, "0.6")) for n, u in urls)
open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % linhas)
open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)
print("\nEndereço definido: %s\nsitemap.xml e robots.txt gerados com %d páginas." % (BASE, len(urls)))
