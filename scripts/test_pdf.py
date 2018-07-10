from PyPDF2 import PdfFileReader
import os


if __name__ == "__main__":
    DATA = "/mnt/d/Data/Projects/IR/Data"
    FPATH_PDF = os.path.join(DATA, "scrapy_data_pdf")
    files = os.listdir(FPATH_PDF)
    invalid = []
    count = 0
    for f in files:
        count += 1
        if count % 500 == 0:
            print(count)
        fp = os.path.join(FPATH_PDF, f)
        try:
            doc = PdfFileReader(open(fp, "rb"))
        except:
            print(fp)
            invalid.append(fp)

    print("=========invalid===========")
    print(invalid)
    # invalid = ['D16-1208.pdf', 'E97-1003.pdf', 'E97-1018.pdf', 'E97-1039.pdf', 'E97-1040.pdf', 'I17-4004.pdf', 'L00-1119.pdf', 'L00-1241.pdf', 'L00-1278.pdf', 'L02-1036.pdf', 'L02-1078.pdf', 'L02-1126.pdf', 'L02-1147.pdf', 'L02-1170.pdf', 'L02-1192.pdf', 'L02-1239.pdf', 'L02-1336.pdf', 'L04-1068.pdf', 'L04-1138.pdf', 'L04-1153.pdf', 'L04-1212.pdf', 'L04-1245.pdf', 'L04-1268.pdf', 'L04-1272.pdf', 'L04-1420.pdf', 'L04-1423.pdf', 'L04-1492.pdf', 'L06-1010.pdf', 'L06-1022.pdf', 'L06-1047.pdf', 'L06-1085.pdf', 'L06-1123.pdf', 'L06-1135.pdf', 'L06-1290.pdf', 'L06-1325.pdf', 'L06-1398.pdf', 'L06-1473.pdf', 'L06-1486.pdf', 'L08-1073.pdf', 'L08-1102.pdf', 'L08-1134.pdf', 'L08-1167.pdf', 'L08-1188.pdf', 'L08-1228.pdf', 'L08-1485.pdf', 'L08-1613.pdf', 'L10-1014.pdf', 'L10-1027.pdf', 'L10-1079.pdf', 'L10-1087.pdf', 'L10-1115.pdf', 'L10-1154.pdf', 'L10-1236.pdf', 'L10-1331.pdf', 'L10-1390.pdf', 'L10-1488.pdf', 'L12-1022.pdf', 'L12-1042.pdf', 'L12-1051.pdf', 'L12-1089.pdf', 'L12-1109.pdf', 'L12-1161.pdf', 'L12-1268.pdf', 'L12-1274.pdf', 'L12-1284.pdf', 'L12-1335.pdf', 'L12-1357.pdf', 'L12-1437.pdf', 'L12-1470.pdf', 'L12-1498.pdf', 'L12-1669.pdf', 'L14-1021.pdf', 'L14-1041.pdf', 'L14-1094.pdf', 'L14-1141.pdf', 'L14-1151.pdf', 'L14-1154.pdf', 'L14-1230.pdf', 'L14-1256.pdf', 'L14-1357.pdf', 'L14-1361.pdf', 'L14-1405.pdf', 'L14-1420.pdf', 'L14-1431.pdf', 'L14-1533.pdf', 'L14-1563.pdf', 'L14-1638.pdf', 'L14-1729.pdf', 'O03-1000.pdf', 'O06-3000.pdf', 'O94-1010.pdf', 'P01-1053.pdf', 'P15-2137.pdf', 'Q18-1006.pdf', 'W01-0518.pdf', 'W03-2108.pdf', 'W04-2504.pdf', 'W10-0707.pdf', 'W12-1503.pdf', 'W12-1506.pdf', 'W14-6201.pdf', 'W17-7804.pdf', 'W17-8003.pdf']
    # 
    # for f in invalid:
    #     fp = os.path.join(FPATH_PDF, f)
    #     print(fp)
    #     os.remove(fp)
