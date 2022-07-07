**Student 1**: James Fallon  - **Student Number**: 18394123
**Student 2**: Alex O Neill   - **Student Number**: 18414882

**Project Supervisor**: Gareth Jones
# myTrip User Manual

## 1. Introduction

1.1 Overview

1.2 Disclaimer

## 2. App System

3.1 Layout

3.2 Key Features

## 3. App Features

3.1 Create Account

3.2 Login

3.3 Create Trip

3.4 User Interests

3.5 View Current Trip

## 3. Installation Guide

To use this web application, all you have to do is visit https://mytrip.computing.dcu.ie/register

### 1. Introduction

1.1 Overview

MyTrip is a web application for travel enthusiasts. It acts as a recommender system for people going on trips that want to experience events and activities that suit their interests. 

Currently trip planning websites already exist but we find that they appeal to a very particular group of people. Most of these websites cater towards family attractions and a lot of the time they are attractions most people are already aware of. The goal of our application is to improve this experience, recommending people attractions/activities that suit their interests and filter out the ones they will dislike. Travel websites lack this USP that keeps people returning.

MyTrip plans on solving this issue by using machine learning algorithms such as content based filtering and semantic analysis to generate recommended activities based on the user's interests.


1.2 Disclaimer
myTrip is not responsible for any inappropriate names or event information that may be offensive. Although there will be an effort to stop these from happening.

Any damage done to devices while using myTrip is not myTrip’s liability. The application was extensively tested throughout development and no harm was done toany test machine.

### 2. App System

2.1 Layout
The user will start at the register screen. They will be able to create an account, log in or use the forgot password function. Once the user manages to log in they will be greeted by the preference-selection interface.

Once the user specifies their interests, they can then create a trip. They will be asked for their destination and the dates of their trip.

Once the user has specified their preference and their interests for the recommendations, they will be taken to the current trip screen. This is the homepage.

The navigation bar will change and adapt to the page that the user is currently on. On the homepage you have links to Paths, Activities, Restaurants and best reviewed attractions. On the home page you have user settings, where a user can change their preferences.

The layout of the system will be discussed in great detail below, taking the user step-by-step through the entire system and any use case they may have.

2.2 Key Features

The main features of myTrip is to bring users together with great recommendations based on the preferences they enjoy most. These recommendations can involve anything from a coffee shop that suits the users likes to a day out in the top rated park in the city. The goal is to get people connected with more attractions then they normally would, especially with the ones that suit them the most. The key feature is being a powerful, single place to get people together and find activities and restaurants for great, effortless trip. The simple UI removes the barriers between the user and the attractions.

The accurate recommendations are the key feature. They archives their intention to display the best possible items based on the content the user has already told us they like, and also on likes and dislikes from users just like them. This means the user is not only seeing all the attractions they have already heard of, or even ones they already assumed they'd enjoy. This app is ideal for people who may not be familiar with their surrounding area, and what it can offer to them specifically.

The goal is to ensure recommendations that are recommended to the user, are accurate and improve the users experience. This only happens if they recommendations are easily accessible, which is a major feature of myTrip.

## 3. App Features

3.1 Create Account

If the user does not have an existing account, they will be offered to make one. They will be asked to enter their username, email address and password to keep their account secure. Once all these details have been entered, the user will then be able to access the account. They will be directed
to the sign in page.

<img src="images/welcome.png" alt="welcome"/>


3.1.1 Email confirmation

The email that is supplied in the create account form, will be sent a confirmation
email to ensure a secure account.

<img src="images/accountconfirm.png" alt="confirm"/>

3.2 Login

As seen in the screenshot above, if the user already has an account with myTrip, they may sign in straight away. They will be asked for their username and their password that they supplied when creating their account. Once logged in, they will be sent straight to the current trip page of the application.

3.3 Create Trip

By selecting the desired location, you can create a Trip. Once the location is clicked, you can fill in the expected arrival and departure of the trip, and the application will create your trip. This will direct you to the user-preference page. 

<img src="images/forgotpassword.png" alt="password"/>

3.4 User Interests

The user will now be able to specify their interests. They will be asked to provide a rating for some random attractions. this will be a number of restaurant and a number of activities. Below this they will also be able to specify their preferences for food types and activity types that they would enjoy most on their trip. This will be used to cater recommendations to the user. The user will then be directed to the homepage.

3.5 View Current Trip

The homepage will then be presented to the user. The homepage will present the recommendations to the user regarding their current trip. The navigation bar across the top will control what part of the page the user wishes to see. The recommendations are grouped by restaurants, activities and best reviewed. These events will be clickable by the user so they can find out more about the recommendation item. 

