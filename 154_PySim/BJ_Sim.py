####################################
####################################
###     Omar Flores Estrada     ####
###     CSCI 154 Dr. Thanos     ####
###        4.18.2021            ####
####################################
####################################

from __future__ import print_function 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Shadow # libaries for array manipulation and visualization 

HIT_GO = 0                  # At each move deal & player can make the choice to HIT or STAND
STAND_GO = 1   
actions = [HIT_GO, STAND_GO] 

# Policy for the player
# The player will go BUST if past 21
policyPlayer = np.zeros(22)      # Array that goes up to 21, that's the crucial point for players
for i in range(12, 20):
    policyPlayer[i] = HIT_GO # Player will take risk between this range to HIT

policyPlayer[20] = STAND_GO  # once at this point, Player will STAND 
policyPlayer[21] = STAND_GO  # Definitely stand here

def targetPolicyPlayer(acePlayerHand, playerSum, dealerCard): #Target policy of player
    return policyPlayer[playerSum]      #returns sum to decipher what to do

def behaviorPolicyPlayer(acePlayerHand, playerSum, dealerCard): 
    # bernoulli random number generator
    if np.random.binomial(1, 0.5) == 1: #(Number of trials (1) we only need 1 time, Probability of occurence, size = number of times to check)
        return STAND_GO             # if randomly returns 1 == 1 player takes action to stand, 1/2 chance
    return HIT_GO                   # if not HIT

# Policy for the dealer
policyDealer = np.zeros(22)         # Same 1D array for the dealer, he can BUST too
for i in range(12, 17):             # The dealer will keep Hitting until the value >= 17 
    policyDealer[i] = HIT_GO
for i in range(17, 22):             # Dealer will STAND when within this range of 17 - 21
    policyDealer[i] = STAND_GO 

def getCard():                      # Infinite Deck policy
    card = np.random.randint(1, 14) # returns a random int from the range 1 - 13 since there are 13 ranks in blackjack
    card = min(card, 10)            # Any card from the ranks will default to 10 if it goes past 10 (ex. - Jack, Queen, King, Etc)
    return card                     # return the value of the card

def play(policyPlayerFn, initialState=None, initialAction=None):
    playerSum = 0               #initializing variables
    playerTrajectory = []       #How the player is performing 
    acePlayerHand = False     #Whether or not for player to use Ace as an 11
    
    dealerCard1 = 0             #The initial 2 cards for the dealer
    dealerCard2 = 0 
    aceDealerHand = False     #Whether or not the dealer uses the Ace as an 11
 
    if initialState is None:    #Generate a random initial state
        numOfAce = 0
        while playerSum < 12:   # If the sum of the players card is less than 12, hit the deck
            card = getCard()    # get a card with the function
            if card == 1:       # if you get an ACE 
                numOfAce += 1   # Increment number of aces held
                card = 11       # give card 11 value 
                acePlayerHand = True  
            playerSum += card   # Add card value to the overall player's sum

        if playerSum > 21:      # If we go over 21 
            playerSum -= 10     # decrement the player sum by 10 treating the ace like a 1
            if numOfAce == 1:   # No longer will be using that Ace for it's 11 value
                acePlayerHand = False 

        dealerCard1 = getCard() # Initialize the 2 Dealer's cards
        dealerCard2 = getCard() 

    else: # default else 
        acePlayerHand = initialState[0] 
        playerSum = initialState[1] 
        dealerCard1 = initialState[2] 
        dealerCard2 = getCard() 

    state = [acePlayerHand, playerSum, dealerCard1] # Initializing the game state 

    dealerSum = 0                               # Okay now it's the Dealer's turn, initializing the Dealer's sum 
    if dealerCard1 == 1 and dealerCard2 != 1:   # If the dealer gets 1 Ace and one regular card
        dealerSum += 11 + dealerCard2           # increment by ACE (11) plus the regular card
        aceDealerHand = True                  # Dealer has a usable ace
    elif dealerCard1 != 1 and dealerCard2 == 1:     # Same scenario but in case card 2 is an ACE
        dealerSum += dealerCard1 + 11 
        aceDealerHand = True 
    elif dealerCard1 == 1 and dealerCard2 == 1: # In case both cards are ACEs 
        dealerSum += 1 + 11                     # Only use one ACE in value 11
        aceDealerHand = True                  
    else:                                       # default Else just add up the sum of the cards 
        dealerSum += dealerCard1 + dealerCard2 


    while True:                                 # Where the game starts for player
        if initialAction is not None:           # If there is an action to be initially done
            action = initialAction 
            initialAction = None                # Reloads it
        else:
            # Action based on the current sum of the player
            action = policyPlayerFn(acePlayerHand, playerSum, dealerCard1) # we have the first dealer card cause we just assume the other face down one is a 10
            # Tracking the trajectory to see the performance 
        playerTrajectory.append([action, (acePlayerHand, playerSum, dealerCard1)])

        if action == STAND_GO: 
            break                                   # if Stand break from the while loop 
        playerSum += getCard()                      # Else to HIT

        if playerSum > 21:                          # if player BUSTS goes over 21
            if acePlayerHand == True:             # if player has an Ace and can use it as a 1 instead of 11
                playerSum -= 10                 
                acePlayerHand = False             # No more usable ACE (11)
            else:
                return state, -1, playerTrajectory  # Else BUST player loses and gets a -1 

#################################################################

    while True: # Dealer's turn
        action = policyDealer[dealerSum]
        if action == STAND_GO: 
            break                                   # if STAND then break from the while loop here
        dealerSum += getCard()                      # else HIT another card
        if dealerSum > 21:                          # If dealer BUSTS
            if aceDealerHand == True:             # But has an ACE 
                dealerSum -= 10                     # Treat the ACE as a 1 and not an 11
                aceDealerHand = False             # No longer usable ACE (11)
            else:
                return state, 1, playerTrajectory   # Dealer goes BUST returns a +1 for the player 



    if playerSum > dealerSum:                       # Now we can compare the sums of both Player & Dealer
        return state, 1, playerTrajectory           
    elif playerSum == dealerSum:                    # If same sum for both hands 
        return state, 0, playerTrajectory 
    else: 
        return state, -1, playerTrajectory          # If sum is not larger than dealer sum return -1



#############################################################33
## Monte Carlo #####


def monteCarlo(iterations): 
    games = 0
    for i in range(0, iterations): 
        _, reward, _ = play(targetPolicyPlayer) 
        games += reward 
    return games



##########################################################333

# Printing the pie chart

test = 0 

test = monteCarlo(1000000)
losses = 1000000 + test 
print(test)

wins = 1000000 - test 

# Creating dataset
outcomes = ['Wins', 'Losses']
  
data = [losses, wins]

explode = (0.1, 0.0)
colors = ( "orange", "cyan")
wp = { 'linewidth' : 1, 'edgecolor' : "green" }
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)

fig, ax = plt.subplots(figsize =(10, 7))
  
wedges, texts, autotexts = ax.pie(data, 
                                  autopct = lambda pct: func(pct, data),
                                  explode = explode, 
                                  labels = outcomes,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))
  

ax.legend(wedges, outcomes,
          title ="Blackjack Outcomes",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))

plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Blackjack 1,000,000 outcomes")

plt.show()

