import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import os

# Change if your monitor dpi varies
MY_DPI = 96

def get_int_in_range(prompt, min, max):
    while True:
        print(prompt)
        try:
            x = int(input())
            assert(min <= x <= max)

            return x
        
        except:
            print("Invalid Input")




def main():
    print()
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f[f.rindex(".")+1:] == "txt"]

    if (len(files) == 0):
        print(f"No valid txt file in directory ({os.getcwd()})\n\nExiting the program...")
        return
    elif (len(files) == 1):
        file_index = 0
    else:
        print("Several txt files were found in the current working directory:")
        for a, b in enumerate(files):
            print(f"\t{a+1}. {b}")
        print()

        file_index = get_int_in_range("Specify the file you want to be used as a plotting guide by inputting the corresponding number:", 1, len(files)) - 1

    file_name = files[file_index][:files[file_index].rindex(".")]
    file_path = os.path.join(os.getcwd(), files[file_index])
        
    print("Coordinates are being taken from: " + file_path)
    print("Process in progress, please wait...")


    with open(file_path, 'r') as file:
        lines = file.readlines()

    try:
        coordinates = [tuple(map(int, line.split())) for line in lines]
    except:
        print("Invalid file contents (file should contain 2 ints on each line seperated by spaces")
        return

    hull = ConvexHull(coordinates)
    hull_coordinates = [coordinates[x] for x in hull.vertices] + [coordinates[hull.vertices[0]]]

    x_coords, y_coords = zip(*coordinates)
    hull_x_coords, hull_y_coords = zip(*hull_coordinates)

    if max(x_coords) < max(y_coords):
        y_coords, x_coords = x_coords, y_coords
        hull_x_coords, hull_y_coords = hull_y_coords, hull_x_coords

    canvas_width, canvas_height = 960, 540
    plt.figure(figsize=(canvas_width / MY_DPI, canvas_height / MY_DPI))
    plt.axis([0, canvas_width, 0, canvas_height])   


    plt.scatter(x_coords, y_coords, c = 'black', s=1, label='Вихідні точки') 
    plt.plot(hull_x_coords, hull_y_coords, 'b-', linewidth = 3, label = "Опукла оболонка")


    plt.axis('off')  
    plt.legend(loc='upper right', fontsize='small')


    output_path = file_path = os.path.join(os.getcwd(), file_name + "_with_hull.png")
    plt.savefig(output_path, dpi=MY_DPI, pad_inches=0)

    print("\nProcess finished")
    print(f" PNG file saved at: {output_path}")


if (__name__ == "__main__"):
    main()