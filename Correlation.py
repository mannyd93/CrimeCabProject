import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

crimeRate = pd.read_csv("chicagoCrimeRates.csv")
crimeRate = pd.Series.tolist(crimeRate["Crime Rate"])

pickupRate = pd.read_csv("chicagoTaxiRates.csv")
pickupRate = pd.Series.tolist(pickupRate["Pickup Rate"])

dropoffRate = pd.read_csv("chicagoTaxiRates.csv")
dropoffRate = pd.Series.tolist(dropoffRate["Dropoff Rate"])


 
def getPoints(xvalues, yvalues):
    points = []
    for i in range(len(xvalues)):
        points.append((xvalues[i], yvalues[i]))
    return points

def compute_error_for_line_given_points(b, m, points):
    totalError = 0
    for i in range( len(points)):
        x = points[i] [0]
        y = points[i][ 1]
        totalError += (y - (m * x + b)) ** 2
    return totalError / float(len(points))

def step_gradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x = points[i][ 0]
        y = points[i][ 1]
        b_gradient += -(2/N) * (y - ((m_current * x) + b_current))
        #print((m_current * x) + b_current)
        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current))
    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]

def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
    b = starting_b
    m = starting_m
    for i in range(num_iterations):
        b, m = step_gradient(b, m, points, learning_rate)
    return [b, m]


def run(cabRate, nameOfRate):
    points = getPoints(crimeRate, cabRate)
    learning_rate = 0.0000000000001
    initial_b = 0 # initial y-intercept guess
    initial_m = 0 # initial slope guess
    num_iterations = 1000
    print ("Starting gradient descent at b = {0}, m = {1}, error = {2}".format(initial_b, initial_m, compute_error_for_line_given_points(initial_b, initial_m, points)))
    print ("Running...")
    [b, m] = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
    print ("After {0} iterations b = {1}, m = {2}, error = {3}".format(num_iterations, b, m, compute_error_for_line_given_points(b, m, points)))
    yvalues = [m*x + b for x in crimeRate]
   
    plt.plot(crimeRate, yvalues)
    plt.scatter(crimeRate, cabRate)
    plt.xlabel("Crime Rate")
    plt.ylabel(nameOfRate)
    title = "Crime Rate vs. " + nameOfRate
    plt.title(title)
    plt.show()


run(pickupRate, "Pickup Rate")
#run(dropoffRate, "Dropoff Rate")





