# Dashboard Expert Audit Report

Project reviewed: Coffee Shop Sales & Customer Behavior Intelligence Dashboard  
Technology stack: Streamlit, Pandas, Plotly  
Review role: Senior Data Analyst, BI Consultant, Dashboard UX Reviewer, Hiring Manager  
Review date: 17 June 2026

## A. Overall Verdict

This dashboard is stronger than a basic student demo. It has a polished Streamlit layout, clear KPI cards, business-oriented tab names, dynamic filters, product analysis, demand analysis, operational recommendations, and a Data QA/export section. It looks portfolio-ready for LinkedIn and internship submission after some cleanup.

However, it is not fully MNC/client-ready yet. It currently feels like a polished portfolio dashboard rather than a production business intelligence product. The visual design is impressive for Streamlit, but the analytics are still mostly descriptive. The recommendations are directionally useful but generic, and the dashboard does not yet quantify business impact, variance, growth, targets, profitability, or action priority.

| Area | Rating / 10 | Expert View |
|---|---:|---|
| Business value | 7.0 | Good operational use case, but decisions need stronger quantification. |
| Visual design | 7.5 | Modern and professional for Streamlit, but sidebar and chart density need refinement. |
| Analytics depth | 6.0 | Solid descriptive analytics; limited diagnostic and predictive depth. |
| Storytelling | 6.5 | Good section naming, but the narrative is not yet problem-to-insight-to-action. |
| Technical quality | 7.0 | Clean data preparation and dynamic filtering, with some validation and robustness gaps. |
| Interview/LinkedIn impact | 7.5 | Strong enough to attract attention, but needs sharper business story and screenshots. |

Final verdict: portfolio-ready with caveats; client-ready only after Priority 1 fixes.

## B. Business Problem Clarity

The project explains that it supports revenue tracking, product intelligence, customer demand behavior, staffing, inventory, and recommendations. That gives the viewer a reasonable sense of purpose.

What works:

- The dashboard title and hero communicate the business area clearly.
- The executive KPI section gives immediate performance context.
- The tabs map to common client questions: revenue, products, demand, operations, actions, and data quality.
- The recommended action cards make the dashboard feel more decision-oriented than a normal chart gallery.

What is still weak:

- The client problem is broad: "coffee shop sales and customer behavior" rather than a specific business challenge such as declining sales, store optimization, staffing inefficiency, SKU rationalization, or category growth.
- The dashboard does not define the target user clearly. It could be for a store manager, regional manager, analyst, or executive, but each would need different depth.
- There is no baseline, target, or performance benchmark. A client cannot easily tell whether $698.81K revenue is good, bad, above target, or below target.
- Recommended actions are not ranked by impact, urgency, or confidence.
- The dashboard explains what happened, but not enough of why it happened or what exact financial outcome action could produce.

Decision clarity score: medium. A non-technical client can understand the dashboard, but a business leader would still ask, "What should I do first, and how much will it matter?"

## C. KPI Review

| KPI | Useful? | Placement | Label clarity | Expert review |
|---|---|---|---|---|
| Total Revenue | Yes | Strong | Clear | The most important headline metric. It should include MoM change and date range context. |
| Transactions | Yes | Strong | Clear | Useful volume metric. Since transaction_id is unique per row in the default data, this is effectively row count; the dashboard should clarify this. |
| AOV | Yes | Strong | Clear | Good commercial KPI. Current value rounds to $5, which is too coarse; use one or two decimals. |
| Items Sold | Yes | Strong | Clear | Useful for demand planning. Good note showing items/order. |
| Products Sold | Somewhat | Acceptable | Slightly unclear | "Products Sold" means distinct product IDs, not total units. Rename to "Distinct Products" to avoid misinterpretation. |
| Best Store | Yes | Strong | Clear | Useful, but needs revenue share and gap versus other stores. Hell's Kitchen is only slightly ahead of Astoria and Lower Manhattan. |
| Top Category | Yes | Strong | Clear | Good for category focus. Needs revenue share and change over time. |
| Peak Hour | Yes | Strong | Clear | Useful for staffing, but should become a peak demand window, not a single hour. |

Missing KPIs:

- Revenue per store
- Store contribution percentage
- Average items per transaction
- Revenue share by category
- Month-over-month revenue change
- Month-over-month transaction change
- Best store revenue gap versus second store
- Peak demand window, such as 8:00-11:00
- Low-demand opportunity window
- Top category contribution percentage
- Product concentration, such as top 10 SKU revenue share
- Revenue per operating hour
- Average unit price
- Basket size trend
- Refunds/discounts/margins if available

Highest priority KPI improvement: add MoM change and revenue share percentages. Without those, the executive section gives numbers but not performance interpretation.

## D. Dashboard Structure Review

Current tabs:

- Boardroom Overview
- Product Intelligence
- Customer Demand
- Operations
- Executive Actions
- Data QA

The flow is mostly logical. It starts with executive context, then moves into product, customer demand, operations, recommendations, and QA. This is better than a random chart collection.

Recommended structural changes:

- Merge "Executive Actions" into the top executive area or make it the final section of "Boardroom Overview." Executives should not need a separate tab to find recommendations.
- Rename "Customer Demand" to "Demand Patterns" or "Customer Demand Patterns." The current tab is fine, but "behavior" implies customer-level or segment-level analytics that the data does not contain.
- Rename "Operations" to "Staffing & Operations" because most insights are staffing and workload related.
- Keep "Data QA" as a separate tab, but make it more compact and more audit-oriented.
- Consider reducing the story to four decision tabs: Executive Overview, Product & Category Mix, Demand & Staffing, Data QA.

Storytelling assessment:

- Current story: performance summary to charts to broad recommendations.
- Stronger story needed: business problem to revenue trend to store/category drivers to demand constraint to prioritized actions.

The dashboard is close to a professional flow, but it still feels like sections assembled around available charts rather than a tightly argued client narrative.

## E. Visual Design / UI UX Review

What looks strong:

- The hero section is visually polished and gives a boardroom-style first impression.
- KPI cards are modern, readable, and aligned well on desktop.
- The dark sidebar contrasts nicely with the light dashboard canvas.
- Plotly charts are clean and use mostly appropriate chart types.
- The app feels more professional than a default Streamlit dashboard.

Specific UI flaws:

- The browser tab title remains generic as "Streamlit." For portfolio/client use, it should reflect the dashboard name.
- The sidebar filter area is too tall because every selected product/category/type is displayed as a chip. On a laptop viewport, this consumes a lot of space and makes filtering feel heavy.
- The upload control in the sidebar has weak contrast in the rendered view; the button text appears too faint.
- The first viewport looks impressive, but it does not show any chart. A client on a laptop must scroll before seeing actual analysis.
- Some KPI cards with text values, especially Best Store, risk truncation or uneven visual weight depending on viewport width.
- The donut chart for Category Revenue Mix is crowded. Small categories become hard to read, and labels compete inside narrow slices.
- The product chart truncates long product names, which helps visually, but the ellipses still create a portfolio/demo feel unless full names are available through tooltip or table.
- Rounded cards and shadows are attractive, but they are somewhat heavy for a dense BI dashboard. A more restrained enterprise design would use slightly smaller radii and lighter shadows.
- The color palette is stylish but not always meaningful. Colors do not consistently map to business semantics such as growth, risk, store, category, or demand intensity.
- The Streamlit top-right Deploy button and main menu remain visible, which reduces client-ready polish for screenshots.

Laptop readability:

- KPI cards are readable.
- Sidebar controls are readable but bulky.
- Charts are readable after scrolling.
- Dense product/category visuals need better spacing and label management.

Overall UI verdict: visually strong for portfolio use, but still visibly Streamlit and slightly over-styled for a real enterprise BI tool.

## F. Chart Review

### Monthly Revenue Trend

The line chart is the right chart type for time series. It shows a clear upward trend from January through June 2023, with monthly revenue rising from about $81.7K in January to about $166.5K in June.

Issues:

- It does not show MoM percentage change.
- It does not explain what caused the growth.
- It does not include target, forecast, or benchmark.
- Only six months are available, so trend interpretation should be careful.

Improvement: add MoM growth labels, a trend annotation, and a short insight such as "June revenue is 2.04x January revenue."

### Store Revenue Benchmark

Horizontal bar chart is appropriate for store comparison. Sorting is mostly readable.

Issues:

- Store revenue is very close: Hell's Kitchen $236.5K, Astoria $232.2K, Lower Manhattan $230.1K. The dashboard calls Hell's Kitchen "best store," but the gap is small and should be quantified.
- The chart does not show contribution percentage or variance from average.

Improvement: add revenue share and gap-to-leader labels. The insight should say the store network is balanced, not just that one store is best.

### Revenue by Product Category

Horizontal bar chart is appropriate. It clearly shows Coffee and Tea dominance.

Issues:

- Category share is not shown directly in this chart.
- Small categories are visible but not contextualized.
- The chart does not distinguish strategic categories from add-on categories.

Improvement: add revenue share, cumulative share, and an ABC-style classification.

### Top Products by Revenue

Horizontal bar chart is appropriate for product ranking. Truncated labels improve layout.

Issues:

- Product names are partially hidden on the axis.
- The chart ranks by revenue only, not margin, units, transactions, or repeatability.
- It does not identify whether high revenue comes from high price, high quantity, or both.

Improvement: add tooltip fields for quantity, orders, average price, and revenue share. Consider a table plus bar chart pair.

### Lowest Products by Revenue

This chart is useful but risky. Low revenue does not automatically mean poor performance. A low-revenue SKU may be new, seasonal, niche, supply-limited, or high-margin.

Issues:

- The chart can encourage incorrect retirement decisions.
- It does not show units, margin, stock availability, days sold, or category role.
- It lacks a warning that low revenue is a screening signal, not a final decision.

Improvement: rename to "Products for Review" and add criteria: revenue, units, revenue share, days active, and category.

### Demand by Hour

The bar chart is appropriate and supports staffing decisions. Peak demand around 10:00 is clear.

Issues:

- A single peak hour is less operationally useful than a peak window.
- It does not separate weekday/weekend or store-level demand.
- It does not show average transactions per day per hour, which would be more staffing-relevant.

Improvement: show peak window, store-specific hourly demand, and average hourly load per operating day.

### Day-Hour Demand Heatmap

The heatmap is a strong chart choice for operational planning.

Issues:

- The color scale is useful but could be paired with annotations for top cells.
- It does not turn the pattern into recommended staffing coverage.
- Some viewers may need a short interpretation near the chart.

Improvement: highlight top five day-hour cells and convert them into staffing suggestions.

### Store Workload Matrix

The matrix is appropriate for comparing workload by store and time slot.

Issues:

- It uses broad time slots, which may hide important hourly peaks.
- It uses transaction counts only, not items sold or revenue load.
- It does not show capacity or staff availability.

Improvement: add a store-hour matrix or a toggle between transactions, items, and revenue.

### Category Revenue Mix

The donut chart communicates broad category share but becomes crowded.

Issues:

- Small slices are hard to read.
- Donut charts are weaker for comparing many categories.
- Labels inside slices overlap or rotate awkwardly for smaller categories.

Improvement: replace with a sorted bar chart or Pareto chart. If keeping the donut, group small categories into "Other."

### Product Ledger/Table

The ledger is one of the better additions because it gives exact values and revenue share.

Issues:

- It focuses only on top product performance.
- It does not include average price, items per transaction, category rank, or contribution class.
- It is not clearly export-ready as a business report table.

Improvement: add filters/search, ABC class, average unit price, quantity share, and rank.

## G. Analytics Depth Review

Descriptive analytics: good. The dashboard clearly shows revenue, transactions, products, categories, stores, time slots, hourly demand, and day-hour patterns.

Diagnostic analytics: limited. The dashboard identifies top categories and peak hours, but it does not explain drivers. For example, it does not separate whether June growth came from higher transaction volume, higher AOV, specific stores, or product mix.

Operational analytics: moderate. Staffing and inventory recommendations exist, and the heatmap/workload matrix support operations. However, the recommendations are not quantified by demand per store, per hour, or per day.

Recommendation analytics: basic. The action cards are useful, but they are mostly template recommendations. They do not rank actions by expected impact, confidence, affected store, affected category, or time window.

Recommended analytical upgrades:

- Month-over-month revenue and transaction growth
- Store-wise comparison with revenue share and variance from average
- Product contribution percentage and cumulative contribution
- ABC analysis for products/categories
- Peak-hour staffing recommendation by store
- Low-performing product review with criteria beyond revenue
- Category mix analysis over time
- Inventory planning insight by category and peak window
- Demand seasonality by weekday and month
- Executive summary narrative generated from actual metric thresholds
- Store/category drilldowns
- Revenue decomposition: transaction volume versus AOV
- Pareto chart for top products

Current analytics maturity: strong descriptive dashboard, early-stage business intelligence, not yet advanced consulting analytics.

## H. Data Quality and Robustness Review

What works:

- CSV and Excel upload handling is included.
- Required columns are checked.
- Column names are normalized.
- Transaction date, time, quantity, unit price, transaction ID, and product ID are converted.
- Derived fields are created: revenue, hour, month, year-month, day, week start, and time slot.
- Missing key fields are dropped with warnings.
- Duplicate rows are detected and reported.
- Data QA tab shows filtered rows, original rows, date coverage, missing cells, column missing counts, unique counts, and data types.
- Download of filtered dataset is available.

Risks and gaps:

- Duplicate rows are only detected, not handled. That may be fine for audit transparency, but a business user needs guidance on whether duplicates affect KPIs.
- `transaction_qty` and `unit_price` invalid values are filled with 0, which prevents crashes but may hide data quality issues and understate revenue.
- Time parsing falls back to broad Pandas parsing. Some uploaded files could parse incorrectly depending on locale or format.
- Missing transaction time becomes hour 0 because `.dt.hour.fillna(0)` is used. That can create false midnight demand.
- The dashboard accepts uploaded files but does not preview validation errors by column before processing.
- The app does not appear to validate negative quantities, negative prices, future dates, zero-price products, impossible hours, or duplicate transaction IDs.
- The Data QA tab shows missing cells after filtering, but not invalid values that were coerced to zero or dropped.
- The existing `reports/executive_snapshot_error.txt` contains `name 'px' is not defined`, which is a visible project artifact and should be resolved before portfolio submission.
- The raw CSV already includes a `total_revenue` column, but the app recomputes revenue. That is acceptable, but the dashboard should clarify which revenue source is authoritative.
- There is no automated test or smoke-check artifact included for the Streamlit app.

Robustness verdict: better than a basic demo, but not yet production-grade.

## I. Portfolio / Hiring Manager Review

Would this impress a recruiter?

Yes, for an internship or junior data analyst portfolio, this would likely make a positive impression. It shows that the creator can move beyond basic charts and think about KPIs, filters, business sections, product performance, demand patterns, and data QA. The design also shows care.

What is strong:

- Professional visual first impression
- Streamlit plus Pandas plus Plotly implementation
- Clear executive KPI section
- Multiple analysis angles: revenue, store, product, demand, operations
- Good inclusion of Data QA and export
- Dynamic filters and upload capability
- Business language throughout the dashboard

What looks weak:

- The phrase "MNC-style" is asserted more than proven.
- Recommendations are generic and not backed by quantified impact.
- No growth percentages, benchmarks, targets, or variance analysis.
- No margin or profitability view.
- No customer segmentation despite "customer behavior" language.
- Some visuals are still standard chart outputs with styling rather than deeper BI thinking.
- Existing error artifact in the reports folder hurts polish.

What would make it more interview-worthy:

- Add a sharp business problem statement: "How should a coffee chain allocate staffing and product focus across stores to increase revenue and reduce low-demand waste?"
- Add MoM growth and store contribution metrics.
- Add one advanced analytical method such as Pareto/ABC analysis.
- Add a quantified recommendation section: action, impacted store/category, evidence, expected effect.
- Be ready to explain data cleaning assumptions, especially transaction uniqueness and time parsing.

Best screenshots for LinkedIn:

- Hero plus Executive Summary KPI section.
- Boardroom Overview showing Monthly Revenue Trend and Store Revenue Benchmark.
- Product Intelligence showing Top Products and Category Mix, preferably after chart label cleanup.
- Customer Demand heatmap.
- Executive Actions section after adding quantified recommendations.

Suggested interview story:

"I built a Streamlit BI dashboard from transaction-level coffee shop data to help managers understand revenue performance, category contribution, product winners, peak demand windows, and staffing opportunities. I cleaned and standardized the data pipeline, added interactive filters and upload support, built executive KPIs and operational visuals, and converted the analysis into action recommendations. The next iteration would add MoM growth, store variance, ABC product analysis, and quantified staffing recommendations."

## J. Priority Improvement Roadmap

### Priority 1: Must fix before showing to client/recruiter

| Problem | Why it matters | Suggested fix | Difficulty | Impact |
|---|---|---|---|---|
| Recommendations are generic | Clients need specific decisions, not broad advice | Make actions dynamic with evidence: store, category, peak window, revenue share, and priority | Medium | High |
| No MoM growth or comparison KPIs | Raw numbers lack business interpretation | Add MoM revenue change, transaction change, AOV change, and highest growth month | Medium | High |
| "Products Sold" label is ambiguous | It can be confused with quantity sold | Rename to "Distinct Products" or add a note | Easy | Medium |
| AOV is rounded too aggressively | "$5" looks imprecise and less analytical | Show `$4.69` or one decimal | Easy | Medium |
| Sidebar is bulky | Laptop users must scroll through filters before analysis | Collapse advanced filters or reduce default chip visibility | Medium | High |
| Existing report error file | Looks unfinished in a portfolio package | Fix or remove the broken report generation artifact after confirming scope | Easy | Medium |
| Low-revenue products may be misinterpreted | Low revenue does not equal bad product | Rename to "Products for Review" and add quantity/share/context | Easy | High |
| Browser/page title is generic | Reduces client polish | Set a visible project title in browser/server configuration if possible | Easy | Low |

### Priority 2: Should improve for portfolio quality

| Problem | Why it matters | Suggested fix | Difficulty | Impact |
|---|---|---|---|---|
| Category donut is crowded | Hard to read small categories | Replace with Pareto or sorted bar chart; group small categories as Other | Medium | High |
| Store winner gap is not quantified | The best store is only slightly ahead | Add revenue share and gap versus second store | Easy | Medium |
| Demand insight is only peak hour | Operations need staff windows | Create peak demand window by store and day | Medium | High |
| No business problem statement | Story is broad | Add a short client problem and decision objective above KPIs | Easy | High |
| Data QA lacks invalid-value checks | Missing cells alone are not enough | Add invalid dates, zero revenue, negative qty/price, duplicate transaction ID checks | Medium | High |
| Product analysis lacks contribution logic | Top products need portfolio framing | Add revenue share, cumulative share, ABC class | Medium | High |
| Color semantics are inconsistent | Business dashboards need meaning | Define fixed colors by store/category or semantic status | Medium | Medium |

### Priority 3: Advanced improvements for standout impact

| Problem | Why it matters | Suggested fix | Difficulty | Impact |
|---|---|---|---|---|
| No forecasting | Limits strategic planning | Add lightweight demand forecast for next month or week | Hard | High |
| No profitability | Revenue alone can mislead | Add margin if cost data is available | Hard | High |
| No customer segmentation | "Customer behavior" is limited without customers | Add loyalty/customer data or rename the dashboard focus | Hard | Medium |
| No target tracking | Executives want performance vs goal | Add target revenue, variance, and status indicators | Medium | High |
| No automated report output | Client delivery often needs PDF/PPT | Add executive snapshot export once the current report error is fixed | Hard | Medium |
| No scenario modeling | Strong BI projects support decisions | Add price/volume what-if model for AOV and revenue | Hard | High |

## K. Final Recommendation

This dashboard is ready to show as a polished portfolio draft, but not as a final client/MNC dashboard. It is visually impressive for Streamlit and demonstrates strong junior data analyst capability. For recruiter viewing, it is close. For client presentation, it needs stronger business logic, more precise KPIs, quantified recommendations, and a cleaner sidebar experience.

What should be fixed first:

1. Add MoM growth and revenue share KPIs.
2. Make recommendations dynamic, specific, and evidence-backed.
3. Rename ambiguous metrics and charts.
4. Improve the product/category visuals, especially the donut and low-revenue product chart.
5. Strengthen Data QA with invalid-value and parsing-risk checks.

Should the layout be redesigned or polished?

Polish first. The current structure is good enough to keep. A full redesign is not necessary. The main need is sharper executive storytelling, cleaner filter ergonomics, and stronger chart interpretation.

Should it remain Streamlit or move to Power BI?

For a Python/data analyst portfolio, keep Streamlit. It shows coding ability, data preparation, and interactive app development. For a corporate BI role or client-facing operations dashboard, a Power BI version would be more recognizable to business stakeholders. The best portfolio strategy would be to keep this Streamlit version and optionally add a Power BI companion screenshot/report later.

What would make it look like a real company dashboard?

- A clear business objective and target audience
- KPIs with comparison, variance, and trend
- Store/category contribution percentages
- Action cards tied to quantified evidence
- Demand recommendations by store and time window
- Data QA that flags true business risks
- A cleaner sidebar with fewer visible chips
- Exportable executive summary
- Less generic language and more specific management decisions

Bottom line: this is a strong portfolio project, not a basic student demo. It is approximately 70-75% of the way to a client-ready analytics product. The next improvement should not be more decoration; it should be deeper business analysis and more decision-grade recommendations.
