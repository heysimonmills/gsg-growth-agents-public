#!/usr/bin/env python3
"""
Helcim Inc. - Weekly Google Ads Performance Report
Runs every Monday, covers last 7 days vs prior 7 days + last 30 days.
"""

import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.ads.googleads.client import GoogleAdsClient

CUSTOMER_ID = "9954926882"
RECIPIENT_EMAIL = "simon@georgestgrowth.com"
SENDER_EMAIL = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]


def micros(m):
    return round(m / 1_000_000, 2)


def pct(n, d):
    if d == 0:
        return "N/A"
    return f"{((n - d) / d * 100):+.1f}%"


def fmt_pct(v):
    if v is None:
        return "N/A"
    try:
        return f"{float(v):.1%}"
    except Exception:
        return "N/A"


def get_date_ranges():
    today = datetime.utcnow().date()
    l7_end = today - timedelta(days=1)
    l7_start = today - timedelta(days=7)
    p7_end = today - timedelta(days=8)
    p7_start = today - timedelta(days=14)
    l30_start = today - timedelta(days=30)
    return (
        l7_start.strftime("%Y-%m-%d"), l7_end.strftime("%Y-%m-%d"),
        p7_start.strftime("%Y-%m-%d"), p7_end.strftime("%Y-%m-%d"),
        l30_start.strftime("%Y-%m-%d"), l7_end.strftime("%Y-%m-%d"),
    )


def fetch_account_summary(ga, cid, start, end):
    q = f"""
        SELECT
          metrics.impressions, metrics.clicks, metrics.cost_micros,
          metrics.conversions, metrics.cost_per_conversion
        FROM customer
        WHERE segments.date BETWEEN '{start}' AND '{end}'
    """
    rows = list(ga.search(customer_id=cid, query=q))
    if not rows:
        return None
    m = rows[0].metrics
    return {
        "impressions": m.impressions,
        "clicks": m.clicks,
        "cost": micros(m.cost_micros),
        "conversions": round(m.conversions, 1),
        "cpa": micros(m.cost_per_conversion),
    }


def fetch_campaign_data(ga, cid, start, end):
    q = f"""
        SELECT
          campaign.name, campaign.status, campaign.advertising_channel_type,
          campaign.bidding_strategy_type,
          campaign_budget.amount_micros,
          metrics.impressions, metrics.clicks, metrics.cost_micros,
          metrics.conversions, metrics.cost_per_conversion,
          metrics.search_impression_share,
          metrics.search_rank_lost_impression_share,
          metrics.search_budget_lost_impression_share
        FROM campaign
        WHERE campaign.status = 'ENABLED'
          AND segments.date BETWEEN '{start}' AND '{end}'
        ORDER BY metrics.cost_micros DESC
    """
    campaigns = []
    for row in ga.search(customer_id=cid, query=q):
        c = row.campaign
        m = row.metrics
        b = row.campaign_budget
        if m.impressions == 0:
            continue
        campaigns.append({
            "name": c.name,
            "type": c.advertising_channel_type.name,
            "bidding": c.bidding_strategy_type.name,
            "budget": micros(b.amount_micros),
            "impressions": m.impressions,
            "clicks": m.clicks,
            "cost": micros(m.cost_micros),
            "conversions": round(m.conversions, 1),
            "cpa": micros(m.cost_per_conversion),
            "is": m.search_impression_share,
            "is_lost_rank": m.search_rank_lost_impression_share,
            "is_lost_budget": m.search_budget_lost_impression_share,
        })
    return campaigns


def fetch_top_keywords(ga, cid, start, end):
    q = f"""
        SELECT
          campaign.name,
          ad_group_criterion.keyword.text,
          ad_group_criterion.keyword.match_type,
          ad_group_criterion.quality_info.quality_score,
          metrics.impressions, metrics.clicks, metrics.cost_micros,
          metrics.conversions, metrics.cost_per_conversion,
          metrics.search_impression_share,
          metrics.search_rank_lost_impression_share
        FROM keyword_view
        WHERE ad_group_criterion.status != 'REMOVED'
          AND segments.date BETWEEN '{start}' AND '{end}'
          AND metrics.impressions > 20
        ORDER BY metrics.cost_micros DESC
        LIMIT 15
    """
    keywords = []
    for row in ga.search(customer_id=cid, query=q):
        k = row.ad_group_criterion
        m = row.metrics
        keywords.append({
            "text": k.keyword.text,
            "match": k.keyword.match_type.name,
            "qs": k.quality_info.quality_score,
            "campaign": row.campaign.name,
            "impressions": m.impressions,
            "clicks": m.clicks,
            "cost": micros(m.cost_micros),
            "conversions": round(m.conversions, 1),
            "cpa": micros(m.cost_per_conversion),
            "is": m.search_impression_share,
            "is_lost_rank": m.search_rank_lost_impression_share,
        })
    return keywords


def generate_action_items(l7, p7, campaigns, keywords):
    actions = []

    if l7 and p7:
        cpa_change = (l7["cpa"] - p7["cpa"]) / p7["cpa"] * 100 if p7["cpa"] > 0 else 0
        conv_change = (l7["conversions"] - p7["conversions"]) / p7["conversions"] * 100 if p7["conversions"] > 0 else 0

        if cpa_change > 30:
            actions.append(f"🚨 CPA up {cpa_change:+.0f}% WoW (${p7['cpa']} → ${l7['cpa']}) — review bidding and conversion tracking.")
        if conv_change < -20:
            actions.append(f"🚨 Conversions down {conv_change:.0f}% WoW — check for campaign disruptions or tracking issues.")

    for c in campaigns:
        if c["is_lost_budget"] > 0.2 and c["conversions"] > 0:
            actions.append(f"⚠️ {c['name']}: {c['is_lost_budget']:.0%} IS Lost to Budget — campaign is being throttled (${c['budget']}/day).")
        if c["is_lost_rank"] > 0.7 and c["conversions"] > 0:
            actions.append(f"⚠️ {c['name']}: {c['is_lost_rank']:.0%} IS Lost to Rank — low QS or bids suppressing delivery.")
        if c["cpa"] > 1000 and c["conversions"] > 0:
            actions.append(f"⚠️ {c['name']}: CPA ${c['cpa']:,} — above $1,000 threshold, review bidding and keyword mix.")

    for kw in keywords:
        if kw["qs"] in (3, 4) and kw["cost"] > 100:
            actions.append(f"⚠️ Keyword \"{kw['text']}\" (QS {kw['qs']}) spent ${kw['cost']:,} — bid penalty active, review ad copy alignment.")
        if kw["conversions"] == 0 and kw["cost"] > 300:
            actions.append(f"⚠️ Keyword \"{kw['text']}\" spent ${kw['cost']:,} with 0 conversions — consider pausing or restructuring.")

    if not actions:
        actions.append("✅ No critical issues detected this week. Continue monitoring.")

    return actions


def build_html(l7, p7, l30, campaigns_l7, campaigns_l30, keywords_l7, actions, run_date):
    def wow_class(val, good_dir):
        try:
            v = float(val.replace("%", "").replace("+", ""))
            if good_dir == "up":
                return "good" if v > 0 else "bad" if v < -10 else "neutral"
            else:
                return "good" if v < 0 else "bad" if v > 10 else "neutral"
        except Exception:
            return "neutral"

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  body {{ font-family: Arial, sans-serif; font-size: 14px; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #0057b8; padding-bottom: 8px; }}
  h2 {{ color: #1a1a2e; margin-top: 30px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
  th {{ background: #1a1a2e; color: white; padding: 8px 10px; text-align: left; font-size: 13px; }}
  td {{ padding: 7px 10px; border-bottom: 1px solid #eee; font-size: 13px; }}
  tr:hover td {{ background: #f9f9f9; }}
  .good {{ color: #28a745; font-weight: bold; }}
  .bad {{ color: #dc3545; font-weight: bold; }}
  .neutral {{ color: #6c757d; }}
  .action-item {{ background: #fff8e1; border-left: 4px solid #ffc107; padding: 8px 12px; margin: 6px 0; border-radius: 2px; }}
  .metric-box {{ display: inline-block; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 12px 20px; margin: 6px; text-align: center; min-width: 140px; }}
  .metric-val {{ font-size: 22px; font-weight: bold; color: #1a1a2e; }}
  .metric-label {{ font-size: 11px; color: #6c757d; text-transform: uppercase; }}
  .metric-wow {{ font-size: 12px; margin-top: 4px; }}
</style>
</head>
<body>
<h1>📊 Helcim — Weekly Ads Report</h1>
<p style="color:#6c757d;">Week of {run_date} &nbsp;|&nbsp; Helcim Inc. (Account: 9954926882)</p>
"""

    if l7 and p7:
        html += "<h2>Account Overview — Last 7 Days vs Prior 7 Days</h2><div>"
        metrics = [
            ("Spend", f"${l7['cost']:,.0f}", pct(l7['cost'], p7['cost']), "up"),
            ("Clicks", f"{l7['clicks']:,}", pct(l7['clicks'], p7['clicks']), "up"),
            ("Conversions", f"{l7['conversions']}", pct(l7['conversions'], p7['conversions']), "up"),
            ("CPA", f"${l7['cpa']}", pct(l7['cpa'], p7['cpa']), "down"),
            ("Impressions", f"{l7['impressions']:,}", pct(l7['impressions'], p7['impressions']), "up"),
        ]
        for label, val, wow, good_dir in metrics:
            wc = wow_class(wow, good_dir)
            html += f"""
      <div class="metric-box">
        <div class="metric-val">{val}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-wow {wc}">{wow} WoW</div>
      </div>"""
        html += "</div>"

    html += "<h2>🎯 Action Items</h2>"
    for action in actions:
        html += f'<div class="action-item">{action}</div>'

    html += "<h2>Campaign Performance — Last 7 Days</h2>"
    html += "<table><tr><th>Campaign</th><th>Type</th><th>Cost</th><th>Conv</th><th>CPA</th><th>IS</th><th>IS Lost Rank</th><th>IS Lost Budget</th></tr>"
    for c in campaigns_l7:
        ilr_class = ' class="bad"' if c["is_lost_rank"] and c["is_lost_rank"] > 0.7 else ''
        ilb_class = ' class="bad"' if c["is_lost_budget"] and c["is_lost_budget"] > 0.2 else ''
        html += f"""<tr>
<td>{c['name']}</td><td>{c['type']}</td>
<td>${c['cost']:,}</td><td>{c['conversions']}</td><td>${c['cpa']}</td>
<td>{fmt_pct(c['is'])}</td><td{ilr_class}>{fmt_pct(c['is_lost_rank'])}</td><td{ilb_class}>{fmt_pct(c['is_lost_budget'])}</td>
</tr>"""
    html += "</table>"

    html += "<h2>Campaign Performance — Last 30 Days</h2>"
    html += "<table><tr><th>Campaign</th><th>Cost</th><th>Conv</th><th>CPA</th><th>IS</th><th>IS Lost Rank</th><th>Budget/Day</th></tr>"
    for c in campaigns_l30:
        ilr_class = ' class="bad"' if c["is_lost_rank"] and c["is_lost_rank"] > 0.7 else ''
        html += f"""<tr>
<td>{c['name']}</td>
<td>${c['cost']:,}</td><td>{c['conversions']}</td><td>${c['cpa']}</td>
<td>{fmt_pct(c['is'])}</td><td{ilr_class}>{fmt_pct(c['is_lost_rank'])}</td><td>${c['budget']}/day</td>
</tr>"""
    html += "</table>"

    html += "<h2>Top Keywords by Spend — Last 7 Days</h2>"
    html += "<table><tr><th>Keyword</th><th>Match</th><th>QS</th><th>Cost</th><th>Conv</th><th>CPA</th><th>IS</th><th>IS Lost Rank</th></tr>"
    for kw in keywords_l7:
        qs = kw["qs"] if kw["qs"] else "—"
        qs_class = ' class="bad"' if kw["qs"] and kw["qs"] <= 4 else ''
        html += f"""<tr>
<td>"{kw['text']}"</td><td>{kw['match']}</td><td{qs_class}>{qs}</td>
<td>${kw['cost']}</td><td>{kw['conversions']}</td><td>${kw['cpa']}</td>
<td>{fmt_pct(kw['is'])}</td><td>{fmt_pct(kw['is_lost_rank'])}</td>
</tr>"""
    html += "</table>"

    html += f"""
<hr style="margin-top:40px;border:none;border-top:1px solid #eee;">
<p style="color:#aaa;font-size:12px;">Generated by George St Growth automated reporting · {run_date}</p>
</body></html>"""

    return html


def send_email(html, run_date):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Helcim — Weekly Ads Report ({run_date})"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    print(f"Email sent to {RECIPIENT_EMAIL}")


def main():
    run_date = datetime.utcnow().strftime("%B %d, %Y")
    l7_start, l7_end, p7_start, p7_end, l30_start, l30_end = get_date_ranges()

    client = GoogleAdsClient.load_from_storage()
    ga = client.get_service("GoogleAdsService")

    print("Fetching account summary...")
    l7 = fetch_account_summary(ga, CUSTOMER_ID, l7_start, l7_end)
    p7 = fetch_account_summary(ga, CUSTOMER_ID, p7_start, p7_end)
    l30 = fetch_account_summary(ga, CUSTOMER_ID, l30_start, l30_end)

    print("Fetching campaign data...")
    campaigns_l7 = fetch_campaign_data(ga, CUSTOMER_ID, l7_start, l7_end)
    campaigns_l30 = fetch_campaign_data(ga, CUSTOMER_ID, l30_start, l30_end)

    print("Fetching keyword data...")
    keywords_l7 = fetch_top_keywords(ga, CUSTOMER_ID, l7_start, l7_end)

    print("Generating action items...")
    actions = generate_action_items(l7, p7, campaigns_l7, keywords_l7)

    print("Building report...")
    html = build_html(l7, p7, l30, campaigns_l7, campaigns_l30, keywords_l7, actions, run_date)

    print("Sending email...")
    send_email(html, run_date)
    print("Done.")


if __name__ == "__main__":
    main()
