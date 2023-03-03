#!/usr/bin/env python
# coding: utf-8

# In[72]:


from nltk.corpus import wordnet as wn
from concepts import Definition, Context
from translate import Translator
import translators as ts
d = Definition()
translator= Translator(from_lang="en", to_lang="tr")


# In[73]:


def unique(ls):
    unique_list = []
    for i in ls:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list


# In[74]:


def write_file(file_path, lines):
    file = open(file_path, 'w', encoding="utf-8")
    for line in lines:
        file.writelines(line)
    file.close()


# In[75]:


def get_file_lines(object_name, properties):
    lines = []
    object_name = format_word(object_name)
    for i in properties[1]:
        if "'" in i or "'" in object_name:
            continue
        i = i.replace("-", "_")
        lines.append(object_name + "(X):-"+ i + "(X).\n")
    return lines


# In[76]:


def format_word(word):
    word = word.lower() 
    word = word.replace("-", "_")
    word = word.replace(".", "_")
    word = word.replace("'", "_")
    word = word.replace("\"", "_")
    return word


# In[77]:


def format_translation(word):
    word = word.lower()
    word = word.replace("-", " ")
    word = word.replace("_", " ")
    word = word.replace(".", " ")
    return word


# In[78]:


def get_translated_file_lines(word_list):
    lines = []
    for i in word_list:
        #translation = translator.translate(format_translation(i))
        translation = ts.bing(format_translation(i),from_language='en' , to_language='tr')
        #translation =i
        lines.append(format_word(i) + '("' + translation + '").\n')
    return lines


# In[79]:


def get_first_lines():
    lines = []
    lines.append(":- set_prolog_flag(encoding,iso_latin_1).\n\n")
    lines.append("say(Word, L1):-\n")
    lines.append("   Goal =.. [Word,X],\n")
    lines.append("   findall(X, Goal,L),\n")
    lines.append("   remove_redundancies(L,L1).\n\n")
    lines.append("\n")
    lines.append("\n")
    lines.append("\n")
    return lines


# In[80]:


def get_last_lines():
    lines = []
    lines.append("\n\n\nremove_redundancies([X],[X]).\n")
    lines.append("remove_redundancies([X|Xs],[X|Ys]):-\n")
    lines.append("   member(X,Xs),\n")
    lines.append("   delete_all(X,Xs,Xs1),\n")
    lines.append("   remove_redundancies(Xs1,Ys).\n\n")
    lines.append("remove_redundancies([X|Xs],[X|Ys]):-\n")
    lines.append("   not(member(X,Xs)),\n")
    lines.append("   remove_redundancies(Xs,Ys).\n\n")
    lines.append("delete_all(_,[],[]).\n")
    lines.append("delete_all(X, [X|Xs], Ys):-\n")
    lines.append("   delete_all(X,Xs,Ys).\n\n")
    lines.append("delete_all(X,[Y|Xs],[Y|Ys]):-\n")
    lines.append("   not(X = Y),\n")
    lines.append("   delete_all(X,Xs,Ys).\n")
    lines.append("\n")
    lines.append("\n")
    lines.append("\n")
    return lines


# In[81]:


def get_hyponyms(word):
    words_hyponyms = {}
    ls = list(set([i for i in word.closure(lambda s:s.hyponyms(), depth=1)]))
    words_hyponyms[format_synset_name(word)] = [word.lemma_names(),format_synset_name_list(ls)]
    
    for item in ls:
        new_words_hyponyms = get_hyponyms(item)
        for i in new_words_hyponyms.keys():
            if i in words_hyponyms.keys():
                words_hyponyms[i] = [unique(words_hyponyms[i][0]+ new_words_hyponyms[i][0]),unique(words_hyponyms[i][1]+new_words_hyponyms[i][1])]
            else:
                words_hyponyms[i] = new_words_hyponyms[i]
    return words_hyponyms


# In[82]:


def format_synset_name(synset):
    synset = str(synset).lower() 
    prefix = 'synset(\''
    suffix = '\')'
    if synset.startswith(prefix):
        synset = synset[len(prefix):]
    if synset.endswith(suffix):
        synset = synset[:-len(suffix)]
    synset = synset.split(".")[0]
    return synset


# In[83]:


def format_synset_name_list(synset_list):
    ls = []
    for i in synset_list:
        ls.append(format_synset_name(i))
    return ls


# In[84]:


vehicle = wn.synset('vehicle.n.01')
typesOfVehicles = list(set([w for s in vehicle.closure(lambda s:s.hyponyms(), depth=1) for w in s.lemma_names()]))


# In[85]:


file_text_list = []
last_items = []
words_hyponyms = get_hyponyms(wn.synset('vehicle.n.01'))
for i in words_hyponyms.keys():
    file_text_list = file_text_list + get_file_lines(i, words_hyponyms[i])
    if words_hyponyms[i][1] == []:
        last_items.append(i)
file_text_list = get_first_lines() + file_text_list + get_translated_file_lines(last_items) + get_last_lines()
write_file("timetmymemory.pl", file_text_list)


# In[123]:


get_hyponyms(wn.synset('vehicle.n.01'))


# In[87]:


objects_properties = {}
typesOfVehicles = unique(typesOfVehicles)
for i in typesOfVehicles:
    digraph = wn.digraph([wn.synset(i + '.n.01')])
    digraph = digraph.split("{")[1]
    digraph = digraph.split("}")[0]

    synsets = digraph.split(";")
    lst = []
    for s in synsets:
        s = s.strip()
        if s != "":
            s = s.split("->")
            s = s[1].split('\'')
            s = s[1]
            lst.append(s.split(".")[0])
    lst = unique(lst)
    #if i not in list(objects_properties.keys()):
    objects_properties[i] = lst
    d.add_object(i, lst)
c = Context(*d)
print(c)


# In[ ]:




