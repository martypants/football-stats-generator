"""
Main aggregator module that combines data from all scrapers
"""
import pandas as pd
import logging
from datetime import datetime
from scrapers.espn_scraper import ESPNScraper
from scrapers.fbref_scraper import FBrefScraper
from scrapers.transfermarkt_scraper import TransfermarktScraper
from scrapers.understat_scraper import UnderstatScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatsAggregator:
    def __init__(self):
        self.espn = ESPNScraper()
        self.fbref = FBrefScraper()
        self.transfermarkt = TransfermarktScraper()
        self.understat = UnderstatScraper()
        self.aggregated_data = []
    
    def aggregate_player_stats(self, player_name, team_name):
        """
        Aggregate player stats from all sources
        """
        logger.info(f"Aggregating stats for {player_name}")
        
        espn_stats = self.espn.scrape_player_stats(player_name)
        fbref_stats = self.fbref.scrape_player_stats(player_name)
        transfermarkt_stats = self.transfermarkt.scrape_player_stats(player_name, team_name)
        
        # Combine all stats
        combined_stats = {
            "player_name": player_name,
            "team_name": team_name,
            "timestamp": datetime.now().isoformat(),
            "sources": ["ESPN", "FBref", "Transfermarkt"],
            "stats": {
                "espn": espn_stats,
                "fbref": fbref_stats,
                "transfermarkt": transfermarkt_stats
            }
        }
        
        self.aggregated_data.append(combined_stats)
        return combined_stats
    
    def aggregate_team_stats(self, team_name, league="champions-league"):
        """
        Aggregate team stats from all sources
        """
        logger.info(f"Aggregating team stats for {team_name}")
        
        espn_stats = self.espn.scrape_team_stats(team_name, league)
        fbref_stats = self.fbref.scrape_team_season_stats(team_name)
        understat_stats = self.understat.scrape_team_stats(team_name, league)
        
        combined_stats = {
            "team_name": team_name,
            "league": league,
            "timestamp": datetime.now().isoformat(),
            "sources": ["ESPN", "FBref", "Understat"],
            "stats": {
                "espn": espn_stats,
                "fbref": fbref_stats,
                "understat": understat_stats
            }
        }
        
        self.aggregated_data.append(combined_stats)
        return combined_stats
    
    def aggregate_match_stats(self, team1, team2, league="champions-league"):
        """
        Aggregate match statistics between two teams
        """
        logger.info(f"Aggregating match stats: {team1} vs {team2}")
        
        understat_stats = self.understat.scrape_match_stats(team1, team2, league)
        
        combined_stats = {
            "team1": team1,
            "team2": team2,
            "league": league,
            "timestamp": datetime.now().isoformat(),
            "sources": ["Understat"],
            "stats": {
                "understat": understat_stats
            }
        }
        
        self.aggregated_data.append(combined_stats)
        return combined_stats
    
    def export_to_csv(self, filename="football_stats.csv"):
        """
        Export aggregated data to CSV file
        """
        try:
            # Flatten the data for CSV export
            flattened_data = []
            for data in self.aggregated_data:
                flattened_data.append(data)
            
            df = pd.DataFrame(flattened_data)
            df.to_csv(filename, index=False)
            logger.info(f"Data exported successfully to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return None
    
    def get_aggregated_data(self):
        """
        Get all aggregated data
        """
        return self.aggregated_data