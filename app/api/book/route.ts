// POST /api/book — the booking form's details (the modal and the homepage form in public/js/birdline.js).
//
// Checks the fields, then emails them to the team through Resend (https://resend.com) and writes them to the function log
// (Vercel → project → Logs) as a backup. Environment variables:
//   RESEND_API_KEY     from resend.com (or the Resend integration in the Vercel Marketplace). Without it the lead is only logged.
//   BOOK_NOTIFY_TO     who gets the email; several addresses separated by commas. Default: mike@birdlinestudios.com
//   BOOK_NOTIFY_FROM   the sender. Default: "Birdline Website <onboarding@resend.dev>", which Resend allows before a domain is
//                      verified (it then only delivers to the Resend account's own address). After verifying birdlinestudios.com
//                      in Resend, set e.g. "Birdline Website <website@birdlinestudios.com>".
// The visitor always goes on to the calendar whatever happens here: Calendly sends its own booking email too.
import { NextResponse } from "next/server";

export const runtime = "nodejs";

const PERSONAL = /^(gmail|googlemail|yahoo|ymail|rocketmail|hotmail|outlook|live|msn|icloud|me|mac|aol|protonmail|proton|pm|gmx|mail|zoho|yandex|fastmail|hey|duck|comcast|att|verizon|sbcglobal|cox|qq|163|126)\./i;
const SIZES = new Set(["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]);

type Lead = { name: string; email: string; company: string; size: string; source: string; page: string; referrer: string };

const text = (v: unknown, max: number) => (typeof v === "string" ? v.trim().replace(/\s+/g, " ").slice(0, max) : "");
const domainOf = (email: string) => (/^[^\s@]+@([^\s@]+\.[^\s@]+)$/.exec(email)?.[1] || "").toLowerCase();
const escapeHtml = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c] as string);

export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = (await req.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ ok: false, error: "Send the form as JSON." }, { status: 400 });
  }

  // the honeypot: a filled "website" field is a bot, and it gets a quiet yes
  if (text(body.website, 200)) return NextResponse.json({ ok: true, emailed: false });

  const lead: Lead = {
    name: text(body.name, 120),
    email: text(body.email, 200).toLowerCase(),
    company: text(body.company, 120),
    size: text(body.size, 20),
    source: text(body.source, 200),
    page: text(body.page, 200),
    referrer: text(body.referrer, 300),
  };
  const domain = domainOf(lead.email);
  if (!lead.name) return NextResponse.json({ ok: false, error: "Add your full name." }, { status: 400 });
  if (!domain) return NextResponse.json({ ok: false, error: "That email address doesn’t look complete." }, { status: 400 });
  if (PERSONAL.test(domain)) return NextResponse.json({ ok: false, error: "Please use your company email. Personal email providers aren’t accepted." }, { status: 400 });
  if (!lead.company) return NextResponse.json({ ok: false, error: "Add your company name." }, { status: 400 });
  if (!lead.size || !SIZES.has(lead.size)) return NextResponse.json({ ok: false, error: "Choose your company size." }, { status: 400 });

  const when = new Date().toISOString();
  console.log("[book] lead", JSON.stringify({ ...lead, at: when }));

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.warn("[book] RESEND_API_KEY is not set: the lead above was logged but not emailed");
    return NextResponse.json({ ok: true, emailed: false });
  }

  const to = (process.env.BOOK_NOTIFY_TO || "mike@birdlinestudios.com").split(",").map((s) => s.trim()).filter(Boolean);
  const from = process.env.BOOK_NOTIFY_FROM || "Birdline Website <onboarding@resend.dev>";
  const rows: [string, string][] = [
    ["Name", lead.name],
    ["Work email", lead.email],
    ["Company", lead.company || "—"],
    ["Company size", lead.size || "—"],
    ["How they heard about Birdline", lead.source || "—"],
    ["Page", lead.page || "—"],
    ["Came from", lead.referrer || "—"],
    ["Submitted", when],
  ];
  const subject = `Call request: ${lead.name}${lead.company ? ` · ${lead.company}` : ` · ${domain}`}`;
  const plain = `${lead.name} asked to book a call through birdlinestudios.com.\n\n` + rows.map(([k, v]) => `${k}: ${v}`).join("\n") +
    `\n\nThey were sent on to Calendly to pick a time; reply to this email to reach them directly.`;
  const html = `<div style="font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#0b1220">
<p><strong>${escapeHtml(lead.name)}</strong> asked to book a call through birdlinestudios.com.</p>
<table cellpadding="6" style="border-collapse:collapse">${rows
    .map(([k, v]) => `<tr><td style="color:#5f6982;padding-right:16px;white-space:nowrap">${escapeHtml(k)}</td><td>${escapeHtml(v)}</td></tr>`)
    .join("")}</table>
<p style="color:#5f6982">They were sent on to Calendly to pick a time. Reply to this email to reach them directly.</p></div>`;

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from, to, subject, text: plain, html, reply_to: lead.email }),
    });
    if (!res.ok) {
      console.error("[book] Resend refused the email", res.status, (await res.text()).slice(0, 500));
      return NextResponse.json({ ok: true, emailed: false });
    }
    return NextResponse.json({ ok: true, emailed: true });
  } catch (err) {
    console.error("[book] could not reach Resend", err);
    return NextResponse.json({ ok: true, emailed: false });
  }
}
