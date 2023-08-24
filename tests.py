from scipy.stats import t, chi2

def student_t_test(data):
    print('-------------------------------------------')
    print('Student\'s T-test                          |')
    print('-------------------------------------------')

    null_hypothesis = 'There is NO significant age difference between smart TV and laptop users'
    alt_hypothesis = 'There is SIGNIFICANT age difference between smart TV and laptop users'

    print('Null hypothesis:', null_hypothesis)
    print('Alt hypothesis:', alt_hypothesis)

    laptop_users = data[data['Device'] == 'Laptop']
    smart_tv_users = data[data['Device'] == 'Smart TV']

    laptop_ages = laptop_users['Age']
    smart_tv_ages = smart_tv_users['Age']

    # means
    mean_smart_tv = sum(smart_tv_ages) / len(smart_tv_ages)
    mean_laptop = sum(laptop_ages) / len(laptop_ages)

    # variances
    variance_smart_tv = sum((x - mean_smart_tv) ** 2 for x in smart_tv_ages) / (len(smart_tv_ages) - 1)
    variance_laptop = sum((x - mean_laptop) ** 2 for x in laptop_ages) / (len(laptop_ages) - 1)

    pooled_variance = ((len(smart_tv_ages) - 1) * variance_smart_tv + (len(laptop_ages) - 1) * variance_laptop) / (len(smart_tv_ages) + len(laptop_ages) - 2)

    degrees_of_freedom = len(smart_tv_ages) + len(laptop_ages) - 2
    significance_level = 0.05

    critical_t_value = t.ppf(1 - significance_level, degrees_of_freedom)
    t_statistic = (mean_smart_tv - mean_laptop) / (pooled_variance * ((1 / len(smart_tv_ages)) + (1 / len(laptop_ages)))) ** 0.5

    print()
    print('Significance level:', significance_level)
    print('Degrees of Freedom:', degrees_of_freedom)
    print('Critical T-value:', critical_t_value)
    print('T-statistic:', t_statistic)
    print()

    # results
    if abs(t_statistic) > critical_t_value:
        print('Null Hypothesis is REJECTED:', alt_hypothesis)
    else:
        print('Null hypothesis is NOT REJECTED:', null_hypothesis)

    print('-------------------------------------------')

def pearson_chi_squared_test(data):
    print('-------------------------------------------')
    print('Pearson\'s Chi-squared Test                |')
    print('-------------------------------------------')

    null_hypothesis = 'There is NO relationship between country and device'
    alt_hypothesis = 'There is a RELATIONSHIP between country and device'

    print('Null hypothesis:', null_hypothesis)
    print('Alt hypothesis:', alt_hypothesis)

    countries = data['Country']
    devices = data['Device']

    total_entries = len(countries)

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

    # chi-squared calculation
    chi_squared = 0
    for country, devices in observed_frequencies.items():
        for device, frequency in devices.items():
            expected_count = expected_frequencies[country][device]
            chi_squared += ((frequency - expected_count) ** 2) / expected_count

    # degrees of freedom and critical value
    degrees_of_freedom = (len(row_totals) - 1) * (len(column_totals) - 1)
    significance_level = 0.05
    critical_value = chi2.ppf(1 - significance_level, degrees_of_freedom)

    print()
    print('Significance level:', significance_level)
    print('Degrees of Freedom:', degrees_of_freedom)
    print('Critical Value:', critical_value)
    print('Chi-squared:', chi_squared)
    print()

    # results
    if chi_squared < critical_value:
        print('Null hypothesis is NOT REJECTED:', null_hypothesis)
    else:
        print('Null hypothesis is REJECTED:', alt_hypothesis)

    print('-------------------------------------------')