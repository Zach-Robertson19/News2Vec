# News2Vec
A program that find the cosine similarity between reddit r/politics data using the Word2Vec word embedding model.

Usage.

1. Get data from the desired subreddit.
  Use Get_Data\subreddit_data_to_csv.py
 
2. Create Word2Vec Model using subreddit data.
  Use unk_set.py Word2Vec_Model
  
3. Find headlines you want to compare and build the Compare_Headlines object inside of unk_set.py
  comp = Compare_Headlines(path to Word2Vec Model, list of sentence strings)
  
4. Use the Compare_Headlines object to find the cosine similarity.
  cos_sim = comp.CosineSimilarity(comp.vectors, comp.titles[0], comp.titles[1])
