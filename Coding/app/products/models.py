from django.db import models

# Create your models here.
from base.models import Base
from brands.models import Brand
from customers.models import Customer
from subcategories.models import SubCategory


class Product(Base):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    des = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    NAM = 'NAM'
    NU = 'NU'
    KHAC = 'KHAC'
    GIOI_TINH = [
        (NAM, 'NAM'),
        (NU, 'NU'),
        (KHAC, 'KHAC')
    ]
    gender = models.CharField(
        max_length=100,
        choices=GIOI_TINH,
        default=NAM,
    )
    image_name = models.CharField(max_length=100)
    image_link = models.URLField(max_length=500)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product_Link(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    product_link = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_link')


class Attribute(models.Model):
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


# color and size
class Attribute_Varchar(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


# price
class Attribute_Float(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)


# quantity
class Attribute_Int(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()


class WishlistProduct(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


class CF(object):
    """docstring for CF"""

    def __init__(self, Y_data, k, dist_func=cosine_similarity, uuCF=1):
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF

        # doi row trong ma tran ( dong 0 thanh dong 1, dong 1 thanh dong 0, dong 2 giu nguyen )
        # print(Y_data[:, [1, 0, 2]])

        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        # number of users and items. Remember to add 1 since id starts from 0
        # lay so luong user trong he thong
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        # lay so luong item trong he thong
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1

    def add(self, new_data):
        """
        Update Y_data matrix when new ratings come.
        For simplicity, suppose that there is no new user or item.
        """
        self.Y_data = np.concatenate((self.Y_data, new_data), axis=0)

    def normalize_Y(self):
        users = self.Y_data[:, 0]  # all users - first col of the Y_data
        # print(users)
        # [10 10 10  8  8  8  8  8  8  4  4  4  4  8  5  5  5  5  5  6  6  6  6  6 6  6]
        self.Ybar_data = self.Y_data.copy()
        # print(self.Ybar_data)
        # [[10 16  4]
        #  [10 14  3]
        #  [10 18  1]
        #  [ 8 18  1]
        #  [ 8 16  3]
        #  [ 8  5  4]
        #  [ 8 12  4]
        #  [ 8  8  4]
        #  [ 8  1  3]
        #  [ 4  8  5]
        #  [ 4  5  3]
        #  [ 4  1  2]
        #  [ 4 14  4]
        #  [ 8 10  5]
        #  [ 5 10  3]
        #  [ 5 18  4]
        #  [ 5  5  5]
        #  [ 5  1  4]
        #  [ 5 12  3]
        #  [ 6  8  5]
        #  [ 6 14  4]
        #  [ 6  1  2]
        #  [ 6 16  4]
        #  [ 6 18  1]
        #  [ 6 12  5]
        #  [ 6  5  5]]
        self.mu = np.zeros((self.n_users,))
        # print(self.mu) co n_users user trong he thong
        # [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        for n in range(self.n_users):
            # row indices of rating done by user n since indices need to be integers, we need to convert
            # astype(np.int32) chuyen doi sang so nguyen int 32 bit

            #  # print(users)
            # [10 10 10  8  8  8  8  8  8  4  4  4  4  8  5  5  5  5  5  6  6  6  6  6 6  6]
            ids = np.where(users == n)[0].astype(np.int32)
            # print(ids)
            # []: user 0 ko danh gia san pham nao
            # []
            # []
            # []
            # [ 9 10 11 12]: user 4 danh gia san pham có stt la  9 10 11 12
            # [14 15 16 17 18]
            # [19 20 21 22 23 24 25]
            # []
            # [ 3  4  5  6  7  8 13]
            # []
            # [0 1 2]

            # indices of all ratings associated with user n
            # lay id_items ma user da danh gia
            item_ids = self.Y_data[ids, 1]
            # and the corresponding ratings
            # lay rating ma user da danh gia
            ratings = self.Y_data[ids, 2]

            # print(ratings)
            # []                ==> mean: 0
            # []                ==> mean: 0
            # []                ==> mean: 0
            # []                ==> mean: 0
            # [5 3 2 4]         ==> mean: 3.5
            # [3 4 5 4 3]       ==> mean:3.8
            # [5 4 2 4 1 5 5]   ==> mean:  3.71
            # []                ==> mean: 0
            # [1 3 4 4 4 3 5]   ==> mean: 3.43
            # []                ==> mean: 0
            # [4 3 1]           ==> mean: 2.67

            # take mean
            m = np.mean(ratings)
            if np.isnan(m):
                m = 0  # to avoid empty array and nan value

            # print(self.mu) co n_users user trong he thong
            # [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

            self.mu[n] = m
            # print(f'{self.mu[n]} ---- {ratings}')
            # normalize
            self.Ybar_data[ids, 2] = ratings - self.mu[n]


        # print(self.Ybar_data)
        ################################################
        # form the rating matrix as a sparse matrix. Sparsity is important
        # for both memory and computing efficiency. For example, if #user = 1M,
        # #item = 100k, then shape of the rating matrix would be (100k, 1M),
        # you may not have enough memory to store this. Then, instead, we store
        # nonzeros only, and, of course, their locations.
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
                                       (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))

        print(self.Ybar.toarray())
        #  (16, 10)      1
        #   (14, 10)      0
        #   (18, 10)      -1
        #   (18, 8)       -2
        #   (16, 8)       0
        #   (5, 8)        0
        #   (12, 8)       0
        #   (8, 8)        0
        #   (1, 8)        0
        #   (8, 4)        1
        #   (5, 4)        0
        #   (1, 4)        -1
        #   (14, 4)       0
        #   (10, 8)       1
        #   (10, 5)       0
        #   (18, 5)       0
        #   (5, 5)        1
        #   (1, 5)        0
        #   (12, 5)       0
        #   (8, 6)        1
        #   (14, 6)       0
        #   (1, 6)        -1
        #   (16, 6)       0
        #   (18, 6)       -2
        #   (12, 6)       1
        #   (5, 6)        1

        # Chuyển đổi ma trận này sang định dạng Hàng thưa được nén
        self.Ybar = self.Ybar.tocsr()
        print(self.Ybar.T)
        print("YBAR.T")
        print(self.Ybar.T)

    def similarity(self):
        eps = 1e-6
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
        print(self.S)

    def refresh(self):
        """
        Normalize data and calculate similarity matrix again (after
        some few ratings added)
        """
        self.normalize_Y()
        self.similarity()

    def fit(self):
        self.refresh()

    def __pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all users who rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        # print("Ádasd")
        # print(ids)
        # Ádasd
        # [ 0  2 19]
        # Ádasd
        # [ 1 10 17]
        # ....

        # Step 2:
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        print("Ádasd")
        print(users_rated_i)


        # Step 3: find similarity btw the current user and others
        # who already rated i
        sim = self.S[u, users_rated_i]
        # Step 4: find the k most similarity users
        a = np.argsort(sim)[-self.k:]
        print("SIMMMMMMMM")
        print(sim)
        print(a)
        # [1. 0. 0.]
        # [1 2 0]
        # [0. 0. 1.]
        # and the corresponding similarity levels
        nearest_s = sim[a]
        print(nearest_s)
        # How did each of 'near' users rated item i
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

        return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """

        if self.uuCF: return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend(self, u):
        """
        Determine all items should be recommended for user u.
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which
        have not been rated by u yet.
        """
        # print(self.Y_data)
        ids = np.where(self.Y_data[:, 0] == u)[0]
        # vi tri phan tu thoa dieu kien trong self.Y_data
        print("ids")
        print(np.where(self.Y_data[:, 0] == u))
        # [0 1 2]

        items_rated_by_u = self.Y_data[ids, 1].tolist()
        # print(items_rated_by_u)
        # [16, 14, 18]
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                # u = 10
                rating = self.__pred(u, i)
                # preduct user u va item thứ i
                if rating > 0:
                    recommended_items.append(i)

        return recommended_items

    def print_recommendation(self, u):
        # for u in range(self.n_users):
        #     recommended_items = self.recommend(u)
        #     if self.uuCF:
        #         print
        #         '    Recommend item(s):', recommended_items, 'for user', u
        #     else:
        #         print
        #         '    Recommend item', u, 'for user(s) : ', recommended_items
        recommended_items = self.recommend(u)
        return recommended_items
