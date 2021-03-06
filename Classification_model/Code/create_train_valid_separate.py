import pandas as pd
import numpy as np
import sys

def class1(x):
	if x >= 0:
		return 2
	else:
		return 1
# up  and down
#6628 and 5947
#7153 and 5729
def class0(x):
	if x >= 0:
		return 0
	else:
		return 1

if len(sys.argv)>1:
	y = sys.argv[1]

	#input 
	# python create_train_valid.py (no. of training years),(no.of test years),yr1,yr2....
	# python create_train_valid.py 2,2,1,1992,1993,1994,1995,1996
	y = map(int,y.split(','))
	print y
	no_tr = y[0]
	no_vd = y[1]
	no_ts = y[2]

	Train = []
	Valid = []
	Test = []
	for i in range(no_tr):
		Train.append(y[3+i])
	for j in range(no_vd):
		Valid.append(y[3+no_tr+j])
	for k in range(no_ts):
		Test.append(y[3+no_tr+no_vd+k])
else:
	Train = [1991, 1992, 1993, 1994]
	Valid = [1995, 1996, 1997]
	Test = [1998,1999]
print Train, Valid, Test

print('Read Data')
data  = pd.read_csv('../Data/Final_new_dataset.csv')
f = open('../Data/col_names.txt', 'r')
c = f.readlines()
f.close()
cols = []
cols.append('date')
for i in c:
	cols.append(i.split('\n')[0])

#cols.append('zfret0')
output_data = data['zfret1']
data['zfret1'] = map(class1,output_data)
#data['zfret0'] = map(class0, output_data)



print 'Form Groups'
leng = len(data)
data_groups = data.groupby(by='zfret1')
data_1 = data_groups.get_group(1)
z1 = np.array(data_1.index)
data_2 = data_groups.get_group(2)
z2 = np.array(data_2.index)


print 'Creating Training Dataset'
train_data1 = data_1.ix[z1[:20000]]
train_data2 = data_2.ix[z2[:20000]]
train_data = pd.concat([train_data1, train_data2])

z = np.array(train_data.index)
np.random.shuffle(z)
train_data.reindex(np.random.permutation(train_data.index))

print 'Creating Validation Dataset'
valid_data1 = data_1.ix[z1[20000:40000]]
valid_data2 = data_2.ix[z2[20000:40000]]
valid_data = pd.concat([valid_data1, valid_data2])

valid_data.reindex(np.random.permutation(valid_data.index))




print 'Creating Test Dataset'
test_data1 = data_1.ix[z1[40000:]]
test_data2 = data_2.ix[z2[40000:]]
test_data = pd.concat([test_data1, test_data2])

valid_data.reindex(np.random.permutation(valid_data.index))

name_tr = '_'.join(map(str, Train))
name_vd = '_'.join(map(str, Valid))
name_ts = '_'.join(map(str, Test))

print 'Storing Training, Validation and Test files'
train_data[cols].to_csv('../Data/Train_'+name_tr+'.csv', index = False)
valid_data[cols].to_csv('../Data/Valid_'+name_vd+'.csv', index = False)
test_data[cols].to_csv('../Data/Test_'+name_ts+'.csv', index = False)




