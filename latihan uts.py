import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

permintaan = ctrl.Antecedent(np.arange(0, 5001, 1), 'permintaan')
persediaan = ctrl.Antecedent(np.arange(0, 1001, 1), 'persediaan')
produksi = ctrl.Consequent(np.arange(0, 8001, 1), 'produksi')

# PERMINTAAN
permintaan['turun'] = fuzz.trapmf(permintaan.universe, [0, 0, 1000, 3000])
permintaan['naik'] = fuzz.trapmf(permintaan.universe, [1000, 3000, 5000, 5000])

# PERSEDIAAN
persediaan['sedikit'] = fuzz.trapmf(persediaan.universe, [0, 0, 200, 400])
persediaan['sedang'] = fuzz.trimf(persediaan.universe, [200, 400, 800])
persediaan['banyak'] = fuzz.trapmf(persediaan.universe, [400, 800, 1000, 1000])

# PRODUKSI
produksi['berkurang'] = fuzz.trapmf(produksi.universe, [0, 0, 2000, 7000])
produksi['bertambah'] = fuzz.trapmf(produksi.universe, [2000, 7000, 8000, 8000])

rule1 = ctrl.Rule(permintaan['turun'] & persediaan['banyak'], produksi['berkurang'])
rule2 = ctrl.Rule(permintaan['turun'] & persediaan['sedang'], produksi['berkurang'])
rule3 = ctrl.Rule(permintaan['turun'] & persediaan['sedikit'], produksi['bertambah'])
rule4 = ctrl.Rule(permintaan['naik'] & persediaan['banyak'], produksi['berkurang'])
rule5 = ctrl.Rule(permintaan['naik'] & persediaan['sedang'], produksi['bertambah'])
rule6 = ctrl.Rule(permintaan['naik'] & persediaan['sedikit'], produksi['bertambah'])

produksi_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
produksi_simulasi = ctrl.ControlSystemSimulation(produksi_ctrl)

permintaan_input = 2000
persediaan_input = 500

produksi_simulasi.input['permintaan'] = permintaan_input
produksi_simulasi.input['persediaan'] = persediaan_input

try:
    produksi_simulasi.compute()
    hasil_produksi = produksi_simulasi.output['produksi']

    print(f"Permintaan (Input): {permintaan_input} kemasan")
    print(f"Persediaan (Input): {persediaan_input} kemasan")
    print("-" * 30)
    print(f"Hasil Produksi: {hasil_produksi:.2f} kemasan")
    print(f"Jumlah Produksi: {int(round(hasil_produksi))} kemasan")

    print("\nMenampilkan grafik fuzzifikasi dan defuzzifikasi...")
    
    permintaan.view(sim=produksi_simulasi) # Grafik Permintaan
    persediaan.view(sim=produksi_simulasi) # Grafik Persediaan

    # Grafik Defuzzifikasi Output (Grafik naik turun fuzzy yang digabungkan)
    produksi.view(sim=produksi_simulasi) 
    
    plt.show() 
except Exception as e:
    print(f"\n❌ Error Komputasi Terdeteksi: {e}")