import matplotlib.pyplot as plt

algos = [
    'AES',
    'Blowfish',
    'tripleDES',
    'RSA',
]

sizes = [
    'very-short',
    'short',
    'medium',
    'long',
    'very-long'
]

data = {}

for algo in algos:
    data[algo] = {}
    for size in sizes:
        with open('./data/{}_{}.txt'.format(algo, size)) as f:
            data[algo][size] = [float(line.rstrip()) for line in f]


def plot_aes_long():
    with open('./data/AES_long.txt') as f:
        data = [float(line.rstrip()) for line in f]
        
    x = [i for i in range(0, 1000)]
    # plt.plot(data)
    plt.scatter(x=x, y=data)
    plt.ylabel('execution time')
    plt.xlabel('Attempt #')
    # plt.show()

    import numpy as np
    from scipy.signal import savgol_filter
    yhat = savgol_filter(data, 51, 3)

    # plt.plot(x,y)
    plt.plot(x, yhat, color='red')

    # 1024 characters (long)
    plt.legend(['AES (Savitzky-Golay)', 'AES'])
    plt.show()


def plot_symmetric():
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    x = [1,2,3,4,5]
    x_names = [16,64, 256, 1024, 4096]
    # print(aes)
    plt.plot(x, aes, linestyle='--')
    plt.plot(x, blowfish, linestyle=':')
    plt.plot(x, tripleDES)
    plt.xticks(x, x_names)
    plt.ylabel('Average execution time (ms)')
    plt.xlabel('Initial message length (characters)')
    plt.legend(['AES', 'Blowfish', 'tripleDES'])
    plt.show()



def plot_all():
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    x = [1,2,3,4,5]
    x_names = [16,64, 256, 1024, 4096]
    # print(aes)
    plt.scatter(x, aes)
    # plt.plot(x, aes, linestyle='--')
    # plt.scatter(x, blowfish)
    # plt.plot(x, blowfish, linestyle=':')
    # plt.scatter(x, tripleDES)
    # plt.plot(x, tripleDES)
    plt.scatter(x, rsa)
    # plt.plot(x, rsa, linestyle='-.')
    plt.xticks(x, x_names)
    plt.ylabel('Average execution time (ms)')
    plt.xlabel('Initial message length (characters)')
    # plt.legend(['AES', 'Blowfish', 'tripleDES', 'RSA'])
    plt.legend(['AES', 'RSA'])
    plt.show()



def calculate_table(algo):
    import statistics
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    results = []

    for size in sizes:
        average = round(statistics.mean(data[algo][size]), 3)
        median = round(statistics.median(data[algo][size]), 3)
        stdev = round(statistics.stdev(data[algo][size]), 3)
        results.append([average, median, stdev])

    print(''.ljust(12), 'mean ', 'med  ', 'stdev')
    for index, size in enumerate(sizes):
        print(size.ljust(12),
            str(results[index][0]).ljust(5),
            str(results[index][1]).ljust(5),
            str(results[index][2]).ljust(5)
        )
    return results


# plot_aes_long()
plot_all()
# calculate_table('RSA')