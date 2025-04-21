
import pandas as pd
import matplotlib.pyplot as plt

def generate_statistics(df):
    df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')

    # 1. Monthly visit trend
    visits_by_month = df.groupby(df['Visit_time'].dt.to_period("M")).size()

    # 2. Monthly visits by insurance
    insurance_trend = df.groupby([df['Visit_time'].dt.to_period("M"), 'Insurance']).size().unstack(fill_value=0)

    # 3. Monthly visits by race
    race_trend = df.groupby([df['Visit_time'].dt.to_period("M"), 'Race']).size().unstack(fill_value=0)

    # 4. Monthly visits by gender
    gender_trend = df.groupby([df['Visit_time'].dt.to_period("M"), 'Gender']).size().unstack(fill_value=0)

    # 5. Monthly visits by ethnicity
    ethnicity_trend = df.groupby([df['Visit_time'].dt.to_period("M"), 'Ethnicity']).size().unstack(fill_value=0)

    def plot_trend(trend_df, title, filename):
        plt.figure(figsize=(10, 6))
        trend_df.plot(marker='o', ax=plt.gca())
        plt.title(title)
        plt.xlabel("Month")
        plt.ylabel("Visit Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    plot_trend(visits_by_month, "Monthly Visit Trend", "monthly_visits.png")
    plot_trend(insurance_trend, "Monthly Visits by Insurance Type", "insurance_trend.png")
    plot_trend(race_trend, "Monthly Visits by Race", "race_trend.png")
    plot_trend(gender_trend, "Monthly Visits by Gender", "gender_trend.png")
    plot_trend(ethnicity_trend, "Monthly Visits by Ethnicity", "ethnicity_trend.png")
