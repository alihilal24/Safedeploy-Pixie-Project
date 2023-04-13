import sys
import pandas as pd


def addToRow(df, row, col, val):
    df.at[row, col] = val
    return df


if __name__ == '__main__':

    inputfilename = sys.argv[1]

    outputfilename = sys.argv[2] if len(
        sys.argv) > 2 else 'Formatted_Pod_Performance.csv'

    data = pd.read_csv(inputfilename, on_bad_lines='skip')

    # filename = input("Enter name of new CSV filename: ")
    #
    # if not filename.endswith('.csv'):
    #     filename += '.csv'

    index_to_remove = data[data['Table ID: network_timeseries']
                           == 'Table ID: Pod Performance Flamegraph'].index[0]+2

    # Drop all rows before the index of the specific string
    data = data.drop(index=range(index_to_remove))

    df = pd.DataFrame(columns=['NAMESPACE', 'POD', 'CONTAINER', 'CMDLINE',
                      'STACK TRACE ID', 'STACK TRACE', 'COUNT', 'PERCENTAGE'])

    for index, row in data.iterrows():
        st = str(row['Table ID: network_timeseries'])
        arr = st.split()
        df = addToRow(df, index, 'NAMESPACE', arr[0])
        df = addToRow(df, index, 'POD', arr[1])
        df = addToRow(df, index, 'CONTAINER', arr[2])
        df = addToRow(df, index, 'CMDLINE', arr[3])
        df = addToRow(df, index, 'STACK TRACE ID', arr[4])
        stacktrace = ''
        for i in range(5, len(arr)-3):
            stacktrace += arr[i] + ' '
        df = addToRow(df, index, 'STACK TRACE', stacktrace)
        df = addToRow(df, index, 'COUNT', arr[len(arr)-3])
        df = addToRow(df, index, 'PERCENTAGE', str(arr[len(arr)-1]))

    # df.to_csv(filename, index=False)

    df.to_csv(outputfilename, index=False)
