import timeit


def menghitung(n):

    # Fungsi atau kode yang ingin diukur waktu komputasinya
    # Contoh:
    for i in range(n):
        pass


menghitung(1000000)

code_to_test = """

def menghitung(n):

    # Fungsi atau kode yang ingin diukur waktu komputasinya
    # Contoh:
    for i in range(n):
        pass
        
menghitung(1000000)
"""

execution_time = timeit.timeit(code_to_test, number=1)

print("Waktu eksekusi:", execution_time, "detik")
