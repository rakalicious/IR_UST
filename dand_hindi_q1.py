import openpyxl as px
from bitarray import bitarray
import operator

"""Special character removed
    Words containing digit removed
    if total frequency of a token is greater than 0.5 times no. of document then it is considered stop word
    nothing is done in stemming
    bitarray was used for query
    query of any length will be processed (and or and not should be spelt correctly)
    answer is provided as the document number
    """

def doc_tokenizer(lst , tokenized_lst):
    #tokenize each document into words
    for i in range(len(lst)):
        tokenized_lst.append([])
        tokenized_lst.append(lst[i].split(" "))

def improve_tokens(lst):
    #delete special char , num and make lowercase

    #remove all special characters
    utfstart = b'\xe0\xa4\x80'
    utfend = b'\xe0\xa5\xbf'
    #print(utfbytes.decode('utf8'))
    # print(decode_utf8(utfbytes))
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            temp = ''.join(k for k in lst[i][j] if k >= utfstart.decode('utf8') and k <= utfend.decode('utf8'))
            lst[i][j] = temp

    #if is digit then remove
    for i in lst:
        for j in i:
            for s in j:
                if(s.isdigit()):
                    i.remove(j)
                    break

    #convert all to loercase
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = lst[i][j].lower()

    #delete all blank lists
    for i in lst:
        if(not i):
            lst.remove(i)
    #delete all blank strings
    for i in lst:
        for j in i:
            if (j == ""):
                i.remove(j)


def freq_in_docs(lst, freq , freq_per_doc):
    for i in range(len(lst)):
        frequency_per_doc[i] = {}
        for j in lst[i]:
            if(j == "" or j == "।"):
                continue
            #frequency of tokens in overall documents
            if(j in freq):
                freq[j] += 1
            else:
                freq[j] = 1

            #frequency of tokens in each documnent
            if(j in freq_per_doc[i]):
                freq_per_doc[i][j] += 1
            else:
                freq_per_doc[i][j] = 1


def inverted_indexing(lst , inverted):
    #convert inverted indexing
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if(lst[i][j] in inverted):
                inverted[lst[i][j]].append(i)
                #print(lst[i][j])
            else:
                inverted[lst[i][j]] = []
                inverted[lst[i][j]].append(i)
    if('' in inverted):
        del inverted['']

def convert_to_bit(inverse , bit_dict , n):
    #make the bitarray dictionary for each token
    for i in inverse:
        temp = ''
        for j in range(n):
            if(j in inverse[i]):
                temp += '1'
            else:
                temp += '0'
        bit_dict[i] = bitarray(temp)



def process_query(q , bit_dict,n):
    file = open("hindi_query_output.txt", "a")
    file.write(q[:-1] + " : ")
    #divide the query into and/or/not + token and perform bitwise operations
    temp_str = ''
    for i in range(n):
        temp_str += '0'
    q = q.lower()
    tokenized_query = q.split(" ")
    if(tokenized_query[0] not in bit_dict.keys()):
        file.write("Not Found")
        return
    ans = bit_dict[tokenized_query[0]]

    for i in range(1,len(tokenized_query)):
        second_man = bit_dict[tokenized_query[i+1]]
        if(tokenized_query[i+1] not in bit_dict.keys()):
            second_man = temp_str
        else:
            second_man = bit_dict[tokenized_query[i + 1][:-1]]
        if(tokenized_query[i] == 'and'):
            ans = ans & second_man
        elif(tokenized_query[i] == 'or'):
            ans = ans | second_man
        elif (tokenized_query[i] == 'not'):
            ans = ans & (~second_man)
        i += 1

        #to stop the loop from going out of bounds
        if(i >= len(tokenized_query)-1):
            break
        print(i)
    ans = str(ans)
    #print(ans[10:-1])
    flag = 0
    for i in range(len(ans)):
        if(ans[i] == '1'):
            flag = 1
            file.write(str(i-9) + " ")

    if(flag == 0):
        file.write("Not Found")
    file.write("\n")
    file.close()

def delete_stop_words(frequency_all , total_no_doc):
    #delete frequent more than required words in documents
    temp = sorted(frequency_all.items(), key=operator.itemgetter(1), reverse=True)
    print(temp)
    for i in temp:
        #print(i[0])
        if(i[1] > 0.5*total_no_doc):
            del frequency_all[i[0]]
        else:
            break

W = px.load_workbook('Dand_Prakriya.xlsx')
p = W.get_sheet_by_name(name = 'Sheet')

eng_list = []
hindi_list = []

#reading documents
for row in p.iter_rows():
    eng_list.append(row[0].internal_value)
    hindi_list.append(row[1].internal_value)


token_in_doc = []
total_no_doc = len(hindi_list)

#tokenize and improve
doc_tokenizer(hindi_list, token_in_doc)
#print(token_in_doc)
improve_tokens(token_in_doc)


#find the frequencies
frequency_all = {}
frequency_per_doc = {}
freq_in_docs(token_in_doc, frequency_all , frequency_per_doc)
#delete stopwords
delete_stop_words( frequency_all , total_no_doc)

file = open("hindi_frequency_of_tokens.txt", "w")
for i in frequency_all:
    file.write(i +" "+ str(frequency_all[i]) + "\n")
file.close()

#inverted indexing
inv_freq = {}
inverted_indexing(token_in_doc, inv_freq)
file = open("hindi_inverted_indexing.txt", "w")
for i in inv_freq:
    file.write(i +" "+ str(inv_freq[i]) + "\n")
file.close()

#make bitarray
bit_dict = {}
convert_to_bit(inv_freq, bit_dict , total_no_doc)

#temp = sorted(frequency_all.items(), key=operator.itemgetter(1), reverse=False)

file = open("hindi_query.txt", "r")
file2 = open("hindi_query_output.txt", "w")
file2.close()
for line in file:
    process_query(line , bit_dict , total_no_doc)
file.close()
