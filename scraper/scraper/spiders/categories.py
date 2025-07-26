from datetime import datetime
categorie=['catalogue/category/books/travel_2/index.html',
 'catalogue/category/books/mystery_3/index.html',
 'catalogue/category/books/historical-fiction_4/index.html',
 'catalogue/category/books/sequential-art_5/index.html',
 'catalogue/category/books/classics_6/index.html',
 'catalogue/category/books/philosophy_7/index.html',
 'catalogue/category/books/romance_8/index.html',
 'catalogue/category/books/womens-fiction_9/index.html',
 'catalogue/category/books/fiction_10/index.html',
 'catalogue/category/books/childrens_11/index.html',
 'catalogue/category/books/religion_12/index.html',
 'catalogue/category/books/nonfiction_13/index.html',
 'catalogue/category/books/music_14/index.html',
 'catalogue/category/books/default_15/index.html',
 'catalogue/category/books/science-fiction_16/index.html',
 'catalogue/category/books/sports-and-games_17/index.html',
 'catalogue/category/books/add-a-comment_18/index.html',
 'catalogue/category/books/fantasy_19/index.html',
 'catalogue/category/books/new-adult_20/index.html',
 'catalogue/category/books/young-adult_21/index.html',
 'catalogue/category/books/science_22/index.html',
 'catalogue/category/books/poetry_23/index.html',
 'catalogue/category/books/paranormal_24/index.html',
 'catalogue/category/books/art_25/index.html',
 'catalogue/category/books/psychology_26/index.html',
 'catalogue/category/books/autobiography_27/index.html',
 'catalogue/category/books/parenting_28/index.html',
 'catalogue/category/books/adult-fiction_29/index.html',
 'catalogue/category/books/humor_30/index.html',
 'catalogue/category/books/horror_31/index.html',
 'catalogue/category/books/history_32/index.html',
 'catalogue/category/books/food-and-drink_33/index.html',
 'catalogue/category/books/christian-fiction_34/index.html',
 'catalogue/category/books/business_35/index.html',
 'catalogue/category/books/biography_36/index.html',
 'catalogue/category/books/thriller_37/index.html',
 'catalogue/category/books/contemporary_38/index.html',
 'catalogue/category/books/spirituality_39/index.html',
 'catalogue/category/books/academic_40/index.html',
 'catalogue/category/books/self-help_41/index.html',
 'catalogue/category/books/historical_42/index.html',
 'catalogue/category/books/christian_43/index.html',
 'catalogue/category/books/suspense_44/index.html',
 'catalogue/category/books/short-stories_45/index.html',
 'catalogue/category/books/novels_46/index.html',
 'catalogue/category/books/health_47/index.html',
 'catalogue/category/books/politics_48/index.html',
 'catalogue/category/books/cultural_49/index.html',
 'catalogue/category/books/erotica_50/index.html',
 'catalogue/category/books/crime_51/index.html']

date=datetime.now().strftime("%Y-%m-%d")

def get_categories(categorie=categorie, date=date):
    started_time = datetime.strptime('2025-07-26', "%Y-%m-%d")
    execution_date = datetime.strptime(date, "%Y-%m-%d")
    
    index=(execution_date-started_time).days
        
    return categorie[index]

get_categories()
