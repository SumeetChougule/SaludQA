import pandas as pd

df = pd.read_csv("data/medquad.csv")

fraction = 0.20
sampled_df = df.sample(frac=fraction, random_state=42)
# Save the sampled DataFrame to a new CSV file
sampled_df.to_csv("data/fractional_data.csv", index=False)
