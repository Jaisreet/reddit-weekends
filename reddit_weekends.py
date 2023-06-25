import sys
import pandas as pd
import numpy as np
from scipy import stats
from datetime import date
import matplotlib.pyplot as plt



OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]
    counts = pd.read_json(reddit_counts, lines=True)
    
    #only taking the values from 2012 and 2013 and canada
    filtered = counts[(counts['date'].dt.year >= 2012) & (counts['date'].dt.year <= 2013) & (counts['subreddit'] == 'canada')]

    # separting weekends and weekdays
    weekdays = filtered[filtered['date'].dt.weekday < 5]
    weekends = filtered[filtered['date'].dt.weekday >= 5]
   
    #initial test
    initial_ttest_p = stats.ttest_ind(weekdays['comment_count'], weekends['comment_count']).pvalue
    initial_weekday_normality_p = stats.normaltest(weekdays['comment_count']).pvalue
    initial_weekend_normality_p = stats.normaltest(weekends['comment_count']).pvalue
    initial_levene_p = stats.levene(weekdays['comment_count'], weekends['comment_count']).pvalue

    #fix 1 - transforming data using np.log (seemed better than others)

    transformed_weekday = np.log(weekdays['comment_count'])
    transformed_weekend = np.log(weekends['comment_count'])
    plt.hist(transformed_weekday, alpha=0.5, label='Weekdays')
    plt.hist(transformed_weekend, alpha=0.5, label='Weekends')
    plt.xlabel('Transformed Comment Count')
    plt.ylabel('Frequency')
    plt.legend()
    #plt.show()

    transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    transformed_levene_p = stats.levene(transformed_weekday, transformed_weekend).pvalue

    # Fix 2 - Central Limit Theorem
    filtered['year'] = filtered['date'].dt.isocalendar().year
    filtered['week'] = filtered['date'].dt.isocalendar().week

    grouped = filtered.groupby(['year', 'week', filtered['date'].dt.weekday])

    weekly_means = grouped['comment_count'].mean().reset_index()

    weekly_weekday = weekly_means[weekly_means['date'] < 5]['comment_count']
    weekly_weekend = weekly_means[weekly_means['date'] >= 5]['comment_count']


    weekly_weekday_normality_p = stats.normaltest(weekly_weekday).pvalue
    weekly_weekend_normality_p = stats.normaltest(weekly_weekend).pvalue
    weekly_levene_p = stats.levene(weekly_weekday, weekly_weekend).pvalue
    weekly_ttest_p = stats.ttest_ind(weekly_weekday, weekly_weekend).pvalue


    # Fix 3 - a non-parametric test
    utest_p = stats.mannwhitneyu(weekdays['comment_count'], weekends['comment_count'], alternative='two-sided').pvalue


    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p,
        initial_weekday_normality_p=initial_weekday_normality_p,
        initial_weekend_normality_p=initial_weekend_normality_p,
        initial_levene_p=initial_levene_p,
        transformed_weekday_normality_p=transformed_weekday_normality_p,
        transformed_weekend_normality_p=transformed_weekend_normality_p,
        transformed_levene_p=transformed_levene_p,
        weekly_weekday_normality_p=weekly_weekday_normality_p,
        weekly_weekend_normality_p=transformed_weekend_normality_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest_ps,
    ))



if __name__ == '__main__':
    main()
