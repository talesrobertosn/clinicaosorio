# Site do Centro Médico Osório

Site estático. Todas as páginas ficam soltas na raiz, sem subpastas: a única pasta é `assets`, com imagens, folha de estilo e script.

---

## 1. Subir no GitHub, pelo navegador

1. Crie um repositório novo.
2. Clique em "Add file", "Upload files".
3. Arraste tudo de uma vez: os arquivos `.html`, o `robots.txt`, o `.nojekyll` e a pasta `assets` inteira. O GitHub aceita arrastar a pasta e mantém a estrutura.
4. Commit.
5. Em Settings, Pages, escolha branch `main` e pasta `/ (root)`.

O arquivo `.nojekyll` já está incluso e evita que o GitHub processe os arquivos.

Os caminhos são relativos, então o site funciona aberto direto do computador, em subpasta de repositório e em domínio próprio, sem ajuste nenhum.

---

## 2. Antes de divulgar: três trocas

### 2.1 Link de avaliação do Google — aplicado, mas dá para melhorar

Os botões "Avaliar no Google" (na home e em `avaliacao.html`) usam hoje o link curto do perfil: `https://share.google/lWadXp8W3LIXvR18x`. Funciona: abre o perfil, e de lá a pessoa avalia.

O ideal é o link direto de avaliação, que já abre a janela com as cinco estrelas prontas. Cada toque a menos aumenta bastante a taxa de conclusão no celular. Como obter:

- Depois de reivindicar o perfil: no painel do Perfil da Empresa, opção de pedir avaliações. Ele entrega o link pronto.
- Sem reivindicar: abra o perfil no computador, clique em Escrever avaliação e copie o endereço que aparece na barra do navegador.

Quando tiver esse link, troque nas duas páginas:

```bash
grep -rl "share.google/lWadXp8W3LIXvR18x" . | xargs sed -i 's|https://share.google/lWadXp8W3LIXvR18x|SEU_LINK_DIRETO|g'
```

### 2.2 Coordenadas do mapa
Os dados estruturados usam coordenadas aproximadas do Edifício Wawel. Confirme no Google Maps (clique no local, copie as coordenadas) e substitua:

```bash
grep -rl '"latitude":-25.4306' . | xargs sed -i 's|"latitude":-25.4306,"longitude":-49.2733|"latitude":LAT,"longitude":LON|g'
```

### 2.3 Endereço do site — já aplicado

O site já está apontado para `https://centromedicosorio.com.br`. Canonical, og:url, imagem de compartilhamento, dados estruturados, `sitemap.xml` e `robots.txt` estão todos com esse endereço, e o arquivo `CNAME` já vem pronto no pacote.

Se o domínio registrado for outro, rode uma vez dentro da pasta e edite o CNAME:

```bash
python3 definir-dominio.py https://ODOMINIOCERTO.com.br
echo "odominiocerto.com.br" > CNAME
```

## 3. Domínio próprio (registro.br)

1. Registros A apontando para: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
2. CNAME `www` apontando para `usuario.github.io`
3. Settings, Pages, Custom domain: informe `centromedicosorio.com.br`. O arquivo `CNAME` já está no pacote; nunca apague em envios futuros.
4. Marque "Enforce HTTPS" quando o certificado sair.
5. Registre o domínio no CPF do Dr. Omar ou no CNPJ da clínica.

---

## 4. Depois de publicar

1. Search Console: adicionar a propriedade, verificar por TXT no registro.br, enviar o sitemap.
2. Perfil da Empresa no Google: nome, endereço e telefone idênticos aos do site, letra por letra. Acrescentar o endereço do site.
3. MedPrev e Doctoralia: completar e incluir o link do site.
4. Testar os dados estruturados em `search.google.com/test/rich-results`.
5. QR code na recepção apontando para `avaliacao.html`.

---

## 5. Botão de WhatsApp

Os botões de WhatsApp já estão no site: no topo da página inicial, na barra fixa do celular, no painel flutuante do computador, na página de contato e em todas as faixas de agendamento. Só falta o número.

Todos apontam para `https://wa.me/55SEUNUMERO`. Assim que tiver o número, rode uma vez, dentro da pasta:

```bash
grep -rl "55SEUNUMERO" . | xargs sed -i 's|55SEUNUMERO|5541999999999|g'
```

Trocando `5541999999999` pelo número real, com o 55 na frente, DDD, e sem espaços, traços ou parênteses.

Enquanto não trocar, o botão leva a uma página de erro do WhatsApp. Ou você troca antes de divulgar, ou remove os botões.

## 6. Como acrescentar coisas

### Um novo médico
Duplique o bloco `.medico` de `dr-omar.html` para uma página nova, por exemplo `dra-fulana.html`, e acrescente um cartão em `index.html`. Cada profissional precisa do próprio CRM e do próprio RQE, e só pode ter anunciada a especialidade que tiver RQE registrado no Conselho.

### Um novo convênio
`convenios.html`, na lista. Quando a lista estiver completa, apague o parágrafo em itálico que avisa que ela está sendo atualizada.

### Um novo texto de dúvida
1. Duplique `unha-encravada.html` e troque o conteúdo.
2. Acrescente o cartão em `duvidas.html` e, se for importante, em `index.html`. O padrão do cartão é:

```html
<a class="duvida duvida--2" href="ARQUIVO.html">
  <div><em>Categoria</em><b>Título chamativo</b><span>Uma linha de resumo.</span></div>
  <span class="ler">Ler agora</span>
</a>
```

As variações `duvida--1` a `duvida--4` mudam só a cor do fundo.

3. Rode `definir-dominio.py` de novo para atualizar o sitemap, e peça a indexação no Search Console.

### O bloco de laudo
É o elemento de assinatura do site, usado nas páginas que traduzem achados de exame:

```html
<div class="laudo">
  <div class="laudo__r">TRECHO DO LAUDO</div>
  <div class="laudo__c">texto do laudo, com as quebras de linha reais</div>
</div>
<p class="traducao">Em português claro: ...</p>
```

---

## 7. Regras de conteúdo que não podem ser violadas

- Rodapé com nome, CRM e RQE em todas as páginas. Já é automático.
- Sem depoimento de paciente reproduzido dentro do site.
- Sem imagem de paciente real, sem antes e depois.
- Sem superlativo: nada de melhor, referência, excelência.
- Sem promessa de resultado. Benefício e limite sempre juntos.
- Nada oferecido em troca de avaliação.
- A clínica atende clínica e cirurgia geral de modo amplo; endoscopia e cirurgia ambulatorial são os focos, mas o site não fecha o atendimento nesses dois.
- Só se anuncia a especialidade com RQE registrado. O RQE 5109 é de Cirurgia Geral, e é assim que aparece no site. Os demais assuntos aparecem como procedimentos e condições atendidas, o que é permitido e captura a busca do mesmo jeito.

---

## 8. Design

Paleta: `--tinta #0A1E42` (azul-noite), `--azul #17549C`, `--agua #2FB4CF` (turquesa), `--papel #F3F7FB`, `--ambar #E0A03C` (só nas estrelas de avaliação).

Regra da casa: o turquesa é cor de ação. Botão, link de contato, foco de teclado. Nunca decoração, nunca título.

Tipografia: Fraunces nos títulos, Manrope no corpo, texto em 18,5 pixels, entrelinha 1,75.

Fotos ficam dentro de molduras em arco (`.arco`), com anel turquesa deslocado atrás.

Tudo em um arquivo só: `assets/site.css`.

---

## 9. Páginas

```
index.html                   Home
endoscopia.html              Serviço
preparo-endoscopia.html      Preparo, com a ferramenta de horários
cirurgia-ambulatorial.html   Serviço
consultas.html               Serviço
dr-omar.html                 Perfil do médico
duvidas.html                 Índice dos textos
azia-e-queimacao.html        Texto
gastrite-no-laudo.html       Texto, com o bloco de laudo
unha-encravada.html          Texto
caroco-na-pele.html          Texto
convenios.html  contato.html  avaliacao.html  privacidade.html  404.html
robots.txt  .nojekyll  definir-dominio.py
assets/                      imagens, site.css, site.js
```

---

## 10. Pendências

- Horário de atendimento não informado: a página de contato mostra "confirme por telefone".
- Lista completa de convênios.
- Número de WhatsApp.
- Logos: vieram com fundo branco e o recorte foi automático. Com os originais em SVG ou PNG transparente, é só substituir em `assets`.
- Fotos que fariam diferença: o médico sentado no consultório em conversa, e a sala de endoscopia com o equipamento, sem paciente.
