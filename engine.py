"""Core Game Engine"""

from config import DICTIONARY
from random import sample, shuffle

class Engine:
    def __init__(self, path = ''):
        """Initialize Engine, load Dictionary from Path if passed
        else, load from default source

        Arguments:
            path {str} : Path to dictionary file

        Returns:
            None
        """
        if bool(path):
            self.seed(path)
        else:
            self.seed(DICTIONARY)

        self.pool = []
        self.picked = []
        self.matchable = []

    def seed(self, path:str):
        """Read Dictionary Text File
        
        Arguments:
            path {str} : Path to text file

        Returns:
            None
        """
        dict_file = open(path, 'r')
        self.dictionary = tuple([w.strip() for w in dict_file.readlines()])

    def pick(self, number:int = 3, indices:list = []):
        """Get List of Words from Dictionary
        
        Arguments:
            number {int} : Number of Items
            indices {list} : List of Indices

        Returns:
            {list} : List of words
        """
        if len(indices):
            self.picked = []
        
            for i in indices:
                self.picked.append(self.dictionary[i])
        else:
            self.picked = sample(self.dictionary, number)

        return self.picked

    def search(self, source = ''):
        """Find Anagrams from Dictionary

        Arguments:
            source {str|list} : Characters to user
        
        Returns:
            {list} : List of words 
        """
        matchable = []

        if len(source):
            pool = source
        else:
            pool = self.pool
            self.matchable = matchable

        for word in self.dictionary:
            if sorted(word) == sorted(pool):
                matchable.append(word)

        return matchable

    def combine(self, number:int = 3, words:list = []):
        """Create a Scrambled Character Pool

        Automatically calls pick() method
        
        Arguments:
            number {int} : Number of Items to Pick
            words {int} : List of Words

        Returns:
            {list} : Letter pool
        """
        pool = []

        if len(words):
            picked = words
        else:
            picked = self.pick(number)
            self.matchable = []
            self.pool = pool

        for word in picked:
            word = list(word)
            for char in pool:
                if char in word:
                    word.remove(char)
            pool += word
        shuffle(pool)

        return pool

    def check(self, word:str, pool = []):
        """Check if Word can be formed from Pool and exists in the Dictionary
        
        Arguments:
            word {str} : Word to check
            pool {list} : List of characters
        
        Returns:
            {bool}
        """
        if len(pool) == 0:
            pool = self.pool

        if word in self.dictionary:
            for char in set(word):
                if list(word).count(char) > pool.count(char):
                    return False
                    break
            return True
        else:
            return False

    def score(self, word:str):
        """Calculates the Score of a Word using Scrabble Points
        
        Arguments:
            word {str}
        
        Returns:
            {int}
        """
        scrabble = [
            (1, ['e', 'a', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u']),
            (2, ['d', 'g']),
            (3, ['b', 'c', 'm', 'p']),
            (4, ['f', 'h', 'v', 'w', 'y']),
            (5, ['k']),
            (8, ['j', 'x']),
            (10, ['q', 'z'])
        ]

        score = 0
        for char in word:
            for point, letters in scrabble:
                if char in letters:
                    score += point
        
        return score