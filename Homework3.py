import pystan
import pandas as pd
import numpy as np

data = pd.read_csv('trend2.csv')
data = data.drop(columns=['cc'])
data.dropna(inplace=True)

country, unique = pd.factorize(np.array(data.country))
country += 1
year, unique2 = pd.factorize(np.array(data.year))
year += 1

two_intercept = """
data {
  int<lower=0> N;
  int<lower=0> J;
  int<lower=0> K;
  int<lower=1,upper=J> country[N];
  int<lower=1, upper=K> year[N];
  matrix[N,2] X;
  vector[N] y;
}
parameters {
  real a;
  vector[J] a1;
  vector[K] a2;
  vector[2] B;
  real mu_a1;
  real<lower=0,upper=100> sigma_a1;
  real mu_a2;
  real<lower=0,upper=100> sigma_a2;
  real<lower=0,upper=100> sigma_y;
}
transformed parameters {

  vector[N] y_hat;

  for (i in 1:N)
    y_hat[i] = a + a1[country[i]] + a2[year[i]] + X[i, 1:2] * B;
}
model {
  a ~ normal (0,1);
  sigma_a1 ~ gamma(1,0.5);
  mu_a1 ~ normal(0,10);
  a1 ~ normal (mu_a1, sigma_a1);
  sigma_a2 ~ gamma(1,0.5);
  mu_a2 ~ normal(0,10);
  a2 ~ normal (mu_a2, sigma_a2);

  B ~ normal (0, 1);

  sigma_y ~ uniform(0, 100);
  y ~ normal(y_hat, sigma_y);
}
"""

two_intercept_data = {'N': data.shape[0],
                          'J': len(np.unique(country)),
                          'K': len(np.unique(year)),
                          'country': country,
                          'year': year,
                          'X': data[['gini_net', 'rgdpl']],
                          'y': data['church2']}


ModelFit = pystan.stan(model_code=two_intercept, data=two_intercept_data, iter=1250, chains=2)
#I ran the model with 1000 iterations and it wasn't converging 1250 seems to do the trick
return ModelFit

#Informative, incorrect prior

two_intercept_badprior = """
data {
  int<lower=0> N;
  int<lower=0> J;
  int<lower=0> K;
  int<lower=1,upper=J> country[N];
  int<lower=1, upper=K> year[N];
  matrix[N,2] X;
  vector[N] y;
}
parameters {
  real a;
  vector[J] a1;
  vector[K] a2;
  vector[2] B;
  real mu_a1;
  real<lower=0,upper=100> sigma_a1;
  real mu_a2;
  real<lower=0,upper=100> sigma_a2;
  real<lower=0,upper=100> sigma_y;
}
transformed parameters {

  vector[N] y_hat;

  for (i in 1:N)
    y_hat[i] = a + a1[country[i]] + a2[year[i]] + X[i, 1:2] * B;
}
model {
  a ~ normal (0,1);
  sigma_a1 ~ gamma(1,0.5);
  mu_a1 ~ normal(0,10);
  a1 ~ normal (mu_a1, sigma_a1);
  sigma_a2 ~ gamma(1,0.5);
  mu_a2 ~ normal(0,10);
  a2 ~ normal (mu_a2, sigma_a2);

  B ~ normal (4.3, 1); //10x higher than the estimate from the original model

  sigma_y ~ uniform(0, 100);
  y ~ normal(y_hat, sigma_y);
}
"""

two_intercept_data = {'N': data.shape[0],
                          'J': len(np.unique(country)),
                          'K': len(np.unique(year)),
                          'country': country,
                          'year': year,
                          'X': data[['gini_net', 'rgdpl']],
                          'y': data['church2']}


ModelFit2 = pystan.stan(model_code=two_intercept_badprior, data=two_intercept_data, iter=1250, chains=2)
return ModelFit2

#Adding an informative prior (10x the original estimate) pulls the Beta estimate toward the former information but not nearly as drastically as I expected. The original estimate was 0.43 and with the prior it was 0.48. 
