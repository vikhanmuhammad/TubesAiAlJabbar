import math
import random

# Fungsi generate chromosome
def generateChromosome(chromosomeSize):
    chromosome = []
    for i in range(chromosomeSize):
        chromosome.append(random.randint(0, 1))
    return chromosome

# Fungsi decode chromosome
def decodeChromosome(chromosome):
    x1 = chromosome[0:5]
    x2 = chromosome[5:10]
    x1 = int(''.join([str(i) for i in x1]), 2)
    x2 = int(''.join([str(i) for i in x2]), 2)
    x1 = -10 + (10-(-10)) * (x1/(2**5-1))
    x2 = -10 + (10-(-10)) * (x2/(2**5-1))

    return round(x1, 3), round(x2, 3)

# Fungsi penghitungan fitness
def fitness(x1, x2):
    heuristics = -1 * (math.sin(x1) * math.cos(x2) + (4/5) * math.exp(1 - math.sqrt(x1**2 + x2**2)))
    return (1 / heuristics)

# Fungsi pemilihan orangtua
def selectParents(population, numParents):
    parents = []
    for i in range(numParents):
        x = random.randint(0, len(population) - 1)
        parents.append(population[x])
    return parents

# Fungsi crossover (pindah silang) dengan probabilitas 0,8
def crossover(parent1, parent2):
    offspring1 = []
    offspring2 = []
    pc = 0.8
    for i in range(10):
        if random.random() < pc:
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        else:
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])
    return offspring1, offspring2

# Fungsi mutasi
def mutasi(child1, child2):
    pm = 0.3
    for i in range(len(child1)):
        if random.random() < pm:
            child1[i] = str(1 - int(child1[i]))
    for i in range(len(child2)):
        if random.random() < pm:
            child2[i] = str(1 - int(child2[i]))
    return child1, child2

# Fungsi pindah generasi (elitism agar gen terbaik tidak hilang) probabilitas 0,8
def elitism(population, offspring):
    allChromosomes = population + offspring
    allFitness = [fitness(*decodeChromosome(chromosome)) for chromosome in allChromosomes]
    pc = 0.8

    if random.random() < pc:
        idx = allFitness.index(max(allFitness))
        bestChromosome = allChromosomes[idx]
    else:
        # Jika probabilitas elitisme tidak terpenuhi, maka hanya mengambil salah satu individu secara acak
        bestChromosome = random.choice(allChromosomes)

    return bestChromosome

def main():
    fitnessPopulation = {}
    previousBestChromosome = None  # Untuk menyimpan individu terbaik dari generasi sebelumnya

    print('-'*76)
    print('{} {:^10} {} {:^10} {} {:^10} {} {:^10} {} {:^20} {}'.format('|', 'Population', '|', 'Chromosome', '|', 'x1', '|', 'x2', '|', 'Fitness', '|'))
    print('-'*76)
    for i in range(10):
        chromosome = "".join(list(map(str, [i for i in generateChromosome(10)])))
        x1, x2 = decodeChromosome(chromosome)
        fitnessPopulation[chromosome] = fitness(x1, x2)
        # Menambahkan data ke tabel
        print('{} {:^10} {} {:^10} {} {:^10} {} {:^10} {} {:^20} {}'.format('|', i+1, '|', chromosome, '|', x1, '|', x2, '|', fitnessPopulation[chromosome], '|'))

    i = 0
    print('-'*76)
    print('{} {:^10} {} {:^10} {} {:^10} {} {:^10} {} {:^20} {}'.format('|', 'Generation', '|', 'Chromosome', '|', 'x1', '|', 'x2', '|', 'Fitness', '|'))
    print('-'*76)

    stagnationLimit = 100  # Ambang batas stagnasi (misalnya, 10 generasi tanpa peningkatan)
    stagnationCount = 0  # Menghitung berapa banyak generasi tanpa peningkatan
    bestFitness = -float('inf')  # Menyimpan fitness terbaik yang ditemukan

    while True:
        highestPopulation = sorted(fitnessPopulation, key=fitnessPopulation.get, reverse=True)
        # Menggunakan fungsi selectParents untuk memilih orangtua
        parents = selectParents(highestPopulation, 2)  # Memilih 2 orangtua
        parent1 = parents[0]
        parent2 = parents[1]

        offspring1, offspring2, = crossover(parent1, parent2)
        child1, child2 = mutasi(offspring1, offspring2)

        child1 = "".join(list(map(str, [i for i in child1])))
        child2 = "".join(list(map(str, [i for i in child2])))
        x11, x21 = decodeChromosome(child1)
        x12, x22 = decodeChromosome(child2)

        if (fitness(x11, x21) > min(fitnessPopulation.values()) and (fitness(x12, x22) > min(fitnessPopulation.values()))):
            fitnessPopulation.popitem()
            fitnessPopulation[child1] = fitness(x11, x21)
            fitnessPopulation[child2] = fitness(x12, x22)

        fitnessPopulation = dict(sorted(fitnessPopulation.items(), key=lambda item: item[1], reverse=True))

        # Menggunakan fungsi elitism untuk memutuskan apakah mempertahankan individu terbaik dari generasi sebelumnya
        if previousBestChromosome is not None:
            bestChromosome = elitism([previousBestChromosome], [highestPopulation[0]])
            if bestChromosome == previousBestChromosome:
                fitnessPopulation.popitem()
                fitnessPopulation[previousBestChromosome] = fitness(*decodeChromosome(previousBestChromosome))

        previousBestChromosome = highestPopulation[0]

        # Menambahkan data ke tabel
        print('{} {:^10} {} {:^10} {} {:^10} {} {:^10} {} {:^20} {}'.format('|', i+1, '|', highestPopulation[0], '|', decodeChromosome(parent1)[0], '|', decodeChromosome(parent2)[1], '|', fitnessPopulation[highestPopulation[0]], '|'))
        # Periksa apakah fitness terbaik dalam generasi saat ini lebih baik
        if fitnessPopulation[highestPopulation[0]] > bestFitness:
            bestFitness = fitnessPopulation[highestPopulation[0]]
            stagnationCount = 0  # Reset stagnation count
        else:
            stagnationCount += 1  # Tidak ada peningkatan, tambahkan stagnationCount

        # Periksa apakah telah terjadi stagnasi
        if stagnationCount >= stagnationLimit:
            print("Evolusi tidak menghasilkan kemajuan. Menghentikan evolusi.")
            break
        i += 1

    print("Kromosom terbaik : ", highestPopulation[0])
    print("x1 : ", decodeChromosome(parent1)[0])
    print("x2 : ", decodeChromosome(parent2)[1])
    print("Fitness : ", fitnessPopulation[highestPopulation[0]])

if __name__ == "__main__":
    main()
