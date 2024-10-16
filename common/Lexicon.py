import pandas as pd
import re

class Lexicon:
    """
    Class that initializes the alphabet, word_list and letter_freq
    
    Parameters
    ----------
    alphabet:list
        a list of characters of the letters of the alphabet
    word_list:list
        a list containing all the valid words
    letter_freq:dict
        a dictionary of letter:frquency pairs, sorted by highest frequency
    
    Methods
    -------
    generate_word_list()
        initializes the word_list attribute
        
    calculate_letter_freq()
        initializes the letter_freq attribute
        
    calculate _letter_rep(num_cubes)
        Calculates how many times a letter will be repeated, given a number of cubes.
        it returns a list and dictionary representation of this letter repetition
    """
    
    #constructor
    def __init__(self):
        """
        Constructor           
        """
        self.alphabet = list(map(chr, range(97, 123))) #alphabet
        
        #method calls
        self.generate_word_list()
        self.calculate_letter_freq()
        
        
    def generate_word_list(self):
        """
        Imports the AOA master_file, filters words, and returns a list of the valid words
        """
        #created a dataframe from the excel file
        df = pd.read_excel("src/Master_file_AoAmeasures.xlsx")
        
        #Get rid of the rows that containwhose length is less than 1 and greater than 6 character
        #targeting
        df = df[df['WORD'].str.len() > 1 ]
        df = df[df['WORD'].str.len() <= 6]
        
        #Filter out words that have special characters, spaces and 
        pattern = re.compile("^[a-z]+$")
        df = df[df['WORD'].apply(lambda word: bool(pattern.match( word.strip() )))]
        df=df.drop_duplicates(subset=["WORD"])
        self.word_list = df["WORD"].to_list()
    
    def calculate_letter_freq(self):
        """
        Calculates the frequency of the letters in percentages
        """
        #initializes a dictionary to keep count of the letters in the alphabet
        letter_freq ={letter:0 for letter in self.alphabet}
        
        #total of characters
        total_chars = 0
        
        #counts how many times the letters are repeated
        all_in_one = ""
        for word in self.word_list:
            for letter in word.strip():
                total_chars +=1
                letter_freq[letter] += 1
        
        #sorts the letter_freq dictionary items by the value, in descending order
        #Where the letter with the most counts goes first
        letter_freq = dict(sorted(letter_freq.items(), key=lambda item: item[1], reverse=True))
               
        #converts the letter:count pairs to letter:percentage and assign the dictionary to self.letter_freq
        self.letter_freq = {letter:count/total_chars for letter,count in letter_freq.items()}
        
    def calculate_letter_reps(self, num_cubes:int)->tuple:
        """
        Creates a dictionary where the keys are the letters of the alphabet and the values 
        are integers representing how many times a letter should repeat.
        First it makes sure that each letter is repeated at least once, 
        and then adds the corresponding percentage of the reminder (using the frequency percentage)
        Returns a two-item tuple, where the first one is the dictionary representation, and the second
        is a list representation of the letter repetitions.
        
        Parameters
        ----------
        num_cubes:int
            The total number of cubes. Must be >= 5
            since 5 cubes is the least number of cubes that allows for every letter
            to appear at least once
        
        Example
        ------
        >> calculate_letter_reps(5)
        >> {'e':2, 'a':2, ..., 'y':1}, 
        ['e','e','a','a',..., 'y']
        """
        
        #initializes a dictionary based on self.letter_rep where each letter key has a value of 1
        #this ensures that every letter repeats at least once
        reps = {letter:1 for letter in self.letter_freq.keys()}
        
        #represents the total number of repetitions left, after the previous step
        #where we ensured that each letter repeats at least once
        remaining_reps = (6*num_cubes)-26
        
        #flag for the while loop
        flag = True 
        
        #distribute the letters based on the frequency and the current remaining repetitions
        while flag:
            
            #snapshot of the current count of repetitions left
            #will be used as a reference to know how many repetitions correspond to each letter
            reference= remaining_reps
            
            for letter, freq in self.letter_freq.items():
                
                #break out of the for and while loop when there are not more repetitions
                if remaining_reps==0: 
                    flag=False
                    break
                    
                #calculate the corresponding portion of the available repetitions, 
                #based on the frequency percentage
                local_reps = round(freq*reference)
                
                
                #Break out of for loop in the case that the corresponding repetitions are zero
                if local_reps==0:
                    #in the case that the current letter is also the same as the most frequent letter 'e'
                    #we must stop the while loop
                    if letter == 'e':
                        flag = False
                    break
                
                #in the case that the local is greater than the total repetitions
                elif local_reps>remaining_reps:
                    
                    #Add the reminder of total
                    reps[letter] +=remaining_reps
                    remaining_reps = 0
                
                else: 
                    #Add the local repetitions to the respective letter in the reps dictionary
                    reps[letter]+=local_reps
                    
                    #deducts the amount just added to a letter from the total amount of repetitions available
                    remaining_reps-=local_reps
        
        #in the case that there are still repetitions left (a small number by now)
        #distribute one by one until there are none left
        for letter in self.letter_freq.keys():
            if remaining_reps != 0:
                reps[letter] +=1
                remaining_reps -=1
        
        #makes a list version of the rep dictionary
        reps_list_indices = []
        reps_list_characters = []
        
        for letter,rep in reps.items():
            reps_list_characters +=[letter]*rep
            reps_list_indices+= [self.alphabet.index(letter)]*rep
            
        return reps, reps_list_indices, reps_list_characters