# AI4CODE 

Today, Jupyter Notebooks are one of the main sources Data Scientists use to write their codes and explain the stories behind these codes with markdowns. To be able to tell a good story about their projects, many people use two entities: codes and markdowns. 

It would be pretty useful to find a method that can understand the relationships between the codes and markdowns. And the objective of this project is to find this method. 

As in all other Data Science projects, one of the key steps to be taken when starting a project is to find/collect a quality dataset that contains all the necessary information to solve the defined problem. And in this project, the AI4Code data that is published by Google will be used. The AI4Code data contains code cells and markdown cells of 140,000 Jupyter Notebooks. The code cells in these notebooks are in the correct order while the markdown cells are shuffled.  (The details of the data can be found in this link: https://www.kaggle.com/competitions/AI4Code/data). And to reach the objective, which is finding a method that can understand the relationships between the codes and markdowns, I will try to find the correct ordering of the codes in the notebooks based on the shuffled markdowns.

To evaluate the performance of different methods, Kendall Tau Correlation will be used.

$$K = 1 - 4 \frac{\sum_i S_{i}}{\sum_i n_i(n_i - 1)}$$
