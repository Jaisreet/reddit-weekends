## Analysis of Reddit Comments on Weekdays vs. Weekends

This project aims to investigate whether there is a difference in the number of Reddit comments posted on weekdays compared to weekends in the /r/canada subreddit. The provided data, extracted from the Reddit Comment archive, includes a count of daily comments in each Canadian-province subreddit and /r/canada itself.

### Problem Statement

The main question we seek to answer is whether there is a significant difference in the number of comments posted on weekdays and weekends in the /r/canada subreddit during the years 2012 and 2013.

### Data Preparation

The first step is to prepare the data by creating a DataFrame from the provided JSON file (`reddit-counts.json.gz`). The data is loaded using Pandas, and the relevant years (2012 and 2013) as well as the /r/canada subreddit are selected. The comments are then divided into weekdays (Saturday and Sunday) and weekdays (Monday to Friday) based on the day of the week using `datetime.date.weekday`.

### Student's T-Test

To determine if there is a significant difference in the number of comments between weekdays and weekends, we perform a Student's T-test using the `scipy.stats` module. Before conducting the test, we check for normality using `stats.normaltest` and for equal variances using `stats.levene`. This helps us assess the appropriateness of the T-test. The results of the T-test, normality test, and variance test are recorded and outputted.

### Data Transformation

To address any non-normality in the data, we apply a data transformation to the comment counts. Various transformation options, such as logarithmic, exponential, square root, and squared, are considered. The transformation that brings the data closest to a normal distribution is chosen.

### Central Limit Theorem

Applying the Central Limit Theorem, we group the comments by year and week number, calculating the mean comment count for weekdays and weekends in each week. This generates sample means that can be assumed to follow a normal distribution. We then assess normality and equal variances using appropriate tests. Finally, we conduct a T-test to determine if there is a significant difference between the mean comment counts on weekdays and weekends.

### Non-Parametric Test (Mann-Whitney U-test)

Additionally, we perform a non-parametric Mann-Whitney U-test on the original, non-transformed comment counts to assess the difference between weekdays and weekends. The U-test does not assume normality or equal variances and provides insights into the likelihood of the larger number of comments occurring on weekends compared to weekdays.

### Output

The `reddit_weekends.py` program provides output in the format specified by the provided `reddit_weekends_hint.py` template. The output includes the p-values from the various tests conducted on the data, allowing for easy verification and comparison.

### Usage

To run the analysis, follow these steps:

1. Install the necessary dependencies: Pandas, NumPy, and SciPy.

2. Clone the repository:
   ```
   git clone https://github.com/your-username/reddit-weekends.git
   ```

3. Navigate to the project directory:
   ```
   cd reddit-weekends
   ```

4. Place the input data file, `reddit-counts.json.gz`, in the project directory.

5. Run the program to analyze the difference in comment counts between weekdays and weekends:
   ```
   python3 reddit_weekends.py reddit-counts.json.gz
   ```

6. The program will conduct the T-test, assess normality and variance, perform data transformations, apply the Central Limit Theorem, and conduct the Mann-Whitney U-test. The p
