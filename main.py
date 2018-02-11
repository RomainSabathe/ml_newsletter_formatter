import yaml
import pandas as pd
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = '/home/romain/my_git/ml_newsletter_formatter'

CATEGORIES_INFO = [
    {
        'name': 'General Machine Learning',
        'url_logo': 'https://image.flaticon.com/icons/png/512/653/653500.png'},
    {
        'name': 'Deep Learning',
        'url_logo': 'https://image.flaticon.com/icons/png/512/149/149243.png'},
    {
        'name': 'Computer Vision',
        'url_logo': 'https://image.flaticon.com/icons/png/512/722/722174.png'},
    {
        'name': 'Optimisation & Learning Theory',
        'url_logo': 'https://image.flaticon.com/icons/png/512/179/179121.png'},
    {
        'name': 'GANs & Adversarial Attacks',
        'url_logo': 'https://image.flaticon.com/icons/png/512/112/112272.png'},
    {
        'name': 'Interpratibility & Fairness',
        'url_logo': 'https://image.flaticon.com/icons/png/512/45/45669.png'},
    {
        'name': 'Reinforcement Learning',
        'url_logo': 'https://image.flaticon.com/icons/png/512/249/249156.png'},
    {
        'name': 'Natural Language Processing',
        'url_logo': 'https://image.flaticon.com/icons/png/512/484/484582.png'},
    {
        'name': 'Food For Thoughts',
        'url_logo': 'https://image.flaticon.com/icons/png/512/543/543723.png'},
    {
        'name': 'Data Science & Visualisations',
        'url_logo': 'https://image.flaticon.com/icons/png/512/680/680208.png'},
    {
        'name': 'Everything Else',
        'url_logo': 'https://image.flaticon.com/icons/png/512/263/263051.png'},
    {
        'name': 'Laugh of the week',
        'url_logo': 'https://image.flaticon.com/icons/png/512/56/56243.png'}]


TYPE_LOGOS = {
    'blog': 'https://image.flaticon.com/icons/png/512/60/60736.png',
    'medium': 'https://image.flaticon.com/icons/png/512/174/174858.png',
    'paper': 'https://image.flaticon.com/icons/png/512/155/155292.png',
    'video': 'https://image.flaticon.com/icons/png/512/149/149125.png',
    'github': 'https://image.flaticon.com/icons/png/512/25/25231.png',
    'notes': 'https://image.flaticon.com/icons/png/512/149/149353.png',
    'news': 'https://image.flaticon.com/icons/png/512/4/4442.png'}



def render():
    j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                         trim_blocks=True)

    categories = _load_categories()

    with open('rendered.html', 'w') as f:
        f.write(j2_env.get_template('template.html').render(categories=categories))


def _load_categories():
    with open('newsletters/yaml/week_005.yml', 'r') as f:
        content = yaml.load(f)

    def add_article_logos(article):
        """Article is a dict."""
        types = article['type'].split(' + ')
        article['urls_logo'] = []
        for type in types:
            if type.lower() in TYPE_LOGOS:
                article['urls_logo'].append(TYPE_LOGOS[type.lower()])

        return article

    for i, article in enumerate(content['articles']):
        content['articles'][i] = add_article_logos(article)

    df = pd.DataFrame(content['articles'])
    df = df.fillna("")

    categories = []
    for category_name, group in df.groupby('category'):
        category_info = _get_category_info(category_name)
        categories.append({
            'name': category_name,
            'articles': group.to_dict(orient='records'),
            'url_logo': category_info.get('url_logo', '')})

    # Ordering
    def ordering_key(category):
        try:
            category_info = _get_category_info(category['name'])
            return category_info['position']
        except ValueError:
            # This category is unusal: we place it at the end.
            return 99
    categories = sorted(categories, key=ordering_key)
    return categories


def _get_category_info(category_name):
    for i, cat_dict in enumerate(CATEGORIES_INFO):
        if cat_dict['name'].lower() == category_name.lower():
            cat_dict['position'] = i
            return cat_dict
    print('Could not find category: {}'.format(category_name))
    raise ValueError


if __name__ == '__main__':
    render()
