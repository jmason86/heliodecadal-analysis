import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import stylecloud
from stop_words import get_stop_words
import string
from PyPDF2 import PdfReader


def download_white_paper_titles():
    url = "https://reporting.alchemer.com/reportsview/?key=623127-13376550-8a09f093495c28aa861b0eda14f1103f&realtime=true"
    response = requests.get(url)
    open("whitepapers.csv", "wb").write(response.content)


def download_white_paper_pdfs(df_titles):
    for i, url in enumerate(df_titles['1:Upload White Paper  '].values): 
        response = requests.get(url)
        title = df_titles['White Paper Title'].values[i]
        title = title.replace("/","-")
        open('white_papers/' + title + '.pdf', 'wb').write(response.content)


def read_white_paper_titles():
    df = pd.read_csv('whitepapers.csv')
    df['Date Submitted'] = pd.to_datetime(df['Date Submitted'])
    df['name'] = df['First Name:Author'] + df['Last Name:Author']
    df.rename(columns={'Pick at most two of the following main topics for your white paper.':'main topic'}, inplace=True)
    df.rename(columns={'From your previous selections, pick at most two of the following subcategories for Basic Research.':'basic research'}, inplace=True)
    return df


def read_white_paper_pdfs():
    filenames = glob.glob("white_papers/*.pdf")
    
    text = ''
    for file in filenames: 
        reader = PdfReader(file)
        for page in reader.pages:
            text+=page.extract_text()

    return text


def plot_data(df):
    sns.set_theme()
    p = sns.lineplot(data=df, x="Date Submitted", y="Response ID")
    p.figure.savefig("time_series.png")
    pass


def generate_stats(df, text_papers):
    num_unique_authors = len(pd.unique(df['name']))
    print('unique author count:{}'.format(num_unique_authors))
    make_pie_chart(df)
    text_titles = str(df['White Paper Title'].values)
    #make_word_cloud(text_titles)
    make_word_cloud(text_papers)

    
def make_pie_chart(df):
    p2 = df['main topic'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(18, 10))
    p2.yaxis.set_visible(False)
    p2.xaxis.set_visible(False)
    fig = p2.get_figure()
    fig.savefig("pie.png")


def make_word_cloud(text, shape='fas fa-sun'):
    stop_words = get_stop_words('english')
    stop_words.extend(list(string.ascii_lowercase))
    stop_words.extend(['et al', 'et', 'al', 'et al.', 'physic', 'geophys', 'doi', 'two', 'thu', 'space physic', 'res lett', 'provide', 'can', 'th', 'de', 'also', 're', 'res', 'lett', 'res lett', 'will', 'however', 'org', 'well', 'within', 'white paper', 'doi', 'http', 'https', 'figure', 'observation', 'observations', 'measurement', 'understanding', 'journal'])
    stylecloud.gen_stylecloud(text=text,
                              icon_name=shape, # To select the shape, pick a name from https://fontawesome.com/icons?d=gallery&m=free
                              palette='colorbrewer.diverging.Spectral_11',
                              background_color='black',
                              gradient='radial',
                              size=1920,
                              custom_stopwords=stop_words)


if __name__ == "__main__":
    do_download = False
    if do_download: 
        download_white_paper_titles()
    df_titles = read_white_paper_titles()
    if do_download: 
        download_white_paper_pdfs(df_titles)
    
    text_papers = read_white_paper_pdfs()
    #plot_data(df_titles)
    generate_stats(df_titles, text_papers)

    
