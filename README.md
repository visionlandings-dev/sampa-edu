# Sampa Educacional — Site Institucional

Landing page oficial da Sampa Educacional. Página estática com lista VIP, ecossistema de formação e redirecionamento pós-formulário.

## Stack

- HTML5 semântico, autocontido (zero dependências de build)
- CSS custom properties + Grid + Framer-inspired transitions
- Google Fonts async (Space Grotesk + Manrope)
- Schema.org JSON-LD para SEO
- Deploy: Vercel Static (sem framework, sem build step)

## Estrutura

```
sampa-edu/
├── public/
│   ├── index.html       ← landing principal
│   ├── obrigado.html    ← confirmação pós-formulário
│   ├── sitemap.xml      ← indexação Google / Bing
│   └── robots.txt       ← diretrizes para crawlers
├── vercel.json          ← configuração de deploy e headers
├── .gitignore
└── README.md
```

## Deploy

**Vercel (recomendado)**

1. Importe o repositório no [vercel.com/new](https://vercel.com/new)
2. Framework Preset: `Other`
3. Output Directory: `public`
4. Build Command: *(vazio)*
5. Deploy

**GitHub Pages (alternativo)**

Configure `gh-pages` apontando para `/public`.

## Domínio

Produção: `https://sampaeducacional.com.br`

Configure o domínio em **Vercel → Project → Domains**.

## Contato embarcado

- WhatsApp: `https://wa.me/5511967992285`
- Instagram: `https://www.instagram.com/sampa_edu/`

## Schema.org

`EducationalOrganization` com `hasOfferCatalog` listando os 6 pilares do ecossistema. Validar em [schema.org/docs/gs.html](https://validator.schema.org/).

## Licença

Propriedade de **LEALI GESTÃO EDUCACIONAL LTDA** — todos os direitos reservados.
