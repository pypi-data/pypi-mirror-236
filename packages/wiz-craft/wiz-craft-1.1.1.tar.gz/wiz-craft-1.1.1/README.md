<p align="center">
  <img src="https://svgshare.com/i/wCo.svg" alt="wizcraft-banner" />
</p>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) 

[![Downloads](https://static.pepy.tech/personalized-badge/wiz-craft?period=total&units=international_system&left_color=brightgreen&right_color=orange&left_text=Downloads)](https://pepy.tech/project/wiz-craft)

![PyPI - Version](https://img.shields.io/pypi/v/wiz-craft)


# WizCraft - CLI-Based Dataset Preprocessing Tool

WizCraft is a cutting-edge Command Line Interface (CLI) tool developed to simplify the process of dataset preprocessing for machine learning tasks. It aims to provide a seamless and efficient experience for data scientists of all levels, facilitating the preparation of data for various machine-learning applications.

**[Try the tool online here](https://replit.com/@PinakDatta/DataWiz)**

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Tasks](#tasks)
  - [Data Description](#data-description)
  - [Handle Null Values](#handle-null-values)
  - [Encode Categorical Values](#encode-categorical-values)
  - [Feature Scaling](#feature-scaling)
  - [Save Preprocessed Dataset](#save-preprocessed-dataset)



## Features

- Load and preprocess your dataset effortlessly through a Command Line Interface (CLI).
- View dataset statistics, null value counts, and perform data imputation.
- Encode categorical variables using one-hot encoding.
- Normalize and standardize numerical features for better model performance.
- Download the preprocessed dataset with your desired modifications.

## Getting Started

### Installation

1. Run the pip command:
   ```bash
   pip install wiz-craft

2. To use the module, use the commands:
    ```python
    from wizcraft.preprocess import Preprocess
    wiz_obj = Preprocess()
    wiz_obj.start()  

3. Follow the on-screen prompts to load your dataset, select target variables, and perform preprocessing tasks.

<p align="center">
  <img src="https://i.imgur.com/jYLwMN7.png" alt="wizcraft-cli_welcome" width = "600" height = "300" />
</p>

## Features Available

### Data Description

<p>
  <img src="https://i.imgur.com/2CUMMoX.png" alt="data_description_preview" />
</p>

1. View statistics and properties of numeric columns.
2. Explore unique values and statistics of categorical columns.
3. Display a snapshot of the dataset.

### Handle Null Values

<p>
  <img src="https://i.imgur.com/JlkyQl5.png" alt="null_data_preview" />
</p>

1. Show NULL value counts in each column.
2. Remove specific columns or fill NULL values with mean, median, or mode, or even using KNN technique.
### Encode Categorical Values

<p>
  <img src="https://i.imgur.com/0gEfhpi.png" alt="one_hot_encode_preview" />
</p>

1. Identify and list categorical columns.
2. Perform one-hot encoding on categorical columns.

### Feature Scaling

<p>
  <img src="https://i.imgur.com/kfpoXeG.png" alt="scaling_preview" />
</p>

1. Normalize the data in a column using Min-Max scaling or Standard Scaler.

### Save Preprocessed Dataset

<p>
  <img src="https://i.imgur.com/1XywkGQ.png" alt="save_preview" />
</p>

1. Download the modified dataset with applied preprocessing steps.

