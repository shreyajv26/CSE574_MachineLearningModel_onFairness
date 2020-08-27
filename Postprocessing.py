
from utils import *
#######################################################################################################################
# YOU MUST FILL OUT YOUR SECONDARY OPTIMIZATION METRIC (either accuracy or cost)!
# The metric chosen must be the same for all 5 methods.
#
# Chosen Secondary Optimization Metric: cost
#######################################################################################################################
""" Determines the thresholds such that each group has equal predictive positive rates within 
    a tolerance value round(epsilon,16). For the Naive Bayes Classifier and SVM you should be able to find
    a nontrivial solution with round(epsilon,16)=0.02. 
    Chooses the best solution of those that satisfy this constraint based on chosen 
    secondary optimization criteria.
"""
def enforce_demographic_parity(categorical_results, epsilon):
    _races = list(categorical_results.keys())
    demographic_parity_data = {}
    thresholds = {}
    ppr={}
    for key in categorical_results.keys():
        p=[]
        for i in range(1, 101):
            threshold = float(i) / 100.0
            eval_copy = list.copy(categorical_results[key])
            eval_copy = apply_threshold(eval_copy, threshold)
            _true_rate=get_num_predicted_positives(eval_copy)
            _true_rate /= len(categorical_results[key])
            p.append(_true_rate)
        ppr[key]=p


    tpr_dic_h={}
    tpr_dic_c={}
    for i in range(0,len(ppr[_races[0]])):
        for j in range(0,len(ppr[_races[1]])):
            if(abs(round(ppr[_races[0]][i],16)-round(ppr[_races[1]][j],16))<round(epsilon,16)):
                tpr_dic_h[round(ppr[_races[0]][i],16)]=i
                tpr_dic_c[round(ppr[_races[0]][i],16)]=j

    
    tpr_dic_a={} 

    for k in range(0,len(ppr[_races[2]])):
        for l in tpr_dic_h.keys() :
            if(abs(round(ppr[_races[2]][k],16)-l)<round(epsilon,16)):
                tpr_dic_a[(l)]=k

    
    tpr_dic_other={}

    for m in range(0,len(ppr[_races[3]])):
        for p in tpr_dic_a.keys():
            if(abs(round(ppr[_races[3]][m],16)-p)<round(epsilon,16)):
                tpr_dic_other[(p)]=m
    
    prev=-float("inf")
    final_dictionary={}

    for t in tpr_dic_other.keys():
        hi=tpr_dic_h[t]
        
        ci=tpr_dic_c[t]
        ai=tpr_dic_a[t]
        oi=tpr_dic_other[t]
        _dictionary={}
        _dictionary[_races[0]]=apply_threshold(categorical_results[_races[0]],float(hi+1) / 100.0)
        _dictionary[_races[1]]=apply_threshold(categorical_results[_races[1]],float(ci+1) / 100.0)
        _dictionary[_races[2]]=apply_threshold(categorical_results[_races[2]],float(ai+1) / 100.0)
        _dictionary[_races[3]]=apply_threshold(categorical_results[_races[3]],float(oi+1) / 100.0)

        m=apply_financials(_dictionary)
        if m>prev:
            prev=m
            thresholds[_races[0]]=float(hi+1) / 100.0
            thresholds[_races[1]]=float(ci+1) / 100.0
            thresholds[_races[2]]=float(ai+1) / 100.0
            thresholds[_races[3]]=float(oi+1) / 100.0
            demographic_parity_data=_dictionary
        

    
    return demographic_parity_data, thresholds

    


    # Must complete this function!
    #return demographic_parity_data, thresholds

    return None, None

#######################################################################################################################
""" Determine thresholds such that all groups have equal TPR within some tolerance value round(epsilon,16), 
    and chooses best solution according to chosen secondary optimization criteria. For the Naive 
    Bayes Classifier and SVM you should be able to find a non-trivial solution with round(epsilon,16)=0.01
"""
def enforce_equal_opportunity(categorical_results,epsilon):

    _races = list(categorical_results.keys())
    thresholds = {}
    equal_opportunity_data = {}
    
    true_positives={}
    false_positives={}

    for group in categorical_results.keys():
        true_positives[group], false_positives[group], group1=get_ROC_data(categorical_results[group], group)
        

    
    tpr_dic_h={}
    tpr_dic_c={}
    for i in range(0,len(true_positives[_races[0]])):
        for j in range(0,len(true_positives[_races[1]])):
            if(abs(round(true_positives[_races[0]][i],16)-round(true_positives[_races[1]][j],16))<round(epsilon,16)):
                tpr_dic_h[round(true_positives[_races[0]][i],16)]=i
                tpr_dic_c[round(true_positives[_races[0]][i],16)]=j

   
    tpr_dic_a={} 

    for k in range(0,len(true_positives[_races[2]])):
        for l in tpr_dic_h.keys() :
            if(abs(round(true_positives[_races[2]][k],16)-l)<round(epsilon,16)):
                tpr_dic_a[(l)]=k

    
    tpr_dic_other={}

    for m in range(0,len(true_positives[_races[3]])):
        for p in tpr_dic_a.keys():
            if(abs(round(true_positives[_races[3]][m],16)-p)<round(epsilon,16)):
                tpr_dic_other[(p)]=m

    
    
    prev=-float("inf")
    final_dictionary={}

    for t in tpr_dic_other.keys():
        hi=tpr_dic_h[t]
        
        ci=tpr_dic_c[t]
        ai=tpr_dic_a[t]
        oi=tpr_dic_other[t]
        _dictionary={}
        _dictionary[_races[0]]=apply_threshold(categorical_results[_races[0]],float(hi+1) / 100.0)
        _dictionary[_races[1]]=apply_threshold(categorical_results[_races[1]],float(ci+1) / 100.0)
        _dictionary[_races[2]]=apply_threshold(categorical_results[_races[2]],float(ai+1) / 100.0)
        _dictionary[_races[3]]=apply_threshold(categorical_results[_races[3]],float(oi+1) / 100.0)

        m=apply_financials(_dictionary)
        if m>prev:
            prev=m
            thresholds[_races[0]]=float(hi+1) / 100.0
            thresholds[_races[1]]=float(ci+1) / 100.0
            thresholds[_races[2]]=float(ai+1) / 100.0
            thresholds[_races[3]]=float(oi+1) / 100.0
            final_dictionary=_dictionary


    
    
    return final_dictionary, thresholds
#######################################################################################################################

"""Determines which thresholds to use to achieve the maximum profit or maximum accuracy with the given data
"""

def enforce_maximum_profit(categorical_results):
    _races = list(categorical_results.keys())
    mp_data = {}
    thresholds = {}

    # Must complete this function!
    #return mp_data, thresholds
    
    final_dictionary={}
    
    for key in categorical_results.keys():
        prev=-float("inf")
        for i in range(1,101):
                d=apply_threshold(categorical_results[key],float(i) / 100.0)
                m=apply_financials(d,True)
                if m>prev:
                    prev=m
                    thresholds[key]=float(i) / 100.0
                    
    _dictionary={}
    _dictionary[_races[0]]=apply_threshold(categorical_results[_races[0]],thresholds[_races[0]])
    _dictionary[_races[1]]=apply_threshold(categorical_results[_races[1]],thresholds[_races[1]])
    _dictionary[_races[2]]=apply_threshold(categorical_results[_races[2]],thresholds[_races[2]])
    _dictionary[_races[3]]=apply_threshold(categorical_results[_races[3]],thresholds[_races[3]])
    
    
    
    # Must complete this function!
    #return mp_data, thresholds
    
    return _dictionary, thresholds

#######################################################################################################################
""" Determine thresholds such that all groups have the same PPV, and return the best solution
    according to chosen secondary optimization criteria
"""

def enforce_predictive_parity(categorical_results, epsilon):
    _races = list(categorical_results.keys())
    predictive_parity_data = {}
    thresholds = {}
    ppv={}

    for key in categorical_results.keys():
        p=[]
        for i in range(1, 101):
            threshold = float(i) / 100.0
            eval_copy = list.copy(categorical_results[key])
            eval_copy = apply_threshold(eval_copy, threshold)
            _p=get_positive_predictive_value(eval_copy)
            p.append(_p)
        ppv[key]=p

    
    tpr_dic_h={}
    tpr_dic_c={}
    for i in range(0,len(ppv[_races[0]])):
        for j in range(0,len(ppv[_races[1]])):
            if(abs(round(ppv[_races[0]][i],16)-round(ppv[_races[1]][j],16))<round(epsilon,16)):
                tpr_dic_h[round(ppv[_races[0]][i],16)]=i
                tpr_dic_c[round(ppv[_races[0]][i],16)]=j

   
    tpr_dic_a={} 

    for k in range(0,len(ppv[_races[2]])):
        for l in tpr_dic_h.keys() :
            if(abs(round(ppv[_races[2]][k],16)-l)<round(epsilon,16)):
                tpr_dic_a[(l)]=k

    
    tpr_dic_other={}

    for m in range(0,len(ppv[_races[3]])):
        for p in tpr_dic_a.keys():
            if(abs(round(ppv[_races[3]][m],16)-p)<round(epsilon,16)):
                tpr_dic_other[(p)]=m

    
    
    prev=-float("inf")
    final_dictionary={}

    for t in tpr_dic_other.keys():
        hi=tpr_dic_h[t]
        
        ci=tpr_dic_c[t]
        ai=tpr_dic_a[t]
        oi=tpr_dic_other[t]
        _dictionary={}
        _dictionary[_races[0]]=apply_threshold(categorical_results[_races[0]],float(hi+1) / 100.0)
        _dictionary[_races[1]]=apply_threshold(categorical_results[_races[1]],float(ci+1) / 100.0)
        _dictionary[_races[2]]=apply_threshold(categorical_results[_races[2]],float(ai+1) / 100.0)
        _dictionary[_races[3]]=apply_threshold(categorical_results[_races[3]],float(oi+1) / 100.0)

        m=apply_financials(_dictionary)
        if m>prev:
            prev=m
            thresholds[_races[0]]=float(hi+1) / 100.0
            thresholds[_races[1]]=float(ci+1) / 100.0
            thresholds[_races[2]]=float(ai+1) / 100.0
            thresholds[_races[3]]=float(oi+1) / 100.0
            predictive_parity_data=_dictionary



    
    return predictive_parity_data, thresholds

    ###################################################################################################################
""" Apply a single threshold to all groups, and return the best solution according to 
    chosen secondary optimization criteria
"""

def enforce_single_threshold(categorical_results):
    _races = list(categorical_results.keys())
    single_threshold_data = {}
    thresholds = {}
    accuracy_list = []
    for i in range (1,100):
        single_threshold_data[_races[2]] = apply_threshold(categorical_results[_races[2]],float(i)/100)
        single_threshold_data[_races[1]] = apply_threshold(categorical_results[_races[1]],float(i)/100)
        single_threshold_data[_races[0]] = apply_threshold(categorical_results[_races[0]],float(i)/100)
        single_threshold_data[_races[3]] = apply_threshold(categorical_results[_races[3]],float(i)/100)
        accuracy_list.append(get_total_accuracy(single_threshold_data))
    max_accuracy=((accuracy_list.index(max(accuracy_list))/100)+0.01)
    single_threshold_data[_races[2]] = apply_threshold(categorical_results[_races[2]],max_accuracy)
    single_threshold_data[_races[1]] = apply_threshold(categorical_results[_races[1]],max_accuracy)
    single_threshold_data[_races[0]] = apply_threshold(categorical_results[_races[0]],max_accuracy)
    single_threshold_data[_races[3]] = apply_threshold(categorical_results[_races[3]],max_accuracy)
    thresholds = {_races[2]:max_accuracy,_races[1]:max_accuracy,_races[0]:max_accuracy,_races[3]:max_accuracy}

        
    print ("......Categorical results.....")

   

    # Must complete this function!
    return single_threshold_data, thresholds

    #return None, None