import pandas as pd
import seaborn as sns
import requests
import stylecloud
import matplotlib.pyplot as plt


def download_white_papers():
    url = "https://reporting.alchemer.com/reportsview/?key=623127-13376550-8a09f093495c28aa861b0eda14f1103f&realtime=true"
    response = requests.get(url)
    open("whitepapers.csv", "wb").write(response.content)


def read_data():
    df = pd.read_csv('whitepapers.csv')
    df['Date Submitted'] = pd.to_datetime(df['Date Submitted'])
    df['name'] = df['First Name:Author'] + df['Last Name:Author']
    df.rename(columns={'Pick at most two of the following main topics for your white paper.':'main topic'}, inplace=True)
    df.rename(columns={'From your previous selections, pick at most two of the following subcategories for Basic Research.':'basic research'}, inplace=True)
    return df


def plot_data(df):
    sns.set_theme()
    p = sns.lineplot(data=df, x="Date Submitted", y="Response ID")
    p.figure.savefig("time_series.png")
    pass


def generate_stats(df):
    num_unique_authors = len(pd.unique(df['name']))
    print('unique author count:{}'.format(num_unique_authors))
    make_pie_chart(df)
    make_word_cloud(df)

    
def make_pie_chart(df):
    p2 = df['main topic'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(18, 10))
    p2.yaxis.set_visible(False)
    p2.xaxis.set_visible(False)
    fig = p2.get_figure()
    fig.savefig("pie.png")


def make_word_cloud(df):
    text = str(df['White Paper Title'].values)
    stylecloud.gen_stylecloud(text=text,
                              icon_name='fas fa-sun',
                              palette='colorbrewer.diverging.Spectral_11',
                              background_color='black',
                              gradient='radial',
                              size=1024)


if __name__ == "__main__":
    do_download = False
    if do_download: 
        download_white_papers()

    df = read_data()
    plot_data(df)
    generate_stats(df)
