# DEAP_Evolutionary_Algorithm
Archive for COMP 3160, Adversary game of 3 players with evolutionary algorithm

Three bystanders, P1, P2 and P3, witness a hit-and-run accident, with the victim seri- ously injured. None of these bystanders has the appropriate (medical) skill to help the injured. They are fully aware of their civic duty – to immediately call the emergency number 000 (Triple-Zero) and report the accident so that both police and ambulance can be dispatched to the accident site to help the victim as well as carry out the police investigation. Each of the bystander can either volunteer (V) to call Triple-Zero, or remain apathetic (A) to the victim and do nothing. The assumed facts are:

1. If none of three bystanders volunteers to call Triple-Zero, the victim will die, and each of P1, P2 and P3 will suffer from lifelong shame and guilt.

2. There is a cost to calling Triple-Zero: the volunteer would need to provide their own details, wait at the accident site until the ambulance/ police arrives, and will likely be called to visit the police station and provide more evidence regarding the accident in future if necessary.
 
3. Thecostdecreasesiftherearemorethanonevolunteers–individuallytheywill need to provide less detail, and they will not have to make lonely trip to the police station in future if it becomes necessary.
 
4. The three bystanders are generally sociable – they prefer to be in each-other’s company than by their own.
 
5. If at least one bystander volunteers, the victim will be treated, and the one(s) who don’t volunteer would not have to suffer from lifelong guilt and shame.

If you were one of those witnesses, would you call Triple-Zero, or remain a mute spectator?

We model this 3VD game by the payoff matrix given in Table 1 below.
Pj & Pk
| | 0V | 1V | 2Vs |
|-----|----|----|----|
|V| 5 | 6 | 8 | 
|-----|----|----|----|
Pi |A| 0 | 9 | 7 |

Payoffs to Pi, under how many of {Pj, Pk} play V.
