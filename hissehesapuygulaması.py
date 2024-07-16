
#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import yfinance as yf
npNaN = np.nan
import pandas_ta as pta
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import base64
from tempfile import NamedTemporaryFile
from yahoo_fin import stock_info as si
from streamlit_option_menu import option_menu

  
tabs= ["TEMEL","TEKNİK","AL-SAT"]

page = st.sidebar.radio("📈HİSSE ANALİZ",tabs)

if page == "TEKNİK":
  figs=[]

  
  ### Tüm stok ihtiyaçlarınızı tek bir yerde bulun
  Hisse senedi hareketini daha iyi anlamak için sadece birkaç teknik gösterge sağlamakla kalmıyor, aynı zamanda gelecekteki fiyatı tahmin etmek için bir Sinir Ağ modelimiz var.""",unsafe_allow_html=True)
  
  # Kullanıcıdan hisse senedi simgesini al
  ticker = st.text_input("Hisse Senedi Göstergesi")
  
  ticker = ticker.upper()
  # Eğer bir simge girilmemişse, varsayılan olarak "BIST100" olarak ayarladım
  if ticker == "":
      ticker = "XU100.IS"
  # Girilen simgeyi görüntüle
  st.write("**BIST100 için örnek sembol girişi:** **PGSUS.IS**, **DOAS.IS** **vb.**")
  st.write("**S&P500 için örnek sembol girişi:** **^GSPC**, **NVDA**, **TSLA**, **AMZN** **etc.**")
  
  # Finansal API'den (Örn: Yahoo Finance) simgeye ait hisse verilerini aldım
  df = si.get_data(ticker)
  df["date"] = df.index
  
  # Hisse DataFrame'inden gerekli verileri çıkardım
  open_prices = df['open']
  close_prices = df['close']
  volumes = df['volume']
  high_prices = df['high']
  low_prices = df['low']
  dates = df['date']
  DATA_LEN = 300
  
  
  # Her veri sütunu için son DATA_LEN sayısı kadar veri noktasını aldım
  dates = dates[-DATA_LEN:].to_list()
  close_prices = close_prices[-DATA_LEN:].to_list()
  open_prices = open_prices[-DATA_LEN:].to_list()
  volumes = volumes[-DATA_LEN:].to_list()
  high_prices = high_prices[-DATA_LEN:].to_list()
  low_prices = low_prices[-DATA_LEN:].to_list()
  
  # İleriki hesaplamalar için 'close' sütununu seçtim
  close_for_calc = df['close'][-DATA_LEN:]
  
  
  st.text("");st.text("");st.text("")
  
  
  
  st.markdown("## Teknik Göstergeler")
  
  # Kapanış Fiyatı Görselleştirme
  fig = plt.figure()
  plt.title(f"{ticker} için kapanış fiyatları: {ticker} şu anda {round(close_prices[len(close_prices) - 1], 2)}", fontsize=15,color="black")
  plt.xlabel("Gün Sonrası", fontsize=12,color="black")
  plt.ylabel("Fiyat", fontsize=12,color="black")
  plt.plot(close_prices, label='Kapanış Fiyatı')
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  st.markdown("***")
  
  
  
  # RSI 
  relative_strength_indexs = pta.rsi(close_for_calc, length=14)
  relative_strength_indexs = relative_strength_indexs.to_list()
  
  
  fig = plt.figure()
  plt.plot(relative_strength_indexs, label='RSI Değeri')
  plt.title(f"14 günlük RSI ", fontsize=17, color="black")
  plt.xlabel("Gün Sonrası", fontsize=15, color="black")
  plt.ylabel("RSI Değeri", fontsize=15, color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  
  st.text("")
  st.markdown("Verilen grafikte, RSI > 70 aşırı alım hissesini ve RSI < 30 aşırı satım hissesini gösterir.")
  st.markdown("***")
  
  
  # Bollinger Bantları
  # Kapanış fiyatlarının 5 günlük hareketli ortalamasını hesapladım
  close_avg = close_for_calc.rolling(5).mean().to_list()
  
  # Kapanış fiyatlarının 5 günlük hareketli standart sapmasını hesapladım
  standard_deviations = close_for_calc.rolling(5).std().to_list()
  
  upper_bollinger_band = []
  lower_bollinger_band = []
  
  # Her veri noktası için üst ve alt Bollinger Bantlarını hesapladım
  for i in range(len(standard_deviations)):
      # Üst sınırı, kapanış ortalaması artı iki kat standart sapma olarak hesapladım
      upper_bound = close_avg[i] + (standard_deviations[i] * 2)
  
      # Alt sınırı, kapanış ortalamasından iki kat standart sapma çıkartarak hesapladım
      lower_bound = close_avg[i] - (standard_deviations[i] * 2)
  
      upper_bollinger_band.append(upper_bound)
      lower_bollinger_band.append(lower_bound)
  
  
  
  fig = plt.figure()
  plt.plot(close_avg, label='Basit Hareketli Ortalama',color="black")
  plt.plot(upper_bollinger_band, label='Üst Bant')
  plt.plot(lower_bollinger_band, label='Alt Bant')
  plt.plot(close_prices, 'r', label='Kapanış Fiyatı')
  plt.title("2 std'li Bollinger Bantları", fontsize=17,color="black")
  plt.xlabel("Sonraki gün sayısı", fontsize=15,color="black")
  plt.ylabel("Fiyat", fontsize=15,color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  st.markdown("***")
  
  
  
  # OBV 
  on_balance_volumes = []
  obv = 0
  
  on_balance_volumes.append(obv)
  
  # Her veri noktası için On-Balance Volume (OBV) değerini hesapladım
  for i in range(1, len(volumes)):
      if close_prices[i] > close_prices[i - 1]:
          obv += volumes[i]
          on_balance_volumes.append(obv)
  
      elif close_prices[i] < close_prices[i - 1]:
          obv -= volumes[i]
          on_balance_volumes.append(obv)
  
      else:
          obv += 0
          on_balance_volumes.append(obv)
  
  
  NUM_OF_DAYS_2 = 5
  obv_df = pd.DataFrame(on_balance_volumes)
  obv_sma = obv_df.rolling(NUM_OF_DAYS_2).mean()
  
  
  
  fig = plt.figure()
  plt.plot(on_balance_volumes, label='OBV')
  plt.plot(obv_sma, label=' OBV için Basit Hareketli Ortalama')
  plt.title("OBV (On Balance Volume)  Bakiye Hacmi", fontsize=17,color="black")
  plt.xlabel("Sonraki gün sayısı", fontsize=15,color="black")
  plt.ylabel("OBV", fontsize=15,color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  st.markdown("***")
  
  
  # MACD
  ema12 = close_for_calc.ewm(span=12, adjust=False).mean()
  ema26 = close_for_calc.ewm(span=26, adjust=False).mean()
  
  macd = ema12 - ema26
  
  signal = macd.ewm(span=9, adjust=False).mean()
  
  fig = plt.figure()
  plt.plot(macd.to_list(), label='MACD')
  plt.plot(signal.to_list(), label='Signal')
  plt.title("Hareketli Ortalama Yakınsama Farklılığı", fontsize=17,color="black")
  plt.ylabel("MACD", fontsize=15,color="black")
  plt.xlabel("Gün Sonrası", fontsize=15,color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  st.markdown("***")
  
  
  
  # Momentum
  MOMENTUM_PERIOD = 10
  
  momentum_values = []
  
  # Her veri noktası için momentum değerlerini hesapladım
  for i in range(MOMENTUM_PERIOD, len(close_prices)):
      curr_close_price = close_prices[i]
      period_start_close_price = close_prices[i - MOMENTUM_PERIOD]
  
      # Momentumu, mevcut kapanış fiyatı ile dönem başından itibaren fiyat arasındaki fark olarak hesapladım
      momentum_values.append(curr_close_price - period_start_close_price)
  
  momentum_sum = 0
  
  # Momentum değerlerinin toplamını hesapladım
  for i in range(len(momentum_values)):
      momentum_sum += momentum_values[i]
  
  # Ortalama momentumu hesapladım
  avg_momentum = momentum_sum / len(momentum_values)
  
  fig = plt.figure()
  plt.plot(momentum_values, label='Momentum Values')
  plt.title(f"{MOMENTUM_PERIOD} gün boyunca hisse senedinin ivmesi ", fontsize=17,color="black")
  plt.ylabel("Momentum", fontsize=15,color="black")
  plt.xlabel("Gün Sonrası", fontsize=15,color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  
  
  
  pivot_points = []
  # Her veri noktası için pivot noktalarını hesapladım
  for i in range(len(close_for_calc)):
      if i == 0:
          pivot_points.append(float("nan"))  # İlk pivot noktasını NaN olarak ayarladım
      else:
          prev_high = high_prices[i - 1]
          prev_low = low_prices[i - 1]
          prev_close = close_prices[i - 1]
  
          # Pivot noktasını önceki yüksek, düşük ve kapanış fiyatlarının ortalaması olarak hesapladım
          pivot_point = (prev_high + prev_low + prev_close) / 3
          pivot_points.append(pivot_point)
  
  
  
  resistance_1 = []
  support_1 = []
  resistance_2 = []
  support_2 = []
  
  
  # Pivot noktalarına göre destek ve direnç seviyelerini hesapladım
  for i in range(len(pivot_points)):
      if i == 0:
          resistance_1.append(float("nan"))  # İlk direnç seviyesini NaN olarak ayarladım
          support_1.append(float("nan"))  # İlk destek seviyesini NaN olarak ayarladım
      else:
          prev_high = high_prices[i - 1]
          prev_low = low_prices[i - 1]
  
          # Birinci direnç ve destek seviyelerini hesapladım
          r1 = (2 * pivot_points[i]) - prev_low
          s1 = (2 * pivot_points[i]) - prev_high
  
          # İkinci direnç ve destek seviyelerini hesapla
          r2 = pivot_points[i] + (prev_high - prev_low)
          s2 = pivot_points[i] - (prev_high - prev_low)
  
          resistance_1.append(r1)
          support_1.append(s1)
          resistance_2.append(r2)
          support_2.append(s2)
  
  
  fig = plt.figure()
  plt.plot(close_prices, label='Kapanış Fiyatı')
  plt.plot(resistance_1, label='Direnç (birinci)')
  plt.plot(support_1, label='Destek (birinci)')
  plt.plot(resistance_2, label='Direnç (ikinci)')
  plt.plot(support_2, label='Destek (ikinci)')
  plt.title("Destek ve Direnç", fontsize=17, color="black")
  plt.xlabel("Gün Sonrası", fontsize=15, color="black")
  plt.ylabel("Fiyat", fontsize=15, color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  
  
  st.text("")
  st.markdown("Destek ve dirençleri daha iyi görmek için lütfen grafiği yakınlaştırın.")
  st.markdown("***")
  
  
  
  st.markdown("## Gelecek Fiyat Tahminleri")
  
  # Veri kümesini hazırla
  dataset = close_prices
  
  dataset = np.array(dataset)
  training = len(dataset)
  dataset = np.reshape(dataset, (dataset.shape[0], 1))
  
  # Veri kümesini ölçeklendir
  scaler = MinMaxScaler(feature_range=(0, 1))
  scaled_data = scaler.fit_transform(dataset)
  
  train_data = scaled_data[0:int(training), :]
  
  # Özellikleri ve etiketleri hazırla
  x_train = []
  y_train = []
  prediction_days = 60
  
  for i in range(prediction_days, len(train_data)):
      x_train.append(train_data[i-prediction_days:i, 0])
      y_train.append(train_data[i, 0])
  
  x_train, y_train = np.array(x_train), np.array(y_train)
  
  # Handle missing values in X (replace NaN with mean)
  x_train = np.nan_to_num(x_train, nan=np.nanmean(x_train))
  # Handle missing values in y (replace NaN with mean)
  y_train = np.nan_to_num(y_train, nan=np.nanmean(y_train))
  
  # Doğrusal Regresyon modelini eğit
  reg = LinearRegression().fit(x_train, y_train)
  
  x_tomm = close_prices[len(close_prices) - prediction_days:len(close_prices)]
  x_tomm = np.array(x_tomm)
  x_tomm_reshaped = x_tomm.reshape(-1, 1)
  
  # Yeniden şekillendirilmiş veriyi ölçeklendir
  x_tomm_scaled = scaler.transform(x_tomm_reshaped)
  
  # Ölçeklenmiş veriyi tekrar (1, n_features) şekline getir
  x_tomm_scaled_reshaped = x_tomm_scaled.reshape(1, -1)
  
  # Handle missing values in future predictions (replace NaN with mean)
  x_tomm_scaled_reshaped = np.nan_to_num(x_tomm_scaled_reshaped, nan=np.nanmean(x_tomm_scaled_reshaped))
  
  # Tahmin yap
  prediction = reg.predict(x_tomm_scaled_reshaped)
  prediction = scaler.inverse_transform(prediction.reshape(1, -1))
  
  # Tahmini göster
  st.markdown(f"#### Yarının tahmini için: {ticker} = {round(prediction[0][0], 2)}")
  
  st.markdown("***")
  
  # Kullanıcıdan gelecek gün sayısı girişi (20'yi geçmemesi önerilir)
  FUTURE_DAYS = st.text_input("Gelecek gün sayısını girin (20'yi geçmemesi önerilir)")
  
  try:
      FUTURE_DAYS = int(FUTURE_DAYS)
  except:
      FUTURE_DAYS = 10
  
  predicted_prices = []
  tot_prices = list(close_prices)
  
  # Belirtilen gün sayısı için gelecekteki fiyatları tahmin et
  for i in range(FUTURE_DAYS):
      x_prices = tot_prices[len(tot_prices) - prediction_days: len(tot_prices)]
      x_prices_reshaped = np.array(x_prices).reshape(1, -1)
      
      x_prices_scaled = np.zeros_like(x_prices_reshaped)
      for j in range(x_prices_reshaped.shape[1]):
          feature = x_prices_reshaped[:, j]
          feature_scaled = scaler.transform(feature.reshape(-1, 1))
          x_prices_scaled[:, j] = feature_scaled.flatten()
      
      # Handle missing values in future predictions (replace NaN with mean)
      x_prices_scaled = np.nan_to_num(x_prices_scaled, nan=np.nanmean(x_prices_scaled))
      
      prediction = reg.predict(x_prices_scaled)
      
      prediction_inverse_scaled = scaler.inverse_transform(prediction.reshape(-1, 1))
      
      tot_prices = np.concatenate((tot_prices, prediction_inverse_scaled.flatten()))
      predicted_prices.append(prediction_inverse_scaled)
  
  tot_prices = np.array(tot_prices)
  predicted_prices = np.array(predicted_prices)
  
  tot_prices = np.reshape(tot_prices, (tot_prices.shape[0]))
  predicted_prices = np.reshape(predicted_prices, (predicted_prices.shape[0]))
  
  fig = plt.figure()
  plt.plot(tot_prices, label='Tahmin Edilen Gelecek Fiyatlar')
  plt.plot(close_prices, label='Şimdiki fiyatlar')
  plt.xlabel("Gün Sonrası", fontsize=15, color="black")
  plt.ylabel("Fiyat", fontsize=15, color="black")
  plt.title("Gelecek Fiyat Tahminleri", fontsize=17, color="black")
  plt.legend()
  fig_html = mpld3.fig_to_html(fig)
  components.html(fig_html, height=500)
  figs.append(fig)
  
  
  
  # PDF İndirme İşlevselliği
  def create_download_link(val, filename):
      b64 = base64.b64encode(val)  
      return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Dosyayı indir</a>'
  
  st.text("")
  export_as_pdf = st.button("Raporu PDF Olarak Dışa Aktar")
  
  FONT_FAMILY = "Arial"
  WIDTH = 210
  HEIGHT = 297
  name = ""
  
  if export_as_pdf:
      # Yeni bir PDF örneği oluştur
      pdf = FPDF()
      pdf.add_page()
  
      # Ana başlık için yazı tipini ve boyutunu ayarla
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.ln(40)
      pdf.multi_cell(w=0, h=15, txt=f"Hisse senedi analizi: {ticker}", align='C')  # 'C' parametresi ile metni ortala
      pdf.ln(60)
  
      # Giriş için yeni bir sayfa ekle
      pdf.ln(40)
      pdf.add_page()
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="Giris")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=15)
      pdf.multi_cell(w=0, h=7, txt=f"Bu rapor, {ticker} hissesini cesitli teknik gostergeleri ve diger teknikleri kullanarak analiz edecek ve verilen hissenin gelecekteki egilimleri hakkinda fikir verecektir.")
      pdf.ln(50)
      pdf.ln(50)
  
      # Kullanılan göstergeler için yeni bir sayfa ekle
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="Kullanilan Gostergeler")
      pdf.ln(30)
  
      # Göstergelerin bir listesini tanımla
      indicators = ["RSI", 
                  "Bollinger Bantlari", 
                  "OBV", 
                  "MACD", 
                  "Momentum"]
  
      pdf.set_font(FONT_FAMILY, size=20)
  
      for i in range(len(indicators)):
          pdf.cell(0, txt=f"{i + 1}. {indicators[i]}")
          pdf.ln(10)  # Her gösterge başlığından sonra 6 birim yüksekliğinde bir boşluk bırakır
  
  
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="RSI")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(w=0, h=7,
                     txt=f"RSI veya Goreceli Güc Endeksi, bir hissenin asiri alim veya asiri satim durumunu gosterir. RSI >= 70, bir hissenin asiri alindigini ve fiyatda bir dusus olabilecegini gosterirken, RSI <= 30, bir hissenin asiri satildigini ve yakin bir gelecekte boga egilimi gosterebilecegini gosterir.")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=20)
      pdf.multi_cell(w=0, h=10, txt=f"RSI grafigi, {ticker} icin bir yil boyunca asagida verilmistir:")
      pdf.ln(8)
  
      # RSI grafiğini geçici bir resim dosyası olarak kaydet
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[1].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name, 12, 100, WIDTH - 20, 100)
      name = ""
      pdf.ln(115)
      pdf.set_font(FONT_FAMILY, size=12)
  
      curr_rsi = relative_strength_indexs[len(relative_strength_indexs) - 1]
      rsi_mean = pd.Series(relative_strength_indexs).mean()
  
      rsi_state_rel = f"high" if curr_rsi > rsi_mean + 2.5 else f"low"
      rsi_state_abs = f"low" if curr_rsi < 45 else (f"medium" if curr_rsi < 60 else f"high")
      sell_state = f"selling" if rsi_state_abs == "low" else f"buying"
      price_action_dir = f"upward" if sell_state == "selling" else f"downward"
  
      pdf.multi_cell(w=0, h=7,    
                     txt=f"Mevcut RSInin {round(curr_rsi, 2)} oldugu goruluyor ki bu, bir yil suren hisse senedi egilimine gore {rsi_state_rel} olarak kabul edilir. Normal bir senaryoda boyle bir RSI, {rsi_state_abs} olarak kabul edilir. Bu nedenle bu, daha fazla {sell_state} oldugunu ve yakin bir gelecekte {price_action_dir} bir egilim olabilecegini gosterir. Unutmayin ki bu, sirket veya sirketin genel performansi veya karliligi hakkindaki insanlarin duygularini dikkate almayan yalnizca bir teknik gosterge oldugu icin bu stratejiyi kullanmanin bir riski vardir. Bu, sadece bu gosterge icin degil, bundan sonraki tum diger gostergeler icin de gecerlidir.")
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="Bollinger Bantlari")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(w=0, h=7,
                     txt=f"Bollinger bantlarini kullanarak borsadaki oynaklik ve hareket halindeki onemli trendlerin olup olmadigi hakkinda fikir edinilebilir. Bollinger bantlari RSI ile desteklendiginde bize hisse senedinin durumu hakkinda cok net bir resim veriyor.")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(
          w=0, h=7, txt=f"Bollinger bantlari kullanarak hisse senedi piyasasinin volatilitesi hakkinda bir fikir edinmek mumkun ve herhangi bir buyuk trendin olup olmadigini takip etmek mumkun. RSI ile birlestirildiginde, bir hissenin durumu hakkinda cok net bir resim elde edebiliriz.")
      pdf.ln(10)
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[2].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name,
                12, 90, WIDTH - 20, 100)
      name = ""
      pdf.ln(100)
      pdf.set_font(FONT_FAMILY, size=12)
  
      close_price_sma_status = "above" if close_prices[len(close_prices) - 1] > close_avg[len(close_avg) - 1] else "below"
      close_sma_stat_msg = "bu, hisse senedinin 5 gunluk SMA donemi uzerinde boga egilimi gosterdigi anlamina gelir." if close_price_sma_status == "uzerinde" else "bu, hisse senedinin yakin gecmiste veya 5 gunluk SMA donemi boyunca dusus gosterdigi anlamina gelir." if close_price_sma_status == "above" else "bu, hisse senedinin yakin zamanda veya SMA donemi boyunca dusus egilimi gosterdigi anlamina gelir"
      pdf.ln(20)
      pdf.multi_cell(w=0, h=7,
                     txt=f"Bu durumda, mevcut kapanis fiyatinin 5 gunluk bir donem uzerinde oldugunu gorebiliriz. {close_sma_stat_msg}")
      
      pdf.ln(20)
  
      closer_band = "upper band" if abs(
          upper_bollinger_band[len(upper_bollinger_band) - 1] - close_prices[len(close_prices) - 1]) < abs(
          lower_bollinger_band[len(lower_bollinger_band) - 1] - close_prices[len(close_prices) - 1]) else "lower band"
  
      print(abs(upper_bollinger_band[len(upper_bollinger_band) - 1] - close_prices[len(close_prices) - 1]))
      print(abs(lower_bollinger_band[len(
          lower_bollinger_band) - 1] - close_prices[len(close_prices) - 1]))
  
      pdf.multi_cell(w=0, h=7,
                     txt=f"Artik devam edip ust ve alt bollinger bantlarina bakabiliriz. Sectigimiz hisse senedinin {closer_band} bandina daha yakin oldugunu gorebiliriz. Buna bakarak hisse senedinin egilimini ve gucunu tespit edebiliriz. Boylece bu, RSI gostergemizi cok sorunsuz bir sekilde tamamliyor.")
  
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="OBV")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(w=0, h=7,
                     txt=f"OBV veya On Balance Volume, bir varligin toplam islem hacmi hakkinda bir fikir edinmek ve hareket edip etmedigini takip etmek icin kullanilabilir. Bir hissenin OBV'sindeki herhangi buyuk hareketler, buyuk kurumsal yatirimcilar tarafindan yapilan herhangi hareketleri takip etmek icin kullanilabilir.")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=20)
      pdf.multi_cell(
          w=0, h=10, txt=f"{ticker} icin bir yil boyunca OBV'nin bir gorsellestirmesi:")
      pdf.ln(3)
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[3].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name,
                12, 90, WIDTH - 20, 100)
      name = ""
      pdf.ln(120)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.ln(30)
      pdf.multi_cell(w=0, h=7,
                     txt=f'Bu durumda, son OBV trendine bakarsak, buyuk kurumsal yatirimcilarla sadece siradan yatirimcilar arasindaki genel gorunum hakkinda iyi bir fikir edinebiliriz. Ayrica, OBV gostergesi herhangi baska ayrinti gerektirmez.')
  
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="MACD")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(w=0, h=7,
                     txt="MACD gostergesi bize hisse senedinin trendi hakkinda iyi bir fikir veriyor. MACD degerindeki artis sunu gosterir: "
                         "Fiyatin gosterdigi ve muhtemelen isaretin artan bir egilim gosterdigini varsayarsak, bunun tersi de dogrudur. Ayrica "
                         "MACD ile sinyal cizgisinin kesismesinin yeni bir trendin baslangicini gosterdigine dikkat edilmelidir.")
  
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=20)
      pdf.multi_cell(
          w=0, h=10, txt=f"{ticker} icin bir yil boyunca Momentum'un bir gorsellestirmesi:")
      pdf.ln(3)
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[4].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name,
                11, 100, WIDTH - 20, 100)
      name = ""
  
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="Momentum")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=12)
      pdf.multi_cell(w=0, h=7,
                     txt=f"Adi gibi Momentum gostergesi bize bir hisse senedinin momentumu, yani bir hisse senedinin sahip oldugu trendin gucu hakkinda fikir verir. Momentuma bakarak bir alim, satim, yukselis veya dusus egiliminin ne kadar sure devam edecegini belirleyebiliriz.")
      pdf.ln(15)
      pdf.set_font(FONT_FAMILY, size=20)
      pdf.multi_cell(
          w=0, h=10, txt=f"{ticker} icin bir yil boyunca OBVnin bir gorsellestirmesi:")
      pdf.ln(3)
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[5].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name,
                12, 90, WIDTH - 20, 100)
      name = ""
      pdf.ln(110)
      pdf.set_font(FONT_FAMILY, size=12)
  
      momentum_over_0 = "over zero" if momentum_values[len(momentum_values) - 1] > 0 else "below zero"
      curr_momentum = momentum_values[len(momentum_values) - 1]
      pdf.ln(30)
      pdf.multi_cell(
          w=0, h=7,
          txt=f"Son momentum degerlerine baktigimizda, hissenin momentumunu kolayca cikarabiliriz. Hissenin mevcut momentumu {round(curr_momentum, 2)} ve yil boyunca ortalama momentumu {round(avg_momentum, 2)}.")
  
  
      pdf.add_page()
      pdf.ln(5)
      pdf.set_font(FONT_FAMILY, size=30)
      pdf.cell(0, txt="Gelecek Fiyat Tahmini")
      pdf.ln(30)
      pdf.set_font(FONT_FAMILY, size=20)
      pdf.multi_cell(
          w=0, h=10, txt=f"Makine Ogrenimi modelimizin {FUTURE_DAYS} gun boyunca {ticker} ile ilgili tahmini:")
      pdf.ln(10)
      with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
          figs[7].savefig(tmpfile.name)
          name = tmpfile.name
  
      pdf.image(name,
                12, 70, WIDTH - 20, 100)
      name = ""
      html = create_download_link(pdf.output(dest="S").encode("latin-1"), f"{ticker} analizi")
      st.markdown(html, unsafe_allow_html=True)
      st.text("")
       
if page == "TEMEL":

    #streamlit.config.theme.base = "dark"
    st.title("**HİSSE TEMEL ANALİZ**")
    st.subheader(":chart:**:blue[hisse analiz]** :chart:", divider='blue')
    #st.set_page_config(
    # page_title="Hisse Hedef Fiyat Hesaplayıcı",
    #  page_icon="https://example.com/icon.png",
    #  layout="centered",
    #)
    
    
    
    # Kullanıcıdan hisse senedi adı almak için input fonksiyonu kullanın
    #hisse_adi = input("Hisse Adı : ").upper()
    hisse_input = st.text_input("**Hisse Adı (Sadece Borsadaki Kısaltma Adını Girin):**").upper()
    hisse_adi = hisse_input
    
    if hisse_adi:
      # hisse_adi değişkenini url1 değişkeninde hisse parametresine atayın
      url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse_adi
      #time.sleep(0.01)
      # web sitesinden yıl ve dönem bilgilerini çekmek için BeautifulSoup kullanın
      r1=requests.get(url1)
      s1=BeautifulSoup(r1.text, "html.parser")
      secim=s1.find("select", id="ddlMaliTabloFirst")
      secim2=s1.find("select", id="ddlMaliTabloGroup")
    
      #print(secim2)
    
      # yıl ve dönem bilgilerini listelere atayın
      grup=[]
      tarihler=[]
      yıllar=[]
      donemler=[]
    
      # try to find the elements with BeautifulSoup
      try:
        cocuklar=secim.findChildren("option")
        grup=secim2.find("option")["value"]
    
    
        for i in cocuklar:
          tarihler.append(i.string.rsplit("/"))
    
        for j in tarihler:
          yıllar.append(j[0])
          donemler.append(j[1])
    
    
        if len(tarihler)>=4:
          # parametreler değişkenini oluşturun
          parametreler=(
              ("companyCode",hisse_adi),
              ("exchange","TRY"),
              ("financialGroup",grup),
              ("year1",yıllar[0]),
              ("period1",donemler[0]),
              ("year2",yıllar[1]),
              ("period2",donemler[1]),
              ("year3",yıllar[2]),
              ("period3",donemler[2]),
              ("year4",yıllar[3]),
              ("period4",donemler[3])
          )
          #print(tarihler)
          # web servisine istek gönderin ve veriyi alın
          url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
          r2= requests.get(url2,params=parametreler).json()["value"]
    
          # veriyi bir veri çerçevesine dönüştürün
          veri=pd.DataFrame.from_dict(r2)
    
          # gereksiz sütunları kaldırın
          veri.drop(columns=["itemCode","itemDescEng"],inplace=True)
          # Select the first row by its index
          ##En Son ÇEYREK
          Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
          ozkaynaklar1 = float(Ozkaynaklar.iloc[0, 1].replace(",", "."))      
          OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
          OdenmisSermaye1 = float(OdenmisSermaye.iloc[0, 1].replace(",", "."))      
          NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
          NetDonemKarı1 = float(NetDonemKarı.iloc[0, 1].replace(",", "."))      
          ##Bir Önceki Çeyrek
          Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
          ozkaynaklar_2 = float(Ozkaynaklar.iloc[0,2].replace(",", "."))  
          OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']     
          OdenmisSermaye_2 = float(OdenmisSermaye.iloc[0, 2].replace(",", ".")) 
          NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
          NetDonemKarı_2 = float(NetDonemKarı.iloc[0,2].replace(",", "."))       
          #İki Önceki Çeyrek Bilanço
          Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
          ozkaynaklar_3 = float(Ozkaynaklar.iloc[0,3].replace(",", "."))  
          OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']     
          OdenmisSermaye_3 = float(OdenmisSermaye.iloc[0, 3].replace(",", "."))    
          NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
          NetDonemKarı_3 = float(NetDonemKarı.iloc[0,3].replace(",","."))      
          ##Dört Dönem Önceki Bilanço
          Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
          ozkaynaklar_4 = float(Ozkaynaklar.iloc[0,4].replace(",", "."))  
          OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
          OdenmisSermaye_4 = float(OdenmisSermaye.iloc[0,4].replace(",", ".")) # 4 Dönem Önceki Bilanço
          NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
          NetDonemKarı_4 = float(NetDonemKarı.iloc[0,4].replace(",","."))
    
          #g_donemler = float(donemler.iloc[0])
          #g_yıllar = float(yıllar.iloc[0])   
          #g_tarihler = float(tarihler.iloc[0])
          #st.write(f"**(Güncel Bilanço Dönemi: {g_tarihler}**")
          #print("Özkaynaklar:", ozkaynaklar1)
          #print("Ödenmiş Sermaye:", OdenmisSermaye)
          ###print(f"Özkaynaklar: {float(ozkaynaklar1):,.2f}") # comma and dot separators
          ###print(f"Ödenmiş Sermaye: {float(OdenmisSermaye):,.2f}")
    
      # Print the desired data
          #print(ozkaynaklar)
          #print(OdenmisSermaye)
          # veriyi ekrana yazdırın
          #print(veri)
    
      except AttributeError:
        # print a message
        print("An AttributeError occurred")
        # skip the iteration
        #continue
    
      st.write(" İş Yatırım Sayfası İçin Tıklayın: [link](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx)")
      st.write(" Tradingview Grafik Sayfası İçin Tıklayın: [link](https://tr.tradingview.com/chart/)")
    
    
    
      ### KODUN 2. KISMI BURADAN BAŞLIYOR
    
      # URL for the initial page
      url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?"
    
      # Fetch the initial page content
      response = requests.get(url)
      temeldegerler = BeautifulSoup(response.text, "html.parser")
    
      # Find the tables containing the stock data
      table = temeldegerler.find("tbody", id="temelTBody_Ozet")
      f_oranlar = temeldegerler.find("tbody", id="temelTBody_Finansal")
    
      sektorkodu = temeldegerler.find("select", id="ddlSektor")
    
      # Create dictionaries to store stock information
      hisse_sektor = {}
      hisse_oran = {}
      sektor_numara = {}
    
      # Iterate over the first table to extract stock names and sectors
      for row in table.find_all("tr"):
          cells = row.find_all("td")
          hisse = cells[0].find("a").text.upper()
          sektor = cells[2].text
          hisse_sektor[hisse] = sektor
          ###sektor_output = hisse_sektor[hisse_input]
    
      # Iterate over the options in the select element
      for option in sektorkodu.find_all("option"):
          # Get the sector row number
          sektor_numarasi = option["value"]
          # Get the sector name
          sektor_ismi  = option.text
          # Add the pair to the dictionary
          sektor_numara[sektor_ismi] = sektor_numarasi
    
      # Iterate over the second table to extract financial ratios
      for r in f_oranlar.find_all("tr"):
          hucre = r.find_all("td")
          hisse_adi_1 = hucre[0].find("a").text.upper()
          kapanıs = hucre[1].text
          #c3 = float(kapanıs)
          f_k = hucre[2].text
          #c10 = float(fk_value)
          pd_dd = hucre[5].text
          #c11 = float(pd_value)
          hisse_oran[hisse_adi_1] = {"kapanıs": kapanıs, "f_k": f_k, "pd_dd": pd_dd}
    
      # Get the stock name from the user
      stock_name = hisse_adi #input("Hisse Adı Giriniz: ").upper()
    
      st.subheader(":one:**:blue[HİSSE VERİLERİ]**", divider='rainbow')
      
      if stock_name:
          # Check if the input is in the dictionary
          if stock_name in hisse_sektor:
              # Get the sector name from the dictionary
              sektor_output = hisse_sektor[stock_name]
              # Display the sector name
              st.write("**SEKTÖR ALANI:**",  sektor_output)
              #print("Sektör Alanı:", sektor_output)
              # Get the sector row number from the dictionary
              sektor_numarasi = sektor_numara[sektor_output]
              # Add the sector row number to the url
              url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?sektor="+sektor_numarasi
              # Make a new request with the updated url
              response = requests.get(url)
              temeldegerler = BeautifulSoup(response.text, "html.parser")
              sek_ortalama = temeldegerler.find("sectorArea", id="sectorAreaBigData")
              sek_ortalama = temeldegerler.find("div", id="sectorAreaBigData")
              sek_ortalama_fk = temeldegerler.find("div", "second-item text-right")
              sek_ortalama_pd = temeldegerler.find("div", "fifth-item text-right")
              # Ensure elements are found before extracting values
              if sek_ortalama_fk and sek_ortalama_pd:
                  # Get and clean the values
                  sek_ortalama_fk_value = sek_ortalama_fk.text.strip().replace(",", ".")
                  sek_ortalama_pd_value = sek_ortalama_pd.text.strip().replace(",", ".")
    
                  # Convert to floats
                  sek_ortalama_fk_float = float(sek_ortalama_fk_value)
                  sek_ortalama_pd_float = float(sek_ortalama_pd_value)
    
                  # Print the results
                  #print(sek_ortalama)
                  st.write(f"**Sektör F/K Oranı:** {sek_ortalama_fk_float}") #, box=True)
                  st.write(f"**Sektör PD/DD Oranı:** {sek_ortalama_pd_float}")#, box=True)
              else:
                  print("Error: Elements not found. Check website structure or selectors.")
    
    
      # Check if the stock exists in the dictionary
      if stock_name in hisse_oran:
          try:
              # Access the stock data and extract the F/K value
              kapanıs = hisse_oran[stock_name]["kapanıs"].replace(",", ".")
              st.write(f"   :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}") #, box = True)     
              fk_value = hisse_oran[stock_name]["f_k"].replace(",", ".")  # Format with dots as decimal separators
              if fk_value != "A/D":
                st.write(f"**:blue[HİSSE F/K ORANI:]**  {fk_value}") #, box = True)
              else:  
                fk_value_1 = st.number_input(f"**:blue[F/K VERİSİNE ULAŞILAMAMIŞTIR LÜTFEN F/K ORANI GİRİNİZ:]**")
                fk_value = float(fk_value_1)
              pd_value = hisse_oran[stock_name]["pd_dd"].replace(",", ".")
              if pd_value != "A/D":
                st.write(f"**:blue[HİSSE PD/DD ORANI:]**  {pd_value}") #, box = True)
              else:  
                pd_value_1 = st.number_input(f"**:blue[PD/DD VERİSİNE ULAŞILAMAMIŞTIR LÜTFEN PD/DD ORANI GİRİNİZ:]**")
                pd_value = float(pd_value_1)
              #st.write(f"**HİSSE F/K ORANI:**  {fk_value}") #, box = True)
              #st.write(f"**HİSSE PD/DD ORANI:**  {pd_value}") #, box = True)
              #print(f"{stock_name} Hisse Fiyatı: {kapanıs}")
              #print(f"{stock_name} F/K Oranı:  {fk_value}")
              #print(f"{stock_name} PD/DD Oranı:  {pd_value}")
              st.subheader(f"**Bilanço Verileri:**", divider='grey')
              st.write(f"**Güncel Dönem Bilanço Verileri:**")
              st.write(f"**:blue[ÖZKAYNAKLAR:]**  {float(ozkaynaklar1):,.0f}") #", box = True)
              st.write(f"**:blue[ÖDENMİŞ SERMAYE:]**  {float(OdenmisSermaye1):,.0f}") #, box = True)
              st.write(f"**:blue[NET DÖNEM KARI:]**  {float(NetDonemKarı1):,.0f}") #, box = True)
              st.write(f"**Geçmiş Dönem Bilanço Verileri:**")
              st.write(f"**ÖZKAYNAKLAR(Bir Önceki Çeyrek):**  {float(ozkaynaklar_2):,.0f}")
              st.write(f"**ÖZKAYNAKLAR(Bir Önceki Çeyrek):**  {float(OdenmisSermaye_2):,.0f}")         
              st.write(f"**NET DÖNEM KARI(Bir Önceki Çeyrek):**  {float(NetDonemKarı_2):,.0f}")
              st.write(f"**ÖZKAYNAKLAR(Geçmiş Yıl ):**  {float(ozkaynaklar_4):,.0f}") #", box = True)
              st.write(f"**ÖDENMİŞ SERMAYE(Geçmiş Yıl):**  {float(OdenmisSermaye_4):,.0f}") #, box = True)
              st.write(f"**NET DÖNEM KARI(Geçmiş Yıl):**  {float(NetDonemKarı_4):,.0f}") #, box = True)      
          except KeyError:
              #print("Hisse bulunamadı.") # Stock not found in the dictionary
              st.write("Hisse bulunamadı.")
      else:
          #print("Bir sorun var!")  # Stock not found in any of the dictionaries
          st.write(":red[Veri eksikliği var. Lütfen hisseyi kontrol ediniz!]")
        
      #import streamlit_tags as tags
    
      #st.write("Hisse Hedef Fiyat Hesaplayıcı")
    
      # Hisse Fiyatı
      #c3 = st.number_input("Hisse Fiyatı:" )
      #c3 = float(kapanıs)
      c3 = float(kapanıs.replace(".", ""))  # Replace comma with dot
      c3 = c3/100
      
      # Hisse F/K Oranı
      #c10 = float(st.number_input("Hisse F/K Oranı:"))
      c10 = float(fk_value) #.replace(",", "."))
      #if c10 != "A/D":
      #  c10 = st.number_input("F/K Değeri Bulunmamaktadır. Lütfen F/K Değeri Giriniz")
    
      # HİSSE PD/DD ORANI
      #c11 = st.number_input("Hisse PD/DD Oranı: ")
      c11 = float(pd_value) #.replace(",", "."))
    
      # BİST100 /SEKTÖR GÜNCEL F/K ORANI
      #c12 = float(st.number_input("BİST100 / Sektör Güncel F/K Oranı: "))
      c12 = sek_ortalama_fk_float
    
      # BIST100 / Sektör Güncel P/D Oranı
      #c13 = float(st.number_input("BİST100 / Sektör Güncel PD/DD Oranı:"))
      c13 = sek_ortalama_pd_float
    
      # Ödenmiş Sermaye
      ##c4 = st.number_input("Ödenmiş Sermaye: ")
      c4 = float(OdenmisSermaye1) #Otomatik Veri İşlem İçin Bu Satır
      c4_2 = float(OdenmisSermaye_2) #Otomatik Veri İşlem İçin Bu Satır
      c4_3 = float(OdenmisSermaye_3) #Otomatik Veri İşlem İçin Bu Satır
      c4_4 = float(OdenmisSermaye_4) #Otomatik Veri İşlem İçin Bu Satır  
      ###c4 = ("{float(OdenmisSermaye):,.2f}")
      ####c4 = float(OdenmisSermaye.replace(",", "."))
    
      # Yıllık Net Kar
      ##c7 = st.number_input("Yıllık Net Kar: ")
      c7 = float(NetDonemKarı1) #Otomatik Veri İşlem İçin Bu Satır
      c7_2 = float(NetDonemKarı_2)
      c7_3 = float(NetDonemKarı_3)
      c7_4 = float(NetDonemKarı_4)
      ###c7 = ("{float(NetDonemKarı1):,.2f}")
      ###c7 = float(NetDonemKarı1.replace(",", "."))
      #c15 = c7*2
      #st.write(c15)
    
      # Özsermaye
      ##c8 = st.number_input("Özsermaye : ")
      c8 = float(ozkaynaklar1) #Otomatik Veri İşlem İçin Bu Satır
      c8_2 = float(ozkaynaklar_2)
      c8_3 = float(ozkaynaklar_3)
      c8_4 = float(ozkaynaklar_4)
      ###c8 = (f"{float(ozkaynaklar1):,.2f}")
      ###c8 = float(ozkaynaklar1.replace(",", "."))
    
      # Güncel Piyasa Değeri
      #c9 = st.number_input("Güncel Piyasa Değeri: ")
    
      # HİSSE HESAPLAYICISI SELECT BOX İLE F/K VE PD/DD ORANLARINA GÖRE HESAPLAMA
      #st.write("**HİSSE HEDEF FİYAT HESAPLAYICI**")
      st.subheader(":two:**HİSSE HEDEF FİYAT HESAPLAYICI**", divider='rainbow')
    
      operation = st.selectbox(":blue[**HİSSE FİYAT HESAPLAMARI İÇİN İŞLEM SEÇİN:**]", ["İŞLEM SEÇİN", "GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI", "BİR ÇEYREK SONRAKİ HEDEF FİYATI TAHMİNİ", "1 YIL SONRAKİ HİSSE HEDEF FİYATI TAHMİNİ", "1. Çeyrek Bilanço Hisse Oranları-3 Aylık", "2. Çeyrek Bilanço Hisse Oranları-6 Aylık", "3. Çeyrek Bilanço Hisse Oranları-9 Aylık", "4. Çeyrek Bilanço Hisse Oranları-12 Aylık"])
      #if operation == "Tüm Hedef Fiyatları Göster":
      if operation == "İŞLEM SEÇİN":
        st.write(f"İŞLEM SEÇİN")
        #st.write(f":red[Aşağıdaki kırmızı uyarı yazısı veriler girilmediği için çıkmaktadır. Lütfen verileri girip yapmak istediğiniz işlemi seçin.]")
      
      elif operation == "GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI":
        #c7_3 = c7+c6 ## Yılsonu Net Kar Tahmini
        c16_4 = c7 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17 = c3 / c16_4 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")    
    
      elif operation == "BİR ÇEYREK SONRAKİ HEDEF FİYATI TAHMİNİ":  
        c7_y = c7+(c7-c7_2)
        #c7_3 = c7+c6 ## Yılsonu Net Kar Tahmini
        c16_4 = c7_y / c4 ## EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17 = c3 / c16_4 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7_y*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7_y/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7_y / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")         
    
      elif operation == "1 YIL SONRAKİ HİSSE HEDEF FİYATI TAHMİNİ":
        c7_1 = c7*4 ## Yılsonu Net Kar Tahmini
        c10_f = c7/c4
        c16_1 = c7_1 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17_1 = c3 / c16_1 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7_1*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17_1)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")  
      
      elif operation == "1. Çeyrek Bilanço Hisse Oranları-3 Aylık":
        c7_1 = c7*4 ## Yılsonu Net Kar Tahmini
        c10_f = c7/c4
        c16_1 = c7_1 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17_1 = c3 / c16_1 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7_1*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17_1)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")  
    
      elif operation == "2. Çeyrek Bilanço Hisse Oranları-6 Aylık":
        c7_2 = c7*2 ## Yılsonu Net Kar Tahmini
        c10_f = c7/c4
        c16_2 = c7_2 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17_2 = c3 / c16_2 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7_2*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17_2)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")  
    
      elif operation == "3. Çeyrek Bilanço Hisse Oranları-9 Aylık":
        c6 = c7/3
        c7_3 = c7+c6 ## Yılsonu Net Kar Tahmini
        c10_f = c7/c4
        c16_3 = c7_2 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17_3 = c3 / c16_3 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7_3*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17_3)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7_3/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7_3 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
    
      elif operation == "4. Çeyrek Bilanço Hisse Oranları-12 Aylık":
        #c7_3 = c7+c6 ## Yılsonu Net Kar Tahmini
        c16_4 = c7 / c4 ## Yılsonu EPS(Hisse Başı Kazanç) Tahmini
        #c16 =  c7 / c4     ## EPS(Hisse Başı Kazanç)
        c17 = c3 / c16_4 ## Yılsonu F/K Oranı Tahmini
        c21 = (c7*7)+(c8*0.5)
        potansiyel_fiyat = c21/c4
        future_fk = (c3/c17)*c12
        fk_hedef_fiyat = c3 / c10 * c12
        pd_hedef_fiyat = c3 / c11 * c13
        ozsermaye_hf = (c7/c8)*10/c11*c3 ##Yılsonu Tahmini Özsermaye Karlılığına Göre Hedef Fiyat
        odenmis_hedef_fiyat = (c7 / c4) * c10
        ortalama_hesap = ( fk_hedef_fiyat + future_fk + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
        st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
        st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")    
          
      #if operation == "ORTALAMA HEDEF FİYAT":
      #st.write(ortalama_hesap)
      #if ortalama_hesap < kapanıs :
        #st.write(f":blue[**TÜM HESAPLAMALARIN ORTALAMA FİYATI:**] {ortalama_hesap:,.2f}")
      #else :
        #st.write(f"**TÜM HESAPLAMALARIN ORTALAMA FİYATI:** :green[{ortalama_hesap:,.2f}]")
      #elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
        #st.write(f":blue[**Güncel EPS (Hisse Başı Kazanç):**] { c16 :,.2f}")
        #st.write(f":blue[**Yılsonu EPS (Hisse Başı Kazanç) Tahmini:**] { c16_3 :,.2f}")    
        #st.write(f":blue[**Güncel F/K:**] { c17 :,.2f}")
        #st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
        #st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
        #st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {fk_hedef_fiyat:,.2f}")
        #st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
        #st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
        #st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
        #st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
        #st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
       
      
      
      ##elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
      ##  c21 = (c7*7)+(c8*0.5)
      ##  potansiyel_fiyat = c21/c4
      ##  st.write(f":blue[**POTANSİYEL DEĞERİNE GÖRE HİSSE FİYATI:**] {potansiyel_fiyat:,.2f}")
      ##  #st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")
      #operation = st.selectbox("[ORTALAMA HEDEF FİYAT]")
      ##  fk_hedef_fiyat = c3 / c10 * c12
      ##  pd_hedef_fiyat = c3 / c11 * c13
      ##  ozsermaye_hf = (c7/c8)*10/c11*c3
      ##  odenmis_hedef_fiyat = (c7 / c4) * c10
      ##  c21 = (c7*7)+(c8*0.5)
      ##  potansiyel_fiyat = c21/c4
      ##  ortalama_hesap = ( fk_hedef_fiyat + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
      #if operation == "ORTALAMA HEDEF FİYAT":
      #st.write(ortalama_hesap)
      #if ortalama_hesap < kapanıs :
        #st.write(f":blue[**TÜM HESAPLAMALARIN ORTALAMA FİYATI:**] {ortalama_hesap:,.2f}")
      #else :
        #st.write(f"**TÜM HESAPLAMALARIN ORTALAMA FİYATI:** :green[{ortalama_hesap:,.2f}]")
      #elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
      ##  st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
      ##  st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
      ##  st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
      ##  st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
      ##  st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
      ##  st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
       
    
    else:
      st.write(":arrow_up:","Lütfen Yukarıdaki Alana Hisse Yazınız",":arrow_up:")
      st.write("(Not: Bankalar ve Faktöring Şirketleri Dahil Değildir)")
    
    
    
        #if __name__ == "__main__":
        #  st.run()
    
    
    #!streamlit run deneme.py & npx localtunnel --port 8501
