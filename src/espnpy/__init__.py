from .client import ESPNClient, LeagueProxy

__version__ = "1.0.0"

# Create a global default client for convenience (espnpy.nfl.teams())
_default_client = ESPNClient()

# Expose common leagues explicitly for IDE Auto-complete
league_164205 = _default_client.league_164205
league_180659 = _default_client.league_180659
league_2009 = _default_client.league_2009
league_236461 = _default_client.league_236461
league_242041 = _default_client.league_242041
league_244293 = _default_client.league_244293
league_267979 = _default_client.league_267979
league_268565 = _default_client.league_268565
league_270555 = _default_client.league_270555
league_270557 = _default_client.league_270557
league_270559 = _default_client.league_270559
league_270563 = _default_client.league_270563
league_271937 = _default_client.league_271937
league_272073 = _default_client.league_272073
league_282 = _default_client.league_282
league_283 = _default_client.league_283
league_289234 = _default_client.league_289234
league_289237 = _default_client.league_289237
league_289262 = _default_client.league_289262
league_289271 = _default_client.league_289271
league_289272 = _default_client.league_289272
league_289274 = _default_client.league_289274
league_289277 = _default_client.league_289277
league_289279 = _default_client.league_289279
league_3 = _default_client.league_3
absolute = _default_client.absolute
afc_asian_cup = _default_client.afc_asian_cup
afc_challenge_cup = _default_client.afc_challenge_cup
afc_champions = _default_client.afc_champions
afc_cup = _default_client.afc_cup
afc_cupq = _default_client.afc_cupq
afc_saff_championship = _default_client.afc_saff_championship
afc_w_asian_cup = _default_client.afc_w_asian_cup
aff_championship = _default_client.aff_championship
affliction = _default_client.affliction
afl = _default_client.afl
arg_1 = _default_client.arg_1
arg_2 = _default_client.arg_2
arg_3 = _default_client.arg_3
arg_4 = _default_client.arg_4
arg_copa = _default_client.arg_copa
arg_copa_de_la_superliga = _default_client.arg_copa_de_la_superliga
arg_supercopa = _default_client.arg_supercopa
arg_supercopa_internacional = _default_client.arg_supercopa_internacional
arg_trofeo_de_la_campeones = _default_client.arg_trofeo_de_la_campeones
atp = _default_client.atp
aus_1 = _default_client.aus_1
aus_w_1 = _default_client.aus_w_1
aut_1 = _default_client.aut_1
bang_fighting = _default_client.bang_fighting
bangabandhu_cup = _default_client.bangabandhu_cup
banni_fight = _default_client.banni_fight
banzay = _default_client.banzay
barracao = _default_client.barracao
battlezone = _default_client.battlezone
bel_1 = _default_client.bel_1
bel_promotion_relegation = _default_client.bel_promotion_relegation
bellator = _default_client.bellator
benevides = _default_client.benevides
big_fight = _default_client.big_fight
blackout = _default_client.blackout
bol_1 = _default_client.bol_1
bol_copa = _default_client.bol_copa
bol_ply_rel = _default_client.bol_ply_rel
bosnia = _default_client.bosnia
boxe = _default_client.boxe
bra_1 = _default_client.bra_1
bra_2 = _default_client.bra_2
bra_3 = _default_client.bra_3
bra_camp_carioca = _default_client.bra_camp_carioca
bra_camp_gaucho = _default_client.bra_camp_gaucho
bra_camp_mineiro = _default_client.bra_camp_mineiro
bra_camp_paulista = _default_client.bra_camp_paulista
bra_carioca_groupa = _default_client.bra_carioca_groupa
bra_carioca_groupb = _default_client.bra_carioca_groupb
bra_copa_do_brazil = _default_client.bra_copa_do_brazil
bra_copa_do_nordeste = _default_client.bra_copa_do_nordeste
bra_supercopa_do_brazil = _default_client.bra_supercopa_do_brazil
brazilian_freestyle = _default_client.brazilian_freestyle
budo = _default_client.budo
caf_champions = _default_client.caf_champions
caf_championship = _default_client.caf_championship
caf_championship_qual = _default_client.caf_championship_qual
caf_confed = _default_client.caf_confed
caf_cosafa = _default_client.caf_cosafa
caf_nations = _default_client.caf_nations
caf_nations_qual = _default_client.caf_nations_qual
caf_w_nations = _default_client.caf_w_nations
cage_warriors = _default_client.cage_warriors
campeones_cup = _default_client.campeones_cup
can_w_nsl = _default_client.can_w_nsl
caribbean_series = _default_client.caribbean_series
cfl = _default_client.cfl
champions_tour = _default_client.champions_tour
chi_1 = _default_client.chi_1
chi_1_promotion_relegation = _default_client.chi_1_promotion_relegation
chi_2 = _default_client.chi_2
chi_copa_chi = _default_client.chi_copa_chi
chi_super_cup = _default_client.chi_super_cup
chn_1 = _default_client.chn_1
chn_1_promotion_relegation = _default_client.chn_1_promotion_relegation
club_friendly = _default_client.club_friendly
col_1 = _default_client.col_1
col_2 = _default_client.col_2
col_copa = _default_client.col_copa
col_superliga = _default_client.col_superliga
college_baseball = _default_client.college_baseball
college_football = _default_client.college_football
college_softball = _default_client.college_softball
concacaf_central_american_cup = _default_client.concacaf_central_american_cup
concacaf_champions = _default_client.concacaf_champions
concacaf_champions_cup = _default_client.concacaf_champions_cup
concacaf_confederations_playoff = _default_client.concacaf_confederations_playoff
concacaf_gold = _default_client.concacaf_gold
concacaf_gold_qual = _default_client.concacaf_gold_qual
concacaf_leagues_cup = _default_client.concacaf_leagues_cup
concacaf_nations_league = _default_client.concacaf_nations_league
concacaf_u23 = _default_client.concacaf_u23
concacaf_w_champions_cup = _default_client.concacaf_w_champions_cup
concacaf_w_gold = _default_client.concacaf_w_gold
concacaf_womens_championship = _default_client.concacaf_womens_championship
conmebol_america = _default_client.conmebol_america
conmebol_america_femenina = _default_client.conmebol_america_femenina
conmebol_libertadores = _default_client.conmebol_libertadores
conmebol_recopa = _default_client.conmebol_recopa
conmebol_sudamericana = _default_client.conmebol_sudamericana
crc_1 = _default_client.crc_1
cyp_1 = _default_client.cyp_1
den_1 = _default_client.den_1
dominican_winter_league = _default_client.dominican_winter_league
dream = _default_client.dream
ecu_1 = _default_client.ecu_1
eng_1 = _default_client.eng_1
eng_2 = _default_client.eng_2
eng_3 = _default_client.eng_3
eng_4 = _default_client.eng_4
eng_5 = _default_client.eng_5
eng_charity = _default_client.eng_charity
eng_fa = _default_client.eng_fa
eng_league_cup = _default_client.eng_league_cup
eng_trophy = _default_client.eng_trophy
eng_w_1 = _default_client.eng_w_1
eng_w_fa = _default_client.eng_w_fa
eng_w_league_cup = _default_client.eng_w_league_cup
esp_1 = _default_client.esp_1
esp_2 = _default_client.esp_2
esp_copa_de_la_reina = _default_client.esp_copa_de_la_reina
esp_copa_del_rey = _default_client.esp_copa_del_rey
esp_joan_gamper = _default_client.esp_joan_gamper
esp_super_cup = _default_client.esp_super_cup
esp_w_1 = _default_client.esp_w_1
eur = _default_client.eur
euroamericana_supercopa = _default_client.euroamericana_supercopa
f1 = _default_client.f1
fiba = _default_client.fiba
fifa_concacaf_olympicsq = _default_client.fifa_concacaf_olympicsq
fifa_conmebol_olympicsq = _default_client.fifa_conmebol_olympicsq
fifa_cwc = _default_client.fifa_cwc
fifa_friendly = _default_client.fifa_friendly
fifa_friendly_w = _default_client.fifa_friendly_w
fifa_friendly_u21 = _default_client.fifa_friendly_u21
fifa_intercontinental_cup = _default_client.fifa_intercontinental_cup
fifa_intercontinental_cup = _default_client.fifa_intercontinental_cup
fifa_intercontinental_cup_not_used = _default_client.fifa_intercontinental_cup_not_used
fifa_olympics = _default_client.fifa_olympics
fifa_shebelieves = _default_client.fifa_shebelieves
fifa_w_champions_cup = _default_client.fifa_w_champions_cup
fifa_w_concacaf_olympicsq = _default_client.fifa_w_concacaf_olympicsq
fifa_w_olympics = _default_client.fifa_w_olympics
fifa_wcq_ply = _default_client.fifa_wcq_ply
fifa_world = _default_client.fifa_world
fifa_world_u17 = _default_client.fifa_world_u17
fifa_world_u20 = _default_client.fifa_world_u20
fifa_worldq_afc = _default_client.fifa_worldq_afc
fifa_worldq_afc_conmebol = _default_client.fifa_worldq_afc_conmebol
fifa_worldq_caf = _default_client.fifa_worldq_caf
fifa_worldq_concacaf = _default_client.fifa_worldq_concacaf
fifa_worldq_concacaf_ofc = _default_client.fifa_worldq_concacaf_ofc
fifa_worldq_conmebol = _default_client.fifa_worldq_conmebol
fifa_worldq_ofc = _default_client.fifa_worldq_ofc
fifa_worldq_uefa = _default_client.fifa_worldq_uefa
fifa_wwc = _default_client.fifa_wwc
fifa_wwcq_ply = _default_client.fifa_wwcq_ply
fifa_wworld_u17 = _default_client.fifa_wworld_u17
fifa_wworldq_uefa = _default_client.fifa_wworldq_uefa
fng = _default_client.fng
fra_1 = _default_client.fra_1
fra_1_promotion_relegation = _default_client.fra_1_promotion_relegation
fra_2 = _default_client.fra_2
fra_coupe_de_france = _default_client.fra_coupe_de_france
fra_super_cup = _default_client.fra_super_cup
fra_w_1 = _default_client.fra_w_1
friendly_emirates_cup = _default_client.friendly_emirates_cup
ger_1 = _default_client.ger_1
ger_2 = _default_client.ger_2
ger_2_promotion_relegation = _default_client.ger_2_promotion_relegation
ger_a_bayernliganorth = _default_client.ger_a_bayernliganorth
ger_dfb_pokal = _default_client.ger_dfb_pokal
ger_playoff_relegation = _default_client.ger_playoff_relegation
ger_super_cup = _default_client.ger_super_cup
gha_1 = _default_client.gha_1
global_arnold_clark_cup = _default_client.global_arnold_clark_cup
global_champs_cup = _default_client.global_champs_cup
global_club_challenge = _default_client.global_club_challenge
global_finalissima = _default_client.global_finalissima
global_gulf_cup = _default_client.global_gulf_cup
global_pinatar_cup = _default_client.global_pinatar_cup
global_toulon = _default_client.global_toulon
global_u20_intercontinental_cup = _default_client.global_u20_intercontinental_cup
global_w_finalissima = _default_client.global_w_finalissima
global_wchamps_cup = _default_client.global_wchamps_cup
gre_1 = _default_client.gre_1
gua_1 = _default_client.gua_1
hockey_world_cup = _default_client.hockey_world_cup
hon_1 = _default_client.hon_1
idn_1 = _default_client.idn_1
ifc = _default_client.ifc
ifl = _default_client.ifl
ind_1 = _default_client.ind_1
ind_2 = _default_client.ind_2
ir1_1_promotion_relegation = _default_client.ir1_1_promotion_relegation
irl = _default_client.irl
irl_1 = _default_client.irl_1
ita_1 = _default_client.ita_1
ita_2 = _default_client.ita_2
ita_coppa_italia = _default_client.ita_coppa_italia
ita_super_cup = _default_client.ita_super_cup
jpn_1 = _default_client.jpn_1
jpn_world_challenge = _default_client.jpn_world_challenge
k1 = _default_client.k1
ken_1 = _default_client.ken_1
ksa_1 = _default_client.ksa_1
ksa_kings_cup = _default_client.ksa_kings_cup
ksw = _default_client.ksw
lfa = _default_client.lfa
lfc = _default_client.lfc
liv = _default_client.liv
llb = _default_client.llb
lls = _default_client.lls
lpga = _default_client.lpga
m1 = _default_client.m1
mens_college_basketball = _default_client.mens_college_basketball
mens_college_hockey = _default_client.mens_college_hockey
mens_college_lacrosse = _default_client.mens_college_lacrosse
mens_college_volleyball = _default_client.mens_college_volleyball
mens_college_water_polo = _default_client.mens_college_water_polo
mens_olympics_basketball = _default_client.mens_olympics_basketball
mens_olympics_golf = _default_client.mens_olympics_golf
mex_1 = _default_client.mex_1
mex_2 = _default_client.mex_2
mex_campeon = _default_client.mex_campeon
mexican_winter_league = _default_client.mexican_winter_league
mfc = _default_client.mfc
mlb = _default_client.mlb
mys_1 = _default_client.mys_1
nascar_premier = _default_client.nascar_premier
nascar_secondary = _default_client.nascar_secondary
nascar_truck = _default_client.nascar_truck
nba = _default_client.nba
nba_development = _default_client.nba_development
nba_summer_california = _default_client.nba_summer_california
nba_summer_golden_state = _default_client.nba_summer_golden_state
nba_summer_las_vegas = _default_client.nba_summer_las_vegas
nba_summer_orlando = _default_client.nba_summer_orlando
nba_summer_sacramento = _default_client.nba_summer_sacramento
nba_summer_utah = _default_client.nba_summer_utah
nbl = _default_client.nbl
ned_1 = _default_client.ned_1
ned_2 = _default_client.ned_2
ned_3 = _default_client.ned_3
ned_3_promotion_relegation = _default_client.ned_3_promotion_relegation
ned_cup = _default_client.ned_cup
ned_playoff_relegation = _default_client.ned_playoff_relegation
ned_supercup = _default_client.ned_supercup
ned_w_1 = _default_client.ned_w_1
ned_w_eredivisie_cup = _default_client.ned_w_eredivisie_cup
ned_w_knvb_cup = _default_client.ned_w_knvb_cup
nfl = _default_client.nfl
nga_1 = _default_client.nga_1
nhl = _default_client.nhl
nll = _default_client.nll
nonfifa = _default_client.nonfifa
nor_1 = _default_client.nor_1
nor_1_promotion_relegation = _default_client.nor_1_promotion_relegation
ntw = _default_client.ntw
ofc = _default_client.ofc
olympics_baseball = _default_client.olympics_baseball
olympics_mens_ice_hockey = _default_client.olympics_mens_ice_hockey
olympics_womens_ice_hockey = _default_client.olympics_womens_ice_hockey
other = _default_client.other
pancrase = _default_client.pancrase
par_1 = _default_client.par_1
par_1_supercopa = _default_client.par_1_supercopa
per_1 = _default_client.per_1
pfl = _default_client.pfl
pga = _default_client.pga
pll = _default_client.pll
por_1 = _default_client.por_1
por_1_promotion_relegation = _default_client.por_1_promotion_relegation
por_taca_portugal = _default_client.por_taca_portugal
pride = _default_client.pride
proelite = _default_client.proelite
puerto_rican_winter_league = _default_client.puerto_rican_winter_league
rfa = _default_client.rfa
rizin = _default_client.rizin
roc = _default_client.roc
rsa_1 = _default_client.rsa_1
rsa_1_promotion_relegation = _default_client.rsa_1_promotion_relegation
rsa_2 = _default_client.rsa_2
rsa_mtn8 = _default_client.rsa_mtn8
rus_1 = _default_client.rus_1
rus_1_promotion_relegation = _default_client.rus_1_promotion_relegation
sco_1 = _default_client.sco_1
sco_1_promotion_relegation = _default_client.sco_1_promotion_relegation
sco_2 = _default_client.sco_2
sco_2_promotion_relegation = _default_client.sco_2_promotion_relegation
sco_challenge = _default_client.sco_challenge
sco_cis = _default_client.sco_cis
sco_tennents = _default_client.sco_tennents
sfl = _default_client.sfl
sgp_1 = _default_client.sgp_1
shark_fights = _default_client.shark_fights
shooto_brazil = _default_client.shooto_brazil
shooto_japan = _default_client.shooto_japan
shoxc = _default_client.shoxc
slv_1 = _default_client.slv_1
strikeforce = _default_client.strikeforce
swe_1 = _default_client.swe_1
swe_1_promotion_relegation = _default_client.swe_1_promotion_relegation
tfc = _default_client.tfc
tgl = _default_client.tgl
tha_1 = _default_client.tha_1
tpf = _default_client.tpf
tur_1 = _default_client.tur_1
uefa_champions = _default_client.uefa_champions
uefa_champions_qual = _default_client.uefa_champions_qual
uefa_euro = _default_client.uefa_euro
uefa_euro_u19 = _default_client.uefa_euro_u19
uefa_euro_u21 = _default_client.uefa_euro_u21
uefa_euro_u21_qual = _default_client.uefa_euro_u21_qual
uefa_europa = _default_client.uefa_europa
uefa_europa_conf = _default_client.uefa_europa_conf
uefa_europa_conf_qual = _default_client.uefa_europa_conf_qual
uefa_europa_qual = _default_client.uefa_europa_qual
uefa_euroq = _default_client.uefa_euroq
uefa_nations = _default_client.uefa_nations
uefa_super_cup = _default_client.uefa_super_cup
uefa_w_europa = _default_client.uefa_w_europa
uefa_w_nations = _default_client.uefa_w_nations
uefa_wchampions = _default_client.uefa_wchampions
uefa_weuro = _default_client.uefa_weuro
ufc = _default_client.ufc
ufl = _default_client.ufl
uga_1 = _default_client.uga_1
uru_1 = _default_client.uru_1
uru_2 = _default_client.uru_2
usa_1 = _default_client.usa_1
usa_ncaa_m_1 = _default_client.usa_ncaa_m_1
usa_ncaa_w_1 = _default_client.usa_ncaa_w_1
usa_nwsl = _default_client.usa_nwsl
usa_nwsl_cup = _default_client.usa_nwsl_cup
usa_nwsl_summer_cup = _default_client.usa_nwsl_summer_cup
usa_open = _default_client.usa_open
usa_usl_1 = _default_client.usa_usl_1
usa_usl_l1 = _default_client.usa_usl_l1
usa_usl_l1_cup = _default_client.usa_usl_l1_cup
usa_w_usl_1 = _default_client.usa_w_usl_1
ven_1 = _default_client.ven_1
venezuelan_winter_league = _default_client.venezuelan_winter_league
vfc = _default_client.vfc
wec = _default_client.wec
wnba = _default_client.wnba
womens_college_basketball = _default_client.womens_college_basketball
womens_college_field_hockey = _default_client.womens_college_field_hockey
womens_college_hockey = _default_client.womens_college_hockey
womens_college_lacrosse = _default_client.womens_college_lacrosse
womens_college_volleyball = _default_client.womens_college_volleyball
womens_college_water_polo = _default_client.womens_college_water_polo
womens_olympics_basketball = _default_client.womens_olympics_basketball
womens_olympics_golf = _default_client.womens_olympics_golf
world_baseball_classic = _default_client.world_baseball_classic
wta = _default_client.wta
xfc = _default_client.xfc
xfl = _default_client.xfl

def __getattr__(name: str) -> LeagueProxy:
    """
    Fallback for dynamically requested leagues at the module level.
    Example: `espnpy.eng_1.teams()` will automatically resolve here.
    """
    return getattr(_default_client, name)

__all__ = [
    "ESPNClient",
    "league_164205",
    "league_180659",
    "league_2009",
    "league_236461",
    "league_242041",
    "league_244293",
    "league_267979",
    "league_268565",
    "league_270555",
    "league_270557",
    "league_270559",
    "league_270563",
    "league_271937",
    "league_272073",
    "league_282",
    "league_283",
    "league_289234",
    "league_289237",
    "league_289262",
    "league_289271",
    "league_289272",
    "league_289274",
    "league_289277",
    "league_289279",
    "league_3",
    "absolute",
    "afc_asian_cup",
    "afc_challenge_cup",
    "afc_champions",
    "afc_cup",
    "afc_cupq",
    "afc_saff_championship",
    "afc_w_asian_cup",
    "aff_championship",
    "affliction",
    "afl",
    "arg_1",
    "arg_2",
    "arg_3",
    "arg_4",
    "arg_copa",
    "arg_copa_de_la_superliga",
    "arg_supercopa",
    "arg_supercopa_internacional",
    "arg_trofeo_de_la_campeones",
    "atp",
    "aus_1",
    "aus_w_1",
    "aut_1",
    "bang_fighting",
    "bangabandhu_cup",
    "banni_fight",
    "banzay",
    "barracao",
    "battlezone",
    "bel_1",
    "bel_promotion_relegation",
    "bellator",
    "benevides",
    "big_fight",
    "blackout",
    "bol_1",
    "bol_copa",
    "bol_ply_rel",
    "bosnia",
    "boxe",
    "bra_1",
    "bra_2",
    "bra_3",
    "bra_camp_carioca",
    "bra_camp_gaucho",
    "bra_camp_mineiro",
    "bra_camp_paulista",
    "bra_carioca_groupa",
    "bra_carioca_groupb",
    "bra_copa_do_brazil",
    "bra_copa_do_nordeste",
    "bra_supercopa_do_brazil",
    "brazilian_freestyle",
    "budo",
    "caf_champions",
    "caf_championship",
    "caf_championship_qual",
    "caf_confed",
    "caf_cosafa",
    "caf_nations",
    "caf_nations_qual",
    "caf_w_nations",
    "cage_warriors",
    "campeones_cup",
    "can_w_nsl",
    "caribbean_series",
    "cfl",
    "champions_tour",
    "chi_1",
    "chi_1_promotion_relegation",
    "chi_2",
    "chi_copa_chi",
    "chi_super_cup",
    "chn_1",
    "chn_1_promotion_relegation",
    "club_friendly",
    "col_1",
    "col_2",
    "col_copa",
    "col_superliga",
    "college_baseball",
    "college_football",
    "college_softball",
    "concacaf_central_american_cup",
    "concacaf_champions",
    "concacaf_champions_cup",
    "concacaf_confederations_playoff",
    "concacaf_gold",
    "concacaf_gold_qual",
    "concacaf_leagues_cup",
    "concacaf_nations_league",
    "concacaf_u23",
    "concacaf_w_champions_cup",
    "concacaf_w_gold",
    "concacaf_womens_championship",
    "conmebol_america",
    "conmebol_america_femenina",
    "conmebol_libertadores",
    "conmebol_recopa",
    "conmebol_sudamericana",
    "crc_1",
    "cyp_1",
    "den_1",
    "dominican_winter_league",
    "dream",
    "ecu_1",
    "eng_1",
    "eng_2",
    "eng_3",
    "eng_4",
    "eng_5",
    "eng_charity",
    "eng_fa",
    "eng_league_cup",
    "eng_trophy",
    "eng_w_1",
    "eng_w_fa",
    "eng_w_league_cup",
    "esp_1",
    "esp_2",
    "esp_copa_de_la_reina",
    "esp_copa_del_rey",
    "esp_joan_gamper",
    "esp_super_cup",
    "esp_w_1",
    "eur",
    "euroamericana_supercopa",
    "f1",
    "fiba",
    "fifa_concacaf_olympicsq",
    "fifa_conmebol_olympicsq",
    "fifa_cwc",
    "fifa_friendly",
    "fifa_friendly_w",
    "fifa_friendly_u21",
    "fifa_intercontinental_cup",
    "fifa_intercontinental_cup",
    "fifa_intercontinental_cup_not_used",
    "fifa_olympics",
    "fifa_shebelieves",
    "fifa_w_champions_cup",
    "fifa_w_concacaf_olympicsq",
    "fifa_w_olympics",
    "fifa_wcq_ply",
    "fifa_world",
    "fifa_world_u17",
    "fifa_world_u20",
    "fifa_worldq_afc",
    "fifa_worldq_afc_conmebol",
    "fifa_worldq_caf",
    "fifa_worldq_concacaf",
    "fifa_worldq_concacaf_ofc",
    "fifa_worldq_conmebol",
    "fifa_worldq_ofc",
    "fifa_worldq_uefa",
    "fifa_wwc",
    "fifa_wwcq_ply",
    "fifa_wworld_u17",
    "fifa_wworldq_uefa",
    "fng",
    "fra_1",
    "fra_1_promotion_relegation",
    "fra_2",
    "fra_coupe_de_france",
    "fra_super_cup",
    "fra_w_1",
    "friendly_emirates_cup",
    "ger_1",
    "ger_2",
    "ger_2_promotion_relegation",
    "ger_a_bayernliganorth",
    "ger_dfb_pokal",
    "ger_playoff_relegation",
    "ger_super_cup",
    "gha_1",
    "global_arnold_clark_cup",
    "global_champs_cup",
    "global_club_challenge",
    "global_finalissima",
    "global_gulf_cup",
    "global_pinatar_cup",
    "global_toulon",
    "global_u20_intercontinental_cup",
    "global_w_finalissima",
    "global_wchamps_cup",
    "gre_1",
    "gua_1",
    "hockey_world_cup",
    "hon_1",
    "idn_1",
    "ifc",
    "ifl",
    "ind_1",
    "ind_2",
    "ir1_1_promotion_relegation",
    "irl",
    "irl_1",
    "ita_1",
    "ita_2",
    "ita_coppa_italia",
    "ita_super_cup",
    "jpn_1",
    "jpn_world_challenge",
    "k1",
    "ken_1",
    "ksa_1",
    "ksa_kings_cup",
    "ksw",
    "lfa",
    "lfc",
    "liv",
    "llb",
    "lls",
    "lpga",
    "m1",
    "mens_college_basketball",
    "mens_college_hockey",
    "mens_college_lacrosse",
    "mens_college_volleyball",
    "mens_college_water_polo",
    "mens_olympics_basketball",
    "mens_olympics_golf",
    "mex_1",
    "mex_2",
    "mex_campeon",
    "mexican_winter_league",
    "mfc",
    "mlb",
    "mys_1",
    "nascar_premier",
    "nascar_secondary",
    "nascar_truck",
    "nba",
    "nba_development",
    "nba_summer_california",
    "nba_summer_golden_state",
    "nba_summer_las_vegas",
    "nba_summer_orlando",
    "nba_summer_sacramento",
    "nba_summer_utah",
    "nbl",
    "ned_1",
    "ned_2",
    "ned_3",
    "ned_3_promotion_relegation",
    "ned_cup",
    "ned_playoff_relegation",
    "ned_supercup",
    "ned_w_1",
    "ned_w_eredivisie_cup",
    "ned_w_knvb_cup",
    "nfl",
    "nga_1",
    "nhl",
    "nll",
    "nonfifa",
    "nor_1",
    "nor_1_promotion_relegation",
    "ntw",
    "ofc",
    "olympics_baseball",
    "olympics_mens_ice_hockey",
    "olympics_womens_ice_hockey",
    "other",
    "pancrase",
    "par_1",
    "par_1_supercopa",
    "per_1",
    "pfl",
    "pga",
    "pll",
    "por_1",
    "por_1_promotion_relegation",
    "por_taca_portugal",
    "pride",
    "proelite",
    "puerto_rican_winter_league",
    "rfa",
    "rizin",
    "roc",
    "rsa_1",
    "rsa_1_promotion_relegation",
    "rsa_2",
    "rsa_mtn8",
    "rus_1",
    "rus_1_promotion_relegation",
    "sco_1",
    "sco_1_promotion_relegation",
    "sco_2",
    "sco_2_promotion_relegation",
    "sco_challenge",
    "sco_cis",
    "sco_tennents",
    "sfl",
    "sgp_1",
    "shark_fights",
    "shooto_brazil",
    "shooto_japan",
    "shoxc",
    "slv_1",
    "strikeforce",
    "swe_1",
    "swe_1_promotion_relegation",
    "tfc",
    "tgl",
    "tha_1",
    "tpf",
    "tur_1",
    "uefa_champions",
    "uefa_champions_qual",
    "uefa_euro",
    "uefa_euro_u19",
    "uefa_euro_u21",
    "uefa_euro_u21_qual",
    "uefa_europa",
    "uefa_europa_conf",
    "uefa_europa_conf_qual",
    "uefa_europa_qual",
    "uefa_euroq",
    "uefa_nations",
    "uefa_super_cup",
    "uefa_w_europa",
    "uefa_w_nations",
    "uefa_wchampions",
    "uefa_weuro",
    "ufc",
    "ufl",
    "uga_1",
    "uru_1",
    "uru_2",
    "usa_1",
    "usa_ncaa_m_1",
    "usa_ncaa_w_1",
    "usa_nwsl",
    "usa_nwsl_cup",
    "usa_nwsl_summer_cup",
    "usa_open",
    "usa_usl_1",
    "usa_usl_l1",
    "usa_usl_l1_cup",
    "usa_w_usl_1",
    "ven_1",
    "venezuelan_winter_league",
    "vfc",
    "wec",
    "wnba",
    "womens_college_basketball",
    "womens_college_field_hockey",
    "womens_college_hockey",
    "womens_college_lacrosse",
    "womens_college_volleyball",
    "womens_college_water_polo",
    "womens_olympics_basketball",
    "womens_olympics_golf",
    "world_baseball_classic",
    "wta",
    "xfc",
    "xfl",
]
