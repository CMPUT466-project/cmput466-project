# cmput466-project

### The two different preprocessed data are in the folder processed_datasets(with stopwords) and processed_datasets2(without stopwords)


Pay attention:
Two folders contain separated training data and test data are with_stop_word_usable_data and without_stop_word_usable_data.<br>

They are generated through a python file called generate_dataset_from_preprocessed_data.py, you may also want to change the parameters inside to generate different dataset.<br>

In each folder, you can see 10 folders, each categories got two folders, "category2" and "category".<br>
  
What's the difference?<br>
They got the same trainingX and trainingY, but they are using different test data, and word_dict will be different as well.<br>

<b>I suggest use all "category2" folders at this moment, it seems to have a more reasonable testset.</b>
  
