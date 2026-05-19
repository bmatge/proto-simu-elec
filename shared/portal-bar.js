/* Injects a slim portal bar at the top of any simulator page.
   Usage in a simulator's <head>:
     <link rel="stylesheet" href="/shared/portal-bar.css">
     <script src="/shared/portal-bar.js" defer></script>
   The current simulator is derived from the URL path (/<slug>/...). */
(function () {
  function currentSlug() {
    const seg = window.location.pathname.split("/").filter(Boolean);
    return seg[0] || "";
  }

  function buildBar(manifest, slug) {
    const bar = document.createElement("nav");
    bar.className = "portal-bar";
    bar.setAttribute("aria-label", "Portail simulateurs");

    const home = document.createElement("a");
    home.className = "portal-bar__home";
    home.href = "/";
    home.textContent = "Portail simulateurs";
    bar.appendChild(home);

    const current = manifest.simulators.find((s) => s.slug === slug);
    if (current) {
      const sep = document.createElement("span");
      sep.className = "portal-bar__sep";
      sep.textContent = "/";
      bar.appendChild(sep);
      const title = document.createElement("span");
      title.className = "portal-bar__title";
      title.textContent = current.title;
      bar.appendChild(title);
    }

    const select = document.createElement("select");
    select.className = "portal-bar__switcher";
    select.setAttribute("aria-label", "Changer de simulateur");
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Autres simulateurs…";
    select.appendChild(placeholder);
    manifest.simulators
      .filter((s) => s.slug !== slug)
      .forEach((s) => {
        const opt = document.createElement("option");
        opt.value = "/" + s.slug + "/";
        opt.textContent = s.title;
        select.appendChild(opt);
      });
    select.addEventListener("change", function () {
      if (select.value) window.location.href = select.value;
    });
    bar.appendChild(select);

    return bar;
  }

  function publishHeight(bar) {
    const update = () => {
      const h = bar.offsetHeight || 0;
      document.documentElement.style.setProperty("--portal-bar-height", h + "px");
    };
    update();
    if (typeof ResizeObserver !== "undefined") {
      new ResizeObserver(update).observe(bar);
    } else {
      window.addEventListener("resize", update);
    }
  }

  function mount() {
    fetch("/shared/simulators.json", { cache: "no-cache" })
      .then((r) => r.json())
      .then((manifest) => {
        const bar = buildBar(manifest, currentSlug());
        document.body.insertBefore(bar, document.body.firstChild);
        publishHeight(bar);
      })
      .catch(() => {
        /* portal manifest unavailable — skip injection silently */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
