#!/usr/bin/env python3
"""Generates the Rudrakhchya static site. Run: python3 build.py
All prices live in the PRICES block below - change them here and rebuild."""
import html, urllib.parse, os

# ---------------------------------------------------------------- PRICES (NRS)
ACT = {3: 10000, 6: 10000, 7: 10000}      # activated (consecrated) - from the live site
ENG = {3: 1500, 6: 1500, 7: 1500}          # energized bead only
ENG_LOCKET = {3: 2500, 6: 2500, 7: 2500}   # energized bead in Panchadhatu Om locket
ACT_PENDANT = 3000                         # activated bead + locket add-on (CONFIRM)
GAURI = [("Standard", "NRS 18,000"), ("Above 36 mm", "NRS 35,000 – 40,000"), ("Above 40 mm", "NRS 50,000+")]
PENDANT_IMG = "assets/img/pendant.jpg"     # drop the pendant photo here and rebuild
BUNDLE_ACT = {"3 + 7": 18000, "3 + 6 + 7": 26000}   # activated bundles - from live site
PRICES_CONFIRMED = False                  # False = shows a "preview pricing" banner

WA = "9779823783486"
IG = "https://www.instagram.com/rudr_akshya/"
SITE = "https://rudrakshapasal.com"


def nrs(n):
    return "NRS {:,}".format(n)


def wa(msg):
    return "https://wa.me/%s?text=%s" % (WA, urllib.parse.quote(msg))


NAV = [("index.html", "Home"), ("collection.html", "Shop"), ("about.html", "Our Story"),
       ("history.html", "Rudraksha"), ("authenticity.html", "Authenticity"),
       ("learn.html", "Sacred Beads"), ("contact.html", "Contact")]


def head(title, desc, page, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{'' if page == 'index.html' else page}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{'' if page == 'index.html' else page}">
<meta property="og:image" content="{SITE}/assets/img/hero-mala.jpg">
<meta name="theme-color" content="#120D09">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%238A4B2E'/%3E%3Ccircle cx='32' cy='32' r='28' fill='none' stroke='%23D9A441' stroke-width='3'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Figtree:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{extra}
</head>
<body>
<div class="ember-field"></div>
<div class="grain"></div>
<nav aria-label="Main">
  <div class="nav-in">
    <a class="logo" href="index.html">RUDRA<span>KHCHYA</span></a>
    <div class="nav-links" id="navLinks">
{chr(10).join('      <a href="%s"%s>%s</a>' % (h, ' class="active" aria-current="page"' if h == page else '', t) for h, t in NAV)}
    </div>
    <div style="display:flex;gap:.8rem;align-items:center">
      <a class="nav-cta" href="{wa('Namaste, I am interested in a Rudraksha.')}">WhatsApp</a>
      <button class="burger" id="burger" aria-label="Menu" aria-expanded="false">☰</button>
    </div>
  </div>
</nav>
"""


def foot(scripts=""):
    banner = ""
    if not PRICES_CONFIRMED:
        banner = '<div class="preview-banner">Preview build — prices are not final yet.</div>'
    return f"""
<footer>
  <div class="wrap foot">
    <a class="logo" href="index.html">RUDRA<span>KHCHYA</span></a>
    <div class="mantra">"Every bead is a prayer made solid."</div>
    <div class="foot-links">
      <a href="collection.html">Shop</a><a href="gaurishankar.html">Gaurishankar</a><a href="about.html">Story</a><a href="history.html">Rudraksha</a><a href="authenticity.html">Authenticity</a><a href="learn.html">Learn</a><a href="faq.html">FAQ</a><a href="contact.html">Contact</a><a href="{IG}">Instagram</a>
    </div>
    <div>© 2026 Rudrakhchya · rudrakshapasal.com · Nepal<br>
      <span style="font-size:.68rem;opacity:.7">Bead photos: <a href="https://commons.wikimedia.org/wiki/File:Rudraksha_sixfaces_by_sankar.jpg" style="text-decoration:underline">Sankar 1995</a> via Wikimedia Commons, <a href="https://creativecommons.org/licenses/by-sa/4.0/" style="text-decoration:underline">CC BY-SA</a>.
      Descriptions of benefits reflect traditional belief and are not medical or financial advice.</span></div>
  </div>
</footer>
{banner}
<script src="site.js"></script>
{scripts}
</body>
</html>
"""


def cta_final(h2="Your bead is <em>waiting for you.</em>", lead="Nepal-sourced, energized or fully Guru-consecrated. Message us and we will guide you personally."):
    return f"""<section class="final">
  <div class="wrap">
    <span class="eyebrow reveal" style="justify-content:center">Ready to Receive?</span>
    <h2 class="reveal">{h2}</h2>
    <p class="lead reveal">{lead}</p>
    <div class="hero-ctas reveal" style="justify-content:center">
      <a class="btn btn-fire" href="collection.html">Shop the Collection ✦</a>
      <a class="btn btn-ghost" href="{wa('Namaste, I am ready to order a Rudraksha.')}">Order on WhatsApp</a>
    </div>
    <p class="reveal" style="font-size:.85rem;color:var(--ash-dim)">Follow our journey — bead stories, ritual glimpses &amp; availability · <a href="{IG}" style="color:var(--gold)">@rudr_akshya</a></p>
  </div>
</section>"""


# ---------------------------------------------------------------- BEAD DATA
BEADS = {
    3: dict(num="३", name="3 Mukhi", sub="3 Mukhi · Trimurti · Mars", title="The Trinity That Frees",
            desc="Brahma, Vishnu and Mahesh in one seed. In tradition, Agni's fire within the three faces is said to burn accumulated karma — the unseen weight that blocks progress despite sincere effort.",
            chips=["Deity · Trimurti", "Planet · Mangal", "Element · Fire"],
            fits=["Feel stuck despite sincere effort", "Carry guilt, grief or past karma", "Have Mangal dosh or a weak Mars in the chart"],
            img='<img src="https://commons.wikimedia.org/wiki/Special:FilePath/Rudraksha_beads.jpg?width=800" alt="Rudraksha beads from Nepal" loading="lazy">',
            legend_t="Ancient Legend · The Trinity's Tear",
            legend="A devotee prayed a thousand years asking which of the three gods was supreme. On the final day, all three appeared at once — and wept together, for they had never been asked to stand as one. Where their three tears fell upon the same earth, a Rudraksha tree grew, and every bead upon it bore three faces."),
    6: dict(num="६", name="6 Mukhi", sub="6 Mukhi · Kartikeya · Venus", title="The Commander's Focus",
            desc="Ruled by Kartikeya, the six-faced commander of the divine armies. Traditionally worn to build willpower, focus and confidence, with Shukra's grace associated with charm and harmony.",
            chips=["Deity · Kartikeya", "Planet · Shukra", "Element · Earth"],
            fits=["Seek focus and discipline in studies or career", "Face competition or scattered willpower", "Have Shukra afflictions or seek confidence"],
            img='<img src="https://commons.wikimedia.org/wiki/Special:FilePath/Rudraksha_sixfaces_by_sankar.jpg?width=800" alt="Six mukhi Rudraksha bead" loading="lazy">',
            legend_t="Ancient Legend · Six Mothers, One Son",
            legend="When Shiva's radiance fell into the reeds, six sparks became six infants, each cradled by one of the Krittika mothers. Parvati gathered them in one embrace — and they became a single child with six faces: Shanmukha, who would command the armies of the gods."),
    7: dict(num="७", name="7 Mukhi", sub="7 Mukhi · Mahalakshmi · Saturn", title="The Grace That Opens",
            desc="Ruled by Maa Mahalakshmi and governed by Shani. Seven faces are linked to the Saptamatrikas, the seven divine mothers, and the bead is traditionally worn for abundance and steadiness through Saturn's periods.",
            chips=["Deity · Mahalakshmi", "Planet · Shani", "Element · Earth"],
            fits=["Face financial hardship or blocked opportunities", "Are in Sade Sati or a Shani dasha", "Seek Mahalakshmi's grace and abundance"],
            img='<img src="assets/img/bead-closeup.jpg" alt="Close-up of a Rudraksha bead showing its natural mukhi furrows" width="900" height="409" loading="lazy">',
            legend_t="Ancient Legend · Mahalakshmi's Gift",
            legend="A ruined merchant wept by the Ganga. Mahalakshmi came as an old woman and placed a seven-faced bead in his palm: \"This is not wealth. This is the door through which wealth flows — but first, your heart must be worthy of it.\" On the seventh dawn his fortunes turned. He returned to thank her; only rippling water remained, and the soft scent of lotus."),
}


def pendant_fig():
    if os.path.exists(PENDANT_IMG):
        return ('<figure class="photo"><img src="%s" alt="Panchadhatu Om locket pendant that opens to hold a Rudraksha bead" loading="lazy"></figure>' % PENDANT_IMG)
    return ""


def bead_card(k, kind="act", featured=False):
    b = BEADS[k]
    chips = "".join('<span class="chip">%s</span>' % c for c in b["chips"])
    fits = "".join("<li>%s</li>" % f for f in b["fits"])
    extra = ""
    if kind == "home":
        cls, attrs = "bead-card", ""
        ctl = f"""
        <div class="price-row">
          <div class="price">{nrs(ACT[k])}<small>Activated · Energized {nrs(ENG[k])}</small></div>
          <a class="btn btn-fire" href="collection.html">Choose ✦</a>
        </div>"""
    else:
        if kind == "eng":
            base, add, tier, cls = ENG[k], ENG_LOCKET[k] - ENG[k], "Energized", "bead-card eng"
            plain, locket = "Energized bead only", "Energized bead in Panchadhatu locket"
        else:
            base, add, tier, cls = ACT[k], ACT_PENDANT, "Activated", "bead-card premium"
            plain, locket = "Consecrated · Guru's dakshina included", "Consecrated bead in Panchadhatu locket"
        attrs = (f' data-bead data-base="{base}" data-add="{add}" data-name="{b["name"]}" data-tier="{tier}"'
                 f' data-sub-plain="{plain}" data-sub-locket="{locket}"')
        ctl = f"""
        <label class="addon"><input type="checkbox" data-pendant> With Panchadhatu Om locket (+{nrs(add)})</label>
        <div class="price-row">
          <div class="price"><span data-price>{nrs(base)}</span><small data-pricesub>{plain}</small></div>
          <a class="btn btn-fire" data-order href="{wa('Namaste, I would like to order the %s Rudraksha — %s.' % (b['name'], tier))}">Order ✦</a>
        </div>"""
    if kind == "eng":
        body = f"""
        <figure class="card-photo">{b['img']}</figure>
        <span class="devnum">{b['num']}</span>
        <div class="sub">{b['sub']}</div>
        <h3>{b['title']}</h3>
        <p class="desc">{b['desc']}</p>
        <div class="chips">{chips}</div>{ctl}"""
    else:
        body = f"""
        <figure class="card-photo">{b['img']}</figure>
        <span class="devnum">{b['num']}</span>
        <div class="sub">{b['sub']}</div>
        <h3>{b['title']}</h3>
        <p class="desc">{b['desc']}</p>
        <div class="chips">{chips}</div>
        <ul class="fitlist">{fits}</ul>{ctl}
        <details class="legend">
          <summary>{b['legend_t']}</summary>
          <p>{b['legend']}</p>
        </details>"""
    return f"""
      <article class="{cls} reveal" data-tilt{attrs}>{body}
      </article>"""


def gauri_box():
    rows = "".join(
        f'<label><input type="radio" name="gs" value="{i}" data-label="{lbl}" data-text="{txt}"{" checked" if i == 0 else ""}><span>{lbl}</span></label>'
        for i, (lbl, txt) in enumerate(GAURI))
    return f"""<div class="gauri-box" data-gauri>
        <div class="seg three" role="radiogroup" aria-label="Gaurishankar size">{rows}</div>
        <div class="price-row">
          <div class="price"><span data-gprice>{GAURI[0][1]}</span><small>Final price confirmed with photos of the exact bead</small></div>
          <a class="btn btn-fire" data-gorder href="{wa('Namaste, I am interested in a Gaurishankar Rudraksha.')}">Order ✦</a>
        </div>
      </div>"""


RITES = [
    ("१", "Sourcing &amp; Certification", "Hand-selected in Nepal. Each bead is examined for authentic mukhi formation.", "Origin"),
    ("२", "Sankalpa — The Vow", "The Guru takes a formal sankalpa binding the bead to its purpose, opening the 54-day period of unbroken ritual discipline.", "Vedic"),
    ("३", "Japa — 2,00,000 Chants", "Two lakh repetitions of the bead's own beeja mantra are chanted over the bead until the count is complete.", "Vedic · Tantric"),
    ("४", "Havan — The Fire Ritual", "A sacred fire ceremony with offerings made in the bead's name, sealing the japa through Agni, the divine witness.", "Vedic"),
    ("५", "Tantric Invocation", "The ruling deity of the mukhi is invoked into the bead through Tantric sadhana and nyasa.", "Tantric"),
    ("६", "Guru's Blessing", "On the 54th day the bead is blessed and prepared for its wearer. The Guru's dakshina is included — nothing more is asked of you.", "Completion"),
]


def rites_grid():
    return '<div class="rite-grid">' + "".join(
        f'<div class="rite reveal"><span class="step">{n}</span><h3>{t}</h3><p>{d}</p><span class="tag">{g}</span></div>'
        for n, t, d, g in RITES) + "</div>"


DUAL = """<div class="dual">
      <div class="rite reveal"><h3>The Vedic Path</h3><ul>
        <li>Sankalpa and shuddhi (purification) as the shastras describe</li>
        <li>2 lakh japa of the mukhi's Vedic beeja mantra</li>
        <li>Havan — offerings through the sacred fire</li>
        <li>Prana pratishtha — establishing life-force in the bead</li></ul></div>
      <div class="rite reveal"><h3>The Tantric Path</h3><ul>
        <li>Invocation of the ruling deity into the bead</li>
        <li>Nyasa — placing mantra syllables upon the bead</li>
        <li>54 unbroken days of sadhana by our Guru</li>
        <li>Energy sealing, so the charge travels with the bead to you</li></ul></div>
    </div>"""

FAQ_ITEMS = [
    ("Ordering &amp; delivery", [
        ("How do I order?", "Choose your bead on the Shop page and press Order. It opens WhatsApp with your choice already written. We confirm availability, and you confirm payment and delivery details with us before anything is sent."),
        ("Do you ship outside Nepal?", "Yes. Delivery within Nepal is free. For India and the rest of the world, message us your country and we confirm the shipping cost before you commit to anything."),
        ("Which bead is right for me?", "Message us your questions or birth details and we will talk it through. The Sacred Beads page also explains what each mukhi is traditionally associated with."),
    ]),
    ("Energized vs activated", [
        ("What is the difference between energized and activated?", f"An energized bead is a genuine Nepal-sourced Rudraksha that has been energized and is ready to wear, from {nrs(min(ENG.values()))}. An activated bead goes through our Guru's full 54-day Vedic and Tantric consecration with 2 lakh chants and havan. It costs more because of the Guru's time, years of practice and dakshina."),
        ("What is the locket option?", f"Your bead comes set in a Panchadhatu Om locket pendant that opens to hold it, so it is ready to wear. An energized bead in the locket is {nrs(min(ENG_LOCKET.values()))}."),
        ("What is Gaurishankar Rudraksha?", "Two beads joined naturally, traditionally seen as the union of Shiva (Shankar) and Parvati (Gauri). It is rare, so it is priced by size, from NRS 18,000."),
    ]),
    ("Authenticity", [
        ("How do I know the bead is genuine?", "Activated and Gaurishankar beads come with a certificate matched to photographs of that exact bead. For any bead you can ask us for close-up photos or a video first. See the Authenticity page for how to inspect a bead yourself."),
        ("Do you provide X-ray reports?", "X-ray reports are available for rare or high-value beads, such as large Gaurishankar, and on request. Ask us on WhatsApp."),
    ]),
    ("Wearing &amp; care", [
        ("How do I wear it?", "Traditionally the first wearing is on a Monday morning at sunrise, after a gentle cleansing, with the beeja mantra chanted 7 or 108 times. See the Sacred Beads page for the full steps."),
        ("How do I care for the bead?", "Keep it away from harsh chemicals, perfume and soaking in water for long periods. Wipe it with a soft dry cloth, and a little natural oil now and then keeps the surface supple."),
    ]),
]


def faq_html(items=FAQ_ITEMS, limit=None):
    out = '<div class="faq">'
    n = 0
    for grp, qs in items:
        if limit is None:
            out += f"<h3>{grp}</h3>"
        for q, a in qs:
            if limit is not None and n >= limit:
                break
            out += f"<details><summary>{q}</summary><p>{a}</p></details>"
            n += 1
    return out + "</div>"


def faq_ld(items=FAQ_ITEMS):
    import json
    qa = [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
          for _, qs in items for q, a in qs]
    return '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}, ensure_ascii=False)


def page_hero(eyebrow, h1, lead):
    return f"""<header class="page-hero"><div class="wrap">
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</div></header>"""


pages = {}

# ================================================================ HOME
tiers = f"""
<section id="paths">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow reveal">Choose how you receive it</span>
      <h2 class="reveal">Three ways to <em>begin</em></h2>
      <p class="lead reveal mt1">Genuine Nepal-sourced Rudraksha, in the form that fits your budget and your practice.</p>
    </div>
    <div class="tiers">
      <div class="tier reveal"><h3>Energized</h3>
        <div class="from"><small>Bead from</small>{nrs(min(ENG.values()))}</div>
        <p>A genuine Rudraksha, energized and ready to wear. An easy, honest way to begin.</p>
        <ul><li>Bead {nrs(min(ENG.values()))}</li><li>In Panchadhatu Om locket {nrs(min(ENG_LOCKET.values()))}</li><li>3, 6 and 7 Mukhi</li></ul>
        <p class="mt1"><a href="collection.html#energized" style="color:var(--gold)">See energized beads →</a></p></div>
      <div class="tier featured reveal"><span class="badge">Guru-consecrated</span><h3>Activated</h3>
        <div class="from"><small>From</small>{nrs(min(ACT.values()))}</div>
        <p>The full 54-day Vedic &amp; Tantric consecration with 2 lakh chants and havan, priced for the Guru's time and practice.</p>
        <ul><li>Certificate + consecration record</li><li>Guru's dakshina included</li><li>Free shipping within Nepal</li></ul>
        <p class="mt1"><a href="collection.html#activated" style="color:var(--gold)">See activated beads →</a></p></div>
      <div class="tier reveal"><h3>Gaurishankar</h3>
        <div class="from"><small>From</small>{GAURI[0][1]}</div>
        <p>A rare natural joining of two beads, priced by size. Large beads are available on request.</p>
        <ul><li>Standard {GAURI[0][1]}</li><li>Above 36 mm {GAURI[1][1]}</li><li>Above 40 mm {GAURI[2][1]}</li></ul>
        <p class="mt1"><a href="gaurishankar.html" style="color:var(--gold)">About Gaurishankar →</a></p></div>
    </div>
  </div>
</section>"""

home = head("Rudrakhchya | Sacred Rudraksha from Nepal — 3, 6 & 7 Mukhi",
            "Nepal-sourced Rudraksha: energized beads from NRS 1,500, Guru-consecrated beads (54 days, 2 lakh chants) and rare Gaurishankar. Panchadhatu locket option. Free shipping within Nepal.",
            "index.html")
home += f"""
<header class="hero">
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">Nepal Sourced · Guru Consecrated</span>
      <h1>Sacred beads, <em>sourced</em> in Nepal &amp; consecrated by ritual.</h1>
      <p class="lead">3 Mukhi, 6 Mukhi and 7 Mukhi Rudraksha, and the rare Gaurishankar — hand-selected in Nepal. Choose a simply energized bead, or one fully consecrated by our Guru through 2 lakh mantra chants, havan and 54 days of Vedic &amp; Tantric ceremony.</p>
      <div class="hero-ctas">
        <a class="btn btn-fire" href="collection.html">View Collection ✦</a>
        <a class="btn btn-ghost" href="{wa('Namaste, I am interested in a Rudraksha.')}">Ask on WhatsApp</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><b>2L</b><span>Chants (activated)</span></div>
        <div class="stat"><b>54</b><span>Days of ritual</span></div>
        <div class="stat"><b>20mm+</b><span>Activated beads</span></div>
        <div class="stat"><b>Cert.</b><span>Activated &amp; rare beads</span></div>
      </div>
    </div>
    <div class="hero-3d">
      <div class="halo"></div>
      <figure class="hero-photo" id="heroPhoto">
        <img src="assets/img/hero-mala.jpg" alt="Rudraksha bead bracelet on dark wood in warm light" width="1200" height="1125" fetchpriority="high" loading="eager">
      </figure>
      <div class="bead-medal" title="Turn the bead with your cursor"><canvas id="beadCanvas" aria-label="Rotating 3D Rudraksha bead"></canvas></div>
      <span class="bead-caption">Authentic Nepali Rudraksha · live 3D bead</span>
    </div>
  </div>
</header>

<div class="ribbon" aria-hidden="true"><div class="ribbon-track">
  {"".join("<span>ॐ क्लीं नमः</span><span>✦</span><span>ॐ हुं नमः</span><span>✦</span><span>ॐ महालक्ष्म्यै नमः</span><span>✦</span><span>ॐ नमः शिवाय</span><span>✦</span>" for _ in range(3))}
</div></div>

<section id="standard">
  <div class="wrap">
    <span class="eyebrow reveal">Why Rudrakhchya</span>
    <h2 class="reveal">Sourced. Documented. <em>Consecrated.</em></h2>
    <div class="pillars">
      <div class="pillar reveal"><span class="glyph">🏔️</span><h3>Nepal Sourcing</h3><p>Beads come directly from Nepal, hand-examined for genuine mukhi formation before anything else happens.</p></div>
      <div class="pillar reveal"><span class="glyph">📜</span><h3>Proof for Rare Beads</h3><p>Activated and Gaurishankar beads come with a certificate matched to photographs of that exact bead. Ask for photos of any bead first.</p></div>
      <div class="pillar reveal"><span class="glyph">🔱</span><h3>Vedic &amp; Tantric Ritual</h3><p>Activated beads receive prana pratishtha, havan, 2 lakh japa and Tantric invocation from our Guru over 54 days.</p></div>
      <div class="pillar reveal"><span class="glyph">🌺</span><h3>Your Choice</h3><p>Energized from NRS 1,500, fully activated, or set in a Panchadhatu locket. You pay for the depth you want.</p></div>
    </div>
  </div>
</section>
{tiers}

<section id="beads" class="alt">
  <div class="wrap">
    <span class="eyebrow reveal">Sacred Collection</span>
    <h2 class="reveal">The Three <em>Sacred Beads</em></h2>
    <p class="lead reveal mt1">Three mukhis, three deities, three traditional purposes — clear the path, command the path, open the path.</p>
    <div class="beads">{bead_card(3, "home")}{bead_card(6, "home")}{bead_card(7, "home")}
    </div>
  </div>
</section>

<section id="consecration">
  <div class="wrap">
    <span class="eyebrow reveal">54 Days of Devotion</span>
    <h2 class="reveal">Not a product. <em>A sacred transfer.</em></h2>
    <p class="lead reveal mt1">Every activated bead passes through the same six stages. The mantra and the deity differ for each mukhi — the depth never does.</p>
    {rites_grid()}
    {DUAL}
    <p class="center mt2 reveal"><a class="btn btn-ghost" href="about.html">Read the Guru's story →</a></p>
  </div>
</section>

<section id="proof" class="alt">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal">
        <span class="eyebrow">Authenticity</span>
        <h2 class="mt1">A real bead should <em>prove itself.</em></h2>
        <p class="lead mt1">Rudraksha is widely imitated. That is why activated and Gaurishankar beads carry a certificate, why we share close-up photographs of any bead on request, and why rare beads can come with an X-ray report.</p>
        <p class="mt2"><a class="btn btn-fire" href="authenticity.html">How we verify a bead ✦</a></p>
      </div>
      <div class="photo reveal"><img src="assets/img/bead-closeup.jpg" alt="Natural mukhi furrows on a Rudraksha bead" width="900" height="409" loading="lazy"></div>
    </div>
  </div>
</section>

<section id="history">
  <div class="wrap center">
    <span class="eyebrow reveal">The Tear of Rudra</span>
    <h2 class="reveal">Older than <em>the story we tell.</em></h2>
    <p class="lead reveal mt1">From the Puranic tale of Shiva's tears to the 108-bead mala in a sadhak's hand — learn where Rudraksha comes from and why it has been worn for so long.</p>
    <p class="mt2 reveal"><a class="btn btn-ghost" href="history.html">Explore the history →</a></p>
  </div>
</section>

<section id="bundle" class="alt">
  <div class="wrap">
    <div class="bundle reveal">
      <span class="eyebrow" style="justify-content:center">Sacred Bundles</span>
      <h2 style="margin-top:.8rem">The Complete <em>Path</em></h2>
      <p class="lead" style="margin:1rem auto 0">The 3 Mukhi is traditionally worn to clear what blocks you, the 6 Mukhi to give you the will to walk, and the 7 Mukhi to open what you are cleared for. Each bundle is separately consecrated — one ceremony per bead.</p>
      <div class="bundle-seq"><div class="node">३</div><span class="join">+</span><div class="node">६</div><span class="join">+</span><div class="node">७</div></div>
      <div class="flow">Purify → Command → Receive</div>
      <p style="font-size:.95rem;color:var(--ash-dim);margin-bottom:1.8rem">Activated bundles: 3 + 7 Mukhi — <b style="color:var(--gold)">{nrs(BUNDLE_ACT['3 + 7'])}</b> &nbsp;·&nbsp; 3 + 6 + 7 Complete Path — <b style="color:var(--gold)">{nrs(BUNDLE_ACT['3 + 6 + 7'])}</b></p>
      <a class="btn btn-fire" href="{wa('Namaste, I am interested in a Rudraksha bundle.')}">Enquire About Bundles</a>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap center">
    <span class="eyebrow reveal">Questions</span>
    <h2 class="reveal">Before you <em>decide</em></h2>
    {faq_html(limit=4)}
    <p class="mt2"><a class="btn btn-ghost" href="faq.html">All questions →</a></p>
  </div>
</section>
{cta_final()}
"""
home += foot('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script src="bead3d.js"></script>')
pages["index.html"] = home

# ================================================================ SHOP
shop = head("Shop | Rudrakhchya — Energized, Activated & Gaurishankar Rudraksha",
            "Energized Rudraksha from NRS 1,500, Guru-consecrated 3, 6 and 7 Mukhi, and rare Gaurishankar by size. Panchadhatu Om locket option. Order on WhatsApp. Free shipping in Nepal.",
            "collection.html")
shop += page_hero("The Collection", "Choose your <em>path</em>",
                  "Energized beads for everyday wear, Guru-activated beads for those who want the full consecration, and the rare Gaurishankar. Tap a path to jump to it.")
shop += f"""
<div class="wrap"><nav class="jump" aria-label="Sections">
  <a href="#energized">Energized · from {nrs(min(ENG.values()))}</a>
  <a href="#activated">Activated · from {nrs(min(ACT.values()))}</a>
  <a href="#gaurishankar">Gaurishankar · from {GAURI[0][1]}</a>
  <a href="#locket">Locket pendant</a>
</nav></div>

<section id="energized" class="sec-eng">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Everyday beads</span>
    <h2 class="reveal">Energized <em>Rudraksha</em></h2>
    <p class="lead reveal mt1">Genuine Nepal-sourced beads, energized and ready to wear, priced to be easy to begin with: <b>{nrs(min(ENG.values()))}</b> for the bead, <b>{nrs(min(ENG_LOCKET.values()))}</b> in a Panchadhatu Om locket.</p></div>
    <div class="beads">{bead_card(3, "eng")}{bead_card(6, "eng")}{bead_card(7, "eng")}
    </div>
  </div>
</section>

<section id="locket" class="alt">
  <div class="wrap">
    <div class="{'cols-2' if pendant_fig() else ''}">
      {pendant_fig()}
      <div class="prose reveal" style="margin:0 auto">
        <span class="eyebrow">The locket</span>
        <h2 class="mt1">Panchadhatu Om <em>locket pendant</em></h2>
        <p>A Panchadhatu Om locket that opens to hold your Rudraksha, so the bead sits close to you and stays protected. It makes the bead ready to wear and ready to gift.</p>
        <p><b>Energized bead in the locket: {nrs(min(ENG_LOCKET.values()))}</b> (bead alone {nrs(min(ENG.values()))}). Activated beads can be set in the locket too: +{nrs(ACT_PENDANT)}.</p>
      </div>
    </div>
  </div>
</section>

<section id="activated" class="sec-act">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Guru-consecrated</span>
    <h2 class="reveal">Activated <em>Rudraksha</em></h2>
    <p class="lead reveal mt1">The complete 54-day Vedic &amp; Tantric consecration: 2 lakh chants, havan and the Guru's blessing. It is priced higher because each bead takes the Guru's time and years of practice, and his dakshina is included.</p></div>
    <div class="beads">{bead_card(3)}{bead_card(6, featured=True)}{bead_card(7)}
    </div>
    <div class="bundle reveal mt3">
      <span class="eyebrow" style="justify-content:center">Activated Bundles</span>
      <h2 style="margin-top:.8rem">The Complete <em>Path</em></h2>
      <div class="bundle-seq"><div class="node">३</div><span class="join">+</span><div class="node">६</div><span class="join">+</span><div class="node">७</div></div>
      <p style="font-size:.95rem;color:var(--ash-dim);margin-bottom:1.8rem">3 + 7 Mukhi — <b style="color:var(--gold)">{nrs(BUNDLE_ACT['3 + 7'])}</b> &nbsp;·&nbsp; 3 + 6 + 7 — <b style="color:var(--gold)">{nrs(BUNDLE_ACT['3 + 6 + 7'])}</b></p>
      <a class="btn btn-fire" href="{wa('Namaste, I am interested in a Rudraksha bundle.')}">Enquire About Bundles</a>
    </div>
  </div>
</section>

<section id="gaurishankar" class="alt">
  <div class="wrap">
    <div class="cols-2">
      <div class="prose reveal" style="margin:0">
        <span class="eyebrow">Rare · Collector</span>
        <h2 class="mt1">Gaurishankar <em>Rudraksha</em></h2>
        <p>Two beads joined naturally into one, traditionally seen as the union of Shiva (Shankar) and Parvati (Gauri). It is rare, and its price rises quickly with size.</p>
        <p><a href="gaurishankar.html" style="color:var(--gold);text-decoration:underline">Read about Gaurishankar and how to check one →</a></p>
      </div>
      <div class="panel reveal">{gauri_box()}</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Energized or activated?</span>
    <h2 class="reveal">What you are <em>choosing between</em></h2></div>
    <div class="tbl-wrap"><table class="compare">
      <thead><tr><th></th><th>Energized</th><th>Activated</th></tr></thead>
      <tbody>
        <tr><td>Genuine Nepal-sourced bead</td><td>Yes</td><td>Yes</td></tr>
        <tr><td>Energized and ready to wear</td><td>Yes</td><td>Yes, as part of the full ritual</td></tr>
        <tr><td>54-day Vedic &amp; Tantric consecration</td><td>No</td><td>Yes</td></tr>
        <tr><td>2 lakh mantra chants + havan</td><td>No</td><td>Yes</td></tr>
        <tr><td>Certificate matched to photographs</td><td>Photos on request</td><td>Yes</td></tr>
        <tr><td>Guru's dakshina included</td><td>—</td><td>Yes</td></tr>
        <tr><td>Bead / in Panchadhatu locket</td><td>{nrs(min(ENG.values()))} / {nrs(min(ENG_LOCKET.values()))}</td><td>from {nrs(min(ACT.values()))} / +{nrs(ACT_PENDANT)}</td></tr>
      </tbody></table></div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">How to order</span><h2 class="reveal">Four <em>simple</em> steps</h2></div>
    <div class="steps">
      <div class="rite reveal"><span class="step">१</span><h3>Choose</h3><p>Pick energized, activated or Gaurishankar, and the locket if you want it.</p></div>
      <div class="rite reveal"><span class="step">२</span><h3>Message us</h3><p>Press Order. WhatsApp opens with your choice already written.</p></div>
      <div class="rite reveal"><span class="step">३</span><h3>Confirm</h3><p>We confirm availability. You confirm payment and delivery details with us.</p></div>
      <div class="rite reveal"><span class="step">४</span><h3>Receive</h3><p>Free delivery within Nepal. Shipping to India and abroad is confirmed before you pay.</p></div>
    </div>
  </div>
</section>
{cta_final("Not sure which <em>bead</em> is yours?", "Share your questions or birth details on WhatsApp and we will help you choose.")}
"""
shop += foot()
pages["collection.html"] = shop

# ================================================================ HISTORY
hist = head("Rudraksha History & Meaning — The Tears of Rudra | Rudrakhchya",
            "Where Rudraksha comes from: the Puranic story of Shiva's tears, the Elaeocarpus ganitrus tree, what mukhi means, and why a mala has 108 beads.",
            "history.html")
hist += page_hero("The Tear of Rudra", "A seed with a <em>story</em>",
                  "What Rudraksha is, where it grows, and the traditions that have carried it for centuries. Stories here are given as tradition, not as proven fact.")
hist += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="prose">
      <h2 class="reveal">The name</h2>
      <p class="reveal">The word <b>Rudraksha</b> comes from Sanskrit: <b>Rudra</b>, a name of Shiva, and <b>aksha</b>, meaning eye, and by extension tear. It is usually translated as "the eye of Rudra" or "the tears of Rudra".</p>
      <div class="quote-block reveal">According to Puranic tradition, Shiva meditated for a very long time for the welfare of living beings. When he opened his eyes, tears of compassion fell to the earth, and from them grew the Rudraksha trees.</div>
      <p class="reveal">That is the traditional account. Whatever one believes about the story, it explains why the bead is treated as sacred, and why it is most often associated with Shiva and with meditation.</p>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="cols-2">
      <div class="prose reveal" style="margin:0">
        <h2>The tree and the seed</h2>
        <p>The bead is the hard seed of a tree of the genus <b>Elaeocarpus</b> (the Himalayan species is <i>Elaeocarpus ganitrus</i>). The tree bears a blue fruit, and once the soft flesh is removed, the ridged seed inside is the Rudraksha.</p>
        <p>The trees grow in the Himalayan foothills and across parts of South and Southeast Asia. Nepal is one of the places traditionally known for Rudraksha, which is why we source there.</p>
        <p>The ridges running from one end of the bead to the other are called <b>mukhi</b>, meaning "faces". Texts commonly describe beads from one to fourteen faces, and the trade lists higher counts too. Each mukhi is associated in tradition with a particular deity and planet.</p>
      </div>
      <div class="photo reveal"><img src="assets/img/bead-closeup.jpg" alt="Natural mukhi furrows on a Rudraksha bead" width="900" height="409" loading="lazy"></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">In practice</span><h2 class="reveal">How it has been <em>used</em></h2></div>
    <div class="cols-3 mt3">
      <div class="panel reveal"><h3>As a mala</h3><p>A traditional mala has 108 beads plus one extra, the guru or bindu bead, which marks the start and end of the count when chanting japa.</p></div>
      <div class="panel reveal"><h3>As a single bead</h3><p>A single bead, often a particular mukhi, is worn on a thread or chain, close to the body, in connection with its ruling deity and mantra.</p></div>
      <div class="panel reveal"><h3>In sadhana</h3><p>Shaiva ascetics and householders alike have used Rudraksha for japa and meditation. It is also used in some other devotional traditions.</p></div>
    </div>
    <p class="disclaimer">Traditional texts describe many benefits of Rudraksha. These are statements of belief and practice, not scientific or medical claims, and a bead is not a substitute for professional medical, legal or financial advice.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap center">
    <span class="eyebrow reveal">Continue</span>
    <h2 class="reveal">From story to <em>bead</em></h2>
    <p class="lead reveal mt1">Read what each of our three mukhis is traditionally associated with, or see how we verify a bead.</p>
    <div class="hero-ctas reveal mt2" style="justify-content:center">
      <a class="btn btn-fire" href="learn.html">The Sacred Beads ✦</a>
      <a class="btn btn-ghost" href="authenticity.html">Authenticity</a>
    </div>
  </div>
</section>
{cta_final()}
"""
hist += foot()
pages["history.html"] = hist

# ================================================================ GAURISHANKAR
gs = head("Gaurishankar Rudraksha — Meaning, Sizes & Price | Rudrakhchya",
          "Gaurishankar Rudraksha: two beads joined naturally, traditionally the union of Shiva and Parvati. Sizes and prices from NRS 18,000 and how to check one is genuine.",
          "gaurishankar.html")
gs += page_hero("Rare · Collector", "Gaurishankar <em>Rudraksha</em>",
                "Two beads joined naturally into one. In tradition, Shiva and Parvati together.")
gs += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="cols-2">
      <div class="prose reveal" style="margin:0">
        <h2>What it is</h2>
        <p>A <b>Gaurishankar</b> Rudraksha is two beads that have grown naturally joined at the base. <b>Gauri</b> is Parvati and <b>Shankar</b> is Shiva, and the bead is traditionally regarded as their union.</p>
        <p>Because the joining is a natural accident of growth, a good Gaurishankar is uncommon, and the larger it is, the rarer it becomes.</p>
        <h3>Traditional associations</h3>
        <p>In tradition it is associated with harmony between partners and within the family, with steady devotion, and with the balance of Shiva and Shakti. These are statements of belief, not promises of results.</p>
        <p><b>Mantra:</b> ॐ गौरीशङ्कराय नमः (Om Gaurishankaraya Namah)</p>
      </div>
      <div class="panel reveal">
        <h3>Sizes &amp; price</h3>
        <table class="compare"><tbody>
          {"".join(f"<tr><td>{l}</td><td>{t}</td></tr>" for l, t in GAURI)}
        </tbody></table>
        <p class="note">Larger beads vary a great deal, so the final price is confirmed on WhatsApp with photographs of the exact bead.</p>
        <div class="mt2">{gauri_box()}</div>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Be careful</span><h2 class="reveal">How to check a <em>Gaurishankar</em></h2></div>
    <div class="cols-3 mt3">
      <div class="panel reveal"><h3>Look at the joint</h3><ul><li>A natural joint is uneven and fibrous</li><li>Two separate beads glued together show a seam or filler</li><li>Ask for close-up photographs of the joint</li></ul></div>
      <div class="panel reveal"><h3>Ask for an X-ray</h3><ul><li>It shows whether the beads are truly joined inside</li><li>Recommended for large and high-value beads</li><li>Available from us on request</li></ul></div>
      <div class="panel reveal"><h3>Match the paper</h3><ul><li>The certificate lists size and weight</li><li>Photographs are of the exact bead</li><li>Measure it when it arrives</li></ul></div>
    </div>
    <p class="center mt2 reveal"><a class="btn btn-ghost" href="authenticity.html">More on authenticity →</a></p>
    <p class="disclaimer">Benefits are traditional beliefs, not medical, legal or financial claims.</p>
  </div>
</section>
{cta_final("Interested in a <em>Gaurishankar?</em>", "Tell us the size you want and we will send photographs of the exact beads available.")}
"""
gs += foot()
pages["gaurishankar.html"] = gs

# ================================================================ STORY
story = head("Our Story — Rudrakhchya | The Guru and the 54 Days",
             "The story of Rudrakhchya: Nepal-sourced Rudraksha, the Guru who completed 36 lakh chants, and the 54-day consecration behind every activated bead.",
             "about.html")
story += page_hero("Our Story", "Not a store.<br><em>A transfer of practice.</em>",
                   "Rudrakhchya is built around two things: honest sourcing in Nepal, and a Guru whose practice stands behind every activated bead.")
story += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal center" style="text-align:center">
        <div style="font-family:var(--disp);font-size:clamp(5rem,14vw,9rem);color:var(--gold);line-height:1;text-shadow:0 0 50px rgba(217,164,65,.3)">36</div>
        <div class="eyebrow" style="justify-content:center">Lakh chants — Guru qualification</div>
      </div>
      <div class="prose reveal" style="margin:0">
        <h2>The Guru</h2>
        <p>Before our Guru consecrated a single bead for another person, he spent years in intensive Tantric and Vedic practice, completing <b>36 lakh chants</b> of the sacred mantras associated with the Rudraksha. In this tradition that is the requirement for mantra siddhi, the state in which the mantra is considered to be alive and effective.</p>
        <div class="quote-block">"For 54 days the Guru dissolves himself into the mantra. The bead absorbs that surrender — and carries it, living, to whoever receives it."</div>
        <p>The Guru's dakshina is included in the price of every activated bead. Nothing more is asked of you.</p>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">The journey of a bead</span><h2 class="reveal">From Nepal to <em>your hands</em></h2></div>
    <div class="steps">
      <div class="rite reveal"><span class="step">१</span><h3>Sourcing</h3><p>Beads are selected in Nepal and examined for genuine mukhi formation. Activated beads are 20mm+.</p></div>
      <div class="rite reveal"><span class="step">२</span><h3>Certificate</h3><p>Activated and Gaurishankar beads are documented on their own certificate with photographs, so you can match the bead to the paper.</p></div>
      <div class="rite reveal"><span class="step">३</span><h3>Consecration</h3><p>Activated beads go through 54 days of ritual: 2 lakh chants, havan and Tantric invocation.</p></div>
      <div class="rite reveal"><span class="step">४</span><h3>Delivery</h3><p>Your bead is dispatched with care. Free within Nepal, and shipped worldwide at a cost we confirm in advance.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">What the 54 days contain</span><h2 class="reveal">The <em>consecration</em></h2></div>
    {rites_grid()}
    {DUAL}
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">What we believe</span><h2 class="reveal">Our <em>principles</em></h2></div>
    <div class="cols-3 mt3">
      <div class="panel reveal"><h3>Honest about what it is</h3><p>We describe benefits as tradition teaches them. We do not promise results, and we do not offer a bead as a replacement for medical or financial advice.</p></div>
      <div class="panel reveal"><h3>You choose the depth</h3><p>Energized and activated beads are both genuine. The full consecration is offered, never forced.</p></div>
      <div class="panel reveal"><h3>Proof you can hold</h3><p>A certificate for activated and Gaurishankar beads, photographs of any bead on request, and an X-ray report for rare beads.</p></div>
    </div>
  </div>
</section>
{cta_final("Ask the Guru's <em>team</em> anything.", "Questions about the consecration, the mantras or which bead suits you — we answer personally on WhatsApp.")}
"""
story += foot()
pages["about.html"] = story

# ================================================================ AUTHENTICITY
auth = head("Rudraksha Authenticity & Certificates | Rudrakhchya",
            "How we verify Rudraksha: certificates for activated and Gaurishankar beads, photographs, optional X-ray, and how to inspect a bead yourself.",
            "authenticity.html")
auth += page_hero("Authenticity", "A real bead should <em>prove itself</em>",
                  "Rudraksha is widely imitated and widely over-claimed. Here is exactly what you receive with a Rudrakhchya bead, and how to check any bead you are offered.")
auth += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="cols-2">
      <div class="prose reveal" style="margin:0">
        <h2>The certificate</h2>
        <p>Activated beads and Gaurishankar beads are sold with a certificate that describes <b>that specific bead</b>, not the product in general. For an energized bead you can ask us for close-up photographs or a video of the exact bead before you order. It records the things you can check with your own eyes and a ruler:</p>
        <p>The bead's reference number, its mukhi count, its size and weight, and photographs of the bead matched to the paper. For activated beads, the consecration is recorded too.</p>
        <p>The sample on the right shows the layout. It is an example of the fields, not a real record.</p>
      </div>
      <div class="cert reveal">
        <span class="tag-sample">Sample layout</span>
        <h3>CERTIFICATE OF AUTHENTICITY</h3>
        <dl>
          <dt>Bead reference</dt><dd>RK-0000</dd>
          <dt>Type</dt><dd>7 Mukhi Rudraksha</dd>
          <dt>Origin</dt><dd>Nepal</dd>
          <dt>Size</dt><dd>__ mm</dd>
          <dt>Weight</dt><dd>__ g</dd>
          <dt>Mukhi count</dt><dd>7 natural furrows</dd>
          <dt>Photographs</dt><dd>Attached</dd>
          <dt>Consecration</dt><dd>Activated</dd>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Inspect it yourself</span><h2 class="reveal">Signs of a <em>genuine bead</em></h2></div>
    <div class="cols-3 mt3">
      <div class="panel reveal"><h3>Natural, uneven furrows</h3><ul><li>Mukhi lines run from one end to the other</li><li>They are never perfectly even</li><li>The count matches what is claimed</li></ul></div>
      <div class="panel reveal"><h3>A seed, not a mould</h3><ul><li>Bumpy, slightly irregular surface</li><li>Hole shows natural fibre, not a smooth plastic bore</li><li>No glue lines or seams along a furrow</li></ul></div>
      <div class="panel reveal"><h3>Honest claims</h3><ul><li>The seller names the mukhi and the size</li><li>Photographs are of the bead you receive</li><li>No guaranteed results</li></ul></div>
    </div>
    <p class="disclaimer"><b>A note on the water test.</b> The common "sinks or floats" test is not reliable. Density varies between genuine beads, and fakes can be made to sink. Do not buy or reject a bead on that alone.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Going further</span><h2 class="reveal">X-ray <em>and lab reports</em></h2></div>
    <div class="prose mt2">
      <p class="reveal">An X-ray shows the internal chambers of a bead, which confirms the mukhi count inside and shows whether it has been carved, filled or glued. For a common bead that is usually not needed; for a rare or high-value bead it can matter a great deal.</p>
      <p class="reveal">We provide X-ray observation reports for rare or high-value beads, and on request for others. Message us if you want one for the bead you are considering.</p>
    </div>
    <p class="center mt2 reveal"><a class="btn btn-fire" href="{wa('Namaste, I would like an X-ray report for a Rudraksha.')}">Ask about an X-ray report ✦</a></p>
  </div>
</section>
{cta_final("See it before you <em>decide.</em>", "Ask for close-up photographs or a video of the exact bead before you order.")}
"""
auth += foot()
pages["authenticity.html"] = auth

# ================================================================ LEARN (Sacred Beads)
def aspect(icon, title, text):
    return f'<div class="panel reveal"><h3>{icon} {title}</h3><p>{text}</p></div>'


learn = head("The Sacred Beads — 3, 6 & 7 Mukhi Rudraksha Guide | Rudrakhchya",
             "What the 3 Mukhi, 6 Mukhi and 7 Mukhi Rudraksha are traditionally associated with, their mantras, and how to wear them. English and Nepali.",
             "learn.html")
learn += page_hero("Vedic &amp; Tantric Knowledge", "The <em>Sacred Beads</em> of Rudrakhchya",
                   "Mythology, deity, planet and mantra for each bead, and how to wear it. Everything here is tradition, not a promise of results.")
learn += f"""
<div class="center"><div data-lang-toggle class="hero-ctas" style="justify-content:center;margin:0 0 1rem">
  <button class="btn btn-ghost" data-l="en" aria-pressed="true">English</button>
  <button class="btn btn-ghost" data-l="ne" aria-pressed="false">नेपाली</button>
</div></div>

<div data-lang="en">
<section id="three" style="padding-top:2rem">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">3 Mukhi · Trimurti · Mangal</span><h2 class="reveal">The Trinity That <em>Frees</em></h2></div>
    <div class="cols-3 mt3">
      {aspect("🔱", "The Holy Trinity", "The 3 Mukhi represents Brahma, Vishnu and Mahesh together — creation, preservation and dissolution in one seed.")}
      {aspect("🔥", "Agni, the Unifying Fire", "In tradition Agni is present in all three divine acts. The bead is said to carry the fire that burns accumulated karma.")}
      {aspect("⚡", "Mars and Energy", "Governed by Mars (Mangal), the planet of drive and courage. Traditionally worn by those who feel low in energy or willpower.")}
      {aspect("🌀", "Release of Past Burden", "Associated in tradition with letting go of guilt, heaviness and repeated stagnation.")}
      {aspect("🪐", "Mangal Dosh", "Jyotish tradition recommends the 3 Mukhi for those with a weak or afflicted Mars in the birth chart.")}
      {aspect("🌅", "New Beginnings", "Brahma creates, Vishnu sustains, Shiva dissolves — the bead is associated with inner renewal at any stage of life.")}
    </div>
    <div class="prose mt3">
      <h3 class="reveal">The mythology</h3>
      <p class="reveal">A great devotee prayed to Brahma, Vishnu and Shiva asking which of the three was supreme. For a thousand years he received no answer. On the last day, all three appeared at once and wept together, for they had never been asked to stand as one. Where their three tears fell on the same earth, a Rudraksha tree grew, and every bead on it bore three faces.</p>
      <p class="reveal">In Tantric tradition the 3 Mukhi is also connected to <b>Tripura Sundari</b>, the goddess of three cities, who reveals that apparent opposites are one at the deepest level.</p>
      <p class="reveal"><b>Beeja mantra:</b> ॐ क्लीं नमः (Om Kleem Namah)</p>
    </div>
  </div>
</section>

<section id="six" class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">6 Mukhi · Kartikeya · Shukra</span><h2 class="reveal">The Commander's <em>Focus</em></h2></div>
    <div class="cols-3 mt3">
      {aspect("⚔️", "Kartikeya", "The six-faced commander of the divine armies, born of Shiva's fire and raised by the six Krittika mothers.")}
      {aspect("🎯", "Focus and Discipline", "Traditionally worn by students and professionals who want steadier focus and willpower.")}
      {aspect("🌸", "Venus (Shukra)", "Linked in tradition with charm, harmony and refinement, and recommended for Shukra afflictions.")}
    </div>
    <div class="prose mt3"><p class="reveal"><b>Beeja mantra:</b> ॐ ह्रीं हुं नमः (Om Hreem Hum Namah)</p></div>
  </div>
</section>

<section id="seven">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">7 Mukhi · Mahalakshmi · Shani</span><h2 class="reveal">The Grace That <em>Opens</em></h2></div>
    <div class="cols-3 mt3">
      {aspect("🌺", "Mahalakshmi's Grace", "Governed by Mahalakshmi, the embodiment of wealth, beauty and abundance in tradition.")}
      {aspect("💰", "Livelihood", "Traditionally worn by people facing financial difficulty or blocked income, as a support for steadiness rather than a guarantee.")}
      {aspect("🪐", "Saturn's Remedy", "Recommended in Vedic and Tantric tradition during Sade Sati, Shani dasha and adverse Saturn transits.")}
      {aspect("🔱", "Protection", "Consecrated beads are traditionally regarded as a protective presence for the wearer.")}
      {aspect("💼", "Business and Career", "Worn in the hope of clarity and momentum in work, according to tradition.")}
      {aspect("🧘", "Meditation", "Associated with concentration and with steadier sadhana when worn consistently.")}
    </div>
    <div class="prose mt3">
      <h3 class="reveal">The mythology</h3>
      <p class="reveal">Seven carries great weight in tradition: seven chakras, seven sacred rivers, seven tones. The 7 Mukhi is linked to the Saptamatrikas, the seven divine mothers, and, in the Shiva Purana, to Ananta Sarp, the cosmic serpent of boundlessness.</p>
      <div class="quote-block reveal">A ruined merchant wept on the banks of the Ganga. Mahalakshmi appeared as an old woman and placed a seven-faced bead in his palm. "This is not wealth. This is the door through which wealth flows — but first, your heart must be worthy of it."</div>
      <p class="reveal"><b>Beeja mantra:</b> ॐ हुं नमः (Om Hum Namah)</p>
      <p class="reveal">Want the full detail? Read the <a href="7-mukhi-rudraksha.html" style="color:var(--gold);text-decoration:underline">complete 7 Mukhi guide</a>.</p>
    </div>
  </div>
</section>

<section id="wear" class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">How to wear</span><h2 class="reveal">Activation &amp; <em>wearing</em></h2>
    <p class="lead reveal mt1">Activated beads arrive consecrated. These steps are for your own alignment with the bead.</p></div>
    <div class="steps">
      <div class="rite reveal"><span class="step">१</span><h3>Monday sunrise</h3><p>Monday is governed by Shiva, so it is the traditional day for first wearing.</p></div>
      <div class="rite reveal"><span class="step">२</span><h3>Cleanse</h3><p>Dip the bead in raw milk or clean water for a few minutes and wipe it gently with a clean cloth.</p></div>
      <div class="rite reveal"><span class="step">३</span><h3>Chant</h3><p>Hold the bead to your heart and chant its beeja mantra 7 or 108 times.</p></div>
      <div class="rite reveal"><span class="step">४</span><h3>Wear</h3><p>On a red or gold thread, or a silver or gold chain, touching the skin, close to the heart. Keep others from touching it.</p></div>
    </div>
  </div>
</section>
</div>

<div data-lang="ne" hidden>
<section style="padding-top:2rem">
  <div class="wrap">
    <div class="center"><span class="eyebrow">३ मुखी रुद्राक्ष</span><h2>त्रिमूर्तिको आशीर्वाद — <em>कर्म मुक्तिको बाटो</em></h2></div>
    <div class="prose mt2">
      <p><b>३ मुखी रुद्राक्ष</b> त्रिमूर्ति — ब्रह्मा, विष्णु र महेश — तीनै देवताहरूको प्रतीक हो। सृष्टि, पालन र संहारको एकता यो एउटै बीउमा समाहित छ भन्ने परम्परागत विश्वास छ। अग्नि यस त्रिमूर्तिको जोड्ने शक्ति हो, र मंगल ग्रहद्वारा शासित मानिन्छ।</p>
      <p>परम्परा अनुसार यो विगतका कर्मको भार, अपराधबोध र ऊर्जाको कमीसँग जोडिएको छ। मंगल दोष वा कमजोर मंगल भएकाहरूका लागि जोतिष परम्पराले यसको सिफारिस गर्छ। मन्त्र: <b>ॐ क्लीं नमः</b></p>
    </div>
    <div class="center mt3"><span class="eyebrow">७ मुखी रुद्राक्ष</span><h2>महालक्ष्मीको कृपा — <em>समृद्धिको ढोका</em></h2></div>
    <div class="prose mt2">
      <p><b>७ मुखी रुद्राक्ष</b> महालक्ष्मीसँग सम्बन्धित छ र शनि ग्रहसँग जोडिएको छ। साढेसाती, शनि दशा र आर्थिक अवरोधको समयमा परम्परागत रूपमा यसको प्रयोग गरिन्छ। यसले परिणामको ग्यारेन्टी दिँदैन, श्रद्धा र साधनाको सहयोगीको रूपमा लिइन्छ। मन्त्र: <b>ॐ हुं नमः</b></p>
    </div>
    <div class="center mt3"><span class="eyebrow">लगाउने विधि</span><h2>पहिरने <em>तरिका</em></h2></div>
    <div class="prose mt2">
      <p>सोमबार बिहान सूर्योदयमा रुद्राक्षलाई शुद्ध पानी वा कच्चा दूधमा केही बेर राखेर सफा कपडाले पुछ्नुहोस्। हृदयमा राखी मन्त्र ७ वा १०८ पटक जप्नुहोस्।</p>
      <p>रातो वा सुनौलो धागो वा चाँदी/सुनको चेनमा लगाउनुहोस्, छालासँग सिधै सम्पर्कमा रहने गरी। रुद्राक्षचयाका सक्रिय (activated) दाना ५४ दिन र २ लाख मन्त्र जपसहित, हवन र तन्त्र-वैदिक विधिद्वारा अभिमन्त्रित गरिएको हुन्छ।</p>
    </div>
  </div>
</section>
</div>

<section>
  <div class="wrap"><p class="disclaimer">All benefits described are traditional beliefs and are offered for devotional and cultural interest. They are not medical, legal or financial claims.</p></div>
</section>
{cta_final("Ready to begin <em>your path?</em>", "Choose the bead that fits your need, or ask us which one is right for you.")}
"""
learn += foot()
pages["learn.html"] = learn

# ================================================================ 7 MUKHI GUIDE
seven = head("7 Mukhi Rudraksha — Complete Guide | Rudrakhchya",
             "Complete guide to the 7 Mukhi Rudraksha: Mahalakshmi, Saturn (Shani), mythology, mantra and how to wear it. Nepal-sourced.",
             "7-mukhi-rudraksha.html",
             '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"7 Mukhi Rudraksha Complete Guide","author":{"@type":"Organization","name":"Rudrakhchya"},"url":"https://rudrakshapasal.com/7-mukhi-rudraksha.html"}</script>')
seven += page_hero("Complete Guide", "The <em>7 Mukhi</em> Rudraksha",
                   "Mahalakshmi · Shani (Saturn) · Manipura chakra · traditionally associated with abundance and steadiness.")
seven += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="cols-4">
      <div class="panel reveal"><h3>Deity</h3><p>Mahalakshmi</p></div>
      <div class="panel reveal"><h3>Planet</h3><p>Shani (Saturn)</p></div>
      <div class="panel reveal"><h3>Chakra</h3><p>Manipura</p></div>
      <div class="panel reveal"><h3>Mantra</h3><p>ॐ हुं नमः</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Traditional associations</span><h2 class="reveal">Why it is <em>sought</em></h2></div>
    <div class="cols-3 mt3">
      {aspect("🌺", "Mahalakshmi's Grace", "Governed by Mahalakshmi, associated in tradition with wealth, beauty and abundance.")}
      {aspect("💰", "Livelihood", "Worn by people facing financial difficulty or blocked income, as a support for steadiness, not as a guarantee.")}
      {aspect("🪐", "Saturn", "Recommended in tradition for Sade Sati, Shani dasha and adverse Saturn transits.")}
      {aspect("🔱", "Protection", "Consecrated beads are regarded as a protective presence by those who wear them.")}
      {aspect("💼", "Business &amp; Career", "Traditionally worn in the hope of clarity and momentum in work.")}
      {aspect("🧘", "Meditation", "Associated with concentration and with steadier sadhana.")}
    </div>
  </div>
</section>

<section>
  <div class="wrap"><div class="prose">
    <h2 class="reveal">Mahalakshmi and the number seven</h2>
    <p class="reveal">Seven carries great weight in tradition: seven chakras, seven sacred rivers, seven tones of music, seven days of the week. The 7 Mukhi is said to be a manifestation of Mahalakshmi. In the Shiva Purana, Ananta Sarp, the cosmic serpent of boundlessness, presides over the bead. It is also linked to the Saptamatrikas, the seven divine mothers.</p>
    <div class="quote-block reveal">A merchant, ruined and destitute, sat on the banks of the Ganga and wept. Mahalakshmi appeared as an old woman and placed a seven-faced bead in his palm. "This is not wealth," she said. "This is the door through which wealth flows. But first, your heart must be worthy of it." On the seventh dawn his fortunes turned. He returned to the Ganga, but she was gone — only the soft scent of lotus remained.</div>
    <h3 class="reveal">The Shani (Saturn) connection</h3>
    <p class="reveal">Saturn is the planet of karma, discipline and delay. When it transits adversely, through Sade Sati or a Shani dasha, tradition describes setbacks and a pervasive heaviness. The 7 Mukhi is the bead most often recommended in Vedic and Tantric tradition for these periods, and a consecrated bead is believed by devotees to help appease Saturn's energy.</p>
  </div></div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">How to wear</span><h2 class="reveal">Activation &amp; <em>wearing</em></h2></div>
    <div class="steps">
      <div class="rite reveal"><span class="step">१</span><h3>Monday sunrise</h3><p>The traditional first wearing is on a Monday morning, the day of Shiva.</p></div>
      <div class="rite reveal"><span class="step">२</span><h3>Cleanse</h3><p>Dip in raw milk or clean water for a few minutes and wipe with a clean cloth.</p></div>
      <div class="rite reveal"><span class="step">३</span><h3>Chant</h3><p>Hold it to your heart and chant ॐ हुं नमः (Om Hum Namah) 7 or 108 times.</p></div>
      <div class="rite reveal"><span class="step">४</span><h3>Wear</h3><p>On a red or gold thread or silver or gold chain, touching the skin, close to the heart.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cols-2">
      <div class="panel reveal"><h3>Activated 7 Mukhi</h3><p>Nepal-sourced, certificate, 54-day Vedic &amp; Tantric consecration with 2 lakh chants and havan.</p><div class="price mt1">{nrs(ACT[7])}</div></div>
      <div class="panel reveal"><h3>Energized 7 Mukhi</h3><p>A genuine Nepal-sourced 7 Mukhi, energized and ready to wear, without the full consecration. In a Panchadhatu locket {nrs(ENG_LOCKET[7])}.</p><div class="price mt1">{nrs(ENG[7])}</div></div>
    </div>
    <p class="center mt2"><a class="btn btn-fire" href="collection.html">Choose your 7 Mukhi ✦</a></p>
    <p class="disclaimer">Benefits are traditional beliefs, not medical, legal or financial claims.</p>
  </div>
</section>
{cta_final("Ready to invite <em>Mahalakshmi's grace?</em>", "Order on WhatsApp or ask us a question first.")}
"""
seven += foot()
pages["7-mukhi-rudraksha.html"] = seven

# ================================================================ FAQ
faq = head("FAQ — Rudraksha Questions Answered | Rudrakhchya",
           "Answers about ordering, shipping, natural vs activated Rudraksha, certificates, pendants, wearing and care.",
           "faq.html", faq_ld())
faq += page_hero("Questions", "Frequently <em>asked</em>", "Short answers to the things people ask us most. If yours is missing, message us.")
faq += f"""
<section style="padding-top:1rem"><div class="wrap">{faq_html()}
  <p class="center mt3"><a class="btn btn-fire" href="{wa('Namaste, I have a question about Rudraksha.')}">Ask on WhatsApp ✦</a></p>
</div></section>
"""
faq += foot()
pages["faq.html"] = faq

# ================================================================ CONTACT
contact = head("Contact — Rudrakhchya | WhatsApp & Instagram",
               "Order or ask about Rudraksha on WhatsApp or Instagram. Free shipping in Nepal; India and worldwide shipping confirmed before you pay.",
               "contact.html")
contact += page_hero("We are here to guide you", "Reach <em>us</em>",
                     "Ask about the ritual, confirm availability, enquire about shipping, or place your order. We reply on WhatsApp and Instagram.")
contact += f"""
<section style="padding-top:1rem">
  <div class="wrap">
    <div class="contact-cards">
      <div class="panel reveal"><h3>💬 WhatsApp</h3><p>The fastest way. Ask about the ritual, check availability, confirm shipping or place your order.</p>
        <span class="big-link">+977-9823783486</span><a class="btn btn-fire" href="{wa('Namaste, I am interested in a Rudraksha.')}">Chat on WhatsApp</a></div>
      <div class="panel reveal"><h3>📸 Instagram</h3><p>Follow bead stories, ritual glimpses and availability, or send us a message.</p>
        <span class="big-link">@rudr_akshya</span><a class="btn btn-ghost" href="{IG}">Open Instagram</a></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">What can we help with?</span><h2 class="reveal">Start a <em>conversation</em></h2></div>
    <div class="cols-3 mt3">
      <div class="panel reveal"><h3>🛒 Place an order</h3><p>Tell us the bead and version. We confirm availability and guide you through.</p><p class="mt1"><a href="{wa('Namaste, I would like to place an order.')}" style="color:var(--gold)">Order on WhatsApp →</a></p></div>
      <div class="panel reveal"><h3>🪐 Choosing a bead</h3><p>Not sure which mukhi is right? Share your birth details and we will explain what tradition suggests.</p><p class="mt1"><a href="{wa('Namaste, please help me choose a Rudraksha.')}" style="color:var(--gold)">Ask on WhatsApp →</a></p></div>
      <div class="panel reveal"><h3>🌍 Shipping</h3><p>Message your country and we confirm the cost before you commit to anything.</p><p class="mt1"><a href="{wa('Namaste, what is the shipping cost to my country?')}" style="color:var(--gold)">Ask shipping →</a></p></div>
      <div class="panel reveal"><h3>🔱 The consecration</h3><p>Questions about the 54-day ritual or the Guru?</p><p class="mt1"><a href="about.html" style="color:var(--gold)">Read our story →</a></p></div>
      <div class="panel reveal"><h3>📜 Authenticity</h3><p>Ask for photos, a video or an X-ray report for the bead you are considering.</p><p class="mt1"><a href="authenticity.html" style="color:var(--gold)">How we verify →</a></p></div>
      <div class="panel reveal"><h3>📿 Wearing &amp; care</h3><p>How to wear your bead, which mantra, when to start.</p><p class="mt1"><a href="learn.html" style="color:var(--gold)">Read the guide →</a></p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center"><span class="eyebrow reveal">Delivery</span><h2 class="reveal">We ship <em>worldwide</em></h2></div>
    <div class="ship-grid">
      <div class="panel reveal"><h3>🇳🇵 Nepal</h3><p><b style="color:var(--gold)">Free shipping.</b> All orders within Nepal are delivered free.</p></div>
      <div class="panel reveal"><h3>🇮🇳 India</h3><p>Message us for the rate before you order. We ship across India.</p></div>
      <div class="panel reveal"><h3>🌍 Rest of the world</h3><p>Message your country and we confirm the cost before you pay.</p></div>
    </div>
  </div>
</section>
"""
contact += foot()
pages["contact.html"] = contact

# ================================================================ WRITE + SITEMAP
for name, content in pages.items():
    open(name, "w", encoding="utf8").write(content)
urls = ["" if n == "index.html" else n for n in pages]
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                              "".join("  <url><loc>%s/%s</loc></url>\n" % (SITE, u) for u in urls) + "</urlset>\n")
open("robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
print("built", len(pages), "pages")
