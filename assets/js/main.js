/* Trame di Paesaggio Atelier — interazioni del sito */

/*
 * Configurazione del modulo di contatto.
 * FORM_ENDPOINT: indirizzo del servizio che inoltra le richieste via email
 * (es. Formspree: "https://formspree.io/f/xxxxxxx"), collegato all'indirizzo
 * riservato per le richieste. Finché resta vuoto, l'invio apre il programma di
 * posta del visitatore con la richiesta già compilata, indirizzata a FALLBACK_EMAIL.
 */
var FORM_ENDPOINT = "";
var FALLBACK_EMAIL = "tramedipaesaggioatelier@gmail.com";

(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  /* ---------- Header: stato allo scroll ---------- */
  var header = document.querySelector("[data-header]");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var burger = document.querySelector("[data-burger]");
  function setMenu(open) {
    header.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Chiudi il menu" : "Apri il menu");
  }
  if (burger && header) {
    burger.addEventListener("click", function () {
      setMenu(!header.classList.contains("is-open"));
    });
    header.querySelectorAll("[data-mobile-menu] a").forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1000 && header.classList.contains("is-open")) setMenu(false);
    });
  }

  /* ---------- Menu a tendina "Casi studio" ---------- */
  document.querySelectorAll("[data-dropdown]").forEach(function (drop) {
    var toggle = drop.querySelector("button");
    var closeTimer;
    function set(open) {
      drop.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    }
    toggle.addEventListener("click", function () { set(!drop.classList.contains("is-open")); });
    drop.addEventListener("mouseenter", function () {
      if (window.matchMedia("(hover: hover)").matches) { clearTimeout(closeTimer); set(true); }
    });
    drop.addEventListener("mouseleave", function () {
      if (window.matchMedia("(hover: hover)").matches) closeTimer = setTimeout(function () { set(false); }, 180);
    });
    drop.addEventListener("focusout", function (e) {
      if (!drop.contains(e.relatedTarget)) set(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drop.classList.contains("is-open")) { set(false); toggle.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (!drop.contains(e.target)) set(false);
    });
  });

  /* ---------- Comparsa progressiva dei contenuti ---------- */
  var revealItems = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealItems.forEach(function (el) { io.observe(el); });
  } else {
    revealItems.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Anno nel footer ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Galleria a schermo intero ---------- */
  var lightbox = document.querySelector("[data-lightbox]");
  var gallery = document.querySelector("[data-gallery]");
  if (lightbox && gallery) {
    var items = Array.prototype.slice.call(gallery.querySelectorAll("[data-full]"));
    var lbImg = lightbox.querySelector("[data-lightbox-img]");
    var lbCap = lightbox.querySelector("[data-lightbox-caption]");
    var current = 0;
    var lastFocus = null;

    function show(i) {
      current = (i + items.length) % items.length;
      var btn = items[current];
      lbImg.src = btn.getAttribute("data-full");
      lbImg.alt = btn.getAttribute("data-caption") || "";
      lbCap.textContent = btn.getAttribute("data-caption") || "";
    }
    function open(i) {
      lastFocus = document.activeElement;
      show(i);
      lightbox.hidden = false;
      document.body.classList.add("menu-open");
      lightbox.querySelector("[data-lightbox-close]").focus();
    }
    function close() {
      lightbox.hidden = true;
      document.body.classList.remove("menu-open");
      if (lastFocus) lastFocus.focus();
    }
    items.forEach(function (btn, i) { btn.addEventListener("click", function () { open(i); }); });
    lightbox.querySelector("[data-lightbox-close]").addEventListener("click", close);
    lightbox.querySelector("[data-lightbox-prev]").addEventListener("click", function () { show(current - 1); });
    lightbox.querySelector("[data-lightbox-next]").addEventListener("click", function () { show(current + 1); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) close(); });
    document.addEventListener("keydown", function (e) {
      if (lightbox.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
    if (items.length < 2) {
      lightbox.querySelectorAll(".lightbox__nav").forEach(function (b) { b.hidden = true; });
    }
  }

  /* ---------- Video 3D: caricato solo al clic ---------- */
  document.querySelectorAll("[data-video]").forEach(function (frame) {
    var button = frame.querySelector(".video__play");
    button.addEventListener("click", function () {
      var iframe = document.createElement("iframe");
      iframe.src = frame.getAttribute("data-video");
      iframe.title = button.getAttribute("aria-label");
      iframe.allow = "autoplay; fullscreen";
      iframe.allowFullscreen = true;
      frame.appendChild(iframe);
      button.remove();
    });
  });

  /* ---------- Modulo di contatto ---------- */
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    var status = form.querySelector("[data-form-status]");
    var messages = {
      valueMissing: "Questo campo è necessario.",
      typeMismatch: "Controlla il formato, per favore.",
      checkbox: "Per inviare la richiesta serve il tuo consenso."
    };

    function fieldError(input) {
      var field = input.closest(".field");
      var old = field.querySelector(".field__error");
      if (old) old.remove();
      field.classList.remove("is-invalid");
      input.removeAttribute("aria-invalid");
      if (input.validity.valid) return true;
      var msg = input.type === "checkbox" ? messages.checkbox
        : input.validity.valueMissing ? messages.valueMissing : messages.typeMismatch;
      var err = document.createElement("span");
      err.className = "field__error";
      err.id = input.id + "-errore";
      err.textContent = msg;
      field.appendChild(err);
      field.classList.add("is-invalid");
      input.setAttribute("aria-invalid", "true");
      input.setAttribute("aria-describedby", err.id);
      return false;
    }

    form.querySelectorAll("input, select, textarea").forEach(function (input) {
      input.addEventListener("blur", function () {
        if (input.closest(".field").classList.contains("is-invalid")) fieldError(input);
      });
      input.addEventListener("change", function () {
        if (input.closest(".field").classList.contains("is-invalid")) fieldError(input);
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      status.textContent = "";

      var firstInvalid = null;
      form.querySelectorAll("[required]").forEach(function (input) {
        if (!fieldError(input) && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) { firstInvalid.focus(); return; }
      if (form.elements._gotcha.value) return;

      var data = {
        nome: form.elements.nome.value.trim(),
        struttura: form.elements.struttura.value.trim(),
        tipologia: form.elements.tipologia.value,
        localita: form.elements.localita.value.trim(),
        email: form.elements.email.value.trim(),
        telefono: form.elements.telefono.value.trim(),
        messaggio: form.elements.messaggio.value.trim()
      };

      var success = "Grazie, " + data.nome.split(" ")[0] + ". Abbiamo ricevuto la tua richiesta.\nTi ricontattiamo a breve per fissare la valutazione.";

      if (!FORM_ENDPOINT) {
        var body = [
          "Richiesta di valutazione paesaggistica online", "",
          "Nome: " + data.nome, "Struttura: " + data.struttura, "Tipologia: " + data.tipologia,
          "Località: " + data.localita, "Email: " + data.email, "Telefono: " + data.telefono, "",
          "Lo spazio esterno:", data.messaggio || "-"
        ].join("\n");
        window.location.href = "mailto:" + FALLBACK_EMAIL +
          "?subject=" + encodeURIComponent("Valutazione paesaggistica online — " + data.struttura) +
          "&body=" + encodeURIComponent(body);
        status.classList.add("is-success");
        status.textContent = "Si è aperto il tuo programma di posta con la richiesta già compilata: ti basta inviarla.";
        return;
      }

      var button = form.querySelector("[type=submit]");
      button.disabled = true;
      button.textContent = "Invio in corso";
      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(Object.assign({ _subject: "Valutazione paesaggistica online — " + data.struttura }, data))
      }).then(function (res) {
        if (!res.ok) throw new Error("invio non riuscito");
        form.reset();
        status.classList.add("is-success");
        status.textContent = success;
      }).catch(function () {
        status.classList.add("is-error");
        status.textContent = "Non siamo riusciti a inviare la richiesta. Riprova tra poco, oppure scrivici a " + FALLBACK_EMAIL + ".";
      }).then(function () {
        button.disabled = false;
        button.textContent = "Richiedi la valutazione gratuita";
      });
    });
  }
})();
