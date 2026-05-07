#!/usr/bin/env python3
"""Render all Simon Express subpages."""
import sys
sys.path.insert(0, '.')
from _build_helper import render

ARROW_SVG = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'

# ---- Schema fragments per-page ----
SERVICES_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Refrigerated Trucking Services",
  "provider": { "@type": "LocalBusiness", "@id": "https://www.simonexpress.com/#business", "name": "Simon Express" },
  "serviceType": "Refrigerated Over-the-Road Trucking",
  "areaServed": { "@type": "AdministrativeArea", "name": "Continental United States (48 states)" },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Simon Express Services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Temperature-Controlled Full Truckload" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Refrigerated Food Freight" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Full Truckload (FTL)" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dedicated Reefer Lanes" } }
    ]
  }
}
</script>
'''

CAREERS_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "title": "Class A CDL Reefer Driver",
  "description": "Simon Express is hiring Class A CDL drivers nationwide for over-the-road refrigerated freight across 48 states. Driver-nominated for Best Fleets to Drive For five years running (2022, 2023, 2024, 2025, 2026). Late-model Freightliner Cascadia tractors with Detroit DD15 engines and automatic transmissions, paired with Utility reefer trailers featuring iBright and Lynx Fleet telematics. Top-tier mileage pay, consistent reefer freight year-round, full benefits with 401(k) match after 90 days, real home time, paid orientation, referral bonuses, and pet- and rider-friendly policies. We pay competitively with the best fleets in the country and will match or beat documented competitor offers.",
  "datePosted": "2026-01-01",
  "validThrough": "2027-12-31",
  "employmentType": "FULL_TIME",
  "hiringOrganization": {
    "@type": "Organization",
    "@id": "https://www.simonexpress.com/#org",
    "name": "Simon Express",
    "sameAs": "https://www.simonexpress.com/",
    "logo": "https://www.simonexpress.com/assets/simon-logo-cropped.png"
  },
  "jobLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Salt Lake City",
      "addressRegion": "UT",
      "addressCountry": "US"
    }
  },
  "applicantLocationRequirements": { "@type": "Country", "name": "US" },
  "jobLocationType": "TELECOMMUTE",
  "industry": "Trucking & Transportation",
  "occupationalCategory": "53-3032 Heavy and Tractor-Trailer Truck Drivers",
  "qualifications": "Valid Class A CDL required, with at least 2 years of recent over-the-road experience. Clean MVR preferred — we will talk to candidates with anything in their record. Must be comfortable with 48-state OTR runs.",
  "responsibilities": "Operate a 53-foot refrigerated trailer over the road across the continental US. Transport food-grade freight in compliance with FSMA cold-chain protocols. Submit BOLs and PODs through the Simon Driver App. Communicate with dispatch on appointment changes, delays, and equipment issues. Maintain trailer set-point per load instructions.",
  "skills": "Class A CDL, refrigerated trailer operation, ELD compliance, FSMA cold-chain protocols, electronic document submission, OTR navigation, customer-facing dock interaction.",
  "jobBenefits": "Top-tier mileage pay, consistent weekly miles, full medical / dental / vision benefits, 401(k) match after 90 days, paid orientation, referral bonuses, real home time, late-model Freightliner Cascadia tractors, 53' refrigerated trailers, pet-friendly, rider-friendly.",
  "workHours": "Variable based on hours-of-service. Real home time scheduling — not 'we'll find you something' rhetoric.",
  "directApply": true
}
</script>
'''

FAQ_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Simon Express a good refrigerated trucking company?",
      "acceptedAnswer": { "@type": "Answer", "text": "Simon Express is a national refrigerated trucking carrier run by four generations of the Simon family on the floor, with 99.2% on-time delivery and a five-year run as a driver-nominated Best Fleets to Drive For carrier (2022\u20132026). The carrier specializes exclusively in food-grade freight in 53-foot reefer trailers across 48 states. Strengths include 24/7 human-staffed dispatch, late-model Freightliner Cascadia equipment, and full FSMA / FMCSA / SmartWay compliance." }
    },
    {
      "@type": "Question",
      "name": "What does Simon Express haul?",
      "acceptedAnswer": { "@type": "Answer", "text": "Food and food-grade freight only \u2014 produce, dairy, protein, frozen, beverage, and other refrigerated CPG. Full truckload, 53-foot reefers, all 48 states. Simon Express does not haul household goods, chemicals, or building materials." }
    },
    {
      "@type": "Question",
      "name": "What states does Simon Express serve?",
      "acceptedAnswer": { "@type": "Answer", "text": "All 48 states, with daily lanes coast to coast. Operations are headquartered in Salt Lake City, Utah." }
    },
    {
      "@type": "Question",
      "name": "What temperature ranges can Simon Express maintain?",
      "acceptedAnswer": { "@type": "Answer", "text": "From \u221220\u00b0F frozen to 70\u00b0F ambient, with continuous temperature monitoring on every trailer." }
    },
    {
      "@type": "Question",
      "name": "Does Simon Express offer dedicated lanes?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes \u2014 capacity-committed dedicated reefer lanes for shippers with consistent weekly volume, including assigned tractors and drivers, single-point dispatch, and volume-tier rates." }
    },
    {
      "@type": "Question",
      "name": "Is Simon Express FSMA compliant?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Simon Express meets or exceeds FDA Food Safety Modernization Act (FSMA) sanitary transport requirements, FMCSA / DOT regulations, and ELD requirements. SmartWay-certified carrier, fully insured." }
    }
  ]
}
</script>
'''

# Driver-recruiting-focused FAQ schema for the careers page.
CAREERS_FAQ_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Simon Express a good company to drive for?",
      "acceptedAnswer": { "@type": "Answer", "text": "Simon Express is a family-run national refrigerated carrier hiring Class A CDL drivers nationwide, driver-nominated for Best Fleets to Drive For every year from 2022 through 2026. Drivers get late-model Freightliner Cascadia tractors, consistent reefer freight year-round, top-tier mileage pay, full benefits with 401(k) match, paid orientation, referral bonuses, and real home time. Dispatch is human-staffed 24/7 \u2014 drivers reach a real person, not a phone tree." }
    },
    {
      "@type": "Question",
      "name": "How much do Simon Express drivers make?",
      "acceptedAnswer": { "@type": "Answer", "text": "Simon Express pays top-tier mileage rates, competitive with the best fleets in the country. The carrier matches or beats documented offers from competing fleets. Drivers can call recruiting at 801-260-7010 with a current pay number to discuss specific rates for their experience level and home base." }
    },
    {
      "@type": "Question",
      "name": "What kind of trucks does Simon Express drive?",
      "acceptedAnswer": { "@type": "Answer", "text": "Late-model Freightliner Cascadia tractors with Detroit DD15 engines and automatic transmissions, paired with 53-foot Utility trailers and Carrier reefers featuring iBright and Lynx Fleet telematics." }
    },
    {
      "@type": "Question",
      "name": "Is Simon Express pet- and rider-friendly?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Simon Express welcomes pets in the truck and allows passenger riders. Specifics on weight limits, breed restrictions, and rider sign-up are handled during orientation." }
    },
    {
      "@type": "Question",
      "name": "What experience does Simon Express require for Class A CDL drivers?",
      "acceptedAnswer": { "@type": "Answer", "text": "Simon Express requires Class A CDL drivers with at least 2 years of recent over-the-road experience. Clean MVR is preferred, but the recruiting team will discuss any record \u2014 context matters more than a checkbox. Call 801-260-7010 to talk it through." }
    },
    {
      "@type": "Question",
      "name": "What benefits does Simon Express offer drivers?",
      "acceptedAnswer": { "@type": "Answer", "text": "Full medical, dental, and vision insurance; 401(k) with company match after 90 days; paid orientation; referral bonuses; consistent weekly miles; pet- and rider-friendly policies; late-model equipment; and real home-time scheduling." }
    },
    {
      "@type": "Question",
      "name": "Where is Simon Express based?",
      "acceptedAnswer": { "@type": "Answer", "text": "Simon Express is headquartered in Salt Lake City, Utah, but hires drivers across the United States and runs lanes in 48 states." }
    }
  ]
}
</script>
'''

CONTACT_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "url": "https://www.simonexpress.com/contact.html",
  "mainEntity": {
    "@type": "LocalBusiness",
    "@id": "https://www.simonexpress.com/#business"
  }
}
</script>
'''

ABOUT_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "url": "https://www.simonexpress.com/about.html",
  "mainEntity": {
    "@type": "Organization",
    "@id": "https://www.simonexpress.com/#org"
  }
}
</script>
'''

# ============================================================
# 1.  SERVICES PAGE
# ============================================================
SERVICES_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Services</div>
    <h1>Cold chain.<br/><span class="accent">Coast to coast.</span></h1>
    <p><strong>Simon Express provides national refrigerated trucking services across 48 states.</strong> We operate 53-foot reefer trailers hauling temperature-controlled food freight &mdash; produce, dairy, protein, frozen, and beverage &mdash; with continuous monitoring from origin to dock. Full truckload, dedicated lanes, and team-driver options available. 24/7 dispatch.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">

    <article id="temperature-controlled" class="lane-row reveal">
      <div>
        <div class="label">01 — TEMPERATURE CONTROLLED</div>
        <h3>Set-point holds<br/>from origin to dock.</h3>
      </div>
      <div>
        <p>Multi-temp 53-foot reefer trailers with continuous temperature monitoring and tamper-evident seals. We pull temp logs at every key — origin, fuel, rest, destination — and we hand them to you. If the load needs to be cold, it stays cold. If it needs to be frozen, it stays frozen.</p>
        <ul class="specs">
          <li>−20°F to 70°F set-point range</li>
          <li>Continuous temperature monitoring</li>
          <li>Sealed at origin, scanned at destination</li>
          <li>Pre-cooled before live load</li>
          <li>Multi-temp capable on dual-zone units</li>
          <li>Reefer download on every drop</li>
        </ul>
      </div>
    </article>

    <article id="refrigerated-food" class="lane-row reveal">
      <div>
        <div class="label">02 — REFRIGERATED FOOD</div>
        <h3>Food is all<br/>we haul.</h3>
      </div>
      <div>
        <p>We don't dabble in chemicals, we don't haul building materials, we don't do household goods. We move food — coast to coast, every day. Produce, dairy, protein, frozen, beverage, refrigerated CPG. Lanes from California to the Carolinas, the Pacific Northwest to South Florida. Drivers trained on cold-chain protocols, dispatchers who know what "wet ice" and "tail temp" actually mean.</p>
        <ul class="specs">
          <li>Produce — leafy greens, berries, root</li>
          <li>Dairy — fluid, cultured, cheese</li>
          <li>Protein — boxed beef, pork, poultry</li>
          <li>Frozen — finished goods and bulk</li>
          <li>Beverage — DSD and full-pallet</li>
          <li>Specialty CPG — refrigerated and shelf-stable food</li>
        </ul>
      </div>
    </article>

    <article id="full-truckload" class="lane-row reveal">
      <div>
        <div class="label">03 — FULL TRUCKLOAD</div>
        <h3>One trailer.<br/>One driver.<br/>Door to door.</h3>
      </div>
      <div>
        <p>Dedicated 53-foot reefers — no transfers, no intermediate handling, no LTL surprises. Team-driver options for time-critical lanes and West Coast turnarounds. We accept tenders fast, we pick up on time, and our on-time delivery sits at 99.2%.</p>
        <ul class="specs">
          <li>53-foot reefer trailers</li>
          <li>Solo or team driver</li>
          <li>Live-load and drop-and-hook</li>
          <li>Coast-to-coast lanes</li>
          <li>Power-only available on request</li>
          <li>EDI / API tendering</li>
        </ul>
      </div>
    </article>

    <article id="dedicated-lanes" class="lane-row reveal">
      <div>
        <div class="label">04 — DEDICATED LANES</div>
        <h3>Same trucks.<br/>Same drivers.<br/>Every week.</h3>
      </div>
      <div>
        <p>If you've got consistent weekly volume on a lane, we'll commit capacity to it. Same trucks, same drivers, same dispatcher on your account. You get predictable cost, predictable transit time, and a team that learns your facility's quirks the same way we know our own yard.</p>
        <ul class="specs">
          <li>Capacity-committed weekly tonnage</li>
          <li>Single point of contact in dispatch</li>
          <li>Volume-tier rate structure</li>
          <li>Account-specific KPI reporting</li>
          <li>Round-trip and back-haul optimization</li>
          <li>Onboarding to your TMS</li>
        </ul>
      </div>
    </article>

  </div>
</section>

<section class="stats-strip">
  <div class="wrap">
    <div class="row">
      <div class="stat"><div class="big">48</div><div class="small">STATES SERVED</div></div>
      <div class="stat"><div class="big">−20°F</div><div class="small">REEFER CAPABLE</div></div>
      <div class="stat"><div class="big">53'</div><div class="small">REEFER TRAILERS</div></div>
      <div class="stat"><div class="big">99.2%</div><div class="small">ON-TIME DELIVERY</div></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="glow"></div>
  <div class="inner reveal">
    <div>
      <div class="kicker" style="color:#fff;">START THE LOAD</div>
      <h2 style="margin-top:14px;">Got a lane to run?<br/><span class="accent">Let's quote it.</span></h2>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-xl" data-open-quote>Get a Quote {ARROW_SVG}</button>
      <a href="tel:8012607010" class="btn btn-xl ghost-light">Call 801-260-7010</a>
    </div>
  </div>
</section>
'''

render(
    "services.html",
    title="Services — Refrigerated Trucking · Simon Express · 48 States",
    description="Full truckload refrigerated trucking services from Simon Express. 53' reefer trailers hauling produce, dairy, protein, frozen, and beverage freight across all 48 states. Dedicated lanes available.",
    canonical="services.html",
    body=SERVICES_BODY,
    extra_schema=SERVICES_SCHEMA + FAQ_SCHEMA,
)

# ============================================================
# 2.  FLEET PAGE
# ============================================================
FLEET_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Fleet</div>
    <h1>Late-model.<br/><span class="accent">Locked tight.</span></h1>
    <p><strong>The Simon Express fleet is built around late-model Freightliner Cascadia tractors with Detroit DD15 engines and automatic transmissions, paired with Utility trailers and Carrier reefers.</strong> Every unit runs full telematics through iBright and Lynx Fleet. Air-ride suspension, plate floors, maintained on a strict PM schedule.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">

    <article class="lane-row reveal">
      <div>
        <div class="label">POWER</div>
        <h3>Freightliner<br/>Cascadia.</h3>
      </div>
      <div>
        <p>The Cascadia is the most fuel-efficient over-the-road tractor in the country, and that math compounds when you run it 48 states. Our fleet runs late-model Cascadias with the Detroit DD15 engine and an automatic transmission. The drivers like the cab. The accountants like the MPG. Everybody wins.</p>
        <ul class="specs">
          <li>Late-model Freightliner Cascadia</li>
          <li>Detroit DD15 engine</li>
          <li>Automatic transmission</li>
          <li>Air-ride suspension</li>
          <li>Inverter for the bunk</li>
        </ul>
      </div>
    </article>

    <article class="lane-row reveal">
      <div>
        <div class="label">TRAILER</div>
        <h3>53-foot reefers.<br/>Air-ride. Plate floors.</h3>
      </div>
      <div>
        <p>53-foot Utility reefer trailers with stainless or aluminum plate floors, air-ride suspension, and tandem-slide. Carrier reefer units, regularly serviced, regularly downloaded. We don't let a unit on the road if its temp record isn't clean.</p>
        <ul class="specs">
          <li>53' refrigerated trailers</li>
          <li>Utility trailers with Carrier reefers</li>
          <li>Air-ride suspension</li>
          <li>Plate floors for produce</li>
          <li>Dual-zone capable</li>
          <li>Tamper-evident seals on every load</li>
        </ul>
      </div>
    </article>

    <article class="lane-row reveal">
      <div>
        <div class="label">TELEMATICS</div>
        <h3>Always-on<br/>visibility.</h3>
      </div>
      <div>
        <p>Every tractor and every trailer is connected through iBright and Lynx Fleet telematics. Live tractor telematics, live reefer telematics, live HOS clock. When you ask "where's my load?" — we answer in seconds, not minutes. When the temperature drifts, the reefer talks to dispatch before the driver picks up the phone.</p>
        <ul class="specs">
          <li>iBright tractor telematics</li>
          <li>Lynx Fleet reefer telematics</li>
          <li>ELD-compliant HOS</li>
          <li>Geofenced arrival / departure</li>
          <li>Set-point alerts to dispatch</li>
          <li>Temp logs available on demand</li>
        </ul>
      </div>
    </article>

    <article class="lane-row reveal">
      <div>
        <div class="label">SAFETY</div>
        <h3>Built-in.<br/>Not bolted on.</h3>
      </div>
      <div>
        <p>Forward-looking radar and camera, automatic emergency braking, lane-departure warning, side-object detection — every truck, no exceptions. Drivers are scored monthly on a real safety scorecard, not a guess. Annual training. Quarterly refreshers. We pay for safety because cheap insurance doesn't exist.</p>
        <ul class="specs">
          <li>Forward collision avoidance</li>
          <li>Automatic emergency braking</li>
          <li>Lane-departure warning</li>
          <li>Roll stability control</li>
          <li>Driver safety scorecards</li>
          <li>Annual + quarterly training</li>
        </ul>
      </div>
    </article>

  </div>
</section>

<section class="cta-band">
  <div class="glow"></div>
  <div class="inner reveal">
    <div>
      <div class="kicker" style="color:#fff;">RIDE A NEW CASCADIA</div>
      <h2 style="margin-top:14px;">Ready to drive<br/><span class="accent">a real truck?</span></h2>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-xl" data-open-apply>Start Application {ARROW_SVG}</button>
      <a href="tel:8012607010" class="btn btn-xl ghost-light">Call Recruiting</a>
    </div>
  </div>
</section>
'''

render(
    "fleet.html",
    title="Fleet — Late-Model Cascadias & 53' Reefers · Simon Express",
    description="The Simon Express fleet — late-model Freightliner Cascadias paired with 53-foot dual-zone reefer trailers, full telematics, and active safety on every truck.",
    canonical="fleet.html",
    body=FLEET_BODY,
)

# ============================================================
# 3.  ABOUT PAGE
# ============================================================
ABOUT_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>About</div>
    <h1>Three generations.<br/><span class="accent">One last name.</span></h1>
    <p>Simon Express is a national refrigerated carrier with a family business at its core — same family, same surname, four generations on the floor. We've been hauling food across America for over fifty years.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1fr 1.4fr;gap:80px;align-items:start;" class="about-row reveal">
      <div>
        <div class="kicker">OUR STORY</div>
      </div>
      <div>
        <p style="font-size:20px;line-height:1.55;color:var(--ink);margin-bottom:24px;">
          The Simon family has been moving food across America for four generations on the floor. What started with a single truck has grown into a 48-state refrigerated carrier running lanes coast to coast — but the way we operate hasn't changed. Family answers the phone. Family runs dispatch. Family signs the paychecks.
        </p>
        <p style="font-size:16px;line-height:1.7;color:var(--mute);margin-bottom:18px;">
          We're not the biggest carrier in the country. We don't want to be. We're the carrier you call when you need someone who'll pick up the phone at 2am, when the receiver's giving your driver a hard time, when the weather's against you in Wyoming and the load needs to be in Dallas in eighteen hours. The carrier that hits the dock and hands you a clean temperature log. The carrier whose drivers know what they're hauling and treat it like it's their own.
        </p>
        <p style="font-size:16px;line-height:1.7;color:var(--mute);">
          Three generations of doing one thing. We're not changing the model.
        </p>
      </div>
    </div>
  </div>
</section>

<style>@media (max-width:980px){{.about-row{{grid-template-columns:1fr !important;gap:32px !important;}}}}</style>

<section class="section section-sm" style="background:var(--white);border-top:1px solid var(--line);border-bottom:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker reveal" style="margin-bottom:32px;">THE TIMELINE</div>
    <div class="timeline">
      <div class="item reveal">
        <div class="year">1970s</div>
        <div>
          <h3>The first truck.</h3>
          <p>The Simon family bought its first refrigerated tractor and started hauling produce. One truck, one driver, one Carrier reefer unit, and a phone book full of customers who needed someone reliable.</p>
        </div>
      </div>
      <div class="item reveal">
        <div class="year">1990s</div>
        <div>
          <h3>The second generation.</h3>
          <p>The kids who grew up around the trucks came back from college and grew the operation. New tractors, new lanes east of the Mississippi and west to the coast, the first dedicated dairy and protein customers we still serve today.</p>
        </div>
      </div>
      <div class="item reveal">
        <div class="year">2010s</div>
        <div>
          <h3>48-state coverage.</h3>
          <p>Modern telematics, ELD compliance ahead of the deadline, and lanes from Seattle to Miami, Boston to San Diego. The reefer fleet expanded into multi-temp dual-zone trailers. The cold chain got tighter. So did our on-time numbers.</p>
        </div>
      </div>
      <div class="item reveal">
        <div class="year">Today</div>
        <div>
          <h3>The fourth generation.</h3>
          <p>The next Simons are on the floor — running dispatch, walking the yard, learning the business the same way the previous generations did. The trucks are newer, the technology is sharper, the family is the same.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section values">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <div class="kicker">HOW WE OPERATE</div>
        <h2 style="margin-top:14px;">Three things we<br/><span class="accent">won't compromise on.</span></h2>
      </div>
      <p class="lede">A national carrier still answers to the family name. Here's where that name shows up in how we run.</p>
    </div>
    <div class="rule-grid reveal-stagger">
      <div class="cell">
        <div class="num">01</div>
        <h3>The Cold Chain.</h3>
        <p>If a load is supposed to be 34°F, it's 34°F when it leaves and 34°F when it arrives. Continuous monitoring on every trailer. Temp logs handed to you, not buried in a portal. If the cold chain breaks, you hear it from us first.</p>
      </div>
      <div class="cell">
        <div class="num">02</div>
        <h3>The Phone.</h3>
        <p>Dispatch is staffed 24/7 by humans, not phone trees. You call our number, a person picks up. Drivers can reach a real dispatcher anytime — and so can you, the customer.</p>
      </div>
      <div class="cell">
        <div class="num">03</div>
        <h3>The Truck.</h3>
        <p>Late-model Cascadias, regular maintenance, no skipped PMs. A driver's truck is their workplace. We don't put anyone in equipment we wouldn't drive ourselves.</p>
      </div>
    </div>
  </div>
</section>

<section id="safety" class="dark-section section-lg">
  <div class="glow"></div>
  <div class="wrap" style="position:relative;">
    <div style="display:grid;grid-template-columns:1fr 1.4fr;gap:64px;align-items:start;" class="safety-row reveal">
      <div>
        <div class="kicker" style="color:#fff;">SAFETY &amp; COMPLIANCE</div>
      </div>
      <div>
        <h2 class="block-h" style="margin-bottom:32px;">Boring on paper.<br/><span style="color:var(--red);">Important in practice.</span></h2>
        <p style="font-size:17px;line-height:1.7;color:var(--mute-3);margin-bottom:24px;">
          We meet or exceed every FMCSA, DOT, and FDA Food Safety Modernization Act standard that applies to refrigerated food transportation. ELD compliance, hours-of-service discipline, sanitary trailer protocols, food-grade load handling — all baked into the way we dispatch, not bolted on as an afterthought.
        </p>
        <ul class="specs" style="display:grid;grid-template-columns:1fr 1fr;gap:14px 32px;">
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>FMCSA-compliant ELD</li>
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>FSMA Sanitary Transport</li>
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>SmartWay Carrier</li>
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>Fully insured</li>
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>Driver safety scorecards</li>
          <li style="font-family:var(--mono);font-size:13px;color:#fff;display:flex;gap:10px;align-items:center;"><span style="width:6px;height:6px;background:var(--red);flex-shrink:0;"></span>Annual driver training</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<style>@media (max-width:980px){{.safety-row{{grid-template-columns:1fr !important;gap:24px !important;}}}}</style>

<section class="cta-band">
  <div class="glow"></div>
  <div class="inner reveal">
    <div>
      <div class="kicker" style="color:#fff;">WORK WITH FAMILY</div>
      <h2 style="margin-top:14px;">Three generations.<br/><span class="accent">One handshake.</span></h2>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-xl" data-open-quote>Get a Quote {ARROW_SVG}</button>
      <a href="contact.html" class="btn btn-xl ghost-light">Contact Us</a>
    </div>
  </div>
</section>
'''

render(
    "about.html",
    title="About — Three Generations of Family Trucking · Simon Express",
    description="Simon Express is a national refrigerated trucking carrier run by four generations of the Simon family on the floor. Over 50 years hauling food freight across 48 states.",
    canonical="about.html",
    body=ABOUT_BODY,
    extra_schema=ABOUT_SCHEMA,
)

# ============================================================
# 4.  CAREERS PAGE
# ============================================================
CAREERS_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Careers</div>
    <div class="bf-badge" style="margin:8px 0 28px;" aria-label="Best Fleets to Drive For nominee, five years running 2022 to 2026">
      <div class="bf-laurel">
        <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 34 Q10 26 12 16 Q18 14 22 22 Q24 30 22 36"/>
          <path d="M14 34 Q14 44 20 50 Q26 48 26 40 Q24 34 22 36"/>
          <path d="M50 34 Q54 26 52 16 Q46 14 42 22 Q40 30 42 36"/>
          <path d="M50 34 Q50 44 44 50 Q38 48 38 40 Q40 34 42 36"/>
          <path d="M22 36 Q32 42 42 36" opacity="0.4"/>
          <text x="32" y="40" text-anchor="middle" font-family="Oswald, sans-serif" font-weight="700" font-size="18" fill="currentColor" stroke="none">★</text>
        </svg>
      </div>
      <div class="bf-body">
        <div class="bf-eyebrow">Nominated · Five Years Running</div>
        <div class="bf-program">Best Fleets to Drive For</div>
        <div class="bf-years"><strong>2022</strong> &middot; <strong>2023</strong> &middot; <strong>2024</strong> &middot; <strong>2025</strong> &middot; <strong>2026</strong></div>
      </div>
    </div>
    <h1>Drive for<br/><span class="accent">a family.</span></h1>
    <p><strong>Simon Express is hiring Class A CDL reefer drivers nationwide.</strong> National 48-state OTR refrigerated freight, late-model Freightliner Cascadias, top-tier mileage pay, full benefits with 401(k) match, real home time, paid orientation, referral bonuses, and pet- and rider-friendly policies. Driver-nominated for Best Fleets to Drive For five years running (2022&ndash;2026). Apply online or call 801-260-7010.</p>
  </div>
</section>

<section class="dark-section section-lg">
  <div class="glow"></div>
  <div class="wrap" style="position:relative;">
    <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:80px;align-items:center;" class="hire-row">
      <div class="reveal">
        <div class="kicker" style="color:#fff;">WHY DRIVE FOR SIMON</div>
        <h2 class="block-h" style="margin-top:14px;">
          Top pay.<br/>
          Steady freight.<br/>
          <div><span class="red-bar">Real home time.</span></div>
        </h2>
        <p style="font-size:18px;line-height:1.6;color:var(--mute-3);max-width:520px;margin:48px 0 36px;">
          A national fleet that still knows your name. You'll know dispatch by name, your truck by number, and you'll run real miles every week. We pay competitively and we mean it — call us with the number you're being offered elsewhere and we'll work to beat it.
        </p>
        <div style="display:flex;gap:14px;flex-wrap:wrap;">
          <button type="button" class="btn btn-lg" data-open-apply>Start Application {ARROW_SVG}</button>
          <a href="tel:8012607010" class="btn btn-lg ghost-light">Talk to a Recruiter</a>
        </div>
      </div>
      <div class="careers-card reveal">
        <div class="head">WHAT YOU GET</div>
        <ul>
          <li>{CHECK_SVG}<span>Top pay in the industry — call to compare</span></li>
          <li>{CHECK_SVG}<span>Consistent reefer miles, week after week</span></li>
          <li>{CHECK_SVG}<span>Late-model Freightliner Cascadias</span></li>
          <li>{CHECK_SVG}<span>53' reefer trailers — air-ride, well-maintained</span></li>
          <li>{CHECK_SVG}<span>Full benefits + 401(k) match after 90 days</span></li>
          <li>{CHECK_SVG}<span>Quick orientation + referral bonuses</span></li>
          <li>{CHECK_SVG}<span>Home time that actually happens</span></li>
          <li>{CHECK_SVG}<span>Pet &amp; rider friendly</span></li>
        </ul>
        <div class="pay-grid">
          <div>
            <div class="h">Top<br/>Pay</div>
            <div class="body">Competitive with the best fleets in the country — call us and we'll beat the number you're looking at.</div>
          </div>
          <div>
            <div class="h accent">Good<br/>Miles</div>
            <div class="body">Steady reefer freight year-round. No sitting. No "we'll find you something."</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>@media (max-width:980px){{.hire-row{{grid-template-columns:1fr !important;gap:48px !important;}}}}</style>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <div class="kicker">REQUIREMENTS</div>
        <h2 style="margin-top:14px;">What we're<br/><span class="accent">looking for.</span></h2>
      </div>
      <p class="lede">Straightforward. Honest work, honest qualifications.</p>
    </div>
    <div class="rule-grid cols-2 reveal-stagger">
      <div class="cell">
        <h3>Class A CDL</h3>
        <p>Valid Class A commercial driver's license with at least 2 years of recent over-the-road experience.</p>
      </div>
      <div class="cell">
        <h3>Driving Record</h3>
        <p>Clean MVR preferred. We'll talk to candidates with anything in their record — context matters more than a check-box.</p>
      </div>
      <div class="cell">
        <h3>OTR Comfortable</h3>
        <p>Our lanes are 48-state. You'll be away from home and we'll get you home. Steady freight beats a rotating schedule any day.</p>
      </div>
      <div class="cell">
        <h3>Customer Side</h3>
        <p>You represent Simon at every dock. Show up clean, hit your appointment time, hand the receiver a paper-clean BOL. The rest is straightforward.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--white);border-top:1px solid var(--line);">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <div class="kicker">DRIVER FAQ</div>
        <h2 style="margin-top:14px;">What drivers<br/><span class="accent">ask first.</span></h2>
      </div>
      <p class="lede">The straight answers to the questions that matter before you sign on. More questions? Recruiting picks up at <a href="tel:8012607010" style="color:var(--red);font-weight:600;">801-260-7010</a>.</p>
    </div>
    <div class="faq-grid reveal-stagger">
      <details class="faq-item">
        <summary><h3>Is Simon Express a good company to drive for?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Family-run national refrigerated carrier, driver-nominated for Best Fleets to Drive For five years running (2022&ndash;2026). Late-model Freightliner Cascadia tractors, consistent reefer freight year-round, top-tier mileage pay, full benefits with 401(k) match, paid orientation, referral bonuses, and real home time. Dispatch is human-staffed 24/7 &mdash; you reach a person, not a phone tree.</p>
      </details>
      <details class="faq-item">
        <summary><h3>How much do Simon Express drivers make?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Top-tier mileage rates, competitive with the best fleets in the country. Call us with the number you&apos;re being offered elsewhere and we&apos;ll work to beat it. Specifics depend on experience level, home base, and lane preference. Recruiting at <a href="tel:8012607010" style="color:var(--red);font-weight:600;">801-260-7010</a>.</p>
      </details>
      <details class="faq-item">
        <summary><h3>What kind of trucks will I drive?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Late-model Freightliner Cascadia tractors with Detroit DD15 engines and automatic transmissions, paired with 53-foot Utility trailers and Carrier reefers featuring iBright and Lynx Fleet telematics. Strict PM schedule.</p>
      </details>
      <details class="faq-item">
        <summary><h3>Are you pet- and rider-friendly?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Yes to both. Pets in the truck and passenger riders are welcome. Specifics on weight limits, breeds, and rider sign-up are walked through in orientation.</p>
      </details>
      <details class="faq-item">
        <summary><h3>What experience do you require?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>We require Class A CDL with at least 2 years of recent over-the-road experience. Clean MVR is preferred &mdash; but we&apos;ll talk to candidates with anything in their record. Context matters more than a checkbox.</p>
      </details>
      <details class="faq-item">
        <summary><h3>What benefits come with the job?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Full medical, dental, and vision; 401(k) with company match after 90 days; paid orientation; referral bonuses; consistent weekly miles; pet- and rider-friendly; late-model equipment; real home-time scheduling.</p>
      </details>
      <details class="faq-item">
        <summary><h3>What kind of home time can I expect?</h3><span class="faq-toggle" aria-hidden="true">+</span></summary>
        <p>Real home time &mdash; not the &quot;we&apos;ll find you something&quot; rhetoric you hear elsewhere. Specifics depend on the lane, but recruiting walks through realistic schedules during the call rather than after you sign on.</p>
      </details>
    </div>
  </div>
</section>

<section class="form-section" style="background:var(--paper);">
  <div class="wrap">
    <div class="row">
      <div class="contact-info reveal">
        <div class="kicker">APPLY NOW</div>
        <h2 style="margin-top:14px;">Three minutes.<br/>One callback.<br/><span style="color:var(--red);">Maybe a job.</span></h2>
        <p class="lede">Fill out the form on the right and recruiting will call you back within one business day. Want to talk first? Call <strong>801-260-7010</strong> — a real person will pick up.</p>
        <div class="info-list" style="margin-top:32px;">
          <div class="item">
            <div class="label">RECRUITING</div>
            <div class="value"><a href="tel:8012607010">801-260-7010</a></div>
          </div>
          <div class="item">
            <div class="label">EMAIL</div>
            <div class="value"><a href="mailto:info@simonexpress.com">info@simonexpress.com</a></div>
          </div>
          <div class="item">
            <div class="label">HQ</div>
            <div class="value">Salt Lake City, UT</div>
          </div>
          <div class="item">
            <div class="label">HOURS</div>
            <div class="value">24/7 Dispatch · Recruiting Mon–Fri</div>
          </div>
        </div>
      </div>

      <div class="form-card reveal">
        <h2>Driver application.</h2>
        <p class="intro">A real person reads every one of these. Recruiting will call you within one business day.</p>
        <form data-simon-form="apply" novalidate>
          <div class="form-status" role="alert"></div>
          <div class="field-row">
            <div class="field"><label>First Name <span class="required">*</span></label><input name="firstName" type="text" required autocomplete="given-name"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Last Name <span class="required">*</span></label><input name="lastName" type="text" required autocomplete="family-name"/><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field"><label>Email <span class="required">*</span></label><input name="email" type="email" required autocomplete="email"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Phone <span class="required">*</span></label><input name="phone" type="tel" required autocomplete="tel"/><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field"><label>City / State <span class="required">*</span></label><input name="location" type="text" required placeholder="e.g. Boise, ID"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Class A CDL <span class="required">*</span></label><select name="cdlA" required><option value="">Select…</option><option>Yes — 2+ years OTR experience</option><option>Yes — less than 2 years OTR</option><option>No</option></select><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field">
              <label>Years Driving</label>
              <select name="yearsDriving"><option value="">Select…</option><option>Less than 1</option><option>1–2</option><option>3–5</option><option>6–10</option><option>10+</option></select>
            </div>
            <div class="field">
              <label>Endorsements</label>
              <select name="endorsements"><option value="">Select…</option><option>None</option><option>Hazmat</option><option>Tanker</option><option>Doubles/Triples</option><option>Multiple</option></select>
            </div>
          </div>
          <div class="field"><label>Anything you want us to know?</label><textarea name="notes" placeholder="Home time preferences, equipment preferences, schedule…"></textarea></div>
          <button type="submit" class="btn btn-lg" style="width:100%;justify-content:center;">Send Application {ARROW_SVG}</button>
        </form>
      </div>
    </div>
  </div>
</section>
'''

render(
    "careers.html",
    title="Careers — Class A CDL Drivers Wanted · Simon Express · 48-State Reefer",
    description="Now hiring Class A CDL drivers at Simon Express. Late-model Freightliner Cascadias, 53' reefer trailers, top pay, real home time. Apply in under 3 minutes.",
    canonical="careers.html",
    body=CAREERS_BODY,
    extra_schema=CAREERS_SCHEMA + CAREERS_FAQ_SCHEMA,
)

# ============================================================
# 5.  DRIVER APP PAGE
# ============================================================
DRIVER_APP_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Driver App</div>
    <h1>The Simon<br/><span class="accent">Driver App.</span></h1>
    <p>Every tool you need on the road, in one place. No clipboards. No three-separate-apps. No dispatch calling because paperwork is missing.</p>
  </div>
</section>

<section class="app-section" style="padding:80px 0;">
  <div class="wrap">
    <div class="row">
      <div class="reveal">
        <div class="kicker">BUILT FOR DRIVERS</div>
        <h2 style="margin-top:14px;">One app.<br/><span style="color:var(--red);">Whole job.</span></h2>
        <p class="lede">
          Built by people who've done the job. Talk to dispatch, submit your paperwork, find your fuel, run your route — without juggling apps. Works offline when you're out of signal, syncs the moment you're back.
        </p>
        <div class="app-features reveal-stagger">
          <div class="app-feature">
            <div class="icon-box"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9l-6-6z"/><path d="M14 3v6h6M9 13h6M9 17h6"/></svg></div>
            <div><h4>Document Submission</h4><p>Snap BOLs, PODs, and receipts. Auto-synced to dispatch before wheels stop rolling.</p></div>
          </div>
          <div class="app-feature">
            <div class="icon-box"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="11" height="18" rx="1"/><path d="M14 8h3a2 2 0 012 2v7a2 2 0 01-4 0v-5l-1-2"/></svg></div>
            <div><h4>Fuel Locations</h4><p>Approved stops and live diesel prices — one tap from any exit. Save your card, save your time.</p></div>
          </div>
          <div class="app-feature">
            <div class="icon-box"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M6 16V9a4 4 0 014-4h4M18 8v7a4 4 0 01-4 4h-4"/></svg></div>
            <div><h4>Smart Routing</h4><p>HOS-aware routes with live reroutes for weather, traffic, and parking availability.</p></div>
          </div>
          <div class="app-feature">
            <div class="icon-box"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5l8-3z"/><path d="M9 12l2 2 4-4"/></svg></div>
            <div><h4>HOS / ELD</h4><p>Hours of service, ELD compliance, and breaks tracked at a glance. No surprises at a scale.</p></div>
          </div>
        </div>
      </div>
      <div class="phone-mockup reveal" aria-hidden="true">
        <div class="phone">
          <div class="screen">
            <div class="status"><span>9:41</span><span>●●●●</span></div>
            <div class="notch"></div>
            <div class="body">
              <div class="greet">GOOD MORNING</div>
              <div class="driver-id">DRIVER</div>
              <div class="load-card">
                <div class="top">CURRENT LOAD · LD# 0060423</div>
                <div class="route">SLC, UT → DALLAS, TX</div>
                <div class="meta">1,230 mi · Deliver Wed 06:00</div>
              </div>
              <div class="tile-grid">
                <div class="tile"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9l-6-6z"/><path d="M14 3v6h6M9 13h6M9 17h6"/></svg><div class="label">Submit BOL</div></div>
                <div class="tile"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="11" height="18" rx="1"/><path d="M14 8h3a2 2 0 012 2v7a2 2 0 01-4 0v-5l-1-2"/></svg><div class="label">Fuel Stops</div></div>
                <div class="tile"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M6 16V9a4 4 0 014-4h4M18 8v7a4 4 0 01-4 4h-4"/></svg><div class="label">Route</div></div>
                <div class="tile"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5l8-3z"/><path d="M9 12l2 2 4-4"/></svg><div class="label">HOS / ELD</div></div>
              </div>
              <div class="fuel-card">
                <div class="top">NEXT FUEL STOP</div>
                <div class="row">
                  <div><div class="station">Love's · Rawlins, WY</div><div class="miles">142 mi · $3.84/gal</div></div>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="glow"></div>
  <div class="inner reveal">
    <div>
      <div class="kicker" style="color:#fff;">DRIVE WITH US</div>
      <h2 style="margin-top:14px;">Ready to use this<br/><span class="accent">on every load?</span></h2>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-xl" data-open-apply>Start Application {ARROW_SVG}</button>
      <a href="tel:8012607010" class="btn btn-xl ghost-light">Call 801-260-7010</a>
    </div>
  </div>
</section>
'''

render(
    "driver-app.html",
    title="Driver App — One App, Whole Job · Simon Express",
    description="The Simon Express Driver App — BOL submission, approved fuel stops, HOS-aware routing, and HOS / ELD compliance in one place. Built for drivers, by people who've done the job.",
    canonical="driver-app.html",
    body=DRIVER_APP_BODY,
)

# ============================================================
# 6.  CONTACT PAGE
# ============================================================
CONTACT_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Contact</div>
    <h1>Pick up<br/><span class="accent">the phone.</span></h1>
    <p>Dispatch is staffed 24 hours a day, every day. Real humans on the line. Whether you're shipping freight across the country, looking to drive, or just need to know where your load is — call, email, or fill the form.</p>
  </div>
</section>

<section class="form-section">
  <div class="wrap">
    <div class="row">
      <div class="contact-info reveal">
        <div class="kicker">DIRECT LINE</div>
        <h2 style="margin-top:14px;">One number.<br/>Open 24/7.</h2>
        <p class="lede">Dispatch is staffed around the clock. Recruiting and accounts run weekday business hours. Either way, a person picks up — not a tree.</p>
        <div class="info-list" style="margin-top:32px;">
          <div class="item">
            <div class="label">PHONE</div>
            <div class="value"><a href="tel:8012607010"><strong>801-260-7010</strong></a><br/><span style="font-size:13px;color:var(--mute);">Dispatch &middot; Recruiting &middot; Accounts</span></div>
          </div>
          <div class="item">
            <div class="label">EMAIL</div>
            <div class="value"><a href="mailto:info@simonexpress.com">info@simonexpress.com</a></div>
          </div>
          <div class="item">
            <div class="label">HQ</div>
            <div class="value">Salt Lake City, Utah<br/><span style="font-size:13px;color:var(--mute);">Visit by appointment</span></div>
          </div>
          <div class="item">
            <div class="label">HOURS</div>
            <div class="value">Dispatch — 24/7<br/>Recruiting / Accounts — Mon–Fri</div>
          </div>
          <div class="item">
            <div class="label">COVERAGE</div>
            <div class="value">All 48 states<br/><span style="font-size:13px;color:var(--mute);">53' refrigerated trailers</span></div>
          </div>
        </div>
      </div>

      <div class="form-card reveal">
        <h2>Send a message.</h2>
        <p class="intro">For freight quotes, driver applications, billing, or general questions. We reply within one business day.</p>
        <form data-simon-form="contact" novalidate>
          <div class="form-status" role="alert"></div>
          <div class="field-row">
            <div class="field"><label>Name <span class="required">*</span></label><input name="name" type="text" required autocomplete="name"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Company</label><input name="company" type="text" autocomplete="organization"/></div>
          </div>
          <div class="field-row">
            <div class="field"><label>Email <span class="required">*</span></label><input name="email" type="email" required autocomplete="email"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Phone</label><input name="phone" type="tel" autocomplete="tel"/></div>
          </div>
          <div class="field">
            <label>What is this about? <span class="required">*</span></label>
            <select name="topic" required>
              <option value="">Select…</option>
              <option>Freight quote</option>
              <option>Driver application</option>
              <option>Existing shipment</option>
              <option>Billing / Accounts</option>
              <option>Press / Media</option>
              <option>Other</option>
            </select>
            <div class="error-msg">Required</div>
          </div>
          <div class="field"><label>Message <span class="required">*</span></label><textarea name="message" required></textarea><div class="error-msg">Required</div></div>
          <button type="submit" class="btn btn-lg" style="width:100%;justify-content:center;">Send Message {ARROW_SVG}</button>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="glow"></div>
  <div class="inner reveal">
    <div>
      <div class="kicker" style="color:#fff;">URGENT FREIGHT?</div>
      <h2 style="margin-top:14px;">Don't fill a form.<br/><span class="accent">Call dispatch.</span></h2>
    </div>
    <div class="actions">
      <a href="tel:8012607010" class="btn btn-xl">Call 801-260-7010 {ARROW_SVG}</a>
    </div>
  </div>
</section>
'''

render(
    "contact.html",
    title="Contact — 801-260-7010 · 24/7 Dispatch · Simon Express",
    description="Contact Simon Express — national refrigerated trucking carrier serving all 48 states. 24/7 dispatch at 801-260-7010 or info@simonexpress.com.",
    canonical="contact.html",
    body=CONTACT_BODY,
    extra_schema=CONTACT_SCHEMA + FAQ_SCHEMA,
)

# ============================================================
# 7.  QUOTE PAGE (standalone)
# ============================================================
QUOTE_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Get a Quote</div>
    <h1>Tell us about<br/><span class="accent">the load.</span></h1>
    <p>Quick form. Real human reads it. Dispatch will get back within one business day. Need it moving today? Call <a href="tel:8012607010" style="color:var(--red);font-weight:600;">801-260-7010</a>.</p>
  </div>
</section>

<section class="form-section">
  <div class="wrap">
    <div class="row">
      <div class="contact-info reveal">
        <div class="kicker">FOR SHIPPERS</div>
        <h2 style="margin-top:14px;">53' reefers.<br/><span style="color:var(--red);">48 states.</span></h2>
        <p class="lede">We haul food and food-grade freight only. From a single pallet to a full reefer, on a one-time tender or a committed weekly lane.</p>
        <div class="info-list" style="margin-top:32px;">
          <div class="item">
            <div class="label">CALL DISPATCH</div>
            <div class="value"><a href="tel:8012607010"><strong>801-260-7010</strong></a><br/><span style="font-size:13px;color:var(--mute);">24/7 — real human</span></div>
          </div>
          <div class="item">
            <div class="label">EMAIL</div>
            <div class="value"><a href="mailto:info@simonexpress.com">info@simonexpress.com</a></div>
          </div>
          <div class="item">
            <div class="label">EQUIPMENT</div>
            <div class="value">53' refrigerated trailers<br/><span style="font-size:13px;color:var(--mute);">−20°F to 70°F set-point</span></div>
          </div>
          <div class="item">
            <div class="label">RESPONSE</div>
            <div class="value">Within one business day<br/><span style="font-size:13px;color:var(--mute);">Faster if it's urgent — call</span></div>
          </div>
        </div>
      </div>

      <div class="form-card reveal">
        <h2>Get a freight quote.</h2>
        <p class="intro">All fields with * are required. The more detail you give us, the better we can rate the load.</p>
        <form data-simon-form="quote" novalidate>
          <div class="form-status" role="alert"></div>
          <div class="field-row">
            <div class="field"><label>Your Name <span class="required">*</span></label><input name="name" type="text" required autocomplete="name"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Company <span class="required">*</span></label><input name="company" type="text" required autocomplete="organization"/><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field"><label>Email <span class="required">*</span></label><input name="email" type="email" required autocomplete="email"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Phone <span class="required">*</span></label><input name="phone" type="tel" required autocomplete="tel"/><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field"><label>Pickup City / State <span class="required">*</span></label><input name="origin" type="text" required placeholder="e.g. Fresno, CA"/><div class="error-msg">Required</div></div>
            <div class="field"><label>Delivery City / State <span class="required">*</span></label><input name="destination" type="text" required placeholder="e.g. Dallas, TX"/><div class="error-msg">Required</div></div>
          </div>
          <div class="field-row">
            <div class="field">
              <label>Commodity</label>
              <select name="commodity"><option value="">Select…</option><option>Produce</option><option>Dairy</option><option>Protein / Meat</option><option>Frozen</option><option>Beverage</option><option>Other Food / CPG</option></select>
            </div>
            <div class="field">
              <label>Temperature</label>
              <select name="temperature"><option value="">Select…</option><option>Frozen (−20°F to 0°F)</option><option>Refrigerated (33°F to 40°F)</option><option>Cool (40°F to 55°F)</option><option>Ambient (55°F+)</option></select>
            </div>
          </div>
          <div class="field-row">
            <div class="field"><label>Pickup Date</label><input name="pickupDate" type="date"/></div>
            <div class="field">
              <label>Frequency</label>
              <select name="frequency"><option value="">Select…</option><option>One-time</option><option>Weekly</option><option>Multiple per week</option><option>Dedicated lane</option></select>
            </div>
          </div>
          <div class="field-row">
            <div class="field"><label>Pallets / Weight</label><input name="loadDetails" type="text" placeholder="e.g. 24 pallets, 38,000 lbs"/></div>
            <div class="field">
              <label>Equipment</label>
              <select name="equipment"><option value="">Select…</option><option>53' Reefer</option><option>53' Reefer with plate floor</option><option>Multi-temp dual-zone</option><option>Not sure</option></select>
            </div>
          </div>
          <div class="field"><label>Notes</label><textarea name="notes" placeholder="Special handling, appointment requirements, contacts at origin / destination…"></textarea></div>
          <button type="submit" class="btn btn-lg" style="width:100%;justify-content:center;">Send Quote Request {ARROW_SVG}</button>
        </form>
      </div>
    </div>
  </div>
</section>
'''

render(
    "quote.html",
    title="Get a Quote — Refrigerated Freight · Simon Express",
    description="Get a freight quote from Simon Express. National refrigerated trucking carrier with 53' reefer trailers serving all 48 states — one-time loads to dedicated lanes. Real humans on the phone — 801-260-7010.",
    canonical="quote.html",
    body=QUOTE_BODY,
)

# ============================================================
# 8.  TRACKING PAGE (Coming Soon)
# ============================================================
TRACKING_BODY = f'''
<section class="page-header">
  <div class="wrap reveal">
    <div class="crumbs"><a href="/">Home</a><span>/</span>Customer Tracking</div>
    <h1>Customer<br/><span class="accent">Tracking.</span></h1>
    <p>Live shipment tracking for Simon Express customers. Coming soon &mdash; in the meantime, dispatch can give you a real-time status on any active load by phone or email.</p>
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="wrap">
    <div style="max-width:760px;margin:0 auto;padding:80px 0;text-align:center;" class="reveal">
      <div class="kicker no-rule" style="justify-content:center;margin-bottom:24px;">COMING SOON</div>
      <h2 style="font-family:var(--display);font-weight:700;font-size:clamp(40px,5vw,68px);text-transform:uppercase;line-height:1.0;letter-spacing:-0.02em;margin-bottom:24px;">
        Self-serve tracking<br/><span style="color:var(--red);">is on the way.</span>
      </h2>
      <p style="font-size:18px;line-height:1.65;color:var(--mute);max-width:580px;margin:0 auto 40px;">
        We're building a customer portal so you can pull live load status, ETAs, and temperature logs without picking up the phone. Until it ships, dispatch is your portal &mdash; and they answer faster than any web app anyway.
      </p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:48px;">
        <a href="tel:8012607010" class="btn btn-xl">Call Dispatch · 801-260-7010 {ARROW_SVG}</a>
        <a href="mailto:info@simonexpress.com?subject=Shipment%20Status%20Request" class="btn btn-xl ghost">Email a Status Request</a>
      </div>
      <div style="border-top:1px solid var(--line);padding-top:32px;margin-top:16px;">
        <div class="kicker no-rule" style="justify-content:center;margin-bottom:14px;">WHAT YOU&apos;LL GET WHEN IT LAUNCHES</div>
        <div class="rule-grid cols-2" style="border-top:1px solid var(--line);">
          <div class="cell">
            <h3>Live Load Status</h3>
            <p>Real-time GPS position, current ETA, and delivery countdown for every active load on your account.</p>
          </div>
          <div class="cell">
            <h3>Temperature Logs</h3>
            <p>On-demand reefer set-point and actual-temperature charts, downloadable for your records and FSMA documentation.</p>
          </div>
          <div class="cell">
            <h3>Document Library</h3>
            <p>BOLs, PODs, weight tickets, and lumper receipts &mdash; all attached to the load, all available the moment they hit the driver&apos;s phone.</p>
          </div>
          <div class="cell">
            <h3>Multi-User Accounts</h3>
            <p>Add your team. Each user gets the right level of access &mdash; logistics, accounting, receiving &mdash; without a single shared password.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

render(
    "tracking.html",
    title="Customer Tracking — Coming Soon · Simon Express",
    description="Customer shipment tracking portal for Simon Express is coming soon. In the meantime, call dispatch at 801-260-7010 or email info@simonexpress.com for a real-time status on any active load.",
    canonical="tracking.html",
    body=TRACKING_BODY,
)

# ============================================================
# 9.  DRIVER LOGIN PAGE
# ============================================================
DRIVER_LOGIN_BODY = f'''
<section style="background:linear-gradient(180deg,#0F0F11 0%,#0B0B0C 100%);min-height:calc(100vh - 180px);display:flex;align-items:center;justify-content:center;padding:80px 20px;position:relative;overflow:hidden;">
  <div aria-hidden="true" style="position:absolute;inset:0;background:radial-gradient(circle at 25% 30%,rgba(215,25,32,0.18),transparent 55%),radial-gradient(circle at 80% 80%,rgba(215,25,32,0.10),transparent 55%);pointer-events:none;"></div>
  <div style="position:relative;z-index:1;width:100%;max-width:440px;">
    <div style="text-align:center;margin-bottom:32px;" class="reveal">
      <div class="kicker no-rule" style="color:var(--red);justify-content:center;margin-bottom:14px;">DRIVER PORTAL</div>
      <h1 style="font-family:var(--display);font-weight:700;font-size:clamp(36px,4vw,52px);text-transform:uppercase;line-height:1.0;letter-spacing:-0.02em;color:#fff;">
        Driver<br/><span style="color:var(--red);">Login.</span>
      </h1>
      <p style="font-size:15px;line-height:1.55;color:var(--mute-3);max-width:360px;margin:18px auto 0;">
        Sign in to access your loads, BOL submission, fuel cards, and HOS / ELD.
      </p>
    </div>
    <form class="form-card reveal" style="background:rgba(28,29,32,0.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.10);box-shadow:0 1px 0 rgba(255,255,255,0.08) inset,0 24px 56px rgba(0,0,0,0.5);" onsubmit="event.preventDefault();alert('Driver login authentication is being set up. For now, please contact dispatch at 801-260-7010 if you need help accessing the app.');return false;">
      <div class="field">
        <label style="color:#fff;">Driver Code <span class="required">*</span></label>
        <input type="text" name="driver_code" required autocomplete="username" placeholder="Your driver code" style="background:rgba(255,255,255,0.04);color:#fff;border-color:rgba(255,255,255,0.12);" />
      </div>
      <div class="field">
        <label style="color:#fff;">Password <span class="required">*</span></label>
        <input type="password" name="password" required autocomplete="current-password" placeholder="••••••••" style="background:rgba(255,255,255,0.04);color:#fff;border-color:rgba(255,255,255,0.12);" />
      </div>
      <button type="submit" class="btn btn-lg" style="width:100%;justify-content:center;margin-top:8px;">
        Sign In {ARROW_SVG}
      </button>
      <div style="margin-top:24px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.08);text-align:center;">
        <p style="font-size:13px;color:var(--mute-3);line-height:1.55;margin:0;">
          Trouble signing in? Call dispatch at <a href="tel:8012607010" style="color:var(--red);font-weight:600;text-decoration:none;">801-260-7010</a> &mdash; a real person will help.
        </p>
      </div>
    </form>
    <div style="text-align:center;margin-top:28px;" class="reveal">
      <a href="/" style="font-family:var(--mono);font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:var(--mute-2);text-decoration:none;">&larr; Back to simonexpress.com</a>
    </div>
  </div>
</section>
'''

render(
    "driver-login.html",
    title="Driver Login · Simon Express",
    description="Driver portal login for Simon Express drivers. Access your loads, BOL submission, fuel cards, and HOS / ELD in one place.",
    canonical="driver-login.html",
    body=DRIVER_LOGIN_BODY,
    noindex=True,
)

print("\nAll pages built.")
