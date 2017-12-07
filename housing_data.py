import quandl
import pandas as pd
import pickle

api_key = open('Quandl_API_Key.txt', 'r').read()


def state_list():
    fifty_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fifty_states[0][0][1:]


def grab_initial_state_data():
    state_abbv = state_list()
    main_df = pd.DataFrame()

    for abbv in state_abbv:
        url = "FMAC/HPI_" + str(abbv)
        state = str(abbv)
        df = quandl.get(url, authtoken=api_key)
        df.rename(columns=lambda x: x.replace('Value', f'{state}'), inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
    print(main_df.head())

    pickle_out = open('fifty_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


def python_pickle_in():
    pickle_in = open('fifty_states.pickle', 'rb')
    HPI_data = pickle.load(pickle_in)
    # print(HPI_data)
    return HPI_data

def pandas_pickle():
    data = python_pickle_in()
    data.to_pickle('pandas_gen.pickle')
    HPI_data2 = pd.read_pickle('pandas_gen.pickle')
    print('New Pickle From Pandas\n', HPI_data2.head())


if __name__ == '__main__':
    grab_initial_state_data()
    python_pickle_in()
    # pandas_pickle()
