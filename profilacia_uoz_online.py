# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import pickle

# nacitam si pomocny subor na kategorizaciu okresov
df_okresy = pd.read_csv("okresy.csv")
df_odbory = pd.read_csv("odbory.csv")
# nacitam uoz testovacie data 
df = pd.read_csv('data_uoz.csv', sep = ',', encoding='utf-8', decimal='.')

st.title("Profilácia UoZ (alfa verzia)")
st.write("### Prosím vyplnťe dotazník ###")

# volby pohlavia
pohlavia = ('', "muž", "žena")
pohl = st.selectbox("Pohlavie", pohlavia)
if pohl == 'žena':
    pohl_zena = 1
else:
    pohl_zena = 0

# volba veku
vek = st.slider("Prosím zvoľte Váš vek", 0, 100, 1)

# okres trvaleho bydliska
okresy = ('Bratislava I', 'Bratislava II', 'Bratislava III', 'Bratislava IV', 'Bratislava V', 
          'Malacky ', 'Pezinok', 'Senec', 'Dunajská Streda ', 'Galanta', 'Hlohovec', 'Piešťany', 
          'Senica', 'Skalica', 'Trnava', 'Bánovce nad Bebravou', 'Ilava', 'Myjava', 
          'Nové Mesto nad Váhom', 'Partizánske', 'Považská Bystrica', 'Prievidza', 
          'Púchov', 'Trenčín', 'Komárno', 'Levice', 'Nitra ', 'Nové Zámky', 'Šaľa', 
          'Topoľčany', 'Zlaté Moravce', 'Bytča', 'Čadca', 'Dolný Kubín', 'Kysucké Nové Mesto',
          'Liptovský Mikuláš', 'Martin', 'Námestovo', 'Ružomberok', 'Turčianske Teplice',
          'Tvrdošín', 'Žilina', 'Banská Bystrica', 'Banská Štiavnica', 'Brezno', 'Detva',
          'Krupina', 'Lučenec', 'Poltár', 'Revúca', 'Rimavská Sobota', 'Veľký Krtíš',
          'Zvolen', 'Žarnovica', 'Žiar nad Hronom', 'Bardejov', 'Humenné', 'Kežmarok', 
          'Levoča', 'Medzilaborce', 'Poprad', 'Prešov', 'Sabinov', 'Snina', 'Stará Ľubovňa', 
          'Stropkov', 'Svidník', 'Vranov nad Topľou', 'Gelnica', 'Košice I', 'Košice II', 
          'Košice III', 'Košice IV', 'Košice - okolie', 'Michalovce', 'Rožňava', 'Sobrance', 
          'Spišská Nová Ves', 'Trebišov')
trv_byd = st.selectbox("Trvalé bydlisko", okresy)

trv_bydlisko = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'kraj2'].values[0]

# najvysie dosiahnute vzdelanie
vzdelanie_stupen = ( 'žiadne', 'základoškolské', 'nižsie stredoškolské',  'úplné stredoškolské',  'vysokoškolské')
naj_vzde = st.selectbox("Najvyššie dosiahnuté vzdelanie", vzdelanie_stupen)

if naj_vzde == 'základoškolské':
    vzdelanie = 'zakladne'
elif naj_vzde == 'nižsie stredoškolské':
    vzdelanie = 'stredne_nizsie'
elif naj_vzde == 'úplné stredoškolské':
    vzdelanie = 'stredne_uplne'
elif naj_vzde == 'vysokoškolské':
    vzdelanie = 'vysokoskolske'
else:
    vzdelanie = 'ziadne'

# typ dosiahnuteho vzdelania
odbory = df_odbory['nazov_kod']
odbor = st.selectbox("V akom odbore ste dosiahli najvyššie vzdelanie?", odbory)  

skola_odbor = df_odbory.loc[df_odbory['nazov_kod'] == odbor, 'skola_odbor_skupina'].values[0] 

# ci ma alebo nema titul
if skola_odbor == 'ziadny':
    ma_titul = 0
else:
    ma_titul = 1

# rodinny stav
stavy = ("slobodný, slobodná", "ženatý, vydatá", "rozvedený, rozvedená", "vdovec, vdova", 
         "registrované partnerstvo")

stav = st.selectbox("Aký je Váš rodinný stav?", stavy)

if stav == "slobodný, slobodná":
    rodinny_stav = "slobodny"
elif (stav == "ženatý, vydatá" or stav == "registrované partnerstvo"):
    rodinny_stav =  "zavazok"
elif  stav == "rozvedený, rozvedená":
    rodinny_stav = 'rozvedeny'
else:
    rodinny_stav= 'vdovec'
# vodicak
vodicak = st.selectbox('Máte vodičský preukaz skupiny A, A1, A2, AM, B alebo B1?', ['áno', 'nie'])
if vodicak == 'áno':
    vodicak_zakl = 1
else:
    vodicak_zakl = 0

# uroven Aj
jazyk_aj = st.selectbox('Na akej úrovni ovládate anglický jazyk?', 
                        ['neovládam', 'elementárna - A1 alebo A2', 
                         'pokročilá - B1 alebo B2','vysoká - C1 alebo c2 '])
if jazyk_aj == 'neovládam':
    jazyk_en = 0
elif jazyk_aj == 'elementárna - A1 alebo A2':
    jazyk_en = .33
elif jazyk_aj == 'pokročilá - B1 alebo B2':
    jazyk_en = .66
else:
    jazyk_en = 1

# uroven DE
jazyk_nem = st.selectbox('Na akej úrovni ovládate nemecký jazyk?', 
                        ['neovládam', 'elementárna - A1 alebo A2', 
                         'pokročilá - B1 alebo B2','vysoká - C1 alebo c2 '])
if jazyk_nem == 'neovládam':
    jazyk_de = 0
elif jazyk_nem == 'elementárna - A1 alebo A2':
    jazyk_de = .33
elif jazyk_nem == 'pokročilá - B1 alebo B2':
    jazyk_de = .66
else:
    jazyk_de = 1

# mesiac zaradenia do evidencie
mes_zaradenia = st.slider('V ktorom mesiaci ste zaradený do evidencie UoZ?', 1, 12, 1)

# pred zaradenim do evidencie
postavenie_pred = st.selectbox('Aké bolo vaše postavenie bezprostredne pred zaradením do evidencie UoZ?', 
                    ['pracujúci', 'študent', 'opatrujúci dieťa alebo blízku osobu', 
                     'inak poistená osoba (poberateľ dôchodku, práceneschopný...)', 'nezamestnaný'])

if postavenie_pred == 'pracujúci':
    dov_zaradenia = 'pracujuci'
elif postavenie_pred == 'študent':
    dov_zaradenia = 'absolventi'
elif postavenie_pred == 'opatrujúci dieťa alebo blízku osobu':
    dov_zaradenia = 'opatrujuci'
elif postavenie_pred == 'inak poistená osoba (poberateľ dôchodku, práceneschopný...)':
    dov_zaradenia = 'inak_poisteni'
else :
    dov_zaradenia = 'nezamestnani'
    
# prechadzajuce zamestnanie podla NACE
nace_pred = st.selectbox('V akom odvetví ste pracovali naposledy?', 
                         ['A+B', 'C', 'D+E+F', 'G', 'J+K+L', 'M', 'R+S+T+U', 'nezname'],
                         help = 'pre viac informácii navštívte http://www.nace.sk/')
predch_zam_nace = nace_pred

# prechadchadzajuce zamestnanie podla ISCO
isco_pr = st.selectbox('Akú profesiu ste vykonávali naposledy?', 
                         ['0 ozbrojené sily',
                          '1 zákonodarcovia',
                          '2 špecialisti',
                          '3 odborní pracovníci',
                          '4 administratívni pracovníci',
                          '5 služby a obchod',
                          '6 poľnohospodárstvo',
                          '7 remeselníci',
                          '8 operátori',
                          '9 nekvalifikovaní pracovníci',
                          'neznáme'])

if isco_pr == '0 ozbrojené sily':
    isco_pred = '0_ozbrojene_sily'
elif isco_pr == '1 zákonodarcovia':
    isco_pred = '1_zakonodarcovia'
elif isco_pr == '2 špecialisti':
    isco_pred = '2_specialisti'
elif isco_pr == '3 odborní pracovníci':
    isco_pred = '3_odb_pracovnici'
elif isco_pr == '4 administratívni pracovníci':
    isco_pred = '4_adm_pracovnici'
elif isco_pr == '5 služby a obchod':
    isco_pred = '5_sluzby_obchod'
elif isco_pr == '6 poľnohospodárstvo':
    isco_pred = '6_polnohosp'
elif isco_pr == '7 remeselníci':
    isco_pred = '7_remeselnici'
elif isco_pr == '8 operátori':
    isco_pred = '8_operatori'
elif isco_pr == '9 nekvalifikovaní pracovníci':
    isco_pred = '9_nekval_prac'
else:
    iscopred ='nezname'

predch_zam_isco = isco_pred

# pocet evidovanie ako UoZ za posl 24 mesiacov
predch_ev_pocet = st.slider('Koľkokrát ste boli evidovaný ako UoZ za posledných 24 mesiacov?', 0, 10, 1)

# pocet mesiacov evidovani ako UoZ za posl 24 mesiacov
predch_ev_roky = st.slider('Koľko z posledných 24 mesiacov ste boli evidovaný ako UoZ?', 0, 24, 1)

# bol niekedy v minulosti dobrovolne nezamestnany
dob_nez = st.selectbox('Boli ste v minulosti dobrovoľne nezamestnaný?', ['áno', 'nie'])

if dob_nez == 'áno':
    dobr_nezam = 1
else:
    dobr_nezam = 0

# ci ma zaujem ist pracovat do zahranicia
zahranicie = st.selectbox('Plánujete odísť do zhraničia?', ['áno', 'nie'])

if zahranicie == 'áno':
    umysel_do_zahr = 1
else:
    umysel_do_zahr = 0
    
# pocet zaujmov
zaujmy = st.multiselect('O ktoré z nasledujúcich by ste mali v budúcnosti záujem?', 
                        ['pracovať aj mimo územia SR', 'pracovať aj na skrátený úväzok', 
                        'vykonávať SZČ', 'dochádzať do zamestnania', 'o vzdelávanie', 
                        'vykonávať absolventskú prax', 'ďalej študovať dennou formou'])
pocet_zaujmov = len(zaujmy)
    
# pocet znevyhodneni a z toho potrebne binarne premenne
znevyhodnenia = st.multiselect('Ktoré z nasledujúcich znevýhodnení pre Vás platia?', 
                               ['mám menej ako 26 rokov a ukončil som štúdium pred menej ako 2 rokmi a nemal som odvtedy pravidelne platené zamestnanie',
                                'najmenej 12 predchádzajúcich mesiacov som nemal pravidelne platené zamestnanie',
                                'som štátny príslušník tretej krajiny, ktorému bol udelený azyl',
                                'žijem ako osamelá dospelá osoba s jednou alebo viacerými osobami odkázanými na moju starostlivosť',
                                'mám zdravotné postihnutie'], help = 'môžete zvoliť viacero možností')

# znevyhodneny bez pravidelneho zamestnania
if 'najmenej 12 predchádzajúcich mesiacov som nemal pravidelne platené zamestnanie' in znevyhodnenia:
    znevyh_bez_pravid_zam = 1
else:
    znevyh_bez_pravid_zam = 0

# znevyhodneny absolvent
if 'mám menej ako 26 rokov a ukončil som štúdium pred menej ako 2 rokmi a nemal som odvtedy pravidelne platené zamestnanie' in znevyhodnenia:
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
dobaprax = st.slider('Koľko rokov máte prax na trhu práce?', 0, 70, 1)

# poberanie davky v hmotnej nudzi
davka_v_nudzi = st.selectbox('Poberáte dávku v hmotnej núdzi?', ['áno', 'nie'])

if davka_v_nudzi == 'áno':
    dhn = 1
else:
    dhn = 0

# dlzka aktivnych opatreni na trhu prace
aotp_cas_za_2r = st.slider('Koľko z predchádzajúcich 24 mesiacov ste strávili aktívnymi opatreniami na trhu práce?',
                           0, 24, 1)

# zle veci hlzam su zatial defautlne zvolene ako priemery
hlzam_sp_isco_5 = 0.105
hlzam_sp_isco_9 = 0.086
hlzam_bp_isco_2 = 0.085
hlzam_bp_isco_4 = 0.073
hlzam_bp_isco_8 = 0.437
hlzam_bp_isco_9 = 0.071

# nezamestnanost 
nezam_celk = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'nezam_celk'].values[0]
nezam_odch = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'nezam_odch'].values[0]

# vpm
vpm = df_okresy.loc[df_okresy['nazov_okresu'] == trv_byd, 'vpm'].values[0]

# priemerny hruby vymeriavaci zaklad
vz_zec = st.slider('Aká bola Vaša priemerná hrubá mzda (v eurách) za posledné dva roky?', 0, 2000, 1, 
                   help = 'v prípade, že Vaša hrubá mzda bola viac ako 2000 eur, zvoľte 2000')

# priemerny prijem z dohod
vz_doh = st.slider('Aký bol Váš hrubý priemerný mesačný príjem (v eurách) z práce na dohody za posledné dva roky?', 0, 2000, 1)

# dlzka zamestnanosti v mesiacoch 2 roky pred zaredenim
dlzka_zec = st.slider('Koľko z posledných 24 mesiacov ste boli zamestnaný?', 0, 24, 1)

# dlzka dohody v mesiacoch 2 roky pred zaredenim
dlzka_doh = st.slider('Koľko z posledných 24 mesiacov ste boli zamestnaný ako dohodár?', 0, 24, 1)

# dlzka meterskej v mesiacoch 2 roky pred zaredenim
dlzka_dieta = st.slider('Koľko mesiacov ste strávili na materskej dovolenke alebo starostlivosťou o dieťa za 2 roky pred aktuálnym zaradením?', 0, 24, 1)
  

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
    
ok2 = st.button("Stlačte ma pre výpočet")

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
    st.subheader("Pravdepodobnosť, že budete po 1 roku nezamestnaný je: " + str('{:.2f}'.format(probs[-1]*100)) + " %")


