////////////////////////////////////////////
//      Omar Flores Estrada     //////////
//      CSCI 154                //////////
//      Team Syntax Terror      /////////
//      4.8.2021               //////////
///////////////////////////////////////////
#include<iostream> // input output
#include<string> // using string variables
#include<ctime>  // rand
#include<vector> // vectors for the struct
#include<cstdlib> // for the rand() function
using std::vector;
using std:: string;
// So far I have mostly done a lot of data abstraction and representation. 
// I still need to workout the basics of the game (Blackjack) logic.

// Enumeration to represent the various card types in a deck.
enum Rank {ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE};
enum Suit {SPADES, HEARTS, DIAMONDS, CLUBS};

// Going to use struct first then experiment with class when I'm done
struct Card // My user defined data type, a combo of various different data elements
{
    Rank rank; // a variable from the enum
    Suit suit;
    int num_suits = 4; // max number of types 
    int num_ranks = 13;
};

// Deck uses cards vector, and we can change the card type without having to change deck type
struct Deck
{
    vector<Card> cards; // our vector of cards in a deck
    int max_deck_size = 52; // there are 52 cards in a standard deck for blackjack
};

struct Player // a struct for player which holds elements such as score and vector of cards
{
    vector<Card> hand; 
    string name; // Player & Dealer
    int sum = 0;
};

struct Game // Struct of Game that brings everything together, encapsulation of data
{
    vector<Player> players; // how many players are in a game
    Deck deck; 
    int num_players = 2; // 2 players in blackjack as of now
    int num_cards_per_hand = 2; // start off with 2 cards
    int twenty_one = 21;  // the goal is to reach 21 or as close as you can
};

// Prototyping my functions // 
void initialize(Deck&); // We want to use a lot of pass by reference to maintain elements
void print_deck(const Deck&); // Prints the whole deck
void print_card(const Card&); // Prints single card, good for reusability
void shuffle(Deck&); // Shuffles by using rand() function, could modify later with better shuffle
bool deal_cards(Game&); // Deals the 2 cards to each player
void print_hand(const vector<Card>&); // prints the cards in each players hand
void initialize(Game&); // Starts the game and encapsulates other functions 
void add_players(Game&); // Creates and adds players to player vector
void print_game(const Game&); // const because when we print we don't change anything, prints game status
void play(Game&);

int get_score(Card&); // Function to get the total in every players hand 
int get_total(vector<Card>&);


int main()
{
    // Deck my_deck;
    // shuffle(my_deck);
    // print_deck(my_deck);
    // vector<Card> hand_1;
    // vector<Card> hand_2;
    // print_hand(hand_1);
    // std::cout<<'\n';
    // print_hand(hand_2);
    // print_deck(my_deck);

    Game blackjack; // declare blackjack from game struct
    //initialize(blackjack); 
    // deal_cards(blackjack);
    // print_game(blackjack);
    play(blackjack);
    std::cout << "\n--- Compiled ---\n";
    return 0;
}

void initialize(Deck& deck) // Initializes the deck for the game to begin
{
    Card card; // Card vector 
    for(int suit = 0; suit< card.num_suits; suit++) // nested for loop to distribute the card values
    {
        for(int rank = 0; rank < card.num_ranks; rank++)
        {
            card.suit = Suit(suit);
            card.rank = Rank(rank);
            deck.cards.push_back(card); // push back cards into the vector, could use a stack later?
        }
    }
}

void print_deck(const Deck& deck) // prints the whole deck through a loop and reusable function
{
    for(Card c : deck.cards)
    {
        print_card(c);
    }
}

void print_card(const Card& card) // Prints cards attributes, could maybe use a switch statement?
{
    string rank;
    string suit;
    if (card.rank == 0) { rank = "One"; } // if statements to assign string values
    else if (card.rank == 1) { rank = "Two"; }
    else if (card.rank == 2) { rank = "Three"; }
    else if (card.rank == 3) { rank = "Four"; }
    else if (card.rank == 4) { rank = "Five"; }
    else if (card.rank == 5) { rank = "Six"; }
    else if (card.rank == 6) { rank = "Seven"; }
    else if (card.rank == 7) { rank = "Eight"; }
    else if (card.rank == 8) { rank = "Nine"; }
    else if (card.rank == 9) { rank = "Ten"; }
    else if (card.rank == 10) { rank = "Jack (10)"; }
    else if (card.rank == 11) { rank = "Queen (10)"; }
    else if (card.rank == 12) { rank = "King (10)"; }
    else{ rank = "Ace (1 or 11)"; }

    if (card.suit == 0) { suit = "Spades"; }
    else if (card.suit == 1) { suit = "Hearts"; }
    else if (card.suit == 2) { suit = "Diamonds"; }
    else if (card.suit == 3) { suit = "Clubs"; }

    std:: cout<< rank << " of " << suit << '\n';
}

// Create a deck that is empty and randomly pick from an already made deck in order to shuffle
void shuffle(Deck& deck)
{
    Deck shuffled;
    while(!deck.cards.empty())
    {
        // size_t because it's an index variable
        size_t rand_index = rand() % deck.cards.size(); 
         // add selected rand card to shuffled deck
        shuffled.cards.push_back(deck.cards[rand_index]);
        // syntax of the erase method, begin place and then add place you want to erase
        deck.cards.erase(deck.cards.begin() + rand_index);
    }
    deck = shuffled;
}

bool deal_cards(Game& game) 
{
    if (game.deck.cards.size() < game.num_players * game.num_cards_per_hand) 
    {
        // If there isn't enough cards left base case
        return false;
    }
    // nested for loop to assign # of cards to each player
    for (int card = 0; card < game.num_cards_per_hand; card++)
    {
        for (int player = 0; player < game.num_players; player++)
        {
            // game has players and each player has a hand which is a vector, which 
            // gets pushed back a card from the top of the deck [0]
            // then we erase/remove top card of the deck 
            game.players[player].hand.push_back(game.deck.cards[0]);
            game.deck.cards.erase(game.deck.cards.begin());
        }
    }
    return true;
}

void print_hand(const vector<Card>& hand) // similar to print deck but different arguments 
{
    for (Card c : hand)
    {
        print_card(c); // look at this awesome reusable function again
    }
}

void initialize(Game& game) // initializes the game and calls upon all neccessary functions
{
    // Everything is compartmentalized even add_players, I'll add more mechanics later
    initialize(game.deck);
    shuffle(game.deck);
    add_players(game);
}

void add_players(Game& game) // adds players to the game, used in initialization for game
{
    for (int i = 0; i < game.num_players; i++)
    {
        Player new_player;
        game.players.push_back(new_player);
    }
}

void print_game(const Game& game) // Maybe convert everything to strings to send to a GUI
{
    std::cout<<"________________________________\n";
    for (int player = 0; player < game.num_players; player++)
    {
        print_hand(game.players[player].hand);
        std::cout<<"-------------------\n";
    }
    std::cout<<"________________________________\n";
    print_deck(game.deck);
}

int get_score(Card& card)
{  // function to return total from one card, lets make a total of whole hand now using this
    int sum;
    if (card.rank == 0) {sum+=1; } // if statements to assign string values
    else if (card.rank == 1) {sum+=2; }
    else if (card.rank == 2) {sum+=3; }
    else if (card.rank == 3) {sum+=4; }
    else if (card.rank == 4) {sum+=5; }
    else if (card.rank == 5) {sum+=6; }
    else if (card.rank == 6) {sum+=7; }
    else if (card.rank == 7) {sum+=8; }
    else if (card.rank == 8) {sum+=9; }
    else if (card.rank == 9) {sum+=10; }
    else if (card.rank == 10) {sum+=10; } // Jack
    else if (card.rank == 11) {sum+=10; } // Queen
    else if (card.rank == 12) {sum+=10; } //King
    else { sum += 11; } // Ace
    return sum;
}

int get_total(vector<Card>& hand) // similar to print deck but different arguments 
{
    int total = 0;
    for (Card c : hand)
    {
        total += get_score(c);// look at this awesome reusable function again
    }
    return total;
}

////////////////////////////////////////////

void play(Game& game)
{
    initialize(game);
    deal_cards(game);

    bool game_over = false;
    size_t dealer = 0;

    while(!game_over)
    {   
        std::cout<< "Dealer's hand: \n";
        print_hand(game.players[dealer].hand);
        int dealer_total = get_total(game.players[dealer].hand);
        std::cout<< "Dealer's total: " << dealer_total << '\n';

        std::cout<< "Your hand: \n";
        size_t player = (dealer + 1) % game.num_players;
        print_hand(game.players[player].hand);
        int player_total = get_total(game.players[player].hand);

        std::cout<< "Player's total: " << get_total(game.players[player].hand) << '\n';

        std::cout<<"\n";

        if (dealer_total > player_total)
        {
            std::cout<<"\nThe house wins unfortunately"; 
        }
        else
        {
            std::cout<<"\nPlayer wins!";
        }

        game_over = true;
    }
}