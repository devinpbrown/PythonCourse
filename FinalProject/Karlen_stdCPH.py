import pandas as pd
from lifelines import CoxPHFitter

data = pd.read_csv('projectdata.csv')

cph_data = data[['supp_term', 'time', 'rivalry', 'govsupp', 'powerkin', 'demsupp', 'postcoldwar', 'leadership_change', 'gdp_downturn', 'sponsor_conflict', 'sanction_threat', 'sanction']]
cph_data = cph_data.dropna()


cph=CoxPHFitter()
cph.fit(cph_data, 'time', event_col='supp_term')
cph.print_summary()
