---
name: mobile-app-financial-planning
description: >
  Financial planning toolkit for mobile application businesses. Covers 3-5 year
  revenue projections with cohort-based modelling, cost structure (COGS, S&M,
  R&D, G&A), cash flow analysis, runway calculation, unit economics (CAC, LTV,
  payback), spending pattern analysis, subscription pricing strategy, fundraising
  scenario modelling, and three-scenario planning (conservative / base /
  optimistic). Use when: building investor financial models, projecting MRR/ARR,
  calculating burn rate and runway, evaluating pricing tiers, planning headcount
  budgets, auditing subscription costs, or preparing for a funding round.
version: 1.0.0
merged-from:
  - startup-financial-modeling v1.0.0
  - budget-optimizer v1.0.0
---

# Mobile App Financial Planning

> From monthly budget hygiene to 3-year investor models:
> financial clarity for mobile application businesses at every stage.

---

## Scope

This skill covers two levels of financial work that mobile founders typically need
simultaneously. **Operational finance** addresses day-to-day budget management,
subscription audits, and burn rate monitoring. **Strategic finance** addresses
multi-year revenue projections, unit economics, and fundraising scenarios.

Use each section independently or together depending on your current need.

---

## 1. Revenue Modelling

### Cohort-Based MRR Projection

Build revenue from customer acquisition and retention by cohort rather than from
a single growth-rate assumption. This produces more accurate projections and makes
sensitivity analysis meaningful.

```
MRR = Σ (Cohort Size × Retention Rate × ARPU)
ARR = MRR × 12
```

**Monthly Customer Acquisition.** Define new customers acquired each month, broken
out by channel if your attribution allows it.

**Retention Curve.** Model customer retention over time. Typical SaaS / mobile
subscription benchmarks:

| Month after signup | Retention (typical) |
| ------------------ | ------------------- |
| 1                  | 100%                |
| 3                  | 90%                 |
| 6                  | 85%                 |
| 12                 | 75%                 |
| 24                 | 70%                 |

**Expansion Revenue.** Include upsell and cross-sell revenue as a separate line.
This prevents the model from undervaluing high-retention cohorts.

### Business Model Variants

**SaaS / Subscription.** Revenue drivers are new MRR, expansion MRR, contraction
MRR, and churned MRR. Target gross margin is 75–85%.

**Marketplace.** Revenue equals GMV multiplied by take rate (typically 10–30%
depending on category). Model buyer and seller economics separately if acquisition
costs differ.

**Transactional.** Project transaction volume, revenue per transaction, and
purchase frequency. Include seasonality assumptions.

---

## 2. Cost Structure

Organise costs into four standard categories to make the model comparable to
industry benchmarks and investor expectations.

**Cost of Goods Sold (COGS)** — Hosting and infrastructure, payment processing
fees, variable customer support, and third-party services consumed per customer.
COGS as a percentage of revenue is the primary driver of gross margin.

**Sales and Marketing (S&M)** — Customer acquisition spend, sales team
compensation, marketing tools, and content production. The CAC payback period
(months of subscription revenue to recover acquisition cost) should be tracked
monthly.

**Research and Development (R&D)** — Engineering compensation, product management,
design, and development infrastructure. On mobile teams, R&D is typically the
largest cost category at early stage.

**General and Administrative (G&A)** — Executive team, finance, legal, HR, office,
and insurance. Target G&A at 10–15% of total expenses once the business reaches
meaningful scale.

---

## 3. Headcount Planning

Model headcount by department and role. Use fully-loaded cost (salary plus benefits
and taxes, typically 1.30–1.40× base salary) rather than base salary alone.

**Typical early-stage ratios.** Engineering: 40–50% of headcount. Sales and
Marketing: 25–35%. G&A: 10–15%. Customer Success: 5–10%.

**Ramp time.** New hires are not fully productive on day one. Model a 3-month ramp
for individual contributors and a 6-month ramp for managers. This prevents the
model from assuming immediate revenue impact from a hiring wave.

---

## 4. Cash Flow and Runway

```
Beginning Cash
+ Revenue Collected (apply payment terms: net-30 contracts delay cash inflow)
- Operating Expenses Paid
- Capital Expenditure
= Ending Cash

Runway (months) = Ending Cash ÷ Average Monthly Burn Rate
Monthly Burn    = Total Monthly Expenses − Monthly Revenue
```

**Common pitfalls.** Revenue recognised is not the same as cash received. Annual
contracts paid upfront create cash surpluses that hide structural burn. Annual
contracts billed monthly defer cash and create burn that looks worse than it is.
Model cash explicitly, not just P&L.

---

## 5. Unit Economics

Unit economics are the per-customer version of the income statement. They answer
whether the business model is sound before scale makes the numbers large enough
to obscure problems.

**Customer Acquisition Cost (CAC)** — Total S&M spend in a period divided by new
customers acquired in that period. Track by channel where attribution is available.

**Lifetime Value (LTV)** — Average revenue per customer multiplied by gross margin,
divided by churn rate. A shortcut formula: `LTV = ARPU × Gross Margin % ÷ Monthly Churn Rate`.

**CAC Payback Period** — Months of gross profit required to recover the acquisition
cost. Under 12 months is strong for mobile subscription; under 18 months is
acceptable.

**LTV:CAC Ratio** — The foundational health metric. Greater than 3:1 indicates a
sustainable model. Less than 2:1 requires immediate attention to either CAC
reduction or retention improvement.

**Burn Multiple** — Net burn divided by net new ARR. Below 1.5 is efficient. Above
2.5 at Series A stage is a concern for most investors.

**Magic Number** — Net new ARR divided by prior-quarter S&M spend. Greater than
0.75 suggests the sales and marketing engine is working.

---

## 6. Three-Scenario Framework

Every financial model should include three scenarios tied to specific input
assumptions rather than vague optimism or pessimism.

**Conservative (P10)** — Slower customer acquisition (−30%), higher churn (+20%),
higher CAC (+25%). Used for cash management and minimum funding calculations.

**Base (P50)** — Most likely outcomes based on current trajectory. Primary
planning scenario for board reporting and budgeting.

**Optimistic (P90)** — Faster growth (+30% acquisition), better retention (−20%
churn), lower CAC (−25%). Used for upside planning and maximum valuation scenarios.

**Sensitivity levers.** The variables that typically have the largest impact on
outcome are monthly customer acquisition rate, average contract value, monthly
churn rate, and CAC. Run scenarios by varying each independently and in combination.

---

## 7. Pricing Strategy

**Freemium.** Core features free; premium features behind a subscription or
one-time purchase. Typical conversion rate: 2–5%. Requires large top-of-funnel
volume to produce meaningful subscription revenue.

**Subscription.** Monthly or annual payment. Annual plans improve LTV and should
be presented at a 30–50% discount to the monthly equivalent. Apple and Google take
30% in year one, 15% from year two onward — model this explicitly.

**One-Time Purchase.** Viable for simple utility apps. Limits development
sustainability because there is no recurring revenue to fund ongoing updates.

**Price Discovery.** A/B testing via App Store Connect is the most reliable
approach. Perceived value of an annual plan should be positioned as 20–30% below
the annualised monthly rate.

---

## 8. Fundraising Scenarios

**Dilution Calculation.**

```
Post-Money Valuation = Pre-Money Valuation + Investment Amount
Investor Dilution %  = Investment ÷ Post-Money Valuation
```

**Funding Amount.** Size the raise to cover operations through the next
investor-meaningful milestone plus a six-month buffer. Raising too little forces
a premature bridge round. Raising too much creates unnecessary dilution.

**Use of Funds Template.**

```
Product Development:   [X]% — Engineering headcount and infrastructure
Sales and Marketing:   [X]% — UA spend and sales team
G&A and Operations:    [X]% — Finance, legal, admin
Working Capital:       [X]% — Buffer for assumptions proving wrong
```

---

## 9. Operational Budget: Subscription Audit

For teams already operating, a quarterly subscription audit often surfaces
meaningful savings before any strategic modelling is necessary.

**Audit process.** Export all recurring charges from the last three months of
bank statements or credit card records. Categorise each into: actively used,
occasionally used, unused, or unknown. For anything unused or unknown, cancel
immediately. For occasionally used tools, evaluate whether a lower tier or an
annual consolidation reduces cost.

**Spending ratios to track.** Development tools: target under 8% of R&D payroll.
Marketing tools: target under 5% of S&M spend. Infrastructure: target under
10% of COGS.

---

## 10. Model Validation Checklist

Before presenting a financial model to investors or the board, verify the following.

- [ ] Revenue growth rate is achievable: 3× in Year 2, 2× in Year 3 is aggressive
      but common at early stage — anything faster requires strong evidence
- [ ] Unit economics are positive: LTV:CAC greater than 3:1, payback under 18 months
- [ ] Burn multiple is reasonable: below 2.0 by Year 2–3
- [ ] Headcount scales proportionally: revenue per employee should be growing
- [ ] Gross margin is appropriate for the business model
- [ ] S&M spending is tied to a CAC assumption that is achievable given channel data
- [ ] Cash flow is modelled separately from P&L with payment terms applied
- [ ] All three scenarios have been generated and the conservative case is survivable
- [ ] Sentry DSN, API keys, and other secrets are not embedded in any shared model
      files (relevant if the model is exported or shared outside the team)

---

## Common Pitfalls

**Overly optimistic revenue.** New apps rarely hit aggressive acquisition projections.
Model conservative customer acquisition and realistic churn before assuming
favourable scenarios.

**Underestimating costs.** Add a 20% buffer to all expense estimates. Fully-loaded
compensation, software subscriptions, and legal costs are routinely underestimated
by first-time founders.

**Confusing revenue and cash.** Annual contracts, delayed invoicing, and App Store
payment cycles all create gaps between when revenue is recognised and when cash
arrives.

**Static headcount.** Hiring takes 3–6 months to fill roles, and new hires require
3–6 months to reach full productivity. A hiring plan that assumes immediate
contribution will always overshoot on both cost and output.

**Single-scenario planning.** A model with only a base case is not a model — it
is a guess. Always produce the conservative case and plan for what you will do
if that case materialises.
