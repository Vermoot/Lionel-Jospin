import os
import discord
import time
import random

def scramble(word):
    return "".join(random.sample(word, len(word))).lower()


def loadWords():
    dico = open("liste_francais.txt", 'r')
    wordList = []
    for line in dico:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList


def main():
    print("Chargement de la liste...")
    wordList = loadWords()
    print("CHARGÉ")
    for i in range(0,10):
        print(random.choice(wordList))