class Judge:
    """
    Intended use: Three search
    Class to create Judge objects that allows to check the how many mono and rainbow words can be spelled.
    
    Attributes
    ----------
    alphabet:list 
        a list containing the character letters in the alphabet
        
    words:list
        a list of strings, where each item is a word of up to 6 characters.
    
    Methods
    -------
    is_rainbow(word:list, letters:list, cube_record:list, color:int)->bool
        Checks recursively if a given word is a rainbow word based on a letter permutation
        and returns True or False
        
    is_mono(word:list, letters:list)->int
        Checks if a given string is a mono word given a color-combination. returns
        the applicable color, or None if it's not possible.
    
    analyze_together(permutation:list, generate_dict:bool=False)->list
        Counts how many mono and rainbow words are there in the words list, based on the combination.
        It returns a list with stats from the total words
        
    analyze_mono(letters:list)->list
        only counts how many mono words can be spelled given a permutation, and returns the total
        
    analyze_rainbow(letters:list)->list
        only counts how many rainbow words can be spelled given a permutation, and returns the total
        
    
    """
    def __init__(self, alphabet:list, words:list):
        """
        Contructor that initializes the alphabet, words and best attributes
        """
        self.alphabet = alphabet
        self.words = words
        #We could add something like best_mono, best_rainbow.
        #which can be useful if we want to use multi threading
    
      
    def is_rainbow(self,word:list, letters:list, cube_record:list, color:int=0)->bool:
        """
        Checks recursively if a given word is a rainbow word based on a letter combination
        and return True or False respectively.
        
        Attributes
        ----------
        word:list
            A list representing a word, each item is a letter in said word.
            i.e ['s','l','o','g','a','n']
            
        letters:list
            a list containing letters, where every letter in the alphabet appears at least once
            
        cube_record:list
            it should be an empty list, that will keep track of what cubes were the chosen colors taken from
            
        color:int
            represent which out of the six colors are we considering at a given level of recursion
            default value is zero
        """
        
        #base case is True when level=6
        #we only care about levels 0 through 5
        if(color == 6):
            #since only the unspellable words make it here
            #we must return false.
            return False
        else:
            #loop trhough all of the indices that are attached to the current color.
            for i in range(color,len(letters),6):

                #get the letter stored at the current index in the letters list
                letter = letters[i]
                
                #calculate to which cube does the letter belong to
                cube = i//6

                if letter in word and cube not in cube_record:
                    word.remove(letter)
                    cube_record.append(cube)

                    #in the case that the list word has no elements, end the method call
                    if not word:
                        return True

                    #Recursive call to the next level
                    if self.is_rainbow(word,letters,cube_record,color+1):
                        return True

                    else:
                        #in the case that the recursive call returns false

                        #re append the letter, so that we can consider it again
                        word.append(letter)

                        #delete the current cube id from the cube_record
                        cube_record.remove(cube)

            #in the case that none of the letters in this level (aka color) are part of the word
            #we would like to still move on to check the next one
            return self.is_rainbow(word,letters,cube_record,color+1)

    
    def is_mono(self,word:list, letters:list)->int:
        """
        Checks if a given string is a mono word given a letter permutation. returns
        the applicable color, or None if it's not possible.
        
        Parameters
        ----------
        word:list
            a list representing a word, each item is a letter in said word.
            i.e ['s','l','o','g','a','n']
            
        letters:list
            a list containing letters, where every letter in the alphabet appears at least once
        
        """
        #TODO: think about he possibility of a word being able to be spelled within two different colors and how that can           affect the reward
        
        #iterate through the six colors
        for color in range(6):
            #make a copy of the word since we don't want to modify the word
            word_copy = word.copy()
            
            #loop through all the letters mapped to the current color
            for i in range(color,len(letters),6):
                
                #get the letter stored at the current index in the letters list
                letter = letters[i]
                
                #in the case that the current letter is present (at least once) in the copy of word list
                if letter in word_copy:
                    
                    #remove the current letter from the copy of word
                    word_copy.remove(letter)
                    
                    #check if the word has been completely spelled out
                    #in order to terminate the method call
                    if not word_copy:
                        return color
        return None
        


            
    def count_words(self,letters:list)->list:
        """
        Counts how many rainbow and mono words can be spelled given a combination, and returns the totals for each,
        as well as other information, like the range of mono words and optionally the list of words per category.
        
        Parameters
        ----------
        indices:list
            an list of characters where each item a letter of the alphabet.
            The items on indices 0 to 5 are mapped with colors 0 trough 5 respectively
            the items on indices 6 to 11 also with 0 through 5 respectively, and so on.
            
        Example
        --------
        Input
            >>comb=[0,25,13,7,8,20,...,18]
            >>analyze(comb)
        Returns
            >>200, 1500
        
        """
        
        #initializing the count for the total of both mono and rainbow  
        mono = 0
        rainbow =0
        
        #iterate through the words in the self.words list 
        #and increment the value of rainbow and mono_color
        for word in self.words:
            
            mono_result = self.is_mono(list(word),letters)
            rainbow_result = self.is_rainbow(list(word),letters,[])
            
            if isinstance(mono_result, int): 
                mono+=1
            
            if rainbow_result: 
                rainbow+=1
        
        return mono, rainbow