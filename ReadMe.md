
# Regression Week 3: Assessing Fit (polynomial regression)

In this notebook you will compare different regression models in order to assess which model fits best. We will be using polynomial regression as a means to examine this topic. In particular you will:
* Write a function to take an SArray and a degree and return an SFrame where each column is the SArray to a polynomial value up to the total degree e.g. degree = 3 then column 1 is the SArray column 2 is the SArray squared and column 3 is the SArray cubed
* Use matplotlib to visualize polynomial regressions
* Use matplotlib to visualize the same polynomial degree on different subsets of the data
* Use a validation set to select a polynomial degree
* Assess the final fit using test data

We will continue to use the House data from previous notebooks.

# Fire up graphlab create


    import graphlab

Next we're going to write a polynomial function that takes an SArray and a maximal degree and returns an SFrame with columns containing the SArray to all the powers up to the maximal degree.

The easiest way to apply a power to an SArray is to use the .apply() and lambda x: functions. 
For example to take the example array and compute the third power we can do as follows: (note running this cell the first time may take longer than expected since it loads graphlab)


    tmp = graphlab.SArray([1., 2., 3.])
    tmp_cubed = tmp.apply(lambda x: x**3)
    print tmp
    print tmp_cubed

    [INFO] [1;32m1449878677 : INFO:     (initialize_globals_from_environment:282): Setting configuration variable GRAPHLAB_FILEIO_ALTERNATIVE_SSL_CERT_FILE to C:\Users\581889\AppData\Local\Dato\Dato Launcher\lib\site-packages\certifi\cacert.pem
    [0m[1;32m1449878677 : INFO:     (initialize_globals_from_environment:282): Setting configuration variable GRAPHLAB_FILEIO_ALTERNATIVE_SSL_CERT_DIR to 
    [0mThis trial license of GraphLab Create is assigned to lee_michael2@bah.com and will expire on December 31, 2015. Please contact trial@dato.com for licensing options or to request a free non-commercial license for personal or academic use.
    
    [INFO] Start server at: ipc:///tmp/graphlab_server-27492 - Server binary: C:\Users\581889\AppData\Local\Dato\Dato Launcher\lib\site-packages\graphlab\unity_server.exe - Server log: C:\Users\581889\AppData\Local\Temp\graphlab_server_1449878677.log.0
    [INFO] GraphLab Server Version: 1.7.1
    

    [1.0, 2.0, 3.0]
    [1.0, 8.0, 27.0]
    

We can create an empty SFrame using graphlab.SFrame() and then add any columns to it with ex_sframe['column_name'] = value. For example we create an empty SFrame and make the column 'power_1' to be the first power of tmp (i.e. tmp itself).


    ex_sframe = graphlab.SFrame()
    ex_sframe['power_1'] = tmp
    print ex_sframe

    +---------+
    | power_1 |
    +---------+
    |   1.0   |
    |   2.0   |
    |   3.0   |
    +---------+
    [3 rows x 1 columns]
    
    

# Polynomial_sframe function

Using the hints above complete the following function to create an SFrame consisting of the powers of an SArray up to a specific degree:


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

To test your function consider the smaller tmp variable and what you would expect the outcome of the following call:


    print polynomial_sframe(tmp, 3)

    +---------+---------+---------+
    | power_1 | power_2 | power_3 |
    +---------+---------+---------+
    |   1.0   |   1.0   |   1.0   |
    |   2.0   |   4.0   |   8.0   |
    |   3.0   |   9.0   |   27.0  |
    +---------+---------+---------+
    [3 rows x 3 columns]
    
    

# Visualizing polynomial regression

Let's use matplotlib to visualize what a polynomial regression looks like on some real data.


    sales = graphlab.SFrame('kc_house_data.gl/')

As in Week 3, we will use the sqft_living variable. For plotting purposes (connecting the dots), you'll need to sort by the values of sqft_living. For houses with identical square footage, we break the tie by their prices.


    sales = sales.sort(['sqft_living', 'price'])
    sales




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">id</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">date</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">price</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">bedrooms</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">bathrooms</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_living</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_lot</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">floors</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">waterfront</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">3980300371</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-09-26 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">142000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">290.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">20875</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2856101479</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-07-01 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">276000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">370.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1801</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1723049033</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-06-20 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">245000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">380.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">15000</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1222029077</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-10-29 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">265000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">384.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">213444</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6896300380</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-10-02 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">228000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5900</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">9266700190</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2015-05-11 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">245000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2000</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6303400395</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2015-01-30 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">325000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">410.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">8636</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4322200105</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2015-03-31 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">229050.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">3298</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">7549801385</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-06-12 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">280000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6720</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">8658300340</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2014-05-23 00:00:00+00:00</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">80000.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.75</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">430.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5050</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
    </tr>
</table>
<table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">view</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">condition</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">grade</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_above</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_basement</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">yr_built</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">yr_renovated</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">zipcode</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">lat</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">290</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1963</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98024</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.53077245</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">370</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1923</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98117</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.67782145</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">3</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">380</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1963</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98168</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.48103428</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">3</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">384</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2003</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98070</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.41772688</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1953</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98118</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.52604001</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1920</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98103</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.69377314</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">410</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1953</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98146</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.5076723</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1949</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98136</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.5374761</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">3</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1922</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98108</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.55198122</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">430</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1912</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">98014</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">47.64994341</td>
    </tr>
</table>
<table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">long</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_living15</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">sqft_lot15</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-121.88842327</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1620.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">22850.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.38911208</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1340.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.322601</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1170.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">15000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.49121696</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1920.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">224341.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.26142752</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">2170.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.34662226</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1340.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">5100.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.35672193</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1190.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">8636.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.391385</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1460.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">4975.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-122.31082137</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1420.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">6720.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-121.90868353</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">1200.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">7500.0</td>
    </tr>
</table>
[21613 rows x 21 columns]<br/>Note: Only the head of the SFrame is printed.<br/>You can use print_rows(num_rows=m, num_columns=n) to print more rows and columns.
</div>



Let's start with a degree 1 polynomial using 'sqft_living' (i.e. a line) to predict 'price' and plot what it looks like.


    poly1_data = polynomial_sframe(sales['sqft_living'], 1)
    poly1_data




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">power_1</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">290.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">370.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">380.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">384.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">410.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">430.0</td>
    </tr>
</table>
[21613 rows x 1 columns]<br/>Note: Only the head of the SFrame is printed.<br/>You can use print_rows(num_rows=m, num_columns=n) to print more rows and columns.
</div>




    poly1_data['price'] = sales['price'] # add price to the data since it's the target


    poly1_data




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">power_1</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">price</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">290.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">142000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">370.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">276000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">380.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">245000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">384.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">265000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">228000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">390.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">245000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">410.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">325000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">229050.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">420.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">280000.0</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">430.0</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">80000.0</td>
    </tr>
</table>
[21613 rows x 2 columns]<br/>Note: Only the head of the SFrame is printed.<br/>You can use print_rows(num_rows=m, num_columns=n) to print more rows and columns.
</div>



NOTE: for all the models in this notebook use validation_set = None to ensure that all results are consistent across users.


    model1 = graphlab.linear_regression.create(poly1_data, target = 'price', features = ['power_1'], validation_set = None)
    model1.coefficients

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 21613
    PROGRESS: Number of features          : 1
    PROGRESS: Number of unpacked features : 1
    PROGRESS: Number of coefficients    : 2
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.007500     | 4362074.696077     | 261440.790724 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">name</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">index</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">value</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">(intercept)</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-43579.0852515</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">power_1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">280.622770886</td>
    </tr>
</table>
[2 rows x 3 columns]<br/>
</div>




    #let's take a look at the weights before we plot
    model1.get("coefficients")




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">name</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">index</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">value</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">(intercept)</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">-43579.0852515</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">power_1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">280.622770886</td>
    </tr>
</table>
[2 rows x 3 columns]<br/>
</div>




    import matplotlib.pyplot as plt
    %matplotlib inline


    plt.plot(poly1_data['power_1'],poly1_data['price'],'.',
            poly1_data['power_1'], model1.predict(poly1_data),'-')




    [<matplotlib.lines.Line2D at 0x1eda0240>,
     <matplotlib.lines.Line2D at 0x1ecf88d0>]




![png](output_26_1.png)


Let's unpack that plt.plot() command. The first pair of SArrays we passed are the 1st power of sqft and the actual price we then ask it to print these as dots '.'. The next pair we pass is the 1st power of sqft and the predicted values from the linear model. We ask these to be plotted as a line '-'. 

We can see, not surprisingly, that the predicted values all fall on a line, specifically the one with slope 280 and intercept -43579. What if we wanted to plot a second degree polynomial?


    poly2_data = polynomial_sframe(sales['sqft_living'], 2)
    my_features = poly2_data.column_names() # get the name of the features


    poly2_data['price'] = sales['price'] # add price to the data since it's the target
    model2 = graphlab.linear_regression.create(poly2_data, target = 'price', features = my_features, validation_set = None)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 21613
    PROGRESS: Number of features          : 2
    PROGRESS: Number of unpacked features : 2
    PROGRESS: Number of coefficients    : 3
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.012500     | 5913020.984255     | 250948.368758 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    


    model2.get("coefficients")




<div style="max-height:1000px;max-width:1500px;overflow:auto;"><table frame="box" rules="cols">
    <tr>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">name</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">index</th>
        <th style="padding-left: 1em; padding-right: 1em; text-align: center">value</th>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">(intercept)</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">199222.496445</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">power_1</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">67.9940640677</td>
    </tr>
    <tr>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">power_2</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">None</td>
        <td style="padding-left: 1em; padding-right: 1em; text-align: center; vertical-align: top">0.0385812312789</td>
    </tr>
</table>
[3 rows x 3 columns]<br/>
</div>




    plt.plot(poly2_data['power_1'],poly2_data['price'],'.',
            poly2_data['power_1'], model2.predict(poly2_data),'-')




    [<matplotlib.lines.Line2D at 0x1ef60d68>,
     <matplotlib.lines.Line2D at 0x1ef60f60>]




![png](output_31_1.png)


The resulting model looks like half a parabola. Try on your own to see what the cubic looks like:


    poly3_data = polynomial_sframe(sales['sqft_living'], 3)
    my_features = poly3_data.column_names() # get the name of the features
    poly3_data['price'] = sales['price'] # add price to the data since it's the target
    model3 = graphlab.linear_regression.create(poly3_data, target = 'price', features = my_features, validation_set = None)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 21613
    PROGRESS: Number of features          : 3
    PROGRESS: Number of unpacked features : 3
    PROGRESS: Number of coefficients    : 4
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.007500     | 3261066.736007     | 249261.286346 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    


    plt.plot(poly3_data['power_1'],poly3_data['price'],'.',
            poly3_data['power_1'], model3.predict(poly2_data),'-')




    [<matplotlib.lines.Line2D at 0x1f5a5c88>,
     <matplotlib.lines.Line2D at 0x1f5a5e80>]




![png](output_34_1.png)


Now try a 15th degree polynomial:


    poly15_data = polynomial_sframe(sales['sqft_living'], 15)
    my_features = poly15_data.column_names() # get the name of the features
    poly15_data['price'] = sales['price'] # add price to the data since it's the target
    model15 = graphlab.linear_regression.create(poly15_data, target = 'price', features = my_features, validation_set = None)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 21613
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.040000     | 2662308.584340     | 245690.511190 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    


    plt.plot(poly15_data['power_1'],poly15_data['price'],'.',
            poly15_data['power_1'], model15.predict(poly15_data),'-')




    [<matplotlib.lines.Line2D at 0x1fc8e208>,
     <matplotlib.lines.Line2D at 0x1f9142b0>]




![png](output_37_1.png)


What do you think of the 15th degree polynomial? Do you think this is appropriate? If we were to change the data do you think you'd get pretty much the same curve? Let's take a look.

# Changing the data and re-learning

We're going to split the sales data into four subsets of roughly equal size. Then you will estimate a 15th degree polynomial model on all four subsets of the data. Print the coefficients (you should use .print_rows(num_rows = 16) to view all of them) and plot the resulting fit (as we did above). The quiz will ask you some questions about these results.

To split the sales data into four subsets, we perform the following steps:
* First split sales into 2 subsets with `.random_split(0.5, seed=0)`. 
* Next split the resulting subsets into 2 more subsets each. Use `.random_split(0.5, seed=0)`.

We set `seed=0` in these steps so that different users get consistent results.
You should end up with 4 subsets (`set_1`, `set_2`, `set_3`, `set_4`) of approximately equal size. 


    half1_data, half2_data = sales.random_split(.5,seed=0)


    set_1,set_2 = half1_data.random_split(.5,seed=0)
    set_3,set_4 = half2_data.random_split(.5,seed=0)

Fit a 15th degree polynomial on set_1, set_2, set_3, and set_4 using sqft_living to predict prices. Print the coefficients and make a plot of the resulting model.


    poly15_data1 = polynomial_sframe(set_1['sqft_living'], 15)
    my_features = poly15_data1.column_names() # get the name of the features
    poly15_data1['price'] = set_1['price'] # add price to the data since it's the target
    model15_1 = graphlab.linear_regression.create(poly15_data1, target = 'price', features = my_features, validation_set = None)
    plt.plot(poly15_data1['power_1'],poly15_data1['price'],'.',
            poly15_data1['power_1'], model15_1.predict(poly15_data1),'-')
    print model15_1.get("coefficients")

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 5404
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2195218.932304     | 248858.822200 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    +-------------+-------+--------------------+
    |     name    | index |       value        |
    +-------------+-------+--------------------+
    | (intercept) |  None |   223312.750249    |
    |   power_1   |  None |   118.086127588    |
    |   power_2   |  None |  -0.0473482011347  |
    |   power_3   |  None | 3.25310342469e-05  |
    |   power_4   |  None | -3.3237215256e-09  |
    |   power_5   |  None | -9.75830457808e-14 |
    |   power_6   |  None | 1.15440303429e-17  |
    |   power_7   |  None | 1.05145869404e-21  |
    |   power_8   |  None | 3.46049616547e-26  |
    |   power_9   |  None | -1.0965445418e-30  |
    +-------------+-------+--------------------+
    [16 rows x 3 columns]
    Note: Only the head of the SFrame is printed.
    You can use print_rows(num_rows=m, num_columns=n) to print more rows and columns.
    


![png](output_44_1.png)



    poly15_data1 = polynomial_sframe(set_1['sqft_living'], 15)
    my_features = poly15_data1.column_names() # get the name of the features
    poly15_data1['price'] = set_1['price'] # add price to the data since it's the target
    model15_1 = graphlab.linear_regression.create(poly15_data1, target = 'price', features = my_features, validation_set = None)
    plt.plot(poly15_data1['power_1'],poly15_data1['price'],'.',
            poly15_data1['power_1'], model15_1.predict(poly15_data1),'-')
    model15_1.get("coefficients").print_rows(num_rows=16, num_columns=3)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 5404
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.020000     | 2195218.932304     | 248858.822200 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    +-------------+-------+--------------------+
    |     name    | index |       value        |
    +-------------+-------+--------------------+
    | (intercept) |  None |   223312.750249    |
    |   power_1   |  None |   118.086127588    |
    |   power_2   |  None |  -0.0473482011347  |
    |   power_3   |  None | 3.25310342469e-05  |
    |   power_4   |  None | -3.3237215256e-09  |
    |   power_5   |  None | -9.75830457808e-14 |
    |   power_6   |  None | 1.15440303429e-17  |
    |   power_7   |  None | 1.05145869404e-21  |
    |   power_8   |  None | 3.46049616547e-26  |
    |   power_9   |  None | -1.0965445418e-30  |
    |   power_10  |  None | -2.42031812001e-34 |
    |   power_11  |  None | -1.99601206815e-38 |
    |   power_12  |  None | -1.07709903836e-42 |
    |   power_13  |  None | -2.72862818122e-47 |
    |   power_14  |  None | 2.44782693024e-51  |
    |   power_15  |  None | 5.01975232977e-55  |
    +-------------+-------+--------------------+
    [16 rows x 3 columns]
    
    


![png](output_45_1.png)



    poly15_data2 = polynomial_sframe(set_2['sqft_living'], 15)
    my_features = poly15_data2.column_names() # get the name of the features
    poly15_data2['price'] = set_2['price'] # add price to the data since it's the target
    model15_2 = graphlab.linear_regression.create(poly15_data2, target = 'price', features = my_features, validation_set = None)
    plt.plot(poly15_data2['power_1'],poly15_data2['price'],'.',
            poly15_data2['power_1'], model15_2.predict(poly15_data2),'-')
    model15_2.get("coefficients").print_rows(num_rows=16, num_columns=3)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 5398
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.000000     | 2069212.978547     | 234840.067186 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    +-------------+-------+--------------------+
    |     name    | index |       value        |
    +-------------+-------+--------------------+
    | (intercept) |  None |   89836.5077331    |
    |   power_1   |  None |   319.806946763    |
    |   power_2   |  None |  -0.103315397041   |
    |   power_3   |  None | 1.06682476069e-05  |
    |   power_4   |  None | 5.75577097708e-09  |
    |   power_5   |  None | -2.54663464734e-13 |
    |   power_6   |  None | -1.09641345062e-16 |
    |   power_7   |  None | -6.36458441759e-21 |
    |   power_8   |  None | 5.52560417041e-25  |
    |   power_9   |  None | 1.35082038959e-28  |
    |   power_10  |  None | 1.18408188248e-32  |
    |   power_11  |  None | 1.98348000692e-37  |
    |   power_12  |  None | -9.92533590324e-41 |
    |   power_13  |  None | -1.60834847074e-44 |
    |   power_14  |  None | -9.12006024331e-49 |
    |   power_15  |  None | 1.68636658343e-52  |
    +-------------+-------+--------------------+
    [16 rows x 3 columns]
    
    


![png](output_46_1.png)



    poly15_data3 = polynomial_sframe(set_3['sqft_living'], 15)
    my_features = poly15_data3.column_names() # get the name of the features
    poly15_data3['price'] = set_3['price'] # add price to the data since it's the target
    model15_3 = graphlab.linear_regression.create(poly15_data3, target = 'price', features = my_features, validation_set = None)
    plt.plot(poly15_data3['power_1'],poly15_data3['price'],'.',
            poly15_data3['power_1'], model15_3.predict(poly15_data3),'-')
    model15_3.get("coefficients").print_rows(num_rows=16, num_columns=3)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 5409
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.012500     | 2269769.506522     | 251460.072754 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    +-------------+-------+--------------------+
    |     name    | index |       value        |
    +-------------+-------+--------------------+
    | (intercept) |  None |   87317.9795531    |
    |   power_1   |  None |   356.304911048    |
    |   power_2   |  None |  -0.164817442811   |
    |   power_3   |  None | 4.40424992697e-05  |
    |   power_4   |  None | 6.48234876343e-10  |
    |   power_5   |  None | -6.7525322662e-13  |
    |   power_6   |  None | -3.36842592657e-17 |
    |   power_7   |  None | 3.60999704255e-21  |
    |   power_8   |  None | 6.46999725624e-25  |
    |   power_9   |  None | 4.23639388917e-29  |
    |   power_10  |  None | -3.62149427028e-34 |
    |   power_11  |  None | -4.27119527388e-37 |
    |   power_12  |  None | -5.61445971718e-41 |
    |   power_13  |  None | -3.87452772757e-45 |
    |   power_14  |  None | 4.69430359435e-50  |
    |   power_15  |  None | 6.39045885969e-53  |
    +-------------+-------+--------------------+
    [16 rows x 3 columns]
    
    


![png](output_47_1.png)



    poly15_data4 = polynomial_sframe(set_4['sqft_living'], 15)
    my_features = poly15_data4.column_names() # get the name of the features
    poly15_data4['price'] = set_4['price'] # add price to the data since it's the target
    model15_4 = graphlab.linear_regression.create(poly15_data4, target = 'price', features = my_features, validation_set = None)
    plt.plot(poly15_data4['power_1'],poly15_data4['price'],'.',
            poly15_data4['power_1'], model15_4.predict(poly15_data4),'-')
    model15_4.get("coefficients").print_rows(num_rows=16, num_columns=3)

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 5402
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2314893.173822     | 244563.136754 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    +-------------+-------+--------------------+
    |     name    | index |       value        |
    +-------------+-------+--------------------+
    | (intercept) |  None |   259020.879452    |
    |   power_1   |  None |   -31.7277162053   |
    |   power_2   |  None |   0.109702769619   |
    |   power_3   |  None | -1.58383847349e-05 |
    |   power_4   |  None | -4.47660623739e-09 |
    |   power_5   |  None | 1.13976573478e-12  |
    |   power_6   |  None | 1.97669120543e-16  |
    |   power_7   |  None | -6.15783678766e-21 |
    |   power_8   |  None | -4.88012304042e-24 |
    |   power_9   |  None | -6.62186781331e-28 |
    |   power_10  |  None | -2.70631583277e-32 |
    |   power_11  |  None | 6.72370411453e-36  |
    |   power_12  |  None |  1.7411564631e-39  |
    |   power_13  |  None | 2.09188375707e-43  |
    |   power_14  |  None | 4.78015565463e-48  |
    |   power_15  |  None | -4.7453533305e-51  |
    +-------------+-------+--------------------+
    [16 rows x 3 columns]
    
    


![png](output_48_1.png)


Some questions you will be asked on your quiz:

**Quiz Question: Is the sign (positive or negative) for power_15 the same in all four models?**

**Quiz Question: (True/False) the plotted fitted lines look the same in all four plots**

# Selecting a Polynomial Degree

Whenever we have a "magic" parameter like the degree of the polynomial there is one well-known way to select these parameters: validation set. (We will explore another approach in week 4).

We split the sales dataset 3-way into training set, test set, and validation set as follows:

* Split our sales data into 2 sets: `training_and_validation` and `testing`. Use `random_split(0.9, seed=1)`.
* Further split our training data into two sets: `training` and `validation`. Use `random_split(0.5, seed=1)`.

Again, we set `seed=1` to obtain consistent results for different users.


    training_and_validation,test_data = sales.random_split(0.9,seed=1)
    train_data, validation_data = training_and_validation.random_split(0.5,seed=1)

Next you should write a loop that does the following:
* For degree in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] (to get this in python type range(1, 15+1))
    * Build an SFrame of polynomial data of train_data['sqft_living'] at the current degree
    * hint: my_features = poly_data.column_names() gives you a list e.g. ['power_1', 'power_2', 'power_3'] which you might find useful for graphlab.linear_regression.create( features = my_features)
    * Add train_data['price'] to the polynomial SFrame
    * Learn a polynomial regression model to sqft vs price with that degree on TRAIN data
    * Compute the RSS on VALIDATION data (here you will want to use .predict()) for that degree and you will need to make a polynmial SFrame using validation data.
* Report which degree had the lowest RSS on validation data (remember python indexes from 0)

(Note you can turn off the print out of linear_regression.create() with verbose = False)


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

    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 1
    PROGRESS: Number of unpacked features : 1
    PROGRESS: Number of coefficients    : 2
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.003000     | 4274505.747987     | 262315.114947 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 2
    PROGRESS: Number of unpacked features : 2
    PROGRESS: Number of coefficients    : 3
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.003000     | 4869005.244131     | 255076.149120 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 3
    PROGRESS: Number of unpacked features : 3
    PROGRESS: Number of coefficients    : 4
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 3271232.649557     | 249640.623557 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 4
    PROGRESS: Number of unpacked features : 4
    PROGRESS: Number of coefficients    : 5
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.004000     | 2676547.198434     | 248689.572032 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 5
    PROGRESS: Number of unpacked features : 5
    PROGRESS: Number of coefficients    : 6
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2330678.377343     | 248281.665797 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 6
    PROGRESS: Number of unpacked features : 6
    PROGRESS: Number of coefficients    : 7
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2344070.143295     | 247280.891725 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 7
    PROGRESS: Number of unpacked features : 7
    PROGRESS: Number of coefficients    : 8
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2452711.310604     | 246772.313122 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 8
    PROGRESS: Number of unpacked features : 8
    PROGRESS: Number of coefficients    : 9
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2504989.234013     | 246671.859042 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 9
    PROGRESS: Number of unpacked features : 9
    PROGRESS: Number of coefficients    : 10
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2525802.177260     | 246663.399621 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 10
    PROGRESS: Number of unpacked features : 10
    PROGRESS: Number of coefficients    : 11
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2532693.511976     | 246670.636994 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 11
    PROGRESS: Number of unpacked features : 11
    PROGRESS: Number of coefficients    : 12
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2534201.088398     | 246675.476971 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 12
    PROGRESS: Number of unpacked features : 12
    PROGRESS: Number of coefficients    : 13
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.010000     | 2534257.195240     | 246676.033273 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 13
    PROGRESS: Number of unpacked features : 13
    PROGRESS: Number of coefficients    : 14
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.020000     | 2534342.869094     | 246674.389430 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 14
    PROGRESS: Number of unpacked features : 14
    PROGRESS: Number of coefficients    : 15
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.020000     | 2534786.244127     | 246672.360649 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    PROGRESS: Linear regression:
    PROGRESS: --------------------------------------------------------
    PROGRESS: Number of examples          : 9761
    PROGRESS: Number of features          : 15
    PROGRESS: Number of unpacked features : 15
    PROGRESS: Number of coefficients    : 16
    PROGRESS: Starting Newton Method
    PROGRESS: --------------------------------------------------------
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | Iteration | Passes   | Elapsed Time | Training-max_error | Training-rmse |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: | 1         | 2        | 0.020000     | 2535496.382161     | 246670.782977 |
    PROGRESS: +-----------+----------+--------------+--------------------+---------------+
    PROGRESS: SUCCESS: Optimal solution found.
    PROGRESS:
    --------------------
    6
    

**Quiz Question: Which degree (1, 2, …, 15) had the lowest RSS on Validation data?**

6

Now that you have chosen the degree of your polynomial using validation data, compute the RSS of this model on TEST data. Report the RSS on your quiz.


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

**Quiz Question: what is the RSS on TEST data for the model with the degree selected from Validation data? (Make sure you got the correct degree from the previous question)**

11203988
