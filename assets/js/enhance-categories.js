<script>
document.addEventListener("DOMContentLoaded", () => {
  const offset = document.querySelector('meta[name="quarto:offset"]')?.content || "";
  const rmDiacritics = (s) => s
    .replace(/[ÁÀÂÃÄ]/g,'A').replace(/[áàâãä]/g,'a')
    .replace(/[ÉÈÊË]/g,'E').replace(/[éèêë]/g,'e')
    .replace(/[ÍÌÎÏ]/g,'I').replace(/[íìîï]/g,'i')
    .replace(/[ÓÒÔÕÖ]/g,'O').replace(/[óòôõö]/g,'o')
    .replace(/[ÚÙÛÜ]/g,'U').replace(/[úùûü]/g,'u')
    .replace(/[Ç]/g,'C').replace(/[ç]/g,'c')
    .replace(/[Ñ]/g,'N').replace(/[ñ]/g,'n');
  const toSlug = (s) => rmDiacritics(String(s||"")).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");

  const classMap = [
    ["matematica","cat--matematica"],
    ["estatistica","cat--estatistica"],
    ["fisica","cat--fisica"],
    ["programacao","cat--programacao"],
    ["curso","cat--curso"],
    ["artigo","cat--artigo"],
    ["serie","cat--serie"],
    ["sumario","cat--sumario"],
  ];

  const enhanceWrap = (wrap, sortDedup=false) => {
    if(!wrap) return;

    if (sortDedup) {
      const items = Array.from(wrap.querySelectorAll(':scope > .quarto-category'));
      const seen = new Map();
      for (const el of items) {
        const key = el.textContent.trim().toLowerCase();
        if (seen.has(key)) el.remove(); else seen.set(key, el);
      }
      const sorted = Array.from(wrap.querySelectorAll(':scope > .quarto-category'))
        .sort((a,b)=>a.textContent.trim().localeCompare(b.textContent.trim(),'pt-BR'));
      sorted.forEach(el => wrap.appendChild(el));
    }

    wrap.querySelectorAll(':scope > .quarto-category').forEach((el) => {
      if (el.dataset.enhancedChip === "1") return;
      const label = el.textContent.trim();
      const slug  = toSlug(label);
      const plain = rmDiacritics(label.toLowerCase());

      for (const [needle, cls] of classMap) {
        if (slug===needle || slug.includes(needle) || plain.includes(needle)) { el.classList.add(cls); break; }
      }

      let chip = el;
      if (el.tagName !== "A") {
        const a = document.createElement('a');
        a.className = el.className;
        a.textContent = label;
        a.href = `${offset}categories.html#${slug}`;
        chip = a;
        el.replaceWith(a);
      } else if (!el.getAttribute('href')) {
        el.setAttribute('href', `${offset}categories.html#${slug}`);
      }

      chip.setAttribute('aria-label', `Ver posts em ${label}`);
      chip.setAttribute('title', `Ver posts em ${label}`);
      chip.dataset.enhancedChip = "1";
    });
  };

  enhanceWrap(document.querySelector('#title-block-header .quarto-categories'), true);
  document.querySelectorAll('main .quarto-categories').forEach(wrap => enhanceWrap(wrap, false));
});
</script>

