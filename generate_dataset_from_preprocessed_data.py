import os
import sys


sep = os.path.sep
current = os.getcwd()
categories = ["business", "entertainment", "politics", "sport","tech"]
generate_stop = True
sentense_length = 7
nums = [str(i) for i in range(10)]
if generate_stop:
    path_with_stopwords = "/processed_datasets/proced_News_Articles"
    for category in categories:
        trainingSetX = []
        trainingSetY = []
        testSetX = []
        testSetY = []
        word_set = set()
        path1 = current+path_with_stopwords+sep+category

        all_files_with_stopwords = [str(path1+sep+relative) for relative in sorted(os.listdir(path1))]
        splitline_stop = len(all_files_with_stopwords) - len(all_files_with_stopwords)//10
        print("split",splitline_stop, len(all_files_with_stopwords))
        trainingTxtFiles_stop = all_files_with_stopwords[:splitline_stop]
        testingTxtFiles_stop = all_files_with_stopwords[splitline_stop:]

        # create training set
        for each_file in trainingTxtFiles_stop:
            #print("file_name:",each_file)
            with open(each_file) as file_obj:
                file_content = [i for i in file_obj.read().splitlines() if i]
            # file_content is each row

            
            for line in file_content:
                words = []
                for each_word in line.split(' '):
                    if each_word:
                        has_num = False
                        for each_num in nums:
                            if each_num in each_word:
                                words.append("thisisanumber")
                                has_num = True
                                break
                        if not has_num:
                            words.append(each_word)
                    
                line_length = len(words)
                
                if line_length >= sentense_length:
                    # update word_set
                    word_set.update(words)

                    # means we can create test and training set based on this substring
                    for i in range(line_length-sentense_length):
                        # string[i,i+sentense_length] is each substring, choose the last word
                        # in each substring as the correct label word, the rest as the training data
                        training_string = words[i:i+sentense_length-1]
                        label = words[i+sentense_length-1]
                        trainingSetX.append(training_string)
                        trainingSetY.append(label)


        for each_file in testingTxtFiles_stop:
            #print("file_name:",each_file)
            with open(each_file) as file_obj:
                file_content = [i for i in file_obj.read().splitlines() if i]
            # file_content is each row

            
            for line in file_content:
                words = []
                for each_word in line.split(' '):
                    if each_word:
                        has_num = False
                        for each_num in nums:
                            if each_num in each_word:
                                words.append("thisisanumber")
                                has_num = True
                                break
                        if not has_num:
                            words.append(each_word)
                    
                line_length = len(words)
                
                if line_length >= sentense_length:
                    # update word_set
                    word_set.update(words)

                    # means we can create test and training set based on this substring
                    for i in range(line_length-sentense_length):
                        # string[i,i+sentense_length] is each substring, choose the last word
                        # in each substring as the correct label word, the rest as the training data
                        training_string = words[i:i+sentense_length-1]
                        label = words[i+sentense_length-1]
                        testSetX.append(training_string)
                        testSetY.append(label)



        # now write to file
        try:
            path = current+sep+"with_stop_word_usable_data"+sep+category
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        with open(path+sep+"trainingX.txt",'w') as file_obj:
            for eachTestSubString in trainingSetX:
                for index in range(len(eachTestSubString)):
                    file_obj.write(eachTestSubString[index])
                    if index != len(eachTestSubString)-1:
                        file_obj.write(" ")
                    else:
                        file_obj.write('\n')

        with open(path+sep+"testX.txt",'w') as file_obj:
            for eachTestSubString in testSetX:
                for index in range(len(eachTestSubString)):
                    file_obj.write(eachTestSubString[index])
                    if index != len(eachTestSubString)-1:
                        file_obj.write(" ")
                    else:
                        file_obj.write('\n')

        with open(path+sep+"trainingY.txt",'w') as file_obj:
            for eachLabel in trainingSetY:
                file_obj.write(eachLabel)
                file_obj.write('\n')
        
        with open(path+sep+"testY.txt",'w') as file_obj:
            for eachLabel in testSetY:
                file_obj.write(eachLabel)
                file_obj.write('\n')    

        with open(path+sep+"word_set",'w') as file_obj:
            for eachword in word_set:
                file_obj.write(eachword)
                file_obj.write('\n')                      

else:
    path_without_stopwords = "/processed_datasets2/proced_News_Articles"              
    for category in categories:
        trainingSetX = []
        trainingSetY = []
        testSetX = []
        testSetY = []
        word_set = set()
        path2 = current+path_without_stopwords+sep+category

        all_files_without_stopwords = [str(path2+sep+relative) for relative in sorted(os.listdir(path2))]
        splitline_nonstop = len(all_files_without_stopwords) - len(all_files_without_stopwords)//10
        print("split",splitline_nonstop, len(all_files_without_stopwords))

        trainingTxtFiles_nonstop = all_files_without_stopwords[:splitline_nonstop]
        testingTxtFiles_nonstop = all_files_without_stopwords[splitline_nonstop:]
        # create training set
        for each_file in trainingTxtFiles_nonstop:
            #print("file_name:",each_file)
            with open(each_file) as file_obj:
                file_content = [i for i in file_obj.read().splitlines() if i]
            # file_content is each row

            
            for line in file_content:
                words = []
                for each_word in line.split(' '):
                    if each_word:
                        has_num = False
                        for each_num in nums:
                            if each_num in each_word:
                                words.append("thisisanumber")
                                has_num = True
                                break
                        if not has_num:
                            words.append(each_word)
                    
                line_length = len(words)
                
                if line_length >= sentense_length:
                    # update word_set
                    word_set.update(words)

                    # means we can create test and training set based on this substring
                    for i in range(line_length-sentense_length):
                        # string[i,i+sentense_length] is each substring, choose the last word
                        # in each substring as the correct label word, the rest as the training data
                        training_string = words[i:i+sentense_length-1]
                        label = words[i+sentense_length-1]
                        trainingSetX.append(training_string)
                        trainingSetY.append(label)


        for each_file in testingTxtFiles_nonstop:
            #print("file_name:",each_file)
            with open(each_file) as file_obj:
                file_content = [i for i in file_obj.read().splitlines() if i]
            # file_content is each row

            
            for line in file_content:
                words = []
                for each_word in line.split(' '):
                    if each_word:
                        has_num = False
                        for each_num in nums:
                            if each_num in each_word:
                                words.append("thisisanumber")
                                has_num = True
                                break
                        if not has_num:
                            words.append(each_word)
                    
                line_length = len(words)
                
                if line_length >= sentense_length:
                    # update word_set
                    word_set.update(words)

                    # means we can create test and training set based on this substring
                    for i in range(line_length-sentense_length):
                        # string[i,i+sentense_length] is each substring, choose the last word
                        # in each substring as the correct label word, the rest as the training data
                        training_string = words[i:i+sentense_length-1]
                        label = words[i+sentense_length-1]
                        testSetX.append(training_string)
                        testSetY.append(label)



        # now write to file
        try:
            path = current+sep+"without_stop_word_usable_data"+sep+category
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        with open(path+sep+"trainingX.txt",'w') as file_obj:
            for eachTestSubString in trainingSetX:
                for index in range(len(eachTestSubString)):
                    file_obj.write(eachTestSubString[index])
                    if index != len(eachTestSubString)-1:
                        file_obj.write(" ")
                    else:
                        file_obj.write('\n')

        with open(path+sep+"testX.txt",'w') as file_obj:
            for eachTestSubString in testSetX:
                for index in range(len(eachTestSubString)):
                    file_obj.write(eachTestSubString[index])
                    if index != len(eachTestSubString)-1:
                        file_obj.write(" ")
                    else:
                        file_obj.write('\n')

        with open(path+sep+"trainingY.txt",'w') as file_obj:
            for eachLabel in trainingSetY:
                file_obj.write(eachLabel)
                file_obj.write('\n')
        
        with open(path+sep+"testY.txt",'w') as file_obj:
            for eachLabel in testSetY:
                file_obj.write(eachLabel)
                file_obj.write('\n')   

        with open(path+sep+"word_set",'w') as file_obj:
            for eachword in word_set:
                file_obj.write(eachword)
                file_obj.write('\n')  

