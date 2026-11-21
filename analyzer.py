
import pandas as pd

def analyze_topics(df):
    topic_counts = (
        df["topic"]
        .value_counts()
        .reset_index()
    )

    topic_counts.columns = ["Topic", "Frequency"]
    
    return topic_counts
