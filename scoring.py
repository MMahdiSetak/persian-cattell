import matplotlib.pyplot as plt

raw_score_table = {
    "A": [[11, 64, 125, 149, 171], [], [9, 40, 56, 59, 174]],
    "B": [[122, 133, 177, 175], [25, 73, 106, 173, 182], [48, 104, 127, 147]],
    "C": [[13, 28, 51, 80, 90, 148], [], [39, 88, 105, 118, 121, 129, 176]],
    "E": [[29, 72, 78, 98, 99, 131, 134], [], [3, 22, 102, 128, 153, 183]],
    "F": [[7, 35, 52, 60, 67, 76, 85], [], [5, 20, 36, 37, 68, 86]],
    "G": [[12, 61, 115, 143, 145], [], [63, 89, 116, 161, 162]],
    "H": [[46, 109, 123, 132, 141, 179, 181], [], [47, 75, 100, 103, 152, 154]],
    "I": [[107, 114, 120, 137, 185], [], [124, 156, 159, 165, 168]],
    "L": [[30, 79, 108, 150, 158], [], [26, 135, 146, 172, 184]],
    "M": [[6, 45, 49, 57, 93, 160], [], [17, 23, 83, 97, 110, 113, 157]],
    "N": [[24, 66, 92, 101, 180], [], [19, 50, 74, 151, 178]],
    "O": [[15, 62, 70, 136, 163, 186], [], [41, 43, 65, 95, 111, 139, 140]],
    "Q1": [[10, 14, 27, 84, 87], [], [32, 38, 54, 77, 82]],
    "Q2": [[18, 44, 91, 112, 167], [], [117, 138, 142, 164, 169]],
    "Q3": [[4, 16, 42, 69, 81], [], [31, 33, 53, 55, 94]],
    "Q4": [[8, 21, 34, 58, 96, 126, 144], [], [71, 119, 130, 155, 166, 170]],
}

score_mapping_table = {
    "A": [(0, 1), (2, 3), (4, 4), (5, 6), (7, 7), (8, 8), (9, 10), (11, 11), (12, 13), (14, 20)],
    "B": [(0, 3), (4, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (-1, -1), (11, 11), (12, 13)],
    "C": [(0, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 17), (18, 19), (20, 20), (21, 26)],
    "E": [(0, 4), (5, 6), (7, 7), (8, 9), (10, 10), (11, 12), (13, 14), (15, 16), (17, 18), (19, 26)],
    "F": [(0, 5), (6, 6), (7, 8), (9, 10), (11, 12), (13, 13), (14, 15), (16, 17), (18, 20), (21, 26)],
    "G": [(0, 6), (7, 9), (10, 10), (11, 12), (13, 14), (15, 15), (16, 16), (17, 18), (-1, -1), (19, 20)],
    "H": [(0, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 19), (20, 21), (22, 26)],
    "I": [(0, 3), (4, 4), (5, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 14), (15, 16), (17, 20)],
    "L": [(0, 4), (5, 6), (7, 7), (8, 9), (10, 11), (12, 13), (14, 14), (15, 16), (17, 18), (19, 20)],
    "M": [(0, 4), (5, 6), (7, 8), (9, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19), (20, 26)],
    "N": [(0, 5), (6, 6), (7, 7), (8, 9), (10, 10), (11, 11), (12, 13), (14, 14), (15, 16), (17, 20)],
    "O": [(0, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 17), (18, 20), (21, 26)],
    "Q1": [(0, 5), (6, 6), (7, 7), (8, 9), (10, 10), (11, 12), (13, 13), (14, 15), (16, 16), (17, 20)],
    "Q2": [(0, 3), (4, 5), (6, 6), (7, 8), (9, 9), (10, 11), (12, 12), (13, 14), (15, 16), (17, 20)],
    "Q3": [(0, 5), (6, 8), (9, 10), (11, 12), (13, 14), (15, 15), (16, 16), (17, 18), (19, 19), (20, 20)],
    "Q4": [(0, 2), (3, 4), (5, 7), (8, 9), (10, 11), (12, 14), (15, 16), (17, 18), (19, 21), (22, 26)],
}


def second_order_score(fs, sex):
    score = {
        "Extroversion": (3 * fs["A"] + 4 * fs["F"] + 4 * fs["H"] - 4 * fs["Q2"] + 17) / 10,
        "Anxiety": (-3 * fs["C"] - fs["H"] + fs["L"] + 3 * fs["O"] - fs["Q3"] + 3 * fs["Q4"] + 44) / 10,
        "Flexibility":
            (-1 * fs["A"] + 4 * fs["E"] + 2 * fs["F"] - 6 * fs["I"] + 2 * fs["L"] - 4 * fs[
                "M"] + 72) / 10 if sex == 2 else
            (-2 * fs["A"] + 2 * fs["F"] - 6 * fs["I"] - 4 * fs["M"] - 2 * fs["Q1"] + 121) / 10,
        "Independence":
            (5 * fs["E"] - fs["G"] + 3 * fs["H"] + 2 * fs["M"] + 4 * fs["Q1"]
             + fs["Q2"] - 22) / 10 if sex == 2 else
            (5 * fs["E"] - fs["G"] + 3 * fs["H"] + 2 * fs["L"] - fs["N"] - 2 * fs["O"] + 2 * fs["Q1"]
             + fs["Q2"] + 6) / 10,
        "Self Control": (7 * fs["G"] + 5 * fs["Q3"] - 11) / 10,
        "Compatibility": (fs["B"] + 3 * fs["C"] + 2 * fs["E"] + 4 * fs["F"] + fs["G"] - fs["H"] - 2 * fs["I"]
                          - 3 * fs["O"] - fs["Q1"] - 4 * fs["Q4"] + 44) / 10,
        "Leadership": (fs["B"] + fs["C"] + fs["E"] + 2 * fs["F"] + 2 * fs["G"] + 2 * fs["H"] - fs["I"]
                       - fs["M"] + fs["N"] - 2 * fs["O"] + 2 * fs["Q3"] - fs["Q4"] + 17) / 10,
        "Creativity": (-3 * fs["A"] + 3 * fs["B"] + 2 * fs["E"] - 3 * fs["F"] + 2 * fs["H"] + 3 * fs["I"]
                       + 2 * fs["M"] - 2 * fs["N"] + 2 * fs["Q1"] + 3 * fs["Q2"] + 6) / 10,
    }
    return score


def plot_score(score, title, raw_score=None):
    # Mid-point
    mid_point = 5.5

    # Function to determine the color based on the number
    def determine_color(number):
        if 4 <= number <= 7:
            return 'green'
        else:
            return 'red'

    # Create figure
    plt.figure(figsize=(10, 6))

    # Plot each bar
    for i, (key, value) in enumerate(reversed(list(score.items()))):
        color = determine_color(value)
        # The bar starts from mid-point and extends to the value
        plt.barh(key, value - mid_point, left=mid_point, color=color)
        if raw_score is not None:
            plt.text(10.1, i, f"{raw_score[key]}", va='center')

    plt.axvline(mid_point, color='black', linewidth=0.8, linestyle='--')  # Mid-point line
    plt.xlabel('Score')
    plt.xlim(1, 10)
    plt.title(title)
    plt.grid(axis='x')
    plt.savefig(f'./report/{title}.png')
    plt.show()
