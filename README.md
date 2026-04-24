# Bidding_strategy
Manual trading challenge

You trade against a secret number of counterparties that all have a **reserve price** ranging between **670** and **920**. You trade at most once with each counterparty. On the next trading day, you’re able to sell all the product for a fair price, **920**.

The distribution of the bids is **uniformly distributed** at **increments of 5** between **670** and **920** (inclusive on both ends). 

<aside>

**Example**: counterparties may have reserve prices at 675 and 680, but not at 676, 677, 678, 679, etc..
</aside>

You may submit **two bids**. If the first bid is **higher** than the reserve price, they trade with you at your first bid. If your second bid is **higher** than the reserve price of a counterparty and **higher** than the mean of second bids of all players you trade at your second bid. If your second bid is **higher** than the reserve price, but **lower** than or **equal** to the mean of second bids of all players, the chance of a trade rapidly decreases: you will trade at your second bid **but** your PNL is penalised by

<img width="253" height="121" alt="{1C83C93F-E0FA-42F2-80AA-1BE8D08E889A}" src="https://github.com/user-attachments/assets/e8189699-c77c-4ca6-a7de-14670ed61157" />
