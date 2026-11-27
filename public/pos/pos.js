/* Sampa Educacional — Pós-graduações
 *
 * 1) CHECKOUT_PADRAO: link de pagamento Asaas único da campanha (Pix à vista ou cartão
 *    em até 12x sem juros, R$ 1.327,50), usado por todos os cursos.
 *    CHECKOUT: opcional — link próprio de um curso; quando preenchido, tem prioridade.
 *    Fluxo: botão "Quero me matricular" → /pos/matricula?curso=<slug> → formulário
 *    → lead salvo no Sampa-Core (edu.leads) → redirecionamento para o link abaixo.
 *    Enquanto o link estiver vazio, o formulário salva o lead e avisa que a equipe
 *    envia o link de pagamento pelo WhatsApp ou e-mail.
 * 2) HOTMART: link de pagamento Hotmart de cada produto (canal Hotmart, páginas /hotmart/<curso>).
 *    Enquanto o link estiver vazio, o botão aparece como "Inscrições em breve" e não leva a lugar nenhum.
 * 3) FASES: campanhas em sequência, com as mesmas condições comerciais. A página mostra
 *    o nome e o prazo da fase vigente (elementos [data-campanha], [data-prazo],
 *    [data-prazo-curto], [data-countdown]). Depois do fim da última fase, os blocos
 *    .js-promo somem e aparecem os avisos .js-ended.
 *    Para mudar nome, prazo ou acrescentar uma fase, edite só a lista FASES.
 *
 * Ao editar, troque o ?v= nos <script src="/pos/pos.js?v=..."> (cache imutável da Vercel).
 */
(function () {
  'use strict';

  var CHECKOUT_PADRAO = '';

  var CHECKOUT = {
    'educacao-especial-e-inclusiva': '',
    'neuropsicopedagogia': '',
    'mba-licitacoes-publicas': '',
    'processos-cognitivos-e-aprendizagem': '',
    'administracao-de-pessoal': '',
    'treinamento-e-desenvolvimento': '',
    'psicologia-nas-organizacoes': '',
    'lideranca-nas-organizacoes': '',
    'gestao-estrategica-de-pessoas': '',
    'inteligencia-de-mercado': '',
    'gestao-estrategica-de-vendas': '',
    'gestao-em-administracao-e-marketing': '',
    'sistemas-de-informacoes-gerenciais': '',
    'governanca-corporativa-e-compliance': '',
    'gestao-financeira-e-contabil': ''
  };

  var HOTMART = {
    'educacao-especial-e-inclusiva': '',
    'neuropsicopedagogia': '',
    'mba-licitacoes-publicas': '',
    'processos-cognitivos-e-aprendizagem': '',
    'administracao-de-pessoal': '',
    'treinamento-e-desenvolvimento': '',
    'psicologia-nas-organizacoes': '',
    'lideranca-nas-organizacoes': '',
    'gestao-estrategica-de-pessoas': '',
    'inteligencia-de-mercado': '',
    'gestao-estrategica-de-vendas': '',
    'gestao-em-administracao-e-marketing': '',
    'sistemas-de-informacoes-gerenciais': '',
    'governanca-corporativa-e-compliance': '',
    'gestao-financeira-e-contabil': ''
  };

  var FASES = [
    { nome: 'Black November', fim: '2026-11-30T23:59:59-03:00' },
    { nome: 'Black December', fim: '2026-12-15T23:59:59-03:00' }
  ];

  function faseAtual() {
    var agora = Date.now();
    for (var i = 0; i < FASES.length; i++) {
      if (agora < new Date(FASES[i].fim).getTime()) return FASES[i];
    }
    return null;
  }
  function prazo(f, curto) {
    var d = new Date(new Date(f.fim).getTime() - 3 * 36e5); // horário de Brasília
    var dd = ('0' + d.getUTCDate()).slice(-2), mm = ('0' + (d.getUTCMonth() + 1)).slice(-2);
    return curto ? dd + '/' + mm : dd + '/' + mm + '/' + d.getUTCFullYear();
  }

  window.SampaPos = {
    checkoutFor: function (slug) {
      var ok = function (u) { return u && /^https:\/\//.test(u); };
      if (ok(CHECKOUT[slug])) return CHECKOUT[slug];
      return ok(CHECKOUT_PADRAO) ? CHECKOUT_PADRAO : '';
    },
    promoActive: function () { return !!faseAtual(); },
    campanha: function () { var f = faseAtual(); return f ? f.nome : ''; },
    prazo: function () { var f = faseAtual(); return f ? prazo(f) : ''; }
  };

  // Canal Hotmart: aponta os botões de compra para o link de pagamento do produto
  document.querySelectorAll('a[data-hotmart]').forEach(function (a) {
    var url = HOTMART[a.getAttribute('data-hotmart')];
    if (url && /^https:\/\//.test(url)) {
      a.href = url;
    } else {
      a.removeAttribute('href');
      a.setAttribute('aria-disabled', 'true');
      a.classList.add('pp-btn--off');
      a.textContent = 'Inscrições em breve';
    }
  });

  // Nome e prazo da fase vigente
  function aplicaFase() {
    var f = faseAtual();
    if (!f) { document.body.classList.add('pp-ended'); return null; }
    document.querySelectorAll('[data-campanha]').forEach(function (el) { el.textContent = f.nome; });
    document.querySelectorAll('[data-prazo]').forEach(function (el) { el.textContent = prazo(f); });
    document.querySelectorAll('[data-prazo-curto]').forEach(function (el) { el.textContent = prazo(f, true); });
    return f;
  }
  function tick() {
    var f = aplicaFase();
    if (!f) return false;
    var ms = new Date(f.fim).getTime() - Date.now();
    var d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60;
    var txt = (d > 0 ? d + 'd ' : '') + h + 'h ' + (m < 10 ? '0' : '') + m + 'min';
    document.querySelectorAll('[data-countdown]').forEach(function (el) { el.textContent = txt; });
    return true;
  }
  if (tick()) { var t = setInterval(function () { if (!tick()) clearInterval(t); }, 30000); }
})();
