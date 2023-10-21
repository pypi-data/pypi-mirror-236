#-------------------------------------------------------------------------------  
def get(tickers, period, interval, norm=False):
    X = yf.download(tickers=tickers, period=period, interval=interval)
    
    if norm == True:
        X = X.Close.div(X.Close.iloc[0]).mul(100)
    return X
#-------------------------------------------------------------------------------   
def shift(df, num_shift, drop_first_shift=True, Label=True): 
    X = df['Close']
    shifted_dict = {}
    shifted_dict['Close'] = df['Close']
    
    for i in range(1,num_shift+1):
        shifted_series = X.shift(i)
        shifted_dict[f'sh{i}'] = shifted_series
    
    X2 = pd.DataFrame(shifted_dict)
    
    if drop_first_shift == True :
        X2 = X2[num_shift::]
    
    if Label == True :
        X2['Label'] = X2['Close']-X2['sh1']
        X2.loc[X2['Label'] < 0 , 'Label'] = 0
        X2.loc[X2['Label'] > 0 , 'Label'] = 1
    
    return X2
#-------------------------------------------------------------------------------   
def Candlestick(symbol):
    fig = go.Figure(data=[go.Candlestick(x=symbol.index,
                                     open=symbol['Open'],
                                     high=symbol['High'],
                                     low=symbol['Low'],
                                     close=symbol['Close'])])
    fig.update_layout(title=f"{symbol} Candlestick Chart",
                  xaxis_title="Date",
                  yaxis_title="Price",
                  xaxis_rangeslider_visible=False)
    return fig.show()
#-------------------------------------------------------------------------------   
def trainTest(dataframe, label, traintest=True, split_size=None):
    X = dataframe.drop(label, axis=1)
    y = dataframe[label]
    
    if traintest == True:
        Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = split_size)
        return Xtrain, Xtest, ytrain, ytest
    
    else:
        return X,y
    return fig.show()
#-------------------------------------------------------------------------------  
def slicArray(X,y,sliceTrain=0.8):
    slicTrain = X.shape[0]*sliceTrain

    Xtrain = X[0:int(slicTrain)]
    Xtest = X[int(slicTrain):]
    ytrain = y[0:int(slicTrain)]
    ytest = y[int(slicTrain):]
    
    return Xtrain , Xtest , ytrain , ytest
#-------------------------------------------------------------------------------  