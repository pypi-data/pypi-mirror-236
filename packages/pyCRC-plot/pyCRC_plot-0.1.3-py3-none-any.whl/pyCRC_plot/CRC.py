# manage data and fit
import pandas as pd
import numpy as np


# first part with least squares
from scipy.optimize import curve_fit

# second part about ODR
from scipy.odr import ODR, Model, Data, RealData

# style and notebook integration of the plots
import seaborn as sns
import matplotlib.pyplot as plt


def hill_eq(x,bot,top, ec50, hs=1):
  return bot + ((top - bot)/(1+10**((ec50-x)*hs)))
  

def fit_individual(x,ydata):
  popt, pcov = curve_fit(
  f=hill_eq,       # model function
  xdata=x,   # x data
  ydata=ydata,   # y data
  p0=(0, 1, -6),      # initial value of the parameters
  maxfev=5000,
  nan_policy="omit")
  bot_opt, top_opt, ec50_opt = popt
  results = [top_opt, bot_opt, ec50_opt, "-", 10**ec50_opt , "-", "1"]
  X = np.linspace(np.min(x),np.max(x), 100)
  fitted = hill_eq(X, bot_opt, top_opt, ec50_opt)  
  return X, fitted, results


def fit_hill(x, ydata): #, label, title):
  ec50s = []
  fit_curve = []
  for cname in ydata:
    column = ydata[cname]
    popt, pcov = curve_fit(
    f=hill_eq,       # model function
    xdata=x,   # x data
    ydata=column,   # y data
    p0=(0, 1, -6),      # initial value of the parameters
    maxfev=5000,
    nan_policy="omit")
    bot_opt, top_opt, ec50_opt = popt
    X = np.linspace(np.min(x),np.max(x), 100)
    fitted = hill_eq(X, bot_opt, top_opt, ec50_opt)
    fit_curve.append(fitted)
    ec50s.append(ec50_opt)

  results = [top_opt, bot_opt, 
             np.mean(ec50s), 
             np.std(ec50s)/np.sqrt(len(ec50s)), 
             10**np.mean(ec50s) , 
             np.std([10**e for e in ec50s])/np.sqrt(len(ec50s)), 
             len(ec50s)]
  #print(f"EC50 = {np.mean(ec50s)} +- {np.std(ec50s)}, N = {len(ec50s)}\n")
  #print(f"Bottom = {bot_opt}, Top = {top_opt}")

  mean_data = np.mean(ydata, axis=1)
  sterr_data = np.std(ydata, axis=1)/np.sqrt(np.ma.size(ydata, axis=1))
  mean_curve = np.mean(fit_curve, axis=0)

  CI_curve = np.std(fit_curve, axis=0)/np.sqrt(np.ma.size(fit_curve, axis=0)) * 1.96
  #popt, pcov = curve_fit(
  #f=hill_eq,       # model function
  #xdata=x,   # x data
  #ydata=mean_data,   # y data
  #p0=(0, 1, -6),      # initial value of the parameters
  #maxfev=5000)
  #bot_opt_mean, top_opt_mean, ec50_opt_mean = popt
  #X = np.linspace(np.min(x),np.max(x), 100)
  #fitted = hill_eq(X, bot_opt_mean, top_opt_mean, ec50_opt_mean)
  return (X, mean_curve, CI_curve, mean_data, sterr_data, results)

