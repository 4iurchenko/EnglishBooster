import gspread
import os
# Link to configure google here https://www.youtube.com/results?search_query=python+google+sheet+2021

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def mask_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[0:start] + s[end:]
    except ValueError:
        return ""

sa = gspread.service_account(filename="secret_client.json")
sh = sa.open("To-do list")
wks = sh.worksheet("ToDo")
print("Rows:", wks.row_count)
print("Columns:", wks.col_count)

w = wks.get_all_values()[3:]

monitor_score = 0
monitor_success = 0
monitor_fail = 0

stage_two_words = []

j = 1
for i in w:
    print("Word number ", j)
    sentence_with_word = i[2]
    word_current = find_between(i[2], "*", "*")
    masked_sentence = mask_between(i[2], "*", "*")
    synonyms = i[3]

    print("write a word for synonyms and antonyms ", synonyms)
    input_word = input()
    if input_word == word_current:
        print("Correct. ", "The example sentence is ", sentence_with_word)
        monitor_success += 1
    else:
        print("Next try will be better. ", "The example can should be ", sentence_with_word)
        monitor_fail += 1
        stage_two_words.append({"word": word_current, "sentence_with_word": sentence_with_word, "masked_sentence": masked_sentence, "synonyms": synonyms})

    j+=1

monitor_score = 100 * monitor_success / (monitor_success + monitor_fail)
print("============================")
print("Great-great, congratulations. You've successful in {success} words, you failed {failed} words. Total score is {score}%".format(success = monitor_success, failed = monitor_fail, score = monitor_score), )

### Stage 2
print("============================")
print("Let's reiterate wrong words again")
j = 1
monitor_score = 0
monitor_success = 0
monitor_fail = 0

for i in stage_two_words:
    print("Word number ", j)
    sentence_with_word = i["sentence_with_word"]
    word_current = i["word"]
    masked_sentence = i["masked_sentence"]
    synonyms = i["synonyms"]

    print("write a word for synonyms and antonyms ", synonyms)
    input_word = input()
    if input_word == word_current:
        print("Correct. ", "The example sentence is ", sentence_with_word)
        monitor_success += 1
    else:
        print("Next try will be better. ", "The example can should be ", sentence_with_word)
        monitor_fail += 1

    j+=1

monitor_score = 100 * monitor_success / (monitor_success + monitor_fail)
print("Great-great, congratulations. You've successful in {success} words, you failed {failed} words. Total score is {score}%".format(success = monitor_success, failed = monitor_fail, score = monitor_score), )
