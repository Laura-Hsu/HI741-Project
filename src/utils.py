import pandas as pd
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "data" 

def generate_key_statistics(df):
    df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')

    # 1. Yearly visit trend
    visits_by_year = df.groupby(df['Visit_time'].dt.to_period("Y")).size()

    # 2. Yearly visits by insurance
    insurance_trend = df.groupby([df['Visit_time'].dt.to_period("Y"), 'Insurance']).size().unstack(fill_value=0)

    # 3. Yearly visits by race
    race_trend = df.groupby([df['Visit_time'].dt.to_period("Y"), 'Race']).size().unstack(fill_value=0)

    # 4. Yearly visits by gender
    gender_trend = df.groupby([df['Visit_time'].dt.to_period("Y"), 'Gender']).size().unstack(fill_value=0)

    # 5. Yearly visits by ethnicity
    ethnicity_trend = df.groupby([df['Visit_time'].dt.to_period("Y"), 'Ethnicity']).size().unstack(fill_value=0)

    def plot_trend(trend_df, title, filename):
        plt.figure(figsize=(12, 6))
        if trend_df.ndim == 1:
            trend_df.plot(kind="bar", ax=plt.gca())
        else:
            trend_df.plot(kind="bar", stacked=True, ax=plt.gca())

        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Visit Count")
        plt.xticks(rotation=0)
        plt.tight_layout()
        output_path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(output_path)
        plt.close()

    plot_trend(visits_by_year, "Yearly Visit Trend", "yearly_visits.png")
    plot_trend(insurance_trend, "Yearly Visits by Insurance Type", "insurance_trend.png")
    plot_trend(race_trend, "Yearly Visits by Race", "race_trend.png")
    plot_trend(gender_trend, "Yearly Visits by Gender", "gender_trend.png")
    plot_trend(ethnicity_trend, "Yearly Visits by Ethnicity", "ethnicity_trend.png")

