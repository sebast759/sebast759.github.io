# Shepherd's Bush Airbnb: where to look at raising prices

Source: Booking.com snapshot of The Hoxton Shepherd's Bush, taken 7 Oct 2026 (2 adults, 1 room, 1 night).
This file identifies dates only. No Airbnb prices were changed.

## Read this first

* **The missing nights are not random.** All 12 fall between 29 Oct and 4 Dec, which is also the most expensive part of the series. That pattern fits pages that broke the parser (for example "only 1 room left" layouts) or sold out nights the parser did not recognise. The November results may therefore understate demand. Check the `error` column in `hoxton_all_rate_rows.csv` for those dates.
* **The hotel is priced for business travel.** Weekday medians: Tue £184 and Wed £179 are highest, Fri £134 and Sun £129 lowest. Spikes in the middle of the week mostly reflect corporate and conference demand (White City media campus, Olympia). Friday and Saturday spikes are the better signal for leisure guests, who are most Airbnb bookings.
* **Every date was scraped on the same day,** so lead time varies from 1 day to 6 months. Near dates are hard evidence. Dates after mid January are weak evidence until scraped again.
* **No promotions were detected on any night.** Booking.com usually shows some discount, so the promo parser may be missing them. Treat the promotion column as unverified.

## Tier 1: strongest signals

| Period | Evidence | Note |
|---|---|---|
| Mon 28 Dec to Sun 3 Jan | 7 night expensive run; Thu 31 Dec, Sat 2 Jan and Sun 3 Jan already sold out; Fri 1 Jan +34% | New Year. Sold out nights 3 months ahead are the clearest signal in the data. |
| Sat 10 Oct | £299, +108% vs Saturday median, +69% vs adjacent nights | 3 days out, so this is close to a real outcome rather than an asking price. Act now or skip. |
| Thu 8 Oct to Thu 15 Oct | 8 night run, mean +50% vs weekday medians | Short lead time; includes the 10 Oct spike. |

## Tier 2: weekend leisure demand

| Date | Price | vs weekday median | Note |
|---|---|---|---|
| Fri 27 and Sat 28 Nov | £204, £239 | +52%, +66% | Black Friday weekend; Westfield London is next door. |
| Sat 5 Dec | £249 | +73% | Jump of +79% vs adjacent nights; 4 Dec is missing. |
| Fri 11 and Sat 12 Dec | £199, £239 | +49%, +66% | Inside a 6 night run (7 to 12 Dec). Christmas party and shopping season. |
| Sat 17 Oct | £239 | +66% | Isolated spike (+60% vs adjacent nights), likely an event. |
| Sat 21 Nov, Sat 14 Nov | £209, £194 | +45%, +35% | Moderate. |

## Tier 3: midweek spikes, check for events before acting

| Period | Mean price | Note |
|---|---|---|
| Mon 2 Nov to Wed 4 Nov | £256 | 4 Nov £314 (+75%). Probably a conference or trade show. |
| Tue 17 Nov to Thu 19 Nov | £257 | 17 Nov £324, the highest observed price. |
| Mon 30 Nov to Thu 3 Dec | £244 to £284 | 2 Dec is missing; 3 Dec +90%. |

Midweek demand only matters for an Airbnb if it takes 1 or 2 night stays. If attendees of an Olympia exhibition are behind these spikes, they do book short term rentals. Check the Olympia London and Shepherd's Bush Empire calendars for these dates.

## Low priority

January to April is close to flat. Small runs on 19 to 20 Jan, 16 to 17 Mar and 6 to 7 Apr are weak: lead time is long, and Mar 16 to 17 is actually 1% below the weekday median. The 6 to 7 Apr run is at the end of the window, where the rolling median has less data.

## Next steps

1. Fix the 12 missing nights. Send one raw page, `raw/booking/2026-11-05.html`, and I will patch the parser.
2. Scrape again weekly until mid December. Dates where the price rises as the date approaches are the real demand.
3. Before changing a price, compare against Airbnb listings nearby. The Hoxton tells you when demand is high, not what your listing can charge.
