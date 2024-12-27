import threading
import time

class ProgressBar():
    def __init__(self, total=0, show_percentage=True, show_bar=True):
        self.total=total
        self.value=0
        self.lock=threading.Lock()
        self.thread=threading.Thread(target=self.progressBar)
        self.show_percentage=show_percentage
        self.show_bar=show_bar
    def progressBar(self):
        if self.total <= 0:
            raise TypeError("Expected 'self.total' > 0.")
        count=0
        last_percentage=-1
        while True:
            percentage=100*self.value/self.total
            if percentage == last_percentage:
                break
            if count == 4 and percentage != 100:
                print("\n"*20)
                if self.show_percentage:
                    print(((" "*50)+"%.2f" % percentage)+"%")
                if self.show_bar:
                    boxes="█"*int(percentage)
                    spaces="░"*(100-int(percentage))
                    print(f"【{boxes}{spaces}】")
                count=0
            if percentage == 100:
                print("\n"*20)
                if self.show_percentage:
                    print(((" "*50)+"%.2f" % percentage)+"%")
                if self.show_bar:
                    boxes="█"*int(percentage)
                    spaces="░"*(100-int(percentage))
                    print(f"【{boxes}{spaces}】")
                break
            last_percentage=percentage
            count+=1
            time.sleep(0.1)
    def start(self):
        self.thread.start()
    def join(self):
        self.thread.join()
    def updateValue(self, value):
        with self.lock:
            self.value = value