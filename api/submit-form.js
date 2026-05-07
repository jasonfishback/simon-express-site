/**
 * /api/submit-form
 *
 * Receives JSON form submissions from quote / apply / contact forms
 * and emails them to info@simonexpress.com.
 *
 * --- Setup (in Vercel dashboard → Project → Settings → Environment Variables) ---
 *   RESEND_API_KEY   = re_xxxxxxxx  (get from https://resend.com — free tier covers a small business volume)
 *   FROM_EMAIL       = no-reply@simonexpress.com   (must be on a verified Resend domain)
 *   TO_EMAIL         = info@simonexpress.com       (where submissions land)
 *
 * If RESEND_API_KEY is not set, the function returns a 200 anyway and the
 * client falls back to opening the user's mail app (mailto:). That keeps
 * the site working from day one even before the email service is configured.
 */

export const config = { runtime: 'edge' };

const FORM_LABELS = {
  quote: 'Freight Quote Request',
  apply: 'Driver Application',
  contact: 'Website Contact',
};

const FIELD_ORDER = {
  quote: [
    'name', 'company', 'email', 'phone',
    'origin', 'destination',
    'commodity', 'temperature',
    'pickupDate', 'frequency',
    'loadDetails', 'equipment',
    'notes',
  ],
  apply: [
    'firstName', 'lastName', 'email', 'phone',
    'location', 'cdlA', 'yearsDriving', 'endorsements',
    'notes',
  ],
  contact: [
    'name', 'company', 'email', 'phone',
    'topic', 'message',
  ],
};

const FIELD_LABELS = {
  firstName: 'First Name',
  lastName: 'Last Name',
  cdlA: 'CDL-A',
  yearsDriving: 'Years Driving',
  pickupDate: 'Pickup Date',
  loadDetails: 'Pallets / Weight',
};

function humanLabel(key) {
  if (FIELD_LABELS[key]) return FIELD_LABELS[key];
  return key.replace(/([A-Z])/g, ' $1').replace(/^./, c => c.toUpperCase());
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function buildEmail(data) {
  const formType = data.formType || 'contact';
  const label = FORM_LABELS[formType] || 'Website Inquiry';
  const order = FIELD_ORDER[formType] || Object.keys(data);

  const seen = new Set();
  const fieldsHtml = [];
  const fieldsText = [];

  for (const key of order) {
    if (data[key] === undefined || data[key] === '' || data[key] == null) continue;
    seen.add(key);
    const labelText = humanLabel(key);
    const value = String(data[key]);
    fieldsHtml.push(
      `<tr><td style="padding:8px 16px 8px 0;color:#6B6F76;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;vertical-align:top;white-space:nowrap;">${escapeHtml(labelText)}</td>` +
      `<td style="padding:8px 0;color:#17181A;font-family:Inter,sans-serif;font-size:14px;line-height:1.5;">${escapeHtml(value).replace(/\n/g, '<br/>')}</td></tr>`
    );
    fieldsText.push(`${labelText}: ${value}`);
  }
  for (const key of Object.keys(data)) {
    if (seen.has(key)) continue;
    if (['formType', 'submittedAt', 'userAgent', 'pageUrl'].includes(key)) continue;
    if (data[key] === '' || data[key] == null) continue;
    fieldsHtml.push(
      `<tr><td style="padding:8px 16px 8px 0;color:#6B6F76;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;vertical-align:top;white-space:nowrap;">${escapeHtml(humanLabel(key))}</td>` +
      `<td style="padding:8px 0;color:#17181A;font-family:Inter,sans-serif;font-size:14px;line-height:1.5;">${escapeHtml(String(data[key])).replace(/\n/g, '<br/>')}</td></tr>`
    );
    fieldsText.push(`${humanLabel(key)}: ${data[key]}`);
  }

  const submittedAt = data.submittedAt || new Date().toISOString();
  const pageUrl = data.pageUrl || '';

  const html = `<!doctype html>
<html><body style="margin:0;padding:0;background:#FAFAF7;">
<table role="presentation" width="100%" style="background:#FAFAF7;padding:32px 16px;">
  <tr><td align="center">
    <table role="presentation" width="600" style="max-width:600px;background:#fff;border:1px solid #E6E7EA;">
      <tr><td style="background:#0B0B0C;padding:24px 32px;">
        <div style="font-family:'Oswald','Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:20px;letter-spacing:-0.01em;color:#fff;text-transform:uppercase;">SIMON EXPRESS</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.18em;color:#D71920;text-transform:uppercase;margin-top:6px;">— Website Submission</div>
      </td></tr>
      <tr><td style="padding:32px;">
        <h1 style="font-family:'Oswald','Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:28px;letter-spacing:-0.02em;color:#17181A;text-transform:uppercase;margin:0 0 24px;">${escapeHtml(label)}</h1>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
          ${fieldsHtml.join('')}
        </table>
      </td></tr>
      <tr><td style="border-top:1px solid #E6E7EA;padding:20px 32px;background:#FAFAF7;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.05em;color:#6B6F76;line-height:1.6;">
          Submitted: ${escapeHtml(submittedAt)}<br/>
          Page: ${escapeHtml(pageUrl)}
        </div>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;

  const text = [
    label,
    '='.repeat(label.length),
    '',
    ...fieldsText,
    '',
    `Submitted: ${submittedAt}`,
    `Page: ${pageUrl}`,
  ].join('\n');

  return { subject: `[Simon Express] ${label}`, html, text };
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let data;
  try {
    data = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Basic spam guard — reject obviously empty payloads.
  const meaningfulFields = Object.keys(data).filter(
    k => !['formType', 'submittedAt', 'userAgent', 'pageUrl'].includes(k)
         && data[k] && String(data[k]).trim() !== ''
  );
  if (meaningfulFields.length < 3) {
    return new Response(JSON.stringify({ error: 'Empty submission' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { subject, html, text } = buildEmail(data);
  const replyTo = data.email || undefined;

  const apiKey  = process.env.RESEND_API_KEY;
  const fromEmail = process.env.FROM_EMAIL || 'Simon Express <onboarding@resend.dev>';
  const toEmail   = process.env.TO_EMAIL   || 'info@simonexpress.com';

  if (!apiKey) {
    // No Resend configured. Log to function output and tell the client we got it
    // — the client also has a mailto: fallback so the user is never stranded.
    console.log('[submit-form] No RESEND_API_KEY configured. Submission:', { subject, text });
    return new Response(JSON.stringify({ ok: true, queued: true, note: 'Email service not configured; submission was logged.' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Send via Resend
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: fromEmail,
        to: [toEmail],
        subject,
        html,
        text,
        ...(replyTo ? { reply_to: replyTo } : {}),
      }),
    });

    if (!r.ok) {
      const detail = await r.text().catch(() => '');
      console.error('[submit-form] Resend error', r.status, detail);
      return new Response(JSON.stringify({ error: 'Email send failed' }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('[submit-form] Network error', err);
    return new Response(JSON.stringify({ error: 'Network error' }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
