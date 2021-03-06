import os
import tarfile
import urllib
from six.moves import urllib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import Imputer, OneHotEncoder, StandardScaler
from AddClasses import CombinedAttributesAdder, DataFrameSelector, CategoricalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint as sp_randint

# Download data (California housing)
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


# Identical Function
def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


fetch_housing_data()
housing = load_housing_data()
# train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42) #Same as defined function
# print(housing.describe())
# housing.hist(bins=50, figsize=(20, 15))
# plt.show()

# Begin Create testing set
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

# Split test data and training data for validation
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

# print(strat_test_set["income_cat"].value_counts()/len(strat_test_set))

# Remove income_cat attribute from data
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)
# End Create testing set

# Map location and price
housing = strat_train_set.copy()
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1,
             s=housing["population"] / 100, label="population", figsize=(10, 7),
             c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True, )
plt.legend()
# plt.show()

# Calculate Standard correlation coefficient
# corr_matrix = housing.corr()
# print(corr_matrix["median_house_value"].sort_values(ascending=False))

# Add custom attribute combinations
housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
housing["bedrooms_per_home"] = housing["total_bedrooms"] / housing["total_rooms"]
housing["population_per_household"] = housing["population"] / housing["households"]
corr_matrix = housing.corr()
# print(corr_matrix["median_house_value"].sort_values(ascending=False))

# Revert to clean training set
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# Begin data cleaning - 3 Options for missing data (numerical)
# housing.dropna(subset=["total_bedrooms"])
# housing.drop("total_bedrooms", axis=1)
# median = housing["total_bedrooms"].median()
# housing["total_bedrooms"].fillna(median, inplace=True)

# OR sklean method
imputer = Imputer(strategy="median")
housing_num = housing.drop("ocean_proximity", axis=1)
imputer.fit(housing_num)
X = imputer.transform(housing_num)
housing_tr = pd.DataFrame(X, columns=housing_num.columns)

# Convert the ocean distances to numbers
housing_cat = housing["ocean_proximity"]
housing_cat_encoded, housing_categories = housing_cat.factorize()
# print(housing_cat_encoded[:10])

# Use one-hot encoding to make these categories which are 0s and 1
encoder = OneHotEncoder()  # At some point CategoricalEncoder will be released to do these two steps simultaneously
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1, 1))

# Using custom transformer to add hyperparameter. Can be easily removed or added to tweak ML performance
attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
housing_extra_attribs = attr_adder.transform(housing.values)

# Feature scaling - included below

# Do all the steps above with pipelines
num_pipeline = Pipeline([
    ('imputer', Imputer(strategy="median")),
    ('attribs_addr', CombinedAttributesAdder()),
    ('std_scaler', StandardScaler()),
])
housing_num_tr = num_pipeline.fit_transform(housing_num)

# Using classes to refactor pipelines (This is a streamlined version of the above)
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', Imputer(strategy="median")),
    ('attribs_adder', CombinedAttributesAdder()),
    ('std_scaler', StandardScaler()),
])

cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('cat_encoder', CategoricalEncoder(encoding="onehot-dense")),
])

full_pipeline = FeatureUnion(transformer_list=[
    ("num_pipeline", num_pipeline),
    ("cat_pipeline", cat_pipeline),
])

housing_prepared = full_pipeline.fit_transform(housing)

# print(housing_prepared.shape)  # (16512, 16)

# Selecting and training a model
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

# Sample Linear regression
some_data = housing.iloc[:5]
some_labels = housing_labels.iloc[:5]
some_data_prepared = full_pipeline.transform(some_data)
# print("Linear reg Predictions: ", lin_reg.predict(some_data_prepared))
# print("Labels: ", list(some_labels))

# Calculate rms error over dataset
housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)

# Decision Tree regression
tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)

# Evaluate Tree - Completely overfits data
housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)

# Improving the decision tree with cross-validation
scores = cross_val_score(tree_reg, housing_prepared, housing_labels, scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores = np.sqrt(-scores)


def display_scores(scores):
    # print("Scores:", scores)
    print("Mean:", scores.mean())
    print("STdev:", scores.std())


lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels, scoring="neg_mean_squared_error", cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
print("Linear")
display_scores(lin_rmse_scores)
print("Decision Tree with cross validation")
display_scores(tree_rmse_scores)  # Mean is actually 70861, worse than linear

# Random Forest Regressor
print("Random Forest Regressor")
forest_reg = RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)

# No cross validation
print("No cross validation")
housing_predictions = forest_reg.predict(housing_prepared)
forest_mse = mean_squared_error(housing_labels, housing_predictions)
forest_rmse = np.sqrt(forest_mse)
print("forest_rmse", forest_rmse)

# Cross validation
print("Cross validation")
scores = cross_val_score(forest_reg, housing_prepared, housing_labels, scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-scores)
display_scores(forest_rmse_scores)

# Fine tuning
print("Randomized search")
param_grid = {"max_depth": [3, None],
              "max_features": sp_randint(1, 11),
              "min_samples_split": sp_randint(2, 11),
              "min_samples_leaf": sp_randint(1, 11),
              "bootstrap": [True, False],
              }

forest_reg = RandomForestRegressor()
random_search = RandomizedSearchCV(forest_reg, param_grid, n_iter=20)
random_search.fit(housing_prepared, housing_labels)  # Doesn't retrain Forest_Reg
print("Best estimator: ", random_search.best_estimator_)

random_forest_reg = RandomForestRegressor(bootstrap=False, criterion='mse', max_depth=None,
                                          max_features=5, max_leaf_nodes=None, min_impurity_decrease=0.0,
                                          min_impurity_split=None, min_samples_leaf=5,
                                          min_samples_split=2, min_weight_fraction_leaf=0.0,
                                          n_estimators=10, n_jobs=1, oob_score=False, random_state=None,
                                          verbose=0, warm_start=False)
scores = cross_val_score(random_forest_reg, housing_prepared, housing_labels, scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-scores)
display_scores(forest_rmse_scores)



# Using Grid search to find optimal hyper parameters
print("Grid Search Forest Regressor")
param_grid = [  # 90 combinations
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]}
]

forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5, scoring='neg_mean_squared_error', refit=True)
grid_search.fit(housing_prepared, housing_labels)  # Doesn't retrain Forest_Reg

print("Best estimator: ", grid_search.best_estimator_)

forest_reg = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
                                   max_features=6, max_leaf_nodes=None, min_impurity_decrease=0.0,
                                   min_impurity_split=None, min_samples_leaf=1,
                                   min_samples_split=2, min_weight_fraction_leaf=0.0,
                                   n_estimators=30, n_jobs=1, oob_score=False, random_state=None,
                                   verbose=0, warm_start=False)

forest_reg.fit(housing_prepared, housing_labels)
scores = cross_val_score(forest_reg, housing_prepared, housing_labels, scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-scores)
display_scores(forest_rmse_scores)  # Best score Mean: 49742.353043 STdev: 1668.75796136

# Feature Importance can be found with
# grid_search.best_estimator_.feature_importances

print("Testing final data with optimized RandomForestRegressor")
final_model = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
                                    max_features=6, max_leaf_nodes=None, min_impurity_decrease=0.0,
                                    min_impurity_split=None, min_samples_leaf=1,
                                    min_samples_split=2, min_weight_fraction_leaf=0.0,
                                    n_estimators=30, n_jobs=1, oob_score=False, random_state=None,
                                    verbose=0, warm_start=False)
final_model.fit(housing_prepared, housing_labels)
X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()
X_test_prepared = full_pipeline.transform(X_test)
final_predictions = final_model.predict(X_test_prepared)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)

print("Final rmse: ", final_rmse)  # 47900.0074067
