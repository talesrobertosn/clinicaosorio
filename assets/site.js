/* Centro Médico Osório — comportamento
   Movimento só como resposta a uma ação de quem usa. */
(function () {
  "use strict";

  // menu no celular
  var botao = document.querySelector(".hamb");
  var nav = document.getElementById("nav");
  if (botao && nav) {
    botao.addEventListener("click", function () {
      var aberto = nav.getAttribute("data-aberto") === "1";
      nav.setAttribute("data-aberto", aberto ? "0" : "1");
      botao.setAttribute("aria-expanded", aberto ? "false" : "true");
    });
  }

  // contato flutuante no desktop
  var flutua = document.querySelector(".flutua");
  if (flutua) {
    var alvo = flutua.querySelector(".flutua__btn");
    var fecha = function () { flutua.setAttribute("data-aberto", "0"); };
    alvo.addEventListener("click", function (e) {
      e.stopPropagation();
      flutua.setAttribute("data-aberto", flutua.getAttribute("data-aberto") === "1" ? "0" : "1");
    });
    document.addEventListener("click", fecha);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") fecha(); });
    flutua.querySelector(".flutua__p").addEventListener("click", function (e) { e.stopPropagation(); });
  }

  // copiar endereço
  Array.prototype.forEach.call(document.querySelectorAll("[data-copiar]"), function (b) {
    b.addEventListener("click", function () {
      var texto = b.getAttribute("data-copiar");
      var pronto = function () {
        var antes = b.textContent;
        b.textContent = "Endereço copiado";
        setTimeout(function () { b.textContent = antes; }, 2200);
      };
      if (navigator.clipboard) {
        navigator.clipboard.writeText(texto).then(pronto, pronto);
      } else {
        var c = document.createElement("textarea");
        c.value = texto; document.body.appendChild(c); c.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(c); pronto();
      }
    });
  });

  // checklist do dia do exame, guardado no próprio aparelho
  var lista = document.querySelector(".checklist");
  if (lista) {
    Array.prototype.forEach.call(lista.querySelectorAll("input[type=checkbox]"), function (c) {
      var chave = "cmo-check-" + c.value;
      try { if (localStorage.getItem(chave) === "1") c.checked = true; } catch (e) {}
      c.addEventListener("change", function () {
        try { localStorage.setItem(chave, c.checked ? "1" : "0"); } catch (e) {}
      });
    });
  }

  // ferramenta de preparo: monta o cronograma do paciente
  var form = document.getElementById("preparo");
  if (form) {
    var saida = document.getElementById("cronograma");
    var linhas = document.getElementById("crono-linhas");
    var titulo = document.getElementById("crono-titulo");

    var fmt = function (d) {
      var dias = ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"];
      var hh = ("0" + d.getHours()).slice(-2), mm = ("0" + d.getMinutes()).slice(-2);
      return dias[d.getDay()] + ", dia " + d.getDate() + ", às " + hh + "h" + mm;
    };

    var montar = function () {
      var data = document.getElementById("data-exame").value;
      var hora = document.getElementById("hora-exame").value;
      if (!data || !hora) { return; }
      var p = data.split("-"), h = hora.split(":");
      var exame = new Date(+p[0], p[1] - 1, +p[2], +h[0], +h[1]);
      if (isNaN(exame.getTime())) { return; }

      var passo = function (horas, texto) {
        return { q: new Date(exame.getTime() - horas * 3600000), t: texto };
      };
      var itens = [
        passo(12, "A partir daqui, prefira comida leve. Evite fritura, gordura e bebida alcoólica."),
        passo(8, "Última refeição. Depois deste horário, nada de comida, leite, bala ou chiclete. Água ainda é permitida."),
        passo(4, "Pare a água. A partir deste horário, jejum completo."),
        passo(1, "Chegue à clínica, com documento, carteirinha do convênio e o pedido médico em mãos."),
        { q: exame, t: "Horário do exame." }
      ];

      linhas.innerHTML = "";
      itens.forEach(function (i) {
        var li = document.createElement("li");
        var t = document.createElement("time");
        t.dateTime = i.q.toISOString();
        t.textContent = fmt(i.q);
        var s = document.createElement("span");
        s.textContent = i.t;
        li.appendChild(t); li.appendChild(s); linhas.appendChild(li);
      });
      titulo.textContent = "Seu preparo para o exame de " + fmt(exame);
      saida.classList.remove("oculto");
      saida.setAttribute("tabindex", "-1");
      saida.focus({ preventScroll: false });
    };

    form.addEventListener("submit", function (e) { e.preventDefault(); montar(); });
  }
})();
