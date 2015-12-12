
# coding: utf-8

# # Regression Week 3: Assessing Fit (polynomial regression)

# In this notebook you will compare different regression models in order to assess which model fits best. We will be using polynomial regression as a means to examine this topic. In particular you will:
# * Write a function to take an SArray and a degree and return an SFrame where each column is the SArray to a polynomial value up to the total degree e.g. degree = 3 then column 1 is the SArray column 2 is the SArray squared and column 3 is the SArray cubed
# * Use matplotlib to visualize polynomial regressions
# * Use matplotlib to visualize the same polynomial degree on different subsets of the data
# * Use a validation set to select a polynomial degree
# * Assess the final fit using test data
# 
# We will continue to use the House data from previous notebooks.

# # Fire up graphlab create

# In[1]:

import graphlab


# Next we're going to write a polynomial function that takes an SArray and a maximal degree and returns an SFrame with columns containing the SArray to all the powers up to the maximal degree.
# 
# The easiest way to apply a power to an SArray is to use the .apply() and lambda x: functions. 
# For example to take the example array and compute the third power we can do as follows: (note running this cell the first time may take longer than expected since it loads graphlab)

# In[2]:

tmp = graphlab.SArray([1., 2., 3.])
tmp_cubed = tmp.apply(lambda x: x**3)
print tmp
print tmp_cubed


# We can create an empty SFrame using graphlab.SFrame() and then add any columns to it with ex_sframe['column_name'] = value. For example we create an empty SFrame and make the column 'power_1' to be the first power of tmp (i.e. tmp itself).

# In[3]:

ex_sframe = graphlab.SFrame()
ex_sframe['power_1'] = tmp
print ex_sframe


# # Polynomial_sframe function

# Using the hints above complete the following function to create an SFrame consisting of the powers of an SArray up to a specific degree:

# In[6]:

def polynomial_sframe(feature, degree):
    # assume that degree >= 1
    # initialize the SFrame:
    poly_sframe = graphlab.SFrame()
    # and set poly_sframe['power_1'] equal to the passed feature
    poly_sframe['power_1'] = feature
    # first check if degree > 1
    if degree > 1:
        # then loop over the remaining degrees:
        # range usually starts at 0 and stops at the endpoint-1. We want it to start at 2 and stop at degree
        for power in range(2, degree+1): 
            # first we'll give the column a name:
            name = 'power_' + str(power)
            # then assign poly_sframe[name] to the appropriate power of feature
            poly_sframe[name] = feature**power
    return poly_sframe


# To test your function consider the smaller tmp variable and what you would expect the outcome of the following call:

# In[7]:

print polynomial_sframe(tmp, 3)


# # Visualizing polynomial regression

# Let's use matplotlib to visualize what a polynomial regression looks like on some real data.

# In[8]:

sales = graphlab.SFrame('kc_house_data.gl/')


# As in Week 3, we will use the sqft_living variable. For plotting purposes (connecting the dots), you'll need to sort by the values of sqft_living. For houses with identical square footage, we break the tie by their prices.

# In[10]:

sales = sales.sort(['sqft_living', 'price'])
sales


# Let's start with a degree 1 polynomial using 'sqft_living' (i.e. a line) to predict 'price' and plot what it looks like.

# In[11]:

poly1_data = polynomial_sframe(sales['sqft_living'], 1)
poly1_data


# In[12]:

poly1_data['price'] = sales['price'] # add price to the data since it's the target


# In[15]:

poly1_data


# NOTE: for all the models in this notebook use validation_set = None to ensure that all results are consistent across users.

# In[14]:

model1 = graphlab.linear_regression.create(poly1_data, target = 'price', features = ['power_1'], validation_set = None)
model1.coefficients


# In[16]:

#let's take a look at the weights before we plot
model1.get("coefficients")


# In[17]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[18]:

plt.plot(poly1_data['power_1'],poly1_data['price'],'.',
        poly1_data['power_1'], model1.predict(poly1_data),'-')


# Let's unpack that plt.plot() command. The first pair of SArrays we passed are the 1st power of sqft and the actual price we then ask it to print these as dots '.'. The next pair we pass is the 1st power of sqft and the predicted values from the linear model. We ask these to be plotted as a line '-'. 
# 
# We can see, not surprisingly, that the predicted values all fall on a line, specifically the one with slope 280 and intercept -43579. What if we wanted to plot a second degree polynomial?

# In[19]:

poly2_data = polynomial_sframe(sales['sqft_living'], 2)
my_features = poly2_data.column_names() # get the name of the features


# In[20]:

poly2_data['price'] = sales['price'] # add price to the data since it's the target
model2 = graphlab.linear_regression.create(poly2_data, target = 'price', features = my_features, validation_set = None)


# In[21]:

model2.get("coefficients")


# In[22]:

plt.plot(poly2_data['power_1'],poly2_data['price'],'.',
        poly2_data['power_1'], model2.predict(poly2_data),'-')


# The resulting model looks like half a parabola. Try on your own to see what the cubic looks like:

# In[24]:

poly3_data = polynomial_sframe(sales['sqft_living'], 3)
my_features = poly3_data.column_names() # get the name of the features
poly3_data['price'] = sales['price'] # add price to the data since it's the target
model3 = graphlab.linear_regression.create(poly3_data, target = 'price', features = my_features, validation_set = None)


# In[25]:

plt.plot(poly3_data['power_1'],poly3_data['price'],'.',
        poly3_data['power_1'], model3.predict(poly2_data),'-')


# Now try a 15th degree polynomial:

# In[26]:

poly15_data = polynomial_sframe(sales['sqft_living'], 15)
my_features = poly15_data.column_names() # get the name of the features
poly15_data['price'] = sales['price'] # add price to the data since it's the target
model15 = graphlab.linear_regression.create(poly15_data, target = 'price', features = my_features, validation_set = None)


# In[30]:

plt.plot(poly15_data['power_1'],poly15_data['price'],'.',
        poly15_data['power_1'], model15.predict(poly15_data),'-')


# What do you think of the 15th degree polynomial? Do you think this is appropriate? If we were to change the data do you think you'd get pretty much the same curve? Let's take a look.

# # Changing the data and re-learning

# We're going to split the sales data into four subsets of roughly equal size. Then you will estimate a 15th degree polynomial model on all four subsets of the data. Print the coefficients (you should use .print_rows(num_rows = 16) to view all of them) and plot the resulting fit (as we did above). The quiz will ask you some questions about these results.
# 
# To split the sales data into four subsets, we perform the following steps:
# * First split sales into 2 subsets with `.random_split(0.5, seed=0)`. 
# * Next split the resulting subsets into 2 more subsets each. Use `.random_split(0.5, seed=0)`.
# 
# We set `seed=0` in these steps so that different users get consistent results.
# You should end up with 4 subsets (`set_1`, `set_2`, `set_3`, `set_4`) of approximately equal size. 

# In[31]:

half1_data, half2_data = sales.random_split(.5,seed=0)


# In[32]:

set_1,set_2 = half1_data.random_split(.5,seed=0)
set_3,set_4 = half2_data.random_split(.5,seed=0)


# Fit a 15th degree polynomial on set_1, set_2, set_3, and set_4 using sqft_living to predict prices. Print the coefficients and make a plot of the resulting model.

# In[35]:

poly15_data1 = polynomial_sframe(set_1['sqft_living'], 15)
my_features = poly15_data1.column_names() # get the name of the features
poly15_data1['price'] = set_1['price'] # add price to the data since it's the target
model15_1 = graphlab.linear_regression.create(poly15_data1, target = 'price', features = my_features, validation_set = None)
plt.plot(poly15_data1['power_1'],poly15_data1['price'],'.',
        poly15_data1['power_1'], model15_1.predict(poly15_data1),'-')
print model15_1.get("coefficients")


# In[43]:

poly15_data1 = polynomial_sframe(set_1['sqft_living'], 15)
my_features = poly15_data1.column_names() # get the name of the features
poly15_data1['price'] = set_1['price'] # add price to the data since it's the target
model15_1 = graphlab.linear_regression.create(poly15_data1, target = 'price', features = my_features, validation_set = None)
plt.plot(poly15_data1['power_1'],poly15_data1['price'],'.',
        poly15_data1['power_1'], model15_1.predict(poly15_data1),'-')
model15_1.get("coefficients").print_rows(num_rows=16, num_columns=3)


# In[44]:

poly15_data2 = polynomial_sframe(set_2['sqft_living'], 15)
my_features = poly15_data2.column_names() # get the name of the features
poly15_data2['price'] = set_2['price'] # add price to the data since it's the target
model15_2 = graphlab.linear_regression.create(poly15_data2, target = 'price', features = my_features, validation_set = None)
plt.plot(poly15_data2['power_1'],poly15_data2['price'],'.',
        poly15_data2['power_1'], model15_2.predict(poly15_data2),'-')
model15_2.get("coefficients").print_rows(num_rows=16, num_columns=3)


# In[45]:

poly15_data3 = polynomial_sframe(set_3['sqft_living'], 15)
my_features = poly15_data3.column_names() # get the name of the features
poly15_data3['price'] = set_3['price'] # add price to the data since it's the target
model15_3 = graphlab.linear_regression.create(poly15_data3, target = 'price', features = my_features, validation_set = None)
plt.plot(poly15_data3['power_1'],poly15_data3['price'],'.',
        poly15_data3['power_1'], model15_3.predict(poly15_data3),'-')
model15_3.get("coefficients").print_rows(num_rows=16, num_columns=3)


# In[46]:

poly15_data4 = polynomial_sframe(set_4['sqft_living'], 15)
my_features = poly15_data4.column_names() # get the name of the features
poly15_data4['price'] = set_4['price'] # add price to the data since it's the target
model15_4 = graphlab.linear_regression.create(poly15_data4, target = 'price', features = my_features, validation_set = None)
plt.plot(poly15_data4['power_1'],poly15_data4['price'],'.',
        poly15_data4['power_1'], model15_4.predict(poly15_data4),'-')
model15_4.get("coefficients").print_rows(num_rows=16, num_columns=3)


# Some questions you will be asked on your quiz:
# 
# **Quiz Question: Is the sign (positive or negative) for power_15 the same in all four models?**
# 
# **Quiz Question: (True/False) the plotted fitted lines look the same in all four plots**

# # Selecting a Polynomial Degree

# Whenever we have a "magic" parameter like the degree of the polynomial there is one well-known way to select these parameters: validation set. (We will explore another approach in week 4).
# 
# We split the sales dataset 3-way into training set, test set, and validation set as follows:
# 
# * Split our sales data into 2 sets: `training_and_validation` and `testing`. Use `random_split(0.9, seed=1)`.
# * Further split our training data into two sets: `training` and `validation`. Use `random_split(0.5, seed=1)`.
# 
# Again, we set `seed=1` to obtain consistent results for different users.

# In[48]:

training_and_validation,test_data = sales.random_split(0.9,seed=1)
train_data, validation_data = training_and_validation.random_split(0.5,seed=1)


# Next you should write a loop that does the following:
# * For degree in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] (to get this in python type range(1, 15+1))
#     * Build an SFrame of polynomial data of train_data['sqft_living'] at the current degree
#     * hint: my_features = poly_data.column_names() gives you a list e.g. ['power_1', 'power_2', 'power_3'] which you might find useful for graphlab.linear_regression.create( features = my_features)
#     * Add train_data['price'] to the polynomial SFrame
#     * Learn a polynomial regression model to sqft vs price with that degree on TRAIN data
#     * Compute the RSS on VALIDATION data (here you will want to use .predict()) for that degree and you will need to make a polynmial SFrame using validation data.
# * Report which degree had the lowest RSS on validation data (remember python indexes from 0)
# 
# (Note you can turn off the print out of linear_regression.create() with verbose = False)

# In[57]:

from math import sqrt
RSS = []
for deg in range(1,16):
    poly_data = polynomial_sframe(train_data['sqft_living'], deg)
    my_features = poly_data.column_names()
    poly_data['price'] = train_data['price']
    model = graphlab.linear_regression.create(poly_data, target = 'price', features = my_features, validation_set = None)
    validation_poly = polynomial_sframe(validation_data['sqft_living'], deg)
    predictions = model.predict(validation_poly)
    errors = validation_data['price'] - predictions
    errors_sq = errors**2
    sum_errors_sq = sum(errors_sq)
    RSS.append(sqrt(sum_errors_sq))
    
minRss = min(RSS)
index = RSS.index(minRss)
print "--------------------"
print str(index+1)


# **Quiz Question: Which degree (1, 2, …, 15) had the lowest RSS on Validation data?**
# 
# 6

# Now that you have chosen the degree of your polynomial using validation data, compute the RSS of this model on TEST data. Report the RSS on your quiz.

# In[ ]:

poly_data = polynomial_sframe(train_data['sqft_living'],6)
my_features = poly_data.column_names()
poly_data['price'] = train_data['price']
model = graphlab.linear_regression.create(poly_data, target = 'price', features = my_features, validation_set = None)
test_poly_data = polynomial_sframe(test_data['sqft_living'], 6)
predictions = model.predict(test_poly_data)
errors = test_data['price'] - predictions
errors_sq = errors**2
sum_errors_sq = sum(errors_sq)
RSS_test = sum_errors_sq
RSS_test


# **Quiz Question: what is the RSS on TEST data for the model with the degree selected from Validation data? (Make sure you got the correct degree from the previous question)**

# 11203988
