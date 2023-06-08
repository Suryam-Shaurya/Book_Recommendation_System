from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Book-Rating_x'].values),
                           rating = list(popular_df['Book-Rating_y'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    ind = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[ind])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for item_ind, score in similar_items:
        items = []
        items.extend(list(books[books['Book-Name'] == pt.index[item_ind]]['Book-Title'].values))
        items.extend(list(books[books['Book-Name'] == pt.index[item_ind]]['Book-Author'].values))
        items.extend(list(books[books['Book-Name'] == pt.index[item_ind]]['Image-URL-M'].values))
        data.append(items)

    print(data)
    return render_template('recommend.html', data = data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)