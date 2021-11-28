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
- Estimate mmr from distribution fit to ranks
