class ArticleReadTimeEngine:
    """
    Defines how long it takes to read an article
    """

    def __init__(self, article):
        self.article = article
        self.words_per_minute = 250
        self.banner_image_adjustment_time = round(1 / 6, 3)

    def check_article_has_banner_image(self):
        """checks if the article has an image"""
        has_banner_image = True
        if not self.article.banner_image:
            has_banner_image = False
            self.banner_image_adjustment_time = 0
        return has_banner_image

    def get_title(self):
        """returns the title of an article"""
        return self.article.title

    def get_tags(self):
        """returns all tags spilt by space in a list"""
        tag_words = []
        [tag_words.extend(tag_word.split()) for tag_word in self.article.list_of_tags]
        return tag_words

    def get_body(self):
        """returns the body of an article"""
        return self.article.body

    def get_description(self):
        """returns the description of an article"""
        return self.article.description

    def get_article_details(self):
        """returns a list containing the title, body, description, and tags of an article"""
        details = []
        details.extend(self.get_title().split())
        details.extend(self.get_body().split())
        details.extend(self.get_description().split())
        details.extend(self.get_tags())
        return details

    def get_read_time(self):
        word_length = len(self.get_article_details())
        read_time = 0
        self.check_article_has_banner_image()

        if word_length:
            time_to_read = word_length / self.words_per_minute
            if time_to_read < 1:
                read_time = (
                        str(round((time_to_read + self.banner_image_adjustment_time) * 60))
                        + " second(s)"
                )
            else:
                read_time = (
                        str(round(time_to_read + self.banner_image_adjustment_time))
                        + " minute(s)"
                )
            return read_time


"""
************* In articles.read_time_engine.py ArticleReadTimeEngine.get_article_details *************
details: ['This', 'Immutable', 'QueryDict', 'Duis', 'aute', 'irure', 'dolor', 'in', 'reprehenderit', 'in', 'voluptate', 
'velit', 'esse', 'cillum', 'dolore', 'eu', 'fugiat', 'nulla', 'pariatur.', 'Excepteur', 'sint', 'occaecat', 'cupidatat',
 'non', 'proident,', 'sunt', 'in', 'culpa', 'qui', 'officia', 'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum.', 
 'Duis', 'aute', 'irure', 'dolor', 'in', 'reprehenderit', 'in', 'voluptate', 'dict', 'query', 'unchanging']
************* In articles.read_time_engine.py ArticleReadTimeEngine.get_article_details *************

"""
