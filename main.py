import pandas
from tests import student_t_test, pearson_chi_squared_test

# load the dataset
data = pandas.read_csv('netflix_userbase.csv')

# Student's T-test
# test the differences in average age of people who watch Netflix on Smart TV vs Laptop
student_t_test(data)

# Pearson's Chi-squared Test
# test the relationship between the viewer's country of origin and their main streaming device
pearson_chi_squared_test(data)