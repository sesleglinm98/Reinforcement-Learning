class Field:
    def __init__(self, size, agent_position, evil_man_position, castle_position):
        self.size = size
        self.agent_position = agent_position
        self.evil_man_position = evil_man_position
        self.reward_position = evil_man_position 
        self.castle_position = castle_position
        self.reward_taken = False  # odulun alinip alinmadigini tutar
        self.evil_man_dead = False  # kotu adamin olup olmedigini tutar

    def get_number_of_states(self):  # toplam kac tane durumun oldugunu dondurur
        # ajan ve kotu adam farkli pozisyonlarda olabilir, castle'ın pozisyonu fix bi yerde olucak
        return self.size*self.size*self.size*self.size*2*2
        # carpi 2 odulun alinip alinmama durumu icin
        # carpi 2 kotu adamin olu olup olmama durumu icin

    def get_state(self):
        # burada yapilan islem belli bir zamanda hangi durumda oldugunun hesaplanmasidir
        # durumun hesaplanmasi bire bir mapping gibi dusunulebilir, her bir durum her bir sayi ile ifade ediliyor
        # bu mapping islemi icinde asagidaki gibi bir hesaplama yapiliyor ve boylece her durumun bir sayi karsiligi oluyor
        state = self.agent_position[0] * self.size * self.size * self.size * 2 * 2
        state = state + self.agent_position[1] * self.size * self.size * 2 * 2
        state = state + self.evil_man_position[0] * self.size * 2 * 2
        state = state + self.evil_man_position[1] * 2 * 2
        if self.evil_man_dead:
            state = state + 3
        else:
            state = state + 2
        if self.reward_taken:
            state = state + 1
        # alinmamasi durumunu yazmaya gerek yok cunku 0 ile toplayip birsey degismeyecekti
        return state

    def make_action(self, action):
        # 3. bir deger dondurulur bu deger yapilan aksiyon sonucundaki hareketi tanimlar, boylece board_class a gonderilerek yapilacak aksiyon belirlenmis olur
        # yapilacak hareketler -> 0 = move ve etkisi olmayan hareketler icin   1 = basarili evil oldurme icin   2 = basarili reward alma icin   3 == rewardin sahaya birakilmasi    4 = basarili rewardi castle'a koyma icin
        (x, y) = self.agent_position
        if action == 0: # go down
            if y == self.size - 1:  # en assagida iken assagi inme eylemi durumu
                return -10, 0, False
            else:
                self.agent_position = (x, y + 1)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # agent evil pozisyonunun yanina geldiyse ceza puanı alip gorev basarisiz olur 
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 1:  # go up
            if y == 0:  # en yukarida iken yukari cikma eylemi durumu
                return -10, 0, False
            else:
                self.agent_position = (x, y - 1)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # agent evil pozisyonunun yanina geldiyse ceza puanı alip gorev basarisiz olur 
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 2:  # go left
            if x == 0:  # en solda iken sola gitme eylemi durumu
                return -10, 0, False
            else:
                self.agent_position = (x - 1, y)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # agent evil pozisyonunun yanina geldiyse ceza puanı alip gorev basarisiz olur 
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 3:  # go right
            if x == self.size - 1:  # en sagda iken saga gitme eylemi durumu
                return -10, 0, False
            else:
                self.agent_position = (x + 1, y)
                if self.agent_position[0] == self.evil_man_position[0] and self.agent_position[1] == self.evil_man_position[1]:  # agent evil pozisyonunun yanina geldiyse ceza puanı alip gorev basarisiz olur 
                    if not self.evil_man_dead:
                        return -20, 0, True
                return -1, 0, False
        elif action == 4:  # pull trigger
            if self.evil_man_dead:
                return -1, 0, False
            elif abs(self.evil_man_position[0] - x) == 1 and abs(self.evil_man_position[1] - y) == 1:
                # print("durum-1", self.evil_man_position, x, y)
                self.evil_man_dead = True
                return 10, 1, False
            elif abs(self.evil_man_position[0] - x) == 0 and abs(self.evil_man_position[1] - y) == 1:
                # print("durum-2", self.evil_man_position, x, y)
                self.evil_man_dead = True
                return 10, 1, False
            elif abs(self.evil_man_position[0] - x) == 1 and abs(self.evil_man_position[1] - y) == 0:
                # print("durum-3", self.evil_man_position, x, y)
                self.evil_man_dead = True
                return 10, 1, False
            else:
                return -1, 0, False
        elif action == 5:  # pickup reward
            if self.reward_taken:  # item onceden alinmissa ve tekrar pickup eylemi secilirse
                return -10, 0, False
            elif self.reward_position != (x, y):  # item bulundugumuz konumda degil ve alma eylemi secilirse
                return -10, 0, False
            else:
                self.reward_taken = True  # itemin bizde oldugunu belirtmek icin
                return 20, 2, False
        elif action == 6: # drop off reward
            if not self.reward_taken:  # item bizde degilse ve drop off eylemi secilirse
                return -10, 0, False
            elif self.castle_position != (x, y):  # item bizdeyse ve castle positionda degilse
                self.reward_position = (x, y)  # itemi bulundugumuz konuma birakiriz
                self.reward_taken = False  # itemin bizde olmadigini belirtmek icin
                return -10, 3, False
            else:
                return 20, 4, True  # True ifadesi ile olayin tamamlandigi belirtilir