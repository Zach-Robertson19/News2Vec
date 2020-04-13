# News2Vec
A program that find the cosine similarity between reddit r/politics titles (which are news headlines according to the subreddit rules) using the Word2Vec word embedding model, which builds word vectors for each word in a corpus, coupled with a numerical averaging method to find approximate sentence vectors.

Usage.

1. Get data from the desired subreddit.
  
  Use subreddit_data_to_csv.py, this will export the data as a csv file into the Get_Data folder
 
2. Create Word2Vec Model using subreddit data.
  
  Use the News2Vec.py Word2Vec_Model object to create the model, the model is automatically created by initilization of the Word2Vec_Model object. The object also saves the sentences in a pkl file after they have been parsed for punctutation. 
  
3. Find headlines you want to compare and build the Compare_Headlines object inside of News2Vec.py
  
  comp = Compare_Headlines(path to Word2Vec Model, list of sentence strings)
  
4. Use the Compare_Headlines object to find the cosine similarity. You must use the returned sentences from comp, not the original sentences as misspelled words are replaced by their closest match that exists in the corpus.
  
  cos_sim = comp.CosineSimilarity(comp.vectors, comp.titles[0], comp.titles[1])
  
Other Methods:

Get_Data/select_data.py - get a subset of data from a larger group of data
  Use Get_Subset_of_Data(start_date, end_date) object to automatically export the subset to a csv, make sure to use mm.dd.YYYY format       for the dates
  
Get_Data/add_data.py - add two data files together if ones start date equals the others end date.
  Use Add_data_files() object to automatically find files that have overlapping dates or where ones start date equals another end
    date and add those data files together.
