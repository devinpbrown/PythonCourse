import csv
import pandas as pd
import numpy as np
import wbdata
from scipy import stats

def linreg(y, x):
    b = np.linalg.inv(x.T @ x) @ x.T @ y #regression and coefficients
    e = y - (x @ b) #finding error term
    sigsq = (e.T @ e)/(x.shape[0] - x.shape[1]) #sigma squared - I didn't subtract another 1 for degress of freedom becuase x.shape[1] includes the list of 1s used for B0
    var = np.diag(np.multiply(sigsq, np.linalg.inv(x.T @ x))) #variance
    SE = np.sqrt(var).reshape(3,1) #standard error
    t = stats.t.ppf(.975, (x.shape[0] - x.shape[1])) #getting t-stat - just as above, I didn't subtract an extra 1 for degrees of freedom since x.shape[1] is already 3 (not 2) becuase of the column of 1s
    plus = b + SE * t #confidence interval plus
    minus = b - SE * t #confidence interval minus
    CI = np.hstack([minus, plus]) #confidence intervals into array
    output = pd.DataFrame(np.hstack([b, SE, CI]), columns=['Coefficients', 'Standard Error', 'CI-', 'CI+']) #creating a dataframe with my coefficients, standard error, and confidence intervals
    print("Here are the results of your regression")
    print(output)
    return output
#an extra comment for something completely unrelated to the previous code

