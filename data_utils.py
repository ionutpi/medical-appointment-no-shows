
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def pre_process(df):
    """     
    Pre-processes the no-show data set in the following way:
    * Convert target to binary variable
    * Convert gender to binary variable
    * Convert dates strings to timestamp

    Parameters:
    ----------
    df : the original no-show data set

    Returns:
    ----------
    pre_processes : the processed no-show data set
    
    """
    pre_processes = df.copy()
    pre_processes['No-show'] = (pre_processes['No-show']=='Yes')*1
    pre_processes['Gender'] = (pre_processes['Gender']=='F')*1
    pre_processes['ScheduledDay'] = pd.to_datetime(pre_processes['ScheduledDay'])
    pre_processes['AppointmentDay'] = pd.to_datetime(pre_processes['AppointmentDay'])
    return pre_processes


def feature_engineering(df):
    """     
    Feature engineering the no-show data set in the to produce:
    * Time, in days, between scheduled day and appointment day.
    * Number of previous appointments at time of appointment
    * Ratio of previously missed appointments at time of appointment
    * If scheduled appointment is in weekend or not

    Parameters:
    ----------
    df : the pre_processes no-show data set

    Returns:
    ----------
    features : the processed no-show data set
    
    """
    features = df.copy()

    features['DaysToApp'] = np.maximum((features['AppointmentDay'] - features['ScheduledDay']).dt.days, 0)
    features['AppWeekend'] = (features['AppointmentDay'].dt.weekday > 4)*1
    features = features.join(features.sort_values(['AppointmentDay'])
                             .groupby(['PatientId'])
                             .cumcount()
                             .rename("PrevAppoint"))
    
    features = features.join(features.sort_values(['AppointmentDay', 'PrevAppoint'])
                             .groupby(['PatientId'])['No-show']
                             .transform(lambda x: x.cumsum().shift())
                             .rename("PrevNoShowAppoint"))

    features['PrevNoShowAppoint'].fillna(0, inplace=True)

    features['NoShowRatio'] = features['PrevNoShowAppoint'] / features['PrevAppoint']
    features['NoShowRatio'].fillna(0, inplace=True)

    return features


def splitting_data(df, x_cols, test_size):
    """
    Splits the data in train and test. 
    You need to pass a list of column names representing 
    the explanatory variables.
    
    Parameters:
    ----------
    df : the features no-show data set

    Returns:
    ----------
    X_train, X_test, Y_train, Y_test : train and test explanatory variables and target data frames
    """
    split_df = df.copy()
    y = split_df['No-show']
    X = split_df[x_cols]

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size, random_state=1, stratify=y)
    return X_train, X_test, Y_train, Y_test