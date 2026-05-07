#!/usr/bin/env python3
"""
Simon Express — page builder.
Reads index.html as the source of truth for shared partials,
and writes each subpage by composing: head + utility_bar + nav + page_body + footer + modals.

This script runs once at build time. Output is plain static HTML — no runtime dependency.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = (ROOT / "index.html").read_text()

# --- extract shared blocks from index.html ---
def extract(start_marker, end_marker):
    """Extract the block between <!-- ============= START ============= -->
    and the next <!-- ============= ... ============= --> marker."""
    pattern = re.compile(
        r'<!-- =+ ' + re.escape(start_marker) + r' =+ -->(.*?)(?=<!-- =+ )',
        re.DOTALL
    )
    m = pattern.search(INDEX)
    if not m:
        print(f"ERROR: could not extract {start_marker}")
        sys.exit(1)
    return m.group(0).rstrip()

UTILITY_BAR = extract("UTILITY BAR", "NAV")
NAV         = extract("NAV", "INTRO BAND")
FOOTER      = extract("FOOTER", "MODALS")
MODALS_RAW  = re.search(r'<!-- =+ MODALS =+ -->.*?(?=<script src="assets/site.js")', INDEX, re.DOTALL)
MODALS      = MODALS_RAW.group(0).rstrip() if MODALS_RAW else ""

# Canonical organization-level schema injected on every page so @id refs resolve.
# NATIONAL POSITIONING: lead with Organization, use MovingAndStorageCompany... NO —
# we are a national OTR refrigerated carrier. The right pattern is Organization
# (national identity) + LocalBusiness (Google Business Profile anchor only).
BASE_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.simonexpress.com/#org",
      "name": "Simon Express",
      "alternateName": ["Simon Express Trucking", "Simon Express Refrigerated"],
      "description": "National refrigerated trucking carrier serving 48 states. Simon Express operates a fleet of 53-foot temperature-controlled reefer trailers hauling food-grade freight \u2014 produce, dairy, protein, frozen, and beverage \u2014 over the road for shippers nationwide. Run by four generations of the Simon family on the floor, with over 50 years of refrigerated transportation experience.",
      "url": "https://www.simonexpress.com/",
      "logo": "https://www.simonexpress.com/assets/simon-logo-cropped.png",
      "image": "https://www.simonexpress.com/assets/truck-arch.jpg",
      "email": "info@simonexpress.com",
      "telephone": "+1-801-260-7010",
      "areaServed": [
        { "@type": "Country", "name": "United States" },
        { "@type": "AdministrativeArea", "name": "Continental United States (48 states)" }
      ],
      "award": [
        "Nominated for Best Fleets to Drive For 2026 (CarriersEdge)",
        "Nominated for Best Fleets to Drive For 2025 (CarriersEdge)",
        "Nominated for Best Fleets to Drive For 2024 (CarriersEdge)",
        "Nominated for Best Fleets to Drive For 2023 (CarriersEdge)",
        "Nominated for Best Fleets to Drive For 2022 (CarriersEdge)"
      ],
      "knowsAbout": [
        "Refrigerated Trucking",
        "Reefer Freight",
        "Temperature-Controlled Trucking",
        "Cold Chain Logistics",
        "Food Grade Transportation",
        "Produce Hauling",
        "Frozen Freight",
        "Dairy Transportation",
        "Protein Transportation",
        "Beverage Hauling",
        "Full Truckload (FTL)",
        "Dedicated Lanes",
        "53-foot Reefer Trailers",
        "Over-the-Road (OTR) Trucking",
        "Nationwide Refrigerated Freight",
        "Interstate Trucking"
      ],
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "telephone": "+1-801-260-7010",
          "contactType": "dispatch",
          "areaServed": "US",
          "availableLanguage": ["English", "Spanish"],
          "hoursAvailable": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "00:00",
            "closes": "23:59"
          }
        },
        {
          "@type": "ContactPoint",
          "telephone": "+1-801-260-7010",
          "contactType": "customer service",
          "areaServed": "US",
          "availableLanguage": ["English", "Spanish"]
        },
        {
          "@type": "ContactPoint",
          "telephone": "+1-801-260-7010",
          "contactType": "recruiting",
          "areaServed": "US",
          "availableLanguage": ["English", "Spanish"]
        }
      ]
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.simonexpress.com/#business",
      "name": "Simon Express",
      "parentOrganization": { "@id": "https://www.simonexpress.com/#org" },
      "description": "Headquarters of Simon Express, a national refrigerated trucking carrier serving 48 states.",
      "url": "https://www.simonexpress.com/",
      "logo": "https://www.simonexpress.com/assets/simon-logo-cropped.png",
      "image": "https://www.simonexpress.com/assets/truck-arch.jpg",
      "telephone": "+1-801-260-7010",
      "email": "info@simonexpress.com",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Salt Lake City",
        "addressRegion": "UT",
        "addressCountry": "US"
      },
      "areaServed": [
        { "@type": "Country", "name": "United States" },
        { "@type": "AdministrativeArea", "name": "Continental United States (48 states)" }
      ],
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00",
        "closes": "23:59",
        "description": "24/7 dispatch"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.simonexpress.com/#website",
      "url": "https://www.simonexpress.com/",
      "name": "Simon Express",
      "publisher": { "@id": "https://www.simonexpress.com/#org" }
    }
  ]
}
</script>
'''

# --- shared head template ---
HEAD_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="https://www.simonexpress.com/{canonical}" />
{robots_meta}
<meta property="og:type" content="website" />
<meta property="og:title" content="{og_title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="https://www.simonexpress.com/{canonical}" />
<meta property="og:site_name" content="Simon Express" />
<meta property="og:image" content="https://www.simonexpress.com/assets/truck-arch.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{og_title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="https://www.simonexpress.com/assets/truck-arch.jpg" />

<meta name="theme-color" content="#0B0B0C" />
<link rel="icon" type="image/png" href="assets/favicon.png" />
<link rel="apple-touch-icon" href="assets/favicon.png" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

<link rel="stylesheet" href="assets/site.css" />
{extra_schema}
</head>
<body>
'''

PAGE_FOOT = '''
{footer}

{modals}

<style>.hide-sm{{}} @media (max-width:820px){{.hide-sm{{display:none !important;}} .utility-bar .wrap{{padding-top:8px;padding-bottom:8px;font-size:11px;}} .utility-bar .left{{gap:14px;}}}}</style>

<script src="assets/site.js" defer></script>
</body>
</html>
'''

def render(out_filename, title, description, canonical, body, extra_schema="", og_title=None, noindex=False):
    head = HEAD_TEMPLATE.format(
        title=title,
        description=description,
        canonical=canonical,
        og_title=og_title or title,
        extra_schema=BASE_SCHEMA + extra_schema,
        robots_meta='<meta name="robots" content="noindex, nofollow" />\n' if noindex else '',
    )
    foot = PAGE_FOOT.format(footer=FOOTER, modals=MODALS)
    html = head + UTILITY_BAR + "\n\n" + NAV + "\n\n" + body + "\n\n" + foot
    (ROOT / out_filename).write_text(html)
    print(f"  wrote {out_filename}  ({len(html):,} bytes)")

# Pages will be filled by the rest of the build pipeline (rendered separately).
if __name__ == "__main__":
    print("Helpers loaded. import and call render() per page.")
