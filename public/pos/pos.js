/* Sampa Educacional — Pós-graduações
 * 1) CHECKOUT: cole aqui o link Asaas de cada curso. Enquanto estiver vazio,
 *    o botão continua em "Consultar matrícula" (WhatsApp com o nome do curso).
 * 2) Prazo da Black November: depois de PROMO_END, os blocos de preço
 *    promocional (.js-promo) somem e aparece o aviso (.js-ended).
 * Ao editar, troque o ?v= nos <script src="/pos/pos.js?v=..."> (cache imutável da Vercel).
 */
(function () {
  'use strict';

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

  // Checkout por curso
  document.querySelectorAll('a[data-checkout]').forEach(function (a) {
    var url = CHECKOUT[a.getAttribute('data-checkout')];
    if (url && /^https:\/\//.test(url)) {
      a.href = url;
      a.removeAttribute('target');
      a.textContent = a.getAttribute('data-label-checkout') || 'Quero me matricular';
    }
  });

  // Prazo
  var root = document.documentElement;
  function tick() {
    var ms = PROMO_END - Date.now();
    if (ms <= 0) { document.body.classList.add('pp-ended'); return false; }
    var d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60;
    var txt = (d > 0 ? d + 'd ' : '') + h + 'h ' + (m < 10 ? '0' : '') + m + 'min';
    document.querySelectorAll('[data-countdown]').forEach(function (el) { el.textContent = txt; });
    return true;
  }
  if (tick()) { var t = setInterval(function () { if (!tick()) clearInterval(t); }, 30000); }
  root.classList.add('js');
})();
