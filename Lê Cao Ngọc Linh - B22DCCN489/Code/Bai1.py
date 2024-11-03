from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd

# Hàm kiểm tra và chuyển đổi dữ liệu
def validdata(n):
    if n == '' or n is None:
        return "N/a"
    try:
        return float(n)
    except ValueError:
        return "N/a"

# Hàm lấy dữ liệu từ web 
def GetDataFromWeb(url, Xpath_player, Data_name):
    # Cài đặt trình điều khiển Chrome
    service = Service(ChromeDriverManager().install())
    driver1 = webdriver.Chrome(service=service)
    # Truy cập trang web
    driver1.get(url)
    headers = []
    sub_headers = []
    player_list = []
    try:
        # Đợi cho đến khi bảng xuất hiện (tối đa 10 giây)
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, Xpath_player)))
        
        # Lấy bảng HTML bằng Selenium với XPath
        table_element = driver1.find_element(By.XPATH, Xpath_player)

        # Lấy mã nguồn HTML của bảng
        html_table = table_element.get_attribute('outerHTML')

        # Phân tích HTML bằng BeautifulSoup
        soup = bs(html_table, 'html.parser')
        
        # Tìm bảng trực tiếp từ mã HTML đã lấy
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                data = []
                for id, play in enumerate(cols[:-1]):
                    if id == 1:
                        a = play.text.strip().split()
                        if len(a) == 2:
                            data.append(a[1])
                        else:
                            data.append(play.text.strip())
                    else:
                        s = play.text.strip()
                        if id >= 4:
                            s = s.replace(",", "")
                            s = validdata(s)
                        data.append(s)
                if len(data) != 0: player_list.append(data)
    finally:
        # Đóng trình duyệt sau khi hoàn tất
        driver1.quit()
        print("Finish " + Data_name)
    return player_list
#Tạo tiêu đề cho bảng kết quả
column_titles = pd.MultiIndex.from_tuples([
    ('', '', 'Name'), ('', '', 'Nation'), ('', '', 'Team'), ('', '', 'Position'), ('', '', 'Age'),
    ('', '', 'Matches Played'),
    ('', 'Playing Time', 'Starts'), ('', 'Playing Time', 'Min'),
    ('', 'Performance', 'non-Penalty Goals'), ('', 'Performance', 'Penalty Goals'),('', 'Performance', 'Assists'), ('', 'Performance', ' Yellow Cards'), ('', 'Performance', 'Red Cards'),
    ('', 'Expected', 'xG'), ('', 'Expected', 'npxG'), ('', 'Expected', 'xAG'),
    ('', 'Progression', 'PrgC'), ('', 'Progression', 'PrgP'), ('', 'Progression', 'PrgR'),
    ('', 'Per 90 minutes', 'Gls'), ('', 'Per 90 minutes', 'Ast'), ('', 'Per 90 minutes', 'G+A'),
    ('', 'Per 90 minutes', 'G-PK'), ('', 'Per 90 minutes', 'G+A-PK'), ('', 'Per 90 minutes', 'xG'),
    ('', 'Per 90 minutes', 'xAG'), ('', 'Per 90 minutes', 'xG+xAG'), ('', 'Per 90 minutes', 'npxG'),('', 'Per 90 minutes','npxG + xAG'),
    ('Goalkeeping', 'Performance', 'GA'), ('Goalkeeping', 'Performance', 'GA90'),
    ('Goalkeeping', 'Performance', 'SoTA'), ('Goalkeeping', 'Performance', 'Saves'),
    ('Goalkeeping', 'Performance', 'Save%'), ('Goalkeeping', 'Performance', 'W'),
    ('Goalkeeping', 'Performance', 'D'), ('Goalkeeping', 'Performance', 'L'),
    ('Goalkeeping', 'Performance', 'CS'), ('Goalkeeping', 'Performance', 'CS%'),
    ('Goalkeeping', 'Penalty Kick', 'PKatt'), ('Goalkeeping', 'Penalty Kick', 'PKA'),
    ('Goalkeeping', 'Penalty Kick', 'PKsv'), ('Goalkeeping', 'Penalty Kick', 'PKm'),
    ('Goalkeeping', 'Penalty Kick', 'Save%'),
    ('Shooting', 'Standard', 'Gls'), ('Shooting', 'Standard', 'Sh'), ('Shooting', 'Standard', 'SoT'),
    ('Shooting', 'Standard', 'SoT%'), ('Shooting', 'Standard', 'Sh/90'), ('Shooting', 'Standard', 'SoT/90'),
    ('Shooting', 'Standard', 'G/Sh'), ('Shooting', 'Standard', 'G/SoT'), ('Shooting', 'Standard', 'Dist'),
    ('Shooting', 'Standard', 'FK'), ('Shooting', 'Standard', 'PK'), ('Shooting', 'Standard', 'PKatt'),
    ('Shooting', 'Expected', 'xG'), ('Shooting', 'Expected', 'npxG'), ('Shooting', 'Expected', 'npxG/Sh'),
    ('Shooting', 'Expected', 'G-xG'), ('Shooting', 'Expected', 'np:G-xG'),
    ('Passing', 'Total', 'Cmp'), ('Passing', 'Total', 'Att'), ('Passing', 'Total', 'Cmp%'),
    ('Passing', 'Total', 'TotDist'), ('Passing', 'Total', 'PrgDist'),
    ('Passing', 'Short', 'Cmp'), ('Passing', 'Short', 'Att'), ('Passing', 'Short', 'Cmp%'),
    ('Passing', 'Medium', 'Cmp'), ('Passing', 'Medium', 'Att'), ('Passing', 'Medium', 'Cmp%'),
    ('Passing', 'Long', 'Cmp'), ('Passing', 'Long', 'Att'), ('Passing', 'Long', 'Cmp%'),
    ('Passing', 'Expected', 'Ast'), ('Passing', 'Expected', 'xAG'), ('Passing', 'Expected', 'xA'),
    ('Passing', 'Expected', 'A-xAG'), ('Passing', 'Expected', 'KP'), ('Passing', 'Expected', '"1/3"'),
    ('Passing', 'Expected', 'PPA'), ('Passing', 'Expected', 'CrsPA'), ('Passing', 'Expected', 'PrgP'),
    ('Pass Types', 'Pass Types', 'Live'), ('Pass Types', 'Pass Types', 'Dead'), ('Pass Types', 'Pass Types', 'FK'),
    ('Pass Types', 'Pass Types', 'TB'), ('Pass Types', 'Pass Types', 'Sw'), ('Pass Types', 'Pass Types', 'Crs'),
    ('Pass Types', 'Pass Types', 'TI'), ('Pass Types', 'Pass Types', 'CK'),
    ('Pass Types', 'Corner Kicks', 'In'), ('Pass Types', 'Corner Kicks', 'Out'), ('Pass Types', 'Corner Kicks', 'Str'),
    ('Pass Types', 'Outcomes', 'Cmp'), ('Pass Types', 'Outcomes', 'Off'), ('Pass Types', 'Outcomes', 'Blocks'),
    ('Goal and Shot Creation', 'SCA', 'SCA'), ('Goal and Shot Creation', 'SCA', 'SCA90'),
    ('Goal and Shot Creation', 'SCA Types', 'PassLive'), ('Goal and Shot Creation', 'SCA Types', 'PassDead'),
    ('Goal and Shot Creation', 'SCA Types', 'TO'), ('Goal and Shot Creation', 'SCA Types', 'Sh'),
    ('Goal and Shot Creation', 'SCA Types', 'Fld'), ('Goal and Shot Creation', 'SCA Types', 'Def'),
    ('Goal and Shot Creation', 'GCA', 'GCA'), ('Goal and Shot Creation', 'GCA', 'GCA90'),
    ('Goal and Shot Creation', 'GCA Types', 'PassLive'), ('Goal and Shot Creation', 'GCA Types', 'PassDead'),
    ('Goal and Shot Creation', 'GCA Types', 'TO'), ('Goal and Shot Creation', 'GCA Types', 'Sh'),
    ('Goal and Shot Creation', 'GCA Types', 'Fld'), ('Goal and Shot Creation', 'GCA Types', 'Def'),
    ('Defensive Actions', 'Tackles', 'Tkl'), ('Defensive Actions', 'Tackles', 'TklW'),
    ('Defensive Actions', 'Tackles', 'Def 3rd'),
    ('Defensive Actions', 'Tackles', 'Mid 3rd'), ('Defensive Actions', 'Tackles', 'Att 3rd'),
    ('Defensive Actions', 'Challenges', 'Tkl'), ('Defensive Actions', 'Challenges', 'Att'),
    ('Defensive Actions', 'Challenges', 'Tkl%'), ('Defensive Actions', 'Challenges', 'Lost'),
    ('Defensive Actions', 'Blocks', 'Blocks'), ('Defensive Actions', 'Blocks', 'Sh'),
    ('Defensive Actions', 'Blocks', 'Pass'), ('Defensive Actions', 'Blocks', 'Int'),
    ('Defensive Actions', 'Blocks', 'Tkl+Int'), ('Defensive Actions', 'Blocks', 'Clr'),
    ('Defensive Actions', 'Blocks', 'Err'),
    ('Possession', 'Touches', 'Touches'), ('Possession', 'Touches', 'Def Pen'), ('Possession', 'Touches', 'Def 3rd'),
    ('Possession', 'Touches', 'Mid 3rd'), ('Possession', 'Touches', 'Att 3rd'), ('Possession', 'Touches', 'Att Pen'),
    ('Possession', 'Touches', 'Live'),
    ('Possession', 'Take-Ons', 'Att'), ('Possession', 'Take-Ons', 'Succ'), ('Possession', 'Take-Ons', 'Succ%'),
    ('Possession', 'Take-Ons', 'Tkld'), ('Possession', 'Take-Ons', 'Tkld%'),
    ('Possession', 'Carries', 'Carries'), ('Possession', 'Carries', 'TotDist'), ('Possession', 'Carries', 'ProDist'),
    ('Possession', 'Carries', 'ProgC'), ('Possession', 'Carries', '"1/3'), ('Possession', 'Carries', 'CPA'),
    ('Possession', 'Carries', 'Mis'), ('Possession', 'Carries', 'Dis'),
    ('Possession', 'Receiving', 'ReC'), ('Possession', 'Receiving', 'PrgR'),
    ('Playing Time', 'Starts', 'Starts'), ('Playing Time', 'Starts', 'Mn/Start'), ('Playing Time', 'Starts', 'Compl'),
    ('Playing Time', 'Starts', 'Subs'), ('Playing Time', 'Starts', 'Mn/Sub'), ('Playing Time', 'Starts', 'unSub'),
    ('Playing Time', 'Team Success', 'PPM'), ('Playing Time', 'Team Success', 'onG'),
    ('Playing Time', 'Team Success', 'onGA'),
    ('Playing Time', 'Team Success(xG)', 'onxG'), ('Playing Time', 'Team Success(xG)', 'onxGA'),
    ('Miscellaneous Stats', 'Performance', 'Fls'), ('Miscellaneous Stats', 'Performance', 'Fld'),
    ('Miscellaneous Stats', 'Performance', 'Off'), ('Miscellaneous Stats', 'Performance', 'Crs'),
    ('Miscellaneous Stats', 'Performance', 'OG'), ('Miscellaneous Stats', 'Performance', 'Recov'),
    ('Miscellaneous Stats', 'Aerial Duels', 'Won'), ('Miscellaneous Stats', 'Aerial Duels', 'Lost'),
    ('Miscellaneous Stats', 'Aerial Duels', 'Won%'),

])
#########################################################################################
# Lấy dữ liệu từ bảng stats standard
url = "https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_standard"]'
Data_name = "Standard"
list = GetDataFromWeb(url, Xpath_player, Data_name)

player_list = []
for p in list:
    try:
        Name, Nation, Position, Team, Age = p[0:5]
        mp, starts, min = p[6:9]
        non_pen, pen_goal, ass, ycard, rcard = [p[13],p[14],p[11],p[16],p[17]]
        xG, npxG, xAG = p[18:21]
        PrgC, PrgP, PrgR = p[22:25]
        Gls, Ast, G_Ao, G_PKo, G_A_PKo, xG, xAG, xG_xAG, npxG, npxG_xAG = p[25:35]
        if min > 90: player_list.append([Name, Nation, Team, Position, Age,mp, starts, min,non_pen, pen_goal, ass, ycard, rcard,xG, npxG, xAG,PrgC, PrgP, PrgR,Gls, Ast, G_Ao, G_PKo, G_A_PKo, xG, xAG, xG_xAG, npxG, npxG_xAG])
    except IndexError:
        break
df_player = pd.DataFrame(player_list, columns=['Name','Nation','Team','Position','Age', 'Matches Played','Starts', 'Min', 'non-Penalty Goals', 'Penalty Goals', 'Assists', ' Yellow Cards', 'Red Cards',
                                               'xG', 'npxG', 'xAG',
                                    
                                'PrgC', 'PrgP', 'PrgR', 
                                'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG','npxG + xAG'])
# df_player.to_csv('Standard.csv')
#########################################################################################
#Lấy dữ liệu từ bảng player keepers
url = "https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_keeper"]'
Data_name = "Keepers"
list = GetDataFromWeb(url, Xpath_player, Data_name)
keeper_list = []

for p in list:
    Name = p[0]
    Team = p[3]
    GAo, GA90o, SoTA, Saves, Save__o, Wo, Do, Lo, CSo, CS_o, PKatt, PKAo, PKsv, PKm, Save_o  = p[10:]
    keeper_list.append([Name,Team,GAo, GA90o, SoTA, Saves, Save__o, Wo, Do, Lo, CSo, CS_o, PKatt, PKAo, PKsv, PKm, Save_o])
df_keepers = pd.DataFrame(keeper_list, columns=['Name','Team','GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS','CS%', 'PKatt', 'PKA', 'PKsv', 'PKm', 'Save%'] )
# df_keepers.to_csv('Keepers.csv')
##########################################################################################
# Lấy dữ liệu từ bảng player shooting
url = "https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_shooting"]'
Data_name = "Shooting"
list = GetDataFromWeb(url, Xpath_player, Data_name)
Shooting_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Gls, Sh, SoT, SoT_o, Sh_90, SoT_90, G_Sh, G_SoT, Dist, FKo, PKo, PKatt,xG, npxG, npxG_Sh, G_xG, np_G_xG  = p[7:]
    Shooting_list.append([Name,Team, Gls, Sh, SoT, SoT_o, Sh_90, SoT_90, G_Sh, G_SoT, Dist, FKo, PKo, PKatt,xG, npxG, npxG_Sh, G_xG, np_G_xG])
df_shooting = pd.DataFrame(Shooting_list, columns=['Name','Team', 'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG'])
# df_shooting.to_csv('Shooting.csv')
#########################################################################################
# Lấy dữ liệu từ bảng player passing
url = "https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_passing"]'
Data_name = "Passing"
list = GetDataFromWeb(url, Xpath_player, Data_name)
# Passing = Passing.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
Passing_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Cmp, Att, Cmp_o, TotDist, sPrgDist ,sCmp, sAtt, sCmp_o, mCmp, mAtt, mCmp_o, lCmp, lAtt, lCmp_o, Ast_, xAG_, xA, A_xAG, KPo, a1_3, PPAo, CrsPA, PrgP_ = p[7:]
    Passing_list.append([Name,Team,Cmp, Att, Cmp_o, TotDist, sPrgDist ,sCmp, sAtt, sCmp_o, mCmp, mAtt, mCmp_o, lCmp, lAtt, lCmp_o, Ast_, xAG_, xA, A_xAG, KPo, a1_3, PPAo, CrsPA, PrgP_])
df_Passing = pd.DataFrame(Passing_list, columns=['Name','Team','Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist' ,'Cmp', 'Att', 'Cmp%' ,'Cmp', 'Att', 'Cmp%' 
  ,'Cmp', 'Att', 'Cmp%' 
  , 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP'])
# df_Passing.to_csv('Passing.csv')
#########################################################################################
#Lấy dữ liệu từ bảng player passing types
url = "https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_passing_types"]'
Data_name = "Passing_types"
list = GetDataFromWeb(url, Xpath_player, Data_name)
# Passing_types = Passing_types.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
Passing_type_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Live, Dead, FKo, TBo, Sw, Crs, TIo, CKo,In, Out, Str, Cmp, Off, Blocks  = p[8:22]
  
    Passing_type_list.append([Name,Team,Live, Dead, FKo, TBo, Sw, Crs, TIo, CKo,In, Out, Str, Cmp, Off, Blocks])
df_passing_type = pd.DataFrame(Passing_type_list, columns=['Name','Team','Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK' 
  ,'In', 'Out', 'Str' 
  ,'Cmp', 'Off', 'Blocks'])
# df_passing_type.to_csv('Pass_types.csv')
#########################################################################################
#Lấy dữ liệu từ bảng goals and short creation
url = "https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_gca"]'
Data_name = "Goal_and_Shot_Creation"
list = GetDataFromWeb(url, Xpath_player, Data_name)
Goal_and_Shot_Creation = []
for p in list:
    Name = p[0]
    Team = p[3]
    SCAo, SCA90o, PassLive, PassDead, TOo, Sh, Fld, Def, GCAo, GCA90o, PassLive, PassDead, TOo, Sh, Fld, Def = p[7:23]

    Goal_and_Shot_Creation.append([Name,Team, SCAo, SCA90o, PassLive, PassDead, TOo, Sh, Fld, Def, GCAo, GCA90o, PassLive, PassDead, TOo, Sh, Fld, Def])
df_Goal_and_Shot_Creation = pd.DataFrame(Goal_and_Shot_Creation, columns=['Name','Team','SCA', 'SCA90','PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def', 
            'GCA', 'GCA90', 
        'PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def' ])
# df_Goal_and_Shot_Creation.to_csv('gca.csv')
#########################################################################################
# Lấy dữ liệu từ bảng defensive actions
url = "https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_defense"]'
Data_name = "Defensive_Actions"
list = GetDataFromWeb(url, Xpath_player, Data_name)
# Defensive_Actions = Defensive_Actions.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
Defensive_Actions = []
for p in list:
    Name = p[0]
    Team = p[3]
    Tkl, TklW, Def3rd, Mid3rd, Att3rd,dTkl, dAtt, Tkl_o, Lost, Blocks, Sh, Pass, Int, Tkl_Int, Clr, Err = p[7:23]

    Defensive_Actions.append([Name,Team, Tkl, TklW, Def3rd, Mid3rd, Att3rd,dTkl, dAtt, Tkl_o, Lost, Blocks, Sh, Pass, Int, Tkl_Int, Clr, Err])
df_Defensive_Actions = pd.DataFrame(Defensive_Actions, columns=['Name','Team','Tkl', 'TklW', 'Def 3rd', 'Mid 3rd', 'Att 3rd' 
  , 'Tkl', 'Att', 'Tkl%', 'Lost' 
 , 'Blocks', 'Sh', 'Pass', 'Int', 'Tkl + Int', 'Clr', 'Err'  ])

# df_Defensive_Actions.to_csv('defense.csv')
#########################################################################################
url = "https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_possession"]'
Data_name = "Possession"
list = GetDataFromWeb(url, Xpath_player, Data_name)
Possession = []
# Possession = Possession.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
for p in list:
    Name = p[0]
    Team = p[3]
    Touches, DefPen, Def3rd, id3rd, Att3rd, AttPen, Live, Att, Succ, Succ_o, Tkld, Tkld_o ,Carries, TotDist, ProDist, ProgC, o1_3, CPAo, Mis, Dis, Rec, PrgR = p[7:29]
    Possession.append( [Name,Team, Touches, DefPen, Def3rd, id3rd, Att3rd, AttPen, Live, Att, Succ, Succ_o, Tkld, Tkld_o ,Carries, TotDist, ProDist, ProgC, o1_3, CPAo, Mis, Dis, Rec, PrgR])
df_possession = pd.DataFrame(Possession, columns=['Name','Team',  'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Live'
                                                  , 'Att', 'Succ', 'Succ%', 'Tkld', 'Tkld%'
                                                  ,'Carries', 'TotDist', 'ProDist', 'ProgC', '1/3', 'CPA', 'Mis', 'Dis'
                                                  , 'Rec', 'PrgR' 
   ])
# df_possession.to_csv('possession.csv')
#########################################################################################
url = "https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_playing_time"]'
Data_name = "Playing_time"
list = GetDataFromWeb(url, Xpath_player, Data_name)
# Playing_time = Playing_time.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
playing_time = []
for p in list:
    Name = p[0]
    Team = p[3]
    Starts, Mn_Start, Compl ,Subs, Mn_Sub, unSub, PPM_o, onG, onGA = p[11:20]
    onxG, onxGA = p[23:25]
    playing_time.append([Name,Team,Starts, Mn_Start, Compl ,Subs, Mn_Sub, unSub, PPM_o, onG, onGA, onxG, onxGA])
df_playing_time = pd.DataFrame(playing_time, columns=['Name','Team','Starts', 'Mn/Start', 'Compl' ,'Subs', 'Mn/Sub', 'unSub', 'PPM', 'onG', 'onGA', 'onxG', 'onxGA'])
# df_playing_time.to_csv('Playing_time.csv')
#########################################################################################
url = "https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats"
Xpath_player = '//*[@id="stats_misc"]'
Data_name = "Miscellaneous_Stats"
list = GetDataFromWeb(url, Xpath_player, Data_name)
# Miscellaneous_Stats = Miscellaneous_Stats.drop(columns=[(np.nan, 'Nation'),(np.nan, 'Pos'),(np.nan, 'Age'), (np.nan, 'Born')], axis=1)
Miscellaneous_Stats = []
for p in list: 
    Name = p[0]
    Team = p[3]
    Fls, Fldo, Offo, Crso, OGo, Recov, Won, Losto, Wono = p[10:14]+p[18:23]
    Miscellaneous_Stats.append([ Name,Team, Fls, Fldo, Offo, Crso, OGo, Recov, Won, Losto, Wono])
df_Miscellaneous_Stats = pd.DataFrame(Miscellaneous_Stats, columns=['Name','Team','Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov', 'Won', 'Lost', 'Won%'])
# df_Miscellaneous_Stats.to_csv('misc.csv')
#########################################################################################
# Gộp các dataframe lại thành 1
dataframes = [df_keepers,df_shooting,df_Passing, df_passing_type,df_Goal_and_Shot_Creation,df_Defensive_Actions,df_possession, df_playing_time,df_Miscellaneous_Stats]
df_merged = df_player
for df in dataframes:
    df_merged = pd.merge(df_merged,df, on = ['Name','Team'], how = 'left')
#########################################################################################
# Sắp xếp theo First Name và Age
df_merged['First Name'] = df_merged['Name'].apply(lambda x: x.split()[0])
df_sorted = df_merged.sort_values(by=['First Name', 'Age'], ascending=[True, False])
df_sorted = df_sorted.drop(columns=['First Name'])
# In ra DataFrame đã sắp xếp
df_sorted.columns = column_titles
df_sorted.to_csv('result.csv', index=False, na_rep='N/a')
print('Du lieu da duoc luu vao file result.csv')
