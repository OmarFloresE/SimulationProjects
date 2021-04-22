####################################
####################################
###     Omar Flores Estrada     ####
###     CSCI 154 Dr. Thanos     ####
###        4.18.2021            ####
####################################
####################################

# • Policy 1: if your hand ≥ 17, stick. Else hit. 
# • Policy 2: if your hand ≥ 17 and is hard, stick. Else hit unless your hand = 21.
# • Policy 4: Always stick. 
# • Two policies of your choice
# Evaluate all policies for the following versions of the game: --------------------------
# • Infinite deck: On every run a card is drawn with equal probability. ###
# • Single deck: One deck of cards is used. The deck is reshuffled after every 

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
for i in range(12, 17): # range is 12 to 16
    policyPlayer[i] = HIT_GO # Player will take risk between this range to HIT

for i in range(17, 22): # Range is 17 to 21
    policyPlayer[i] = STAND_GO



def targetPolicyPlayer(acePlayerHand, playerTotal, dealerCard): #Target policy of player
    return policyPlayer[playerTotal]      #returns sum to decipher what to do

def behaviorPolicyPlayer(acePlayerHand, playerTotal, dealerCard): 
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

def drawCard():                      # Infinite Deck policy
    card = np.random.randint(1, 14) # returns a random int from the range 1 - 13 since there are 13 ranks in blackjack
    card = min(card, 10)            # Any card from the ranks will default to 10 if it goes past 10 (ex. - Jack, Queen, King, Etc)
    return card                     # return the value of the card

def play(policyPlayerFn, initialState=None, initialAction=None):
    playerTotal = 0           #initializing variables
    dealerTotal = 0    
    playerTrackRec = []       #How the player is performing 
    acePlayerHand = False     #Whether or not for player to use Ace as an 11
    # policyTwo = False
    
    dealerCard1 = 0             #The initial 2 cards for the dealer
    dealerCard2 = 0 
    aceDealerHand = False     #Whether or not the dealer uses the Ace as an 11 and has ACE
 
    if initialState is None:    #Generate a random initial state
        totalAces = 0
        while playerTotal < 12:   # If the sum of the players card is less than 12, hit the deck
            card = drawCard()     # get a card with the function
            if card == 1:         # if you get an ACE 
                totalAces += 1    # Increment number of aces held
                card = 11         # give card 11 value 
                acePlayerHand = True  # Currently soft
            playerTotal += card   # Add card value to the overall player's sum
        
        if playerTotal > 21:      # If we go over 21 
            playerTotal -= 10     # decrement the player sum by 10 treating the ace like a 1
            if totalAces == 1:   # No longer will be using that Ace for it's 11 value
                acePlayerHand = False # Currently hard

        # if playerTotal >= 17 and playerTotal <= 21 and acePlayerHand == True:
        #     policyTwo = True


        dealerCard1 = drawCard() # Initialize the 2 Dealer's cards
        dealerCard2 = drawCard() 

    else: # default else 
        acePlayerHand = initialState[0] 
        playerTotal = initialState[1] 
        dealerCard1 = initialState[2] 
        dealerCard2 = drawCard() 

    state = [acePlayerHand, playerTotal, dealerCard1] # Initializing the game state 

                                                # Okay now it's the Dealer's turn, checking for soft/Hard
    if dealerCard1 == 1 and dealerCard2 != 1:   # If the dealer gets 1 Ace and one regular card
        dealerTotal += 11 + dealerCard2           # increment by ACE (11) plus the regular card
        aceDealerHand = True                  # Dealer has a usable ace
    elif dealerCard1 != 1 and dealerCard2 == 1:     # Same scenario but in case card 2 is an ACE
        dealerTotal += dealerCard1 + 11 
        aceDealerHand = True 
    elif dealerCard1 == 1 and dealerCard2 == 1: # In case both cards are ACEs 
        dealerTotal += 1 + 11                     # Only use one ACE in value 11
        aceDealerHand = True                  
    else:                                       # default Else just add up the sum of the cards 
        dealerTotal += dealerCard1 + dealerCard2 


    while True:                                 # Where the game starts for player
        if initialAction is not None:           # If there is an action to be initially done
            action = initialAction 
            initialAction = None                # Reloads it
        else:
            # Action based on the current sum of the player
            action = policyPlayerFn(acePlayerHand, playerTotal, dealerCard1) # we have the first dealer card cause we just assume the other face down one is a 10
            # Tracking the trajectory to see the performance 
        playerTrackRec.append([action, (acePlayerHand, playerTotal, dealerCard1)]) # Appends set action in correspondence to the Ace hand, player total, dealers first card
        
        # if policyTwo == True:
        #     action == STAND_GO
        #     break

        if action == STAND_GO: 
            break                                   # if Stand break from the while loop 
        playerTotal += drawCard()                      # Else to HIT

        if playerTotal > 21:                          # if player BUSTS goes over 21
            if acePlayerHand == True:             # if player has an Ace and can use it as a 1 instead of 11
                playerTotal -= 10                 # Make that soft Ace into a hard Ace 
                acePlayerHand = False             # No more usable ACE (11)
            else:
                return state, -1, playerTrackRec  # Else BUST player loses and gets a -1 

#################################################################

    while True: # Dealer's turn
        action = policyDealer[dealerTotal]
        if action == STAND_GO: 
            break                                   # if STAND then break from the while loop here
        dealerTotal += drawCard()                      # else HIT another card
        if dealerTotal > 21:                          # If dealer BUSTS
            if aceDealerHand == True:             # But has an ACE 
                dealerTotal -= 10                     # Treat the ACE as a 1 and not an 11
                aceDealerHand = False             # No longer usable ACE (11)
            else:
                return state, 1, playerTrackRec   # Dealer goes BUST returns a +1 for the player 



    if playerTotal > dealerTotal:                       # Now we can compare the sums of both Player & Dealer
        return state, 1, playerTrackRec           
    elif playerTotal == dealerTotal:                    # If same sum for both hands 
        return state, 0, playerTrackRec 
    else: 
        return state, -1, playerTrackRec          # If sum is not larger than dealer sum return -1



#############################################################33
## Monte Carlo #####


def monteCarlo(iterations): 
    games = 0
    moves = []
    aceCount = 0
    for i in range(0, iterations): 
        state, reward, _ = play(targetPolicyPlayer)
        if reward == -1:
            games += 1
        moves.append(state[0])
    aceCount = sum(moves)
    return games,aceCount



##########################################################333

# Printing the pie chart

totalGames = 1000000

losses,presentAce = monteCarlo(totalGames)
print(losses)
totalBust = totalGames - losses 
totalWins = totalGames - totalBust
absentAce = totalGames - presentAce

print(totalBust)
print(totalWins)

print(presentAce)
print(absentAce)



# Creating dataset
outcomes = ['Busts', 'Wins']

data = [totalBust, totalWins]

explode = (0.1, 0.0)
colors = ( "brown", "cyan")
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
ax.set_title("Blackjack Infinite Deck, Policy 4")

plt.show()

##################  Aces  ##############################################

outcomes2 = ['Ace unavailable/hard', 'Ace gone soft']
data = [absentAce, presentAce]

explode = (0.1, 0.0)
colors = ( "yellow", "cyan")
wp = { 'linewidth' : 1, 'edgecolor' : "green" }
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)

fig, ax = plt.subplots(figsize =(10, 7))

wedges, texts, autotexts = ax.pie(data, 
                                  autopct = lambda pct: func(pct, data),
                                  explode = explode, 
                                  labels = outcomes2,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 160,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))
  

ax.legend(wedges, outcomes2,
          title ="Blackjack Soft Ace Usage",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))

plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Blackjack Infinite Deck -- Soft Aces Policy 4")

plt.show()
