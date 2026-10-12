/* Dr. Sachin Gupta · Hope Kidney Care — site behaviour (no dependencies) */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  var WA_NUMBER = "918828888077";

  /* ---------- Consultation schedule (IST) ---------- */
  // Days: 0 = Sun … 6 = Sat. Times in 24h minutes.
  var SCHEDULE = {
    hope:  { name: "Hope Kidney Care, Thane",         days: [1, 2, 3, 4, 5, 6], from: 19 * 60, to: 21 * 60, label: "7:00 – 9:00 PM" },
    oscar: { name: "Oscar Hospital, Kasarvadavli",    days: [1, 2, 3, 4, 5, 6], from: 10 * 60, to: 11 * 60, label: "10:00 – 11:00 AM" },
    aims:  { name: "AIMS Hospital, Dombivli",         days: [1, 2, 3, 4, 5, 6], from: 12 * 60, to: 14 * 60, label: "12:00 – 2:00 PM" },
    lions: { name: "Lions Hospital, Koparkhairane",   days: [2, 4],             from: 16 * 60, to: 17 * 60, label: "4:00 – 5:00 PM" }
  };
  var DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function nowIST() {
    var parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Asia/Kolkata", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
    }).formatToParts(new Date());
    var map = {};
    parts.forEach(function (p) { map[p.type] = p.value; });
    var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(map.weekday);
    return { day: day, mins: (parseInt(map.hour, 10) % 24) * 60 + parseInt(map.minute, 10) };
  }

  function sessionsOn(day) {
    return Object.keys(SCHEDULE)
      .map(function (k) { return Object.assign({ key: k }, SCHEDULE[k]); })
      .filter(function (s) { return s.days.indexOf(day) > -1; })
      .sort(function (a, b) { return a.from - b.from; });
  }

  function nextSession(t) {
    var today = sessionsOn(t.day);
    for (var i = 0; i < today.length; i++) {
      if (t.mins < today[i].to) return { s: today[i], day: t.day, live: t.mins >= today[i].from, offset: 0 };
    }
    for (var d = 1; d <= 7; d++) {
      var day = (t.day + d) % 7, list = sessionsOn(day);
      if (list.length) return { s: list[0], day: day, live: false, offset: d };
    }
    return null;
  }

  function renderSchedule() {
    var t = nowIST();

    // Hero / widget "next session" cards
    var n = nextSession(t);
    document.querySelectorAll("[data-next-session]").forEach(function (el) {
      if (!n) return;
      var when = n.live ? "Consulting now" : n.offset === 0 ? "Today" : n.offset === 1 ? "Tomorrow" : DAY_NAMES[n.day];
      el.querySelector("[data-ns-when]").textContent = when + " · " + n.s.label;
      el.querySelector("[data-ns-where]").textContent = n.s.name;
      var dot = el.querySelector(".live-dot");
      if (dot) dot.classList.toggle("is-off", !n.live);
    });

    // Location cards
    document.querySelectorAll("[data-loc]").forEach(function (card) {
      var s = SCHEDULE[card.getAttribute("data-loc")];
      if (!s) return;
      var on = s.days.indexOf(t.day) > -1;
      var live = on && t.mins >= s.from && t.mins < s.to;
      card.classList.toggle("is-today", on);
      var status = card.querySelector(".loc__status");
      if (status) {
        status.textContent = live ? "● Consulting now" : on ? (t.mins < s.from ? "Today · " + s.label : "Done for today") : "Not today";
        status.classList.toggle("is-live", live);
      }
      card.querySelectorAll(".loc__days span").forEach(function (sp) {
        if (parseInt(sp.getAttribute("data-d"), 10) === t.day) sp.classList.add("today");
      });
    });

    // Timetable columns
    document.querySelectorAll(".timetable [data-d]").forEach(function (cell) {
      if (parseInt(cell.getAttribute("data-d"), 10) === t.day) cell.classList.add("today");
    });
  }

  /* ---------- Header + drawer ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var drawer = document.getElementById("drawer");
  var toggle = document.querySelector(".menu-toggle");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
    if (open) { var f = drawer.querySelector("a, button"); if (f) f.focus(); }
    else if (toggle) toggle.focus();
  }
  if (toggle) toggle.addEventListener("click", function () { setDrawer(true); });
  if (drawer) {
    drawer.querySelectorAll("[data-close]").forEach(function (el) {
      el.addEventListener("click", function () { setDrawer(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false);
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Count-up stats ---------- */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
    var started = false;
    new IntersectionObserver(function (entries, obs) {
      if (!entries[0].isIntersecting || started) return;
      started = true; obs.disconnect();
      var t0 = performance.now(), dur = 1200;
      (function tick(now) {
        var p = Math.min(1, (now - t0) / dur);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }).observe(el);
  });

  /* ---------- FAQ filter ---------- */
  var cats = document.querySelectorAll(".faq-cats button");
  cats.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = btn.getAttribute("data-cat");
      cats.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      document.querySelectorAll(".faq details").forEach(function (d) {
        d.hidden = !(cat === "all" || d.getAttribute("data-cat") === cat);
      });
    });
  });

  /* ---------- Misc ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  renderSchedule();
  setInterval(renderSchedule, 60 * 1000);
})();
