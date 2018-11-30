import Levenshtein


def main():
    #originalFilename = "data/AStarTimes2.csv"
    #newFilename = "data/AStarMetrics2.csv"
    originalFilename = "../../../data/AStarTimes5.txt"
    newFilename = "../../../data/AStarMetrics5.csv" 
    with open(originalFilename, "r") as file:
        newFile = open(newFilename, "w+")
        lines = file.readlines()
        for line in lines:
            words = line.split(',')
            original = words[3]
            newWord = words[4]
            newNoStars = newWord.replace('*', '')
            numberOfStars = newWord.count('*')
            withStarsDist = Levenshtein.distance(original, newWord)
            withoutStarsDist = Levenshtein.distance(original, newNoStars)
            newScore = withStarsDist - ((withoutStarsDist-(withStarsDist - numberOfStars))/2.0)
            newLine = line.replace("\n", ",") + str(newScore) + "\n"
            newFile.write(newLine)

if __name__ == '__main__':
  main()
