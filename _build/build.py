"""Static page builder for Dr. Sachin Gupta / Hope Kidney Care.
Usage: python build.py <output_dir>
"""
import sys, os, json

OUT = sys.argv[1]
SITE = "https://www.drsachingupta.in"
PHONE = "+918828888077"; PHONE_TXT = "88288 88077"
LANDLINE = "+912235119484"; LANDLINE_TXT = "022 3511 9484"
OSCAR = "+918989712323"; OSCAR_TXT = "89897 12323"
EMAIL = "info@drsachingupta.in"
WA = "https://wa.me/918828888077?text=" + "Hello%20Dr.%20Sachin%20Gupta%2C%20I%20would%20like%20to%20book%20a%20consultation."
ADDRESS = "Ground Floor, GM House, Opp. Jupiter Hospital, beside Lerida Hotel, Runwal Nagar, Eastern Express Highway, Thane (W), Maharashtra 400601"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + "Hope+Kidney+Care+GM+House+Runwal+Nagar+Eastern+Express+Highway+Thane+400601"

# ---------------------------------------------------------------- icons
ICONS = {
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "arrow": '<path d="M5 12h14M13 5l7 7-7 7"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
 "close": '<path d="M18 6 6 18M6 6l12 12"/>',
 "chev": '<path d="m9 18 6-6-6-6"/>',
 "kidney": '<path d="M10 5.5C9 3.6 6.4 3 4.7 4.4 2.5 6.2 2.3 10 3.3 13.2 4.4 16.6 7.2 19.5 10 18.6c1.7-.6 2-2.5 1-3.8-.6-.8-1-1.7-.6-2.6.3-.7 1-1 1.1-1.9.2-1.6-.5-3.5-1.5-4.8z"/><path d="M14 8c2-1.7 5-1 6 1.5 1.3 3.2.2 7.8-2.7 9.6-1.5.9-3.4.4-3.8-1.1"/><path d="M11.4 11.4c1.3-.2 2.1.5 2.6 1.6v8"/>',
 "droplet": '<path d="M12 2.7s6 6.4 6 11.3a6 6 0 0 1-12 0c0-4.9 6-11.3 6-11.3z"/><path d="M9 14a3 3 0 0 0 3 3"/>',
 "catheter": '<path d="M7 3v4a5 5 0 0 0 10 0V3"/><path d="M12 12v5a4 4 0 0 0 8 0v-1"/><circle cx="20" cy="14" r="2"/><path d="M5 3h4M15 3h4"/>',
 "steth": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
 "transplant": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/><path d="M12 5 9 8l2.5 2.5L14 8l2 2"/>',
 "filter": '<path d="M3 4h18l-7 8.5V19l-4 2v-8.5z"/>',
 "flask": '<path d="M9 3h6M10 3v6.5L4.6 18.4A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.4-2.6L14 9.5V3"/><path d="M7.5 15h9"/>',
 "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "peritoneal": '<path d="M12 3c4.5 0 8 3.5 8 8 0 5-4 10-8 10s-8-5-8-10c0-4.5 3.5-8 8-8z"/><path d="M8 12c1.3-1 2.7-1 4 0s2.7 1 4 0M8 15.5c1.3-1 2.7-1 4 0s2.7 1 4 0"/>',
 "hospital": '<path d="M12 6v4M14 8h-4M18 22V5a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v17"/><path d="M2 22h20M4 22V12h2M20 22V12h-2M10 22v-4h4v4"/>',
 "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 12.9 17 22l-5-3-5 3 1.5-9.1"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/>',
 "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
 "gauge": '<path d="M12 14 15.5 10.5"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
 "sugar": '<path d="M12 2 4 7v10l8 5 8-5V7z"/><path d="M12 22V12M20 7l-8 5-8-5"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "swell": '<path d="M7 3v8a5 5 0 0 0 10 0V3"/><path d="M5 21c2-1.5 4-1.5 7 0s5 1.5 7 0"/>',
 "tired": '<path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z"/>',
 "foam": '<circle cx="8" cy="9" r="3"/><circle cx="15.5" cy="7.5" r="2.5"/><circle cx="14" cy="15" r="4"/><circle cx="6.5" cy="16.5" r="2"/>',
 "quote": '<path d="M3 21c3 0 7-1 7-8V5H3v7h4c0 4-2 6-4 6zM14 21c3 0 7-1 7-8V5h-7v7h4c0 4-2 6-4 6z"/>',
 "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
 "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.6 8.6 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 8.5-8.5 8.4 8.4 0 0 1 8.5 8.5z"/>',
 "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
 "grad": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5M22 10v6"/>',
}
WA_PATH = '<path fill="currentColor" stroke="none" d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zM20.5 3.5A11.8 11.8 0 0 0 1.9 17.7L.2 24l6.4-1.7a11.8 11.8 0 0 0 5.6 1.4C18.8 23.7 24 18.4 24 11.9c0-3.2-1.2-6.1-3.5-8.4z"/>'

def sprite():
    syms = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items())
    syms += f'<symbol id="i-wa" viewBox="0 0 24 24">{WA_PATH}</symbol>'
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>'

def i(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"/></svg>'

EMBLEM = open(os.path.join(OUT, "assets/img/emblem.svg")).read()
def emblem(cls):
    # inline so gradients render everywhere; unique ids per use
    import re, random
    s = EMBLEM.replace('role="img" aria-label="Hope Kidney Care emblem"', f'class="{cls}" aria-hidden="true" focusable="false"')
    uid = cls.split()[0].replace("_", "")
    s = s.replace('id="d"', f'id="d-{uid}"').replace('url(#d)', f'url(#d-{uid})')
    s = s.replace('id="k"', f'id="k-{uid}"').replace('url(#k)', f'url(#k-{uid})')
    return s

def brand(extra=""):
    return f'''<a class="brand{extra}" href="index.html" aria-label="Hope Kidney Care — Dr. Sachin Gupta, home">
      <img class="brand__mark" src="assets/img/emblem.svg" alt="" width="46" height="46">
      <span class="brand__text"><span class="brand__word">Dr. Sachin Gupta</span><span class="brand__sub">Hope Kidney Care</span></span>
    </a>'''

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("hospitals.html", "Hospitals &amp; Timings"), ("faq.html", "FAQs"), ("contact.html", "Contact")]

def nav_links(active):
    return "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)

def head(title, desc, path, extra_ld=None):
    ld = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "Physician", "@id": SITE + "/#doctor", "name": "Dr. Sachin Gupta",
         "medicalSpecialty": "Nephrology", "description": "Consultant Nephrologist & Kidney Transplant Physician in Thane — MBBS, MD (Medicine), DNB (Nephrology).",
         "telephone": PHONE, "email": EMAIL, "url": SITE, "image": SITE + "/assets/img/og-image.png",
         "address": {"@type": "PostalAddress", "streetAddress": "Ground Floor, GM House, Opp. Jupiter Hospital, Runwal Nagar, Eastern Express Highway",
                     "addressLocality": "Thane", "addressRegion": "Maharashtra", "postalCode": "400601", "addressCountry": "IN"},
         "memberOf": ["Indian Society of Nephrology (ISN)", "Indian Society of Organ Transplantation (ISOT)", "AVATAR"]},
        {"@type": "MedicalClinic", "@id": SITE + "/#clinic", "name": "Hope Kidney Care", "telephone": PHONE,
         "address": {"@type": "PostalAddress", "streetAddress": "Ground Floor, GM House, Opp. Jupiter Hospital, Runwal Nagar, Eastern Express Highway",
                     "addressLocality": "Thane", "addressRegion": "Maharashtra", "postalCode": "400601", "addressCountry": "IN"},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "19:00", "closes": "21:00"}],
         "medicalSpecialty": "Nephrology"}
      ]}
    if extra_ld: ld["@graph"].append(extra_ld)
    return f'''<!DOCTYPE html>
<html lang="en-IN" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#2b2c30">
  <link rel="canonical" href="{SITE}/{'' if path == 'index.html' else path}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}/{'' if path == 'index.html' else path}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v=9">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script defer src="assets/js/site.js?v=4"></script>
</head>
<body>
{sprite()}
<a class="skip-link" href="#main">Skip to content</a>
'''

def header(active):
    return f'''
<div class="topbar">
  <div class="container">
    <div class="topbar__items">
      <span class="topbar__item">{i("clock")} Hope Kidney Care · Mon–Sat, 7–9 PM</span>
      <span class="topbar__item topbar__hide-sm">{i("pin")} Runwal Nagar, Thane (W)</span>
    </div>
    <div class="topbar__items">
      <a class="topbar__item" href="tel:{PHONE}">{i("phone")} {PHONE_TXT}</a>
      <a class="topbar__item topbar__hide-sm" href="mailto:{EMAIL}">{i("mail")} {EMAIL}</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="container">
    {brand()}
    <nav class="nav" aria-label="Main">{nav_links(active)}</nav>
    <div class="header-cta">
      <a class="btn btn--ghost btn--sm" href="tel:{PHONE}">{i("phone")} Call</a>
      <a class="btn btn--primary btn--sm" href="contact.html#book">{i("calendar")} Book appointment</a>
      <button class="menu-toggle" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{i("menu")}</button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__scrim" data-close></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer__head">{brand()}<button class="menu-toggle" style="display:inline-flex" type="button" aria-label="Close menu" data-close>{i("close")}</button></div>
    <nav aria-label="Mobile">{"".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}{i("chev")}</a>' for h, t in NAV)}</nav>
    <div class="drawer__contact">
      <a class="btn btn--primary" href="contact.html#book">{i("calendar")} Book appointment</a>
      <a class="btn btn--ghost" href="tel:{PHONE}">{i("phone")} {PHONE_TXT}</a>
    </div>
  </div>
</div>
<main id="main">
'''

def cta():
    return f'''
<section class="section" aria-label="Book a consultation">
  <div class="container">
    <div class="cta reveal">
      <span class="halftone halftone--gold"></span>
      <div>
        <span class="eyebrow">Book a consultation</span>
        <h2>Kidney care that starts with a conversation.</h2>
        <p>Call the clinic to fix a time at Hope Kidney Care or at any of Dr. Gupta's hospital OPDs. Bring your latest reports and your current list of medicines.</p>
      </div>
      <div class="cta__actions">
        <a class="cta__phone" href="tel:{PHONE}"><small>Clinic appointments</small>{PHONE_TXT}</a>
        <a class="btn btn--sun" href="contact.html#book">{i("calendar")} Request an appointment</a>
        <a class="btn btn--light" href="{WA}" target="_blank" rel="noopener">{i("wa")} WhatsApp the clinic</a>
      </div>
    </div>
  </div>
</section>'''

def footer():
    return f'''
</main>
<footer class="site-footer">
  <span class="halftone"></span>
  <div class="container">
    <div class="footer-grid">
      <div>
        {brand()}
        <p class="footer-about">Consultant Nephrologist &amp; Kidney Transplant Physician. MBBS, MD (Medicine), DNB (Nephrology) with over 13 years of experience caring for adults with kidney disease across Thane and Navi Mumbai.</p>
        <p style="font-size:13.5px">Medical Reg. No. 2009/03/1292</p>
      </div>
      <div>
        <h4>Explore</h4>
        <nav class="footer-links" aria-label="Footer">{nav_links("")}</nav>
      </div>
      <div>
        <h4>Consulting at</h4>
        <ul class="footer-links">
          <li><a href="hospitals.html#hope">Hope Kidney Care, Thane</a></li>
          <li><a href="hospitals.html#oscar">Oscar Hospital, Kasarvadavli</a></li>
          <li><a href="hospitals.html#aims">AIMS Hospital, Dombivli</a></li>
          <li><a href="hospitals.html#lions">Lions Hospital, Koparkhairane</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <div class="footer-contact">
          <div>{i("phone")}<span><a href="tel:{PHONE}">{PHONE_TXT}</a> · <a href="tel:{LANDLINE}">{LANDLINE_TXT}</a></span></div>
          <div>{i("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></div>
          <div>{i("pin")}<span>Hope Kidney Care, {ADDRESS}</span></div>
        </div>
      </div>
    </div>
    <p class="disclaimer">The information on this website is for general awareness and is not a substitute for a medical consultation. In an emergency, go to the nearest hospital emergency department.</p>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Dr. Sachin Gupta · Hope Kidney Care. All rights reserved.</span>
      <span>Thane · Dombivli · Navi Mumbai</span>
    </div>
  </div>
</footer>
<div class="fab">
  <a class="fab__wa" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{i("wa")}</a>
  <a class="fab__call" href="tel:{PHONE}" aria-label="Call the clinic">{i("phone")}</a>
</div>
<nav class="mobile-bar" aria-label="Quick actions">
  <a class="mb-call" href="tel:{PHONE}">{i("phone")} Call</a>
  <a class="mb-wa" href="{WA}" target="_blank" rel="noopener">{i("wa")} WhatsApp</a>
  <a class="mb-book" href="contact.html#book">{i("calendar")} Book</a>
</nav>
</body>
</html>
'''

def page_hero(crumb, eyebrow, h1, lead):
    return f'''
<section class="page-hero">
  <span class="halftone"></span>
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a>{i("chev")}<span aria-current="page">{crumb}</span></div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>'''

# ---------------------------------------------------------------- shared content
SPECIALITIES = [
 ("kidney", "Chronic Kidney Disease", "Slowing progression with blood-pressure, sugar and diet control, and planning ahead for every stage of CKD."),
 ("droplet", "Haemodialysis", "Safe, comfortable dialysis with regular adequacy checks, access care and a plan built around your week."),
 ("transplant", "Kidney Transplantation", "Pre-transplant work-up, donor evaluation and lifelong post-transplant follow-up and immunosuppression."),
 ("peritoneal", "Peritoneal Dialysis", "Home-based dialysis — training, catheter care and monitoring so treatment fits your life."),
 ("pulse", "Acute Kidney Injury", "Rapid diagnosis and treatment of sudden loss of kidney function, including in ICU and hospital settings."),
 ("filter", "Glomerular Diseases", "Evaluation of protein or blood in urine, nephrotic and nephritic syndromes, with biopsy-guided treatment."),
 ("flask", "Electrolyte Disorders", "Diagnosis and correction of sodium, potassium, calcium and acid–base imbalances."),
 ("gauge", "Kidney &amp; Hypertension", "Managing high blood pressure that damages kidneys — and kidney problems that raise blood pressure."),
]
CONDITIONS = [
 ("CKD", "Chronic Kidney Disease", "Gradual loss of kidney function over months or years."),
 ("AKI", "Acute Kidney Injury", "A sudden drop in kidney function that needs urgent care."),
 ("HTN", "Hypertension", "High blood pressure — a leading cause and result of kidney disease."),
 ("DKD", "Diabetic Kidney Disease", "Kidney damage from long-standing diabetes."),
 ("KTx", "Kidney Transplant", "Evaluation, transplant planning and lifelong follow-up."),
]
LOCATIONS = [
 dict(key="hope", primary=True, name="Hope Kidney Care", area="Dr. Gupta's own clinic · Runwal Nagar, Thane (W)",
      time="7:00 – 9:00 PM", short="7–9 PM", days=[1,2,3,4,5,6], daytxt="Monday to Saturday",
      addr="Ground Floor, GM House, Opp. Jupiter Hospital, beside Lerida Hotel, Eastern Express Highway, Thane 400601",
      phone=(PHONE, PHONE_TXT), note=None, map=MAPS),
 dict(key="oscar", primary=False, name="Oscar Hospital", area="Kasarvadavli, Ghodbunder Road, Thane (W)",
      time="10:00 – 11:00 AM", short="10–11 AM", days=[1,2,3,4,5,6], daytxt="Monday to Saturday",
      addr=None, phone=(OSCAR, OSCAR_TXT), note="By prior appointment only",
      map="https://www.google.com/maps/search/?api=1&query=Oscar+Hospital+Kasarvadavli+Thane"),
 dict(key="aims", primary=False, name="AIMS Hospital", area="Dombivli",
      time="12:00 – 2:00 PM", short="12–2 PM", days=[1,2,3,4,5,6], daytxt="Monday to Saturday",
      addr=None, phone=(PHONE, PHONE_TXT), note=None,
      map="https://www.google.com/maps/search/?api=1&query=AIMS+Hospital+Dombivli"),
 dict(key="lions", primary=False, name="Lions Hospital", area="Koparkhairane, Navi Mumbai",
      time="4:00 – 5:00 PM", short="4–5 PM", days=[2,4], daytxt="Tuesday &amp; Thursday",
      addr=None, phone=(PHONE, PHONE_TXT), note=None,
      map="https://www.google.com/maps/search/?api=1&query=Lions+Hospital+Koparkhairane+Navi+Mumbai"),
]
HOSPITALS = [
 ("AIMS Hospital", "Dombivli"), ("Jupiter Hospital", "Thane"), ("Nector Hospital", "Thane region"),
 ("Lakecity Hospital", "Thane"), ("Oscar Hospital", "Kasarvadavli, Thane"), ("Siddhivinayak Hospital", "Thane"),
 ("Lions Hospital", "Koparkhairane, Navi Mumbai"),
]
MEMBERS = [
 ("ISN", "Indian Society of Nephrology", "Life Member · ISN India"),
 ("ISOT", "Indian Society of Organ Transplantation", "Life Member"),
 ("AVATAR", "AVATAR", "Life Member"),
]
DAYS = [(1,"Mon"),(2,"Tue"),(3,"Wed"),(4,"Thu"),(5,"Fri"),(6,"Sat"),(0,"Sun")]

def loc_card(l, delay=0):
    days = "".join(f'<span data-d="{d}" class="{"on" if d in l["days"] else ""}" title="{n}">{n[:2]}</span>' for d, n in DAYS)
    note = f'<div>{i("alert")}<span><strong>{l["note"]}</strong></span></div>' if l["note"] else ""
    addr = f'<div>{i("pin")}<span>{l["addr"]}</span></div>' if l["addr"] else ""
    return f'''
      <article class="loc reveal{" loc--primary" if l["primary"] else ""}" id="{l["key"]}" data-loc="{l["key"]}" style="--d:{delay}s">
        <span class="loc__status">{l["daytxt"]}</span>
        <div class="loc__pin">{i("hospital" if not l["primary"] else "kidney")}</div>
        <div>
          <h3>{l["name"]}</h3>
          <p class="loc__area">{l["area"]}</p>
          <div class="loc__meta">
            <div>{i("clock")}<span><strong>{l["time"]}</strong> · {l["daytxt"]}</span></div>
            {note}{addr}
          </div>
          <div class="loc__days" aria-label="Consulting days">{days}</div>
          <div class="btn-row">
            <a class="btn btn--primary" href="tel:{l["phone"][0]}">{i("phone")} {l["phone"][1]}</a>
            <a class="btn btn--ghost" href="{l["map"]}" target="_blank" rel="noopener">{i("pin")} Directions</a>
          </div>
        </div>
      </article>'''

def write(name, html):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)

# ================================================================ HOME
home = head("Dr. Sachin Gupta — Nephrologist &amp; Kidney Transplant Physician in Thane | Hope Kidney Care",
            "Dr. Sachin Gupta, MBBS, MD, DNB (Nephrology) — consultant nephrologist and kidney transplant physician in Thane with 13+ years of experience. CKD, dialysis, AKI, transplant care at Hope Kidney Care.",
            "index.html") + header("index.html") + f'''
<section class="hero">
  <div class="container hero__grid">
    <div>
      <div class="hero__badge reveal"><span class="dot">{i("kidney")}</span> Consultant Nephrologist · Thane</div>
      <h1 class="reveal" style="--d:.05s"><span class="thin">Dr. Sachin Gupta</span>Kidney care, with <span class="text-sun">hope</span> at the centre.</h1>
      <div class="hero__creds reveal" style="--d:.1s">
        <span class="chip chip--sun">MBBS</span><span class="chip chip--sun">MD (Medicine)</span><span class="chip chip--sun">DNB (Nephrology)</span>
        <span class="chip">Kidney Transplant Physician</span>
      </div>
      <p class="lead hero__lead reveal" style="--d:.15s">Expert, unhurried care for chronic kidney disease, dialysis, acute kidney injury and kidney transplantation — for adults across Thane, Dombivli and Navi Mumbai.</p>
      <div class="btn-row reveal" style="--d:.2s">
        <a class="btn btn--primary" href="contact.html#book">{i("calendar")} Book a consultation</a>
        <a class="btn btn--ghost" href="tel:{PHONE}">{i("phone")} {PHONE_TXT}</a>
      </div>
      <div class="hero__stats reveal" style="--d:.25s">
        <div class="stat"><div class="stat__num"><span data-count="13">13</span><sup>+</sup></div><div class="stat__label">Years in<br>practice</div></div>
        <div class="stat"><div class="stat__num"><span data-count="7">7</span></div><div class="stat__label">Hospital<br>associations</div></div>
        <div class="stat"><div class="stat__num"><span data-count="4">4</span></div><div class="stat__label">Weekly OPD<br>locations</div></div>
      </div>
    </div>
    <div class="hero__visual" aria-hidden="true">
      <div class="hero__disc"></div>
      <span class="halftone"></span>
      {emblem("hero__emblem")}
    </div>
  </div>
</section>

<div class="trust" aria-label="Hospital associations">
  <div class="container trust__row">
    <span class="trust__label">Attached to</span>
    <div class="marquee"><div class="marquee__track">
      {"".join(f'<span class="marquee__item">{h} <small style="font-weight:500;color:var(--muted)">{a}</small></span>' for h, a in HOSPITALS * 2)}
    </div></div>
  </div>
</div>

<section class="section">
  <div class="container split">
    <div class="profile-card reveal">
      <span class="halftone halftone--gold"></span>
      <img class="profile-card__mark" src="assets/img/emblem.svg" alt="" width="74" height="74">
      <div class="profile-card__name">Dr. Sachin Gupta</div>
      <div class="profile-card__role">Consultant Nephrologist &amp; Kidney Transplant Physician</div>
      <dl>
        <div><dt>Degrees</dt><dd>MBBS · MD (General Medicine) · DNB (Nephrology)</dd></div>
        <div><dt>Experience</dt><dd>13+ years</dd></div>
        <div><dt>Treats</dt><dd>Adult nephrology patients</dd></div>
        <div><dt>Reg. No.</dt><dd>2009/03/1292</dd></div>
      </dl>
    </div>
    <div class="reveal" style="--d:.1s">
      <span class="eyebrow">About Dr. Gupta</span>
      <h2>A kidney specialist who plans for the long run — with you.</h2>
      <p class="lead">Kidney disease is rarely a one-visit problem. Dr. Sachin Gupta combines a grounding in internal medicine with specialist training in nephrology to look after the whole person — blood pressure, sugar, heart and kidneys together.</p>
      <ul class="checklist">
        <li><span class="tick">{i("check")}</span><div><strong>Clear explanations</strong><span>Reports, stages and options explained in plain language, so you can decide with confidence.</span></div></li>
        <li><span class="tick">{i("check")}</span><div><strong>One doctor, every stage</strong><span>From early CKD to dialysis and transplant, continuity with the same specialist.</span></div></li>
        <li><span class="tick">{i("check")}</span><div><strong>Close to home</strong><span>OPDs in Thane, Kasarvadavli, Dombivli and Koparkhairane through the week.</span></div></li>
      </ul>
      <a class="link-arrow" href="about.html">Read Dr. Gupta's profile {i("arrow")}</a>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Services</span>
      <h2>What we do at Hope Kidney Care</h2>
      <p class="lead">Specialist consultation, dialysis and vascular access — coordinated with the hospitals where Dr. Gupta consults.</p>
    </div>
    <div class="service-feature">
      <article class="svc reveal"><span class="halftone"></span>
        <div class="svc__tag">01 · Consultation</div>
        <h3>Nephrology consultation</h3>
        <p>A thorough review of your symptoms, reports and medicines, with a written plan you can follow.</p>
        <ul><li>CKD staging &amp; follow-up</li><li>Blood pressure &amp; diabetes with kidney involvement</li><li>Second opinions</li></ul>
        <a class="link-arrow" href="services.html#consultation">Learn more {i("arrow")}</a>
      </article>
      <article class="svc reveal" style="--d:.08s"><span class="halftone halftone--gold"></span>
        <div class="svc__tag">02 · Dialysis</div>
        <h3>Haemodialysis &amp; PD</h3>
        <p>Dialysis planned around your routine, with regular monitoring and attention to comfort.</p>
        <ul><li>Maintenance haemodialysis</li><li>Peritoneal (home) dialysis</li><li>Emergency dialysis in hospital</li></ul>
        <a class="link-arrow" href="services.html#dialysis">Learn more {i("arrow")}</a>
      </article>
      <article class="svc reveal" style="--d:.16s"><span class="halftone"></span>
        <div class="svc__tag">03 · Access</div>
        <h3>Perm cath insertion</h3>
        <p>Tunnelled (permanent) dialysis catheter placement for reliable, longer-term dialysis access.</p>
        <ul><li>Planned &amp; urgent insertions</li><li>Catheter care guidance</li><li>Access review &amp; follow-up</li></ul>
        <a class="link-arrow" href="services.html#permcath">Learn more {i("arrow")}</a>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Areas of expertise</span>
      <h2>Complete care for the kidneys</h2>
      <p class="lead">From the first abnormal report to transplant and beyond.</p>
    </div>
    <div class="grid grid--4">
      {"".join(f'<article class="card reveal" style="--d:{(n%4)*0.06:.2f}s"><div class="card__icon">{i(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for n, (ic, t, d) in enumerate(SPECIALITIES))}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Common conditions</span>
      <h2>Conditions Dr. Gupta treats every day</h2>
    </div>
    <div class="conditions">
      {"".join(f'<article class="condition reveal" style="--d:{n*0.05:.2f}s"><div class="condition__abbr text-sun">{a}</div><h3>{t}</h3><p>{d}</p></article>' for n, (a, t, d) in enumerate(CONDITIONS))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Your first visit</span>
      <h2>What to expect</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="step__num">1</div><h3>Book</h3><p>Call or WhatsApp the clinic and choose the location and time that suit you.</p></div>
      <div class="step reveal" style="--d:.06s"><div class="step__num">2</div><h3>Bring your reports</h3><p>Blood and urine tests, scans, discharge summaries and your current medicines.</p></div>
      <div class="step reveal" style="--d:.12s"><div class="step__num">3</div><h3>Consult</h3><p>A detailed assessment, a clear explanation of where things stand and what comes next.</p></div>
      <div class="step reveal" style="--d:.18s"><div class="step__num">4</div><h3>Follow up</h3><p>A written plan, scheduled reviews and the same doctor watching your progress.</p></div>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="container">
    <div class="section-head reveal" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px;max-width:none">
      <div style="max-width:640px"><span class="eyebrow">Where to consult</span><h2 class="mb-0">Four locations, every week</h2></div>
      <a class="link-arrow" href="hospitals.html">Full weekly timetable {i("arrow")}</a>
    </div>
    <div class="locations">{"".join(loc_card(l, n*0.06) for n, l in enumerate(LOCATIONS))}</div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Professional memberships</span>
      <h2>Part of India's nephrology &amp; transplant community</h2>
    </div>
    <div class="badges">
      {"".join(f'<div class="member reveal" style="--d:{n*0.06:.2f}s"><div class="member__seal{' member__seal--long' if len(a) > 4 else ''}">{a}</div><div><strong>{t}</strong><span>{s}</span></div></div>' for n, (a, t, s) in enumerate(MEMBERS))}
    </div>
  </div>
</section>
''' + cta() + footer()
write("index.html", home)

# ================================================================ ABOUT
about = head("About Dr. Sachin Gupta — Nephrologist in Thane | Hope Kidney Care",
             "Meet Dr. Sachin Gupta, MBBS, MD (General Medicine), DNB (Nephrology) — consultant nephrologist and kidney transplant physician with 13+ years of experience in Thane.",
             "about.html") + header("about.html") + page_hero(
    "About", "About Dr. Sachin Gupta",
    "Specialist kidney care, built on <span class=\"text-sun\">13+ years</span> of practice.",
    "Consultant Nephrologist &amp; Kidney Transplant Physician, and founder of Hope Kidney Care in Thane.") + f'''
<section class="section" style="padding-top:0">
  <div class="container split split--wide-left">
    <div class="reveal">
      <h2>Medicine first. Then the kidneys.</h2>
      <p class="lead">Dr. Sachin Gupta trained in general medicine before specialising in nephrology. That background shapes how he practises: kidney disease is treated alongside the blood pressure, diabetes, heart health and everyday routines that affect it.</p>
      <p>Over more than 13 years, Dr. Gupta has cared for adults at every stage of kidney disease — from an unexpected creatinine report to long-term dialysis and kidney transplantation. He consults at his own clinic, Hope Kidney Care in Thane, and is attached to seven hospitals across Thane, Dombivli and Navi Mumbai, which allows him to follow patients from OPD to ward to dialysis unit.</p>
      <p>His areas of focus include chronic kidney disease, haemodialysis and peritoneal dialysis, acute kidney injury, glomerular diseases, electrolyte disorders and kidney transplantation.</p>
    </div>
    <div class="profile-card reveal" style="--d:.1s">
      <span class="halftone halftone--gold"></span>
      <img class="profile-card__mark" src="assets/img/emblem.svg" alt="" width="74" height="74">
      <div class="profile-card__name">Dr. Sachin Gupta</div>
      <div class="profile-card__role">MBBS, MD (Medicine), DNB (Nephrology)</div>
      <dl>
        <div><dt>Role</dt><dd>Consultant Nephrologist &amp; Kidney Transplant Physician</dd></div>
        <div><dt>Clinic</dt><dd>Hope Kidney Care, Thane</dd></div>
        <div><dt>Experience</dt><dd>13+ years</dd></div>
        <div><dt>Patients</dt><dd>Adults</dd></div>
        <div><dt>Reg. No.</dt><dd>2009/03/1292</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Qualifications</span>
      <h2>Education &amp; training</h2>
      <p class="lead">A full medical foundation, followed by national board certification in nephrology.</p>
    </div>
    <div class="timeline reveal" style="--d:.1s">
      <div class="tl"><span class="tl__tag">Super-speciality</span><h3>DNB — Nephrology</h3><p>Diplomate of National Board in Nephrology: dialysis, transplantation, glomerular and critical-care nephrology.</p></div>
      <div class="tl"><span class="tl__tag">Post-graduation</span><h3>MD — General Medicine</h3><p>Internal medicine training covering diabetes, hypertension, cardiac and critical-care medicine.</p></div>
      <div class="tl"><span class="tl__tag">Graduation</span><h3>MBBS</h3><p>Bachelor of Medicine and Bachelor of Surgery.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Approach to care</span>
      <h2>How Dr. Gupta looks after patients</h2>
    </div>
    <div class="grid grid--3">
      <article class="card reveal"><div class="card__icon">{i("chat")}</div><h3>Explain, then decide</h3><p>Every report and option is explained clearly, so patients and families can take part in each decision.</p></article>
      <article class="card reveal" style="--d:.06s"><div class="card__icon">{i("shield")}</div><h3>Protect what's left</h3><p>Early, steady control of blood pressure, sugar, diet and medicines to preserve kidney function for as long as possible.</p></article>
      <article class="card reveal" style="--d:.12s"><div class="card__icon">{i("calendar")}</div><h3>Plan ahead</h3><p>When dialysis or transplant may be needed, planning starts early — so the next step is calm, not an emergency.</p></article>
    </div>
    <div class="quote reveal" style="margin-top:28px">
      <svg class="quote__mark" aria-hidden="true"><use href="#i-quote"/></svg>
      <blockquote>Kidney disease is a long journey. No patient should walk it without a plan — or without hope.</blockquote>
      <cite>— The Hope Kidney Care promise</cite>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Hospital associations</span>
      <h2>Attached to seven hospitals</h2>
      <p class="lead">Admissions, dialysis and transplant care are coordinated with these hospitals across Thane, Dombivli and Navi Mumbai.</p>
    </div>
    <div class="hospitals">
      {"".join(f'<div class="hospital reveal" style="--d:{n*0.04:.2f}s"><div class="hospital__icon">{i("hospital")}</div><div><strong>{h}</strong><span>{a}</span></div></div>' for n, (h, a) in enumerate(HOSPITALS))}
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Memberships</span><h2>Professional memberships</h2></div>
    <div class="badges">
      {"".join(f'<div class="member reveal" style="--d:{n*0.06:.2f}s"><div class="member__seal{' member__seal--long' if len(a) > 4 else ''}">{a}</div><div><strong>{t}</strong><span>{s}</span></div></div>' for n, (a, t, s) in enumerate(MEMBERS))}
    </div>
  </div>
</section>
''' + cta() + footer()
write("about.html", about)

# ================================================================ SERVICES
services = head("Nephrology Services — Dialysis, CKD, Transplant | Dr. Sachin Gupta, Thane",
                "Nephrology consultation, haemodialysis, peritoneal dialysis, perm cath insertion, CKD, AKI and kidney transplant care by Dr. Sachin Gupta at Hope Kidney Care, Thane.",
                "services.html") + header("services.html") + page_hero(
    "Services", "Services &amp; patient care",
    "Specialist kidney care for adults.",
    "Consultation, dialysis and vascular access — with continuity from the clinic to the hospital and back home.") + f'''
<section class="section" style="padding-top:0">
  <div class="container stack-lg">
    <div class="split" id="consultation">
      <div class="reveal">
        <span class="eyebrow">01 · Consultation</span>
        <h2>Nephrology consultation</h2>
        <p class="lead">A complete assessment of your kidney health — history, examination, reports and medicines — ending with a clear, written plan.</p>
        <ul class="checklist">
          <li><span class="tick">{i("check")}</span><div><strong>New kidney problems</strong><span>Raised creatinine, protein or blood in urine, swelling, reduced urine output.</span></div></li>
          <li><span class="tick">{i("check")}</span><div><strong>Ongoing CKD care</strong><span>Staging, diet and medicine review, anaemia and bone-health management.</span></div></li>
          <li><span class="tick">{i("check")}</span><div><strong>BP &amp; diabetes with kidney involvement</strong><span>Medicines chosen to protect the kidneys as well as control numbers.</span></div></li>
        </ul>
      </div>
      <div class="card reveal" style="--d:.1s">
        <div class="card__icon">{i("steth")}</div>
        <h3>Bring to your consultation</h3>
        <ul class="checklist" style="margin-bottom:0">
          <li><span class="tick">{i("check")}</span><span>Recent blood tests (creatinine, urea, electrolytes, haemoglobin)</span></li>
          <li><span class="tick">{i("check")}</span><span>Urine reports and any ultrasound or scan reports</span></li>
          <li><span class="tick">{i("check")}</span><span>Discharge summaries from earlier hospital stays</span></li>
          <li><span class="tick">{i("check")}</span><span>All current medicines, including over-the-counter and herbal</span></li>
        </ul>
      </div>
    </div>

    <div class="split" id="dialysis">
      <div class="card reveal" style="order:0">
        <div class="card__icon">{i("droplet")}</div>
        <h3>Two kinds of dialysis</h3>
        <p><strong style="color:var(--ink)">Haemodialysis</strong> filters the blood through a machine, usually three times a week at a dialysis unit.</p>
        <p class="mb-0"><strong style="color:var(--ink)">Peritoneal dialysis (PD)</strong> uses the lining of the abdomen as a natural filter and can be done at home after training.</p>
      </div>
      <div class="reveal" style="--d:.1s">
        <span class="eyebrow">02 · Dialysis</span>
        <h2>Haemodialysis &amp; peritoneal dialysis</h2>
        <p class="lead">When the kidneys can no longer keep up, dialysis takes over their work. Dr. Gupta helps you choose the right type and keeps it safe and effective over time.</p>
        <ul class="checklist">
          <li><span class="tick">{i("check")}</span><div><strong>Planned start</strong><span>Counselling and access creation before dialysis is urgently needed.</span></div></li>
          <li><span class="tick">{i("check")}</span><div><strong>Regular adequacy checks</strong><span>Blood tests and dose adjustments so dialysis keeps working well.</span></div></li>
          <li><span class="tick">{i("check")}</span><div><strong>Emergency dialysis</strong><span>For acute kidney injury and critical illness at attached hospitals.</span></div></li>
        </ul>
      </div>
    </div>

    <div class="split" id="permcath">
      <div class="reveal">
        <span class="eyebrow">03 · Vascular access</span>
        <h2>Perm cath insertion</h2>
        <p class="lead">A perm cath (tunnelled dialysis catheter) is a soft tube placed in a large neck vein and tunnelled under the skin, giving reliable access for haemodialysis over weeks to months.</p>
        <ul class="checklist">
          <li><span class="tick">{i("check")}</span><div><strong>When it's used</strong><span>While a fistula matures, or when longer-term access is needed quickly.</span></div></li>
          <li><span class="tick">{i("check")}</span><div><strong>Care afterwards</strong><span>Keep the site clean and dry; report fever, redness or discharge promptly.</span></div></li>
        </ul>
      </div>
      <div class="card reveal" style="--d:.1s">
        <div class="card__icon">{i("catheter")}</div>
        <h3>Performed at attached hospitals</h3>
        <p>Perm cath insertions are done in a hospital setting under local anaesthesia. Call the clinic to plan the procedure and the hospital most convenient for you.</p>
        <a class="link-arrow" href="contact.html#book">Plan a procedure {i("arrow")}</a>
      </div>
    </div>

    <div class="split" id="transplant">
      <div class="card reveal">
        <div class="card__icon">{i("transplant")}</div>
        <h3>Across the transplant journey</h3>
        <ul class="checklist" style="margin-bottom:0">
          <li><span class="tick">{i("check")}</span><span>Recipient evaluation and fitness for transplant</span></li>
          <li><span class="tick">{i("check")}</span><span>Living-donor assessment and counselling</span></li>
          <li><span class="tick">{i("check")}</span><span>Post-transplant immunosuppression and monitoring</span></li>
          <li><span class="tick">{i("check")}</span><span>Long-term follow-up to protect the new kidney</span></li>
        </ul>
      </div>
      <div class="reveal" style="--d:.1s">
        <span class="eyebrow">04 · Transplant</span>
        <h2>Kidney transplantation</h2>
        <p class="lead">For many people with kidney failure, a transplant offers the best quality of life. As a kidney transplant physician, Dr. Gupta prepares patients and donors for transplant and looks after the new kidney for life.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Areas of expertise</span>
      <h2>Specialities</h2>
    </div>
    <div class="grid grid--4">
      {"".join(f'<article class="card reveal" style="--d:{(n%4)*0.06:.2f}s"><div class="card__icon">{i(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for n, (ic, t, d) in enumerate(SPECIALITIES))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">When to see a nephrologist</span>
      <h2>Signs your kidneys may need attention</h2>
      <p class="lead">Kidney disease is often silent early on. See a nephrologist if you notice any of these — or if you have diabetes or high blood pressure and haven't had your kidneys checked.</p>
    </div>
    <div class="signs">
      <div class="sign reveal">{i("swell")}Swelling of feet, ankles or face</div>
      <div class="sign reveal" style="--d:.04s">{i("foam")}Foamy or frothy urine</div>
      <div class="sign reveal" style="--d:.08s">{i("droplet")}Blood in urine, or much less urine</div>
      <div class="sign reveal" style="--d:.12s">{i("gauge")}High BP that's hard to control</div>
      <div class="sign reveal">{i("flask")}Raised creatinine or urea on a report</div>
      <div class="sign reveal" style="--d:.04s">{i("tired")}Unusual tiredness, poor appetite, nausea</div>
      <div class="sign reveal" style="--d:.08s">{i("sugar")}Diabetes for 5+ years</div>
      <div class="sign reveal" style="--d:.12s">{i("user")}Family history of kidney disease</div>
    </div>
    <div class="notice reveal" style="margin-top:24px">{i("alert")}<span>Patients treated: <strong>adults</strong>. For children with kidney problems, please consult a paediatric nephrologist.</span></div>
  </div>
</section>
''' + cta() + footer()
write("services.html", services)

# ================================================================ HOSPITALS & TIMINGS
rows = ""
for l in LOCATIONS:
    cells = "".join(f'<td data-d="{d}">' + (f'<span class="slot">{l["short"]}</span>' if d in l["days"] else '<span class="slot slot--off">—</span>') + "</td>" for d, _ in DAYS)
    rows += f'<tr><th scope="row">{l["name"]}<small>{l["area"].split("·")[-1].strip()}</small></th>{cells}</tr>'
hosp = head("Hospitals &amp; OPD Timings — Dr. Sachin Gupta, Nephrologist Thane",
            "Weekly consultation timings for Dr. Sachin Gupta at Hope Kidney Care Thane, Oscar Hospital Kasarvadavli, AIMS Hospital Dombivli and Lions Hospital Koparkhairane.",
            "hospitals.html") + header("hospitals.html") + page_hero(
    "Hospitals &amp; Timings", "Where to consult",
    "OPD timings &amp; hospital associations",
    "Dr. Gupta consults at four locations every week. Today's sessions are highlighted automatically.") + f'''
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="locations">{"".join(loc_card(l, n*0.06) for n, l in enumerate(LOCATIONS))}</div>
  </div>
</section>

<section class="section section--white">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Weekly timetable</span>
      <h2>The week at a glance</h2>
      <p class="lead">Timings can change on public holidays — please call before visiting.</p>
    </div>
    <div class="timetable-wrap reveal">
      <table class="timetable">
        <caption class="visually-hidden">Dr. Sachin Gupta weekly consultation timetable</caption>
        <thead><tr><th scope="col" style="text-align:left">Location</th>{"".join(f'<th scope="col" data-d="{d}">{n}</th>' for d, n in DAYS)}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <div class="notice reveal" style="margin-top:20px">{i("alert")}<span>Oscar Hospital OPD is <strong>by prior appointment only</strong> — call <a href="tel:{OSCAR}" style="font-weight:700">{OSCAR_TXT}</a>. For all other locations, call the clinic on <a href="tel:{PHONE}" style="font-weight:700">{PHONE_TXT}</a>.</span></div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Hospital associations</span>
      <h2>Attached hospitals</h2>
      <p class="lead">For admissions, dialysis, procedures and transplant care.</p>
    </div>
    <div class="hospitals">
      {"".join(f'<div class="hospital reveal" style="--d:{n*0.04:.2f}s"><div class="hospital__icon">{i("hospital")}</div><div><strong>{h}</strong><span>{a}</span></div></div>' for n, (h, a) in enumerate(HOSPITALS))}
    </div>
  </div>
</section>
''' + cta() + footer()
write("hospitals.html", hosp)

# ================================================================ FAQ
FAQS = [
 ("general", "What does a nephrologist treat?", "A nephrologist is a doctor who specialises in the kidneys. This includes chronic kidney disease, acute kidney injury, kidney-related high blood pressure, diabetic kidney disease, protein or blood in the urine, electrolyte problems, dialysis and kidney transplant care."),
 ("general", "When should I see a nephrologist instead of my family doctor?", "If your creatinine is raised, your urine shows protein or blood, you have swelling, your blood pressure is hard to control, or you have had diabetes for many years, a nephrologist can find the cause and plan treatment. Your family doctor may also refer you."),
 ("general", "Does Dr. Gupta treat children?", "Dr. Sachin Gupta treats adult nephrology patients. For children with kidney problems, please consult a paediatric nephrologist."),
 ("ckd", "Can chronic kidney disease be reversed?", "Lost kidney function usually cannot be fully regained, but the progression of CKD can often be slowed significantly. Good control of blood pressure and sugar, the right medicines, diet changes and avoiding kidney-harming drugs all make a real difference — especially when started early."),
 ("ckd", "What do my creatinine and eGFR numbers mean?", "Creatinine is a waste product the kidneys clear from the blood; eGFR is an estimate of how well the kidneys are filtering, calculated from creatinine, age and sex. A lower eGFR means lower kidney function. Dr. Gupta will explain your numbers and your CKD stage at the consultation."),
 ("ckd", "Are painkillers safe for my kidneys?", "Common painkillers such as NSAIDs (for example ibuprofen and diclofenac) can harm the kidneys, especially in people with CKD, diabetes or dehydration. Always check with your doctor before taking regular painkillers or herbal remedies."),
 ("dialysis", "Does starting dialysis mean my kidneys will never work again?", "Not always. In acute kidney injury, dialysis may be needed only for a short time while the kidneys recover. In advanced chronic kidney disease, dialysis is usually long-term unless a kidney transplant is done."),
 ("dialysis", "What is the difference between haemodialysis and peritoneal dialysis?", "Haemodialysis cleans the blood using a machine, usually three sessions a week at a dialysis unit. Peritoneal dialysis uses the lining of your abdomen as a filter and can be done at home every day after training. The right choice depends on your health, lifestyle and preferences."),
 ("dialysis", "What is a perm cath?", "A perm cath is a tunnelled dialysis catheter placed into a large vein in the neck and run under the skin. It gives reliable access for haemodialysis while a fistula matures or when longer-term access is needed quickly. Keep the site clean and dry, and report fever or redness promptly."),
 ("transplant", "Who can get a kidney transplant?", "Many people with kidney failure can be considered for a transplant after a careful evaluation of their heart, infections, other illnesses and overall fitness. A suitable living donor (often a family member) or a deceased-donor kidney is needed."),
 ("transplant", "What care is needed after a kidney transplant?", "After a transplant you will take anti-rejection (immunosuppressive) medicines every day and need regular blood tests and reviews for life. Long-term follow-up helps protect the new kidney and catch problems early."),
 ("visit", "How do I book an appointment?", f"Call or WhatsApp the clinic on {PHONE_TXT}. For Oscar Hospital, Kasarvadavli, call {OSCAR_TXT} — appointments there are by prior booking only. "),
 ("visit", "What should I bring to my first consultation?", "Bring your recent blood and urine reports, any ultrasound or scan reports, discharge summaries from past hospital stays, and a list (or the strips) of every medicine you currently take."),
]
CATS = [("all", "All"), ("general", "General"), ("ckd", "CKD"), ("dialysis", "Dialysis"), ("transplant", "Transplant"), ("visit", "Your visit")]
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in FAQS]}
faq = head("Kidney Health FAQs — Dr. Sachin Gupta, Nephrologist Thane",
           "Answers to common questions about chronic kidney disease, dialysis, perm cath, kidney transplant and booking a consultation with Dr. Sachin Gupta.",
           "faq.html", faq_ld) + header("faq.html") + page_hero(
    "FAQs", "Frequently asked questions",
    "Your kidney questions, answered.",
    "General information to help you understand kidney health. For advice about your own condition, please book a consultation.") + f'''
<section class="section" style="padding-top:0">
  <div class="container" style="max-width:900px">
    <div class="faq-cats reveal" role="group" aria-label="Filter questions">
      {"".join(f'<button type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{t}</button>' for k, t in CATS)}
    </div>
    <div class="faq">
      {"".join(f'<details class="reveal" data-cat="{c}"{" open" if n == 0 else ""}><summary>{q}</summary><div class="faq__body"><p>{a}</p></div></details>' for n, (c, q, a) in enumerate(FAQS))}
    </div>
    <div class="notice reveal" style="margin-top:28px">{i("chat")}<span>Didn't find your question? <a href="{WA}" target="_blank" rel="noopener" style="font-weight:700">WhatsApp the clinic</a> or call <a href="tel:{PHONE}" style="font-weight:700">{PHONE_TXT}</a>.</span></div>
  </div>
</section>
''' + cta() + footer()
write("faq.html", faq)

# ================================================================ CONTACT
contact = head("Contact &amp; Book Appointment — Dr. Sachin Gupta, Hope Kidney Care Thane",
               "Book an appointment with Dr. Sachin Gupta, nephrologist in Thane. Call 88288 88077 or visit Hope Kidney Care, GM House, Runwal Nagar, Thane (W).",
               "contact.html") + header("contact.html") + page_hero(
    "Contact", "Contact &amp; appointments",
    "Book a consultation",
    "Call or WhatsApp the clinic — the team will confirm your slot.") + f'''
<section class="section" style="padding-top:0;padding-bottom:24px" id="book">
  <div class="container">
    <div class="contact-tiles">
      <a class="tile reveal" href="tel:{PHONE}"><div class="tile__icon">{i("phone")}</div><div><small>Clinic appointments</small><strong>{PHONE_TXT}</strong><span>Landline: {LANDLINE_TXT}</span></div></a>
      <a class="tile reveal" href="tel:{OSCAR}" style="--d:.04s"><div class="tile__icon">{i("hospital")}</div><div><small>Oscar Hospital, Kasarvadavli</small><strong>{OSCAR_TXT}</strong><span>Prior appointment required</span></div></a>
      <a class="tile reveal" href="{WA}" target="_blank" rel="noopener" style="--d:.08s"><div class="tile__icon" style="background:#e6f8ee;color:#1a9e52">{i("wa")}</div><div><small>WhatsApp</small><strong>Message the clinic</strong><span>Quick replies during clinic hours</span></div></a>
      <a class="tile reveal" href="mailto:{EMAIL}" style="--d:.16s"><div class="tile__icon">{i("mail")}</div><div><small>Email</small><strong>{EMAIL}</strong></div></a>
      <a class="tile tile--wide reveal" href="{MAPS}" target="_blank" rel="noopener" style="--d:.2s"><div class="tile__icon">{i("pin")}</div><div><small>Hope Kidney Care · Mon–Sat, 7–9 PM</small><strong>GM House, Runwal Nagar, Thane (W)</strong><span>Opp. Jupiter Hospital, beside Lerida Hotel, Eastern Express Highway, 400601</span></div></a>
    </div>
  </div>
</section>

<section class="section section--white" style="padding-top:0;background:transparent">
  <div class="container">
    <div class="map reveal">
      <iframe title="Map to Hope Kidney Care, Thane" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=Hope+Kidney+Care,+GM+House,+Runwal+Nagar,+Eastern+Express+Highway,+Thane+400601&output=embed"></iframe>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">OPD timings</span><h2>Consultation locations</h2></div>
    <div class="locations">{"".join(loc_card(l, n*0.06) for n, l in enumerate(LOCATIONS))}</div>
  </div>
</section>
''' + footer()
write("contact.html", contact)

# Redirect old template URL to the new hospitals page
write("Gallery.html", '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Moved</title><meta http-equiv="refresh" content="0; url=hospitals.html"><link rel="canonical" href="hospitals.html"></head><body><a href="hospitals.html">Hospitals &amp; Timings</a></body></html>')
print("built")
