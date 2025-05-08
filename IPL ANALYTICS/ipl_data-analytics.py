import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import csv
import matplotlib.pyplot as plt
import plotly.express as px

query_params = st.query_params
if "user" in query_params and query_params["user"]:
    st.session_state.logged_in = True
    st.session_state.current_user = query_params["user"]
else:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if not st.session_state.logged_in:
    with st.sidebar:
        selected = option_menu("Main Menu", ["Login", "Register"], icons=["box-arrow-in-right", "person-plus"],menu_icon=["cast"], orientation="vertical")
    if not st.session_state.current_user:
        if selected == "Login":
            st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    font-weight: bold;
                                }
                            </style>
                        """, unsafe_allow_html=True)
            st.markdown('<p class="big-title">LOGIN</p>', unsafe_allow_html=True)
            name = st.text_input("Enter username")
            password = st.text_input("Password", type="password")

            df = pd.read_csv("ipl_reg_data.csv")
            if st.button("Login"):
                if not name or not password:
                    st.error("Please enter both username and password.")
                elif ((df["username"] == name) & (df['password'] == password)).any():
                    st.session_state.logged_in=True
                    st.session_state.current_user=name
                    st.query_params["user"] = name
                    st.success(f"Login successful! Welcome back, {name}.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.Please try again")

        elif selected == "Register":
            st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    font-weight: bold;
                                }
                            </style>
                        """, unsafe_allow_html=True)
            st.markdown('<p class="big-title">REGISTRATION</p>', unsafe_allow_html=True)
            username = st.text_input("Username Name")
            password = st.text_input("Password", type="password")

            df = pd.read_csv("ipl_reg_data.csv")

            if st.button("Register"):
                if username in df["username"].values:
                    st.error("Username already taken. Choose another.")
                elif not username or not password:
                    st.error("All fields are required!")
                elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*()-+=<>?/" for char in password):
                    st.error(" Password must be at least 8 characters long and include at least one number and one special character (!@#$%^&*()-+=<>?/)")
                else:
                    with open("ipl_reg_data.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([username, password])
                    st.success(f" Registration successful! Welcome, {username}!")

if st.session_state.logged_in:
    with st.sidebar:
        selected = option_menu("Main menu", ["Home", "Overall Team Performance","Player Insights", "Venue Analytics","Head-to-Head Analysis","Season Overview", "Log out"],
                               icons=["house", "people", "bar-chart", "geo-alt","trophy","calendar", "box-arrow-right"],
                               menu_icon="cast", orientation="vertical")

    if selected=="Home":
        st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    color: #2E86C1;
                                    font-weight: bold;
                                }
                            </style>
                        """, unsafe_allow_html=True)
        st.subheader(f"Welcome, {st.session_state.current_user}!")
        st.markdown('<p class="big-title">IPL ANALYTICS</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://upload.wikimedia.org/wikipedia/en/1/18/2025_IPL_logo.png">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("""
        
            This dashboard provides deep insights into the IPL, helping you explore **team performances, player statistics, venue trends, and head-to-head comparisons**. Whether you're a cricket enthusiast, analyst, or strategist, this platform equips you with **data-driven insights** to understand the game better.  
            
            #### **What To Explore Here:**
            Overall Team Performance– Analyze team strengths, win-loss records, and consistency.  
            Player Insights – Discover top performers, strike rates, and impact players.  
            Venue Analytics – Identify stadium-specific trends and winning patterns.  
            Head-to-Head Analysis – Compare teams' past encounters and match outcomes.  
            Season Overview – Get a summary of every IPL season, key statistics, and highlights.  
            
            Stay ahead of the game with real-time data and analytics! 
        """)

    elif selected == "Overall Team Performance":
        df = pd.read_csv("IPL_Match_Data.csv")
        unique_team = df["Team1"].dropna().unique()
        st.markdown("""
                        <style>
                            .big-title {
                                font-size: 36px !important;
                                text-align: center;
                                font-weight: bold;
                            }
                        </style>
                    """, unsafe_allow_html=True)
        st.markdown('<p class="big-title">Team Performance</p>', unsafe_allow_html=True)
        selected_team = st.selectbox("Select the Team",unique_team)
        if selected_team:

            team_matches = df[(df["Team1"] == selected_team) | (df["Team2"] == selected_team)]
            matches = len(team_matches)
            wins = df[df["Winner"] == selected_team].shape[0]
            losses = matches - wins

            st.subheader(f" {selected_team} Performance")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Total Matches Played", value=matches)
            with col2:
                st.metric(label="Total Wins", value=wins)
            with col3:
                st.metric(label="Total Losses", value=losses)

            yearly_wins = df[df["Winner"] == selected_team].groupby("Season").size().reset_index(name='Total Wins')

            fig = px.bar(
                yearly_wins,
                x='Season',
                y='Total Wins',
                labels={'Season': 'Season', 'Total Wins': 'Wins'},
                title=f"Yearly Wins for {selected_team}"
            )
            fig.update_layout(
                xaxis=dict(
                    tickmode='linear',
                    tick0=int(yearly_wins['Season'].min()),
                    dtick=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)


    elif selected == "Player Insights":
        df = pd.read_csv("IPL_Match_Data.csv")
        unique_player = df["Player_of_Match"].dropna().unique()
        st.markdown("""
                        <style>
                            .big-title {
                                font-size: 36px !important;
                                text-align: center;
                                font-weight: bold;
                            }
                        </style>
                    """, unsafe_allow_html=True)
        st.markdown('<p class="big-title">Player Insights</p>', unsafe_allow_html=True)
        selected_player = st.selectbox("Select the Player",unique_player)

        if selected_player:
            player_award_count = df[df["Player_of_Match"] == selected_player].shape[0]
            player_matches = df[df["Player_of_Match"] == selected_player]

            player_wins = player_matches[player_matches["Winner"] == player_matches["Team1"]].shape[0] + \
                          player_matches[player_matches["Winner"] == player_matches["Team2"]].shape[0]
            player_losses = player_award_count - player_wins

            st.markdown(f"{selected_player}'s team won {player_wins} out of {player_award_count} matches when they were Player of the Match.")

            labels = ["Wins", "Losses"]
            values = [player_wins, player_losses]
            fig = px.pie(
                names=labels,
                values=values,
                title=f"Matches Won by {selected_player}'s Team when they were Player of the Match",
                hole=0  )
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)


    elif selected == "Venue Analytics":
            df = pd.read_csv("IPL_Match_Data.csv")
            unique_venue = df["Venue"].dropna().unique()
            st.markdown("""
                                    <style>
                                        .big-title {
                                            font-size: 36px !important;
                                            text-align: center;
                                            font-weight: bold;
                                        }
                                    </style>
                                """, unsafe_allow_html=True)
            st.markdown('<p class="big-title">Venue Analytics</p>', unsafe_allow_html=True)
            selected_venue = st.selectbox("Select the Venue",unique_venue)

            if selected_venue:
                venue_matches = df[df["Venue"] == selected_venue].shape[0]
                st.write(f"Matches Played at {selected_venue}: {venue_matches}")

                venue_data = df[df["Venue"] == selected_venue]
                df_long = venue_data.melt(
                    id_vars="Season",
                    value_vars=["Runs_Team1", "Runs_Team2"],
                    var_name="Team",
                    value_name="Runs"
                )
                df_long["Team"] = df_long["Team"].replace({
                    "Runs_Team1": "Team 1 Runs",
                    "Runs_Team2": "Team 2 Runs"
                })
                fig = px.scatter(
                    df_long,
                    x="Season",
                    y="Runs",
                    color="Team",
                    title=f"Runs Scored at {selected_venue} Over the Seasons",
                    labels={"Runs": "Runs Scored"}
                )
                st.plotly_chart(fig, use_container_width=True)

    elif selected == "Head-to-Head Analysis":
        st.markdown("""
                                <style>
                                    .big-title {
                                        font-size: 36px !important;
                                        text-align: center;
                                        font-weight: bold;
                                    }
                                </style>
                            """, unsafe_allow_html=True)
        st.markdown('<p class="big-title">Winner Team Analysis</p>', unsafe_allow_html=True)
        df = pd.read_csv("IPL_Match_Data.csv")
        team_1 = df["Team1"].dropna().unique()
        team_2 = df["Team2"].dropna().unique()
        selected_team1 = st.selectbox("Select Team-1",team_1)
        selected_team2 = st.selectbox("Select Team-2", team_2)

        if selected_team1 and selected_team2 and selected_team1 != selected_team2:
            head_to_head_matches = df[((df["Team1"] == selected_team1) & (df["Team2"] == selected_team2)) | ((df["Team1"] == selected_team2) & (df["Team2"] == selected_team1))]

            team1 = head_to_head_matches[head_to_head_matches["Winner"] == selected_team1].shape[0]
            team2 = head_to_head_matches[head_to_head_matches["Winner"] == selected_team2].shape[0]

            st.write(f" {selected_team1} vs {selected_team2}")
            st.write(f"{selected_team1} Wins: {team1}")
            st.write(f"{selected_team2} Wins: {team2}")

            df = pd.DataFrame({
                "Team": [selected_team1, selected_team2],
                "Wins": [team1, team2]
            })
            fig = px.bar(
                df,
                x="Team",
                y="Wins",
                title=f"Head-to-Head: {selected_team1} vs {selected_team2}",
                labels={"Wins": "Number of Wins"}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif selected == "Season Overview":
        df = pd.read_csv("IPL_Match_Data.csv")
        unique_season = df["Season"].dropna().unique()
        st.markdown("""
                                <style>
                                    .big-title {
                                        font-size: 36px !important;
                                        text-align: center;
                                        font-weight: bold;
                                    }
                                </style>
                            """, unsafe_allow_html=True)
        st.markdown('<p class="big-title">Season Analysis</p>', unsafe_allow_html=True)
        selected_season = st.selectbox("Select the Season",unique_season)

        if selected_season:
            season_data = df[df["Season"] == selected_season]
            most_wins_team = season_data["Winner"].value_counts().idxmax()
            most_wins_count = season_data["Winner"].value_counts().max()

            st.write(f"Most Wins in {selected_season}: {most_wins_team} with {most_wins_count} Wins")

            match_numbers = range(1, len(season_data) + 1)
            total_runs = season_data["Runs_Team1"] + season_data["Runs_Team2"]

            df = pd.DataFrame({
                "Match Number": match_numbers,
                "Total Runs": total_runs
            })
            fig = px.line(
                df,
                x="Match Number",
                y="Total Runs",
                title=f"Total Runs Scored in {selected_season}",
                labels={"Total Runs": "Total Runs", "Match Number": "Match Number"}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif selected == "Log out":
        st.query_params.clear()
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()