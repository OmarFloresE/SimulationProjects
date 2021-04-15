///////////////////////////////////////////
//      Omar Flores Estrada     //////////
//      CSCI 154                //////////
//      Team Syntax Terror      //////////
//      4.8.2021               //////////
///////////////////////////////////////////
#include<iostream>
#include<string>
#include<ctime>
#include<vector>
#include<cstdlib>
using std::vector;
using std:: string;
// So far I have mostly done a lot of data abstraction and representation. 
// I still need to workout the basics of the game (Blackjack) logic.

enum Rank {ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE};
enum Suit {SPADES, HEARTS, DIAMONDS, CLUBS};

struct Card 
{
    Rank rank;
    Suit suit;
    int num_suits = 4;
    int num_ranks = 13;
};

// Deck uses cards, and we can change the card type without having to change deck type
struct Deck
{
    vector<Card> cards;
    string card_back;
    int max_deck_size = 52;
};

struct Player
{
    vector<Card> hand;
    string name; 
    int score;
};


struct Game 
{
    vector<Player> players;
    Deck deck;
    int num_players = 2;
    int num_cards_per_hand = 2;
    int twenty_one = 21; 
};

// Prototyping my functions // 
void initialize(Deck&);
void print_deck(const Deck&);
void print_card(const Card&);
void shuffle(Deck&);
bool deal_cards(Game&);
void print_hand(const vector<Card>&);
void initialize(Game&);
void add_players(Game&);
void print_game(const Game&); // const because when we print we don't change anything


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

    Game blackjack;
    initialize(blackjack);
    deal_cards(blackjack);
    print_game(blackjack);

    std::cout << "\n--- Compiled ---\n";
    return 0;
}

void initialize(Deck& deck)
{
    Card card;
    for(int suit = 0; suit< card.num_suits; suit++)
    {
        for(int rank = 0; rank < card.num_ranks; rank++)
        {
            card.suit = Suit(suit);
            card.rank = Rank(rank);
            deck.cards.push_back(card);
        }
    }
}

void print_deck(const Deck& deck)
{
    for(Card c : deck.cards)
    {
        print_card(c);
    }
}

void print_card(const Card& card)
{
    string rank;
    string suit;
    if (card.rank == 0) { rank = "One"; }
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
        return false;
    }
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

void print_hand(const vector<Card>& hand)
{
    for (Card c : hand)
    {
        print_card(c);
    }
}

void initialize(Game& game)
{
    // Everything is compartmentalized even add_players, I'll add more mechanics later
    initialize(game.deck);
    shuffle(game.deck);
    add_players(game);
}

void add_players(Game& game) 
{
    for (int i = 0; i < game.num_players; i++)
    {
        Player new_player;
        game.players.push_back(new_player);
    }
}

void print_game(const Game& game)
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