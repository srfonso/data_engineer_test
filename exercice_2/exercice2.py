########### reg expressions
# loading modules
import re
import numpy as np
import pandas as pd

# read raw strings
dim_df = pd.read_csv("candidateEvalData/dim_df_correct.csv")
rawDim = dim_df["rawDim"].to_list()

results = []

# Regular expression for the first four
re_1_2_3_4 = "(\d+[\.\,]?\d*)\s*[xX×]\s*(\d+[\.\,]?\d*)(?:\D*(\d+[\.\,]?\d*))?(?:\s*cm)"

# Regular expression for the last one
re_5 = "(\d+)"


# 1: 19×52cm
results.append(
    [rawDim[0]] + list(re.findall(re_1_2_3_4, rawDim[0])[0])
)

# 2: 50 x 66,4 cm
results.append(
    [rawDim[1]] + list(re.findall(re_1_2_3_4, rawDim[1])[0])
)

# 3: 168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)
results.append(
    [rawDim[2]] + list(re.findall(re_1_2_3_4, rawDim[2])[0])
)

# 4: Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)
# We want the Image one
results.append(
    [rawDim[3]] + list(re.findall(re_1_2_3_4, rawDim[3])[1])
)

# 5: 5 by 5in
results.append([
    rawDim[4]] + [2.54*float(item) for item in re.findall(re_5, rawDim[4]) if item]
)

# Create result DataFrame
r_df = pd.DataFrame(results, columns=["rawDim", "height", "width", "depth"])

# Replace commas with dots
value_cols = ["height", "width", "depth"]
r_df[value_cols] = r_df[value_cols].replace(',', '.', regex=True)
# To float64 or Nan
r_df[value_cols] = r_df[value_cols].apply(pd.to_numeric, errors='coerce')
# To file
r_df.to_csv("result_2.csv", index=None)
print(r_df)