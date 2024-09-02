def lookinfolder():
  path = './input'
  pass

def frecuencia_dominante(trace):
  freq = np.fft.fftfreq(len(trace))
  spectra = np.fft.fft(trace)
  index = np.argmax(np.abs(spectra))
  f_dominante = freq[index]
  return f_dominante

def duracion(trace, dt):
  sr       = 1000 / dt #calculo el sampling rate
  nsamples = trace.size 
  t_total  = nsamples / sr #calculo la duracion
  return t_total, nsamples

def graph_trace(trace, dt):
  t_total, nsamples = duracion(trace, dt)
  t = np.linspace(0, t_total, nsamples)

  plt.plot(t, trace)
  plt.show()

def trace_butter(trace, tipo, f_cut, sr):
  fdominante = frecuencia_dominante(trace)
  orden = 15
  nyquist = 0.5 * sr
  print("Nyquist -> ", nyquist)
  print("Sampling rate -> ", sr)
  print("Frecuencia de corte -> ", f_cut)
  print("Orden -> ", orden)
  print("Frecuencia dominante -> ", fdominante)
  
  #diseño el filtro butterworth
  frec_norm = f_cut / nyquist
  b, a = butter(orden, frec_norm, btype=tipo, analog=False)
  return b,a

def apply_filter(b, a, signal):
  filtered = lfilter(b, a, signal)
  return filtered

if __name__ == '__main__':
  long_data = '/content/drive/MyDrive/samples/3D_gathers_pstm_nmo.sgy'
  header = segy_header_scan(long_data)
  dt = header.loc["TRACE_SAMPLE_INTERVAL"]["mean"] / 1000
  sr = 1000/dt

  V3D = xr.open_dataset(
    pathlib.Path(long_data),
    dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193, "ShotPoint":197 },
    extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
  )
  air1 = V3D.isel(ILINE_3D=0, CROSSLINE_3D=0).data
  trace = air1[0]

  #grafico la traza
  graph_trace(trace, dt)
  #hago el filtro
  b, a = trace_butter(trace, 'low', 25, sr)
  #aplico el filtro ala traza
  filtered_trace = apply_filter(b, a, trace)
  #grafico la traza filtrada
  graph_trace(filtered, dt)
  options = [1,2,3,4]
  #interface
  while True:
    print("Elige una opción de la siguiente lista")
    print("1.Graficar traza")
    print("2.Generar filtro")
    print("3.Aplicar filtro")
    print("4.Elegir archivo")
    opc = input()
    if not opc in options:
      print("opcion invalida\ndesea salir?")
      print("1.Si")
      print("2.Continuar")
      res = input()
      if res == 2:
        continue;
      else:
        break;

    if opc == 1:
      print("graficando")
    elif opc == 2:
      print("generando")
    elif opc == 3:
      print("aplicando")
    elif opc == 4:
      res = lookinfolder()
      print("archivos disponibles en carpeta input")
    else:
      break;
  
