from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
import pandas as pd
import numpy as np
import os
os.chdir('Desktop/PythonClassNotes/KocPython2020/in-classMaterial/day17')
tt = pd.read_csv('immSurvey.csv')

alphas = tt.stanMeansNewSysPooled
sample = tt.textToSend

from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(ngram_range=(1, 2),token_pattern=r'\b\w+\b', min_df=1)
X = vec.fit_transform(sample)
pd.DataFrame(X.toarray(), columns=vec.get_feature_names())

from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, alphas,
random_state=1)

rbf = ConstantKernel(1.0) * RBF(length_scale=1.0)
gpr = GaussianProcessRegressor(kernel=rbf, alpha=1e-8)

gpr.fit(Xtrain.toarray(), ytrain)

mu_s, cov_s = gpr.predict(Xtest.toarray(), return_cov=True)

np.corrcoef(ytest, mu_s)

#with bigrams, my accuracy dropped from 0.683 to 0.646
