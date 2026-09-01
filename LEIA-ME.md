# Site do Centro Médico Osório — publicação e manutenção

Site estático, sem dependência de servidor. Basta subir os arquivos.

---

## 1. Antes de publicar: quatro trocas obrigatórias

### 1.1 Link de avaliação do Google
Em `avaliacao/index.html`, procure por `SEU_PLACE_ID` e troque pelo link direto de avaliação.
Onde obter: no painel do Perfil da Empresa no Google, opção de pedir avaliações. O link já abre a janela com as estrelas prontas, o que aumenta muito a conclusão no celular.

### 1.2 Domínio: por enquanto, nenhum

O site não declara endereço nenhum. Não há canonical, não há og:url e não há sitemap.xml.
Isso é proposital: apontar o Google para um endereço que ainda não existe é pior que não apontar para nada. O site funciona normalmente assim, em qualquer lugar onde for hospedado.

Quando o domínio estiver registrado e apontado, rode uma vez, dentro da pasta do site:

```bash
python3 definir-dominio.py https://clinicaosorio.com.br
```

O script insere canonical e og:url em cada página, deixa a imagem de compartilhamento com endereço absoluto (é o que faz a pré-visualização aparecer no WhatsApp), completa os dados estruturados e gera o sitemap.xml e o robots.txt. Depois é só enviar o sitemap no Search Console.

O mesmo script serve para o endereço provisório do GitHub Pages, caso você queira que o site já seja indexado antes do domínio:

```bash
python3 definir-dominio.py https://usuario.github.io/clinicaosorio
```

Nesse caso não há prejuízo na troca depois: quando você define um domínio próprio, o GitHub passa a redirecionar o endereço antigo para o novo, e basta rodar o script de novo com o endereço definitivo.

Enquanto não houver endereço definido, a pré-visualização do link no WhatsApp não mostra imagem. Isso se resolve sozinho quando o script rodar.

### 1.3 Coordenadas do mapa
No bloco de dados estruturados de cada página há `latitude` e `longitude` aproximadas do Edifício Wawel.
Confirme o ponto exato no Google Maps (clique no local, copie as coordenadas) e substitua:

```bash
grep -rl '"latitude":-25.4306' . | xargs sed -i 's|"latitude":-25.4306,"longitude":-49.2733|"latitude":LAT,"longitude":LON|g'
```

### 1.4 Especialidade do RQE
Confirme no portal do CRM-PR a qual especialidade corresponde o RQE 5109 e escreva-a ao lado do registro na página do médico. Enquanto não confirmar, o site anuncia apenas procedimentos e condições, o que já está correto do ponto de vista da Resolução CFM 1.974/2011.

---

## 2. Publicar no GitHub Pages

```bash
git init
git add .
git commit -m "Site do Centro Médico Osório"
git branch -M main
git remote add origin git@github.com:USUARIO/REPOSITORIO.git
git push -u origin main
```

Depois: Settings, Pages, Source: branch `main`, pasta `/ (root)`.

O arquivo `.nojekyll` já está incluso e evita que o GitHub processe as pastas.

### Domínio próprio (registro.br)

1. No registro.br, aponte para o GitHub Pages:
   - Quatro registros A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Um CNAME `www` apontando para `USUARIO.github.io`
2. Em Settings, Pages, Custom domain, informe o domínio. O GitHub cria o arquivo `CNAME` no repositório. Nunca apague esse arquivo em envios futuros.
3. Marque "Enforce HTTPS" depois que o certificado for emitido.
4. Registre o domínio no CPF do Dr. Omar ou no CNPJ da clínica, não em nome de terceiro.

### Atenção aos caminhos

Todos os endereços internos são relativos, então o site funciona aberto direto do computador (clicando no index.html), em subpasta de repositório do tipo `usuario.github.io/clinicaosorio/` e em domínio próprio, sem nenhum ajuste.

O `canonical`, o Open Graph e o `sitemap.xml` continuam apontando para o domínio final, que é o correto para o Google.

---

## 3. Depois de publicar

1. Google Search Console: adicionar a propriedade, verificar por registro TXT no registro.br, enviar `sitemap.xml`.
2. Perfil da Empresa no Google: conferir se nome, endereço e telefone estão idênticos aos do site, letra por letra. Acrescentar o endereço do site.
3. Perfis MedPrev e Doctoralia: completar e incluir o link do site.
4. Testar os dados estruturados em `search.google.com/test/rich-results`.
5. Compartilhar o link em uma conversa de WhatsApp para conferir se a imagem de pré-visualização aparece.

---

## 4. Botão de WhatsApp

Ainda não existe número confirmado, então a barra fixa do celular usa Ligar e Como chegar.
Quando o número existir, edite `assets/site.js`? Não: os botões estão no HTML de todas as páginas. Rode:

```bash
grep -rl 'class="zap"' . | xargs sed -i 's|<a class="zap" href="[^"]*" target="_blank" rel="noopener">|<a class="zap" href="https://wa.me/5541999999999?text=Ol%C3%A1%2C%20gostaria%20de%20agendar" target="_blank" rel="noopener">|'
```

Trocando `5541999999999` pelo número real, com 55 na frente e sem espaços. Troque também o texto do botão de "Como chegar" para "WhatsApp".

---

## 5. Como acrescentar coisas

### Um novo médico
Abra `corpo-clinico/index.html`. Há um bloco comentado com o modelo pronto: copie, troque os dados, descomente. Cada profissional precisa do próprio CRM e do próprio RQE, e só pode ter anunciada a especialidade que tiver RQE registrado.

### Um novo convênio
Abra `convenios/index.html` e acrescente na lista. Quando a lista estiver completa, remova o parágrafo em itálico que avisa que ela está sendo atualizada.

### Um novo artigo
Duplique a pasta `artigos/gastrite-enantematosa-leve-antro/`, renomeie, troque o conteúdo e:
1. acrescente o item na lista em `artigos/index.html`;
2. acrescente a URL no `sitemap.xml`;
3. atualize o `canonical`, o `og:url` e o bloco de dados estruturados no topo do arquivo novo;
4. reenvie o sitemap no Search Console e peça a indexação da URL nova.

O bloco de laudo é o elemento de assinatura do site. A estrutura é:

```html
<div class="laudo">
  <div class="laudo__rot">TRECHO DO LAUDO</div>
  <div class="laudo__corpo">texto do laudo, com as quebras de linha reais</div>
</div>
<p class="traducao">Em português claro: ...</p>
```

---

## 6. Regras de conteúdo que não podem ser violadas

- Rodapé com nome, CRM e RQE em todas as páginas. Já está automático.
- Sem depoimento de paciente reproduzido dentro do site.
- Sem imagem de paciente real, sem antes e depois.
- Sem superlativo: nada de melhor, referência, excelência.
- Sem promessa de resultado. Benefício e limite sempre juntos.
- Nada oferecido em troca de avaliação.

---

## 7. Estrutura dos arquivos

```
index.html                      Home
endoscopia/                     Serviço principal
endoscopia/preparo/             Preparo, com a ferramenta de horários
cirurgia-ambulatorial/          Serviço
consultas/                      Serviço
corpo-clinico/                  Lista de médicos
corpo-clinico/dr-omar-.../      Perfil e dados estruturados do médico
artigos/                        Índice
artigos/gastrite-.../           Primeiro artigo
convenios/  contato/  avaliacao/  privacidade/
404.html  sitemap.xml  robots.txt  .nojekyll
assets/site.css                 Folha de estilo única
assets/site.js                  Menu, contato, copiar endereço, ferramenta de preparo
assets/                         Imagens em WebP com alternativa JPG ou PNG
```

Paleta: `--tinta #0E2148`, `--azul #1B58A6`, `--agua #2BB3CE`, `--papel #F6F9FB`.
Regra da casa: o turquesa é cor de ação. Botão, link de contato, foco de teclado. Nunca decoração, nunca título.

Tipografia: Newsreader nos títulos, Public Sans no corpo, corpo em 18 pixels.

---

## 8. Pendências conhecidas

- Logos vieram de arquivo com fundo branco; o recorte foi feito automaticamente. Se conseguir os originais em SVG ou PNG com transparência, substitua em `assets/`.
- A marca vertical com o wordmark veio de captura de tela em baixa resolução e por isso não foi usada no site, apenas o símbolo. Com o arquivo original, ela pode entrar no rodapé.
- Horário de atendimento não informado: a página de contato mostra "confirme por telefone".
- Fotos que faltam e que teriam mais impacto: o médico sentado no consultório em conversa, e a sala de endoscopia com o equipamento, sem paciente.
