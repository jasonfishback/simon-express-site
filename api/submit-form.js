// api/submit-form.js
// Vercel serverless function — handles all three forms (Quote, Driver App, Contact)
// with layered bot defense and submission logging.
//
// Layers:
//   1. Honeypot field rejection (hidden `website` field — humans don't fill it)
//   2. Minimum form fill time (humans take >2s; bots submit instantly)
//   3. Content sanity checks (gibberish detection, Gmail dot-normalization,
//      blocklist of normalized emails)
//   4. IP rate limiting (max 3 submissions per IP per hour, in-memory)
//   5. Structured logging (every attempt logged with IP, UA, decision)
//
// Legitimate users see no change — all defenses are invisible.

const { Resend } = require('resend');

const resend = new Resend(process.env.RESEND_API_KEY);

// In-memory rate limit store. Vercel serverless instances persist for minutes
// at a time, so this catches the burst-spam case. For longer-term tracking, an
// upstash/redis kv store would be the next step; this is intentionally simple.
const rateLimitStore = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000; // 1 hour
const RATE_LIMIT_MAX = 3;                    // 3 submissions per IP per hour

// Persistent blocklist of normalized Gmail addresses (and other emails) seen
// abusing the forms. Add new ones here as they appear in the logs.
const EMAIL_BLOCKLIST = new Set([
  'elikapaqi35@gmail.com',
]);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getClientIp(req) {
  // Vercel sets x-forwarded-for; take the first IP (the real client)
  const xff = req.headers['x-forwarded-for'];
  if (xff) return xff.split(',')[0].trim();
  return req.headers['x-real-ip'] || req.socket?.remoteAddress || 'unknown';
}

function normalizeEmail(email) {
  if (!email || typeof email !== 'string') return '';
  const lower = email.trim().toLowerCase();
  const [local, domain] = lower.split('@');
  if (!domain) return lower;
  // For Gmail/Googlemail, strip dots and +suffix — these all route to the same inbox
  if (domain === 'gmail.com' || domain === 'googlemail.com') {
    const stripped = local.replace(/\./g, '').split('+')[0];
    return `${stripped}@gmail.com`;
  }
  return lower;
}

// Detect random/gibberish strings — long runs of consonants, no vowels, or
// mixed-case alphanumeric with no spaces. Tuned not to false-positive on
// real names, company names, or city names.
function looksLikeGibberish(value) {
  if (!value || typeof value !== 'string') return false;
  const v = value.trim();
  if (v.length < 8) return false;          // too short to judge

  // No spaces AND length >= 10 AND mixed case AND has digits → very bot-like
  // (real names rarely have digits; real company names rarely lack spaces at length 10+)
  if (v.length >= 10 && !/\s/.test(v) && /[A-Z]/.test(v) && /[a-z]/.test(v) && /[A-Z].*[a-z].*[A-Z]|[a-z].*[A-Z].*[a-z]/.test(v)) {
    // alternating-case pattern like "tKRQDXoHAcEieCHr"
    return true;
  }

  // 6+ consecutive consonants — almost never happens in real English/Spanish words
  if (/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{6,}/.test(v)) {
    return true;
  }

  // Length >= 10 with literally zero vowels (a/e/i/o/u) — gibberish
  if (v.length >= 10 && !/[aeiouAEIOU]/.test(v)) {
    return true;
  }

  return false;
}

// Phone number gibberish detection — sequential keypad patterns, all-same-digit
function looksLikeFakePhone(phone) {
  if (!phone) return false;
  const digits = String(phone).replace(/\D/g, '');
  if (digits.length < 10) return true;     // too short to be a real US phone
  // All same digit
  if (/^(\d)\1+$/.test(digits)) return true;
  // Strictly sequential ascending or descending (1234567890, 0987654321, etc.)
  if (digits === '1234567890' || digits === '0123456789' || digits === '0987654321') return true;
  return false;
}

function rateLimitCheck(ip) {
  const now = Date.now();
  const record = rateLimitStore.get(ip) || { count: 0, windowStart: now };

  // Reset window if expired
  if (now - record.windowStart > RATE_LIMIT_WINDOW_MS) {
    record.count = 0;
    record.windowStart = now;
  }

  record.count += 1;
  rateLimitStore.set(ip, record);

  // Opportunistic cleanup — purge expired entries (cap memory growth)
  if (rateLimitStore.size > 1000) {
    for (const [key, val] of rateLimitStore.entries()) {
      if (now - val.windowStart > RATE_LIMIT_WINDOW_MS) {
        rateLimitStore.delete(key);
      }
    }
  }

  return {
    allowed: record.count <= RATE_LIMIT_MAX,
    count: record.count,
  };
}

function logAttempt({ verdict, reason, formType, ip, userAgent, email, normalizedEmail, body }) {
  // Vercel captures stdout into the function log — viewable at
  // vercel.com → Project → Logs. Keep this single-line JSON for easy grep.
  const entry = {
    ts: new Date().toISOString(),
    verdict,        // 'accepted' | 'blocked'
    reason,         // human-readable reason if blocked
    formType,
    ip,
    userAgent: userAgent?.slice(0, 200),
    email: email?.slice(0, 100),
    normalizedEmail,
    // truncated body preview for forensics — DO NOT log full submissions of
    // legit users in production unless you've added a privacy notice. Bot
    // bodies are fine to log in full because they have no PII.
    bodyPreview: verdict === 'blocked' ? JSON.stringify(body).slice(0, 500) : undefined,
  };
  console.log('[FORM_SUBMIT]', JSON.stringify(entry));
}

// ---------------------------------------------------------------------------
// Handler
// ---------------------------------------------------------------------------

module.exports = async (req, res) => {
  // CORS — only allow same-origin POST. Browsers won't send Origin for same-origin
  // navigations, but they DO for fetch/XHR, so we check when present.
  const origin = req.headers.origin;
  const allowedOrigins = [
    'https://simonexpress.com',
    'https://www.simonexpress.com',
  ];
  if (origin && !allowedOrigins.includes(origin)) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const ip = getClientIp(req);
  const userAgent = req.headers['user-agent'] || '';
  const body = req.body || {};
  const formType = body.formType || 'unknown';

  // -------------------------------------------------------------------------
  // LAYER 1: Honeypot field
  // -------------------------------------------------------------------------
  // The form has a hidden <input name="website"> that real users never see
  // and never fill. Bots fill every field they find.
  if (body.website && body.website.trim() !== '') {
    logAttempt({
      verdict: 'blocked',
      reason: 'honeypot_filled',
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail: normalizeEmail(body.email),
      body,
    });
    // Return 200 so the bot thinks it worked and stops retrying
    return res.status(200).json({ ok: true });
  }

  // -------------------------------------------------------------------------
  // LAYER 2: Minimum form fill time
  // -------------------------------------------------------------------------
  // The form embeds a hidden timestamp when the page loads. If the submission
  // arrives less than 2 seconds later, it's a bot.
  const renderedAt = parseInt(body._t, 10);
  if (renderedAt && Number.isFinite(renderedAt)) {
    const elapsed = Date.now() - renderedAt;
    if (elapsed < 2000) {
      logAttempt({
        verdict: 'blocked',
        reason: `too_fast_${elapsed}ms`,
        formType, ip, userAgent,
        email: body.email,
        normalizedEmail: normalizeEmail(body.email),
        body,
      });
      return res.status(200).json({ ok: true });
    }
  }

  // -------------------------------------------------------------------------
  // LAYER 3: Content sanity checks
  // -------------------------------------------------------------------------
  const normalizedEmail = normalizeEmail(body.email);

  // 3a. Email blocklist (covers the elikapaqi35 case and any future additions)
  if (EMAIL_BLOCKLIST.has(normalizedEmail)) {
    logAttempt({
      verdict: 'blocked',
      reason: 'email_blocklisted',
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body,
    });
    return res.status(200).json({ ok: true });
  }

  // 3b. Gibberish detection on the most-abused free-text fields
  const fieldsToCheck = [
    body.name, body.firstName, body.lastName, body.company,
    body.origin, body.destination, body.location, body.notes,
  ].filter(Boolean);

  const gibberishHits = fieldsToCheck.filter(looksLikeGibberish).length;
  if (gibberishHits >= 2) {
    logAttempt({
      verdict: 'blocked',
      reason: `gibberish_${gibberishHits}_fields`,
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body,
    });
    return res.status(200).json({ ok: true });
  }

  // 3c. Phone sanity
  if (body.phone && looksLikeFakePhone(body.phone)) {
    logAttempt({
      verdict: 'blocked',
      reason: 'fake_phone',
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body,
    });
    return res.status(200).json({ ok: true });
  }

  // 3d. Required fields by form type
  if (!body.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(body.email)) {
    logAttempt({
      verdict: 'blocked',
      reason: 'invalid_email',
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body,
    });
    return res.status(400).json({ error: 'Invalid email' });
  }

  // -------------------------------------------------------------------------
  // LAYER 4: IP rate limiting
  // -------------------------------------------------------------------------
  const rl = rateLimitCheck(ip);
  if (!rl.allowed) {
    logAttempt({
      verdict: 'blocked',
      reason: `rate_limit_${rl.count}`,
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body,
    });
    return res.status(429).json({ error: 'Too many submissions' });
  }

  // -------------------------------------------------------------------------
  // LAYER 5: Accept and send
  // -------------------------------------------------------------------------
  try {
    const emailHtml = buildEmailHtml(formType, body);
    const emailSubject = buildEmailSubject(formType, body);

    await resend.emails.send({
      from: process.env.FROM_EMAIL || 'forms@simonexpress.com',
      to: process.env.TO_EMAIL || 'info@simonexpress.com',
      replyTo: body.email,
      subject: emailSubject,
      html: emailHtml,
    });

    logAttempt({
      verdict: 'accepted',
      reason: 'ok',
      formType, ip, userAgent,
      email: body.email,
      normalizedEmail,
      body: {}, // don't log legit body content
    });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[FORM_SUBMIT] resend_error', err.message);
    return res.status(500).json({ error: 'Send failed' });
  }
};

// ---------------------------------------------------------------------------
// Email templates — keep your existing styling (WEBSITE SUBMISSION header,
// red bar, label/value rows, Submitted timestamp + Page footer)
// ---------------------------------------------------------------------------

function buildEmailSubject(formType, body) {
  switch (formType) {
    case 'quote':       return `Freight Quote Request — ${body.company || body.name || 'Unknown'}`;
    case 'apply':       return `Driver Application — ${body.firstName || ''} ${body.lastName || ''}`.trim();
    case 'contact':     return `Website Contact — ${body.name || 'Unknown'}`;
    default:            return `Simon Express — Website Submission`;
  }
}

function row(label, value) {
  if (!value) return '';
  const safeValue = String(value).replace(/[<>]/g, c => c === '<' ? '&lt;' : '&gt;');
  return `
    <tr>
      <td style="padding:8px 16px;font-family:'Courier New',monospace;font-size:11px;letter-spacing:0.15em;color:#666;text-transform:uppercase;vertical-align:top;width:140px;">${label}</td>
      <td style="padding:8px 16px;font-family:Arial,sans-serif;font-size:14px;color:#222;">${safeValue}</td>
    </tr>`;
}

function buildEmailHtml(formType, body) {
  const title = {
    quote: 'FREIGHT QUOTE REQUEST',
    apply: 'DRIVER APPLICATION',
    contact: 'CONTACT MESSAGE',
  }[formType] || 'WEBSITE SUBMISSION';

  let rows = '';
  if (formType === 'quote') {
    rows =
      row('Name', body.name) +
      row('Company', body.company) +
      row('Email', body.email) +
      row('Phone', body.phone) +
      row('Origin', body.origin) +
      row('Destination', body.destination) +
      row('Commodity', body.commodity) +
      row('Temperature', body.temperature) +
      row('Notes', body.notes);
  } else if (formType === 'apply') {
    rows =
      row('First Name', body.firstName) +
      row('Last Name', body.lastName) +
      row('Email', body.email) +
      row('Phone', body.phone) +
      row('Location', body.location) +
      row('CDL-A', body.cdla) +
      row('Years Driving', body.yearsDriving) +
      row('Notes', body.notes);
  } else {
    rows =
      row('Name', body.name) +
      row('Email', body.email) +
      row('Phone', body.phone) +
      row('Message', body.message || body.notes);
  }

  return `
    <div style="background:#f4f4f4;padding:24px;font-family:Arial,sans-serif;">
      <div style="max-width:640px;margin:0 auto;background:#fff;border:1px solid #e5e5e5;">
        <div style="background:#111;padding:18px 24px;">
          <div style="color:#fff;font-family:'Oswald',Arial,sans-serif;font-size:15px;letter-spacing:0.18em;font-weight:600;">SIMON EXPRESS</div>
          <div style="color:#D71920;font-family:'Courier New',monospace;font-size:11px;letter-spacing:0.18em;margin-top:4px;">— WEBSITE SUBMISSION</div>
        </div>
        <div style="padding:28px 24px 8px 24px;">
          <div style="font-family:'Oswald',Arial,sans-serif;font-size:22px;letter-spacing:0.06em;font-weight:700;color:#111;">${title}</div>
        </div>
        <table style="width:100%;border-collapse:collapse;padding:0 8px;">${rows}</table>
        <div style="background:#fafafa;border-top:1px solid #eee;padding:14px 24px;font-family:'Courier New',monospace;font-size:11px;color:#666;">
          Submitted: ${new Date().toISOString()}<br>
          Page: <a href="https://www.simonexpress.com/" style="color:#D71920;">https://www.simonexpress.com/</a>
        </div>
      </div>
    </div>
  `;
}
