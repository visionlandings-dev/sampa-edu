#!/usr/bin/env python3
"""Gera as páginas estáticas de pós-graduação em public/pos/.

Uso:  python3 scripts/build_pos.py
Os dados dos cursos ficam neste arquivo; o HTML gerado é o que vai para a Vercel.
Links de checkout NÃO ficam aqui: são configurados em public/pos/pos.js.
"""
from html import escape
from pathlib import Path
from urllib.parse import quote
import json

ROOT = Path(__file__).resolve().parent.parent / "public" / "pos"
SITE = "https://sampaedu.com"
WA = "5511967992285"
GRADE_URL = "https://sampagroup.pvunypublica.com.br/curso/{}"
ASSET_V = "20261127"
DEADLINE_ISO = "2026-11-30T23:59:59-03:00"
DEADLINE_TXT = "30/11/2026"

# Condição Black November das especializações de 360h (dados da Sampa)
BLACK = {"de": "R$ 1.770,00", "por": "R$ 1.327,50", "por_num": "1327.50",
         "parc": "12x R$ 110,63 sem juros no cartão de crédito", "off": "25% OFF"}
SHOW_PRICE_360 = True  # mude para False para ocultar preço/prazo nas páginas

BENEFITS = [
    "100% online",
    "Acesso à plataforma liberado logo após a confirmação da matrícula",
    "TCC opcional (Resolução MEC)",
    "Certificado registrado no MEC",
    "Suporte com tutores especializados",
    "Material didático incluso (PDFs e vídeos)",
]
TRUST = ["Compra segura", "7 dias de garantia", "Faculdade nota 4 no MEC"]

SMALL = {"de", "da", "do", "das", "dos", "e", "em", "a", "o", "à", "ao", "na", "no",
         "nas", "nos", "para", "por", "com", "as", "os"}
KEEP = {"ESG", "RH", "MEC", "TCC", "(ESG)"}


def tc(s: str) -> str:
    out = []
    for i, w in enumerate(s.split()):
        if w in KEEP:
            out.append(w)
        elif i and w.lower() in SMALL:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    r = " ".join(out)
    return r.replace("- ", "– ")


def g(*names):
    return [tc(n) for n in names]


COURSES_12 = [
    # área, slug, nome, id, grade (9 x 40h)
    ("aprendizagem", "processos-cognitivos-e-aprendizagem", "Processos Cognitivos e Aprendizagem", 1444, g(
        "TRANSTORNOS E DISTÚRBIOS DA APRENDIZAGEM", "PROCESSOS COGNITIVOS E APRENDIZAGEM",
        "AVALIAÇÃO DA APRENDIZAGEM", "PSICOLOGIA DA APRENDIZAGEM",
        "DESENVOLVIMENTO NEUROPSICOMOTOR E DA APRENDIZAGEM", "PSICOLOGIA DO DESENVOLVIMENTO",
        "NEUROPSICOPEDAGOGIA CLÍNICA", "NEUROCIÊNCIAS DO COMPORTAMENTO",
        "NEUROCIÊNCIAS E AS PRÁTICAS PEDAGÓGICAS")),
    ("pessoas", "administracao-de-pessoal", "Administração de Pessoal", 964, g(
        "SEGURANÇA, MEIO AMBIENTE, SAÚDE E RESPONSABILIDADE SOCIAL", "DIVISÃO E MODELAGEM DE CARGOS E SALÁRIOS",
        "ADMINISTRAÇÃO FINANCEIRA E CONTÁBIL", "GESTÃO DE DEPARTAMENTO PESSOAL",
        "PLANEJAMENTO E CONTROLADORIA FINANCEIRA", "DIREITO DO TRABALHO E DA PREVIDÊNCIA",
        "SISTEMAS DE INFORMAÇÕES GERENCIAIS EM RH", "SEGURANÇA DO TRABALHO E SAÚDE OCUPACIONAL",
        "GOVERNANÇA CORPORATIVA, CONTROLE INTERNO E COMPLIANCE")),
    ("pessoas", "treinamento-e-desenvolvimento", "Treinamento e Desenvolvimento", 3385, g(
        "TREINAMENTO E DESENVOLVIMENTO", "GESTÃO DE TIMES - MÉTODOS ÁGEIS", "CULTURA E CLIMA ORGANIZACIONAL",
        "GESTÃO DO CONHECIMENTO E APRENDIZAGEM ORGANIZACIONAL", "CULTURA DIGITAL PARA O MUNDO DO TRABALHO",
        "DINÂMICAS DE GRUPO E PROGRAMAS DE DESENVOLVIMENTO INDIVIDUAL", "LIDERANÇA E DESENVOLVIMENTO DE EQUIPES",
        "AVALIAÇÃO DE DESEMPENHO DE PESSOAS", "COACHING E PLANEJAMENTO DE CARREIRAS")),
    ("pessoas", "psicologia-nas-organizacoes", "Psicologia nas Organizações", 1453, g(
        "COMUNICAÇÃO EMPRESARIAL", "PSICOLOGIA DO DESENVOLVIMENTO", "CULTURA E CLIMA ORGANIZACIONAL",
        "GESTÃO DE DEPARTAMENTO PESSOAL", "PSICOLOGIA SOCIAL", "FILOSOFIA E ÉTICA PROFISSIONAL",
        "LIDERANÇA E DESENVOLVIMENTO DE EQUIPES", "CONSULTORIA ORGANIZACIONAL", "EMPREENDEDORISMO")),
    ("pessoas", "lideranca-nas-organizacoes", "Liderança nas Organizações", 1283, g(
        "FUNDAMENTOS DA ADMINISTRAÇÃO", "CONSULTORIA ORGANIZACIONAL", "COMUNICAÇÃO EMPRESARIAL",
        "GESTÃO DE RECURSOS HUMANOS", "GESTÃO DE DEPARTAMENTO PESSOAL", "LIDERANÇA E DESENVOLVIMENTO DE EQUIPES",
        "LIDERANÇA E GESTÃO DE EQUIPES", "COMPETÊNCIAS GERENCIAIS", "PSICOLOGIA DOS GRUPOS")),
    ("pessoas", "gestao-estrategica-de-pessoas", "Gestão Estratégica de Pessoas", 1245, g(
        "ESTRATÉGIAS DE GESTÃO E ORGANIZAÇÃO EMPRESARIAL", "GESTÃO DE DEPARTAMENTO PESSOAL",
        "LEGISLAÇÃO E NORMAS TÉCNICAS DE ACESSIBILIDADE", "PSICOLOGIA DOS GRUPOS", "GESTÃO DE RECURSOS HUMANOS",
        "RECRUTAMENTO, SELEÇÃO E SOCIALIZAÇÃO", "TREINAMENTO E DESENVOLVIMENTO",
        "ANÁLISE DE MERCADO: TENDÊNCIA, COMPORTAMENTO E MOVIMENTO", "LIDERANÇA E DESENVOLVIMENTO DE EQUIPES")),
    ("marketing", "inteligencia-de-mercado", "Inteligência de Mercado", 1276, g(
        "GESTÃO DE DEPARTAMENTO PESSOAL", "ANÁLISE DE MERCADO: TENDÊNCIA, COMPORTAMENTO E MOVIMENTO",
        "GESTÃO DO CONHECIMENTO E APRENDIZAGEM ORGANIZACIONAL", "GESTÃO DE SERVIÇOS", "ESTRATÉGIAS DE MARKETING",
        "ANÁLISE E MODELAGEM DE PROCESSOS", "ESTRATÉGIAS DE GROWTH MARKETING",
        "GOVERNANÇA CORPORATIVA, CONTROLE INTERNO E COMPLIANCE", "INOVAÇÃO E TECNOLOGIA APLICADAS AO MARKETING")),
    ("marketing", "gestao-estrategica-de-vendas", "Gestão Estratégica de Vendas", 1250, g(
        "ESTRATÉGIAS DE GESTÃO E ORGANIZAÇÃO EMPRESARIAL", "EMPREENDEDORISMO", "TÉCNICAS DE VENDAS",
        "MARKETING DE RELACIONAMENTO, PÓS-VENDA E FIDELIZAÇÃO DE CLIENTES", "GESTÃO DE COMPRAS E NEGOCIAÇÃO",
        "FORMAÇÃO DE PREÇOS", "ANÁLISE E PESQUISA DE MERCADO", "LIDERANÇA E DESENVOLVIMENTO DE EQUIPES",
        "GESTÃO DE CUSTOS E FINANÇAS")),
    ("marketing", "gestao-em-administracao-e-marketing", "Gestão em Administração e Marketing", 1225, g(
        "ESTRATÉGIAS DE GESTÃO E ORGANIZAÇÃO EMPRESARIAL", "EMPREENDEDORISMO", "FUNDAMENTOS DA ADMINISTRAÇÃO",
        "FUNDAMENTOS DE MARKETING", "ESTRATÉGIAS DE MARKETING", "CIÊNCIA DE DADOS APLICADA À GESTÃO DE MARKETING",
        "GESTÃO DE PROJETOS", "ESTRATÉGIAS DE NEGÓCIOS", "SISTEMA DE INFORMAÇÕES DE MARKETING")),
    ("gestao", "sistemas-de-informacoes-gerenciais", "Sistemas de Informações Gerenciais", 1476, g(
        "IMPLANTAÇÃO E ADMINISTRAÇÃO DE SISTEMAS DE INFORMAÇÃO", "PLANEJAMENTO ESTRATÉGICO DE TECNOLOGIA DA INFORMAÇÃO",
        "ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES", "TECNOLOGIAS E LINGUAGENS DE BANCO DE DADOS",
        "LÓGICA DE PROGRAMAÇÃO", "ESTRUTURA DE DADOS", "ENGENHARIA DE SOFTWARE", "SISTEMAS DE INFORMAÇÕES GERENCIAIS",
        "GESTÃO DA TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO")),
    ("gestao", "governanca-corporativa-e-compliance", "Governança Corporativa e Compliance", 1264, g(
        "ESTRATÉGIAS DE GESTÃO E ORGANIZAÇÃO EMPRESARIAL", "FUNDAMENTOS DO DIREITO",
        "GOVERNANÇA CORPORATIVA, CONTROLE INTERNO E COMPLIANCE", "DIREITO EMPRESARIAL", "DIREITO CIVIL",
        "ÉTICA E CIDADANIA", "SUSTENTABILIDADE AMBIENTAL, SOCIAL E GOVERNANÇA (ESG)",
        "COMPLIANCE E CONTROLE NA ADMINISTRAÇÃO PÚBLICA", "PLANEJAMENTO E CONTROLADORIA FINANCEIRA")),
    ("gestao", "gestao-financeira-e-contabil", "Gestão Financeira e Contábil", 1255, g(
        "ESTRATÉGIAS DE GESTÃO E ORGANIZAÇÃO EMPRESARIAL", "EMPREENDEDORISMO", "FUNDAMENTOS CONTÁBEIS",
        "PLANEJAMENTO ESTRATÉGICO", "TEORIAS CONTÁBEIS", "FINANÇAS CORPORATIVAS",
        "ANÁLISE DAS DEMONSTRAÇÕES CONTÁBEIS", "ANÁLISE E DEMONSTRAÇÃO FINANCEIRA E BANCÁRIA", "CONTABILIDADE DE CUSTOS")),
]

AREAS = [
    ("aprendizagem", "Aprendizagem", "Cognição, desenvolvimento e práticas pedagógicas."),
    ("pessoas", "Pessoas e liderança", "RH, desenvolvimento humano e gestão de equipes."),
    ("marketing", "Marketing e vendas", "Mercado, estratégia comercial e relacionamento."),
    ("gestao", "Gestão e finanças", "Tecnologia, governança, finanças e contabilidade."),
]

EXPRESS = [
    dict(slug="educacao-especial-e-inclusiva", name="Educação Especial e Inclusiva", id=1079, img="eei.jpg",
         img_alt="Professora organiza peças de encaixe coloridas em uma mesa de atividades pedagógicas",
         lead="Pós-graduação para quem quer promover uma escola mais acessível, equitativa e acolhedora.",
         chamada="Planeje atividades pedagógicas mais acessíveis",
         intro="Fundamentos, práticas e estratégias da Educação Especial na perspectiva da inclusão, com foco na aprendizagem, na acessibilidade e na construção de ambientes educacionais mais diversos.",
         highlights=[("Educação inclusiva", "Políticas, legislação e práticas para acolher todos os estudantes."),
                     ("Tecnologias assistivas", "Recursos e normas técnicas que ampliam a acessibilidade."),
                     ("Projetos pedagógicos", "Currículo, didática e planejamento de atividades acessíveis.")],
         grade=["Didática", "Políticas Públicas e Legislação Educacional", "Educação Inclusiva",
                "Tecnologias Assistivas para Acessibilidade", "Legislação e Normas Técnicas de Acessibilidade",
                "Psicopedagogia", "Currículos e Projetos Pedagógicos", "Organização e Legislação da Educação",
                "Desenvolvimento Neuropsicomotor e da Aprendizagem"]),
    dict(slug="neuropsicopedagogia", name="Neuropsicopedagogia", id=1427, img="neuro.jpg",
         img_alt="Educadora analisa cartões ilustrados sobre a mesa, ao lado de um caderno de anotações",
         lead="Pós-graduação para quem quer compreender o cérebro que aprende e intervir com mais precisão.",
         chamada="Entenda como desenvolvimento e aprendizagem se relacionam",
         intro="Bases neurocientíficas, psicológicas e pedagógicas para compreender como o estudante aprende, avaliar dificuldades e planejar intervenções.",
         highlights=[("Avaliação da aprendizagem", "Instrumentos para identificar dificuldades e acompanhar a evolução."),
                     ("Psicologia do desenvolvimento", "As etapas do desenvolvimento e seu impacto na aprendizagem."),
                     ("Neurociências aplicadas", "Neurociências do comportamento levadas às práticas pedagógicas.")],
         grade=["Neurociências do Comportamento", "Psicopedagogia", "Neurociências e as Práticas Pedagógicas",
                "Neuroanatomia", "Psicologia do Desenvolvimento", "Avaliação da Aprendizagem",
                "Transtornos e Distúrbios da Aprendizagem", "Psicologia da Aprendizagem",
                "Avaliação Psicológica e Psicodiagnóstico"]),
]

MBA = dict(slug="mba-licitacoes-publicas", name="MBA em Licitações Públicas à Luz da Lei 14.133/21",
           short="MBA em Licitações Públicas", id=1362, img="mba.jpg",
           img_alt="Profissional lê documentos de um processo de contratação em um escritório com janelas amplas",
           lead="Formação estratégica para atuar com segurança e eficiência nas contratações públicas, da legislação à prática.",
           grade=[("Governança Pública Estratégica", 100), ("Processos Gerenciais da Gestão Pública", 95),
                  ("Licitações Públicas à Luz da Lei 14.133/21", 135),
                  ("Responsabilizações por Atos, Omissões e Ações Administrativas", 90),
                  ("Cidades Inteligentes", 60)])


# ---------------------------------------------------------------- helpers
def wa(course: str) -> str:
    msg = (f"Olá! Tenho interesse na pós-graduação em {course} (Black November). "
           "Pode me ajudar com a matrícula?")
    return f"https://wa.me/{WA}?text={quote(msg)}"


def cta(slug, course, cls="pp-btn pp-btn--yellow", label="Consultar matrícula"):
    return (f'<a class="{cls}" href="{escape(wa(course))}" target="_blank" rel="noopener" '
            f'data-checkout="{slug}">{label}</a>')


def grade_link(cid, label="Ver grade oficial", cls="pp-link"):
    return (f'<a class="{cls}" href="{GRADE_URL.format(cid)}" target="_blank" rel="noopener">'
            f'{label}<span class="sr-only"> (abre o portal da Faculdade Unypública)</span></a>')


def head(title, desc, path, img, jsonld):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="theme-color" content="#003164"/>
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}"/>
  <link rel="canonical" href="{SITE}{path}"/>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  <meta property="og:type" content="website"/>
  <meta property="og:locale" content="pt_BR"/>
  <meta property="og:title" content="{escape(title)}"/>
  <meta property="og:description" content="{escape(desc)}"/>
  <meta property="og:url" content="{SITE}{path}"/>
  <meta property="og:image" content="{SITE}/pos/img/{img}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Manrope:wght@400;600;700;800&display=swap"/>
  <link rel="stylesheet" href="/pos/pos.css?v={ASSET_V}"/>
  <style>html{{scroll-behavior:smooth}}.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body class="pp">
<a class="pp-skip" href="#conteudo">Pular para o conteúdo</a>
"""


def top(dark=False):
    cls = "pp-top pp-top--dark" if dark else "pp-top"
    return f"""<header class="{cls}">
  <div class="pp-wrap">
    <a class="pp-brand" href="/" aria-label="Sampa Educacional — página inicial">Sampa <span>Educacional</span></a>
    <nav aria-label="Pós-graduações">
      <a href="/pos/educacao-especial-e-inclusiva">Educação Especial</a>
      <a href="/pos/neuropsicopedagogia">Neuropsicopedagogia</a>
      <a href="/pos/mba-licitacoes-publicas">MBA Licitações</a>
      <a href="/pos/black-november">Mais 12 opções</a>
    </nav>
  </div>
</header>
"""


def ribbon():
    return (f'<div class="pp-ribbon js-promo" role="note">Black November · {BLACK["off"]} até {DEADLINE_TXT} '
            f'· termina em <b data-countdown>3 dias</b></div>\n'
            f'<div class="pp-ribbon js-ended" role="note">A condição Black November terminou em {DEADLINE_TXT}. '
            f'Consulte as condições atuais pelo WhatsApp.</div>\n')


def price_block():
    if not SHOW_PRICE_360:
        return ""
    return f"""<div class="pp-price js-promo">
          <p class="pp-price__from">De <s>{BLACK["de"]}</s> por</p>
          <p class="pp-price__value">{BLACK["por"]} <small>à vista</small></p>
          <p class="pp-price__inst">ou {BLACK["parc"]}</p>
          <p class="pp-price__deadline">Condição Black November válida até {DEADLINE_TXT}</p>
        </div>"""


IES_LINE = ('<p class="pp-ies">Instituição acadêmica: <strong>Faculdade Unypública</strong>, credenciada pelo MEC (nota 4). '
            'Comercialização e atendimento: <strong>Sampa Educacional</strong>.</p>')


def steps():
    return """<section class="pp-section pp-section--soft" aria-labelledby="como-title">
  <div class="pp-wrap">
    <h2 id="como-title" class="pp-rule">Como funciona a matrícula</h2>
    <ol class="pp-steps">
      <li><b>Escolha e pague</b><p>Fale com a equipe ou use o link de pagamento seguro do curso.</p></li>
      <li><b>Matrícula confirmada</b><p>A Sampa Educacional confirma sua matrícula assim que o pagamento é aprovado.</p></li>
      <li><b>Acesso liberado</b><p>O acesso à plataforma é liberado logo após a confirmação no portal da Faculdade Unypública.</p></li>
    </ol>
  </div>
</section>
"""


def foot():
    return f"""<footer class="pp-foot">
  <div class="pp-wrap">
    <p><strong>Sampa Educacional</strong> · Uma marca do SAMPA.GROUP</p>
    <p>Cursos de pós-graduação lato sensu da Faculdade Unypública, comercializados pela Sampa Educacional. Condições promocionais sujeitas à disponibilidade e válidas até {DEADLINE_TXT}.</p>
    <p><a href="/">Voltar ao site</a> · <a href="{escape(wa('pós-graduação'))}" target="_blank" rel="noopener">Falar no WhatsApp</a></p>
  </div>
</footer>
<script src="/pos/pos.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def course_ld(name, cid, path, hours, price=True):
    d = {"@context": "https://schema.org", "@type": "Course", "name": f"Pós-graduação em {name}",
         "url": SITE + path, "inLanguage": "pt-BR",
         "provider": {"@type": "CollegeOrUniversity", "name": "Faculdade Unypública"},
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                               "courseWorkload": f"PT{hours}H"}}
    if price and SHOW_PRICE_360:
        d["offers"] = {"@type": "Offer", "price": BLACK["por_num"], "priceCurrency": "BRL",
                       "validThrough": DEADLINE_ISO, "category": "Black November",
                       "seller": {"@type": "Organization", "name": "Sampa Educacional"}}
    return d


def grade_list(items, total):
    lis = "\n".join(f"        <li><span>{escape(n)}</span><span>{h}h</span></li>" for n, h in items)
    return f"""<ol class="pp-grade">
{lis}
      </ol>
      <p class="pp-grade__total"><span>Carga horária total</span><span>{total}h</span></p>"""


# ---------------------------------------------------------------- páginas
def page_express(c):
    path = f"/pos/{c['slug']}"
    hl = "\n".join(f'      <article class="pp-highlight"><h3>{escape(t)}</h3><p>{escape(p)}</p></article>'
                   for t, p in c["highlights"])
    ben = "\n".join(f"        <li>{escape(b)}</li>" for b in BENEFITS)
    trust = "".join(f"<span>{t}</span>" for t in TRUST)
    html = head(f"Pós-graduação em {c['name']} · Black November | Sampa Educacional",
                f"{c['lead']} 360h, 100% online, Faculdade Unypública. Condição Black November até {DEADLINE_TXT}.",
                path, c["img"], course_ld(c["name"], c["id"], path, 360))
    html += top(dark=True) + ribbon()
    html += f"""<main id="conteudo">
<section class="pp-express" aria-labelledby="t">
  <div class="pp-wrap">
    <div class="pp-express__copy">
      <p class="pp-eyebrow">Black November</p>
      <h1 id="t">{escape(c['name'])}</h1>
      <p class="pp-express__lead">{escape(c['lead'])}</p>
      <div class="pp-chips"><span class="pp-chip">Pós-graduação</span><span class="pp-chip">360h</span><span class="pp-chip">100% online</span><span class="pp-chip">Nota 4 MEC</span></div>
      {IES_LINE}
      {price_block()}
      <div class="pp-actions">
        {cta(c['slug'], c['name'])}
        <a class="pp-btn pp-btn--ghost" href="#grade">Ver o que você vai estudar</a>
      </div>
    </div>
    <div class="pp-express__photo"><img src="/pos/img/{c['img']}" alt="{escape(c['img_alt'])}" width="410" height="1072" fetchpriority="high"/></div>
  </div>
</section>

<section class="pp-section" aria-labelledby="estudar">
  <div class="pp-wrap">
    <h2 id="estudar" class="pp-rule">{escape(c['chamada'])}</h2>
    <p class="pp-section__intro">{escape(c['intro'])}</p>
    <div class="pp-highlights">
{hl}
    </div>
  </div>
</section>

<section class="pp-section pp-section--soft" id="grade" aria-labelledby="grade-t">
  <div class="pp-wrap pp-two">
    <div>
      <h2 id="grade-t" class="pp-rule">Grade curricular</h2>
      {grade_list([(n, 40) for n in c['grade']], 360)}
      <p style="margin-top:1rem">{grade_link(c['id'], 'Ver a grade no portal da Faculdade Unypública')}</p>
    </div>
    <div>
      <h2 class="pp-rule">O que está incluso</h2>
      <ul class="pp-benefits">
{ben}
      </ul>
      <div class="pp-trust">{trust}</div>
      <div class="pp-actions">{cta(c['slug'], c['name'], 'pp-btn pp-btn--blue')}</div>
    </div>
  </div>
</section>

{steps()}
<section class="pp-section pp-final" aria-labelledby="final-t">
  <div class="pp-wrap">
    <h2 id="final-t">Garanta a condição Black November</h2>
    <p class="js-promo">{BLACK['por']} à vista ou {BLACK['parc']}, até {DEADLINE_TXT}.</p>
    <div class="pp-actions">
      {cta(c['slug'], c['name'])}
      <a class="pp-btn pp-btn--ghost" href="/pos/black-november">Ver outras pós-graduações</a>
    </div>
  </div>
</section>
</main>
"""
    return html + foot()


def page_mba():
    c = MBA
    path = f"/pos/{c['slug']}"
    acc = []
    for i, (n, h) in enumerate(c["grade"], 1):
        acc.append(f"""      <details>
        <summary><span>Disciplina {i} – {escape(n)}</span><span class="h">{h}h</span></summary>
        <div class="pp-acc__body"><p>Disciplina {i} de {len(c['grade'])} · {h} horas · 100% online. A ementa completa está na grade oficial da Faculdade Unypública.</p></div>
      </details>""")
    total = sum(h for _, h in c["grade"])
    ben = "\n".join(f"        <li>{escape(b)}</li>" for b in BENEFITS)
    html = head(f"{c['name']} | Sampa Educacional",
                f"{c['lead']} {total}h, 100% online, Faculdade Unypública.",
                path, c["img"], course_ld(c["name"], c["id"], path, total, price=False))
    html += top() + f"""<main id="conteudo">
<section class="pp-vitrine" aria-labelledby="t">
  <div class="pp-wrap">
    <div>
      <h1 id="t" class="pp-rule">{escape(c['short'])}</h1>
      <p class="pp-vitrine__sub">À luz da Lei 14.133/21 · Faculdade Unypública</p>
      <p class="pp-vitrine__lead">{escape(c['lead'])}</p>
      <div class="pp-chips"><span class="pp-chip">Pós-graduação</span><span class="pp-chip">{total}h</span><span class="pp-chip">100% online</span><span class="pp-chip">Nota 4 MEC</span></div>
      {IES_LINE}
      <div class="pp-actions">
        <a class="pp-btn pp-btn--blue" href="#grade">Ver grade e condições</a>
        {cta(c['slug'], c['short'], 'pp-btn pp-btn--ghost', 'Consultar matrícula')}
      </div>
    </div>
    <div class="pp-vitrine__photo"><img src="/pos/img/{c['img']}" alt="{escape(c['img_alt'])}" width="417" height="684" fetchpriority="high"/></div>
  </div>
</section>

<section class="pp-section pp-section--soft" id="grade" aria-labelledby="grade-t">
  <div class="pp-wrap pp-two">
    <div>
      <h2 id="grade-t" class="pp-rule">Grade curricular</h2>
      <div class="pp-acc">
{chr(10).join(acc)}
      </div>
      <p class="pp-grade__total"><span>Carga horária total</span><span>{total}h</span></p>
      <p style="margin-top:1rem">{grade_link(c['id'], 'Ver a grade no portal da Faculdade Unypública')}</p>
    </div>
    <div>
      <div class="pp-box" id="condicoes">
        <h3>Condições Black November</h3>
        <p>O MBA tem condição comercial própria nesta campanha. Fale com a equipe da Sampa Educacional para receber o valor e as formas de pagamento.</p>
        <div class="pp-actions">{cta(c['slug'], c['short'], 'pp-btn pp-btn--yellow pp-btn--block')}</div>
      </div>
      <h2 class="pp-rule" style="margin-top:2.5rem">O que está incluso</h2>
      <ul class="pp-benefits">
{ben}
      </ul>
    </div>
  </div>
</section>

{steps()}
<section class="pp-section pp-final" aria-labelledby="final-t">
  <div class="pp-wrap">
    <h2 id="final-t">Aprofunde sua atuação em contratações públicas</h2>
    <div class="pp-actions">
      {cta(c['slug'], c['short'])}
      <a class="pp-btn pp-btn--ghost" href="/pos/black-november">Ver outras pós-graduações</a>
    </div>
  </div>
</section>
</main>
"""
    return html + foot()


def page_black():
    path = "/pos/black-november"
    shortcuts = "\n".join(
        f'      <a href="#{k}">{escape(t)}<small>{n} {"curso" if n == 1 else "cursos"}</small></a>'
        for k, t, _ in AREAS for n in [sum(1 for c in COURSES_12 if c[0] == k)])
    sections = []
    for k, t, d in AREAS:
        cards = []
        for area, slug, name, cid, grade in COURSES_12:
            if area != k:
                continue
            gl = "".join(f"<li>{escape(x)}</li>" for x in grade)
            price = (f'<p class="pp-course__price js-promo">De <s>{BLACK["de"]}</s> por <b>{BLACK["por"]}</b> à vista '
                     f'<br>ou {BLACK["parc"].replace(" no cartão de crédito", "")}</p>') if SHOW_PRICE_360 else ""
            cards.append(f"""      <article class="pp-course">
        <h3>{escape(name)}</h3>
        <p class="pp-course__meta">Pós-graduação · 360h · 100% online</p>
        {price}
        <details>
          <summary>Disciplinas (9 × 40h)</summary>
          <ol>{gl}</ol>
        </details>
        <div class="pp-course__actions">
          {cta(slug, name, 'pp-btn pp-btn--blue')}
          {grade_link(cid, 'Grade oficial', 'pp-btn pp-btn--ghost')}
        </div>
      </article>""")
        sections.append(f"""  <section class="pp-area" id="{k}" aria-labelledby="{k}-t">
    <h2 id="{k}-t" class="pp-rule">{escape(t)}</h2>
    <p class="pp-section__intro">{escape(d)}</p>
    <div class="pp-cards">
{chr(10).join(cards)}
    </div>
  </section>""")
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Pós-graduações Black November — Sampa Educacional",
          "itemListElement": [{"@type": "ListItem", "position": i + 1,
                               "item": course_ld(c[2], c[3], path + "#" + c[0], 360)}
                              for i, c in enumerate(COURSES_12)]}
    html = head("Mais 12 opções de pós-graduação · Black November | Sampa Educacional",
                f"12 pós-graduações de 360h da Faculdade Unypública em quatro áreas. {BLACK['por']} à vista até {DEADLINE_TXT}.",
                path, "black.jpg", ld)
    html += top() + ribbon() + f"""<main id="conteudo">
<section class="pp-escolha" aria-labelledby="t">
  <div class="pp-wrap">
    <div>
      <p class="pp-eyebrow" style="color:var(--blue)">Black November</p>
      <h1 id="t" class="pp-rule">Mais 12 opções de pós-graduação</h1>
      <p class="pp-escolha__lead">Amplie sua formação em diferentes áreas do conhecimento, com o atendimento da Sampa Educacional.</p>
      {IES_LINE}
      {price_block()}
    </div>
    <div class="pp-escolha__photo"><img src="/pos/img/black.jpg" alt="Profissional sorridente apoia o queixo na mão ao lado de um notebook" width="432" height="1362" fetchpriority="high"/></div>
  </div>
</section>

<section class="pp-section pp-section--soft" aria-labelledby="areas-q">
  <div class="pp-wrap">
    <h2 id="areas-q" class="pp-areas-q">Qual área você quer aprofundar?</h2>
    <nav class="pp-areas" aria-label="Áreas de pós-graduação">
{shortcuts}
    </nav>
  </div>
</section>

<div class="pp-section">
  <div class="pp-wrap">
{chr(10).join(sections)}
    <p class="pp-back">Procurando outra área? Veja também <a class="pp-link" href="/pos/educacao-especial-e-inclusiva">Educação Especial e Inclusiva</a>, <a class="pp-link" href="/pos/neuropsicopedagogia">Neuropsicopedagogia</a> e o <a class="pp-link" href="/pos/mba-licitacoes-publicas">MBA em Licitações Públicas</a>.</p>
  </div>
</div>

{steps()}
</main>
"""
    return html + foot()


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for c in EXPRESS:
        (ROOT / f"{c['slug']}.html").write_text(page_express(c), encoding="utf-8")
    (ROOT / f"{MBA['slug']}.html").write_text(page_mba(), encoding="utf-8")
    (ROOT / "black-november.html").write_text(page_black(), encoding="utf-8")
    print("ok:", sorted(p.name for p in ROOT.glob("*.html")))


if __name__ == "__main__":
    main()
