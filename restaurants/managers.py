from safedelete.managers import SafeDeleteManager

from restaurants.consts import StatusChoices


class RestaurantBaseManager(SafeDeleteManager):

    def active(self):
        return self.filter(status=StatusChoices.ACTIVE)

    def hidden(self):
        return self.filter(status=StatusChoices.HIDDEN)

    def draft(self):
        return self.filter(status=StatusChoices.DRAFT)

    def checking(self):
        return self.filter(status=StatusChoices.CHECK)


class RestaurantManager(RestaurantBaseManager):
    pass


class CategoryManager(RestaurantBaseManager):
    pass


class ProductManager(RestaurantBaseManager):
    pass


class ProductPortionManager(RestaurantBaseManager):
    pass
