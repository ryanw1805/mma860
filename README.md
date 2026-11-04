# mma860
Business Question: The overarching business question would be what impacts the pricing of Airbnb. Our target audience will be for Airbnb users to help make informed decisions regarding prices when setting up a new Airbnb. They then can use our model to figure out what type of property to purchase, whether the different variables that impact a neighborhood affect the prices it holds as well.


The Technique/Model


1. Simple ln OLS Regression: We will use a log model with the following specification to investigate the % change in price with each variable changing. There are 4 distinct room types, so it will be 4 different binary variables.


ln (Price per night)ᵢ = β₀ + β₁·#bedsᵢ + β₂·Typeᵢ + β₃·host hosting yearsᵢ + β₄·Reviewsᵢ + β₅·super Hostᵢ + β₆·maximum stay nightᵢ + β7·minimum stay night + εᵢ

**Note: change to the specification (minimum stay).** Minimum stay now enters the model as a yes/no variable, not a count of nights:

ln (Price per night)ᵢ = β₀ + β₁·#bedsᵢ + β₂·Typeᵢ + β₃·host hosting yearsᵢ + β₄·Reviewsᵢ + β₅·super Hostᵢ + β₆·maximum stay nightᵢ + β₇·Monthly stayᵢ + εᵢ

Monthly stay = 1 if the listing requires at least 28 nights, otherwise 0. Toronto's short-term rental rules apply to stays under 28 nights, so most hosts set their minimum either below 28 or at exactly 28 (10,811 listings). 52% of the listings in the model are monthly rentals.

Why it changed: with minimum nights as a count, the model assumed each extra night of minimum stay lowers price by the same % (about 1.2% per night). That worked badly at the extremes. Rentals with a 360–365-night minimum were predicted at about $2–4 a night against actual prices of about $40–270, and they showed up as a cluster of outliers in Technique 4.

What changed in the results (neighbourhood fixed-effects model, host-bootstrapped 95% CIs):
- Monthly rentals are about 57% cheaper per night than short-term rentals, the largest effect in the model.
- R² rose from 0.61 to 0.71 (and from 0.54 to 0.66 without neighbourhood fixed effects).
- Superhost went from +0.7% (not significant) to −5.5% (significant), reviews from +0.06% to −0.04% per review, and host years from −1.6% to +0.4% per year. The hotel-room premium fell from +18% to +5% and is no longer significant.
- These shifts happened because short-term listings differ systematically: they have more superhosts (53% vs. 31%) and more reviews (57 vs. 19 on average), and their hosts are newer (3.0 vs. 5.4 years). The count-of-nights version didn't fully capture how much pricier short-term rentals are, so those variables were partly picking that up.
- Beds (+25%), private room (−41%) and shared room (−52%) were essentially unchanged.
- After the change, removing outliers or suspected data errors no longer flips any coefficient's sign or significance.


2. Bootstrapping: To confirm the validity of the model, we will incorporate bootstrapping into this initial hedonic pricing regression, the resampling process is applied directly to the dataset to ensure robust, non-parametric standard errors and confidence intervals. Because listing characteristics and error terms in real estate and rental marketplaces often exhibit spatial clustering, heteroskedasticity, or complex dependencies across listings managed by the same host, standard analytical formulas can miscalculate precision. We will deploy this method on every regression model.


3. Regression with fixed effect and hypothesis testing: To debunk or reinforce the hypothesis that each neighborhood has a difference in price. First, we will organize the average price in each neighborhood from the lowest to the highest. Then conduct a hypothesis test between the two, with the alternate hypothesis being a difference between the average of the most expensive neighborhood and the lowest. For this, we will use alpha of 0.05 and revisit the initial model with a neighborhood fixed effect. Re-estimating the variables will provide us with a more robust model with less omitted variable bias. By holding neighborhood constant, the estimates will have eliminated any differences.

4. Outlier identify: We use a scatter plot to plot the data points. This gives us a visual interpretation on the heteroskedasticity of the data, and we can use it to identify outliers as well. Plot all the listings as dots on a map of their features against price. Most dots will cluster together. Leverage measures how far each dot sits from that crowd. Dots far from the crowd get flagged. We then check whether each flagged listing is a typo or a real but unusual place, and whether removing it would change our results.


5. Logit: We will estimate the effect of price on booking with a control-function IV approach. Log price is treated as endogenous (the variable, log price, is correlated with the error term in the outcome equation) and instrumented with the host’s average price premium on their listings in other neighborhoods. The first stage regresses log price on this instrument, listing and host controls, and neighborhood fixed effects. The first-stage residual is then included alongside log price in a second-stage logit model of whether the listing is booked (1) or not (0). Standard errors are obtained by bootstrapping both stages, resampling hosts.