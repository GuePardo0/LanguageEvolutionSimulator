import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import ProgressBar
import MyImgLib as MIL

class Map():
    def __init__(self, map=""):
        self.water_percentage="not calculated"
        self.map=[]
        if map == "":
            pass
        elif map == "generate":
            self.generateRandomMap()
        else:
            if map.__class__ == str or map == []:
                map=map.lower()
                self.generateGivenMap(map)

    # main methods
    def generateRandomMap(self, rows=100, collumns=100, same_neighbor_probability=0.999, randomness_ammount=40, clean_noise=True, random_variance=0.2, water_bias=0.05, chunk_size=8, chunk_type="size", show_progress=False):
        """
        Description:

        Parameters:
            rows: number of rows of the map
            collumns: number of collumns of the map
            same_neighbor_probability: probability the tile is going to be the same as the majority of its neighboring tiles
                (either land or water)
            randomness_ammount: the ammount of times randomness is going to be generated on top of the map
            clean_noise:
            random_variance: the variance of the range of possibilities of water percentages
                example: random_variance=0.2 -> range of possibilities of water percentages=(0.4, 0.6)
            water_bias: the bias added to the range of possibilities of water percentages
                example: random_variance=0.4, water_bias=0.1 -> range of possibilities of water percentages=(0.4, 0.8)
            chunk_size: the size of the chunks used to generate the bigger portions of the map
            chunk_type: 'size' or 'ratio'
                size: no changes are made to chunk_size
                ratio: chunk_size is the value of the bigger axis over the value given in the chunk_size parameter
            show_progress: Shows a progress bar
        """

        if chunk_type == "ratio":
            bigger_axis=rows
            if collumns > rows:
                bigger_axis=collumns
            chunk_size=int(bigger_axis/chunk_size)
        self.map=self.fillMap(int(rows/chunk_size), int(collumns/chunk_size), 0) # generate a smaller map of water
        self.water_percentage=(random.random()*random_variance)+0.5-(random_variance/2)+water_bias
        self.generateRandomness(self.water_percentage) # generate random land tiles
        self.expandMap(chunk_size) # expand map
        i=0
        if show_progress:
            progress_bar=ProgressBar.ProgressBar(randomness_ammount)
            progress_bar.start()
        while i < randomness_ammount: # generate randomness
            self.generateRandomness(same_neighbor_probability)
            i+=1
            if show_progress:
                progress_bar.updateValue(i)
        if show_progress:
            progress_bar.join()
        if clean_noise:
            self.cleanNoise()

    def generateGivenMap(self, map_name, water_color="#0000FF", water_tolerance=0.55, mark_territories=False, ignore_border=True, border_color="#000000"):
        file_path="images/"+map_name+".png"
        image=MIL.Image(file_path)
        self.map=self.fillMap(len(image.color_data), len(image.color_data[0]), 1)
        for row in range(len(image.color_data)):
            for collumn in range(len(image.color_data[0])):
                pixel=image.color_data[row][collumn]
                is_water=False
                if water_color == "#0000FF":
                    if MIL.areColorsSimilar(pixel, "#0000FF", water_tolerance):
                        is_water=True
                else:
                    if MIL.areColorsSimilar(pixel, water_color, water_tolerance):
                        is_water=True
                if is_water:
                    self.map[row][collumn]=0
        if mark_territories:
            current_number=2
            if ignore_border == True:
                border=image.magicWand(color=border_color, bound=False)
                for border_item in border:
                    self.map[border_item[0]][border_item[1]]=2
                current_number+=1
            print("border done")
            for row in range(len(self.map)):
                for collumn in range(len(self.map[0])):
                    if self.map[row][collumn] == 1:
                        if image.color_data[row][collumn] == [0, 0, 255]:
                            print("eita")
                        center_row=row
                        center_collumn=collumn
                        for i in range(3):
                            selection=image.magicWand(center_row, center_collumn)
                            center_row, center_collumn=MIL.getSelectionCenter(selection)
                        for selection_item in selection:
                            self.map[selection_item[0]][selection_item[1]]=current_number
                        print(f"territory {current_number-2} done")
                        current_number+=1
                    if current_number == 30:
                        break
                if current_number == 30:
                    break

    def setMap(self, map_name):
        if map_name.__class__ == str:
            try:
                with open(f"maps/{map_name}.txt", "r") as file:
                    content=file.readlines()
                self.map=[]
                for row in range(len(content)):
                    self.map.append([])
                    for collumn in range(len(content[0])-1):
                        self.map[row].append(int(content[row][collumn]))
            except:
                raise TypeError("Exists no map with this name")
        else:
            try:
                with open(f"maps/map_{map}.txt", "r") as file:
                    content=file.readlines()
                self.map=[]
                for row in range(len(content)):
                    self.map.append([])
                    for collumn in range(len(content[0])-1):
                        self.map[row].append(int(content[row][collumn]))
            except:
                if map <= 0:
                    raise TypeError("Expected 'map' > 0 or str")
                else:
                    raise TypeError("Exists no map with this index")

    def showMap(self, color_pallet="default", shuffle_colors="default"):
        """
        Description:
            Opens a window showing the map.
            Returns nothing
        
        Parameters:
            color_pallet:
                Type: list of strings of colors
                Description: color pallet to be used on the map. The first color is the color of water and the second one is the default color of land
        """
        try:
            colors=[]
            if shuffle_colors == "default": # shuffle_colors default value is True for the default color pallet and False for any other color pallet
                if color_pallet == "default":
                    shuffle_colors=True
                else:
                    shuffle_colors=False
            if color_pallet == "default":
                colors=["blue", "#555555"]
                color_pallet=MIL.ColorPallet(['#A9A9A9', '#FFFAFA', '#800000', '#FF0000', '#A0522D', '#F4A460', '#FF8C00', '#D2B48C', '#808000', '#FFFF00', '#556B2F', '#7CFC00', '#8FBC8F', '#00FA9A', '#40E0D0', '#008080', '#00FFFF', '#87CEEB', '#708090', '#8A2BE2', '#4B0082', '#8B008B', '#FF00FF', '#DB7093'])
            if shuffle_colors == True:
                random.shuffle(color_pallet.values)
                color_pallet.updateNames()
            colors.extend(color_pallet.values)
            cmap = mcolors.ListedColormap(colors)
            plt.imshow(self.map, cmap=cmap, vmin=0, vmax=(len(colors)-1))
            plt.show()
        except:
            raise ValueError("Map is empty.")

    def saveMap(self, map_index=0, map_name=""):
        if map_name != "":
            self.__writeMap(map_name)
        else:
            if map_index != 0:
                if map_index < 0:
                    raise ValueError("Expected 'map_index' >= 0.")
                self.__writeMap(f"map_{map_index}")
            else:
                index=1
                while True:
                    try:
                        self.__writeMap(f"map_{index}", "x")
                        break
                    except:
                        index+=1

    def fillMap(self, rows, collumns, value):
        map=[]
        for row in range(rows):
            map.append([])
            for collumn in range(collumns):
                map[row].append(value)
        return map

    def expandMap(self, times):
        newmap=self.fillMap(len(self.map)*times, len(self.map[0])*times, 0)
        for row in range(len(newmap)):
            for collumn in range(len(newmap[0])):
                newmap[row][collumn]=self.map[int(row/times)][int(collumn/times)]
        self.map=newmap

    def expandAndCorrectMap(self, times, randomness_ammount=40, clean_noise=True):
        self.expandMap(times)
        for i in range(randomness_ammount):
            self.generateRandomness()
        if clean_noise:
            self.cleanNoise()

    def generateRandomness(self, same_neighbor_probability=0.999):
        for row in range(len(self.map)):
            for collumn in range(len(self.map[0])):
                neighbors=MIL.getNeighbors(self.map, row, collumn)
                neighbor_average=0
                for neighbor in neighbors:
                    neighbor_average+=neighbor
                neighbor_average/=len(neighbors)
                self.map[row][collumn]=self.__calculateTile((neighbor_average*2)-1, same_neighbor_probability)

    def cleanNoise(self):
        for row in range(len(self.map)):
            for collumn in range(len(self.map[0])):
                neighbors=MIL.getNeighbors(self.map, row, collumn)
                if len(neighbors) == 4:
                    neighborsAreTheSame=True
                    neighborsType=neighbors[0]
                    for neighbor in neighbors:
                        if neighbor != neighborsType:
                            neighborsAreTheSame=False
                            break
                    if neighborsAreTheSame:
                        self.map[row][collumn]=neighborsType

    # other methods
    def __calculateTile(self, neighbor_average, same_neighbor_probability):
        random_value=random.random()
        if neighbor_average > 0:
            if random_value < same_neighbor_probability:
                return 1
            else:
                return 0
        elif neighbor_average == 0:
            if random_value < 0.5:
                return 1
            else:
                return 0
        else:
            if random_value > same_neighbor_probability:
                return 1
            else:
                return 0

    """def __sigmoid(self, x):
        return 1/(1+2.7182818284**(-x))
    def __normalizedSigmoid(self, x):
        compression_coeficient=6
        return (((self.__sigmoid(x*compression_coeficient)-(self.__sigmoid(-compression_coeficient)))/(self.__sigmoid(compression_coeficient)-(self.__sigmoid(-compression_coeficient))))*2)-1"""

    def __performEducatedShuffle(self, colors: list):
        for i in range(len(colors)):
            if colors[i].__class__ == str:
                colors[i]=MIL.hexadecimalToRgb(colors[i])
        while i < len(colors):
            if colors.count(colors[i]) > 1:
                colors.pop(i)
                i-=1
            i+=1
        random.shuffle(colors)
        shuffled_colors=[]
        total=len(colors)
        for i1 in range(total):
            if i1 == 0:
                appended_index=0
            else:
                color_to_compare=shuffled_colors[i1-1]
                threshold=200
                while True:
                    i2=0
                    while i2 < len(colors):
                        euclidean_distance=MIL.euclideanDistance(color_to_compare, colors[i2])
                        if euclidean_distance > threshold:
                            appended_index=i2
                            break
                        i2+=1
                    if i2 != len(colors):
                        break
                    threshold-=20
            shuffled_colors.append(colors[appended_index])
            colors.pop(appended_index)
        for i in range(len(shuffled_colors)):
            shuffled_colors[i]=MIL.rgbToHexadecimal(shuffled_colors[i])
        return shuffled_colors

    def __writeMap(self, map_name, mode="w"):
        with open(f"maps/{map_name}.txt", mode) as file:
            for row in range(len(self.map)):
                for collumn in range(len(self.map[0])):
                    file.write(str(self.map[row][collumn]))
                file.write("\n")