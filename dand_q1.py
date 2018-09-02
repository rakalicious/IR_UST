import openpyxl as px
from bitarray import bitarray

def doc_tokenizer(lst , tokenized_lst):
    #tokenize each doc
    for i in range(len(lst)):
        tokenized_lst.append([])
        tokenized_lst.append(lst[i].split(" "))

def improve_tokens(lst):
    #delete special char , num and make lowercase

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            temp = ''.join(k for k in lst[i][j] if k.isalnum())
            lst[i][j] = temp

    for i in lst:
        for j in i:
            if(j.isdigit()):
                i.remove(j)

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            #print(j.type)
            lst[i][j] = lst[i][j].lower()
            #print(lst[i][j])

    for i in lst:
        if(not i):
            lst.remove(i)
    for i in lst:
        for j in i:
            if (j == ""):
                i.remove(j)


def freq_in_docs(lst , freq):
    for i in lst:
        for j in i:
            if(j in freq):
                freq[j] += 1
            else:
                freq[j] = 1


def inverted_indexing(lst , inverted):
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
    for i in inverse:
        temp = ''
        for j in range(n):
            if(j in inverse[i]):
                temp += '1'
            else:
                temp += '0'
        bit_dict[i] = bitarray(temp)


W = px.load_workbook('Dand_Prakriya.xlsx')
p = W.get_sheet_by_name(name = 'Sheet')

eng_list = []
hind_list = []

#reading documents
for row in p.iter_rows():
    eng_list.append(row[0].internal_value)
    hind_list.append(row[1].internal_value)


tok_doc_eng = []
total_doc = len(tok_doc_eng)
tok_doc_hin = []
doc_tokenizer(eng_list , tok_doc_eng)
improve_tokens(tok_doc_eng)

frequency_eng = {}
freq_in_docs(tok_doc_eng, frequency_eng)
inv_eng = {}
inverted_indexing(tok_doc_eng, inv_eng)
bit_dict_eng = {}
convert_to_bit(inv_eng, bit_dict_eng , total_doc)
#print("RAKA".lower())
print(tok_doc_eng)
print(bit_dict_eng)