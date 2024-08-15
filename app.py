import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    loaded_rules = pd.read_pickle('sup_01-conf_01/combined_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('index.html', recommended_news=recommended_news)

@app.route('/edukasi')
def edukasi():
    loaded_rules = pd.read_pickle('sup_01-conf_01/edukasi_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'edukasi', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

@app.route('/otomotif')
def otomotif():
    loaded_rules = pd.read_pickle('sup_01-conf_01/otomotif_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'otomotif', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

@app.route('/ekonomi')
def ekonomi():
    loaded_rules = pd.read_pickle('sup_01-conf_01/ekonomi_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'ekonomi', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

@app.route('/travel')
def travel():
    loaded_rules = pd.read_pickle('sup_01-conf_01/travel_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'travel', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

@app.route('/sport')
def sport():
    loaded_rules = pd.read_pickle('sup_01-conf_01/sport_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'sport', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

@app.route('/food')
def food():
    loaded_rules = pd.read_pickle('sup_01-conf_01/food_rules.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi

    given_tags = ['adha', 'timnas', 'rumah', 'thr', 'liburan', 'skripsi']
    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, 'food', length=50)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news_category.html', recommended_news=recommended_news)

from datetime import datetime
import re

def recommend_news1(given_keywords, rules, df, category = '', idberita = '', length = 10):
    recommended_keywords = given_keywords[:]
    confidence_rules = set()  # List untuk menyimpan aturan dan nilai confidence

    # Cari aturan yang sesuai dengan given_keywords dan tambahkan ke confidence_rules
    for _, rule in rules.iterrows():
        if set(rule['antecedents']).issubset(given_keywords):
            confidence_rules.add((rule['antecedents'], rule['consequents'], int(rule['confidence'] * 10), int(rule['antecedent support'] * 200)))
    
    # Urutkan confidence_rules berdasarkan nilai confidence (dari tertinggi ke terendah)
    confidence_rules = list(confidence_rules)
    confidence_rules.sort(key=lambda x: ((2*(10-(x[3]))) + x[2]), reverse=True)
    
    # Ambil maksimal 4 keyword dengan confidence paling tinggi
    count = 0
    for antecedents, consequents, confidence, antecedents_support in confidence_rules:
      if count >= 4:
        break
      for keyword in consequents:
        if keyword not in recommended_keywords:
          recommended_keywords.append(keyword)
          count += 1
    print(recommended_keywords)
    
    # Cari berita yang mengandung recommended_keywords
    recommended_news = []
    for row in df.itertuples(index=True):
        id = row.Index
        title = row.title
        desc = row.body
        keywords = row.keywords
        date = row.date
        source = row.source
        news_category = row.category
        image=row.image
        
        if idberita == id:
            continue
        if category != '' and category != news_category:
            continue
            
        # Cek jika tidak ada keyword
        if pd.isna(keywords):
            continue

        keyword_set = set(keywords.split(','))
        matched_keywords = set(recommended_keywords) & keyword_set  # Find matching keywords
        unmatched_keywords = set(recommended_keywords) - matched_keywords  # Find remaining unmatched keywords

        # Prioritize news with more matching keywords at the beginning
        if matched_keywords:
          topic_score = sum(len(recommended_keywords) if keyword in given_keywords else len(recommended_keywords) - 2 - (recommended_keywords.index(keyword) - len(given_keywords)) for keyword in matched_keywords) * 10
          given_date = datetime.strptime(date, '%Y-%m-%d')
          today = datetime.strptime('2024-07-28', '%Y-%m-%d')
          days_difference = (today - given_date).days
          date_score = len(recommended_keywords) * 10 - (days_difference * 2)
          score = topic_score + (date_score)
          recommended_news.append((date, desc, score, source, title, id, image))

      # Sort by score
    sorted_news = sorted(recommended_news, key=lambda x: x[2], reverse=True)[:length]
    return [news for news in sorted_news]


@app.route('/news/<id>')
def show_news(id):
    # loaded_rules = pd.read_pickle('association_rules_35k-data_16850antecedents.pickle')
    df_news_tag = pd.read_csv('dataset_update_w_content.csv',index_col=0)
    # Contoh penggunaan fungsi rekomendasi
    id = int(id)
    given_tags = df_news_tag.iloc[id, 5].split(',')

    if df_news_tag.iloc[id,4] == 'edukasi':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/edukasi_rules.pickle')
    elif df_news_tag.iloc[id,4] == 'ekonomi':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/ekonomi_rules.pickle')
    elif df_news_tag.iloc[id,4] == 'otomotif':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/otomotif_rules.pickle')
    elif df_news_tag.iloc[id,4] == 'travel':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/travel_rules.pickle')
    elif df_news_tag.iloc[id,4] == 'sport':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/sport_rules.pickle')
    elif df_news_tag.iloc[id,4] == 'food':
        loaded_rules = pd.read_pickle('./sup_01-conf_01/food_rules.pickle')

    recommended_news = recommend_news1(given_tags, loaded_rules, df_news_tag, df_news_tag.iloc[id,4], id)
    # print("\nRecommended news:\n- "+ "\n- ".join(", ".join(map(str, news)) for news in recommended_news))
    return render_template('news.html', title=df_news_tag.iloc[id,0], image=df_news_tag.iloc[id,7], url=df_news_tag.iloc[id,6], recommended_news=recommended_news)

if __name__ == '__main__':
    app.run(debug=True)