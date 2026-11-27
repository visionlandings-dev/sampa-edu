/* Sampa Educacional — Pós-graduações
 *
 * 1) CHECKOUT_PADRAO: link de pagamento Asaas único da campanha (Pix à vista ou cartão
 *    em até 12x sem juros, R$ 1.327,50), usado por todos os cursos.
 *    CHECKOUT: opcional — link próprio de um curso; quando preenchido, tem prioridade.
 *    Fluxo: botão "Quero me matricular" → /pos/matricula?curso=<slug> → formulário
 *    → lead salvo no Sampa-Core (edu.leads) → redirecionamento para o link abaixo.
 *    Enquanto o link estiver vazio, o formulário salva o lead e avisa que a equipe
 *    envia o link de pagamento pelo WhatsApp ou e-mail.
 * 2) PROMO_END: prazo da Black November. Depois dele, os blocos .js-promo somem e
 *    aparecem os avisos .js-ended.
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

  var PROMO_END = new Date('2026-11-30T23:59:59-03:00');

  window.SampaPos = {
    checkoutFor: function (slug) {
      var ok = function (u) { return u && /^https:\/\//.test(u); };
      if (ok(CHECKOUT[slug])) return CHECKOUT[slug];
      return ok(CHECKOUT_PADRAO) ? CHECKOUT_PADRAO : '';
    },
    promoActive: function () { return Date.now() < PROMO_END.getTime(); }
  };

  function tick() {
    var ms = PROMO_END - Date.now();
    if (ms <= 0) { document.body.classList.add('pp-ended'); return false; }
    var d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60;
    var txt = (d > 0 ? d + 'd ' : '') + h + 'h ' + (m < 10 ? '0' : '') + m + 'min';
    document.querySelectorAll('[data-countdown]').forEach(function (el) { el.textContent = txt; });
    return true;
  }
  if (tick()) { var t = setInterval(function () { if (!tick()) clearInterval(t); }, 30000); }
})();
