"""Core Game Engine"""

from config import DICTIONARY

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

    def seed(self, path:str):
        """Read Dictionary Text File
        
        Arguments:
            path {str} : Path to text file

        Returns:
            None
        """
        dict_file = open(path, 'r')
        self.dictionary = tuple([w.strip() for w in dict_file.readlines()])

    def pick(self, indices:list):
        """Get List of Words from Dictionary
        
        Arguments:
            indices {list} : List of indices {int}
            dictionary {tuple}
        
        Returns:
            {list} : List of words
        """
        words = []
        for i in indices:
            if i < len(self.dictionary):
                words.append(self.dictionary[int(i)])
        return words


    def search(self, anagram:str):
        """Find Words from Dictionary Using an Anagram
        
        Arguments:
            anagram {str}
            dictionary {tuple}
        
        Returns:
            {list} : List of words 
        """
        matches = []
        for word in self.dictionary:
            if sorted(word) == sorted(pattern):
                matches.append(word)
        return matches

    def combine(self, words:list):
        """Create a Letter Pool from Words
        
        Arguments:
            words {list}

        Returns:
            {list} : Letter pool
        """
        self.pool = []
        for word in words:
            word = list(word)
            for char in self.pool:
                if char in word:
                    word.remove(char)
            self.pool += word
        return self.pool

    def check(self, word:str):
        """Check if a Word from a Dictionary can be formed
        using the Letters from a Pool
        
        Arguments:
            word {str} : Word to check
            pool {list} : Letter pool
            dictionary {tuple}
        
        Returns:
            {bool}
        """
        if word in self.dictionary:
            for char in set(word):
                if list(word).count(char) > self.pool.count(char):
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