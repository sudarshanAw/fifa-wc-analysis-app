import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image

import helper
import utils

# getting the files
wc_overall = pd.read_csv('WorldCupOverall.csv')
wc_matches = pd.read_csv('MatchesPlayersGoals.csv')
qualified_teams = pd.read_csv('QualifiedTeams.csv')

# starting streamlit

st.set_page_config(layout="wide")

st.sidebar.subheader('Fifa World Cup (1930 - 2018)')

image = Image.open('fifa.png')
st.sidebar.image(image)

user_menu = st.sidebar.radio('Select a category',
                 (utils.overall,
                  utils.year_wise,
                  utils.country_wise))


# Overall

if user_menu == utils.overall:

    total_wc_played = helper.get_total_wc_played(wc_overall)
    # Total participating nations count
    total_nation_participation_list = helper.get_total_participating_nations(qualified_teams)
    total_nation_participation_count = helper.count(total_nation_participation_list)

    # country and world cup wins

    country_wc_win_freq = helper.get_world_cup_win_frequency(wc_overall)
    chart = helper.plot_bar(px, country_wc_win_freq,
                            x_axis=utils.country,
                            y_axis=utils.no_of_wins,
                            plot_title='Country and World Cup Wins')

    with st.container():
        padding_1, col1, padding_2 = st.columns([10,19,10])
        with col1:
            st.header('Total World Cup Events : ' + str(total_wc_played))
            st.subheader('Total Participating Countries : ' + str(total_nation_participation_count))
            st.header('')


    with st.container():
        col1,padding_1,col2,padding_2 = st.columns([9,6,22,2])
        with col1:
            st.dataframe(pd.Series(total_nation_participation_list, name='Participating Countries'),
                         use_container_width=True)
        with col2:
            st.plotly_chart(chart,
                            use_container_width=True)
    # get wc matches v1

    wc_matches_v1 = helper.get_wc_matches_v1(wc_matches)
    wc_matches_v1_new = helper.get_wc_matches_v1(wc_matches, True)

    # year and total goals
    year_goals_grouped = helper.get_grouped_data(wc_matches_v1,
                                                 group_by_col=utils.year,
                                                 to_be_grouped=utils.goals)
    year_goals_chart = helper.plot_bar(px,
                                       year_goals_grouped,
                                       x_axis=utils.year,
                                       y_axis=utils.goals,
                                       plot_title='FIFA World Cup Goals from 1930 - 2018',
                                       )

    with st.container():
        st.plotly_chart(year_goals_chart,use_container_width=True)


    # player and total goals
    player_goals_grouped = helper.get_grouped_data(wc_matches_v1_new,
                                                   group_by_col=[utils.player_id, utils.player_name],
                                                   to_be_grouped=utils.goals)

    player_goals_grouped = player_goals_grouped.sort_values(by=utils.goals,
                                                            ascending=False)

    player_goal_chart = helper.plot_bar(px,
                                        player_goals_grouped[0:7],
                                        x_axis=utils.player_name,
                                        y_axis=utils.goals,
                                        plot_title='Top 7 goal scorers of all time',
                                        )


    # country and total goals

    country_goals_grouped = helper.get_grouped_data(wc_matches_v1_new,
                                                    group_by_col=utils.country,
                                                    to_be_grouped=utils.goals)

    country_goals_grouped = country_goals_grouped.sort_values(by=utils.goals,
                                                              ascending=False)

    country_goal_chart = helper.plot_bar(px,
                                         country_goals_grouped[0:7],
                                         utils.country,
                                         utils.goals,
                                         plot_title='Top 7 goal scoring countries of all time')


    with st.container():
        col1,padding,col2 = st.columns([19,1,19])
        with col1:
            #st.subheader('Top 10 Goal Scorers of all time')
            st.plotly_chart(player_goal_chart,use_container_width=True)


        with col2:
            #st.subheader('Country scoring highest goals')
            st.plotly_chart(country_goal_chart,use_container_width=True)

# Year-Wise Analysis Section

elif user_menu == utils.year_wise:

    # adding the select box of year to the sidebar

    years_list = helper.get_years_list(wc_overall)

    selected_year = st.sidebar.selectbox('Select Year',years_list)

    total_participating_teams_list = helper.get_total_participating_nations(qualified_teams,
                                                                            selected_year)

    total_participating_teams_count = helper.count(total_participating_teams_list)


    host_country = helper.get_yearly_overall_data(wc_overall,
                                                  selected_year,
                                                  utils.host_country)

    total_attendance = helper.get_yearly_overall_data(wc_overall,
                                                      selected_year,
                                                      utils.total_attendance)


    first = helper.get_yearly_overall_data(wc_overall,
                                           selected_year,
                                           utils.first)


    second = helper.get_yearly_overall_data(wc_overall,
                                            selected_year,
                                            utils.second)
    third = helper.get_yearly_overall_data(wc_overall,
                                           selected_year,
                                           utils.third)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Year : ' + str(selected_year))
    with col2:
        st.subheader('Host Country : ' + str(host_country))
    with col3:
        st.subheader('Total Attendance : ' + str(total_attendance))

    col1,col2 = st.columns(2)
    with col1:
        st.header('')
        st.subheader('Total Participating Nations : ' + str(total_participating_teams_count))
        st.dataframe(pd.Series(total_participating_teams_list,
                               name='Total Participating Nations'),use_container_width=False)

    with col2:
        st.header('')
        st.header('')
        st.header('')
        st.header('')
        st.header('Champion : ' + str(first))
        st.header('First Runner Up : ' + str(second))
        st.header('Second Runner Up : ' + str(third))

    # Task Top 5 highest scoring countries for a given year

    countries_yearly_filtered = helper.get_wc_matches_v1(wc_matches,
                                                         own_goal=True,
                                                         filter_year=selected_year)

    countries_filtered_grouped = helper.get_grouped_data(countries_yearly_filtered,
                                                         group_by_col=utils.country,
                                                         to_be_grouped= utils.goals)

    countries_filtered_grouped = countries_filtered_grouped.sort_values(by= utils.goals,
                                                                        ascending=False)

    country_goal_yearly_chart = helper.plot_bar(px,
                                                countries_filtered_grouped[0:5],
                                                x_axis=utils.country,
                                                y_axis=utils.goals,
                                                plot_title='Top 5 highest scoring Countries')


    # Task Top 5 highest scoring player for a given year

    players_yearly_filtered = helper.get_wc_matches_v1(wc_matches,
                                                       own_goal=True,
                                                       filter_year=selected_year)

    players_filtered_grouped = helper.get_grouped_data(players_yearly_filtered,
                                                       group_by_col=[utils.player_id,utils.player_name],
                                                       to_be_grouped=utils.goals)

    players_filtered_grouped = players_filtered_grouped.sort_values(by=utils.goals,
                                                                    ascending=False)

    players_goal_yearly_chart = helper.plot_bar(px,
                                                players_filtered_grouped[0:5],
                                                x_axis=utils.player_name,
                                                y_axis=utils.goals,
                                                plot_title='Top 5 highest Scoring Players')


    col1,padding,col2 = st.columns([18,3,18])

    with col1:
        st.header('')
        st.plotly_chart(country_goal_yearly_chart, use_container_width=True)

    with col2:
        st.header('')
        st.plotly_chart(players_goal_yearly_chart, use_container_width=True)


elif user_menu == utils.country_wise:

    # getting total participating countries list and add to the selected country sidebar

    total_participating_nations_list = helper.get_total_participating_nations(qualified_teams)
    selected_country = st.sidebar.selectbox('Select Country', total_participating_nations_list)

    country_participation_years = helper.get_country_participation_years(qualified_teams, selected_country)
    country_participation_years_count = helper.count(country_participation_years)


    # given the country how many times it was first , second and third
    first_position = helper.country_wc_win_position(wc_overall, selected_country, 1)

    second_position = helper.country_wc_win_position(wc_overall, selected_country, 2)

    third_position = helper.country_wc_win_position(wc_overall, selected_country, 3)

    padding_1,col1,padding_2 = st.columns([14,15,10])
    with col1:
        st.header(selected_country)


    col1, col2 = st.columns(2)
    with col1:
        st.header('')
        st.subheader('Total World Cup Participations : ' + str(country_participation_years_count))
        st.dataframe(pd.Series(country_participation_years, name='Participation Years'))


    with col2:
        st.header('')
        st.header('')
        st.header('')
        st.header('')
        st.header('World Cup Wins : ' + str(first_position))
        st.header('Second Position : ' + str(second_position))
        st.header('Third Position : ' + str(third_position))

    # how many goal a country has scored in the wc it has participated
    df_filtered_by_country = helper.get_wc_matches_v1(wc_matches,
                                                      filter_country=selected_country)
    country_yearly_goals_grouped = helper.get_grouped_data(df_filtered_by_country,
                                                           group_by_col=utils.year,
                                                           to_be_grouped=utils.goals)

    country_yearly_goals_chart = helper.plot_bar(px,
                                                 country_yearly_goals_grouped,
                                                 x_axis=utils.year,
                                                 y_axis=utils.goals,
                                                 plot_title='Goals in participated world cups')
    with st.container():
        st.header('')
        st.plotly_chart(country_yearly_goals_chart,use_container_width=True)

    # Top 5 players with most goals for a given country

    player_country_goals = helper.get_wc_matches_v1(wc_matches,
                                                    own_goal=True,
                                                    filter_country=selected_country)

    player_country_goals_grouped = helper.get_grouped_data(df_filtered_by_country,
                                                           group_by_col=[utils.player_id, utils.player_name],
                                                           to_be_grouped=utils.goals)

    player_country_goals_grouped = player_country_goals_grouped.sort_values(by=utils.goals,
                                                                            ascending=False)

    player_country_goals_grouped_chart = helper.plot_bar(px, player_country_goals_grouped[0:10],
                                                         x_axis=utils.player_name,
                                                         y_axis=utils.goals,
                                                         plot_title='Top Scorers in World Cups')
    with st.container():
        st.header('')
        st.plotly_chart(player_country_goals_grouped_chart,use_container_width=True)