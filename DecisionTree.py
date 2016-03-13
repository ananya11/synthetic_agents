import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import Imputer



def _replace_non_numeric(df):
	df["SEX"] = df["SEX"].apply(lambda gender: 1 if gender == "male" or "Male"  else 2)
	df["HINCP"] = df["HINCP"].apply(lambda income: 1 if 0<=income<25000 else 2 if 25000<=income<75000 else 3)
	try:
		df["BIN"] = df["BIN"].apply(lambda bin: 1 if bin == "low" else 2 if bin == "medium" else 3)
	except:
		print "no bin"
	return df


def classify(test_data, final_data):
	train_df = _replace_non_numeric(pd.read_csv('data/train.csv'))
	et = ExtraTreesClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0)
	columns = ["AGEP", "SEX", "HINCP", "PERSONS"]

	labels = train_df["BIN"].values
	features = train_df[list(columns)].values

	et_score = cross_val_score(et, features, labels, n_jobs=-1).mean()

	print("{0} -> ET: {1}").format(columns, et_score)

	imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
	imp.fit(features)

	test_df= _replace_non_numeric(pd.read_csv(test_data))

	et.fit(features,labels)

	predictions = et.predict(imp.transform(test_df[columns].values))
	test_df["BIN"]=pd.Series(predictions)
	test_df.to_csv(final_data, cols=['PID','AGEP','SEX','HOME_ZIPCODE', 'HINCP', 'HID', 'PERSONS', 'BIN'], index=False)
