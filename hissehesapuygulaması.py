
#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
#import investpy
import numpy as np
import yfinance as yf




tabs= ["FİNANSAL","TEKNİK ANALİZ","HAKKINDA"]

page = st.sidebar.radio("📈BIST 100",tabs)

if page == "FİNANSAL":

  #streamlit.config.theme.base = "dark"
  st.title("**BIST HİSSE FİYAT **")
  st.subheader("**:blue[BORSA HİSSE HESAPLAYICISI*by hidayet_yakupoglu]** :", divider='red')
  #st.set_page_config(
  # page_title="Hisse Hedef Fiyat Hesaplayıcı",
  #  page_icon="https://example.com/icon.png",
  #  layout="centered",
  #)
  
  
  
  # Kullanıcıdan hisse senedi adı almak için input fonksiyonu kullanın
  #hisse_adi = input("Hisse Adı : ").upper()
  
  
  
  ticker_all_List = pd.read_csv("bist.csv")
  tickers_all=ticker_all_List["Ticker"]
  hisse_input = st.selectbox('Hisse',tickers_all,index=38,help='Analiz Etmek İstediğiniz Hisseyi Seçebilirsiniz.')
  
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
  
    #st.write(" İş Yatırım Sayfası İçin Tıklayın: [link](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx)")
  
    
    #st.write(" Tradingview Grafik Sayfası İçin Tıklayın: [link](https://tr.tradingview.com/chart/)")
    
  
    #Gelecek Özkaynak Tahmini Miktarı
    #Gelecek Özkaynak Tahmini Miktarı
    
      #c22 = st.number_input(f"**Geçmiş Dönem Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın")
      #c24 = st.number_input(f"**Geçmiş Dönem Net Kar:**", value=None, placeholder="Geçmiş Dönem Net Kar tutarını bu alana yazın")
      
      #else:
          #st.write("Hesaplama Yapılamadı")
      #elif islem_1 == " Gelecek Net Kar Tahmini Miktarı":
          # Ensure both c7 and c24 have valid numerical values before calculation
          #if c7 is not None and c24 is not None:
              #c26 = c7 + (c7 - c24)  # Calculate the future equity amount
              #st.write(f"**Gelecek Net Kar Tahmini Miktarı:** {c26}")
          #else:
              #st.write("Hesaplama için Güncel Net Kar ve Geçmiş Dönem Net Kar tutarlarını giriniz.")
      #else:
          #st.write("Hesaplama Yapılamadı")
      
  #with sidebar:
  
  
     
      #if operation == "ORTALAMA HEDEF FİYAT":
      #st.write(ortalama_hesap)
      #if ortalama_hesap < kapanıs :
        #st.write(f":blue[**TÜM HESAPLAMALARIN ORTALAMA FİYATI:**] {ortalama_hesap:,.2f}")
      #else :
        #st.write(f"**TÜM HESAPLAMALARIN ORTALAMA FİYATI:** :green[{ortalama_hesap:,.2f}]")
      #elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
    
    #c22 = st.number_input(f"**Geçmiş Dönem Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın") #{float(ozkaynaklar1):,.0f}")
    #c22 = float((ozkaynaklar_2).replace(",", "."))
    #st.write("Gelecek Özkaynak Tahmini Miktarı", c22)
    #islem_1 = st.selectbox("Gelecek Özkaynak Tahmini Miktarı:", ["Gelecek Özkaynak Tahmini Miktarı"])
    #if islem_1 == "Gelecek Özkaynak Tahmini Miktarı":
      #c25 = c8-c22+c8
      #st.write(f"**Gelecek Özkaynak Tahmini Miktarı:** {c25}")
    #else:
      #st.write("Hesaplama Yapılamadı")  
  
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
  
    st.subheader(":one:**:blue[HİSSE VERİLERİ]**", divider='red')
    
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
            st.write(f"**ÖDENMİŞ SERMAYE(Bir Önceki Çeyrek):**  {float(OdenmisSermaye_2):,.0f}")         
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
    st.subheader(":two:**HİSSE HEDEF FİYAT HESAPLAYICI**", divider='red')
  
    #operation = st.selectbox(":blue[**GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI:**]", ["GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI"])
  
    #operation = st.selectbox(":blue[**HİSSE FİYAT HESAPLAMARI İÇİN İŞLEM SEÇİN:**]", ["İŞLEM SEÇİN", "GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI", "BİR ÇEYREK SONRAKİ HEDEF FİYATI TAHMİNİ", "1 YIL SONRAKİ HİSSE HEDEF FİYATI TAHMİNİ", "1. Çeyrek Bilanço Hisse Oranları-3 Aylık", "2. Çeyrek Bilanço Hisse Oranları-6 Aylık", "3. Çeyrek Bilanço Hisse Oranları-9 Aylık", "4. Çeyrek Bilanço Hisse Oranları-12 Aylık"])
    #if operation == "Tüm Hedef Fiyatları Göster":
    operation = "GÜNCEL BİLANÇOYA GÖRE HİSSE FİYATI"
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
      #st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
      st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
      #st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
      st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
      #st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
      #st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
      #st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
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
      #st.write(f":blue[**Potansiyel Piyasa Değerine Göre Olması Gereken Fiyat:**] { potansiyel_fiyat :,.2f}")    
      st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
      #st.write(f":blue[**YILSONU TAHMİNİ F/K HEDEF FİYATI:**] {future_fk:,.2f}")
      st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
      #st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
      #st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
      #st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
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

elif page == "TEKNİK ANALİZ":
 st.markdown("""hazırlanıyor...""")
 button=st.button("Analiz")
 if button==True:
     with st.spinner("Lütfen Bekleyin..."):


elif page == "HAKKINDA":

 st.markdown("""Developed By ***Hidayet YAKUPOGLU*** v1.0 2024 ***""")
 link = 'https://www.linkedin.com/in/hidayet-yakupo%C4%9Flu-35122a2b/'
 st.write(link)
 st.markdown("""Contact: hidayetyakupoglu@gmail.com""")
    #if __name__ == "__main__":
    #  st.run()


#!streamlit run deneme.py & npx localtunnel --port 8501
