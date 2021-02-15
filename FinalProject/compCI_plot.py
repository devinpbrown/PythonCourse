import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.figure()
plt.xlim(-2, 2)
plt.ylim(0, 11)
plt.yticks(np.arange(0, 10, step=1))
plt.yticks([10,9,8,7,6,5,4,3,2,1,0], ['rivalry', 'govsupp', 'kinship', 'demsupp', 'postcoldwar', 'lead_change', 'gdp_downturn', 'sponsor_conflict', 'sanction_threat', 'sanction'])
plt.vlines(0, ymin=0, ymax=11, linestyle='--', color='black')

cph = np.arange(1.1,11.1,1)
cph_coef= np.flip(np.array([-0.41,-0.60,-1.50,-0.1,0.34,0.58,-0.01,0.72,-0.99,-0.24])) #These are flipped because I want my chart to read from top to bottom, but the array on line 13 is ascending
cph_ci_lower = np.flip(np.array([-0.870825, -0.914233,-2.339458,-0.526808,0.040243,-0.053459,-0.044120,-0.194817,-2.981379,-0.614149]))
cph_ci_high = np.flip(np.array([0.046152,-0.276722,-0.668689, 0.324938,0.639407,1.205707, 0.023272,1.632280,0.992205,0.139204]))

bayes = np.arange(1,11,1)
bayes_coef = np.flip(np.array([-0.45,-0.66,-1.61,-0.15,0.33,0.53,-0.0099,0.6,-1.38,-0.3]))
bayes_low = bayes_coef - 2 * (np.flip(np.array([0.23,0.16,0.45,0.22,0.15,0.32,0.02,0.48,1.27,0.19]))) #This array is the standard deviation, since Pystan doesn't give -95 adn +95 confidence intervals
bayes_high = bayes_coef + 2 * (np.flip(np.array([0.23,0.16,0.45,0.22,0.15,0.32,0.02,0.48,1.27,0.19])))

re = np.arange(0.9,10.9,1)
re_coef = np.flip(np.array([-1.99,0.3,0.11,0.81,0.11,0.1,0.0005,0.2,-7.99,-0.99]))
re_low = re_coef - 2 * (np.flip(np.array([0.41,0.34,0.88,0.54,0.35,10.37,0.04,10.12,6.28,0.51])))
re_high = re_coef + 2 * (np.flip(np.array([0.41,0.34,0.88,0.54,0.35,10.37,0.04,10.12,6.28,0.51])))

plt.plot(cph_coef, cph, 'o', color='r')
plt.hlines(cph, xmin= cph_ci_lower, xmax=cph_ci_high, linestyle= '-', color='r', label="Basic CPH")
plt.plot(bayes_coef, bayes, 'o', color='g')
plt.hlines(bayes, xmin = bayes_low, xmax=bayes_high, linestyle='-', color='g', label="Bayseian CPH")
plt.plot(re_coef, re, 'o', color='b')
plt.hlines(re, xmin=re_low, xmax=re_high, linestyle='-', color='b', label="Bayseian CPH with Random Effects")
plt.legend()
plt.show()
