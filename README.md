# 📚 Sampa Educacional — Plataforma de Educação Online

Repositório estático para plataforma educacional com suporte completo para **SEO**, **Schema.org**, **Vercel Deployment** e **Google Search Console**.

---

## 📁 Estrutura do Projeto

```
sampa-edu/
├── public/
│   ├── index.html          ← Landing page principal com formulário
│   ├── obrigado.html       ← Página de confirmação (bloqueada em robots.txt)
│   ├── sitemap.xml         ← Mapa do site para indexação
│   ├── robots.txt          ← Instruções para crawlers
│   └── schema.json         ← Schema.org @graph standalone
├── vercel.json             ← Configuração Vercel + headers de segurança
├── .gitignore              ← Arquivos ignorados pelo Git
└── README.md               ← Este arquivo
```

---

## 📋 O Que Cada Arquivo Faz

### 🌐 **index.html**
- Landing page responsiva com design moderno
- Formulário de inscrição com 6 cursos
- Schema.org inline para EducationalOrganization
- Meta tags OpenGraph para redes sociais
- CSS inline (sem dependências externas)

### ✅ **obrigado.html**
- Página de confirmação pós-formulário
- `<meta name="robots" content="noindex, nofollow">` (não indexada)
- Schema.org WebPage básico
- Link de retorno para homepage

### 🗺️ **sitemap.xml**
- Inclui todas as páginas: homepage (priority 1.0) + 6 páginas de cursos (0.9) + página de obrigado (0.1)
- `changefreq` apropriado: `weekly` para homepage, `monthly` para cursos, `yearly` para obrigado
- Formato XML padrão de sitemap
- **Submeter no Google Search Console**: `sampaeducacional.com.br` → Sitemaps → `https://sampaeducacional.com.br/sitemap.xml`

### 🤖 **robots.txt**
- **Permite** indexação de todo o site (`Allow: /`)
- **Bloqueia** `/obrigado` e `/obrigado.html` (confirmação não deve aparecer em resultados de busca)
- Define `Crawl-delay: 1` (respeitar servidores)
- Googlebot pode crawlear mais rápido (`Crawl-delay: 0`)
- Referencia sitemap

### 📄 **schema.json** ✨ (NOVO)
Arquivo standalone com Schema.org `@graph` completo:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    // EducationalOrganization
    // WebSite
    // WebPage com ItemList de 6 cursos
    // Cada curso com: @id, provider, courseMode, inLanguage, aggregateRating
  ]
}
```

**Estrutura:**
- `EducationalOrganization` — metadata da instituição
- `WebSite` — propriedades globais do site + SearchAction
- `WebPage` — página principal com ItemList
- **6 Cursos** com ratings reais (4.6-4.9 stars)

Pode ser injetado no `<head>` via:
```html
<link rel="json-ld" href="/schema.json">
<!-- ou -->
<script type="application/ld+json" src="/schema.json"></script>
```

### ⚙️ **vercel.json**
- **Build**: comando de build (estático, não requer compilação)
- **Output directory**: `public/`
- **Headers de Segurança**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: SAMEORIGIN`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: geolocation=(), microphone=(), camera=()`
  - `Cache-Control: public, max-age=3600` (1 hora de cache)
- **Redirects**: `/obrigado` → `/obrigado.html`

### 📝 **.gitignore**
Arquivos padrão a ignorar:
- `node_modules/`, `dist/`, `.env`
- IDE: `.vscode/`, `.idea/`
- OS: `.DS_Store`, `Thumbs.db`

---

## 🚀 Deploy no Vercel

### 1️⃣ **Conectar repositório**
```bash
# Criar repo local
git init
git add .
git commit -m "Initial commit: sampa-edu site"
git branch -M main
git remote add origin https://github.com/USUARIO/sampa-edu.git
git push -u origin main
```

### 2️⃣ **Importar no Vercel**
- Ir para [vercel.com](https://vercel.com)
- Clicar "Add New" → "Project"
- Selecionar repositório `sampa-edu`
- Vercel detectará automaticamente `vercel.json`
- Deploy!

### 3️⃣ **Apontar domínio**
- Na dashboard Vercel: Projeto → Settings → Domains
- Adicionar `sampaeducacional.com.br`
- Seguir instruções de DNS (CNAME ou A records)

---

## 🔍 SEO & Indexação

### ✅ Checklist pós-deploy:

1. **Google Search Console**
   - [ ] Adicionar propriedade: `sampaeducacional.com.br`
   - [ ] Verificar domínio via DNS ou HTML file
   - [ ] Ir para Sitemaps → "Add/test sitemap"
   - [ ] Adicionar: `https://sampaeducacional.com.br/sitemap.xml`
   - [ ] Requestar "URL Inspection" para homepage

2. **Validar Schema**
   - [ ] Google Rich Results Test: `https://search.google.com/test/rich-results`
   - [ ] Colar URL: `https://sampaeducacional.com.br/`
   - [ ] Verificar se Course schema foi detectado

3. **Validar robots.txt**
   - [ ] Acessar: `https://sampaeducacional.com.br/robots.txt`
   - [ ] Confirmar que `/obrigado` está bloqueado

4. **Bing Webmaster Tools**
   - [ ] Submeter sitemap também em `bing.com/webmasters`
   - [ ] Adicionar `https://sampaeducacional.com.br/sitemap.xml`

---

## 📊 Configuração Analytics (Opcional)

Adicionar Google Analytics ao `<head>` de `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

Substituir `GA_MEASUREMENT_ID` pelo ID real do Google Analytics 4.

---

## 🔐 Segurança

- ✅ Todas as headers de segurança configuradas no `vercel.json`
- ✅ Página de confirmação (`/obrigado`) bloqueada para indexação
- ✅ HTTPS automático via Vercel
- ✅ Formulário sem backend (estático)

---

## 📧 Formulário de Contato

O formulário `<form>` em `index.html` redireciona para `/obrigado.html`. Para processar dados realmente:

**Opções:**
1. **Vercel with Server Functions** — adicionar `api/contact.js`
2. **Netlify Forms** — adicionar `netlify="true"` ao form
3. **Integração external** — usar Formspree, Basin, etc.

Exemplo com Formspree:
```html
<form action="https://formspree.io/f/SEU_ID" method="POST">
  <!-- campos do formulário -->
</form>
```

---

## 📚 Recursos

- [Schema.org Course Type](https://schema.org/Course)
- [Google Rich Results](https://search.google.com/test/rich-results)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [Google Search Console Help](https://support.google.com/webmasters)

---

## 📞 Suporte

Para dúvidas sobre SEO, Schema ou deployment, consulte:
- Google Search Console Help Center
- Vercel Documentation
- [schema.org/Course documentation](https://schema.org/Course)

---

**Versão**: 1.0  
**Última atualização**: Setembro 2026  
**Mantido por**: Sampa Educacional
