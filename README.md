# Netflix Userbase Statistics
by [Tomáš Boďa](https://github.com/TomasBoda)

## Dataset
The dataset was download from [kaggle.com](https://www.kaggle.com/datasets/arnavsmayan/netflix-userbase-dataset?resource=download) and is used only for educational purposes.

## External Libraries
The project uses two external libraries:
- [Pandas](https://pandas.pydata.org/) for reading `CSV` files
- [Scipy](https://scipy.org/) for calculating the critical values of the Student's T-test and the Pearson's Chi-Squared Test

## Abstract
The aim of this statistical project is to analyze the Netflix global userbase and gain insights into relationships between different user data to find out correlations and associations between different factors of Netflix usage among its consumers.

First and foremost, we will look at the age of Netflix users in association of their primary device they stream Netflix on. Since smart TVs have become popular in the last decade, we will try to analyze whether there are any differerences in the average age of people streaming Netflix on smart TVs in comparison to people streaming Netflix on laptops.

Secondly, we will try to find out whether there is any correlation between the country of origin of individual users and the device they primarily stream Netflix on.

## Dataset Analysis
The dataset consists of 2500 users, each provided with data such as gender, age, country of origin, primary device, subscription type, plan duration and many more.

Since we are performing two statistical analyses with only a specific subset of data from this dataset, let's look at what kind of values does this dataset provide and what we will need to extract.

Firstly, we load the dataset into our Python project.
```python
data = pandas.read_csv('netflix_userbase.csv')
```
Next, let's see what the minimum, maximum and average age of our users are.
```python
ages = data['Age']

print('Mininum Age:', min(ages))
print('Maximum Age:', max(ages))
print('Average Age:', sum(int(age) for age in ages) / len(ages))

# Minimum Age: 26
# Maximum Age: 51
# Average Age: 38.7956
```
Moreover, let's find out what countries the Netflix users are from.
```python
countries = {}

for country in data['Country']:
    if country not in countries:
        countries[country] = 0
    countries[country] += 1

for country, count in countries.items():
    print(country + ':', count)

# United States: 451
# Canada: 317
# United Kingdom: 183
# Australia: 183
# Germany: 183
# France: 183
# Brazil: 183
# Mexico: 183
# Spain: 451
# Italy: 183
```
Lastly, let's analyze the different kinds of devices Netflix users use for streaming.
```python
devices = {}
for device in data['Device']:
    if device not in devices:
        devices[device] = 0
    devices[device] += 1

for device, count in devices.items():
    print(device + ':', count)

# Smartphone: 621
# Tablet: 633
# Smart TV: 610
# Laptop: 636
```

## Student's T-test
Firstly, we will perform the Student's T-test to gain insights into the age differences between users who stream Netflix on smart TVs in comparison to people streaming Netflix on laptops.

As the null hypothesis (H0) we will consider the following: **There is NO significant age difference between Smart TV and Laptop user**. As the alternative hypothesis (H1), we will consider the exact opposite: **There is a SIGNIFICANT age difference between Smart TV and Laptop users**.

Initially, we will extract our desired values from the dataset.
```python
laptop_users = data[data['Device'] == 'Laptop']
smart_tv_users = data[data['Device'] == 'Smart TV']

laptop_ages = laptop_users['Age']
smart_tv_ages = smart_tv_users['Age']
```
Then, we will calculate the **mean** and **variance** values together with the **pooled variance** value.
```python
# means
mean_smart_tv = sum(smart_tv_ages) / len(smart_tv_ages)
mean_laptop = sum(laptop_ages) / len(laptop_ages)

# variances
variance_smart_tv = sum((x - mean_smart_tv) ** 2 for x in smart_tv_ages) / (len(smart_tv_ages) - 1)
variance_laptop = sum((x - mean_laptop) ** 2 for x in laptop_ages) / (len(laptop_ages) - 1)

# pooled variance
pooled_variance = ((len(smart_tv_ages) - 1) * variance_smart_tv + (len(laptop_ages) - 1) * variance_laptop) / (len(smart_tv_ages) + len(laptop_ages) - 2)
```
Finally, we will calculate the **degrees of freedom**, set our **significance level (alpha)** to `0.05` (5%) and calculate the `critical T-value` together with our most important value - the **T-statistic**.
```python
degrees_of_freedom = len(smart_tv_ages) + len(laptop_ages) - 2
significance_level = 0.05

critical_t_value = t.ppf(1 - significance_level, degrees_of_freedom)
t_statistic = (mean_smart_tv - mean_laptop) / (pooled_variance * ((1 / len(smart_tv_ages)) + (1 / len(laptop_ages)))) ** 0.5
```
Now we have everything we need to either **reject** or **not reject** our null hypothesis.
```python
if abs(t_statistic) > critical_t_value:
    print("Null Hypothesis is REJECTED:", alt_hypothesis)
else:
    print("Null hypothesis is NOT REJECTED:", null_hypothesis)
```

### Results
After running the Student's T-test, we can see that our **null hypothesis has not been rejected**.

The **degrees of freedom** value is set to `1244`, the **critical T-value** is calculated to be `1.65` and the **T-statistic** is `0.84`. Since the **T-statistic** is far less than the **critical T-value**, we can conclude that the null hypothesis has not been rejected and therefore, **there is NO significant age difference between smart TV and laptop users**.

Based on our results, we can conclude that the older generation is quite progressive as far as technology is concerned and there are no major differences between generations in terms of device they stream Netflix on.

## Pearson's Chi-squared Test
Secondly, we will perform the Pearson's Chi-squared Test on categorical data to check if there is any correlation between the viewers' country of origin and the device they usually stream Netflix on. This could give us insights into preferred devices by country.

As the null hypothesis (H0) we will consider the following: **There is NO relationship between country and device**. As our alternative hypothesis (H1), we will consider the exact opposite: **There is a RELATIONSHIP between country and device**.

Again, we will firstly extract the desired values from the dataset and check whether we have the same amount of device and country entries.
```python
countries = data['Country']
devices = data['Device']

assert len(countries) == len(devices), 'The number of countries doesn\'t match the number of devices'
```
For the Pearson's Chi-Squared Test, we need to pre-calculate two things: the **observed frequencies** and the **expected frequencies**. Based on the differences of these values, we will analyse the correlation between countries and devices.

First, we will calculate the observed frequencies. For each unique country, we will calculate the total number of each device type.
```python
# observed frequencies
observed_frequencies = {}

for i in range(total_entries):
    country = countries[i]
    device = devices[i]

    if country not in observed_frequencies:
        observed_frequencies[country] = {}
    if device not in observed_frequencies[country]:
        observed_frequencies[country][device] = 0
    observed_frequencies[country][device] += 1
```
Next, we need to calculate the expected frequencies, which represent expected values with no correlation whatsoever.
```python
# expected frequencies preparation
row_totals = {}
column_totals = {}
grand_total = sum(sum(row.values()) for row in observed_frequencies.values())

for country, devices in observed_frequencies.items():
    row_totals[country] = sum(devices.values())
    for device, frequency in devices.items():
        if device not in column_totals:
            column_totals[device] = frequency
        else:
            column_totals[device] += frequency

# expected frequencies
expected_frequencies = {}

for country, devices in observed_frequencies.items():
    expected_frequencies[country] = {}
    for device, frequency in devices.items():
        expected_frequency = (row_totals[country] * column_totals[device]) / grand_total
        expected_frequencies[country][device] = expected_frequency
```
After we have successfully prepared our data, we can calculate the **chi-square** value based on our observed and expected frequencies.
```python
# chi-squared calculation
chi_squared = 0

for country, devices in observed_frequencies.items():
    for device, frequency in devices.items():
        expected_count = expected_frequencies[country][device]
        chi_squared += ((frequency - expected_count) ** 2) / expected_count
```
The last thing that remains is to define the **significance level (alpha)**, calculate the **degrees of freedom** and get the **critical value**.
```python
degrees_of_freedom = (len(row_totals) - 1) * (len(column_totals) - 1)
significance_level = 0.05
critical_value = chi2.ppf(1 - significance_level, degrees_of_freedom)
```
Now we have everything we need to either **reject** or **not reject** our null hypothesis.
```python
if chi_squared < critical_value:
    print('Null hypothesis is NOT REJECTED:', null_hypothesis)
else:
    print('Null hypothesis is REJECTED:', alt_hypothesis)
```

### Results
After running the Pearson's Chi-squared Test, we can see that our **null hypothesis has not been rejected**.

The **degrees of freedom** value is set to `27`, the **critical value** is calculated to be `40.11` and the **chi-squared** value is `32.42`. Since the **chi-squared** value is less than the **critical value**, we can conclude that the null hypothesis has not been rejected and therefore, **There is NO major relationship or correlation between the country of origin and streaming devices**.

by [Tomáš Boďa](https://github.com/TomasBoda)