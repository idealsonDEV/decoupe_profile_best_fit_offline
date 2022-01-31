import warnings
import locale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.cbook
matplotlib.use('Agg')

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def setDataModel(dataraw):
    data = {}
    weights = [w for w,_ in dataraw]
    label = [l for _,l in dataraw]
    data['weights'] = weights
    data['label'] = label
    data['items'] = list(range(len(weights)))
    data['bins'] = list(range(300))
    data['bin_capacity'] = 5800
    return data

def firstFit(weight, n, c):
    res = 0
    bin_rem = [0] * n
    pack = {}
    for i in range(n):

        j = 0
        while (j < res):
            if (bin_rem[j] >= weight[i][0]):
                bin_rem[j] = bin_rem[j] - weight[i][0] - 10
                pack[j].append(weight[i])
                break
            j += 1

        if (j == res):
            bin_rem[res] = c - weight[i][0] - 10
            if res not in pack.keys():
                pack[res] = []
            pack[res].append(weight[i])
            res = res + 1
    return res, pack

def bestFit2t(weight, n, c):
    res = 0

    bin_rem = [0] * n

    pack = {}

    for i in range(n):

        j = 0

        min = c + 1
        bi = 0

        for j in range(res):
            if (bin_rem[j] >= weight[i][0] and bin_rem[j] - weight[i][0] - 10 < min):
                bi = j
                min = bin_rem[j] - weight[i][0] - 10

        if (min == c + 1):
            bin_rem[res] = c - weight[i][0] - 10
            if res not in pack.keys():
                pack[res] = []
            pack[res].append(weight[i])
            res += 1
        else:
            bin_rem[bi] -= weight[i][0] + 10
            pack[bi].append(weight[i])
    return res, pack


def bestFit(weight, n, c):
    res = 0
    bin_rem = [0] * n
    pack = {}
    for i in range(n):
        j = 0
        minm = c + 1
        bi = 0
        for j in range(res):
            if (bin_rem[j] >= weight[i] and bin_rem[j] - weight[i] - 10 < minm):
                bi = j
                minm = bin_rem[j] - weight[i] - 10
        if (minm == c + 1):
            bin_rem[res] = c - weight[i] - 10
            if res not in pack.keys():
                pack[res] = []
            pack[res].append(weight[i])
            res += 1
        else:
            bin_rem[bi] -= weight[i] + 10
            pack[bi].append(weight[i])
    return res, pack

def solveLinearCut2(data):
    res = {}
    sorteddata = sorted(data['weights'], reverse=True)
    _, bf = bestFit(sorteddata, len(data['weights']), data['bin_capacity'])
    for idbf in bf:
        bf[idbf] = min(bf[idbf]), sorted(bf[idbf])
    ccc =  0
    for xref in sorted(bf.items(), key=lambda item: item[1][0]):
        res[ccc] = {}
        res[ccc]['morceau'] = [yt for yt in xref[1][1]]
        res[ccc]['used'] = sum([yt for yt in xref[1][1]])
        ccc += 1
    return res

def afficheSol(res):
    if len(res) > 0:
        with PdfPages('Impression.pdf') as pdf:
            # A4 canvas
            fig_width_cm = 21
            fig_height_cm = 9.5
            inches_per_cm = 1 / 2.54
            fig_width = fig_width_cm * inches_per_cm
            fig_height = fig_height_cm * inches_per_cm
            fig_size = [fig_width, fig_height]

            for i in res:
                fig = plt.figure()
                fig.set_size_inches(fig_size)
                fig.patch.set_facecolor('#FFFFFF')
                ax = fig.add_subplot()
                ax.invert_yaxis()
                ax.xaxis.set_visible(False)
                ax.yaxis.set_visible(False)
                ax.set_xlim(0, 5800)
                ax.set_ylim(0, 3)
                ax.set_facecolor('#FFFFFF')
                t = 1
                start = 0
                ax.barh(str(t), 5800, left=start, height=0.5, Fill=None, hatch='///')
                for j in res[i]['morceau']:
                    ax.barh(str(t), j, left=start, height=0.5, label=str(j))
                    ax.text(start + (j / 2), t - 1, j, ha='center', va='bottom',
                            color='#000000')
                    start += j
                    t = 1
                plt.legend(loc='upper left',
                           ncol=1, mode="expand", borderaxespad=0.)
                pdf.savefig(dpi=300, orientation='portarit')
                plt.close()

    print(' | Nombre de barres utilise:', len(res))

if __name__ == '__main__':
    test = [(3000,'01'),(2500,'02'),(1200,'03'),(1500,'04'),(2100,'05'),(3200,'06'),(1000,'07'),(900,'08'),(1400,'09')]
    data = setDataModel(test)
    res = solveLinearCut2(data)
    afficheSol(res)
