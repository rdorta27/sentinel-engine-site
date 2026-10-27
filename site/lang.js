(function () {
  // The language follows the saved choice, then the browser, then the page.
  // The selector links say where each language lives. This script adds no routes.
  var KEY = "knowman-lang";

  function canonical(value) {
    if (!value) { return null; }
    var v = String(value);
    if (v === "en" || v.indexOf("en-") === 0) { return "en"; }
    if (v === "es" || v.indexOf("es-") === 0) { return "es"; }
    if (v === "pt" || v.indexOf("pt-") === 0) { return "pt-BR"; }
    return null;
  }

  function valid(value) {
    return value === "en" || value === "es" || value === "pt-BR";
  }

  function saved() {
    try {
      var value = localStorage.getItem(KEY);
      return valid(value) ? value : null;
    } catch (e) {
      return null;
    }
  }

  function remember(value) {
    var lang = canonical(value);
    if (!valid(lang)) { return; }
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  function pageLang() {
    return canonical(document.documentElement.lang);
  }

  function browserLang() {
    var list = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || "en"];
    for (var i = 0; i < list.length; i++) {
      var primary = String(list[i]).toLowerCase().split("-")[0];
      if (primary === "en") { return "en"; }
      if (primary === "es") { return "es"; }
      if (primary === "pt") { return "pt-BR"; }
    }
    return "en";
  }

  function findLink(want) {
    var links = document.querySelectorAll("a[hreflang]");
    for (var i = 0; i < links.length; i++) {
      if (canonical(links[i].getAttribute("hreflang")) === want) { return links[i]; }
    }
    return null;
  }

  function show() {
    document.documentElement.style.visibility = "";
  }

  function go(want) {
    var link = findLink(want);
    if (!link) { show(); return; }
    var target;
    try {
      target = new URL(link.getAttribute("href"), location.href);
    } catch (e) {
      show(); return;
    }
    target.search = location.search;
    target.hash = location.hash;
    if (target.href === location.href) { show(); return; }
    location.replace(target.href);
  }

  document.addEventListener("click", function (e) {
    var node = e.target;
    while (node && node !== document) {
      if (node.tagName === "A" && node.hasAttribute("hreflang")) {
        remember(node.getAttribute("hreflang"));
        return;
      }
      node = node.parentNode;
    }
  });

  var here = pageLang();
  var want = saved();
  if (!want) {
    want = here === "en" ? browserLang() : here;
  }
  if (!want || want === here) { return; }

  // Hide the page until the target is known. A missing link shows it again.
  document.documentElement.style.visibility = "hidden";
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { go(want); });
  } else {
    go(want);
  }
  setTimeout(show, 2000);
})();
