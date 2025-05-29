def doc_so(n):
    dv = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    hc = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
    tr, ch, dvn = n // 100, (n % 100) // 10, n % 10
    s = dv[tr] + " trăm"
    if ch == 0 and dvn != 0: s += " linh " + dv[dvn]
    elif ch != 0:
        s += " " + hc[ch]
        if dvn == 1: s += " mốt"
        elif dvn == 5: s += " lăm"
        elif dvn != 0: s += " " + dv[dvn]
    return s.strip()

n = int(input("Nhap: "))
print(doc_so(n) if 100 <= n <= 999 else "Khong hop le")