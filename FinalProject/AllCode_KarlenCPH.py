import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
import pystan
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

data = pd.read_csv('projectdata.csv')

cph_data = data[['supp_term', 'time', 'rivalry', 'govsupp', 'powerkin', 'demsupp', 'postcoldwar', 'leadership_change', 'gdp_downturn', 'sponsor_conflict', 'sanction_threat', 'sanction']]
cph_data = cph_data.dropna()

cph=CoxPHFitter()
cph.fit(cph_data, 'time', event_col='supp_term')
cph.print_summary()

#####Now starting the Pystan basic CPH model:#####

#getting average of times in the dataset to inform my intercept prior:
math.log(np.mean(data['time']))
# = 1.3654455136492727 - so i'll use -1.4 as my prior for the single intercept

#splitting my data into censored and uncensored, narrowing down to my necessary variables and dropping missing values
cens = data[data['supp_term']==0]
cens = cens[['time','rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]
cens = cens.dropna()
cens_vars = cens[['rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]

uncens = data[data['supp_term']==1]
uncens = uncens[['time','rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]
uncens = uncens.dropna()
uncens_vars = uncens[['rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]


term_data = {'N_uncensored': len(uncens),
            'N_censored':len(cens),
            'NC': 10,
            'X_censored': cens_vars,
            'X_uncensored': uncens_vars,
            'times_censored': cens['time'],
            'times_uncensored': uncens['time']}

term_model_repeat = """
data {
    int<lower=1> N_uncensored;
    int<lower=1> N_censored;
    int<lower=0> NC;
    matrix[N_censored,NC] X_censored;
    matrix[N_uncensored,NC] X_uncensored;
    vector<lower=0>[N_censored] times_censored;
    vector<lower=0>[N_uncensored] times_uncensored;
}
parameters {
    vector[NC] betas;
    real intercept;
}
model {
    betas ~ normal(0,10);
    intercept ~ normal(-1.4,3);
    target += exponential_lpdf(times_uncensored | exp(intercept+X_uncensored*betas));
    target += exponential_lccdf(times_censored | exp(intercept+X_censored*betas));
}
generated quantities {
    vector[N_uncensored] times_uncensored_sampled;
    for(i in 1:N_uncensored) {
        times_uncensored_sampled[i] = exponential_rng(exp(intercept+X_uncensored[i,]*betas));
    }
} """


cph_mod = pystan.StanModel(model_code=term_model_repeat)
HazardFit = cph_mod.sampling(data=term_data, chains=4, n_jobs=2, iter=2000)
HazardFit

#####Now starting CPH in Pystan with Random Effects:#####

#splitting my data into censored and uncensored, narrowing down to my necessary variables and dropping missing values
#This model includes random effects for each supporting country so I included the variable data['external_name'] and factorized it for both samples
cens = data[data['supp_term']==0]
cens = cens[['external_name','time','rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]
cens = cens.dropna()

cens_supp_state, unique = pd.factorize(np.array(cens.external_name))
cens_supp_state += 1

cens_vars = cens[['rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]

uncens = data[data['supp_term']==1]
uncens = uncens[['external_name','time','rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]
uncens = uncens.dropna()

uncens_supp_state, unique2 = pd.factorize(np.array(uncens.external_name))
uncens_supp_state += 1

uncens_vars = uncens[['rivalry','govsupp','powerkin','demsupp','postcoldwar','leadership_change','gdp_downturn','sponsor_conflict','sanction_threat','sanction']]


term_data = {'N_uncensored': len(uncens),
            'N_censored':len(cens),
            'NC': 10,
            'X_censored': cens_vars,
            'X_uncensored': uncens_vars,
            'times_censored': cens['time'],
            'times_uncensored': uncens['time'],
            'cens_supp_state': cens_supp_state,
            'uncens_supp_state': uncens_supp_state,
            'N_css': len(np.unique(cens_supp_state)),
            'N_uss': len(np.unique(uncens_supp_state))}

term_model_repeat = """
data {
    int<lower=1> N_uncensored;
    int<lower=1> N_censored;
    int<lower=0> NC;
    matrix[N_censored,NC] X_censored;
    matrix[N_uncensored,NC] X_uncensored;
    vector<lower=0>[N_censored] times_censored;
    vector<lower=0>[N_uncensored] times_uncensored;
    int<lower=0> N_css;
    int<lower=0> N_uss;
    int<lower=1, upper=N_css> cens_supp_state[N_censored];
    int<lower=1, upper=N_uss> uncens_supp_state[N_uncensored];
}
parameters {
    vector[NC] betas;
    real intercept;
    vector[N_css] cens_intercept;
    vector[N_uss] uncens_intercept;
    real mu_cens_int;
    real mu_uncens_int;
    real<lower=0> sig_cens_int;
    real<lower=0> sig_uncens_int;
}
model {
    betas ~ normal(0,10);
    intercept ~ normal(-1.4, 3);

    mu_cens_int ~ normal(0,0.1);
    sig_cens_int ~ gamma(0.1, 0.1);
    cens_intercept ~ normal(mu_cens_int, sig_cens_int);

    mu_uncens_int ~ normal(0,0.1);
    sig_uncens_int ~ gamma(0.5, 0.1);
    uncens_intercept ~ normal(mu_uncens_int, sig_uncens_int);

    for (i in 1:N_uss){
    target += exponential_lpdf(times_uncensored[i] | exp(intercept+ uncens_intercept[i]+X_uncensored[i,]*betas));}
    for (i in 1:N_css){
    target += exponential_lccdf(times_censored[i] | exp(intercept+cens_intercept[i]+X_censored[i,]*betas));}
}
generated quantities {
    vector[N_uncensored] times_uncensored_sampled;
    for(i in 1:N_uncensored) {
        times_uncensored_sampled[i] = exponential_rng(exp(intercept+uncens_intercept[uncens_supp_state[i]]+X_uncensored[i,]*betas));
    }
} """


cph_mod = pystan.StanModel(model_code=term_model_repeat)
REHazardFit = cph_mod.sampling(data=term_data, chains=2, n_jobs=2, iter=2500)
REHazardFit


#####This is the code used to create my results graph from each model:#####

plt.figure()
plt.xlim(-2, 2)
plt.ylim(0, 11)
plt.yticks(np.arange(0, 10, step=1))
plt.yticks([10,9,8,7,6,5,4,3,2,1,0], ['rivalry', 'govsupp', 'kinship', 'demsupp', 'postcoldwar', 'lead_change', 'gdp_downturn', 'sponsor_conflict', 'sanction_threat', 'sanction'])
plt.vlines(0, ymin=0, ymax=11, linestyle='--', color='black')

cph = np.arange(1.1,11.1,1) #These values supply the y-values for my lines
cph_coef= np.flip(np.array([-0.41,-0.60,-1.50,-0.1,0.34,0.58,-0.01,0.72,-0.99,-0.24])) #These are flipped because I want my chart to read from top to bottom, but the array on line 171 is ascending
cph_ci_lower = np.flip(np.array([-0.870825, -0.914233,-2.339458,-0.526808,0.040243,-0.053459,-0.044120,-0.194817,-2.981379,-0.614149]))
cph_ci_high = np.flip(np.array([0.046152,-0.276722,-0.668689, 0.324938,0.639407,1.205707, 0.023272,1.632280,0.992205,0.139204]))

bayes = np.arange(1,11,1)
bayes_coef = np.flip(np.array([-0.45,-0.66,-1.61,-0.15,0.33,0.53,-0.0099,0.6,-1.38,-0.3])) #These are the coefficients for my simple CPH in pystan
bayes_low = bayes_coef - 2 * (np.flip(np.array([0.23,0.16,0.45,0.22,0.15,0.32,0.02,0.48,1.27,0.19]))) #This array is the standard deviation from the pystan simpl CPH, multiplied by two and subtracted to create the end point two standard deviations below my coefficients
bayes_high = bayes_coef + 2 * (np.flip(np.array([0.23,0.16,0.45,0.22,0.15,0.32,0.02,0.48,1.27,0.19]))) #This line adds 2*standard deviation to create the upper end point for my confidence interval

re = np.arange(0.9,10.9,1)
re_coef = np.flip(np.array([-1.99,0.3,0.11,0.81,0.11,0.1,0.0005,0.2,-7.99,-0.99])) #These are my coefficients for the Random Effects CPH model
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
