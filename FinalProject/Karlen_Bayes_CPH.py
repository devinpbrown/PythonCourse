import pandas as pd
import pystan
import math

data = pd.read_csv('projectdata.csv')

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
