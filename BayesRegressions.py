import pandas as pd
data = pd.read_csv('turnout.csv') #This is in Desktop/PythonClassNotes/KocPython2020/in-classMaterial/day11

turnout_data = {'N': data.shape[0],
                'x': data['income'],
                'y': data['vote']}


turnout_model = """
data {{
    int<lower=0> N;     //number of data points
	vector[N] x;       // (we could also use real x[N] vectorized x values (used because our x values are continuous) Defining data that's going to come in
    int<lower=0, upper=1> y[N];     //sets up our expectation that y will be binary (int because 1 or 0, lower and upper making sure our model doesnt predict something beyond 1)
}}
parameters {        //this is setting up the right side of our equation
    real a;     //real number for our y-intercept
    real b;     //real number for our beta-values (DEVIN QUESTION: do we need to have a 'real variable' for every explanatory variable?)
}
transformed parameters {{
    vector[N] eta;
    eta = a + b*x;
}}
model {{
    a ~ normal(0,10);       //these two lines are providing information for the model, which in general, we want to be uninformative. So for example if we had older information we wanted to add age for voting adults into our model, we could add it here? (maybe if we were using age an an expv, we could add a ~ normal(16, 100) to give it better information?)
    b ~ normal(0,10);
    y ~ bernoulli_logit(eta);       //because we are running a logit, our y is actually a function to make sure that we get an s-shaped graph rather than a straight line
}}
"""

logitFit = pystan.stan(model_code=turnout_model, data=turnout_data, iter=1000, chains=2)

#          mean  se_mean    sd   2.5%    25%    50%    75%  97.5%  n_eff   Rhat
#a         0.27  5.2e-3   0.09   0.11   0.22   0.27   0.33   0.46    289    1.0
#b         0.23  1.4e-3   0.02   0.19   0.22   0.24   0.25   0.28    297    1.0


#CHANGING IT TO A PROBIT MODEL

import pandas as pd
data = pd.read_csv('turnout.csv')

turnout_data = {'N': data.shape[0],
                'x': data['income'],
                'y': data['vote']}


turnout_model_probit = """
data {
    int<lower=0> N;
	vector[N] x;
    int<lower=0, upper=1> y[N];
}
parameters {
    real a;
    real b;
}
transformed parameters {
    vector[N] eta;
    eta = a + b*x;
}
model {
    a ~ normal(0,10);
    b ~ normal(0,10);
    for(n in 1:N) y[n] ~ bernoulli(Phi(eta[n]));
}
"""

probitFit = pystan.stan(model_code=turnout_model_probit, data=turnout_data, iter=1000, chains=2)


##TODO: Generalize the logit model to take K predictors. Include age, educate, and income as predictors.

turnout_model_gen = """
data {
    int<lower=0> N;
    int<lower=0> K;
	matrix[N,K] X;
    int y[N];
}
parameters {
    real a;
    vector[K] B;
}
transformed parameters {
    vector[N] eta;
    eta = a + X*B;
}
model {
    a ~ normal(0,10);
    B ~ normal(0,10);
    y ~ bernoulli_logit(eta);
}
"""
turnout_data = {'N': data.shape[0],
                'K': 3,
                'X': data[['income','age','educate']],
                'y': data['vote']}

logitFit = pystan.stan(model_code=turnout_model_gen, data=turnout_data, iter=1000, chains=2)

#TODO: Make an indicator for the observation being of white race. Allow the intercepts of the logit to vary by race. Place priors on the mean and standard deviation of the random intercepts.

import pandas as pd
data = pd.read_csv('turnout.csv')

race = (data.race == 'white').astype(int)

for i in data.country:
    (data.country == i).astype(int)

turnout_data = {'N': data.shape[0],
                'K': 3,
                'X': data[['age','educate', 'income']],
                'race': race + 1,
                'y': data['vote']}

turnout_model_vint = """
data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N,K] X;
    int y[N];
    int<lower=1, upper=2> race[N];

}
parameters {
    real a;
    vector[2] re; //random effect for race
    real re_mu;
    real<lower=0> re_sigma
    vector[K] B;
}
transformed parameters {
    vector[N] eta;
    eta = a + B*x + re[race]; //race indexed at 1 and 2 (not actually an integer effect)
}
model {
    a ~ normal(0,10);
    re_mu ~ normal(0,10);
    re_sigma ~ gamma(1,.5); //david just likes using a gamma distribution on standard deviations
    re ~ normal(re_mu,re_sigma);
    B ~ normal(0,10);
    y ~ bernoulli_logit(eta);
}
"""

logitFit = pystan.stan(model_code=turnout_model_vint, data=turnout_data, iter=1000, chains=2)


#TODO: Allow the economic slopes and intercept to vary by race

import pandas as pd
data = pd.read_csv('turnout.csv')

race = (data.race == 'white').astype(int)

turnout_data = {'N': data.shape[0],
                'K': 2,
                'X': data[['age','educate']],
                'econ': data['income'],
                'race': race + 1,
                'y': data['vote']}

turnout_model_vint = """
data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N,K] X;
    int y[N];
    int<lower=1, upper=2> race[N];

}
parameters {
    real a;
    vector[2] re; //random effect for race
    real re_mu;
    real<lower=0> re_sigma
    vector[K] B;
    vector[econ] z;
    real mu_z;
    real<lower=0> sigma_z;
}
transformed parameters {
    vector[N] eta;
    eta = a + B*x + z*x + re[race]; //race indexed at 1 and 2 (not actually an integer effect)
}
model {
    a ~ normal(0,10);
    re_mu ~ normal(0,10);
    re_sigma ~ gamma(1,.5); //david just likes using a gamma distribution on standard deviations
    mu_z ~ normal(0,10)
    z ~ normal(mu_z, sigma_z)
    re ~ normal(re_mu,re_sigma);
    B ~ normal(0,10);
    y ~ bernoulli_logit(eta);
}
"""

logitFit = pystan.stan(model_code=turnout_model_vint, data=turnout_data, iter=1000, chains=2)
