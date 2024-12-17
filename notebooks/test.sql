select adv.game_id, 
adv.team_id, 
adv.player_id, 
adv.team_abbreviation,
png_ref.team_icon_path,
adv.player_name,
gl.game_date,
gl.matchup,
gl.WL,
adv.start_position,
round(cast(split_part(adv.min, ':', 1) as double) + (cast(split_part(adv.min, ':', 2) as double) / 60), 2) as min,
trad.pts, 
trad.reb, 
trad.ast, 
trad.oreb, 
trad.to, 
trad.stl, 
trad.blk, 
trad.pf,
concat(cast(trad.fgm as VARCHAR), '/', cast(trad.fga as VARCHAR)) as FG,
concat(cast(trad.fg3m as VARCHAR), '/', cast(trad.fg3a as VARCHAR)) as FG_3PT,
usg_pct, 
ts_pct, 
trad.plus_minus,
cast(trad.pts + 0.4 * trad.FGM - 0.7 * trad.FGA - 0.4*(trad.FTA - trad.FTM) + 0.7 * trad.OREB + 0.3 * trad.DREB + trad.STL + 0.7 * trad.AST + 0.7 * trad.BLK - 0.4 * trad.PF - trad.TO as double) as GS
from box_score_player_stats as adv
join trad_player_stats as trad
on adv.game_id = trad.game_id and adv.team_id = trad.team_id and adv.player_id = trad.player_id
join game_log_df as gl
on gl.team_id = adv.team_id and gl.game_id = adv.game_id
join png_ref on adv.team_id = png_ref.team_id
where adv.min is not null
order by GS desc
limit 8
