# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: HALEY PELLETIER
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from random import shuffle
from load import load_seq
dna = load_seq("./data/X73525.fa")

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    amino_acids = []
    for i in range (0,len(dna),3):
        codon = dna[i:i+3]        
        for r in range(0,len(codons)):
            for c in range(0,len(codons[r])):
                if codons[r][c] == str(codon):
                    amino_acids.append(aa[r])
    amino_acids = collapse(amino_acids)                     
    return amino_acids       

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    print coding_strand_to_AA('TTT') #should return F
    print coding_strand_to_AA('GGG') #should return G
    print coding_strand_to_AA('TTCATG') #should return FM
    print coding_strand_to_AA('CATCACTGGGTTGGA') #should return HHWVG
    
#coding_strand_to_AA_unit_tests()
    
def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    sequence = []
    for i in range(0,len(dna)):
        letter = dna[i]
        if letter == 'G':
            sequence.append('C')
        elif letter == 'C':
            sequence.append('G')
        elif letter == 'A':
            sequence.append('T')
        elif letter == 'T':
            sequence.append('A')
        else:
            return "Error"
    sequence = collapse(sequence)
    return sequence
        
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
    print get_reverse_complement('A') #should return T
    print get_reverse_complement('C') #should return G
    print get_reverse_complement('G') #should return C
    print get_reverse_complement('T') #should return A
    print get_reverse_complement('AAAAAA') #should return TTTTTT
    print get_reverse_complement('D') #should return Error
    print get_reverse_complement('ATTCGGCTAG') #should return CAAGCCGATC
    
#get_reverse_complement_unit_tests()

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    for i in range (0,len(dna),3):
        codon = dna[i:i+3]        
        if (str(codon) == 'TAG') or (str(codon) == 'TAA') or (str(codon) == 'TGA'):
           return dna[0:i]
    return dna        

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    
    print rest_of_ORF('ATGATGATG') #should return whole string
    print rest_of_ORF('ATG') #should return ATG
    print rest_of_ORF('ATGGTTTAGGTAGCCTCGCAATGA') #should return ATGGTT
    print rest_of_ORF('ATGGTTAGACTAGCCTCGCAATGA') #should return ATGGTTAGACTAGCCTCGCAA
    print rest_of_ORF('TAA') #should return nothing
    
#rest_of_ORF_unit_tests()
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    ORFs = []    
    for i in range (0,len(dna),3):      
        codon = dna[i:i+3]              
        if (str(codon) == 'ATG'):
            ORF = rest_of_ORF(dna[i:len(dna)])
            ORFs.append(ORF)  
            dna = dna[(i+len(ORF)):len(dna)]                                                 
    return ORFs
       
#print find_all_ORFs_oneframe('TAGATGCCCATGCCCTAG') #should return ATGCCCATGCCC
                    
def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    dna1 = dna
    dna2 = dna
    dna3 = dna
     
    ORFs = []
    #Reading frame 1
    for i in range (0,len(dna1),3):      
        codon = dna1[i:i+3]              
        if (str(codon) == 'ATG'):
            ORF = rest_of_ORF(dna1[i:len(dna1)])            
            ORFs.append(ORF)  
            dna1 = dna1[(i+len(ORF)):len(dna1)]
    #Reading frame 2
    for i in range (1,len(dna2),3):      
        codon = dna2[i:i+3]               
        if (str(codon) == 'ATG'):
            ORF = rest_of_ORF(dna2[i:len(dna2)])
            ORFs.append(ORF)  
            dna = dna2[(i+len(ORF)):len(dna2)]
    #Reading frame 3   
    for i in range (2,len(dna3),3):      
        codon = dna3[i:i+3]              
        if (str(codon) == 'ATG'):
            ORF = rest_of_ORF(dna3[i:len(dna3)])
            ORFs.append(ORF)  
            dna = dna3[(i+len(ORF)):len(dna3)]
            
    if ORFs == []:
        return ['N/A']        
    else:
        return ORFs
            

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    print find_all_ORFs('ATGCATGTAGATGCC') #should return ATGCATGTAGATGCC, ATG, ATGCC
    
#find_all_ORFs_unit_tests()

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
   
    compl = get_reverse_complement(dna)    
    ORFs = find_all_ORFs(dna)      
    ORFs.extend(find_all_ORFs(compl))    
    return ORFs
    

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    print find_all_ORFs_both_strands('ATGTAGGATGATGGATGTAC') #should return 'ATG', 'ATGATGGATGTAC', 'ATGGATGTAC', 'ATGTAC', 'ATG'
    
#find_all_ORFs_both_strands_unit_tests()

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    ORFs = find_all_ORFs_both_strands(dna)   
    return max(ORFs,key=len)
    
#print longest_ORF('ATGATGTAGATGATGATGTAC') #should return ATGATGATGTAC

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
        
    maxms = []
    for i in range (0,num_trials):
        dna = list(dna)
        shuffle(dna)        
        maxms.append(longest_ORF(collapse(dna)))        
    return len(max(maxms,key=len))     
          
#print longest_ORF_noncoding(dna,1500)

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    aminos = []
    ORFs = find_all_ORFs_both_strands(dna)
    for i in range (0,len(ORFs)):
        if len(ORFs[i]) > threshold:
            aminos.append(coding_strand_to_AA(dna))
    return aminos

#print gene_finder(dna,1000)