#! /usr/bin/python

## Call Bridge				Tue May 10,10:03 AM
###########################################################
# In this game the user plays a game of Call Bridge against
# three computer-generated artificial players.
###########################################################
A=14			
J=13
Q=12							
K=11							
card_ranks=(2,3,4,5,6,7,8,9,10,J,Q,K,A)			
card_suits=('spades','hearts','diamonds','clubs')
hr= "-----------------------------------------------------"
#----------------------------------------------------------
# Header
print hr
print "Call Bridge <<<<<>>>> syed ibtisam tauhidi ------- ||"
print hr
#----------------------------------------------------------

# This holds the rank and suit of an individual card ##
class Card:
        def __init__(self,rank,suit):
                self.suit=suit
		self.rank=rank
		if self.suit == 'spades':
                        self.symbol='Spades'
                elif self.suit == 'hearts':
                        self.symbol='Hearts'
                elif self.suit == 'diamonds':
                        self.symbol='Diamonds'
                elif self.suit == 'clubs':
                        self.symbol='Clubs'          

	def __str__(self): # eg. '3 of Spade'
		if self.rank==14:
			return ("A of " + self.symbol)
		if self.rank==13:
			return ("K of " + self.symbol)
		if self.rank==12:
			return ("Q of " + self.symbol)
		if self.rank==11:
			return ("J of " + self.symbol)
		else:
			res=str(self.rank) + " of " + self.symbol		
			return (res)
#----------------------------------------------------------
# This holds all 52 cards used in the games. This is also used
# to suffle the deck before distributing the cards.     
class Deck:
	deck=[]			# This creates 52 unique cards
	def __init__(self):	# and puts them in deck list.	 
		for rank in card_ranks:	
                        for suit in card_suits:
                            self.deck.append(Card(rank,suit))

	def __str__(self):
		for card in self.deck:
			print str(i)+" : "+str(card)
		return ""

	def suffle(self):	# This is used to suffle the cards
		import random	# using Python's random module.
		nCards=len(self.deck)
		for i in range (nCards):
			j=random.randrange(i,nCards)
			self.deck[i],self.deck[j]=self.deck[j],self.deck[i]

	def get_card(self,index):
		return self.deck[index]
#----------------------------------------------------------
# Returns 1 if card1 wins against card2
# Returns 0 if card1 loses against card2
# (else returns 2 -- should NEVER happen.)
def cb_compare(card1,card2):		
	if card1.suit=='spades':	
		if card2.suit=='spades':
			if card1.rank>card2.rank:
                                return 1
                        elif card1.rank<card2.rank:
                                return 0
                        else:
                                return 2
                elif card2.suit!='spades':
                        return 1
                else:
                        return 2
        elif card1.suit!='spades':
                if card2.suit=='spades':
                        return 0
                elif card2.suit!='spades':
                        if card1.suit==card2.suit:
                                if card1.rank>card2.rank:
                                        return 1
                                elif card1.rank<card2.rank:
                                        return 0
                                else:
                                        return 2
                        elif card1.suit!=card2.suit:
                        # This depends on who made the first
                        # deal. If card1's dealt later, it loses.
                        # This should be properly handled in
                        # function call.
                                return 0
                        else:
                                return 2
        else:
                return 2
#----------------------------------------------------------
# This is used to return a count for the estimated call
# before the game starts. Minimum allowed is 2.
def cb_call_count(hand):	
	count=0		# This is a basic 'safe' algo.
	extra=0		# Needs work.
	for card in hand:	 
		if card.suit=='spades':
			if card.rank>10:
				count+=1
			elif card.rank>3:
				extra+=1
		elif card.rank>11:
			count+=1
	count=int(count+(extra/3))
	if count<2:
		return 2	# Min
	else:
		return count
#----------------------------------------------------------
# This is the board on which each round will be played.
# Unlike the wooden casino boards, this one is just a 1D list.
class Board:
	board=[]
	def __str__(self):
		for card in self.board:
			print str(i)+" : "+str(card)
		return ""
	def add_card(self,rank,suit): 
		self.board.append(Card(rank,suit))
	def get_top(self):
	# This function considers the first card to be top
	# unless replaced by higher-ranked card of same suit
	# or by a spade (i.e. if the top is not a spade.)
		top=self.board[0]
		for card in self.board:
			if card.suit=='spades':
				if top.suit!='spades':
					top=card
				elif card.rank>top.rank:
					top=card
			elif card.suit==top.suit:
				if card.rank>top.rank:
					top=card
		return top
	def clear(self):
		del(self.board[0])
		del(self.board[0])
		del(self.board[0])
		del(self.board[0])
#----------------------------------------------------------
def Dealer(hand,board_top):
	# This function is used by bots to deal its card.
	result=[]
	for card in hand:
		result.append(cb_compare(card,board_top))
	contenders=[]	
	i=0	
	for current in result:
		if current==1:
			contenders.append(hand[i])
		i+=1
	del(result)
	if len(contenders)<1:
		del(contenders)
		return 0
	else:	
		available=0
		if board_top.suit!='spades':
			for card in contenders:
				if card.suit==board_top.suit:
					available=1
		if available==1:
			j=0
			while j<len(contenders):
				if contenders[j].suit=='spades':
					del(contenders[j])
					j=0
				else:
					j+=1
		low_index=Deal(contenders,board_top)
		# This is used by the dealer to figure out which
		# card to deal.
		card0=contenders[low_index]
		i=0
		while card0!=hand[i]:
			i+=1
		return i
#----------------------------------------------------------
def Deal(hand,board_top):
	# It returns the index of the weakest
	# contending card.
	small=0
	if len(hand)==1:	
		return small
	else:
		i=1
		while i<len(hand):			
			res=cb_compare(hand[i],hand[small])			
			if res==0:
				small=i
			i+=1
		return small
#----------------------------------------------------------
def ScoreCount(won,call):
	won=int(won)
	call=int(call)	
	if call<won:
		return -call*10
	elif won>=2*call:
		return -call*10
	else:
		score=(won-call)+(call*10)
		return score
#----------------------------------------------------------
def ask(question):
	try:
		answer=''
		while answer=='':
			answer=raw_input(question)		
	except ValueError:
		answer=ask(question)
	except IndexError:
		answer=ask(question)
	else:
		return answer
#----------------------------------------------------------
def ask_count(PName,man):
	answer=ask(PName)
	if answer.isdigit():
		if answer<len(man):
			return answer
	else:
		return ask_count(PName,man)
#----------------------------------------------------------
class UnitDealRecord:
	def __init__(self,who,rank,suit):
		self.who=who
		self.rank=rank
		self.suit=suit
#----------------------------------------------------------
def HPrint(hand): # This prints index+1.
	i=0	  # Remember to substract.
	for card in hand:
		print str(i+1) + "\t:\t" + str(card)
		i+=1
#----------------------------------------------------------
def CB(PName):

	# Initialization
	print hr
	print "Your Cards :"
	HPrint(man)
	print hr
	bot1_count=cb_call_count(bot1)
	bot1_won=0
	print "@_Johud: I'll go for " + str(bot1_count)
	bot2_count=cb_call_count(bot2)
	bot2_won=0
	print "@_Eggless: I'm in at " + str(bot2_count)
	bot3_count=cb_call_count(bot3)
	bot3_won=0
	print "@_DK: Give me " + str(bot3_count)
	man_count=ask("\n"+PName+": MY CALL ")
	man_won=0
	new_board=Board()

	# Loop for 13 rounds
	step_count=0
	while step_count<13:
		print "\n"
		print "Score :"
		print "JOH:"+str(bot1_won)+"/"+str(bot1_count)+ "\tEGG:"+str(bot2_won)+"/"+str(bot2_count)	
		print "DK:"+str(bot3_won)+"/"+str(bot3_count)+ "\t"+PName+":"+str(man_won)+"/"+str(man_count)+"\n"
		print hr
		print HPrint(man) 
		print hr
		choice=ask("CARD KEY: ")
		intChoice=int(choice)
		intChoice-=1	# See HPrint(hand)
		card=man[intChoice]
		del(man[intChoice])
		print "@"+PName+" >>> " + str(card)	
		new_board.add_card(card.rank,card.suit)
		card_man=str(card)	
		
		new_board_top1=new_board.get_top()
		bot1_index=Dealer(bot1,new_board_top1)
		new_board.add_card(bot1[bot1_index].rank,bot1[bot1_index].suit)
		print "@_Johud >>> " + str(bot1[bot1_index])	
		card_bot1=str(bot1[bot1_index])
		del(bot1[bot1_index])
	
		new_board_top2=new_board.get_top()
		bot2_index=Dealer(bot2,new_board_top2)
		new_board.add_card(bot2[bot2_index].rank,bot2[bot2_index].suit)
		print "@_Eggless >>> " + str(bot2[bot2_index])	
		card_bot2=str(bot2[bot2_index])	
		del(bot2[bot2_index])
	
		new_board_top3=new_board.get_top()
		bot3_index=Dealer(bot3,new_board_top3)
		new_board.add_card(bot3[bot3_index].rank,bot3[bot3_index].suit)
		print "@_DK>>> " + str(bot3[bot3_index])	
		card_bot3=str(bot3[bot3_index])
		del(bot3[bot3_index])
	
		alphaCard=str(new_board.get_top())
		if alphaCard==card_man:
			man_won+=1
		elif alphaCard==card_bot1:
			bot1_won+=1
		elif alphaCard==card_bot2:
			bot2_won+=1
		elif alphaCard==card_bot3:
			bot3_won+=1
		print "Board winner is : " + str(alphaCard)
		step_count+=1
		new_board.clear()
	print "Final Score :"
	print "JOH:"+str(bot1_won)+"/"+str(bot1_count)+ "\tEGG:"+str(bot2_won)+"/"+str(bot2_count)	
	print "DK:"+str(bot3_won)+"/"+str(bot3_count)+ "\t" + PName + ":" + str(man_won)+"/"+str(man_count)+"\n"
	print hr
	print hr

	Score_man=ScoreCount(man_won,man_count)
	Score_bot1=ScoreCount(bot1_won,bot1_count)
	Score_bot2=ScoreCount(bot2_won,bot2_count)
	Score_bot3=ScoreCount(bot3_won,bot3_count)
	return (Score_man,Score_bot1,Score_bot2,Score_bot3)
# <----------- Function and Class Ends Here--------------->
# <----------- Main Begins ------------------------------->
deck=Deck()	# A deck of card
deck.suffle()	# suffled fairly.

man=[]		# The player's hand
bot1=[]		# and those of the bots.
bot2=[]
bot3=[]

# This is how a deck of suffled cards is actually
# distributed. Algorithm is not a concern.
i=0		
while i<52:    
	man.append(deck.get_card(i))
	bot1.append(deck.get_card(i+1))
	bot2.append(deck.get_card(i+2))
	bot3.append(deck.get_card(i+3))
	i+=4
#----------------------------------------------------------
PName=ask("@Dealer : What's your name, kid? ")
Score=CB(str(PName))
print Score
############################################################
# Syed Ibtisam Tauhidi | facebook.com/ibtisam.tauhidi ######
# ####################################################### ##

# This file: cb-core.py

# To play in console download IDLE from www.python.org. Open
# this file in IDLE (Programs > IDLE > CTRL+O) & press F5.

# In any Linux/Unix/Mac shell, if you have Python installed, 
# (which you probably have - you can check using 'type python')
# go to the directory in which this file is saved and just 
# type './cb-core.py'. Even the console-based UI is friendly.

# Other files: cb-tkinter.py <- The GUI