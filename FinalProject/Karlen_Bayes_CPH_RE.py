import pandas as pd
import numpy as np
import pystan
import math

data = pd.read_csv('projectdata.csv')

#getting average of times in the dataset to inform my intercept prior:
math.log(np.mean(data['time']))
# = 1.3654455136492727 - so i'll use -1.4 as my prior for the single intercept

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
