
# function to return the count of passed series or list


def count(data):
    total_count = len(data)
    return total_count


# function to return the required dataframe or series

def get_data(dataframe,required_column_list):
    dataframe = dataframe[required_column_list]
    return dataframe


# function to plot bar chart

def plot_bar(plotly_obj, dataframe, x_axis, y_axis, plot_title):

    fig = plotly_obj.bar(dataframe, x=x_axis,
                 y=y_axis,
                 text=y_axis,
                 )

    fig.update_traces(width=0.5,
                      textposition='outside',
                      marker_color='#F2BB05',
                      hovertemplate = None,
                      hoverinfo= 'skip',
                       )

    fig.update_yaxes(visible=False)

    fig.update_xaxes({'type' : 'category'})

    fig.update_layout(title_text='<i style="font-size:1.6rem;">'+ plot_title +'</i>',
                      title_x=0.5, title_y=0.95,
                      uniformtext_minsize=8,
                      uniformtext_mode='hide',
                      xaxis_title=None,
                      plot_bgcolor = '#0F0A0A')
    return fig


def get_grouped_data(dataframe,group_by_col, to_be_grouped):
    wc_matches_v1_grouped = dataframe.groupby(group_by_col)[to_be_grouped].sum().reset_index()
    return wc_matches_v1_grouped


def get_wc_matches_v1(dataframe, own_goal=False, filter_year=0, filter_country=''):
    req_cols = ['year', 'country', 'player_id', 'player_name', 'home_goals', 'away_goals', 'own_goal']
    dataframe = dataframe[req_cols]
    dataframe['goals'] = dataframe['home_goals'] + dataframe['away_goals']

    if filter_year != 0:
        filter_1 = dataframe['year'] == filter_year
        dataframe = dataframe[filter_1]

    if filter_country != '':
        filter_1 = dataframe['country'] == filter_country
        dataframe = dataframe[filter_1]

    if (own_goal):
        dataframe = dataframe[dataframe['own_goal'] == 0]

    return dataframe

# function to get total world cups played


def get_total_wc_played(dataframe):
    req_col = ['edition']
    total_wc_played = get_data(dataframe,req_col).iloc[-1].values[0]
    return total_wc_played


# total participating nations list
def get_total_participating_nations(dataframe,filter_year=0):
    req_col = 'country'
    if filter_year == 0:
        participating_nations = dataframe[req_col].unique()
        return participating_nations
    else:
        filter_1 = dataframe['year'] == filter_year
        participating_nations = dataframe[filter_1][req_col].unique()
        return participating_nations


# Country and World Cup Win Freqency

def get_world_cup_win_frequency(dataframe):
    bar_data = dataframe['first'].value_counts().reset_index().rename(columns={'index': 'country', 'first': 'no_of_wins'})
    return bar_data

# getting the list of year to add to the select box


def get_years_list(dataframe):
    year_list = dataframe['year'].tolist()
    return year_list;

# using this function first,second, third, hosting_country and total_attendance
# will be extracted for a given year


def get_yearly_overall_data(dataframe,selected_year,column_name):
    filter_year = dataframe['year'] == selected_year
    dataframe = dataframe[filter_year]
    data = dataframe[column_name].values[0]
    return data


# getting the participation years of given country

def get_country_participation_years(dataframe,filter_country):
    req_col = 'year'
    filter_1 = dataframe['country'] == filter_country
    participating_years = dataframe[filter_1][req_col].unique()
    return participating_years


# given a country how many times it won a world cup, first position, second position

def country_wc_win_position(dataframe,country_filter,pos):
    if pos == 1:
        filter_1 = dataframe['first'] == country_filter
        total_first = sum(filter_1)
        return total_first
    elif pos == 2:
        filter_1 = dataframe['second'] == country_filter
        total_second = sum(filter_1)
        return total_second
    elif pos == 3:
        filter_1 = dataframe['third'] == country_filter
        total_third = sum(filter_1)
        return total_third


