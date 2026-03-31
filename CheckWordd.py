#word  as inpyt and check  Vowels and consonents
def check_word(word):
    vowels = 'aeiouAEIOU'
    consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    vowel_count = 0
    consonant_count = 0
    #for loop to iterate through each character in the input word and check if it is a vowel or a consonant. It updates the respective counts accordingly.
    for char in word:
        if char in vowels:
            vowel_count += 1
        elif char in consonants:
            consonant_count += 1
    return vowel_count, consonant_count

# Example usage
#takes the input from user and calls the function to check the number of vowels and consonants in the input word. Finally, it prints the results.
input_word = input("Enter a word: ")
vowels, consonants = check_word(input_word)
print(f"Vowels: {vowels}, Consonants: {consonants}")