class AddTrainingCenter:

    def __init__(self):
        self.centers = self.create_center()

    def create_center(self):
        return {1:0}

    def add_new_center(self):
        newcenter_id = len(self.centers.keys()) + 1
        self.centers.update({newcenter_id : 0})


test = AddTrainingCenter()

test.create_center()
print(test.create_center())
