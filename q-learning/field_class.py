class Field:
    def __init__(self, size, item_pickup, start_position, item_drop_off):
        self.size = size
        self.item_pickup = item_pickup
        self.item_drop_off = item_drop_off
        self.position = start_position
        self.item_in_car = False  # esyanin alinip alinmadigini tutar

        # self.board = board_class()

    def get_number_of_states(self):  # toplam kac tane durumun oldugunu dondurur
        return self.size*self.size*self.size*self.size*self.size*self.size*2 # 2 tane self.size tasiyicinin bulunabilecegi durumlar, 2 tane self.size itemin bulunabilecegi durumlar
        # carpi 2 ise itemin alinip alinmama durumu icin
        # 2 tane daha self.size eklendi item_drop_off degisik pozisyonlara koyabilmek icin

    def get_state(self):
        # burada yapilan islem belli bir zamanda hangi durumda oldugunun hesaplanmasidir
        # durumun hesaplanmasi bire bir mapping gibi dusunulebilir, her bir durum her bir sayi ile ifade ediliyor
        # bu mapping islemi icinde asagidaki gibi bir hesaplama yapiliyor ve boylece her durumun bir sayi karsiligi oluyor
        state = self.position[0] * self.size * self.size * self.size * self.size * self.size * 2
        state = state + self.position[1] * self.size * self.size * self.size * self.size * 2
        state = state + self.item_pickup[0] * self.size * self.size * self.size * 2
        state = state + self.item_pickup[1] * self.size * self. size * 2
        state = state + self.item_drop_off[0] * self.size * 2
        state = state + self.item_drop_off[1] * 2
        if self.item_in_car:  # itemin alinmis olmasi durumu icin
            state = state + 1
        # alinmamasi durumunu yazmaya gerek yok cunku 0 ile toplayip birsey degismeyecekti
        return state

    def make_action(self, action):
        (x, y) = self.position
        if action == 0: # go south - go down
            if y == self.size - 1:  # en assagida iken assagi inme eylemi durumu
                return -10, False
            else:
                self.position = (x, y + 1)
                return -1, False
        elif action == 1:  # go north - go up
            if y == 0:  # en yukarida iken yukari cikma eylemi durumu
                return -10, False
            else:
                self.position = (x, y - 1)
                return -1, False
        elif action == 2:  # go east - go left
            if x == 0:  # en solda iken sola gitme eylemi durumu
                return -10, False
            else:
                self.position = (x - 1, y)
                return -1, False
        elif action == 3:  # go west - go right
            if x == self.size - 1:  # en sagda iken saga gitme eylemi durumu
                return -10, False
            else:
                self.position = (x + 1, y)
                return -1, False
        elif action == 4:  # pickup item
            if self.item_in_car:  # item onceden alinmissa ve tekrar pickup eylemi secilirse
                return -10, False
            elif self.item_pickup != (x, y):  # item bulundugumuz konumda degil ve alma eylemi secilirse
                return -10, False
            else:
                self.item_in_car = True  # itemin bizde oldugunu belirtmek icin
                return 20, False
        elif action == 5: # drop off item
            if not self.item_in_car:  # item bizde degilse ve drop off eylemi secilirse
                return -10, False
            elif self.item_drop_off != (x, y):  # item bizdeyse ve drop off eylemi secilirse
                self.item_pickup = (x, y)  # itemi bulundugumuz konuma birakiriz
                self.item_in_car = False  # itemin bizde olmadigini belirtmek icin
                return -10, False
            else:
                return 20, True  # True ifadesi ile olayin tamamlandigi belirtilirclass Field:
    def __init__(self, size, item_pickup, start_position, item_drop_off):
        self.size = size
        self.item_pickup = item_pickup
        self.item_drop_off = item_drop_off
        self.position = start_position
        self.item_in_car = False  # esyanin alinip alinmadigini tutar

        # self.board = board_class()

    def get_number_of_states(self):  # toplam kac tane durumun oldugunu dondurur
        return self.size*self.size*self.size*self.size*self.size*self.size*2 # 2 tane self.size tasiyicinin bulunabilecegi durumlar, 2 tane self.size itemin bulunabilecegi durumlar
        # carpi 2 ise itemin alinip alinmama durumu icin
        # 2 tane daha self.size eklendi item_drop_off degisik pozisyonlara koyabilmek icin

    def get_state(self):
        # burada yapilan islem belli bir zamanda hangi durumda oldugunun hesaplanmasidir
        # durumun hesaplanmasi bire bir mapping gibi dusunulebilir, her bir durum her bir sayi ile ifade ediliyor
        # bu mapping islemi icinde asagidaki gibi bir hesaplama yapiliyor ve boylece her durumun bir sayi karsiligi oluyor
        state = self.position[0] * self.size * self.size * self.size * self.size * self.size * 2
        state = state + self.position[1] * self.size * self.size * self.size * self.size * 2
        state = state + self.item_pickup[0] * self.size * self.size * self.size * 2
        state = state + self.item_pickup[1] * self.size * self. size * 2
        state = state + self.item_drop_off[0] * self.size * 2
        state = state + self.item_drop_off[1] * 2
        if self.item_in_car:  # itemin alinmis olmasi durumu icin
            state = state + 1
        # alinmamasi durumunu yazmaya gerek yok cunku 0 ile toplayip birsey degismeyecekti
        return state

    def make_action(self, action):
        (x, y) = self.position
        if action == 0: # go south - go down
            if y == self.size - 1:  # en assagida iken assagi inme eylemi durumu
                return -10, False
            else:
                self.position = (x, y + 1)
                return -1, False
        elif action == 1:  # go north - go up
            if y == 0:  # en yukarida iken yukari cikma eylemi durumu
                return -10, False
            else:
                self.position = (x, y - 1)
                return -1, False
        elif action == 2:  # go east - go left
            if x == 0:  # en solda iken sola gitme eylemi durumu
                return -10, False
            else:
                self.position = (x - 1, y)
                return -1, False
        elif action == 3:  # go west - go right
            if x == self.size - 1:  # en sagda iken saga gitme eylemi durumu
                return -10, False
            else:
                self.position = (x + 1, y)
                return -1, False
        elif action == 4:  # pickup item
            if self.item_in_car:  # item onceden alinmissa ve tekrar pickup eylemi secilirse
                return -10, False
            elif self.item_pickup != (x, y):  # item bulundugumuz konumda degil ve alma eylemi secilirse
                return -10, False
            else:
                self.item_in_car = True  # itemin bizde oldugunu belirtmek icin
                return 20, False
        elif action == 5: # drop off item
            if not self.item_in_car:  # item bizde degilse ve drop off eylemi secilirse
                return -10, False
            elif self.item_drop_off != (x, y):  # item bizdeyse ve drop off eylemi secilirse
                self.item_pickup = (x, y)  # itemi bulundugumuz konuma birakiriz
                self.item_in_car = False  # itemin bizde olmadigini belirtmek icin
                return -10, False
            else:
                return 20, True  # True ifadesi ile olayin tamamlandigi belirtilir