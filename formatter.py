def format(api_response):
    timestamp = []
    close = []
    high = []
    low = []
    open = []
    for value in api_response["timestamp"]:
        # append the value to the list
        timestamp.append(value)
    for value in api_response["Close"]:
        # append the value to the list
        close.append(value)
    for value in api_response["Open"]:
        # append the value to the list
        open.append(value)
    for value in api_response["High"]:
        # append the value to the list
        high.append(value)
    for value in api_response["Low"]:
        # append the value to the list
        low.append(value)

    return timestamp,  close, high, low, open