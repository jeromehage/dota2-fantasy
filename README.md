# dota2-fantasy
Trying to automate fantasy point calculations for Dota 2's DPC

Goal:
Something robust that doesn't need to be maintained every season

Done:
- Get DPC schedule by scraping the dota2.com schedule page
- Get list of players on teams with calls to dota2.com/majorsregistration
- Match player names with player_ids from open dota when possible

Todo:
- Scrape dota pro matches from dotabuff
- Download dota matches from opendota
- Update old fantasy script, run calculations

Wishlist:
- Use schedule to select best players for each week
- Take Gosugamers.net or opendota elo for team strength?
more elo: https://twitter.com/DotaDiesel, https://medium.com/@dieseldota
- Estimate mmr from distribution fit to ranks

Feedback from reddit:
- Use opendota for fantasy pts calculations
- DatDota API for pro matches
- https://www.dota2.com/webapi/IDOTA2League/GetLeaguesData/v001?league_ids=13741,13742,13712,13713,13738,13740,13709,13710,13716,13717,13747,13748
- https://github.com/VirenDias/dpc-fantasy
