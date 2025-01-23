best_of_yesterday_prep ="""
select 
adv.game_id, 
adv.team_id, 
adv.player_id, 
adv.team_abbreviation,
adv.player_name,
gl.game_date,
gl.matchup,
gl.WL,
adv.start_position,
concat(cast(split_part(adv.min, ':', 1) as double) + (cast(split_part(adv.min, ':', 2) as double) / 60), 2) as MIN_NUMERIC,
concat(cast(split_part(adv.min, ':', 1) as int), ':', lpad(split_part(adv.min, ':', 2), 2, '0')) as MIN_STRING,
trad.pts, 
trad.reb, 
trad.ast, 
trad.oreb, 
trad.TOV, 
trad.stl, 
trad.blk, 
trad.pf,
concat(cast(trad.fgm as VARCHAR), '/', cast(trad.fga as VARCHAR)) as FG,
concat(cast(trad.fg3m as VARCHAR), '/', cast(trad.fg3a as VARCHAR)) as FG_3PT,
concat(cast(round(usg_pct * 100, 2) as string), '%') as USG_PCT, 
concat(cast(round(ts_pct * 100, 2) as string), '%') as TS_PCT,
trad.plus_minus,
cast(trad.pts + 0.4 * trad.FGM - 0.7 * trad.FGA - 0.4*(trad.FTA - trad.FTM) + 0.7 * trad.OREB + 0.3 * trad.DREB + trad.STL + 0.7 * trad.AST + 0.7 * trad.BLK - 0.4 * trad.PF - trad.TOV as double) as GS
from main.box_adv_player as adv
join main.box_trad_player as trad
on adv.game_id = trad.game_id and adv.team_id = trad.team_id and adv.player_id = trad.player_id
join main.nba_game_log as gl
on gl.team_id = adv.team_id and gl.game_id = adv.game_id
where adv.min is not null
order by GS desc
"""