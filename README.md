## A simple Python wrapper Redditmetrics.com 

Installation
------------

   ```pip install rmwrapper```

Description
-----------
A very minimal wrapper for [Redditmetrics](https://redditmetrics.com).
Redditmetrics is a website that contains historical and recent data from all around [Reddit](https://reddit.com), be it subreddit-specific or general. This package aims to make it more comfortable to use that data with a simplistic interface, since Redditmetrics itself doesn't provide an API. 

Example usage
-------------------
```python
from rmwrapper import RedditMetricsWrapper

# Subreddit-specific methods take the subreddit names as arguments.
RedditMetricsWrapper.subreddit_get_current_subscribers("lain")

# Non-subreddit-specific methods don't take any arguments.
RedditMetricsWrapper.get_fastest_growing_today()

```
List of all available functions
-------------------
Subreddit-specific:
```python
subreddit_get_subscriber_growth_data(subreddit) # Returns the entire available timeline for a specific subreddit and how many subscribers it gained per day.

subreddit_get_subscriber_growth_data(subreddit) # Returns the entire available timeline for a specific subreddit and how many subscribers it had each day.

subreddit_get_rank_data(subreddit) # Returns the entire available timeline for a specific subreddit and what the subreddit rank for it was.

subreddit_get_current_subscribers(subreddit) # Returns the current subscriber count for a specific subreddit.

subreddit_get_current_rank(subreddit) # Returns the current rank for a specific subreddit.
```
General:
```python
get_fastest_growing_today() # Returns 300 fastest growing subreddits today.
get_fastest_growing_week() # Returns 300 fastest growing subreddits this week.
get_fastest_growing_month() # Returns 300 fastest growing subreddits this month.

get_non_default_reddits_today()  # Returns top 300 non-default subreddits today.
get_non_default_reddits_week()  # Returns top 300 non-default subreddits this week.
get_non_default_reddits_month()  # Returns top 300 non-default subreddits this month.

get_top_new_reddits_today()  # Returns top 300 new subreddits today.
get_non_default_reddits_week()  # Returns top 300 new subreddits this week.
get_non_default_reddits_month()  # Returns top 300 new subreddits this month.

get_new_reddits_trending_month() # Returns top 300 trending subreddits this month.
get_new_reddits_trending_3_months() # Returns top 300 trending subreddits in the last 3 months.
get_new_reddits_trending_6_months() # Returns top 300 trending subreddits in the last 6 months.

get_top_n_reddits(n) # Returns top n amount of subreddits sorted by subscriber count.
```


