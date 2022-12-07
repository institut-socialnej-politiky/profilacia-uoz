# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
# pickle musi byt ako import, ale nie ako requirement, lebo je obsiahnuty 
# priamo v tom python backgrounge co bezi na git hube
import pickle 

# naopak lightgbm musi byt v requirements, ale nie ako import
import streamlit as st

# pridam obrazok
from PIL import Image

# otvorenie
image = Image.open('isp_pic2.PNG')

st.image(image)

# nacitam si pomocny subor na kategorizaciu okresov
df_okresy = pd.read_csv("okresy_avg_2021.csv")
df_odbory = pd.read_csv("odbory.csv")
# nacitam uoz testovacie data 
df = pd.read_csv('data_uoz.csv', sep = ',', encoding='utf-8', decimal='.')

st.title("Ukážka profilácie UoZ pomocou strojového učenia")
st.write("Inštitút sociálnej politiky MPSVR SR Vám prináša alfa-verziu online nástroja umožňujúceho profiláciu UoZ. "
         "Tento nástroj vyhodnocuje mieru rizika dlhodobého zotrvania UoZ mimo trhu práce. "
         "Do online dotazníka, prosím, zadajte charakteristiky fiktívneho uchádzača. "
         "Nebojte sa experimentovať s charakteristikami! "
         "Odskúšaním rôznych kombinácií charakteristík nám pomáhate v zlepšovaní tohto nástroja. "
         "Po kliknutí na tlačidlo „Spustiť profiláciu“ sa Vám zjaví odhad pravdepodobnosti, "
         "že si Vami opísaný fiktívny UoZ nenájde uplatnenie na trhu práce do 12 mesiacov od registrácie na úrade práce.")

st.write("Ďakujeme Vám a tešíme sa na Vaše podnety.") 
         
st.write("Váš Inštitút sociálnej politiky")

st.write("----------------------------------------------------------")

# volby pohlavia
pohlavia = ("Muž", "Žena")
pohl = st.selectbox("Pohlavie:", pohlavia)
if pohl == 'Žena':
    pohl_zena = 1
else:
    pohl_zena = 0

# volba veku
vek = st.slider("Vek", 15, 70, 35)

# okres trvaleho bydliska
okresy = ('Bratislava I', 'Bratislava II', 'Bratislava III', 'Bratislava IV', 'Bratislava V', 
          'Malacky', 'Pezinok', 'Senec', 'Dunajská Streda', 'Galanta', 'Hlohovec', 'Piešťany', 
          'Senica', 'Skalica', 'Trnava', 'Bánovce nad Bebravou', 'Ilava', 'Myjava', 
          'Nové Mesto nad Váhom', 'Partizánske', 'Považská Bystrica', 'Prievidza', 
          'Púchov', 'Trenčín', 'Komárno', 'Levice', 'Nitra', 'Nové Zámky', 'Šaľa', 
          'Topoľčany', 'Zlaté Moravce', 'Bytča', 'Čadca', 'Dolný Kubín', 'Kysucké Nové Mesto',
          'Liptovský Mikuláš', 'Martin', 'Námestovo', 'Ružomberok', 'Turčianske Teplice',
          'Tvrdošín', 'Žilina', 'Banská Bystrica', 'Banská Štiavnica', 'Brezno', 'Detva',
          'Krupina', 'Lučenec', 'Poltár', 'Revúca', 'Rimavská Sobota', 'Veľký Krtíš',
          'Zvolen', 'Žarnovica', 'Žiar nad Hronom', 'Bardejov', 'Humenné', 'Kežmarok', 
          'Levoča', 'Medzilaborce', 'Poprad', 'Prešov', 'Sabinov', 'Snina', 'Stará Ľubovňa', 
          'Stropkov', 'Svidník', 'Vranov nad Topľou', 'Gelnica', 'Košice I', 'Košice II', 
          'Košice III', 'Košice IV', 'Košice - okolie', 'Michalovce', 'Rožňava', 'Sobrance', 
          'Spišská Nová Ves', 'Trebišov')
trv_byd = st.selectbox("Okres trvalého pobytu:", okresy)

trv_bydlisko = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'kraj2'].values[0]

# najvysie dosiahnute vzdelanie
vzdelanie_stupen = ('Neznáme',
                    'Neukončené základné vzdelanie', 
                    'Základné vzdelanie', 
                    'Nižšie stredné odborné vzdelanie',
                    'Stredné odborné vzdelanie',  
                    'Úplné stredné odborné vzdelanie',
                    'Úplné stredné všeobecné vzdelanie', 
                    'Vyššie odborné vzdelanie',
                    'Vysokoškolské vzdelanie prvého stupňa',
                    'Vysokoškolské vzdelanie druhého stupňa',
                    'Vysokoškolské vzdelanie tretieho stupňa',
                    )
naj_vzde = st.selectbox("Najvyššie dosiahnuté vzdelanie:", vzdelanie_stupen)

stredoskolske_nizke = ('Nižšie stredné odborné vzdelanie', 
                       'Stredné odborné vzdelanie')
stredoskolske_uplne = ('Úplné stredné odborné vzdelanie', 
                       'Úplné stredné všeobecné vzdelanie',
                       'Vyššie odborné vzdelanie') 
vysokoskolske = ('Vysokoškolské vzdelanie prvého stupňa', 
                 'Vysokoškolské vzdelanie druhého stupňa',
                 'Vysokoškolské vzdelanie tretieho stupňa')

if naj_vzde == 'Základné vzdelanie':
    vzdelanie = 'zakladne'
elif naj_vzde in stredoskolske_nizke:
    vzdelanie = 'stredne_nizsie'
elif naj_vzde in stredoskolske_uplne:
    vzdelanie = 'stredne_uplne'
elif naj_vzde in vysokoskolske:
    vzdelanie = 'vysokoskolske'
else:
    vzdelanie = 'ziadne'

# typ dosiahnuteho vzdelania
odbory = df_odbory['nazov_kod']
odbor = st.selectbox("Odbor najvyššieho dosiahnutého vzdelania:", odbory)  

skola_odbor = df_odbory.loc[df_odbory['nazov_kod'] == odbor, 'skola_odbor_skupina'].values[0] 

# ci ma alebo nema titul
if skola_odbor == 'ziadny':
    ma_titul = 0
else:
    ma_titul = 1

# rodinny stav
stavy = ("Slobodný, slobodná", "Ženatý, vydatá", "Rozvedený, rozvedená", "Vdovec, vdova", 
         "Registrované partnerstvo")

stav = st.selectbox("Rodinný stav:", stavy)

if stav == "Slobodný, slobodná":
    rodinny_stav = "slobodny"
elif (stav == "Ženatý, vydatá" or stav == "Registrované partnerstvo"):
    rodinny_stav =  "zavazok"
elif  stav == "Rozvedený, rozvedená":
    rodinny_stav = 'rozvedeny'
else:
    rodinny_stav= 'Vdovec'
# vodicak
vodicak = st.selectbox('Vodičský preukaz skupiny A, A1, A2, AM, B alebo B1:', ['Áno', 'Nie'])
if vodicak == 'Áno':
    vodicak_zakl = 1
else:
    vodicak_zakl = 0

# uroven Aj
jazyk_aj = st.selectbox('Úroveň anglického jazyka:', 
                        ['Žiadna', 'Elementárna - A1 alebo A2', 
                         'Pokročilá - B1 alebo B2','Vysoká - C1 alebo c2 '])
if jazyk_aj == 'Žiadna':
    jazyk_en = 0
elif jazyk_aj == 'Elementárna - A1 alebo A2':
    jazyk_en = .33
elif jazyk_aj == 'Pokročilá - B1 alebo B2':
    jazyk_en = .66
else:
    jazyk_en = 1

# uroven DE
jazyk_nem = st.selectbox('Úroveň nemeckého jazyka:', 
                        ['Žiadna', 'Elementárna - A1 alebo A2', 
                         'Pokročilá - B1 alebo B2','Vysoká - C1 alebo c2 '])
if jazyk_nem == 'Žiadna':
    jazyk_de = 0
elif jazyk_nem == 'Elementárna - A1 alebo A2':
    jazyk_de = .33
elif jazyk_nem == 'Pokročilá - B1 alebo B2':
    jazyk_de = .66
else:
    jazyk_de = 1

# mesiac zaradenia do evidencie
mes_zaradenia = st.slider('Mesiac zaradenia do evidencie UoZ:', 1, 12, 1)

# pred zaradenim do evidencie
postavenie_pred = st.selectbox('Postavenie bezprostredne pred zaradením do evidencie UoZ:', 
                    ['Pracujúci', 'Študent', 'Opatrujúci dieťa alebo blízku osobu', 
                     'Inak poistená osoba (poberateľ dôchodku, práceneschopný...)', 'Nezamestnaný'])

if postavenie_pred == 'Pracujúci':
    dov_zaradenia = 'pracujuci'
elif postavenie_pred == 'Študent':
    dov_zaradenia = 'absolventi'
elif postavenie_pred == 'Opatrujúci dieťa alebo blízku osobu':
    dov_zaradenia = 'opatrujuci'
elif postavenie_pred == 'Inak poistená osoba (poberateľ dôchodku, práceneschopný...)':
    dov_zaradenia = 'inak_poisteni'
else :
    dov_zaradenia = 'nezamestnani'
    
# prechadzajuce zamestnanie podla NACE
nace_pred = st.selectbox('V akom odvetví pracoval UoZ naposledy?', 
                         ['Neznáme',
                          'A – Poľnohospodárstvo, lesníctvo a rybolov', 
                          'B – Ťažba a dobývanie', 
                          'C – Priemyselná výroba',
                          'D – Dodávka elektriny, plynu, pary a studeného vzduchu',
                          'E – Dodávka vody, čistenie a odvod odpadových vôd, odpady a služby odstraňovania odpadov',
                          'F – Stavebníctvo',
                          'G – Veľkoobchod a maloobchod; oprava motorových vozidiel a motocyklov',
                          'H – Doprava a skladovanie',
                          'I – Ubytovacie a stravovacie služby',
                          'J – Informácie a komunikácia',
                          'K – Finančné a poisťovacie činnosti',
                          'L – Činnosti v oblasti nehnuteľností',
                          'M – Odborné, vedecké a technické činnosti',
                          'N – Administratívne a podporné služby',
                          'O – Verejná správa a obrana; povinné sociálne zabezpečenie',
                          'P – Vzdelávanie',
                          'Q – Zdravotníctvo a sociálna pomoc',
                          'R – Umenie, zábava a rekreácia',
                          'S – Ostatné činnosti',
                          'T – Činnosti domácností ako zamestnávateľov',
                          'U – Činnosti extrateritoriálnych organizácií a združení'],
                         help = 'Pre viac informácii navštívte http://www.nace.sk/')
odvetvia = ('A+B', 'C', 'D+E+F', 'G', 'H', 'I', 'J+K+L', 
            'M', 'N', 'O', 'P', 'Q', 'R+S+T+U', 'nezname')

# vela skaredych podmienok, aby som to prerobil na vstupy
if 'A –' or 'B –' in nace_pred:
    predch_zam_nace = 'A+B'

if 'C –' in nace_pred:
    predch_zam_nace = 'C'

if 'D –' or 'E –' or 'F –' in nace_pred:
    predch_zam_nace = 'D+E+F'

if 'G –' in nace_pred:
    predch_zam_nace = 'G'

if 'H –' in nace_pred:
    predch_zam_nace = 'H'
    
if 'I –' in nace_pred:
    predch_zam_nace = 'I'

if 'J –' or 'K –' or 'L –' in nace_pred:
    predch_zam_nace = 'J+K+L'

if 'M –' in nace_pred:
    predch_zam_nace = 'M'
    
if 'N –' in nace_pred:
    predch_zam_nace = 'N'

if 'O –' in nace_pred:
    predch_zam_nace = 'O'

if 'P –' in nace_pred:
    predch_zam_nace = 'P'

if 'Q –' in nace_pred:
    predch_zam_nace = 'Q'
    
if 'R –' or 'S –' or 'T –' or 'U –' in nace_pred:
    predch_zam_nace = 'R+S+T+U'
    
if nace_pred == 'Neznáme':
    predch_zam_nace = 'nezname'

# prechadchadzajuce zamestnanie podla ISCO
isco_pr = st.selectbox('Naposledy vykonávaná profesia:', 
                       ['Neznáme',
                       '0 Ozbrojené sily',
                       '1 Zákonodarcovia',
                       '2 Špecialisti',
                       '3 Odborní pracovníci',
                       '4 Administratívni pracovníci',
                       '5 Služby a obchod',
                       '6 Poľnohospodári',
                       '7 Remeselníci',
                       '8 Operátori',
                       '9 Nekvalifikovaní pracovníci'])

if isco_pr == '0 Ozbrojené sily':
    isco_pred = '0_ozbrojene_sily'
elif isco_pr == '1 Zákonodarcovia':
    isco_pred = '1_zakonodarcovia'
elif isco_pr == '2 Špecialisti':
    isco_pred = '2_specialisti'
elif isco_pr == '3 Odborní pracovníci':
    isco_pred = '3_odb_pracovnici'
elif isco_pr == '4 Administratívni pracovníci':
    isco_pred = '4_adm_pracovnici'
elif isco_pr == '5 Služby a obchod':
    isco_pred = '5_sluzby_obchod'
elif isco_pr == '6 Poľnohospodári':
    isco_pred = '6_polnohosp'
elif isco_pr == '7 Remeselníci':
    isco_pred = '7_remeselnici'
elif isco_pr == '8 Pperátori':
    isco_pred = '8_operatori'
elif isco_pr == '9 Nekvalifikovaní pracovníci':
    isco_pred = '9_nekval_prac'
else:
    isco_pred ='nezname'

predch_zam_isco = isco_pred

isco_pr_hlzam = st.selectbox('Má UoZ záujem pracovať v konkrétnej profesii?', 
                             ['Nie',
                              '0 Ozbrojené sily',
                              '1 Zákonodarcovia',
                              '2 Špecialisti',
                              '3 Odborní pracovníci',
                              '4 Administratívni pracovníci',
                              '5 Služby a obchod',
                              '6 Poľnohospodári',
                              '7 Remeselníci',
                              '8 Operátori',
                              '9 Nekvalifikovaní pracovníci'])

# skarede if struktury na definovanie hlzam kodov
if isco_pr_hlzam == '2 Špecialisti':
    hlzam_sp_isco_5 = 0
    hlzam_sp_isco_9 = 0
    hlzam_bp_isco_2 = 0.085
    hlzam_bp_isco_4 = 0
    hlzam_bp_isco_8 = 0
    hlzam_bp_isco_9 = 0 
elif isco_pr_hlzam == '4 Administratívni pracovníci':
    hlzam_sp_isco_5 = 0
    hlzam_sp_isco_9 = 0
    hlzam_bp_isco_2 = 0
    hlzam_bp_isco_4 = 0.073
    hlzam_bp_isco_8 = 0
    hlzam_bp_isco_9 = 0
elif isco_pr_hlzam == '5 Služby a obchod':
    hlzam_sp_isco_5 = 0.105
    hlzam_sp_isco_9 = 0
    hlzam_bp_isco_2 = 0
    hlzam_bp_isco_4 = 0
    hlzam_bp_isco_8 = 0
    hlzam_bp_isco_9 = 0
elif isco_pr_hlzam == '8 Operátori':
    hlzam_sp_isco_5 = 0
    hlzam_sp_isco_9 = 0
    hlzam_bp_isco_2 = 0
    hlzam_bp_isco_4 = 0
    hlzam_bp_isco_8 = 0.436
    hlzam_bp_isco_9 = 0
elif isco_pr_hlzam == '9 Operátori':
    hlzam_sp_isco_5 = 0
    hlzam_sp_isco_9 = 0.086
    hlzam_bp_isco_2 = 0
    hlzam_bp_isco_4 = 0
    hlzam_bp_isco_8 = 0
    hlzam_bp_isco_9 = 0.081
else:
    hlzam_sp_isco_5 = 0
    hlzam_sp_isco_9 = 0
    hlzam_bp_isco_2 = 0
    hlzam_bp_isco_4 = 0
    hlzam_bp_isco_8 = 0
    hlzam_bp_isco_9 = 0
# pocet evidovanie ako UoZ za posl 24 mesiacov
predch_ev_pocet = st.slider('Počet evidencii ako UoZ za posledných 24 mesiacov:', 0, 10, 0)

# pocet mesiacov evidovani ako UoZ za posl 24 mesiacov
predch_ev_roky = st.slider('Počet mesiacov evidovaný ako UoZ za posledných 24 mesiacov:', 0, 24, 0)

# bol niekedy v minulosti dobrovolne nezamestnany
dob_nez = st.selectbox('V minulosti dobrovoľne nezamestnaný:', ['Áno', 'Nie'])

if dob_nez == 'Áno':
    dobr_nezam = 1
else:
    dobr_nezam = 0

# ci ma zaujem ist pracovat do zahranicia
zahranicie = st.selectbox('Plány odísť do zahraničia:', ['Áno', 'Nie'])

if zahranicie == 'Áno':
    umysel_do_zahr = 1
else:
    umysel_do_zahr = 0
    
# pocet zaujmov
zaujmy = st.multiselect('UoZ by mal v budúcnosti záujem:', 
                        ['pracovať aj mimo územia SR', 'pracovať aj na skrátený úväzok', 
                        'vykonávať SZČ', 'dochádzať do zamestnania', 'o vzdelávanie', 
                        'vykonávať absolventskú prax', 'ďalej študovať dennou formou'], help = 'môžnosť zvoliť viacero možností alebo žiadnu')
pocet_zaujmov = len(zaujmy)
    
# pocet znevyhodneni a z toho potrebne binarne premenne
znevyhodnenia = st.multiselect('Znevýhodnenia:', 
                               ['má menej ako 26 rokov a ukončil štúdium pred menej ako 2 rokmi a nemal odvtedy pravidelne platené zamestnanie',
                                'najmenej 12 predchádzajúcich mesiacov nemal pravidelne platené zamestnanie',
                                'je štátny príslušník tretej krajiny, ktorému bol udelený azyl',
                                'žije ako osamelá dospelá osoba s jednou alebo viacerými osobami odkázanými na jeho/jej starostlivosť',
                                'má zdravotné postihnutie'], help = 'môžnosť zvoliť viacero možností alebo žiadnu')

# znevyhodneny bez pravidelneho zamestnania
if 'najmenej 12 predchádzajúcich mesiacov nemal pravidelne platené zamestnanie' in znevyhodnenia:
    znevyh_bez_pravid_zam = 1
else:
    znevyh_bez_pravid_zam = 0

# znevyhodneny absolvent
if 'má menej ako 26 rokov a ukončil štúdium pred menej ako 2 rokmi a nemal odvtedy pravidelne platené zamestnanie' in znevyhodnenia:
    znevyh_absolvent = 1
else:
    znevyh_absolvent = 0

# znevyhodneny nizkym vzdelanim
if vzdelanie == 'zakladne' or vzdelanie == 'stredne_nizsie' or vzdelanie == 'ziadne':
    znevyh_nizke_vzd = 1
    znevyh_pocet = len(znevyhodnenia) + 1
else:
    znevyh_nizke_vzd = 0
    znevyh_pocet = len(znevyhodnenia)
    
# znevyhodneny vekom   
if vek >= 50:
    znevyh_pocet = znevyh_pocet + 1

# dlzka praxe v rokoch
dobaprax = st.slider('Prax UoZ na trhu práce v rokoch:', 0, 70, 10)

# poberanie davky v hmotnej nudzi
davka_v_nudzi = st.selectbox('Poberá UoZ dávku v hmotnej núdzi?', ['Nie', 'Áno'])

if davka_v_nudzi == 'Áno':
    dhn = 1
else:
    dhn = 0

# dlzka aktivnych opatreni na trhu prace
aotp_cas_za_2r = st.slider('Koľko z predchádzajúcich 24 mesiacov strávil UoZ aktívnymi opatreniami na trhu práce?',
                           0, 24, 0)

# nezamestnanost 
nezam_celk = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'nezam_celk'].values[0]
nezam_odch = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'nezam_odch'].values[0]

# vpm
vpm = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'vpm'].values[0]

# priemerny hruby vymeriavaci zaklad
vz_zec = st.slider('Priemerná hrubá mzda (v eurách) za posledné dva roky:', 0, 2000, 0, 
                   help = 'v prípade, že hrubá mzda bola viac ako 2000 eur, zvoľte 2000')

# priemerny prijem z dohod
vz_doh = st.slider('Priemerný mesačný príjem (v eurách) z práce na dohody za posledné dva roky:', 0, 2000, 0)

# dlzka zamestnanosti v mesiacoch 2 roky pred zaredenim
dlzka_zec = st.slider('Koľko z posledných 24 mesiacov bol UoZ zamestnaný?', 0, 24, 0)

# dlzka dohody v mesiacoch 2 roky pred zaredenim
dlzka_doh = st.slider('Koľko z posledných 24 mesiacov bol UoZ zamestnaný ako dohodár?', 0, 24, 0)

# dlzka meterskej v mesiacoch 2 roky pred zaredenim
dlzka_dieta = st.slider('Koľko z posledných 24 mesiacov strávil UoZ na materskej alebo rodičovskej dovolenke?', 0, 24, 0)
  

# kontrola premennych, vytvori button ktory ked sa stlaci, tak to bude OK
# ok = st.button("Stlac pre kontrolu premennych")

# if ok:
#     st.subheader("1 Vek: " + str(vek))
#     st.subheader("2 Pohlavie zena: " + str(pohl_zena))
#     st.subheader("3 Trvale bydlisko: " + str(trv_bydlisko))
#     st.subheader("4 Najvyssie vzdelanie: " + str(vzdelanie))
#     st.subheader("5 Vystudovany odbor: " + str(skola_odbor))
#     st.subheader("6 Ma titul: " + str(ma_titul))
#     st.subheader("7 Rodinny stav: " + str(rodinny_stav))
#     st.subheader("8 Vodicak zakladny: " + str(vodicak_zakl))
#     st.subheader("9 Uroven Aj: " + str(jazyk_en))
#     st.subheader("10 Uroven Nem: " + str(jazyk_de))
#     st.subheader("11 Mesiac Zaradenia do evidencie: " + str(mes_zaradenia))
#     st.subheader("12 Co robil tesne pred zaradenim do evidencie: " + str(dov_zaradenia))
#     st.subheader("13 Predchadzajuce zamestnanie NACE: " + str(predch_zam_nace))
#     st.subheader("14 Predchadzajuce zamestnanie ISCO: " + str(predch_zam_isco))
#     st.subheader("15 Pocet evidencii UoZ za posl 24 mes: " + str(predch_ev_pocet))
#     st.subheader("16 Pocet mesiacov ako evidovany UoZ za posl 24 mes: " + str(predch_ev_roky))
#     st.subheader("17 Dobrovolna nezamestnanost v minulosti: " + str(dobr_nezam))
#     st.subheader("18 Umysel ist do zahranicia: " + str(umysel_do_zahr)) 
#     st.subheader("19 Pocet zaujmov ako ci moze dochadzat, vzdelavat sa: " + str(pocet_zaujmov))
#     st.subheader("20 Znevyhodneny student: " + str(znevyh_absolvent))
#     st.subheader("21 Znevyhodneny bez pravidelneho zam: " + str(znevyh_bez_pravid_zam))
#     st.subheader("22 Znevyhodneny kvoli nizkemu vzdelaniu: " + str(znevyh_nizke_vzd))
#     st.subheader("23 Znevyhodnenia pocet: " + str(znevyh_pocet))
#     st.subheader("24 Prax v rokoch: " + str(dobaprax))
#     st.subheader("25 Hlzam isco 5: " + str(hlzam_sp_isco_5))
#     st.subheader("26 Hlzam isco 9: " + str(hlzam_sp_isco_9))
#     st.subheader("27 Hlzam isco 2: " + str(hlzam_bp_isco_2))
#     st.subheader("28 Hlzam isco 4: " + str(hlzam_bp_isco_4))
#     st.subheader("29 Hlzam isco 8: " + str(hlzam_bp_isco_8))
#     st.subheader("30 Hlzam isco 9: " + str(hlzam_bp_isco_9))
#     st.subheader("31 Poberanie davky v hmotnej nudzi: " + str(dhn))
#     st.subheader("32 Aktivne opatrenia na trhu prace za posl 2 roky, dlzka v mes: " + str(aotp_cas_za_2r))
#     st.subheader("33 Nezam celkova v okrese trvaleho byd: " + str(nezam_celk))
#     st.subheader("34 Nezam odchylka v okrese trvaleho byd od SVK: " + str(nezam_odch))
#     st.subheader("35 Podiel voľných pracovných miest v okrese: " + str(vpm))
#     st.subheader("36 Priemerna vyska hrubej mzdy za posledne dva roky: " + str(vz_zec))
#     st.subheader("37 Priemerna vyska prace na dohodu za posledne dva roky: " + str(vz_doh))
#     st.subheader("38 Dlzka zamestnanosti v mesiacoch: " + str(dlzka_zec))
#     st.subheader("39 Dlzka zamestnanosti na dododu v mesiacoch: " + str(dlzka_doh))
#     st.subheader("40 Dlzka materskej pred zaredenim v mesiacoch: " + str(dlzka_dieta))
    
ok2 = st.button("Spustiť profiláciu")

#nacitam svoje premenne
if ok2:
    df_my = {'vek' : vek,
       'pohl_zena' : pohl_zena,
       'trv_bydlisko' : trv_bydlisko,
       'vzdelanie' : vzdelanie,
       'skola_odbor' : skola_odbor,
       'ma_titul' : ma_titul,
       'rodinny_stav' : rodinny_stav,
       'vodicak_zakl' : vodicak_zakl,
       'jazyk_en' : jazyk_en,
       'jazyk_de': jazyk_de,
       'mes_zaradenia' : mes_zaradenia,
       'dov_zaradenia' : dov_zaradenia,
       'predch_zam_nace' : predch_zam_nace,
       'predch_zam_isco' : predch_zam_isco,
       'predch_ev_pocet' : predch_ev_pocet,
       'predch_ev_roky' : predch_ev_roky,
       'dobr_nezam' : dobr_nezam,
       'umysel_do_zahr' : umysel_do_zahr,
       'pocet_zaujmov' : pocet_zaujmov,
       'znevyh_absolvent' : znevyh_absolvent,
       'znevyh_bez_pravid_zam' : znevyh_bez_pravid_zam,
       'znevyh_nizke_vzd' : znevyh_nizke_vzd,
       'znevyh_pocet' : znevyh_pocet,
       'dobaprax' : dobaprax,
       'hlzam_sp_isco_5' : hlzam_sp_isco_5,
       'hlzam_sp_isco_9' : hlzam_sp_isco_9,
       'hlzam_bp_isco_2' : hlzam_bp_isco_2,
       'hlzam_bp_isco_4' : hlzam_bp_isco_4,
       'hlzam_bp_isco_8' : hlzam_bp_isco_4,
       'hlzam_bp_isco_9' : hlzam_bp_isco_9,
       'dhn' : dhn,
       'aotp_cas_za_2r' : aotp_cas_za_2r,
       'nezam_celk' : nezam_celk,
       'nezam_odch' : nezam_odch,
       'vpm' : vpm,
       'vz_zec' : vz_zec,
       'vz_doh' : vz_doh,
       'dlzka_zec' : dlzka_zec,
       'dlzka_doh' : dlzka_doh,
       'dlzka_dieta' : dlzka_dieta}
    # pripojim do dataframe
    df = df.append(df_my, ignore_index = True)
    # nazvy kategorickych, binarnych a numerickych premennych
    vars_cat = df.loc[:,['trv_bydlisko', 'vzdelanie', 'skola_odbor', 'rodinny_stav', 'dov_zaradenia', 'predch_zam_nace', 
                          'predch_zam_isco', 'mes_zaradenia']].columns.tolist()
    vars_bin = df.loc[:,['pohl_zena', 'ma_titul', 'vodicak_zakl', 'dobr_nezam', 'umysel_do_zahr', 'znevyh_absolvent', 
                          'znevyh_bez_pravid_zam', 'znevyh_nizke_vzd', 'dhn', ]].columns.tolist()
    vars_num = df.loc[:,['vek', 'jazyk_en', 'jazyk_de', 'predch_ev_pocet', 'predch_ev_roky', 
                          'pocet_zaujmov','znevyh_pocet', 'dobaprax', 'hlzam_sp_isco_5', 'hlzam_sp_isco_9', 
                          'hlzam_bp_isco_2', 'hlzam_bp_isco_4', 'hlzam_bp_isco_8', 'hlzam_bp_isco_9', 'aotp_cas_za_2r', 
        'nezam_celk', 'nezam_odch', 'vpm', 'vz_zec', 'vz_doh', 'dlzka_zec', 'dlzka_doh', 'dlzka_dieta']].columns.tolist()
    # zoradit podla abecedy
    vars_cat.sort()
    vars_bin.sort()
    vars_num.sort()

    # vysvetlujuce premenne
    X = pd.concat([df[vars_cat].astype('category'),
                    df[vars_bin],
                    df[vars_num]], axis = 1)

    # najdolezitejsie premenne z celkoveho modelu
    X = X[['dov_zaradenia', 'vzdelanie', 'nezam_celk', 'vz_zec', 'dlzka_zec', 
            'znevyh_nizke_vzd', 'predch_ev_pocet', 'trv_bydlisko', 'predch_zam_nace', 'vodicak_zakl',
        'hlzam_bp_isco_9', 'pohl_zena', 'vek', 'jazyk_en', 'vz_doh', 
        'predch_ev_roky', 'mes_zaradenia', 'predch_zam_isco', 'rodinny_stav', 'umysel_do_zahr', 
        'ma_titul', 'vpm', 'hlzam_bp_isco_2', 'znevyh_bez_pravid_zam', 'dlzka_doh', 
        'dhn', 'jazyk_de', 'dobr_nezam', 'aotp_cas_za_2r', 'hlzam_sp_isco_5', 
        'nezam_odch','hlzam_bp_isco_8', 'znevyh_absolvent', 'znevyh_pocet', 'dlzka_dieta',
        'pocet_zaujmov', 'skola_odbor', 'hlzam_bp_isco_4', 'dobaprax', 'hlzam_sp_isco_9'
        ]]
    # najprv kategoricke, potom numericke
    X = pd.concat([X.select_dtypes(include = 'category'),
                   X.select_dtypes(exclude = 'category')],
                  axis = 1)

    # %% load saved model
    with open('LightGBM_reduced.pkl', 'rb') as f:
            lgbcl = pickle.load(f)  

    # predict probabilities on test set
    probs = lgbcl.predict_proba(X)[:,1]
    st.subheader("Pravdepodobnosť, že UoZ s definovanými charakteristikami sa po 1 roku neuplatní na trhu práce je: " + str('{:.2f}'.format(probs[-1]*100)) + " %")





