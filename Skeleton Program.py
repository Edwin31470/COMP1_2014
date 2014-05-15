# Skeleton Program code for the AQA COMP1 Summer 2014 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.2 programming environment
# version 2 edited 06/03/2014


######test change#############


import random
import time
import pdb
import pickle


NO_OF_RECENT_SCORES = 20

ACE_HIGH = False
CARD_SAME_SKIP = False
NO_OF_LIVES = 3


class TCard():
  def __init__(self):
    self.Suit = 0
    self.Rank = 0


class TRecentScore():
  def __init__(self):
    self.Name = ''
    self.Score = 0
    self.Date = ""


class TSavedGame():
  def __init__(self):
    self.score = ''
    self.cardsPlayed = 0
    self.Date = ''


Deck = [None]
RecentScores = [None]
Choice = ''


def GetRank(RankNo):
  Rank = ''
  if RankNo in [1,14]: 
    Rank = 'Ace'
  elif RankNo == 2:
    Rank = 'Two'
  elif RankNo == 3:
    Rank = 'Three'
  elif RankNo == 4:
    Rank = 'Four'
  elif RankNo == 5:
    Rank = 'Five'
  elif RankNo == 6:
    Rank = 'Six'
  elif RankNo == 7:
    Rank = 'Seven'
  elif RankNo == 8:
    Rank = 'Eight'
  elif RankNo == 9:
    Rank = 'Nine'
  elif RankNo == 10:
    Rank = 'Ten'
  elif RankNo == 11:
    Rank = 'Jack'
  elif RankNo == 12:
    Rank = 'Queen'
  elif RankNo == 13:
    Rank = 'King'
  return Rank


def GetSuit(SuitNo):
  Suit = ''
  if SuitNo == 1:
    Suit = 'Clubs'
  elif SuitNo == 2:
    Suit = 'Diamonds'
  elif SuitNo == 3:
    Suit = 'Hearts'
  elif SuitNo == 4:
    Suit = 'Spades'
  return Suit
    

def SaveScores(RecentScores):
  with open("save_scores.txt", mode="w", encoding="utf-8")as savescores:
    for count in range(1,len(RecentScores)):
      savescores.write((RecentScores[count].Name) + "\n")
      savescores.write(str(RecentScores[count].Score) + "\n")
      savescores.write(str(RecentScores[count].Date) + "\n" )

            
def LoadScores():
  RecentScores = [None]
  try:
    with open("save_scores.txt", mode="r", encoding="utf-8") as my_file:
      try:
        for count in range(1,NO_OF_RECENT_SCORES+1):
          Score = TRecentScore()
          Score.Name = my_file.readline().rstrip("\n")
          Score.Score = int(my_file.readline().rstrip("\n"))
          Score.Date = my_file.readline().rstrip("\n")
          RecentScores.append(Score)
      except ValueError:
        print("There was an error.")
    return RecentScores
  except IOError:
    print("There is no file to load from.")  


def DisplayMenu():
  print()
  print('MAIN MENU')
  print()
  print('1. Play game (with shuffle)')
  print('2. Play game (without shuffle)')
  print('3. Display recent scores')
  print('4. Reset recent scores')
  print("5. Options Menu")
  print("6. Save Scores")
  print("7. Load Scores")
  print()
  print('Select an option from the menu (or enter q to quit): ', end='')


def DisplayOptions():
  print()
  print("OPTIONS MENU")
  print()
  print("1. Ace value")
  print("2. Card of same score")
  print()
  print('Select an option from the menu (or enter q to quit): ', end='')


def GetMenuChoice():
  Choice = input().lower()
  Choice = Choice[0]
  print()
  return Choice


def GetOptionChoice():
  Choice = input().lower()
  Choice = Choice[0]
  print()
  return Choice


def SetOptions(OptionChoice):
  if OptionChoice == "1":
    SetAceHighLow()
  elif OptionChoice == "2":
    SetSameScore()
  
def SetAceHighLow():
  global ACE_HIGH
  choice = input("Do you want ace to be high or low?(H/L): ").upper()
  if choice == "H":
    ACE_HIGH = True
  elif choice == "L":
    ACE_HIGH = False


def SetSameScore():
  global CARD_SAME_ENDS
  choice = input("Do you want getting the same card in a row to skip that guess?(Y/N): ").upper()
  if choice == "Y":
    CARD_SAME_ENDS = True
  elif choice == "N":
    CARD_SAME_ENDS = False 
 

def LoadDeck(Deck):
  global ACE_HIGH
  CurrentFile = open('deck.txt', 'r')
  Count = 1
  while True:
    LineFromFile = CurrentFile.readline()
    if not LineFromFile:
      CurrentFile.close()
      break
    Deck[Count].Suit = int(LineFromFile)
    LineFromFile = CurrentFile.readline()
    Deck[Count].Rank = int(LineFromFile)
    if ACE_HIGH == True and Deck[Count].Rank == 1:
      Deck[Count].Rank = 14
    Count = Count + 1


def CreateNewDeck():
  Deck = [None]
  for count1 in range(1,14):
    for count2 in range(1,5):
      card = TCard()
      card.Rank = count1
      card.Suit = count2
      Deck.append(card)
  return Deck


def ShuffleDeck(Deck):
  SwapSpace = TCard()
  NoOfSwaps = 1000
  for NoOfSwapsMadeSoFar in range(1, NoOfSwaps + 1):
    Position1 = random.randint(1, 52)
    Position2 = random.randint(1, 52)
    SwapSpace.Rank = Deck[Position1].Rank
    SwapSpace.Suit = Deck[Position1].Suit
    Deck[Position1].Rank = Deck[Position2].Rank
    Deck[Position1].Suit = Deck[Position2].Suit
    Deck[Position2].Rank = SwapSpace.Rank
    Deck[Position2].Suit = SwapSpace.Suit


def DisplayCard(ThisCard):
  print()
  print('Card is the', GetRank(ThisCard.Rank), 'of', GetSuit(ThisCard.Suit))
  print()


def GetCard(ThisCard, Deck, NoOfCardsTurnedOver):
  ThisCard.Rank = Deck[1].Rank
  ThisCard.Suit = Deck[1].Suit
  for Count in range(1, 52 - NoOfCardsTurnedOver):
    Deck[Count].Rank = Deck[Count + 1].Rank
    Deck[Count].Suit = Deck[Count + 1].Suit
  Deck[52 - NoOfCardsTurnedOver].Suit = 0
  Deck[52 - NoOfCardsTurnedOver].Rank = 0


def IsNextCardHigher(LastCard, NextCard, Choice, Score):
  global CARD_SAME_SKIP
  Higher = False
  if NextCard.Rank > LastCard.Rank:
    Higher = True
  elif NextCard.Rank == LastCard.Rank and CARD_SAME_SKIP == True and Choice == "h":
    Higher = True
    Score = Score - 1
  elif NextCard.Rank == LastCard.Rank and CARD_SAME_SKIP == True and Choice == "l":
    Higher = False
    Score = Score - 1
  return Higher, Score


def GetPlayerName():
  print()
  ChoiceValid = False
  while not ChoiceValid:
    PlayerName = input('Please enter your name: ')
    if PlayerName == "":
      print("You must enter something for your name!")
    else:
      ChoiceValid = True
  print()
  return PlayerName


def GetChoiceFromUser():
  Choice = input('Do you think the next card will be higher than the last card (enter h or l)? ').lower()
  while Choice == "":
    Choice = input("Invalid input. Do you think the next card will be higher than the last card (enter h or l)? ").lower()
  Choice = Choice[0]
  print(Choice)
  return Choice


def SaveGame(Deck, NoOfCardsTurnedOver, LastCard, NextCard):
  with open("deckCopy.txt",mode="w",encoding="utf-8") as my_file:
    for count in range(1,53):
      my_file.write(str(Deck[count].Suit) + "\n")
      my_file.write(str(Deck[count].Rank) + "\n")
  with open("save_game.txt",mode="w",encoding="utf-8") as my_file:
    my_file.write(str(NoOfCardsTurnedOver) + "\n")
    my_file.write(str(LastCard.Suit) + "\n")
    my_file.write(str(LastCard.Rank) + "\n")
    my_file.write(str(NextCard.Suit) + "\n")
    my_file.write(str(NextCard.Rank) + "\n")    


def LoadGame(NoOfCardsTurnedOver):
  Deck = [None]
  Card = TCard()
  with open("deckCopy.txt",mode="r",encoding="utf-8") as my_file:
    for count in range(1,53):
      Card.Suit = my_file.readline().rstrip("\n")
      Card.Rank = my_file.readline().rstrip("\n")

  with open("save_game.txt",mode="r",encoding="utf-8") as my_file:
    my_file.write(str(NoOfCardsTurnedOver) + "\n")
    my_file.write(str(LastCard.Suit) + "\n")
    my_file.write(str(LastCard.Rank) + "\n")
    my_file.write(str(NextCard.Suit) + "\n")
    my_file.write(str(NextCard.Rank) + "\n")  


def DisplayEndOfGameMessage(Score):
  print()
  print('GAME OVER!')
  print('Your score was', Score)
  if Score == 51:
    print('WOW! You completed a perfect game.')
  print()


def DisplayCorrectGuessMessage(Score):
  print()
  if CARD_SAME_SKIP == False:
    print('Well done! You guessed correctly.')
  print('Your score is now ', Score, '.', sep='')
  print()


def ResetRecentScores(RecentScores):
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    RecentScores[Count].Name = ''
    RecentScores[Count].Score = 0
    RecentScores[Count].Date = None


def BubbleSortScores(RecentScores):
  swapMade = True
  list_length = len(RecentScores)
  while swapMade:
    swapMade = False
    list_length = list_length - 1
    for Count in range(1,list_length):
      if RecentScores[Count].Score < RecentScores[Count+1].Score:
        temp = RecentScores[Count]
        RecentScores[Count] = RecentScores[Count+1]
        RecentScores[Count+1] = temp
        swapMade = True


def DisplayRecentScores(RecentScores):
  BubbleSortScores(RecentScores)
  print()
  print('Recent Scores: ')
  print()
  print("{0:<10} {1:<10} {2:<10}".format("Name","Score","Date"))
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    print("{0:<10} {1:<10} {2:<10}".format(RecentScores[Count].Name,RecentScores[Count].Score,RecentScores[Count].Date))
  print()
  print('Press the Enter key to return to the main menu')
  input()
  print()


def UpdateRecentScores(RecentScores, Score):
  addScore = input("Would you like your score to be added to the highscores? (y or n): ").lower()
  addScore = addScore[0]
  if addScore == "y":
    PlayerName = GetPlayerName()
    FoundSpace = False
    Count = 1
    while (not FoundSpace) and (Count <= NO_OF_RECENT_SCORES):
      if RecentScores[Count].Name == '':
        FoundSpace = True
      else:
        Count = Count + 1
    if not FoundSpace:
      for Count in range(1, NO_OF_RECENT_SCORES):
        RecentScores[Count].Name = RecentScores[Count + 1].Name
        RecentScores[Count].Score = RecentScores[Count + 1].Score
        RecentScores[Count].Date = RecentScores[Count + 1].Date
      Count = NO_OF_RECENT_SCORES
    RecentScores[Count].Name = PlayerName
    RecentScores[Count].Score = Score
    RecentScores[Count].Date = time.strftime("%d/%m/%Y")


def PlayGame(Deck, RecentScores):
  noOfLives = NO_OF_LIVES
  LastCard = TCard()
  NextCard = TCard()
  GameOver = False
  GetCard(LastCard, Deck, 0)
  DisplayCard(LastCard)
  NoOfCardsTurnedOver = 1
  while (NoOfCardsTurnedOver < 52) and (not GameOver):
    GetCard(NextCard, Deck, NoOfCardsTurnedOver)
    Choice = ''
    while (Choice != 'h') and (Choice != 'l') and (Choice != "s"):
      Choice = GetChoiceFromUser()
    DisplayCard(NextCard)
    NoOfCardsTurnedOver = NoOfCardsTurnedOver + 1
    Higher, NoOfCardsTurnedOver = IsNextCardHigher(LastCard, NextCard, Choice, NoOfCardsTurnedOver)
    if (Higher and Choice == 'h') or (not Higher and Choice == 'l'):
      DisplayCorrectGuessMessage(NoOfCardsTurnedOver - 1)
      LastCard.Rank = NextCard.Rank
      LastCard.Suit = NextCard.Suit
    elif Choice == "s":
      print(Deck)
      SaveDeck(Deck, NoOfCardsTurnedOver, LastCard, NextCard)
      SaveGame(NoOfCardsTurnedOver)
    else:
      if noOfLives > 0:
        noOfLives = noOfLives - 1
        print("You were wrong! You have {0} lives remaining".format(NO_OF_LIVES+1))
        NoOfCardsTurnedOver = NoOfCardsTurnedOver - 1
      elif noOfLives == 0:
        GameOver = True
  if GameOver:
    DisplayEndOfGameMessage(NoOfCardsTurnedOver - 2)
    UpdateRecentScores(RecentScores, NoOfCardsTurnedOver - 2)
  else:
    DisplayEndOfGameMessage(51)
    UpdateRecentScores(RecentScores, 51)

if __name__ == '__main__':
  for Count in range(1, 53):
    Deck.append(TCard())
  for Count in range(1, NO_OF_RECENT_SCORES + 1):
    RecentScores.append(TRecentScore())
  Choice = ''
  while Choice != 'q':
    DisplayMenu()
    Choice = GetMenuChoice()
    if Choice == '1':
      LoadDeck(Deck)
      SaveDeck(Deck)
      ShuffleDeck(Deck)
      PlayGame(Deck, RecentScores)
    elif Choice == '2':
      LoadDeck(Deck)
      PlayGame(Deck, RecentScores)
    elif Choice == '3':
      DisplayRecentScores(RecentScores)
    elif Choice == '4':
      ResetRecentScores(RecentScores)
    elif Choice == "5":
      DisplayOptions()
      OptionChoice = GetOptionChoice()
      SetOptions(OptionChoice)
    elif Choice == "6":
      SaveScores(RecentScores)
    elif Choice == "7":
      RecentScores = LoadScores()
    elif Choice == "8":
      CreateNewDeck()

