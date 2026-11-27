/* Sampa Educacional — Formulário de matrícula (/pos/matricula?curso=<slug>)
 * Grava a matrícula no Sampa-Core (tabela edu.matriculas; a chave publicável só permite INSERT,
 * nunca leitura) e redireciona para o link Asaas do curso configurado em /pos/pos.js (CHECKOUT).
 * Cada envio dispara o e-mail de aviso (gatilho on_matricula_insert → edge function edu-notify-lead).
 */
(function () {
  'use strict';

  var SUPABASE_URL = 'https://bwzojcgptaitbhxrhoap.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_UIZBu703Kc42COX9dqtgQA_06V6-oxY';
  var DATA = window.SAMPA_MATRICULA || { courses: {}, price: {} };

  var form = document.getElementById('matricula-form');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var sel = $('fcurso'), cpf = $('fcpf'), cep = $('fcep'), wa = $('fwa'), phone = $('fphone');
  var errBox = $('form-err'), btn = $('fsubmit'), btnLabel = btn.textContent;

  var digits = function (v) { return String(v || '').replace(/\D/g, ''); };

  // ── Máscaras ──
  function maskCPF(v) {
    v = digits(v).slice(0, 11);
    return v.replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  }
  function maskCEP(v) { v = digits(v).slice(0, 8); return v.length > 5 ? v.slice(0, 5) + '-' + v.slice(5) : v; }
  function maskPhone(v) {
    v = digits(v).slice(0, 11);
    if (v.length <= 2) return v;
    if (v.length <= 6) return '(' + v.slice(0, 2) + ') ' + v.slice(2);
    if (v.length <= 10) return '(' + v.slice(0, 2) + ') ' + v.slice(2, 6) + '-' + v.slice(6);
    return '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
  }
  cpf.addEventListener('input', function () { cpf.value = maskCPF(cpf.value); $('fcpf-err').hidden = true; });
  cep.addEventListener('input', function () { cep.value = maskCEP(cep.value); $('fcep-err').hidden = true; });
  [wa, phone].forEach(function (el) { el.addEventListener('input', function () { el.value = maskPhone(el.value); }); });

  // ── Validação de CPF (dígitos verificadores) ──
  function validCPF(v) {
    v = digits(v);
    if (v.length !== 11 || /^(\d)\1{10}$/.test(v)) return false;
    for (var t = 9; t < 11; t++) {
      var s = 0;
      for (var i = 0; i < t; i++) s += Number(v[i]) * (t + 1 - i);
      var d = ((10 * s) % 11) % 10;
      if (d !== Number(v[t])) return false;
    }
    return true;
  }

  // ── Curso escolhido ──
  function courseInfo() { return DATA.courses[sel.value] || null; }
  function renderCourse() {
    var c = courseInfo(), price = $('curso-preco');
    $('curso-nome').textContent = c ? c.name : 'Selecione o curso no formulário';
    $('curso-link').href = c ? c.page : '/pos/black-november';
    if (c && c.price && DATA.price.por) {
      var sp = window.SampaPos, camp = sp ? sp.campanha() : '', ate = sp ? sp.prazo() : DATA.price.deadline;
      if (sp && !sp.promoActive()) {
        price.textContent = 'A condição promocional terminou. A equipe confirma os valores atuais após o envio.';
      } else {
        price.textContent = (c.from === false ? 'Condição ' + camp + ': ' : 'De ' + DATA.price.de + ' por ') +
          DATA.price.por + ' à vista ou ' + DATA.price.parc + ', até ' + ate + '.';
      }
    } else if (c) {
      price.textContent = 'A condição Black November deste curso é confirmada pela equipe após o envio.';
    } else {
      price.textContent = '';
    }
    if (c && window.history && history.replaceState) {
      history.replaceState(null, '', '/pos/matricula?curso=' + encodeURIComponent(sel.value));
    }
  }
  var pre = new URLSearchParams(location.search).get('curso');
  if (pre && DATA.courses[pre]) sel.value = pre;
  sel.addEventListener('change', renderCourse);
  renderCourse();

  function showError(msg, focusEl) {
    errBox.textContent = msg; errBox.hidden = false;
    if (focusEl) focusEl.focus();
  }

  function val(name) {
    var el = form.elements[name];
    if (!el) return null;
    var v = String(el.value || '').trim();
    return v === '' ? null : v.slice(0, 2000);
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    errBox.hidden = true;

    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (!validCPF(cpf.value)) { $('fcpf-err').hidden = false; cpf.focus(); return; }
    if (digits(cep.value).length !== 8) { $('fcep-err').hidden = false; cep.focus(); return; }
    if (!$('fconsent').checked) { showError('Aceite a Política de Privacidade para continuar.', $('fconsent')); return; }

    var c = courseInfo();
    var matricula = {
      curso_slug: sel.value,
      curso: c.name,
      name: val('name'),
      dob: val('dob'),
      cpf: digits(cpf.value),
      email: val('email'),
      phone: val('phone'),
      whatsapp: val('whatsapp'),
      cep: digits(cep.value),
      formation: val('formacao'),
      vip_extra: val('vip_extra'),
      user_agent: navigator.userAgent.slice(0, 500),
      source: (location.hostname || 'sampaedu.com') + '/pos/matricula'
    };

    btn.disabled = true;
    btn.textContent = 'Enviando…';
    try {
      var res = await fetch(SUPABASE_URL + '/rest/v1/matriculas', {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY,
          'Content-Type': 'application/json',
          'Content-Profile': 'edu',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify(matricula)
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
    } catch (err) {
      console.error('Falha ao enviar matrícula:', err);
      btn.disabled = false;
      btn.textContent = btnLabel;
      showError('Não foi possível enviar agora. Tente novamente ou fale conosco pelo WhatsApp.');
      return;
    }

    var checkout = window.SampaPos && window.SampaPos.checkoutFor(sel.value);
    if (checkout) {
      btn.textContent = 'Indo para o pagamento…';
      window.location.href = checkout;
      return;
    }

    // Sem link Asaas configurado: confirma o recebimento e oferece o WhatsApp
    form.hidden = true;
    $('success-curso').textContent = c.name;
    $('success-wa').href = 'https://wa.me/' + DATA.wa + '?text=' + encodeURIComponent(
      'Olá! Acabei de preencher a matrícula da pós-graduação em ' + c.name +
      (window.SampaPos && window.SampaPos.campanha() ? ' (' + window.SampaPos.campanha() + ')' : '') +
      '. Pode me enviar o link de pagamento?');
    var ok = $('success');
    ok.hidden = false;
    requestAnimationFrame(function () { ok.focus(); });
  });
})();
