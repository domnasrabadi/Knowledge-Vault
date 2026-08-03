---
type: article
status: raw
quality:
topics: [data-science, interview-prep]
source: ""
created: 2025-02-28
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Given 2 bets and their modelled probability, which would you choose and why 
- Team A Wins = $1.55
	- Model probability = 70%
- Team B Wins or Draw = $1.80
	- Model probability = 30%
- I calculated this correctly using concept of expected values e.g. 
	- EV Outcome 1 = $0.70 \times 1.55 = 1.085$
	- EV Outcome 2 = $0.30 \times 1.80 = 0.54$
	- so you pick outcome 1 as that has higher expected value 

# 2 How would you construct a formula to choose in this scenario 
- I stumbled here and gave something kinda vague 
	- Payoff(A) * P(A) > Payoff(B) * P(B)
	- This is kinda overfitted to this example but given the pressure, it's the best i could come up with 
- getting GPT's help, here is a better answer 
	- $EV = p \times M$
		- where $p$ = probability of winning the bet 
		- and $M$ is the payoff multiplier 
	- so you calculate EV for each outcome 
		- then use this decision rule -> *Choose Bet 1 if $EV_1 > EV_2$, otherwise choose Bet 2*
- honestly, on second thought its not a bad initial answer 

# 3 Given $100, how would you allocate for guaranteed profit with 0 variance
- I dont recall how i answered here, but I mentioned there might be an analytical solution which I didnt have time to work out, so also suggested brute force approach and just calculated for every possible split, what would be the profit 
	- I dont really understand the zero variance part 
- GPT Answer
	- want to allocate your $100 in such a way that both outcomes yield the same total return—and that return exceeds $100
	- set up equations 
		- $x$ = amount wagered on team A to win at $1.55
		- $y$ = amount wagered on Draw or Team B to win at $3.80
		- 2 conditions give this total money constraint - $x + y = 100$
		- equal payoff condition - to guarantee same return regardless of outcome 
			- $1.55 \times x = 3.80 \times y$
	- Solve for $x$ and $y$
		- solve equal payoff condition for 1 variable i.e. $x$
			- $x = \frac{3.8}{1.55} \times y \approx 2.4516 \times y$  - i.e. solving for just $x$ right now 
		- substitute expression into total money constraint
			- $2.4516 y + y = 100 \longrightarrow 3.4516y = 100$
			- since $2.4516 y + y$ is equivalent to $(2.4516 + 1)y$ which simplifies to $3.4516y$ 
		- now solve for $y$
			- $y \approx \frac{100}{3.4516}\approx 28.96$
		- then calculate $x$
			- $x = 100 - 28.96 \approx 71.04$
	- verify for guaranteed payoff
		- if team A wins - Return = $1.55 \times 71.04 \approx 110.12$
		- if team B wins/draw - Return = $3.8 \times 28.96 \approx 110.05$ (rounding errors)
		- this allocation guarantees return of approx $110 regardless of outcome, with zero risk 

# 4 Gambler's Ruin Problem
- only knew name after GPT told me, here's the full question 
	- i answered that i would brute force it using Python after Boris prompted me 
	- given a new problem where you start with $100 and can only bet on A or 1-A (which is essentially just the second outcome), you are only allowed to bet $1 each time, and can continue until you reach $1000 or until you go broke and spend all your money. What is the % of A that needs to be true i.e. the probability A can occur, for you to be able to reach $1000 with at most a 10% chance of going completely broke
- Suppose you have a starting capital $i = \$100$ and a target $T = \$1000$. On each \$1 bet, you win \$1 with probability $A$ and lose \$1 with probability $(1-A)$.
### 4.1.1 Using gambler ruin formula 
For a bet with win probability $p = A$ and loss probability $q = 1-A$, if $p > q$ the probability of reaching the target before going broke is given by
$$

P(\text{reach } T) = \frac{1 - \left(\frac{q}{p}\right)^i}{1 - \left(\frac{q}{p}\right)^T}.

$$
In our case, we want the probability of ruin (going broke) to be at most 10%, i.e.,
$$

P(\text{ruin}) = 1 - P(\text{reach } T) \leq 0.10.

$$
For large $T$ (here $T = 1000$) and if $\left(\frac{q}{p}\right)^T$ is very small, we can approximate
$$

P(\text{ruin}) \approx \left(\frac{q}{p}\right)^i.

$$
Thus, we set
$$

\left(\frac{1-A}{A}\right)^{100} \leq 0.1.

$$
### 4.1.2 Solving the equation 
**Take the 100th Root of Both Sides:**
$$
\frac{1-A}{A} \leq 0.1^{\frac{1}{100}}.
$$
**Evaluate the 100th Root:**
$$
0.1^{\frac{1}{100}} = e^{\frac{\ln(0.1)}{100}} \approx e^{-\frac{2.302585}{100}} \approx e^{-0.02303} \approx 0.9773.
$$
**Set Up the Equation:**   
$$
\frac{1-A}{A} \leq 0.9773.
$$
**Solve for $A$:**

Multiply both sides by $A$:
$$1-A \leq 0.9773\,A$$
$$1 \leq 0.9773\,A + A = 1.9773\,A,$$$$A \geq \frac{1}{1.9773} \approx 0.5057.$$
   
- You need the probability $A$ of winning each \$1 bet to be at least about **50.57%** (or roughly **51%**) to ensure that your chance of going broke is at most 10% before you reach \$1000. 
- could also simulate this process using a loop in Python to validate the analytical result. For example, you might write a simulation that repeatedly bets \$1 starting from \$100, stopping when you reach \$1000 or go broke, and then computing the ruin probability for various $A$ values. The simulation would confirm that when $A$ is around 51%, the probability of ruin drops below 10%.
# 5 Questions 5 to 7, no GPT solution 
1. given logistic regression summary table with p-values, coefficients, variable names - what would you change with this model, what do you notice 
2. interpret and label a partially blank ROC/AUC plot 
3. given a pricing model of static premium pricing given number of historic claims + sum insured, and then a PDP which is a curvy line going downwards right, why is it not smooth 
	- i asked chris this too and it wasnt clear to him either 