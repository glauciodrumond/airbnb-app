"""
AIRBNB data science project for portfolio
"""
# import libraries
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# create main
def main():
    #global file
    st.image('Airbnb-Logo-2.png', width=600)
    st.title('Data Science Project')
    st.write("This is a data science project that you can quickly visualize and "
             "check some analysis from Airbnb data.  \n"
             "Just download any **listings.csv** file, from any region and upload here "
             "to see the magic happens in this app.  \n"
             "If you don't want to download any file, there is a default file to "
             "check the app running.  \nJust choose option **Default file** in the selectbox.  \n"
             "Link to download files: [Airbnb](http://insideairbnb.com/get-the-data.html)")
    st.subheader('Airbnb Data Analysis')
    opt = st.selectbox('Choose option:', ('Upload file', 'Default file'))
    if opt == 'Default file':
        file = 'listings.csv'
    if opt == 'Upload file':
        file = st.file_uploader('Choose data to analyse(.csv)', type='csv')

    if file is not None:
        df = pd.read_csv(file)
        st.subheader('Visualizing the data frame')
        default_cols = ['name', 'neighbourhood', 'room_type', 'price']
        cols = st.multiselect("Columns to visualize", df.columns.tolist(),
                              default=default_cols)
        n = st.slider('Number of rows to visualize', min_value=5, max_value=20)
        st.write(df[cols].head(n))

        st.subheader('Is there any column with null values?')
        st.table(df.isnull().sum())

        st.subheader('Property location')
        st.write('Choose price range')
        min_price = float(df.price.min())
        max_price = float(df.price.max())
        price = st.slider('', min_value=min_price, max_value=max_price,
                          value=(min_price, max_price), step=200.0)
        mapping = df[df['price'].between(left=price[0], right=price[1])]
        st.map(mapping)

        st.subheader('How many properties are available in this data?')
        st.write('There are:', df.shape[0], 'properties available in this data.')

        st.subheader('Number of property by neighborhood')
        st.write(df.neighbourhood.value_counts())

        st.subheader('What type of property is most rented?')

        fig = go.Figure()
        fig.add_trace((go.Histogram(histfunc="count", x=df.room_type)))
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                          width=500, height=300,
                          xaxis={'categoryorder': 'total ascending'}
                          )
        st.plotly_chart(fig)

        st.subheader('Average price by room type')
        st.write(df.groupby("room_type").price.mean())

        st.subheader('Which places have the highest average price?')
        df['neighbourhood'] = df['neighbourhood'].astype(str)
        fig = px.bar(df.groupby(['neighbourhood'])['price'].mean().sort_values(ascending=True).head(20),
                     orientation='h')
        fig.update_layout(margin=dict(l=30, r=10, t=10, b=10),
                          width=600, height=500,
                          yaxis_type='category')
        st.plotly_chart(fig)

        st.subheader('What is the average rental time in days?')
        st.write('The average rental time is:', round(df.minimum_nights.mean()), 'days.')
        st.write("Summary statistic", df.minimum_nights.describe())

        st.subheader('Is there anybody who rents the property all year?')
        if df.minimum_nights.max()>=364:
            st.write('Yes, below you can see some of them where **minimum_nights** >= 365.')
            st.write(df[df.minimum_nights>=364][['host_name', 'room_type', 'neighbourhood']])
        else:
            st.write('Unfortunately there is no properties renting year round.')

        st.subheader('What is the most expensive property available?')
        st.write(df[df['price'] == df['price'].max()][['host_name', 'name', 'price']])

        st.subheader('Boxplot for price')
        fig = go.Figure()

        fig.add_trace(go.Box(
            y=df.price,
            name="Only Whiskers",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))

        fig.add_trace(go.Box(
            y=df.price,
            name="Suspected Outliers",
            boxpoints='suspectedoutliers',  # only suspected outliers
            marker=dict(
                color='rgb(8,81,156)',
                outliercolor='rgba(219, 64, 82, 0.6)',
                line=dict(
                    outliercolor='rgba(219, 64, 82, 0.6)',
                    outlierwidth=2)),
            line_color='rgb(8,81,156)'
        ))

        fig.add_trace(go.Box(
            y=df.price,
            name="Whiskers and Outliers",
            boxpoints='outliers',  # only outliers
            marker_color='rgb(107,174,214)',
            line_color='rgb(107,174,214)'
        ))

        fig.update_layout(title_text="Box Plot Styling Outliers",
                          margin=dict(l=20, r=20, t=40, b=20),
                          width=750, height=600)
        st.plotly_chart(fig)

        st.subheader('Hosts with more property')
        st.table(df.host_id.value_counts().head(10))

        st.subheader('Which property has more reviews?')
        st.write(df.groupby(['id', 'name'])['number_of_reviews']
                 .max().sort_values(ascending=False).head(20))

        st.subheader('Conclusion')
        st.write('This is only a superficial analysis that can be done in the Airbnb database. '
                 'Using this app we can quickly: \n'
                 '* load any data from Airbnb database, \n'
                 '* choose the number of columns to visualize, \n'
                 '* check for null values, \n'
                 '* visualize properties by price range, \n'
                 '* check the number of property available in the data, \n'
                 '* see property by neighborhood, \n'
                 '* check the type of property most rented, \n'
                 '* see the average price by room type, \n'
                 '* see places that have the highest average price, \n'
                 '* see the average rental time in days, \n'
                 '* check for people who rent the property all year, \n'
                 '* most expensive property available, \n'
                 '* check for outliers in price, \n'
                 '* see hosts with more property, \n'
                 '* visualize property with more reviews, and \n'
                 '* check the variable correlation.  \n\n'
                 'This data set is a short version, ideal only for an '
                 'initial approach. It is recommended that the complete data set '
                 'with 106 available attributes be used in a further exploratory analysis.')

        st.subheader('Contact me on my '
                     '[LinkedIn](https://www.linkedin.com/in/glaucio-drumond-1734a018b/)')
        st.write('*Created by*: ***Glaucio Drumond***')


if __name__ == '__main__':
    main()
