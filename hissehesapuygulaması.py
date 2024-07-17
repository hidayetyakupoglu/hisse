
#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import yfinance as yf
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import math

def Supertrend(df, atr_period=10, multiplier=3):
    high, low, close = df['High'], df['Low'], df['Adj Close']
    
    true_range = pd.concat([high - low, high - close.shift(), close.shift() - low], axis=1).abs().max(axis=1)
    average_true_range = true_range.ewm(alpha=1/atr_period, min_periods=atr_period).mean()
    df['ATR'] = average_true_range
    
    hl2 = (high + low) / 2
    
    upper_band = hl2 + (multiplier * average_true_range)
    lower_band = hl2 - (multiplier * average_true_range)
    
    supertrend = pd.Series(True, index=df.index)
    
    for i in range(1, len(df.index)):
        if close.iloc[i] > upper_band.iloc[i-1]:
            supertrend.iloc[i] = True
        elif close.iloc[i] < lower_band.iloc[i-1]:
            supertrend.iloc[i] = False
        else:
            supertrend.iloc[i] = supertrend.iloc[i-1]
            
            if supertrend.iloc[i] and lower_band.iloc[i] < lower_band.iloc[i-1]:
                lower_band.iloc[i] = lower_band.iloc[i-1]
            if not supertrend.iloc[i] and upper_band.iloc[i] > upper_band.iloc[i-1]:
                upper_band.iloc[i] = upper_band.iloc[i-1]
        
        upper_band.iloc[i] = np.nan if supertrend.iloc[i] else upper_band.iloc[i]
        lower_band.iloc[i] = np.nan if not supertrend.iloc[i] else lower_band.iloc[i]
    
    result_df = pd.DataFrame({'Supertrend': supertrend, 'Lowerband': lower_band, 'Upperband': upper_band}, index=df.index)
    
    return result_df
def backtest_supertrend(df, initial_investment=100000, trading_commission=0):
    is_uptrend = df['Supertrend']
    close = df['Adj Close']

    position = False
    total_equity = initial_investment
    shares = 0
    entry_points = []
    exit_points = []

    for i in range(2, len(df)):

        if not position and is_uptrend.iloc[i]:
            shares_float = total_equity / close.iloc[i]
            shares_rounded = math.floor(shares_float)
            shares = shares_rounded
            total_equity -= shares * close.iloc[i]
            entry_points.append((i, close.iloc[i]))
            position = True
            print(f'Buy {shares} shares at {round(close.iloc[i],2)} on {df.index[i].strftime("%d/%m/%Y")}')

        elif position and not is_uptrend.iloc[i]:
            total_equity += shares * close.iloc[i] - trading_commission
            exit_points.append((i, close.iloc[i]))
            position = False
            print(f'Sell at {round(close.iloc[i],2)} on {df.index[i].strftime("%d/%m/%Y")}')

    total_equity += shares * close.iloc[i] - trading_commission if position else 0

    earning = round(total_equity - initial_investment, 2)
    roi = round(earning / initial_investment*100, 1)
    print("*" * 30)
    print(f'Total profit after investing {initial_investment}₺ is {round(earning,2)}₺\nReturn on Investment (ROI): %{roi}')
    print("*" * 30)
    return entry_points, exit_points, total_equity


# Define the symbols of BIST 100
bist100 = ['AEFES.IS', 'AGHOL.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKENR.IS', 'AKGRT.IS', 'AKSA.IS', 'AKSEN.IS',
    'ALARK.IS', 'ALGYO.IS', 'ARCLK.IS', 'ASELS.IS', 'AVOD.IS', 'BAGFS.IS', 'BANVT.IS', 'BIMAS.IS',
    'BIZIM.IS', 'BRISA.IS', 'BRKSN.IS', 'BOBET.IS', 'CCOLA.IS', 'CEMTS.IS', 'CIMSA.IS', 'CMENT.IS', 'CLEBI.IS',
    'DEVA.IS', 'DOHOL.IS', 'DOAS.IS', 'ECILC.IS', 'ECZYT.IS', 'EGSER.IS', 'EKGYO.IS', 'ENJSA.IS',
    'ENKAI.IS', 'EREGL.IS', 'FROTO.IS', 'GARAN.IS', 'GENTS.IS', 'GLYHO.IS', 'GOODY.IS', 'GUBRF.IS',
    'HALKB.IS', 'HURGZ.IS', 'ICBCT.IS', 'IHEVA.IS', 'IHLAS.IS', 'ISFIN.IS', 'ISGYO.IS', 'ISMEN.IS',
    'ISYHO.IS', 'ISCTR.IS', 'KARSN.IS', 'KARTN.IS', 'KCHOL.IS', 'KORDS.IS', 'KOZAA.IS', 'KOZAL.IS',
    'KRDMD.IS', 'LOGO.IS', 'MAVI.IS', 'MGROS.IS', 'NTHOL.IS', 'ODAS.IS', 'OTKAR.IS', 'OZKGY.IS',
    'PETKM.IS', 'PGSUS.IS', 'PRKME.IS', 'QUAGR.IS', 'RAYSG.IS', 'SAHOL.IS', 'SASA.IS', 'SELEC.IS',
    'SISE.IS', 'SKBNK.IS', 'SOKM.IS', 'TATGD.IS', 'TAVHL.IS', 'TCELL.IS', 'THYAO.IS', 'TKFEN.IS',
    'TOASO.IS', 'TRGYO.IS', 'TRKCM.IS', 'TSKB.IS', 'TTKOM.IS', 'TTRAK.IS', 'TUPRS.IS', 'ULKER.IS',
    'ULUSE.IS', 'VAKBN.IS', 'VESTL.IS', 'VESTN.IS', 'VKGYO.IS', 'YATAS.IS', 'YKGYO.IS', 'YKBNK.IS',
    'ZOREN.IS']
  
tabs= ["TEMEL","TEKNİK","AL-SAT"]

page = st.sidebar.radio("📈HİSSE ANALİZ",tabs)
st.sidebar.title("İletişim Bilgileri")
st.sidebar.subheader("Yazar:")
st.sidebar.write("Hidayet YAKUPOĞLU")
st.sidebar.subheader("E-posta:")
st.sidebar.write("hidayetyakupoglu@gmail.com")



if page == "AL-SAT":
    st.markdown("""
    ## AL-SAT Sayfası
    Bu sayfada, BIST 100 endeksindeki hisse senetleri için Supertrend göstergesi kullanarak "Al" veya "Sat" sinyalleri oluşturabilirsiniz.
    butonlara tıklayarak tarama işlemini başlatabilirsiniz.
    """)
    ticker = st.text_input("Hisse Senedi Göstergesi")
    ticker = ticker.upper()
    # Eğer bir simge girilmemişse, varsayılan olarak "BIST100" olarak ayarladım
    if ticker == "":
        ticker = "XU100.IS"
    # Girilen simgeyi görüntüle
    st.write("**BIST100 için örnek sembol girişi:** **ASELS.IS**, **ULKER.IS** **vb.**")
    if st.button("SEÇİLİ HİSSE İÇİN SUPERTREND BACKTEST YAP"): 
     
        df = yf.download(ticker, start='2024-01-01')
        supertrend = Supertrend(df)
        df = df.join(supertrend)
        st.subheader('Supertrend Analizi')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.plot(df['Adj Close'], label='Kapanıs fiyatı')
        ax1.plot(df['Lowerband'], color='green', label='UST BAND')
        ax1.plot(df['Upperband'], color='red', label='ALT BAND')
        ax1.legend()
        # İkinci subplot
        ax2.plot(df['ATR'], color='purple', label='ATR')
        ax2.legend()

        # Başlık ekleme
        fig.suptitle(f'Supertrend Analizi - {ticker}', fontsize=16)

        # Görseli Streamlit'e gönderme
        st.pyplot(fig)
        
        entry_points, exit_points, roi = backtest_supertrend(df)
        roi=((roi-100000)*100)/(100000)
        st.write(f'2024 yılı başından bu yana Toplam Kar %: {roi}')
        


            

    if st.button("DURUM DEĞİŞTİREN HİSSELERİ TARA"):     
        signals = []
        for symbol in bist100:
            try:
                df = yf.download(symbol, start='2024-01-01')
                supertrend = Supertrend(df)
                df = df.join(supertrend)
             
                # Son 5 periyot için al/sat sinyallerini kontrol et
                last_5_signals = []
                for i in range(1, 11):
                    if df['Adj Close'][-i] > df['Lowerband'][-i]:
                        last_5_signals.append("AL ")
                    else:
                        last_5_signals.append("SAT")
        
                signals.append((symbol, ", ".join(last_5_signals)))
        
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
        
        df_signals = pd.DataFrame(signals, columns=['Symbol', 'Son 10 Sinyal(t,t-1,...)'])
        sat_to_al_symbols = df_signals[df_signals['Son 10 Sinyal(t,t-1,...)'].str.endswith('SAT') & df_signals['Son 10 Sinyal(t,t-1,...)'].str.contains('AL ')]
        al_to_sat_symbols = df_signals[df_signals['Son 10 Sinyal(t,t-1,...)'].str.endswith('AL ') & df_signals['Son 10 Sinyal(t,t-1,...)'].str.contains('SAT')]
        # Bu hisseleri sırala
        al_to_sat_symbols_sorted = al_to_sat_symbols.sort_values('Symbol')
        sat_to_al_symbols_sorted = sat_to_al_symbols.sort_values('Symbol')
        
        st.markdown(" SAT SİNYALİNE DÖNEN HİSSELER ")
        
        st.table(al_to_sat_symbols_sorted)
      
        st.markdown(" AL SİNYALİNE DÖNEN HİSSELER ")
        
        st.table(sat_to_al_symbols_sorted)
         
      
    if st.button("TÜM BİST 100 HİSSELERİNİ TARA"):
        signals = []
        for symbol in bist100:
            try:
                df = yf.download(symbol, start='2024-01-01')
                supertrend = Supertrend(df)
                df = df.join(supertrend)
                # Son kapanış fiyatı Supertrend'in alt bandının üzerindeyse al sinyali ver
                if df['Adj Close'][-1] > df['Lowerband'][-1]:
                    signals.append((symbol, "Al"))
                else:
                    signals.append((symbol, "Sat"))
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
        
        df_signals = pd.DataFrame(signals, columns=['Symbol', 'Signal'])
        st.table(df_signals)

if page == "TEKNİK":
    figs=[]
    st.markdown(""" ## Hisse Senedi Fiyat Analizi ve Tahmini  """,unsafe_allow_html=True)
    # Kullanıcıdan hisse senedi simgesini al
    ticker = st.text_input("Hisse Senedi Göstergesi")
    
    ticker = ticker.upper()
    # Eğer bir simge girilmemişse, varsayılan olarak "BIST100" olarak ayarladım
    if ticker == "":
        ticker = "XU100.IS"
    # Girilen simgeyi görüntüle
    st.write("**BIST100 için örnek sembol girişi:** **ASELS.IS**, **ULKER.IS** **vb.**")
    
    
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

    # Calculate EMA for 8, 21, and 50 days
    ema_8 = df['close'].ewm(span=8, adjust=False).mean()[-DATA_LEN:].to_list()
    ema_21 = df['close'].ewm(span=21, adjust=False).mean()[-DATA_LEN:].to_list()
    ema_50 = df['close'].ewm(span=50, adjust=False).mean()[-DATA_LEN:].to_list()
    ema_100 = df['close'].ewm(span=100, adjust=False).mean()[-DATA_LEN:].to_list()
    st.text("");st.text("");st.text("")
    
    
    
    st.markdown("## Teknik Göstergeler")
    
    # Kapanış Fiyatı Görselleştirme
    fig = plt.figure()
    plt.title(f"{ticker} için kapanış fiyatları ve EMA'lar: {ticker} şu anda {round(close_prices[-1], 2)}", fontsize=15, color="black")
    plt.xlabel("Gün Sonrası", fontsize=12, color="black")
    plt.ylabel("Fiyat", fontsize=12, color="black")
    plt.plot(close_prices, label='Kapanış Fiyatı')
    plt.plot(ema_8, label='8 Günlük EMA')
    plt.plot(ema_21, label='21 Günlük EMA')
    plt.plot(ema_50, label='50 Günlük EMA')
    plt.plot(ema_100, label='100 Günlük EMA')
    plt.legend()
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=500)
    
    
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
    
    
  
       
if page == "TEMEL":

    #streamlit.config.theme.base = "dark"
    st.title("**HİSSE TEMEL ANALİZ**")
    st.subheader(":blue[hisse analiz]** :chart:", divider='blue')
    #st.set_page_config(
    # page_title="Hisse Hedef Fiyat Hesaplayıcı",
    #  page_icon="https://example.com/icon.png",
    #  layout="centered",
    #)
    
    
    
    # Kullanıcıdan hisse senedi adı almak için input fonksiyonu kullanın
    #hisse_adi = input("Hisse Adı : ").upper()
    hisse_input = st.text_input("**Hisse Adı (Sembol adı: ASELS,ULKER vb):**").upper()
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
          fd_fav = hucre[3].text
          #c10 = float(fk_value)
          pd_dd = hucre[5].text
          #c11 = float(pd_value)
          hisse_oran[hisse_adi_1] = {"kapanıs": kapanıs, "f_k": f_k, "pd_dd": pd_dd, "fd_fav": fd_fav}
    
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
              sek_ortalama_fav = temeldegerler.find("div", "third-item text-right")
              # Ensure elements are found before extracting values
              if sek_ortalama_fk and sek_ortalama_pd:
                  # Get and clean the values
                  sek_ortalama_fk_value = sek_ortalama_fk.text.strip().replace(",", ".")
                  sek_ortalama_pd_value = sek_ortalama_pd.text.strip().replace(",", ".")
                  sek_ortalama_fav_value = sek_ortalama_fav.text.strip().replace(",", ".")
                  # Convert to floats
                  sek_ortalama_fk_float = float(sek_ortalama_fk_value)
                  sek_ortalama_pd_float = float(sek_ortalama_pd_value)
                  sek_ortalama_fav_float = float(sek_ortalama_fav_value)
                  # Print the results
                  #print(sek_ortalama)
                  st.write(f"**Sektör F/K Oranı:** {sek_ortalama_fk_float}") #, box=True)
                  st.write(f"**Sektör PD/DD Oranı:** {sek_ortalama_pd_float}")#, box=True)
                  st.write(f"**Sektör FD/FAVÖK Oranı:** {sek_ortalama_fav_float}")#, box=True)
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
              fav_value = hisse_oran[stock_name]["fd_fav"].replace(",", ".")
              if fav_value != "A/D":
                st.write(f"**:blue[HİSSE FD/FAVÖK ORANI:]**  {fav_value}") #, box = True)
              else:  
                fav_value_1 = st.number_input(f"**:blue[FD/FAVÖK VERİSİNE ULAŞILAMAMIŞTIR LÜTFEN ORANI GİRİNİZ:]**")
                fav_value = float(fav_value_1)
             
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
      
      # HİSSE FD/FAVÖK ORANI
      #c11 = st.number_input("Hisse PD/DD Oranı: ")
      c00 = float(fav_value) #.replace(",", "."))  
    
      # BİST100 /SEKTÖR GÜNCEL F/K ORANI
      #c12 = float(st.number_input("BİST100 / Sektör Güncel F/K Oranı: "))
      c12 = sek_ortalama_fk_float
    
      # BIST100 / Sektör Güncel P/D Oranı
      #c13 = float(st.number_input("BİST100 / Sektör Güncel PD/DD Oranı:"))
      c13 = sek_ortalama_pd_float

      # BIST100 / Sektör Güncel FD/FAVÖK Oranı
      #c13 = float(st.number_input("BİST100 / Sektör Güncel FD/FAVÖK Oranı:"))
      c01 = sek_ortalama_fav_float
     
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
      
      fk_hedef_fiyat = c3 / c10 * c12
      pd_hedef_fiyat = c3 / c11 * c13
      fav_hedef_fiyat = c3 / c00* c01
      ortalama_hesap = ( fk_hedef_fiyat + pd_hedef_fiyat + fav_hedef_fiyat  ) / 3
      st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
      st.write(f":blue[**FD/FAVÖK HEDEF FİYAT:**] {fav_hedef_fiyat:,.2f}")  
      st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
      st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
      st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")    
    
     
    
    
    
    

