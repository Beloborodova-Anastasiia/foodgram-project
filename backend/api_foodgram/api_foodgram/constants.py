FILTER_FAVORITE_OR_SHOPPING = 1
ERROR_MESSAGES = {
    'exists': 'уже есть в',
    'non_exists': 'нет в',
    'ban_himself': 'Вы не можете добавить себя в',
}
FAVORITE_OR_SHOPPING = ['favorite', 'shopping']
PATH_TO_DATA = '/*/foodgram-project-react/data/ingredients.csv'
PATH_FAVORITE = r'(?P<recipe_id>[0-9]+)/favorite'
PATH_SUBSCRIPTIONS = 'subscriptions'
PATH_SUBSCRIBE = r'(?P<author_id>[0-9]+)/subscribe'
PASH_SHOPPING_CART = r'(?P<recipe_id>[0-9]+)/shopping_cart'
PATH_DOWNLOAD_SHOPPING_CART = 'download_shopping_cart'
RECIPES_LIMIT_DEFAULT = 3
SAVE_AS = 'attachment; filename="shopping_cart.csv"'
SUBSCRIB_IN_PATH = 'subscrib'
