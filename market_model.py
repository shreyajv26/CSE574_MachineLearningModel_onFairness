from sklearn import svm
from Preprocessing import preprocess
from Postprocessing import *
from utils import *

metrics = ["race", "sex", "age", 'c_charge_degree', 'priors_count', 'c_charge_desc']
training_data, training_labels, test_data, test_labels, categories, mappings = preprocess(metrics)

SVR = svm.LinearSVR(C=1.0/float(len(test_data)), max_iter=10000)
SVR.fit(training_data, training_labels)

training_class_predictions = SVR.predict(training_data)
training_predictions = []
test_class_predictions = SVR.predict(test_data)
test_predictions = []


for i in range(len(training_labels)):
    training_predictions.append(training_class_predictions[i])

for i in range(len(test_labels)):
    test_predictions.append(test_class_predictions[i])



training_race_cases = get_cases_by_metric(training_data, categories, "race", mappings, training_predictions, training_labels)
test_race_cases = get_cases_by_metric(test_data, categories, "race", mappings, test_predictions, test_labels)


print("enforcing equal opportunity")
training_race_cases_max_profit, thresholds_mp = enforce_equal_opportunity(training_race_cases,0.01)
test_race_cases_max_profit = test_race_cases.copy()

for group in test_race_cases_max_profit.keys():
    test_race_cases_max_profit[group] = apply_threshold(test_race_cases_max_profit[group], thresholds_mp[group])
    
total_cost = apply_financials(training_race_cases_max_profit)

total_accuracy = get_total_accuracy(training_race_cases_max_profit)

print ("")
print("Accuracy on training data: " + str(total_accuracy))
print ("")
print("Accuracy on test data:")
print(get_total_accuracy(test_race_cases_max_profit))
print("")

print("Cost on training data: ")
print('${:,.0f}'.format(total_cost))
print ("")
print("Cost on test data:")
print('${:,.0f}'.format(apply_financials(test_race_cases_max_profit)))
print("")



for group in training_race_cases_max_profit.keys():
    TPR = get_true_positive_rate(training_race_cases_max_profit[group])
    print("TPR for " + group + ": " + str(TPR))

print("")
for group in training_race_cases_max_profit.keys():
    FPR = get_false_positive_rate(training_race_cases_max_profit[group])
    print("FPR for " + group + ": " + str(FPR))

print("")
for group in training_race_cases_max_profit.keys():
    FNR = get_false_negative_rate(training_race_cases_max_profit[group])
    print("FNR for " + group + ": " + str(FNR))


print("")
for group in training_race_cases_max_profit.keys():
    TNR = get_true_negative_rate(training_race_cases_max_profit[group])
    print("TNR for " + group + ": " + str(TNR))

print("")
for group in training_race_cases_max_profit.keys():
    print("Threshold for " + group + ": " + str(thresholds_mp[group]))

print("")    
