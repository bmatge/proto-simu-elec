/* Business-stakeholder "behind-the-scenes" modal.

   Usage in any simulator/page:
     <link rel="stylesheet" href="/shared/business-modal.css">
     <script type="application/json" id="business-modal-data">
       {
         "title": "Coulisses méthodo — <nom de l'outil>",
         "audience": "DGEC / pilotage du Plan d'électrification",
         "intro": "Avant de figer ce simulateur, voici les choix de modélisation, les données qu'il nous faut, et les questions ouvertes pour les acteurs métier.",
         "sections": {
           "perimetre":  [ "string", {"q": "...", "note": "...", "status": "todo|ok|open"} ],
           "arbitrages": [ ... ],
           "sources":    [ ... ],
           "hypotheses": [ ... ],
           "attention":  [ ... ]
         },
         "updated": "2026-05-20"
       }
     </script>
     <script src="/shared/business-modal.js" defer></script>

   The JSON drives the rendering — no per-page HTML is required beyond
   the <script type="application/json"> block. The 5 sections are fixed
   to enforce a consistent reading grid across all simulators/maps/dashboards.
*/
(function () {
  const SECTIONS = [
    {
      key: "perimetre",
      title: "Périmètre & public cible",
      hint: "Qui est l'utilisateur, quelle décision on l'aide à prendre, et où s'arrête le simulateur."
    },
    {
      key: "arbitrages",
      title: "Arbitrages méthodologiques",
      hint: "Les choix de modélisation à valider — horizon, agrégations, conventions de calcul."
    },
    {
      key: "sources",
      title: "Sources de données nécessaires",
      hint: "Ce qu'il faut récupérer (et auprès de qui) pour que le simulateur soit utilisable en production."
    },
    {
      key: "hypotheses",
      title: "Hypothèses & paramètres de calcul",
      hint: "Valeurs par défaut, taux, durées — ce qui n'est ni de la donnée ni de l'arbitrage de modèle."
    },
    {
      key: "attention",
      title: "Points d'attention / questions ouvertes",
      hint: "Risques, edge cases, sujets à trancher collectivement avant mise en ligne."
    }
  ];

  function loadData() {
    const tag = document.getElementById("business-modal-data");
    if (!tag) return null;
    try {
      return JSON.parse(tag.textContent);
    } catch (err) {
      console.warn("[business-modal] JSON invalide :", err);
      return null;
    }
  }

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) {
      for (const k in attrs) {
        if (k === "class") node.className = attrs[k];
        else if (k === "text") node.textContent = attrs[k];
        else if (k === "html") node.innerHTML = attrs[k];
        else node.setAttribute(k, attrs[k]);
      }
    }
    if (children) {
      (Array.isArray(children) ? children : [children]).forEach((c) => {
        if (c) node.appendChild(c);
      });
    }
    return node;
  }

  function buildItem(entry) {
    const li = el("li");
    let q, note, status;
    if (typeof entry === "string") {
      q = entry;
    } else if (entry && typeof entry === "object") {
      q = entry.q || "";
      note = entry.note;
      status = entry.status;
    }
    if (status) li.setAttribute("data-status", status);
    const qSpan = el("span", { class: "bm-q", text: q });
    li.appendChild(qSpan);
    if (note) {
      li.appendChild(el("span", { class: "bm-note", text: note }));
    }
    return li;
  }

  function buildSection(def, items, index) {
    const wrap = el("section", { class: "bm-section" });
    const header = el("div", { class: "bm-section__header" }, [
      el("span", { class: "bm-section__num", text: String(index + 1) }),
      el("h3", { class: "bm-section__title", text: def.title })
    ]);
    wrap.appendChild(header);
    wrap.appendChild(el("p", { class: "bm-section__hint", text: def.hint }));

    if (!items || items.length === 0) {
      wrap.appendChild(
        el("p", {
          class: "bm-section__hint",
          text: "— Section à compléter avec les acteurs métier —"
        })
      );
      return wrap;
    }
    const ul = el("ul");
    items.forEach((entry) => ul.appendChild(buildItem(entry)));
    wrap.appendChild(ul);
    return wrap;
  }

  function buildDialog(data) {
    const dialog = el("dialog", { class: "bm-dialog", "aria-labelledby": "bm-dialog-title" });
    const inner = el("div", { class: "bm-dialog__inner" });

    const header = el("header", { class: "bm-dialog__header" });
    const titles = el("div", { class: "bm-dialog__titles" });
    if (data.audience) {
      titles.appendChild(el("span", { class: "bm-dialog__eyebrow", text: data.audience }));
    }
    titles.appendChild(
      el("h2", { class: "bm-dialog__title", id: "bm-dialog-title", text: data.title || "Coulisses méthodologiques" })
    );
    if (data.intro) {
      titles.appendChild(el("p", { class: "bm-dialog__intro", text: data.intro }));
    }
    header.appendChild(titles);

    const closeBtn = el("button", {
      type: "button",
      class: "bm-dialog__close",
      "aria-label": "Fermer la modale",
      text: "✕"
    });
    closeBtn.addEventListener("click", () => dialog.close());
    header.appendChild(closeBtn);
    inner.appendChild(header);

    const body = el("div", { class: "bm-dialog__body" });
    SECTIONS.forEach((def, i) => {
      const items = (data.sections && data.sections[def.key]) || [];
      body.appendChild(buildSection(def, items, i));
    });
    inner.appendChild(body);

    const footer = el("div", { class: "bm-dialog__footer" });
    const left = el("span", {
      html:
        "<strong>À l'attention des acteurs métier.</strong> Cette page liste ce qui doit être validé / fourni pour fiabiliser l'outil."
    });
    footer.appendChild(left);
    if (data.updated) {
      footer.appendChild(el("span", { text: "Mis à jour : " + data.updated }));
    }
    inner.appendChild(footer);

    dialog.appendChild(inner);

    // Close on backdrop click (clicks bubbling to the <dialog> itself)
    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) dialog.close();
    });

    return dialog;
  }

  function buildTrigger(dialog) {
    const btn = el("button", {
      type: "button",
      class: "bm-trigger",
      "aria-haspopup": "dialog",
      "aria-label": "Voir la méthode, les données et les arbitrages de cette page"
    });
    btn.appendChild(el("span", { class: "bm-trigger__icon", text: "i" }));
    btn.appendChild(el("span", { class: "bm-trigger__label", text: "Méthode, données et arbitrages" }));
    btn.addEventListener("click", () => {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    });
    return btn;
  }

  function mount() {
    const data = loadData();
    if (!data) return;
    const dialog = buildDialog(data);
    document.body.appendChild(dialog);
    document.body.appendChild(buildTrigger(dialog));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
