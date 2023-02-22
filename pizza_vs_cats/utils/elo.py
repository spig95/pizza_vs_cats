#: Default K-factor.
K_FACTOR = 10
#: Default rating class.
RATING_CLASS = float
#: Default initial rating.
INITIAL = 1200
#: Default Beta value.
BETA = 200


class Elo(object):

    def __init__(self, k_factor=K_FACTOR, rating_class=RATING_CLASS,
                 initial=INITIAL, beta=BETA):
        self.k_factor = k_factor
        self.rating_class = rating_class
        self.initial = initial
        self.beta = beta

    def expect(self, rating, other_rating):
        """The "E" function in Elo. It calculates the expected score of the
        first rating by the second rating.
        """
        diff = float(other_rating) - float(rating)
        f_factor = 2 * self.beta  # rating disparity
        return 1. / (1 + 10 ** (diff / f_factor))

    def adjust(self, rating, series):
        """Calculates the adjustment value."""
        return sum(score - self.expect(rating, other_rating)
                   for score, other_rating in series)

    def rate(self, rating, series):
        """Calculates new ratings by the game result series."""
        k = self.k_factor
        new_rating = float(rating) + k * self.adjust(rating, series)
        return new_rating

    def adjust_1vs1(self, rating1, rating2, drawn=False):
        return self.adjust(rating1, [(1, rating2)])

    def rate_1vs1(self, rating1, rating2, drawn=False):
        scores = (1, 0)
        return (self.rate(rating1, [(scores[0], rating2)]),
                self.rate(rating2, [(scores[1], rating1)]))

    def quality_1vs1(self, rating1, rating2):
        return 2 * (0.5 - abs(0.5 - self.expect(rating1, rating2)))

    def create_rating(self, value=None, *args, **kwargs):
        if value is None:
            value = self.initial
        return self.rating_class(value, *args, **kwargs)
