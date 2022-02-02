# CS1210: HW3 version 1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["awchristopher"])

######################################################################
# In this homework, you will build the internals for Boggle, a popular
# word game played with 16 6-sided dice. At the same time, in class we
# will develop the interactive user interface for Boggle, so that your
# solution, augmented with what we do in class, will give you a
# playable Boggle game. This assignment will also give us a chance to
# work on a system using the object-oriented paradigm.
#
# This is version 1 of the template file, which does not include the
# user interface.  I will periodically release updated versions, which
# you can then merge into your own code: still, be sure to follow the
# instructions carefully, so as to ensure your code will work with the
# new template versions that contain the GUI we develop in class.
#
# The rules of Boggle are available online. Basically, you will roll
# the dice and arrange them into a 4x4 grid. The top faces of the die
# will display letters, and your job is to find words starting
# anywhere in the grid using only adjacent letters (where "adjacent"
# means vertically, horizontally, and diagonally adjacent). In our
# version of Boggle, there are no word length constraints beyond those
# implicitly contained in the master word list.
#
# Although other dice configurations are possible, the original Boggle
# dice are (in no particular order):
D = ["aaeegn","abbjoo","achops","affkps","aoottw","cimotu","deilrx","delrvy",
     "distty","eeghnw","eeinsu","ehrtvw","eiosst","elrtty","himnqu","hlnnrz"]

# You will need sample() from the random module to roll the die.
from random import sample

######################################################################
# Boggle is the base class for our system; it is analogous to the
# Othello class in our implementation of that game.  It contains all
# the important data elements for the current puzzle, including:
#    Boggle.board = the current puzzle board
#    Boggle.words = the master word list
#    Boggle.solns = the words found in the current puzzle board
#    Boggle.lpfxs = the legal prefixes found in the current puzzle board
# Additional data elements are used for the GUI and scoring, which
# will be added in subsequent versions of the template file.
#
# Note: we will opt to use Knuth's 5,757 element 5-letter word list
# ('words.dat') from the Wordnet puzzle, but the 113,809 element list
# of words from HW1 ('words.txt') should also work just as easily.
#
class Boggle ():
    # This is the class constructor. It should read in the specified
    # file containing the dictionary of legal words and then invoke
    # the play() method, which manages the game.
    def __init__(self, input='words.dat'):
        self.board = [[] for i in range(4)]
        self.words = [ ]
        self.solns = set()
        self.lpfxs = set()
        pass

    # Printed representation of the Boggle object is used to provide a
    # view of the board in a 4x4 row/column arrangement.
    def __repr__(self):
        #From Othello code
        print('\n'.join([ ' '.join([j for j in self.board[i]]) for i in range(len(self.board))]) + '\n')

    # The readwords() method opens the file specified by filename,
    # reads in the word list converting words to lower case and
    # stripping any excess whitespace, and stores them in the
    # Boggle.words list.
    def readwords(self, filename):
        #Reads in all words from the file and puts them in self.words
        wordslst = open(filename, 'r')
        for line in wordslst:
            self.words.append(line.lower().strip())
        print('Read {} words'.format(len(self.words)))

    # The newgame() method creates a new Boggle puzzle by rolling the
    # dice and assorting them to the 4x4 game board. After the puzzle
    # is stashed in Boggle.board, the method also computes the set of
    # legal feasible word prefixes and stores this in Boggle.lpfxs.
    def newgame(self):
        ##List of boggle board, the first loop goes through every four dice, the second loops goes through four
        ##dice starting that the location of the first loop. Then takes a random letter from each die and appends it 
        ##to the corresponding index location/"row". (j//4 -> Ex. 4//4 = index location 1/ row 1, 8//4 = index location 2/ row 2
        for j in range(0,16,4):
            for i in range(j,j+4):
                lett=sample(D[i],1)
                self.board[j//4].append(lett[0].upper())
        ##Set of legal prefixes, loops through every word in self.words and then loops through every letter in each word,
        ##creating and adding it to the previous letter of that word, creating the list of prefixes
        for word in self.words:
            prefix = ''
            for pref in word:
                prefix += pref
                self.lpfxs.add(prefix)
        return self.board
       
    # The solve() method constructs the list of words that are legally
    # embedded in the given Boggle puzzle. The general idea is search
    # recursively starting from each of the 16 puzzle positions,
    # accumulating solutions found into a list which is then stored on
    # Boggle.solns.
        
    # The method makes use of two internal "helper" functions,
    # adjacencies() and extend(), which perform much of the work.
    def solve(self): 
        # Helper function adjacencies() returns all legal adjacent
        # board locations for a given location loc. A board location
        # is considered legal and adjacent if (i) it meets board size
        # constraints (ii) is not contained in the path so far, and
        # (iii) is adjacent to the specified location loc.
        def adjacencies(loc, path):
            allAdj = []
            ##Loops through every possible direction and if the location is not already in the path and 
            ##and is inbounds, the it adds that move to the list of possible moves
            for direction in ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)):
                adj=list(loc)
                adj[0] += direction[0]
                adj[1] += direction[1]
                if tuple(adj) not in path and adj[0] <= 3 and adj[1] <= 3 and adj[0] >= 0 and adj[1] >= 0: 
                    allAdj.append(tuple(adj))
            return(allAdj)            
                     
        # Helper function extend() is a recursive function that takes
        # a location loc and a path traversed so far (exclusive of the
        # current location loc). Together, path and loc specify a word
        # or word prefix. If the word is in Boggle.words, add it to
        # Boggle.solns, because it can be constructed within the
        # current puzzle. Otherwise, if the current prefix is still in
        # Boggle.lpfxs, attempt to extend the current path to all
        # adjacencies of location loc. To do this efficiently, a
        # particular path extension is abandoned if the current prefix
        # is no longer contained in self.lpfxs, because that means
        # there is no feasible solution to this puzzle reachable via
        # this extension to the current path/prefix.
        def extend(loc, path=[]):
            newPath = path + [loc] #Newpath is the path with the location added on, needed to do this so I could use the original path later.
            
            ##Loops through every possible move returned by adjacencies and if the move(i) has not already been made and is a legal prefix,
            ##then extend is called recursively with i(the move checked) and newPath(the path with the location from the previous call of extend
            ##added on).
            if self.extract(newPath) in self.lpfxs: #Base case, if the path is a legal prefix
                if self.extract(newPath) in self.words: # Base case, if the path is a legal word then it is added to self.solns
                    self.solns.add(self.extract(newPath))
                for i in adjacencies(loc, path):
                    if i not in path and self.extract(newPath) in self.lpfxs:
                        extend(i, newPath) #Recursive step
            elif self.extract(newPath) not in self.lpfxs:  
                pass      
            
        ##Loops through every location on the board, calling extend to get all possible legal words 
        for i in range(4):
            for j in range(4):
                extend((i,j))
        print('Path contains {} legal solutions.'.format(len(self.solns)))
        print('Cheat: {}'.format(self.solns))

    # The extract() method takes a path and returns the underlying
    # word from the puzzle board.
    def extract(self, path):
        wordChose = ''
        ##Loops through every location in the given path and adds the respective letter to the word.
        for j in path:
            wordChose += self.board[j[0]][j[1]]
        return(wordChose.lower())

    # The checkpath() method takes a path and returns the word it
    # represents if the path is legal (i.e., formed of distinct and
    # sequentially adjacent locations) and realizes a legal word,
    # False otherwise.
    def checkpath(self, path): 
        ##Loops through the path and checks if it is a legal word/move. 
        ##If it is not a legal word/move it is caught and returns False, if it is a legal word, the word is returned.
        for j in range(len(path)-1):
            i = j + 1
            if path[j][0] >= 0 and path[j][0] <= 3 and path[j][1] >= 0 and path[j][1] <= 3 and path[i][0] >= 0 and path[i][0] <= 3 and path[i][1] >= 0 and path[i][1] <= 3 and len(path[j]) <= 6 and len(path[i]) <= 6:
                if path[j] != path[i] and (int(path[j][0]) - int(path[i][0])) >= -1 and int(path[j][0])-int(path[i][0]) <= 1 and (int(path[j][1]) - int(path[i][1])) >= -1 and int(path[j][1])-int(path[i][1]) <= 1 and path[j] not in path[j+1:]:
                    pass
                else:
                    print("Illegal path. Try again!")
                    return False
            else:
                print("Illegal path: Try again!") 
                return False
            
        if self.extract(path) in self.solns:
            return(self.extract(path))
        else:
            print("Unrecognized word: {}".format(self.extract(path)))
            print("Try again")
            return False
           
    # The round() method plays a round (i.e., a single puzzle) of
    # Boggle. It should return True as long as the player is willing
    # to continue playing additional rounds of Boggle; when it returns
    # False, the Boggle game is over.
    #
    # Hint: Look to HW1's round() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def rounds(self):
        # The recover() helper function converts a list of integers
        # into a path. Thus '3 2 2 1 1 2 2 3' becomes [(3, 2), (2, 1),
        # (1, 2), (2, 3)].
        def recover(path):
            ##Loops through the path without the white spaces by 2 and appends the current number and the following number to a tuple,
            ##creating the path.
            newPath = []
            for x in range(0,len(path.split()),2):
                newPath.append((int(path.split()[x]),int(path.split()[x+1])))
            return(newPath)   
        print("Input 'r1 c1 r2 c2...'; '/'=display, ':'=show, '+'=new puzzle; ','=quit")
        print("       where 'r1 c1 r2 c2...' specifies a path as a series of row,col coordinates.")
        
        ##These functions are called to start the game
        self.readwords('words.dat')
        self.newgame()
        self.solve()
        self.__repr__()
        currentWords = []
        constant = 0
        
        ##Loops continuously through this since constant never changes. Checks the users input and 
        ##if it is a single character then it does the corresponding task('/',':',',','+')
        while constant == 0:
            userIn = input()
            if len(userIn) == 1:
                if userIn == '/':
                    self.__repr__()
                elif userIn == ':':
                    print('{} word(s) found so far:'.format(len(currentWords)))
                    for i in currentWords:
                        print(i)
                elif  userIn == ',':
                    print('You found {} out of {} possible words.'.format(len(currentWords),len(self.solns)))
                    return False
                elif userIn == '+':
                    currentWords.clear()
                    self.solns.clear()
                    self.board = [[],[],[],[]]
                    self.newgame()
                    self.solve()
                    self.__repr__()                
                else:
                    print('Invalid input.')
                    
            ##If the users input is more than 1 character, then it reaches this. and calls recover and 
            ##checkpath. If the word is legal and hasn't already been used then it is added to the 
            ##list of current words.
            else:
                pathway = recover(userIn)
                if self.checkpath(pathway):
                    if self.extract(pathway) in currentWords:
                        print('That word has already been used, try again!')
                    elif self.extract(pathway) not in currentWords:
                        currentWords.append(self.extract(pathway))
                        print('Correct! You found {}!'.format(self.extract(pathway)))
                        if len(currentWords) == len(self.solns):
                            print("Congratulations! You found all {} words!".format(len(self.solns)))

    # The play() method when invoked initiates a sequence of
    # individual Boggle rounds by repeatedly invoking the rounds()
    # method as long as the user indicates they are interested in
    # playing additional puzzles.
    #
    # Hint: Look to HW1's play() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def play(self):
        ##Continuously loops through self.rounds until it returns False, in that case, the game is over.
        print('Welcome to Boggle!')
        while self.rounds() == True:
            pass
        else:
            print('Game over.')
            
######################################################################
if __name__ == '__main__':
    Boggle()
