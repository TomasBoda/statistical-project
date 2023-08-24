import pandas
from tests import student_t_test, pearson_chi_squared_test

# load the dataset
data = pandas.read_csv('netflix_userbase.csv')

# Student's T-test
# test the differences in average age of people who stream Netflix on smart TV vs laptop
student_t_test(data)

# Pearson's Chi-squared Test
# test the relationship or correlation between the viewers' country of origin and their primary streaming device
pearson_chi_squared_test(data)