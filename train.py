#import libraries
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import glob

class DecisionTree:
    def __init__(self, train_df, val_df, test_df, target, max_depth = None, min_info_gain = 0, alpha = 0.1):
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df
        self.max_depth = max_depth
        self.min_info_gain = min_info_gain
        self.target = target
        self.alpha = alpha
    
    def variance(self, y):
        if len(y) == 1:
            return 0
        return y.var()

    def info_gain(self, y, mask):
        a = sum(mask)
        b = mask.shape[0] - a
        if a == 0 or b == 0:
            return 0
        else:
            return self.variance(y) - (self.variance(y[mask])*a/(a+b) + self.variance(y[-mask])*b/(a+b))
    
    def info_gain_ratio(self, y, mask):
       if len(mask) == 1:
           return 0
       return self.info_gain(y, mask)/self.variance(mask)
 
    def max_info_gain(self, x, y):
        colname = x.name
        if colname == 'trip_distance':
            step_size = 20
        elif colname == 'fare_amount':
            step_size = 40
        else: 
            step_size = 4
        # options = x.sort_values().unique()
        options = sorted(set(x))
        options = options[1 :: step_size]

        res = -1
        split_value = -1000
        num = 0
        for value in options:
            mask = x >= value
            ig = self.info_gain(y, mask)
            if ig is not None and ig > res: 
                res = ig
                split_value = value
                num = num + 1  
                #new 
        if num == 0 or res == -1:
            return (None, None, False)
        else: 
            return(split_value, res, True)
        
    def get_best_split(self, x, out):
        try:
            masks = x.drop(out, axis = 1).apply(self.max_info_gain, y = x[out])
            if masks is None or len(masks) == 0 or np.sum(masks.loc[2, :]) == 0 or masks.empty:
                return (None, None, None)
            masks = masks.loc[:, masks.loc[2,:]]
            masks = masks.apply(pd.to_numeric)
            
            if self.min_info_gain is not None:
             masks = masks.loc[:, masks.loc[1,:] > self.min_info_gain]

            masks['Max'] = masks.idxmax(axis = 1)
            split_vari = masks.loc[1][-1]
            split_value = masks[split_vari][0]
            split_ig = masks[split_vari][1]
            return(split_vari, split_value, split_ig)
        except KeyError:
            return (None, None, None)
        except ValueError:
            return (None, None, None)

    def make_split(self, vari, value, data):
        data1 = data[data[vari] >= value]
        data2 = data[data[vari] < value]
        return data1, data2

    def make_pred(self, data):
        return data.mean()
    
    ##new##
    def count_leaves(self, tree):
        if not isinstance(tree, dict):
            return 1
        
        question = list(tree.keys())[0]
        left, right = tree[question]

        left_cnt = self.count_leaves(left)
        right_cnt = self.count_leaves(right)
        return left_cnt + right_cnt

    def cost_complexity(self, tree):
        if not isinstance(tree, dict):
            return tree
        
        question = list(tree.keys())[0]
        left, right = tree[question]

        left_pruned = self.cost_complexity(left)
        right_pruned = self.cost_complexity(right)
        pruned_tree = {question: [left_pruned, right_pruned]}

        # Calculate the misclassification error for the pruned tree and the majority class
        pruned_tree_error = self.evaluate_model(pruned_tree, self.val_df)
        originial_tree_error = self.evaluate_model(tree, self.val_df)
    
        # Calculate the cost-complexity measure for the pruned tree and the majority class
        leaf_count_pruned = self.count_leaves(pruned_tree)
        leaf_count_original = self.count_leaves(tree)
        pruned_tree_cost_complexity = pruned_tree_error + self.alpha*leaf_count_pruned
        original_tree_cost_complexity = originial_tree_error + self.alpha*leaf_count_original

        if pruned_tree_cost_complexity < original_tree_cost_complexity:
            return pruned_tree
        else:
            return tree 
        
    def prune(self, tree):
        return self.cost_complexity(tree)
    
    def train_tree(self, data, counter = 0):
        var, val, ig = self.get_best_split(data, self.target)
        if self.max_depth != None and counter >= self.max_depth:
            return self.make_pred(data[self.target])
        if ig is not None and ig != 0 and len(data) != 0:
            counter += 1
            left, right = self.make_split(var, val, data)
            split_type = ">="
            question = "{} {}  {}".format(var, split_type, val)
            subtree = {question: []}

            yes_ans = self.train_tree(left, counter) 
            no_ans = self.train_tree(right, counter)
            if yes_ans == no_ans:
                subtree = yes_ans #new subtree
            else:
                subtree[question].append(yes_ans)
                subtree[question].append(no_ans)
        else:
            return self.make_pred(data[self.target])
        return subtree

    def classi_pred(self, observaction, side):
        quest_key = next(iter(side.keys())) #get the first key, or the first question
        vari = quest_key.split()[0] #choose what variables to compare
        if isinstance(observaction, pd.Series):
            if observaction[vari] >= float(quest_key.split()[2]):
                answer = side[quest_key][0]
            else:
                answer = side[quest_key][1]
        if isinstance(observaction, list):
            if vari == 'x1':
                index = 0
            else:
                index = 1
            if observaction[index] >= float(quest_key.split()[2]):
                answer = side[quest_key][0]
            else:
                answer = side[quest_key][1]
        #base case: if the answer is not a dict
        if not isinstance(answer, dict):
            return answer
        else:
            return self.classi_pred(observaction, answer) #go to the side of condition
            
    def evaluate_model(self, tree, data):
      pred = []
      for i in range(data.shape[0]):
        prediction =  self.classi_pred(data.iloc[i, :], tree)
        pred.append(prediction)
      actual = data[self.target].tolist()
      mse = np.mean((np.array(actual) - np.array(pred))**2)
      return mse
    
    def get_depth(self, tree):
        #print(isinstance(tree, dict), tree)
        if isinstance(tree, dict):
            left, right = list(tree.values())[0]
            return max(self.get_depth(left), self.get_depth(right)) + 1
        else:
            return 1

def train_evaluate_tree(train_df, val_df, test_df, target, max_depth = None, prune = False, min_info_gain = None, alpha = 0.1):
    model = DecisionTree(train_df, val_df, test_df, target, max_depth = max_depth, min_info_gain= min_info_gain, alpha = alpha)
    tree = model.train_tree(train_df)
    depth = model.get_depth(tree)
    #prune
    if prune: 
        tree = model.prune(tree)
    mse_train = model.evaluate_model(tree, train_df)
    mse_test = model.evaluate_model(tree, test_df)
    print(f"The train set mse is {mse_train}")
    print(f"The test set mse is {mse_test}")
    return depth, tree, mse_train, mse_test

def load_data(file_pattern):
  '''
  Load data and preprocessing data
  '''
  filenames = glob.glob(file_pattern)
  columns_to_keep = ['passenger_count', 'trip_distance', 'tip_amount', 'fare_amount', 'extra', 'period'] 
  df = pd.DataFrame()
  df_test = pd.DataFrame()
  sampling_fraction = 0.2
  for filename in filenames:
    sub_df = pd.read_csv(filename)
    sub_df = sub_df[columns_to_keep]
    sampled_chunk, sample_chunk_test = train_test_split(sub_df , test_size= sampling_fraction)
    df = pd.concat([df, sampled_chunk])
    df_test = pd.concat([df_test, sample_chunk_test])
  return df, df_test 

def base_line(data, target):
    mean_target = data[target].mean()
    median_target = data[target].median()
    mean_mse = np.mean((data[target] - mean_target)**2)
    med_mse = np.mean((data[target] - median_target)**2)
    return mean_mse, med_mse

if __name__ == "__main__":
    ###################################LOAD DATA##########################################
    file_pattern = 'data/*.csv'
    df, df_test = load_data(file_pattern)
    train_df, val_df = train_test_split(df, test_size = 0.2)
    mean_mse, med_mse = base_line(df_test, 'tip_amount')
    print(f"For baseline, the mean of mean squared error the dataset is {mean_mse}, and the mean of median squared errror is {med_mse}")
    ###############################################TRAIN TREE########################################################################
    dep, tree, mse_train, mse_test = train_evaluate_tree(train_df,val_df, df_test, 'tip_amount', min_info_gain = 0.01)

    lowest_mse = mse_test
    best_max_depth = dep
    best_tree = tree
    best_min_info_gain = None
    min_info_gains = [0.05, 0.1, 0.2]
    max_depth = dep - 5
    for min_info_gain in min_info_gains:
            _, cur_tree, mse_train, mse_test = train_evaluate_tree(train_df,val_df, df_test, 'tip_amount', max_depth = max_depth, prune = True, min_info_gain = min_info_gain ,alpha = 0.1)

            if mse_test < lowest_mse:
                lowest_mse = mse_test
                best_min_info_gain = min_info_gain
                best_max_depth = max_depth
                best_tree = cur_tree
    print(f" best max_depth {best_max_depth}, best minimum information {best_min_info_gain}, with lowest mse {lowest_mse}")
    print(best_tree)

