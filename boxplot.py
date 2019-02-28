%matplotlib inline

import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
iris = sns.load_dataset("iris")
sns.boxplot(data=iris);